python3 /home/haotian/Megatron-LLM/tools/preprocess_data.py \
    --input=/pure-mlo-scratch/data/raw_data/meditron_mega/meditron_mega_val.jsonl \
    --output_prefix=/pure-mlo-scratch/data/tokenized/meditron-mega-train/meditron-mega-validation-tiktok \
    --dataset_impl=mmap \
    --tokenizer_type=TiktokenTokenizer \
    --vocab_file=/pure-mlo-scratch/trial-runs/meta-llama-3-8b/models--meta-llama--Llama-3-8B-hf/snapshots/1460c22666392e470910ce3d44ffeb2ab7dbd4df/tokenizer.model \
    --workers=32 \
    --chunk_size=32 \