echo "Init"
# python misc_scripts/parallelize.py /pure-mlo-scratch/trial-runs/gap-replay-70b/checkpoints/llama2-70b-tp8-pp8/ --tp=8 --pp=1 --it=$1
python ../make_scripts/parallelize.py /pure-mlo-scratch/make_project/trial-runs/meditron-7b-summarizer/llama-2-7b-tp4-pp1-meditron-summarizer/ --tp=1 --pp=1 --it=$1
echo "End"
