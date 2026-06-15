"""SportKlub bulk skraper preko WordPress REST API-ja (Faza 1).

SportKlub (n1info platforma) izlaze WP REST API sa ~449k clanaka.
Endpoint: /wp-json/wp/v2/posts?per_page=100&page=N
Vraca cist title, datum, kategorije -> idealno za bulk prikupljanje.

Pokretanje:
    .venv/bin/python src/scraping/sportklub_api.py --broj 1500
    .venv/bin/python src/scraping/sportklub_api.py --broj 1500 --kategorija 326845  # samo Bundesliga
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import re
import time

import requests

from common import DATA_RAW, HEADERS, Headline, save_csv

API = "https://sportklub.n1info.rs/wp-json/wp/v2"
PER_PAGE = 100


def _clean_html(s: str) -> str:
    """WP vraca naslov sa HTML entitetima (npr. &#8220;) - dekoduj."""
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()


def fetch_categories() -> dict[int, str]:
    r = requests.get(f"{API}/categories?per_page=100", headers=HEADERS, timeout=20)
    return {c["id"]: c["name"] for c in r.json()}


def scrape(broj: int, kategorija: int | None = None, pause: float = 1.0) -> list[Headline]:
    cats = fetch_categories()
    today = _dt.date.today().isoformat()
    rows: list[Headline] = []
    page = 1
    while len(rows) < broj:
        params = {"per_page": PER_PAGE, "page": page, "_fields": "title,link,date,categories"}
        if kategorija:
            params["categories"] = kategorija
        r = requests.get(f"{API}/posts", headers=HEADERS, params=params, timeout=20)
        if r.status_code != 200:
            print(f"  stop na strani {page}: status {r.status_code}")
            break
        data = r.json()
        if not data:
            break
        for p in data:
            title = _clean_html(p.get("title", {}).get("rendered", ""))
            if not title:
                continue
            cat_ids = p.get("categories", [])
            rubrika = cats.get(cat_ids[0], "") if cat_ids else ""
            rows.append(
                Headline(
                    naslov=title,
                    izvor="sportklub",
                    url=p.get("link", ""),
                    datum=(p.get("date", "") or "")[:10],
                    rubrika=rubrika,
                    datum_scrape=today,
                )
            )
        print(f"  strana {page}: ukupno {len(rows)}")
        page += 1
        time.sleep(pause)
    return rows[:broj]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--broj", type=int, default=1500, help="koliko naslova prikupiti")
    ap.add_argument("--kategorija", type=int, default=None, help="ID kategorije (opciono)")
    args = ap.parse_args()

    rows = scrape(args.broj, args.kategorija)
    today = _dt.date.today().isoformat()
    out = DATA_RAW / f"sportklub_api_{today}.csv"
    save_csv(rows, out)
    print(f"\nSnimljeno {len(rows)} naslova -> {out}")


if __name__ == "__main__":
    main()
