"""RSS skraper za sportske naslove (Faza 1).

Pokriva izvore koji nude RSS:
  - Mozzart Sport: 6 numerisanih feed-ova (rss/0.xml .. rss/5.xml)
  - SportKlub:     jedan glavni feed (redirect na n1info)

B92 nema javni RSS za sport -> radice se zasebnim HTML skraperom.

Pokretanje:
    .venv/bin/python src/scraping/rss_scraper.py
    .venv/bin/python src/scraping/rss_scraper.py --izvor mozzart
"""
from __future__ import annotations

import argparse
import datetime as _dt
import time

import feedparser

from common import DATA_RAW, Headline, save_csv

# Registar RSS izvora: izvor -> lista feed URL-ova
RSS_SOURCES: dict[str, list[str]] = {
    "mozzart": [f"https://www.mozzartsport.com/rss/{i}.xml" for i in range(6)],
    "sportklub": ["https://sportklub.rs/feed"],
}


def _today() -> str:
    return _dt.date.today().isoformat()


def _parse_date(entry) -> str:
    """Vrati datum objave kao ISO string ako postoji."""
    tm = entry.get("published_parsed") or entry.get("updated_parsed")
    if tm:
        return _dt.date(tm.tm_year, tm.tm_mon, tm.tm_mday).isoformat()
    return ""


def scrape_source(izvor: str, feeds: list[str], pause: float = 1.0) -> list[Headline]:
    rows: list[Headline] = []
    today = _today()
    for url in feeds:
        feed = feedparser.parse(url)
        print(f"  [{izvor}] {url} -> {len(feed.entries)} unosa")
        for e in feed.entries:
            title = (e.get("title") or "").strip()
            if not title:
                continue
            rows.append(
                Headline(
                    naslov=title,
                    izvor=izvor,
                    url=e.get("link", ""),
                    datum=_parse_date(e),
                    rubrika=(e.get("category") or "").strip(),
                    datum_scrape=today,
                )
            )
        time.sleep(pause)  # ljubazno prema serveru
    return rows


def dedup(rows: list[Headline]) -> list[Headline]:
    """Egzaktna deduplikacija po ID-u (ID = hash normalizovanog naslova)."""
    seen: set[str] = set()
    out: list[Headline] = []
    for r in rows:
        if r.id in seen:
            continue
        seen.add(r.id)
        out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--izvor", choices=list(RSS_SOURCES) + ["all"], default="all")
    args = ap.parse_args()

    targets = RSS_SOURCES if args.izvor == "all" else {args.izvor: RSS_SOURCES[args.izvor]}

    for izvor, feeds in targets.items():
        print(f"== {izvor} ==")
        rows = scrape_source(izvor, feeds)
        before = len(rows)
        rows = dedup(rows)
        out = DATA_RAW / f"{izvor}_raw_{_today()}.csv"
        n = save_csv(rows, out)
        print(f"  ukupno {before}, posle dedup {n} -> {out.relative_to(DATA_RAW.parents[1])}")


if __name__ == "__main__":
    main()
