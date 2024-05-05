echo "Init"
# python misc_scripts/parallelize.py /pure-mlo-scratch/trial-runs/gap-replay-70b/checkpoints/llama2-70b-tp8-pp8/ --tp=8 --pp=1 --it=$1
# python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/trial-runs/meditron-7b-summarizer/llama-2-7b-tp4-pp1-meditron-summarizer/ --tp=1 --pp=1 --vocab=32019 --it=$1
# python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/trial-runs/meditron-7b-generator/llama-2-7b-tp4-pp1-meditron-generator1/ --tp=1 --pp=1 --vocab=32019 --it=$1
# python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/trial-runs/meditron-7b-direct/llama-2-7b-tp4-pp1-meditron-direct/ --tp=1 --pp=1 --vocab=32019 --it=$1
# python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/trial-runs/meditron-7b-direct-trunc/llama-2-7b-tp4-pp1-meditron-direct-trunc/ --tp=1 --pp=1 --vocab=32019 --it=$1
# python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/trial-runs/pubmed-13b-summarizer/llama-2-13b-tp8-pp1-ex1pubmedreplay-summarizer/ --tp=1 --pp=1 --vocab=32019 --it=$1
# python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/trial-runs/pubmed-13b-generator/llama-2-13b-tp8-pp1-ex1pubmedreplay-generator1/ --tp=1 --pp=1 --vocab=32019 --it=$1
# python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/trial-runs/pubmed-13b-direct-trunc/llama-2-13b-tp8-pp1-ex1pubmedreplay-direct-trunc/ --tp=1 --pp=1 --vocab=32019 --it=$1
# python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/spring2024/trial-runs/meditron-7B-BHC/llama-2-7b-tp4-pp1-meditron-bhc-2k/ --tp=1 --pp=1 --vocab=32019 --it=$1
# python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/spring2024/trial-runs/meditron-7B-DI/llama-2-7b-tp4-pp1-meditron-di-2k/ --tp=1 --pp=1 --vocab=32019 --it=$1
python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/spring2024/trial-runs/meditron-7B-DI-v5-6k/llama-2-7b-tp4-pp1-meditron-di-6k-v5/ --tp=1 --pp=1 --vocab=32019 --it=$1
echo "End"
