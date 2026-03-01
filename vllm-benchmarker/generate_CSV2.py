import csv

# CSV file path
csv_file = "test_cases_temp.csv"

# Common values
random_input_len = 256
random_output_len = 256
request_rate = 10000

# base_url = "http://mi325-vllm-0151.default.svc.cluster.local:80"

base_url0 = "http://llama-vllm0.default.svc.cluster.local:80"
base_url1 = "http://llama-vllm1.default.svc.cluster.local:80"
base_url2 = "http://llama-vllm2.default.svc.cluster.local:80"
base_url3 = "http://llama-vllm3.default.svc.cluster.local:80"
base_url4 = "http://llama-vllm4.default.svc.cluster.local:80"
base_url5 = "http://llama-vllm5.default.svc.cluster.local:80"
base_url6 = "http://llama-vllm6.default.svc.cluster.local:80"
base_url7 = "http://llama-vllm7.default.svc.cluster.local:80"



# Open CSV file for writing
with open(csv_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    
    # Write header
    writer.writerow(["random-input-len", "random-output-len", "request-rate", "num-prompts", "base-url", "model"])
    
    # Write 1–40 rows
    for num_prompts in range(1, 41):
        writer.writerow([random_input_len, random_output_len, request_rate, num_prompts, base_url0, ""])
        writer.writerow([random_input_len, random_output_len, request_rate, num_prompts, base_url1, ""])
        writer.writerow([random_input_len, random_output_len, request_rate, num_prompts, base_url2, ""])
        writer.writerow([random_input_len, random_output_len, request_rate, num_prompts, base_url3, ""])
        writer.writerow([random_input_len, random_output_len, request_rate, num_prompts, base_url4, ""])
        writer.writerow([random_input_len, random_output_len, request_rate, num_prompts, base_url5, ""])
        writer.writerow([random_input_len, random_output_len, request_rate, num_prompts, base_url6, ""])
        writer.writerow([random_input_len, random_output_len, request_rate, num_prompts, base_url7, ""])

print(f"CSV file '{csv_file}' generated successfully.")