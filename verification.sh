# arguments required by `torchrun`
DISTRIBUTED_ARGS="--nproc_per_node 1 --nnodes 1 --node_rank 0 --master_addr localhost --master_port 8000"
LLAMA_ARGS="--use_rms_norm --glu_activation swiglu --no_tie_embed_logits --no_new_tokens --layernorm_epsilon 1e-5"
COMMON_ARGS="--hidden_dropout 0.0 --attention_dropout 0.0 --no_bias_gelu_fusion"

torchrun $DISTRIBUTED_ARGS verify_correctness.py \
	--model_name=llama3 \
	--model_size=8 \
	--load=/pure-mlo-scratch/trial-runs/meta-llama-3-8b/megatron \
	--data_path=/pure-mlo-scratch/data/tokenized/meditron-mega-train/meditron-mega-validation-tiktok_text_document \
	--tokenizer_type=TiktokenTokenizer \
	--vocab_file=/pure-mlo-scratch/trial-runs/meta-llama-3-8b/models--meta-llama--Meta-Llama-3-8B/snapshots/1460c22666392e470910ce3d44ffeb2ab7dbd4df/tokenizer.model \
	--huggingface_cache=/pure-mlo-scratch/trial-runs/meta-llama-3-8b \
	--huggingface_device=cuda:1 \
	$COMMON_ARGS $LLAMA_ARGS  # dont include LLAMA_ARGS if using Falcon