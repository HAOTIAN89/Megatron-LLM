import re
from argparse import ArgumentParser
from pathlib import Path
from subprocess import Popen
from typing import Optional

from do_finetuning import prepare_checkpoint

def int_or_str(val: str) -> int | str:
    try:
        return int(val)
    except ValueError:
        return val


def main(checkpoint: Path, tp: int = 1, pp: int = 1, vocab: int = 32017,
         it: Optional[int | str] = None, model: str = "llama2") -> Path:
    out = checkpoint.parent/re.sub("tp[0-9]+-pp[0-9]+", f"tp{tp}-pp{pp}", checkpoint.name)
    print(f"checkpoint: {checkpoint}")
    print(f"out: {out}")    
    assert out != checkpoint
    cmd = ["python", "../tools/checkpoint_util_new.py",
           f"--target_tensor_parallel_size={tp}",
           f"--target_pipeline_parallel_size={pp}",
           f"--model_type={model}", f"--true_vocab_size={vocab}", "--bf16",
           f"--load_dir={checkpoint}", f"--save_dir={out}"]
    if it is not None:
        cmd.append(f"--load_iteration={it}")
    with Popen(cmd) as proc:
        assert proc.wait() == 0
    # with prepare_checkpoint(checkpoint, iteration=it):
    #     print(f"Parallelizing to tp{tp} pp{pp} the iteration {it} to: {out}")
    #     with Popen(cmd) as proc:
    #         assert proc.wait() == 0
    return out


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("--tp", type=int, default=1)
    parser.add_argument("--pp", type=int, default=1)
    parser.add_argument("--vocab", type=int, default=32017)
    parser.add_argument("--it", type=int_or_str)
    parser.add_argument("--model", default="llama2")
    args = parser.parse_args()
    main(args.checkpoint, tp=args.tp, pp=args.pp, vocab=args.vocab,
         it=args.it, model=args.model)
