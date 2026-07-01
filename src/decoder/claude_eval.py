#!/usr/bin/env python3
"""Faza 3c — Dekoderski LLM (Anthropic Claude): evaluacija na CELOM skupu.

Profesor je dozvolio "ChatGPT, Gemini (i drugi)" → Claude je validan dekoderski
model. Bez fine-tuninga (zatvoren model) → samo evaluacija. Poredimo iste prompt
varijante (SR/EN, zero/few-shot, sa/bez definicije) iz prompts.py — identičan
protokol i metrike kao baseline/enkoder, radi uporedne tabele.

Zašto Claude ovde: plaćeni Anthropic API nema oštre besplatne rate-limite kao
free Gemini, pa se ceo skup (2200) može odraditi brzo i pouzdano. Keš i dalje
čuva napredak (results/decoder_cache/) — prekid/nastavak bez ponovnih poziva.

Model (CLI --model):
  • claude-haiku-4-5   — najjeftiniji/najbrži, idealan za 0/1 klasifikaciju
                         (~$1/$5 po MTok). PREPORUKA za ovaj zadatak.
  • claude-opus-4-8    — najsposobniji (default po politici), ali skuplji (~$5/$25).
  • claude-sonnet-4-6  — sredina.

Ključ:
  export ANTHROPIC_API_KEY=sk-ant-...
Pokretanje:
  pip install -r requirements-decoder.txt        # anthropic
  python src/decoder/claude_eval.py --model claude-haiku-4-5 --limit 50      # smoke
  python src/decoder/claude_eval.py --model claude-haiku-4-5                 # pun
  python src/decoder/claude_eval.py --variants sr_zero_def en_zero_def
"""
from __future__ import annotations

import argparse
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from baseline import common  # noqa: E402
from decoder import prompts  # noqa: E402
# deli keš/parsiranje sa ostalim dekoderskim skriptama (DRY)
from decoder.chatgpt_eval import CACHE_DIR, load_cache, parse_label  # noqa: E402

