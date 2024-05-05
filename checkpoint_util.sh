python tools/checkpoint_util_new.py \
	--target_tensor_parallel_size 4 \
	--target_pipeline_parallel_size 1 \
	--load_dir /pure-mlo-scratch/make_project/spring2024/trial-runs/meditron-7B-BHC-v2/megatron_500-extend \
	--save_dir /pure-mlo-scratch/make_project/spring2024/trial-runs/meditron-7B-BHC-v2/ \
	--model_type llama2 \
	--true_vocab_size 32019 \
	--bf16