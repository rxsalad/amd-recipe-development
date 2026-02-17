import subprocess
import requests
import time
import csv


def load_test_cases_from_csv(csv_file, base_url="", model=""):
    test_cases = []
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f, skipinitialspace=True)

        try:
            for row in reader:
                # Clean up empty strings like "" → ""
                cleaned_row = {k.strip(): v.strip().strip('"') for k, v in row.items()}
        
                # Convert numeric fields
                cleaned_row["random-input-len"] = int(cleaned_row["random-input-len"])
                cleaned_row["random-output-len"] = int(cleaned_row["random-output-len"])
                cleaned_row["request-rate"] = int(cleaned_row["request-rate"])
                cleaned_row["num-prompts"] = int(cleaned_row["num-prompts"])
        
                if base_url:
                    cleaned_row["base-url"] = base_url
                if model:
                    cleaned_row["model"] = model
                test_cases.append(cleaned_row)
        except Exception as e:
            print(f"Error reading CSV file: {e}", flush=True)
            time.sleep(999999) # Need troubleshooting

    return test_cases


def check_vllm_ready(HEALTH_ENDPOINT):
    RETRY_INTERVAL = 10  
    MAX_RETRIES = 5      

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(HEALTH_ENDPOINT, timeout=2)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass  # server not ready yet

        print(f"\n!!!!!! Attempt {attempt}: vLLM server not ready, retrying in {RETRY_INTERVAL}s...", flush=True)
        time.sleep(RETRY_INTERVAL)

    print("\n!!!!!! vLLM server did not become ready within the timeout period.", flush=True)
    return False


def run_benchmark(base_url, model, random_input_len, random_output_len, request_rate, num_prompts, temp_file):

    cmd = [
        "vllm", "bench", "serve",
        "--base-url", str(base_url),
        "--model", str(model),
        "--dataset-name", "random",
        "--random-input-len", str(random_input_len),
        "--random-output-len", str(random_output_len),
        "--request-rate", str(request_rate),
        "--num-prompts", str(num_prompts),
        "--ignore-eos",
        "--trust-remote-code",
        "--save-result",
        "--result-dir", ".",
        "--result-filename", str(temp_file),
    ]

    print("\n" + "-" * 40 + "> Running:")
    print(" ".join(cmd), flush=True)

    result = subprocess.run(cmd, capture_output=True,text=True)

    if result.returncode != 0:
        print("\n" + "-" * 40 + "> Benchmark Failed:")
        print(result.stderr, flush=True)
        return False

    print("\n" + "-" * 40 + "> Benchmark completed:")
    print(result.stdout, flush=True)
    return True