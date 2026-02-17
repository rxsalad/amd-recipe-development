import os
import csv
from bson import json_util, ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()


username     = os.getenv("MDB_USERNAME", "")
password     = os.getenv("MDB_PASSWORD", "")
host         = os.getenv("MDB_HOST", "")
database     = os.getenv("MDB_DATABASE", "") 
benchmark_db = os.getenv("MDB_BENCHMARK_DB", "")


# Build connection URI and Connect to MongoDB
uri = f"mongodb+srv://{username}:{password}@{host}/?tls=true&authSource={database}&retryWrites=true&w=majority"
mongo_db_client = MongoClient(uri)


print("⚠️  Be careful: This will DROP all collections in the benchmark database!")
cmd = input("Continue? yes - drop all, others - exit: ").strip().lower()
if cmd != "yes":
    os._exit(0)

# Connect to the benchmark database
db = mongo_db_client[benchmark_db]

# List all collections
collections = db.list_collection_names()
print("Collections before drop:", collections)

# Drop each collection
for col_name in collections:
    db[col_name].drop()
    print(f"Dropped collection: {col_name}")

# Task metadata
# Optional: keep the metadata of each task, and task_id of each task should be unique
tasks = db["tasks"]
tasks.create_index( [("task_id", 1) ], unique=True )
tasks.create_index( [("timestamp", 1) ] ) # Single field index, ascending order

# Results — test data is usually consistent per task, but consistency is not required.
results = db["results"]
results.create_index( [("task_id",1), ("timestamp",1)] ) # Compound index, ascending order

# Verify
print("Collections after drop:", db.list_collection_names())

