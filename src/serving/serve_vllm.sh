#!/usr/bin/env bash
# Ask Your Database — vLLM Serving Launch Script (ROCm / CUDA compatible)
set -euo pipefail

MODEL="${VLLM_MODEL:-./outputs/final_adapter}"
PORT="${VLLM_PORT:-8080}"
HOST="${VLLM_HOST:-0.0.0.0}"
MAX_MODEL_LEN="${VLLM_MAX_MODEL_LEN:-4096}"
GPU_MEMORY_UTILIZATION="${VLLM_GPU_MEMORY_UTILIZATION:-0.90}"
DTYPE="${VLLM_DTYPE:-bfloat16}"

echo "=========================================================="
echo " Starting vLLM OpenAI-Compatible Server"
echo " Model:                   ${MODEL}"
echo " Endpoint:                http://${HOST}:${PORT}/v1"
echo " Dtype:                   ${DTYPE}"
echo " Max Context Length:      ${MAX_MODEL_LEN}"
echo " GPU Memory Utilization:  ${GPU_MEMORY_UTILIZATION}"
echo "=========================================================="

exec python -m vllm.entrypoints.openai.api_server \
    --model "${MODEL}" \
    --host "${HOST}" \
    --port "${PORT}" \
    --dtype "${DTYPE}" \
    --max-model-len "${MAX_MODEL_LEN}" \
    --gpu-memory-utilization "${GPU_MEMORY_UTILIZATION}" \
    --trust-remote-code

