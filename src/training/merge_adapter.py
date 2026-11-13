"""Script to merge LoRA adapter weights into base model and export standalone weights."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

logger = logging.getLogger("merge_adapter")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def merge_and_save(
    base_model_name: str,
    adapter_path: str,
    output_path: str,
    device: str = "cpu",
) -> None:
    """Merge LoRA adapter into base model and write to disk."""
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    logger.info("Loading base model: %s", base_model_name)
    dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float32

    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=dtype,
        device_map=device if device != "cpu" else None,
        trust_remote_code=True,
    )

    logger.info("Loading adapter from: %s", adapter_path)
    model = PeftModel.from_pretrained(base_model, adapter_path)

    logger.info("Merging adapter into base model weights...")
    merged_model = model.merge_and_unload()

    logger.info("Saving merged model to: %s", output_path)
    Path(output_path).mkdir(parents=True, exist_ok=True)
    merged_model.save_pretrained(output_path)

    logger.info("Saving tokenizer to: %s", output_path)
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    tokenizer.save_pretrained(output_path)

    logger.info("Successfully merged and saved model to %s", output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge LoRA adapter weights into base model")
    parser.add_argument(
        "--base-model",
        default="Qwen/Qwen2.5-Coder-7B-Instruct",
        help="Base model identifier or path",
    )
    parser.add_argument(
        "--adapter-path",
        default="./outputs/final_adapter",
        help="Path to trained LoRA adapter directory",
    )
    parser.add_argument(
        "--output-path",
        default="./outputs/merged_model",
        help="Destination directory for merged weights",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Device to perform merge on (cpu, cuda, rocm)",
    )

    args = parser.parse_args()
    merge_and_save(
        base_model_name=args.base_model,
        adapter_path=args.adapter_path,
        output_path=args.output_path,
        device=args.device,
    )


if __name__ == "__main__":
    main()

