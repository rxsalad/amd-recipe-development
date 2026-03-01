import csv

# CSV file path
csv_file = "test_cases_temp.csv"

# Common values
random_input_len = 1024
random_output_len = 1024
request_rate = 10000

# base_url = "http://mi325-vllm-0151.default.svc.cluster.local:80"

base_url0 = "http://vllm-8000.default.svc.cluster.local:80"
base_url1 = "http://vllm-8001.default.svc.cluster.local:80"


# Open CSV file for writing
with open(csv_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    
    # Write header
    writer.writerow(["random-input-len", "random-output-len", "request-rate", "num-prompts", "base-url", "model"])
    
    # Write 1–40 rows
    for num_prompts in range(1, 41):
        writer.writerow([random_input_len, random_output_len, request_rate, num_prompts, base_url0, ""])
        writer.writerow([random_input_len, random_output_len, request_rate, num_prompts, base_url1, ""])

print(f"CSV file '{csv_file}' generated successfully.")