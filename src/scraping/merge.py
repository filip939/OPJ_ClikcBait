"""Spaja sve sirove snapshotove (data/raw/*.csv) u jedan deduplikovan skup.

Dedup u dva nivoa:
  1) egzaktni - po `id` (hash normalizovanog naslova)
  2) near-duplicate - rapidfuzz token_sort_ratio iznad praga (isti dogadjaj,
     sitne razlike, cesto isti naslov sa razlicitih portala)

Izlaz:
  data/interim/headlines.csv  - ciscen, deduplikovan skup spreman za anotaciju
  data/metadata.csv           - id, url, izvor, datum, datum_scrape

Pokretanje:
    .venv/bin/python src/scraping/merge.py
    .venv/bin/python src/scraping/merge.py --prag 92
"""
from __future__ import annotations

import argparse
import glob

import pandas as pd
from rapidfuzz import fuzz

from common import COLUMNS, ROOT, normalize_for_dedup

RAW_GLOB = str(ROOT / "data" / "raw" / "*.csv")
OUT_HEADLINES = ROOT / "data" / "interim" / "headlines.csv"
OUT_META = ROOT / "data" / "metadata.csv"


def load_all() -> pd.DataFrame:
    files = sorted(glob.glob(RAW_GLOB))
    if not files:
        raise SystemExit("Nema fajlova u data/raw/ - prvo pokreni rss_scraper.py")
    frames = [pd.read_csv(f, dtype=str, keep_default_na=False) for f in files]
    df = pd.concat(frames, ignore_index=True)
    print(f"Ucitano {len(df)} redova iz {len(files)} fajl(ova)")
    return df


def exact_dedup(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset="id", keep="first").reset_index(drop=True)
    print(f"Egzaktni dedup: {before} -> {len(df)} (-{before - len(df)})")
    return df


def fuzzy_dedup(df: pd.DataFrame, prag: int = 92) -> pd.DataFrame:
    """Uklanja near-duplicate naslove. Blokira po prve 2 reci radi brzine."""
    df = df.copy()
    df["_norm"] = df["naslov"].map(normalize_for_dedup)
    df["_blok"] = df["_norm"].str.split().str[:2].str.join(" ")

    drop_idx: set[int] = set()
    for _, grupa in df.groupby("_blok"):
        idxs = grupa.index.tolist()
        for i in range(len(idxs)):
            if idxs[i] in drop_idx:
                continue
            a = df.at[idxs[i], "_norm"]
            for j in range(i + 1, len(idxs)):
                if idxs[j] in drop_idx:
                    continue
                b = df.at[idxs[j], "_norm"]
                if fuzz.token_sort_ratio(a, b) >= prag:
                    drop_idx.add(idxs[j])

    before = len(df)
    df = df.drop(index=drop_idx).drop(columns=["_norm", "_blok"]).reset_index(drop=True)
    print(f"Fuzzy dedup (prag={prag}): {before} -> {len(df)} (-{len(drop_idx)})")
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prag", type=int, default=92, help="prag slicnosti za fuzzy dedup (0-100)")
    args = ap.parse_args()

    df = load_all()
    df = exact_dedup(df)
    df = fuzzy_dedup(df, args.prag)

    # Sortiranje radi preglednosti
    df = df.sort_values(["izvor", "datum"]).reset_index(drop=True)

    OUT_HEADLINES.parent.mkdir(parents=True, exist_ok=True)
    df[COLUMNS].to_csv(OUT_HEADLINES, index=False, encoding="utf-8")
    df[["id", "url", "izvor", "datum", "datum_scrape"]].to_csv(
        OUT_META, index=False, encoding="utf-8"
    )

    print(f"\nFINALNO: {len(df)} jedinstvenih naslova")
    print("  po izvoru:", df["izvor"].value_counts().to_dict())
    print(f"  -> {OUT_HEADLINES.relative_to(ROOT)}")
    print(f"  -> {OUT_META.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
