'''
Finetune pipline
'''

import re
import time
import math
from contextlib import contextmanager
from pathlib import Path
from typing import Optional
from subprocess import Popen, PIPE
from argparse import ArgumentParser, Namespace



CHECKPOINTS = {
    ("baseline", 7): "/pure-mlo-scratch/alhernan/megatron-data/checkpoints/llama2-7b-tp4-pp1",
    ("baseline", 13): "/pure-mlo-scratch/alhernan/megatron-data/checkpoints/llama2-13b-tp8-pp1",
    ("baseline", 70): "/pure-mlo-scratch/alhernan/megatron-data/checkpoints/llama2-70b-tp8-pp8",

    ("ex1pubmed", 7): "/pure-mlo-scratch/trial-runs/ex1-pubmed/checkpoints/llama2-7b-tp4-pp1-optimized",
    ("ex1gapreplay", 7): "/pure-mlo-scratch/trial-runs/ex1-gap-replay/checkpoints/llama2-7b-tp4-pp1",
    ("ex1gapreplay2epochs", 7): "/pure-mlo-scratch/trial-runs/ex1-gap-replay-2-epochs/checkpoints/llama2-7b-tp4-pp1",

    ("ex1pubmedreplay", 7): "/pure-mlo-scratch/trial-runs/ex1-pubmed-replay/checkpoints/llama2-7b-tp4-pp1",
    ("ex1pubmedreplayorca", 7): "/pure-mlo-scratch/alhernan/megatron-data/checkpoints/instructed/llama-2-7b-tp4-pp1-ex1pubmedreplay-orca-it0018000-seq4096",
    ("ex1pubmedreplay", 13): "/pure-mlo-scratch/trial-runs/ex1-pubmed-replay-13b/checkpoints/llama2-13b-tp8-pp1",   # this is what we need, Llama2-13b pretrained on pubmed

    ("ex3pubmedreplaycode", 7): "/pure-mlo-scratch/trial-runs/ex3-pubmed-replay-code/checkpoints/llama2-7b-tp4-pp1",
    ("ex3pubmedcode", 13): "/pure-mlo-scratch/trial-runs/ex3-pubmed-code-13b/checkpoints/llama2-13b-tp8-pp1",

    ("ex4pubmedup", 7): "/pure-mlo-scratch/trial-runs/ex4-pubmed-up-23/checkpoints/llama2-7b-tp4-pp1",
    ("ex5pubmedreplaycode2B", 7): "/pure-mlo-scratch/trial-runs/ex5-pubmed-replay-code-2b/checkpoints/llama2-7b-tp4-pp1",

    ("pmc", 7): "/pure-mlo-scratch/alhernan/megatron-data/checkpoints/llamaPMC-7b-tp4-pp1",
    ("pmc", 13): "/pure-mlo-scratch/alhernan/megatron-data/checkpoints/llamaPMC-13b-tp8-pp1",

    ("gap", 70): "/pure-mlo-scratch/trial-runs/gap-replay-70b/checkpoints/llama2-70b-tp8-pp8",
    ("guidelines", 70): "/pure-mlo-scratch/trial-runs/guidelines-70b/checkpoints/llama2-70b-tp8-pp8",
    
    ("meditron", 7): "/pure-mlo-scratch/trial-runs/meditron-7b/checkpoints/llama2-7b-tp4-pp1",
    ("meditron", 70): "/pure-mlo-scratch/trial-runs/meditron-70b/checkpoints/llama2-70b-tp8-pp8",
    
    ("meditron-7B-BHC-extend", 7): "/pure-mlo-scratch/make_project/spring2024/trial-runs/meditron-7B-BHC-v2/llama2-7b-tp4-pp1",
}

