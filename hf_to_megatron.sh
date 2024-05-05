# python weights_conversion/hf_to_megatron.py llama2 --size=7 \
# 	--out=/pure-mlo-scratch/make_project/spring2024/trial-runs/meditron-7B-BHC-v2/megatron_500-extend \
#   --model-path=/pure-mlo-scratch/make_project/spring2024/trial-runs/meditron-7B-BHC-v2/hf_checkpoint_500-extend \

python weights_conversion/hf_to_megatron.py llama3 --size 8 --model-path /pure-mlo-scratch/trial-runs/meta-llama-3-8B/models--meta-llama--Llama-3-8B-hf/snapshots/1460c22666392e470910ce3d44ffeb2ab7dbd4df \
    --out /pure-mlo-scratch/trial-runs/meta-llama-3-8B/megatron_check \
    --cache-dir /pure-mlo-scratch/trial-runs/meta-llama-3-8B \


