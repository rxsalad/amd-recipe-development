import torch
import torch.nn as nn

# Check GPUs
device0 = torch.device("cuda:0")
device1 = torch.device("cuda:1")

# Input batch size and hidden size
batch_size = 4
input_size = 8
output_size = 8

# Split output across 2 GPUs (tensor parallelism along output dim)
half_output = output_size // 2

# --- Create all weights and biases in CPU memory first ---
weight0 = nn.Parameter(torch.randn(input_size, half_output))
weight1 = nn.Parameter(torch.randn(input_size, half_output))
bias0 = nn.Parameter(torch.randn(half_output))
bias1 = nn.Parameter(torch.randn(half_output))

# --- Load model weights (large data) to respective GPUs ---
# CPU -> GPU transfers occur over PCIe (within a single NUMA node or cross 2 NUMA nodes), typically done once at model load
weight0 = weight0.to(device0)
bias0 = bias0.to(device0)

weight1 = weight1.to(device1)
bias1 = bias1.to(device1)

# --- Create input tensor in CPU memory ---
x = torch.randn(batch_size, input_size)

# Transfer it to both GPUs over PCIe (within a single NUMA node or cross 2 NUMA nodes), done per inference batch
x0 = x.to(device0)
x1 = x.to(device1) 

# --- Forward pass ---
# Only a kernel launch command is sent from CPU; the GPU already has the data, model weights, and kernels in its memory
out0 = x0 @ weight0 + bias0  # Partial output on GPU0
out1 = x1 @ weight1 + bias1  # Partial output on GPU1

# Concatenate partial outputs on GPU0
# The GPU-GPU copy (out1 -> GPU0) occurs via NVLink/XGMI if available, else PCIe

out = torch.cat([out0, out1.to(device0)], dim=1)

# Transfer final output back to CPU for further processing or evaluation
print(out.cpu())