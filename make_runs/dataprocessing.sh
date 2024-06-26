echo "Init"
python /home/haotian/Megatron-LLM/tools/preprocess_instruct_data.py --input=/pure-mlo-scratch/make_project/spring2024/data/raw/version6.0/DI_valid_dataset_v6_6k.jsonl \
    --output_prefix=/pure-mlo-scratch/make_project/spring2024/data/tokenized/di-6k-v6-val \
    --tokenizer_type=SentencePieceTokenizer \
    --vocab_file=/pure-mlo-scratch/llama/tokenizer.model \
    --chunk_size=32 --workers=32 \
    --vocab_extra_ids_list "[bib_ref],[/bib_ref],[fig_ref],[/fig_ref],[bib],[/bib],[fig],[/fig],[table],[/table],[formula],[/formula],<|im_start|>,<|im_end|>" \
    --question_key='prompt' \
    --answer_key='reference' 
echo "End"

# Besides that, remember to change the wandb account by wandb login --relogin and export WANDB_API_KEY=<project_key>