N_DOCS = {
    "medmcqa": 159669,
    "cotmedmcqa": 182822,
    "medqa": 10178,
    "cotmedqa": 10178,
    "medqa-5-shot": 10178,
    "cotmedqa-qbank": 8204,
    "cotmedqa-gpt4": 8207,
    "pubmedqa": 200000,
    "cotpubmedqa": 200000,
    "mixed": 193450,
    "mixedmed": 369847,
    "cotmixedmed": 359669,
    "newpubmedqa": 200000,
    "newcotpubmedqa": 200000,
    "medmixturea": 31609,
    "summarizer": 27000,
    "generator1": 27000,
    "direct": 27000,
    "direct-trunc": 27000,
    "bhc-2k": 31800,
    "di-2k": 48800,
    "bhc-2k-v2": 31800,
    "di-2k-v2": 51600,
    "di-2k-v2.1": 58300,
    "bhc-2k-v3": 15400,
    "di-2k-v3": 17700,
    "bhc-6k-v4": 67100,
    "di-6k-v4": 68600,
    "bhc-2k-v4": 16500,
    "di-2k-v4": 48400,
    "bhc-8k-v5": 68200,
    "di-8k-v5": 68700,
    "bhc-6k-v5": 66400,
    "di-6k-v5": 68500,
    "bhc-6k-v6": 38300,
    "di-6k-v6": 39400, 
}
CHECKPOINTS = {key: Path(value) for key, value in CHECKPOINTS.items()}
# OUT_ROOT = Path("/pure-mlo-scratch/zechen/meditron/benchmarks/ft_preprocessed/tokenized/")
OUT_ROOT = Path("/pure-mlo-scratch/make_project/spring2024/data/tokenized/")
# FINAL_CHECKPOINT_ROOT = Path("/pure-mlo-scratch/alhernan/megatron-data/checkpoints/instructed/")
FINAL_CHECKPOINT_ROOT = Path("/pure-mlo-scratch/make_project/spring2024/trial-runs/meditron-7B-BHC-v6-6k/")
DEFAULT_EPOCHS = 3
DEFAULT_SEQ = 6144
DEFAULT_LOSS_MASK = 0.0

@contextmanager
def prepare_checkpoint(checkpoint: Path, iteration: Optional[int | str] = None):
    # change the latest_checkpointed_iteration to desired iteration
    if iteration is not None:
        latest_txt = checkpoint/"latest_checkpointed_iteration.txt"
        with open(latest_txt) as f:
           orig_iter = f.read()
        with open(latest_txt, "w+") as f:
            f.write(str(iteration))

    try:
        yield
    finally:
        if iteration is not None:
            with open(latest_txt) as f:
                current_iter = f.read()
            if current_iter == str(iteration):
                with open(latest_txt, "w+") as f:
                    f.write(orig_iter)

def execute(cmd: list[str]):
    with Popen(cmd) as proc:
        assert proc.wait() == 0


def get_parallel_levels(checkpoint: Path | str, size: Optional[int] = None) -> tuple[int, int]:
    if isinstance(checkpoint, Path):
        assert size is None
        path = checkpoint
    else:
        path = CHECKPOINTS[checkpoint, size]

    if rmatch := re.match("^.*-tp([0-9]+)-pp([0-9]+).*$", path.name):
        return tuple(map(int, rmatch.groups()))
    raise ValueError(f"Could not infer tp and pp from {path}")


def tokenize_data(run_name: str, paths: list[Path], rank: int, qkey: str = "prompt",
                  akey: str = "gold", skey: Optional[str] = None,
                  verbose: bool = True) -> Path:
    if verbose:
        print("Tokenizing data!")
    out = OUT_ROOT/run_name
    out_prefix = out/run_name
    if Path(f"{out_prefix}-text.bin").exists():
        if verbose:
            print("Data already tokenized!")
        return out_prefix
    if rank > 0:
        if verbose:
            print("Not main node, ignoring data tokenization")
        return out_prefix
    assert len(paths) > 0, "--data argument required when the data is not already tokenized"
    out.mkdir()
    paths = list(map(str, paths))
    extra_vocabs = "[bib_ref],[/bib_ref],[fig_ref],[/fig_ref],[bib],[/bib],[fig],[/fig],[table],[/table],[formula],[/formula],<|im_start|>,<|im_end|>"
    cmd = ["python", "/home/haotian/Megatron-LLM/tools/preprocess_instruct_data.py", "--input"] + paths 
    cmd += [f"--output_prefix={out_prefix}", "--tokenizer_type=SentencePieceTokenizer",
            "--vocab_file=/pure-mlo-scratch/llama/tokenizer.model", "--chunk_size=32",
            "--workers=32", "--vocab_extra_ids_list", extra_vocabs,
            f"--question_key={qkey}", f"--answer_key={akey}"]
    if skey is not None:
        cmd.append(f"--system_key={skey}")
    execute(cmd)
    return out_prefix


