import json
from datasets import load_dataset

dataset = load_dataset("bigcode/starcoderdata", data_dir="julia", split="train", cache_dir="/path/to/cache/")

with open("/path/to/raw.jsonl", "w+") as f:
    for document in dataset:
        document = {"id": document['id'], "text": document['content']}
        f.write(json.dumps(document) + "\n")