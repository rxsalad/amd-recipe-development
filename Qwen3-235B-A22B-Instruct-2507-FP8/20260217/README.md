# Progress

Two vLLM images were tested with [Qwen/Qwen3-235B-A22B-Instruct-2507-FP8](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507-FP8) under identical conditions, including the same MI325x8 node, with 4 GPUs allocated per each and excuteded sequentially.

- vllm-0.11.1 - [docker.io/rocm/vllm:rocm7.0.0_vllm_0.11.1_20251103](https://hub.docker.com/layers/rocm/vllm/rocm7.0.0_vllm_0.11.1_20251103/images/sha256-8d60429043d4d00958da46039a1de0d9b82df814d45da482497eef26a6076506)
- vllm-0.15.1 - [docker.io/vllm/vllm-openai-rocm:v0.15.1](https://hub.docker.com/layers/vllm/vllm-openai-rocm/v0.15.1/images/sha256-4c7fbd92fe07e4dab956d283b5d61b971f6242516647df6af06fdcbc34fddc2c)

Initial benchmarks indicate that vllm-0.15.1 outperforms vllm-0.11.1 in all apsects.