def infer_ndocs(cmd: list[str], autoaccept_iters: bool = True) -> int:
    n_docs = None
    training_started = False
    with Popen(cmd, stdout=PIPE, text=True) as proc:
        for n_line, line in enumerate(map(lambda line: line.strip(), iter(proc.stdout.readline, ""))):
            print(line)
            if (rmatch := re.match("^number of documents: ([0-9]+)$", line)):
                n_docs = int(rmatch.group(1))
            if line.startswith("[before the start of training step]"):
                training_started = True
            if n_line >= 2000 or n_docs is not None or training_started:
                break
        proc.terminate()
    for _ in range(10):
        print("zzz")
        time.sleep(1)  # to wait for the closure of the port :6000
    if n_docs is None:
        print("Falied to infer the number of documents, look at log above")
        return int(input("Now enter number of documents manually: "))
    print("Number of documents inferred:", n_docs)
    if autoaccept_iters or input(f"Accept {n_docs} documents? (y/n) ") != "n":
        return n_docs
    return int(input("Now enter number of documents manually: "))


def finetune(args: Namespace, data_path: Path, val_path: Path, out: Path):
    load_check = out.exists() and len(list(out.glob("iter*"))) > 0
    if load_check:
        print(f"Final checkpoint exists, resuming training {out}")
        load_from = out
    else:
        load_from = CHECKPOINTS[args.checkpoint, args.size]
        latest_txt = load_from/"latest_checkpointed_iteration.txt"

    tp, pp = get_parallel_levels(out)
    wandb_id = out.name.replace(f"-tp{tp}-pp{pp}", "").replace("llama-2", "llama2")
    wandb = ["--wandb", "--wandb-project", "Phase2stage7", "--wandb-id",
             wandb_id]
    model_name = "llama" if args.checkpoint == "pmc" else "llama2"
    cmd = ["bash", "/home/haotian/Megatron-LLM/examples/finetunenew.sh", model_name, "--instruct", "--micro-batch", 
           args.micro_batch, "--global-batch", "64", "--tp", tp, "--pp", pp, "--seq-len",
           args.seq, "--checkpoint", load_from, "--data", data_path,
           "--out", out, "--loss-mask", args.loss_mask, "--save-interval", args.save_interval]
    if args.intermediate_iter is not None:
        cmd += ["--it", args.intermediate_iter]
    if val_path is not None:
        cmd += ["--val-path", val_path]
    status_path = out/".status.txt"
    print("Status path:", status_path)

    if args.rank > 0 or load_check:
        intermediate_iter = None
    else:
        intermediate_iter = args.intermediate_iter

    if not load_check:
        if args.run_name in N_DOCS:
            n_docs = N_DOCS[args.run_name]
        else:
            print("Trying to infer the number of documents in the dataset")
            assert args.nodes == 1, "n docs infer only supported when nodes=1"
            cmd = list(map(str, cmd))
            n_docs = infer_ndocs(cmd, autoaccept_iters=args.autoaccept_iters)
        n_iters = args.epochs*n_docs/64
        n_iters = 10*int(math.ceil(n_iters/10))  # to make it a multiple of 10 xd
        cmd += ["--iters", n_iters]

        if args.rank == 0:
            out.mkdir(exist_ok=True)
            with open(status_path, "w+") as f:
                print(f"Training for {n_iters} iterations", file=f)

    if args.nodes > 1:
        cmd += ["--nodes", args.nodes, "--rank", args.rank, "--addr", args.addr]

    # execute command
    print("Finetuning")
    cmd += wandb
    cmd = list(map(str, cmd))
    execute(cmd)

    if args.rank == 0:
        with open(status_path, "a") as f:
            print("Training done", file=f)
    return out


