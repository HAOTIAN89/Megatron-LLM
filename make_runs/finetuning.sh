python /home/haotian/Megatron-LLM/make_scripts/do_finetuning.py --checkpoint=meditron \
    --size 7 \
    --run_name=bhc-6k-v6 \
    --data /pure-mlo-scratch/make_project/spring2024/data/raw/version6.0/BHC_train_dataset_v6_6k_filtered.jsonl \
    --val /pure-mlo-scratch/make_project/spring2024/data/raw/version6.0/BHC_valid_dataset_v6_6k_filtered.jsonl \
    --micro_batch=2 \
    --save_interval=400 || exit 1