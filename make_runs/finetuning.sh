python /home/haotian/Megatron-LLM/make_scripts/do_finetuning.py --checkpoint=meditron \
    --size 7 \
    --run_name=bhc-2k \
    --data /pure-mlo-scratch/make_project/spring2024/data/raw/BHC_train_dataset.jsonl \
    --val /pure-mlo-scratch/make_project/spring2024/data/raw/BHC_valid_dataset.jsonl \
    --micro_batch=8 \
    --save_interval=500 || exit 1