# približne cene ($/1M tokena) — proveri aktuelne pre konačne procene
PRICING = {
    "claude-haiku-4-5": (1.0, 5.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-opus-4-8": (5.0, 25.0),
}


def classify_one(client, model, system, user_prompt):
    """Jedan poziv Claude-a. Vrati (tekst, (in_tok, out_tok)).
    NB: ne šaljemo temperature/thinking — na Opus 4.8/4.7 bi temperature dala 400,
    a za 0/1 klasifikaciju nam ne treba thinking. Sistemski prompt traži SAMO cifru."""
    resp = client.messages.create(
        model=model,
        max_tokens=16,
        system=system,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    u = resp.usage
    return text, (u.input_tokens, u.output_tokens)


def _classify_with_retry(client, model, system, user, naslov):
    """Jedan naslov sa retry-jem (SDK i sam retry-uje 429). Vrati
    (msg, (in_tok, out_tok), ok)."""
    for attempt in range(5):
        try:
            msg, (ti, to) = classify_one(client, model, system, user)
            return msg, (ti, to), True
        except Exception as e:  # rate limit / transient
            if attempt == 4:
                print(f"\n   ⚠️  neuspeh '{naslov[:40]}…': {e}")
                return "", (0, 0), False
            time.sleep(min(2 ** attempt * 2, 30))
    return "", (0, 0), False


def run_variant(client, model, variant, texts, labels, limit, holdout,
                min_interval, workers):
    system, template = prompts.build_prompt(
        variant["lang"], variant["shots"], variant["with_def"])
    cache_path = CACHE_DIR / f"{model}__{variant['id']}.jsonl"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache = load_cache(cache_path)

    fewshot_naslovi = {n for n, _ in prompts.FEWSHOT}
    pairs = list(zip(texts, labels))
    if holdout and variant["shots"] == "few":
        pairs = [(t, y) for t, y in pairs if t not in fewshot_naslovi]
    if limit:
        pairs = pairs[:limit]

    # keširane predikcije uzmi odmah; ostalo pošalji (paralelno) na API
    preds = {n: cache[n]["pred"] for n, _ in pairs if n in cache}
    todo = [(n, lab) for n, lab in pairs if n not in cache]

    n_in = n_out = n_calls = 0
    done = 0
    lock = threading.Lock()

    def work(item):
        nonlocal n_in, n_out, n_calls, done
        naslov, lab = item
        user = template.format(naslov=naslov)
        msg, (ti, to), ok = _classify_with_retry(client, model, system, user,
                                                  naslov)
        pred = parse_label(msg) if ok else None
        with lock:  # keš i brojači su deljeni -> serijalizuj upis
            if ok:
                n_in += ti
                n_out += to
                n_calls += 1
            if pred is not None:
                preds[naslov] = pred
                common.append_jsonl(
                    {"naslov": naslov, "true": lab, "pred": pred, "raw": msg},
                    cache_path)
            done += 1
            if done % 50 == 0:
                sys.stdout.write(f"\r   {variant['id']}: {done}/{len(todo)} "
                                 f"novih (workers={workers})")
                sys.stdout.flush()

    if todo:
        if workers <= 1:
            for it in todo:
                work(it)
        else:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                list(ex.map(work, todo))
    print()

    # sastavi metrike u originalnom redosledu para
    y_true, y_pred, skipped = [], [], 0
    for naslov, lab in pairs:
        p = preds.get(naslov)
        if p is None:
            skipped += 1
            continue
        y_true.append(lab)
        y_pred.append(p)

    m = common.compute_metrics(y_true, y_pred) if y_true else {}
    row = {"model": model, "variant": variant["id"], "lang": variant["lang"],
           "shots": variant["shots"], "with_def": variant["with_def"],
           "n_eval": len(y_true), "n_unparsed": skipped, "new_api_calls": n_calls}
    for k in ("accuracy", "precision_kb", "recall_kb", "f1_kb", "f1_macro"):
        row[k] = f"{m[k]:.3f}" if k in m else "—"
    return row, (n_in, n_out)


def main():
    ap = argparse.ArgumentParser(description="Faza 3c Claude (Anthropic) eval.")
    ap.add_argument("--model", default="claude-opus-4-8",
                    help="npr. claude-haiku-4-5 (jeftino), claude-opus-4-8, "
                         "claude-sonnet-4-6")
    ap.add_argument("--variants", nargs="+", default=None,
                    help="id-jevi iz prompts.VARIANTS (podrazumevano sve)")
    ap.add_argument("--limit", type=int, default=None,
                    help="evaluiraj samo prvih N (smoke-test)")
    ap.add_argument("--rpm", type=float, default=0,
                    help="opcioni throttle (NOVIH zahteva/min); 0 = bez (plaćeni "
                         "tier ima visoke limite, SDK i sam retry-uje 429)")
    ap.add_argument("--workers", type=int, default=10,
                    help="broj paralelnih API zahteva (1 = sekvencijalno)")
    ap.add_argument("--holdout-fewshot", action="store_true", default=True)
    ap.add_argument("--out", default=str(common.RESULTS / "decoder_results.csv"))
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("❌ Postavi ANTHROPIC_API_KEY (export ANTHROPIC_API_KEY=sk-ant-...).")
    try:
        import anthropic
    except ImportError:
        sys.exit("❌ Nedostaje SDK: pip install -r requirements-decoder.txt (anthropic).")
    client = anthropic.Anthropic(max_retries=5)
    min_interval = 60.0 / args.rpm if args.rpm > 0 else 0.0

    variants = prompts.VARIANTS
    if args.variants:
        variants = [v for v in prompts.VARIANTS if v["id"] in args.variants]
        if not variants:
            sys.exit(f"Nepoznate varijante. Dostupne: "
                     f"{[v['id'] for v in prompts.VARIANTS]}")

    texts, labels = common.load_dataset()
    print(f"Eval skup: {len(texts)} naslova | model={args.model} | "
          f"varijanti={len(variants)}")

    rows, tot_in, tot_out = [], 0, 0
    for v in variants:
        print(f"\n=== {v['id']} ===")
        row, (ti, to) = run_variant(client, args.model, v, texts, labels,
                                    args.limit, args.holdout_fewshot,
                                    min_interval, args.workers)
        rows.append(row)
        tot_in += ti
        tot_out += to
        print(f"   F1_kb={row['f1_kb']} acc={row['accuracy']} "
              f"(neparsiranih={row['n_unparsed']})")

    rows.sort(key=lambda r: r["f1_kb"], reverse=True)
    common.write_results_csv(rows, args.out)

    if args.model in PRICING and (tot_in or tot_out):
        pin, pout = PRICING[args.model]
        cost = tot_in / 1e6 * pin + tot_out / 1e6 * pout
        print(f"\n💰 Novi pozivi ove sesije: in={tot_in} out={tot_out} tok "
              f"→ ~${cost:.4f} ({args.model}).")
    print("ℹ️  Keširani odgovori se ne plaćaju ponovo (results/decoder_cache/).")


if __name__ == "__main__":
    main()
