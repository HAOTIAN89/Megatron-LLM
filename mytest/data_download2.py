import json
import tqdm
from datasets import load_dataset

# the `cache_dir` is optional
dataset = load_dataset("Open-Orca/OpenOrca", cache_dir="/path/to/cache", split="train")
with open("/path/to/raw/data.jsonl", "w+") as f:
    for document in tqdm(dataset):
        if document["id"].startswith("cot."):
            f.write(json.dumps(document) + "\n")