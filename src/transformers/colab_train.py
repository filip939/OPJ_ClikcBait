#!/usr/bin/env python3
"""Faza 3b — JEDAN FAJL za Google Colab (BESPLATNO).

Šta radi (sve sam):
  1) klonira javni repo na čisto (rešava getcwd/ugnežđene-klonove probleme),
  2) instalira zavisnosti,
  3) trenira BERTić pa mBERT (10-fold CV, epohe 2/3/4, batch 64),
  4) na KRAJU jasno ISPIŠE PUNE PUTANJE do rezultata + sam sadržaj CSV-ova.

Kako pokrenuti na Colabu:
  • Runtime → Change runtime type → T4 GPU
  • Otpremi ovaj fajl (levo, ikonica za upload) ILI nalepi sadržaj u ćeliju
  • Pokreni:   !python colab_train.py
        (ili, ako si nalepio u ćeliju, samo pokreni ćeliju)

Brže/krace (po želji):
  !python colab_train.py --quick           # 2 folda, brzi smoke (par minuta)
  !python colab_train.py --models bertic   # samo jedan model
  !python colab_train.py --batch-size 32   # ako zafali VRAM
"""
import argparse
import glob
import os
import subprocess
import sys

REPO_URL = "https://github.com/filip939/OPJ_ClikcBait.git"
CLONE_DIR = "/content/repo"


def sh(cmd, cwd="/content"):
    print(f"\n$ {cmd}", flush=True)
    return subprocess.run(cmd, shell=True, cwd=cwd).returncode


def main():
    ap = argparse.ArgumentParser(description="Faza 3b — Colab runner")
    ap.add_argument("--models", nargs="+", default=["bertic", "mbert"],
                    choices=["bertic", "mbert"])
    ap.add_argument("--epochs", nargs="+", type=int, default=[2, 3, 4])
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--quick", action="store_true",
                    help="2 folda (brzi smoke)")
    args = ap.parse_args()

    # 1) čist klon (izbegni getcwd grešku ako je CWD obrisan)
    os.chdir("/content")
    sh(f"rm -rf {CLONE_DIR} /content/OPJ")
    if sh(f"git clone {REPO_URL} {CLONE_DIR}") != 0:
        sys.exit("❌ git clone nije uspeo (repo privatan ili nema mreže?).")
    hits = glob.glob(f"{CLONE_DIR}/**/src/transformers/finetune.py",
                     recursive=True)
    if not hits:
        sys.exit("❌ Ne nalazim finetune.py u kloniranom repou.")
    root = hits[0].split("/src/transformers/")[0]
    os.chdir(root)
    print(f"\nROOT = {root}", flush=True)

    # 2) zavisnosti
    sh("pip -q install -U transformers datasets accelerate scikit-learn")

    # 3) trening
    epochs = " ".join(str(e) for e in args.epochs)
    quick = " --quick" if args.quick else ""
    for model in args.models:
        rc = sh(f"python src/transformers/finetune.py --model {model} "
                f"--epochs {epochs} --batch-size {args.batch_size}{quick}",
                cwd=root)
        if rc != 0:
            print(f"⚠️  {model} je pao (returncode={rc}) — vidi grešku iznad.")

    # 4) ISPIS PUTANJA + sadržaja
    print("\n" + "=" * 64)
    print("📂 REZULTATI (pune putanje — ovde ih nađeš / desni-klik → Download):")
    found = sorted(glob.glob(f"{root}/results/encoder_*_results.csv"))
    if not found:
        print("  (nema CSV-ova — trening verovatno nije završio, vidi greške)")
    for f in found:
        print(f"\n  ▶ {f}")
        print(open(f, encoding="utf-8").read())
    print("=" * 64)
    print("ℹ️  Kopiraj gornje tabele (ili skini CSV-ove iz fajl panela levo).")


if __name__ == "__main__":
    main()
