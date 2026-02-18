# Progress

Made [amd/DeepSeek-R1-MXFP4](https://huggingface.co/amd/DeepSeek-R1-MXFP4) work with vLLM by following [this discussion](https://github.com/ROCm/aiter/issues/1468).

Tested 2 images on the same MI350x8 node, one at a time. Some paramaters in the vLLM dev are not supported in the vLLM latest:

- vLLM dev: [docker.io/rocm/vllm-dev:dsfp4_1120](https://hub.docker.com/layers/rocm/vllm-dev/dsfp4_1120/images/sha256-deefdb324c7f04a96d852d6924788bf0d31e9a6ad91b508b2865051e48bcd2e1)

- vLLM latest - [docker.io/vllm/vllm-openai-rocm:v0.15.1](https://hub.docker.com/layers/vllm/vllm-openai-rocm/v0.15.1/images/sha256-4c7fbd92fe07e4dab956d283b5d61b971f6242516647df6af06fdcbc34fddc2c) 

There are a lot of flags to run the vLLM server, and it will take some time to digest them all.

Initial benchmarks indicate that performance is within the expected range, and the vLLM dev appears to offer significant performance improvements (over 100%) while also supporting additional parameters.
