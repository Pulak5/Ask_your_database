"""LoRA fine-tuning script for text-to-SQL using SFTTrainer.

Usage:
    python -m src.training.train_lora --config src/training/configs/lora_config.yaml
    python -m src.training.train_lora --config src/training/configs/lora_config.yaml --resume-from-checkpoint outputs/checkpoint-100
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import yaml


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def build_formatting_func(tokenizer):
    """Return a formatting function that extracts the completion portion."""
    def formatting_func(examples):
        outputs = []
        for prompt, completion in zip(examples["prompt"], examples["completion"]):
            outputs.append(prompt + completion)
        return outputs
    return formatting_func


def main():
    parser = argparse.ArgumentParser(description="LoRA fine-tuning for text-to-SQL.")
    parser.add_argument("--config", default="src/training/configs/lora_config.yaml")
    parser.add_argument("--resume-from-checkpoint", default=None, type=str)
    parser.add_argument("--wandb-project", default=None)
    parser.add_argument("--no-wandb", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)

    model_name: str = cfg["model_name"]
    output_dir: str = cfg["output_dir"]
    lora_cfg: dict = cfg["lora"]
    train_cfg: dict = cfg["training"]
    data_cfg: dict = cfg["data"]

    # Logging setup
    if args.no_wandb:
        os.environ["WANDB_DISABLED"] = "true"
        report_to = "tensorboard"
    elif args.wandb_project:
        os.environ["WANDB_PROJECT"] = args.wandb_project
        report_to = "wandb"
    else:
        report_to = "tensorboard"

    # Lazy imports (require GPU environment)
    import torch
    from datasets import load_dataset
    from peft import LoraConfig, TaskType
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        TrainingArguments,
    )
    from trl import DataCollatorForCompletionOnlyLM, SFTTrainer

    print(f"Loading tokenizer from {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    print(f"Loading model from {model_name}...")
    dtype = torch.bfloat16 if train_cfg.get("bf16", True) else torch.float16

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=dtype,
        device_map="auto",
        trust_remote_code=True,
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # LoRA config
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=lora_cfg["rank"],
        lora_alpha=lora_cfg["alpha"],
        lora_dropout=lora_cfg["dropout"],
        target_modules=lora_cfg["target_modules"],
        bias="none",
    )

    # Load datasets
    print(f"Loading training data from {data_cfg['train_file']}...")
    dataset = load_dataset(
        "json",
        data_files={
            "train": data_cfg["train_file"],
            "validation": data_cfg["val_file"],
        },
    )

    # DataCollator: train only on completions
    # The response template marks the beginning of the SQL completion
    response_template = "### SQL:\n"
    collator = DataCollatorForCompletionOnlyLM(
        response_template=response_template,
        tokenizer=tokenizer,
    )

    formatting_func = build_formatting_func(tokenizer)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=train_cfg["num_epochs"],
        per_device_train_batch_size=train_cfg["per_device_train_batch_size"],
        per_device_eval_batch_size=train_cfg.get("per_device_eval_batch_size", 4),
        gradient_accumulation_steps=train_cfg["gradient_accumulation_steps"],
        learning_rate=train_cfg["learning_rate"],
        warmup_ratio=train_cfg["warmup_ratio"],
        lr_scheduler_type=train_cfg["lr_scheduler_type"],
        bf16=train_cfg.get("bf16", True),
        fp16=not train_cfg.get("bf16", True),
        logging_steps=train_cfg["logging_steps"],
        save_steps=train_cfg["save_steps"],
        eval_steps=train_cfg["eval_steps"],
        evaluation_strategy="steps",
        save_strategy="steps",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to=report_to,
        run_name=f"text2sql-lora-{Path(output_dir).name}",
        seed=train_cfg.get("seed", 42),
        dataloader_pin_memory=True,
    )

    # Trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        peft_config=peft_config,
        formatting_func=formatting_func,
        data_collator=collator,
        max_seq_length=train_cfg["max_length"],
        tokenizer=tokenizer,
    )

    print("Starting training...")
    resume = args.resume_from_checkpoint
    trainer.train(resume_from_checkpoint=resume)

    print(f"Saving adapter to {output_dir}/final_adapter...")
    trainer.model.save_pretrained(f"{output_dir}/final_adapter")
    tokenizer.save_pretrained(f"{output_dir}/final_adapter")

    # Save training metrics
    metrics = trainer.evaluate()
    print(f"Final eval metrics: {json.dumps(metrics, indent=2)}")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    (Path(output_dir) / "eval_metrics.json").write_text(json.dumps(metrics, indent=2))

    print("✅ Training complete.")


if __name__ == "__main__":
    main()
