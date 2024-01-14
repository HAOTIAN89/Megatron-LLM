echo "Init"
# python ../weights_conversion/megatron_to_hf.py --input_dir=/pure-mlo-scratch/make_project/trial-runs/meditron-7b-direct/llama-2-7b-tp1-pp1-meditron-direct --output_dir=/pure-mlo-scratch/make_project/trial-runs/meditron-7b-direct/hf_checkpoint_new --vocab_extra_ids_list="[bib_ref],[/bib_ref],[fig_ref],[/fig_ref],[bib],[/bib],[fig],[/fig],[table],[/table],[formula],[/formula],<|im_start|>,<|im_end|>" --override_special_tokens='bos=<|im_start|>','eos=<|im_end|>'
# python ../weights_conversion/megatron_to_hf.py --input_dir=/pure-mlo-scratch/make_project/trial-runs/meditron-7b-direct-trunc/llama-2-7b-tp1-pp1-meditron-direct-trunc --output_dir=/pure-mlo-scratch/make_project/trial-runs/meditron-7b-direct-trunc/hf_checkpoint_new --vocab_extra_ids_list="[bib_ref],[/bib_ref],[fig_ref],[/fig_ref],[bib],[/bib],[fig],[/fig],[table],[/table],[formula],[/formula],<|im_start|>,<|im_end|>" --override_special_tokens='bos=<|im_start|>','eos=<|im_end|>'
# python ../weights_conversion/megatron_to_hf.py --input_dir=/pure-mlo-scratch/make_project/trial-runs/meditron-7b-generator/llama-2-7b-tp1-pp1-meditron-generator1 --output_dir=/pure-mlo-scratch/make_project/trial-runs/meditron-7b-generator/hf_checkpoint_new --vocab_extra_ids_list="[bib_ref],[/bib_ref],[fig_ref],[/fig_ref],[bib],[/bib],[fig],[/fig],[table],[/table],[formula],[/formula],<|im_start|>,<|im_end|>" --override_special_tokens='bos=<|im_start|>','eos=<|im_end|>'
# python ../weights_conversion/megatron_to_hf.py --input_dir=/pure-mlo-scratch/make_project/trial-runs/meditron-7b-summarizer/llama-2-7b-tp1-pp1-meditron-summarizer --output_dir=/pure-mlo-scratch/make_project/trial-runs/meditron-7b-summarizer/hf_checkpoint_new --vocab_extra_ids_list="[bib_ref],[/bib_ref],[fig_ref],[/fig_ref],[bib],[/bib],[fig],[/fig],[table],[/table],[formula],[/formula],<|im_start|>,<|im_end|>" --override_special_tokens='bos=<|im_start|>','eos=<|im_end|>'
# python ../weights_conversion/megatron_to_hf.py --input_dir=/pure-mlo-scratch/make_project/trial-runs/pubmed-13b-direct-trunc/llama-2-13b-tp1-pp1-ex1pubmedreplay-direct-trunc --output_dir=/pure-mlo-scratch/make_project/trial-runs/pubmed-13b-direct-trunc/hf_checkpoint_new --vocab_extra_ids_list="[bib_ref],[/bib_ref],[fig_ref],[/fig_ref],[bib],[/bib],[fig],[/fig],[table],[/table],[formula],[/formula],<|im_start|>,<|im_end|>" --override_special_tokens='bos=<|im_start|>','eos=<|im_end|>'
# python ../weights_conversion/megatron_to_hf.py --input_dir=/pure-mlo-scratch/make_project/trial-runs/pubmed-13b-generator/llama-2-13b-tp1-pp1-ex1pubmedreplay-generator1 --output_dir=/pure-mlo-scratch/make_project/trial-runs/pubmed-13b-generator/hf_checkpoint_new --vocab_extra_ids_list="[bib_ref],[/bib_ref],[fig_ref],[/fig_ref],[bib],[/bib],[fig],[/fig],[table],[/table],[formula],[/formula],<|im_start|>,<|im_end|>" --override_special_tokens='bos=<|im_start|>','eos=<|im_end|>'
python ../weights_conversion/megatron_to_hf.py --input_dir=/pure-mlo-scratch/make_project/trial-runs/pubmed-13b-summarizer/llama-2-13b-tp1-pp1-ex1pubmedreplay-summarizer --output_dir=/pure-mlo-scratch/make_project/trial-runs/pubmed-13b-summarizer/hf_checkpoint_new_new --vocab_extra_ids_list="[bib_ref],[/bib_ref],[fig_ref],[/fig_ref],[bib],[/bib],[fig],[/fig],[table],[/table],[formula],[/formula],<|im_start|>,<|im_end|>" --override_special_tokens='bos=<|im_start|>','eos=<|im_end|>'
echo "End"