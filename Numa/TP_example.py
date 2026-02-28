import torch
import torch.nn as nn
import torch.distributed as dist

# -------------------------------
# Setup devices (2 GPUs)
# -------------------------------
device0 = torch.device("cuda:0")
device1 = torch.device("cuda:1")

# -------------------------------
# Model dimensions
# -------------------------------
batch_size = 4
input_size = 8
hidden_size = 8
output_size = 8

# Split output across 2 GPUs (tensor parallel along output dimension)
half_hidden = hidden_size // 2
half_output = output_size // 2

# -------------------------------
# Layer 1 weights (CPU -> GPU)
# -------------------------------
weight1_0 = nn.Parameter(torch.randn(input_size, half_hidden))
weight1_1 = nn.Parameter(torch.randn(input_size, half_hidden))
bias1_0 = nn.Parameter(torch.randn(half_hidden))
bias1_1 = nn.Parameter(torch.randn(half_hidden))

weight1_0 = weight1_0.to(device0)
bias1_0 = bias1_0.to(device0)
weight1_1 = weight1_1.to(device1)
bias1_1 = bias1_1.to(device1)

# -------------------------------
# Layer 2 weights (CPU -> GPU)
# -------------------------------
weight2_0 = nn.Parameter(torch.randn(hidden_size, half_output))
weight2_1 = nn.Parameter(torch.randn(hidden_size, half_output))
bias2_0 = nn.Parameter(torch.randn(half_output))
bias2_1 = nn.Parameter(torch.randn(half_output))

weight2_0 = weight2_0.to(device0)
bias2_0 = bias2_0.to(device0)
weight2_1 = weight2_1.to(device1)
bias2_1 = bias2_1.to(device1)

# -------------------------------
# Input tensor on CPU
# -------------------------------
x = torch.randn(batch_size, input_size)

# Move input to both GPUs for Layer 1
x0 = x.to(device0)
x1 = x.to(device1)

# -------------------------------
# Forward pass: Layer 1 (tensor parallel)
# -------------------------------
out1_0 = x0 @ weight1_0 + bias1_0  # GPU0 partial output
out1_1 = x1 @ weight1_1 + bias1_1  # GPU1 partial output

# ---------------------------------------
# Collective Communication (*** All-Gather ***) for Layer 2 input
# ---------------------------------------
# Each GPU computes a slice of Layer 1 output.
# If Layer 2 needs the full input, we must gather all partial outputs across GPUs.
# In real distributed setup, this would use:
# dist.all_gather(out_list, out_local)
# Here we simulate it manually with torch.cat:
full_input_layer2 = torch.cat([out1_0, out1_1.to(device0)], dim=1)  # now full input on GPU0

# -------------------------------
# Forward pass: Layer 2 (tensor parallel)
# -------------------------------
# Split full input to both GPUs for Layer 2
input2_0 = full_input_layer2.to(device0) # PyTorch is smart here: it doesn’t actually move the data, it just returns a view of the same tensor.
input2_1 = full_input_layer2.to(device1)

out2_0 = input2_0 @ weight2_0 + bias2_0  # GPU0 partial output
out2_1 = input2_1 @ weight2_1 + bias2_1  # GPU1 partial output

# ---------------------------------------
# Collective Communication (All-Gather) for final output
# ---------------------------------------
# To get the full output, gather partial outputs from all GPUs
# In real distributed setup: dist.all_gather(final_list, out2_local)
final_out = torch.cat([out2_0, out2_1.to(device0)], dim=1)

print(final_out)