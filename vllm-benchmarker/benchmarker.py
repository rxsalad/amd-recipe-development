import os
import time
import json
from pymongo import MongoClient
from datetime import datetime, timezone
from zoneinfo import ZoneInfo 
from helper import check_vllm_ready, run_benchmark, load_test_cases_from_csv
from dotenv import load_dotenv
load_dotenv()

username     = os.getenv("MDB_USERNAME", "")
password     = os.getenv("MDB_PASSWORD", "")
host         = os.getenv("MDB_HOST", "")
database     = os.getenv("MDB_DATABASE", "")      # The database that stores the user credentials
benchmark_db = os.getenv("MDB_BENCHMARK_DB", "")  # The database that stores the benchmark results

task_id     = os.getenv("TASK_ID", "")
others      = os.getenv("OTHERS", "")
base_url    = os.getenv("BASE_URL", "")
model       = os.getenv("MODEL", "")

temp_file = "./temp.json"

# Build connection URI and Connect to MongoDB
uri = f"mongodb+srv://{username}:{password}@{host}/?tls=true&authSource={database}&retryWrites=true&w=majority"
mongo_db_client = MongoClient(uri)


try:
    db = mongo_db_client[benchmark_db]
    temp = db.command("ping") # should return {'ok': 1.0} if successful
    print("\nConnected to MongoDB successfully!", flush=True)
except Exception as e:
    print(f"\nError connecting to MongoDB: {e}", flush=True)
    time.sleep(999999) # Need troubleshooting
    

csv_file  = f"./test_cases_default.csv"
csv_file_injected = f"./test_cases.csv"
if os.path.isfile(csv_file_injected): # Check if file exists
    csv_file = csv_file_injected
    print(f"\nUsing injected test cases from {csv_file_injected}", flush=True)
else:
    print(f"\nUsing default test cases from {csv_file}", flush=True)


test_cases = load_test_cases_from_csv(csv_file, base_url, model)
if len(test_cases) == 0:
    print("\nNo test cases found in the CSV file.", flush=True)
    time.sleep(999999) # Need troubleshooting


for test_case in test_cases:
    print("\n" + "-" * 40 + "> Test Case:", flush=True)
    print(test_case, flush=True)

    HEALTH_ENDPOINT = test_case['base-url'] + "/health" 
    if not check_vllm_ready(HEALTH_ENDPOINT):
        print("\n!!!!!! Skipping test case due to vLLM server not being ready.", flush=True)
        continue
    
    temp = run_benchmark(test_case['base-url'], test_case['model'], test_case['random-input-len'], test_case['random-output-len'], test_case['request-rate'], test_case['num-prompts'], temp_file)

    if not temp:
        print("\n!!!!!! Skipping result insertion due to benchmark failure.", flush=True)
        continue
    else:
        try:
            with open(temp_file, 'r') as f:
                result_data = json.load(f)
                print("\n" + "-" * 40 + "> Test Result:", flush=True)

                result_data["task_id"]   = task_id
                result_data["timestamp"] = datetime.now(timezone.utc)     
                result_data["date"]      = str(datetime.now(ZoneInfo("America/Los_Angeles")).date())
                result_data["base_url"]  = test_case['base-url']
                result_data["others"]    = others

                print(result_data, flush=True)

                db = mongo_db_client[benchmark_db]
                results = db["results"]
                result = results.insert_one(result_data)
                print("Inserted document ID:", result.inserted_id, flush=True)

        except Exception as e:
            print(f"\n!!!!!! Error inserting result into MongoDB: {e}", flush=True)
            time.sleep(999999) # Need troubleshooting


print("\n" + "-" * 40 + "> Test completed", flush=True)
time.sleep(999999) # Completed