def main(args: Namespace):
    if (args.checkpoint, args.size) not in CHECKPOINTS:
        raise KeyError(f"Invalid checkpoint, size configuration: {args.checkpoint}, {args.size}")

    # change path names if tp or pp is overriden
    tp, pp = get_parallel_levels(args.checkpoint, args.size)
    if args.pp is not None:
        path = CHECKPOINTS[args.checkpoint, args.size]
        CHECKPOINTS[args.checkpoint, args.size] = path.parent/path.name.replace(f"pp{pp}", f"pp{args.pp}")
    if args.tp is not None:
        path = CHECKPOINTS[args.checkpoint, args.size]
        CHECKPOINTS[args.checkpoint, args.size] = path.parent/path.name.replace(f"tp{tp}", f"tp{args.tp}")

    # check if this run has been completed before, i.e. if the huggingface checkpoint exists
    suffix = "" if args.intermediate_iter is None else f"-it{args.intermediate_iter:07d}"
    suffix += "" if args.epochs == DEFAULT_EPOCHS else f"-ep{args.epochs}"
    suffix += "" if args.seq == DEFAULT_SEQ else f"-seq{args.seq}"
    suffix += "" if args.loss_mask == DEFAULT_LOSS_MASK else f"-loss{args.loss_mask}"
    suffix += "" if args.id is None else f"-{args.id}"
    llama_v = f"llama-{args.size}b" if args.checkpoint == "pmc" else f"llama-2-{args.size}b"
    tp, pp = get_parallel_levels(args.checkpoint, args.size)
    out = FINAL_CHECKPOINT_ROOT/f"{llama_v}-tp{tp}-pp{pp}-{args.checkpoint}-{args.run_name}{suffix}"
    final_checkpoint = Path(str(out).replace(f"tp{tp}-pp{pp}", "hf"))
    if final_checkpoint.exists():
        print("Final huggingface checkpoint for this model and run already "
              f"exists at {final_checkpoint}")
        exit(1)

    if tp*pp > 8:
        print("Note: The selected checkpoint requires at least", int(math.ceil(tp*pp/8)),
              f"nodes to train as it has tp={tp}, pp={pp}")

    # start pipeline
    data_prefix = tokenize_data(args.run_name, args.data, args.rank, qkey=args.qkey,
                                akey=args.akey, skey=args.skey)
    if len(args.val) == 0:
        val_prefix = None
    else:
        val_prefix = tokenize_data(f"{args.run_name}-val", args.val, args.rank, qkey=args.qkey,
                                   akey=args.akey, skey=args.skey)
    finetune(args, data_prefix, val_prefix, out)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--checkpoint", default="baseline", choices=[name for name, size in CHECKPOINTS],
                        help="Name of the model to finetune")
    parser.add_argument("--size", default=7, choices=[7, 13, 70], type=int,
                        help="Size of the model to finetune")
    parser.add_argument("--run_name", required=True,
                        help="Name of the run (e.g. cotmcq or pubmedqa")
    parser.add_argument("--data", nargs="+", type=Path, default=[],
                        help="Paths of the jsonl files to train with")
    parser.add_argument("--val", nargs="+", type=Path, default=[],
                        help="Paths of the jsonl files to validate data")
    parser.add_argument("--no_autoaccept_iters", action="store_false", dest="autoaccept_iters",
                        help="Ask for confirmation when the number of iterations is inferred")
    parser.add_argument("--intermediate_iter", type=int,
                        help=("Specify the iteration of the checkpoint to train, "
                              "instead of using the latest available checkpoint"))
    parser.add_argument("--question_key", default="prompt", dest="qkey",
                        help="Specify question key in the json")
    parser.add_argument("--answer_key", default="gold", dest="akey",
                        help="Specify answer key in the json")
    parser.add_argument("--system_key", dest="skey",
                        help="Specify system key in the json")
    parser.add_argument("--micro_batch", type=int, default=32,
                        help="Micro batch size")
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS,
                        help="Epochs to train for")
    parser.add_argument("--seq", type=int, default=DEFAULT_SEQ,
                        help="Sequence length")
    parser.add_argument("--rank", type=int, default=0, help="Rank")
    parser.add_argument("--nodes", type=int, default=1, help="Number of nodes")
    parser.add_argument("--addr", default="gpu001.rcp.epfl.ch", help="Master addr")
    parser.add_argument("--loss_mask", type=float, default=DEFAULT_LOSS_MASK)
    parser.add_argument("--save_interval", type=int, default=800)
    parser.add_argument("--id", help="Unique ID to append to the run name")
    parser.add_argument("--tp", type=int, help="Force tp to use")
    parser.add_argument("--pp", type=int, help="Force pp to use")
    args = parser.parse_args()
    main(args)
