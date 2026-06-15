"""Mozzart bulk skraper preko enumeracije ID-eva clanaka (Faza 1).

Mozzart nema upotrebljiv API. Ali clanci imaju sekvencijalne numericke ID-eve,
a stranica izlaze pravi naslov u <meta property="og:title"> cak i sa
placeholder slug-om. Fiksni prefiks 'fudbal/vesti/x/<id>' radi za BILO koji ID.

Strategija: poci od najnovijeg ID-a (auto-detekcija iz RSS-a) i ici unazad,
preskacuci nevazece (komentari, obrisani). Skuplja se naslov + prava kategorija
iz og:url.

Pokretanje:
    .venv/bin/python src/scraping/mozzart_bulk.py --broj 1500
    .venv/bin/python src/scraping/mozzart_bulk.py --broj 1500 --start 546400
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import time

import feedparser
import requests
from bs4 import BeautifulSoup

from common import DATA_RAW, HEADERS, Headline, save_csv

PREFIX = "fudbal/vesti/x"  # fiksni placeholder prefiks - radi za sve ID-eve
BASE = "https://www.mozzartsport.com"
PLACEHOLDER_RE = re.compile(r"^\d+\s*\|\s*Mozzart", re.I)  # npr. "546409 | Mozzart Sport"


def detect_max_id() -> int:
    """Najveci ID iz trenutnih RSS feed-ova = polazna tacka."""
    ids: list[int] = []
    for i in range(6):
        f = feedparser.parse(f"{BASE}/rss/{i}.xml")
        for e in f.entries:
            m = re.search(r"/(\d{5,})(?:/|$)", e.get("link", ""))
            if m:
                ids.append(int(m.group(1)))
    return max(ids) if ids else 546500


def fetch_one(idnum: int, today: str) -> Headline | None:
    u = f"{BASE}/{PREFIX}/{idnum}"
    try:
        r = requests.get(u, headers=HEADERS, timeout=15)
    except requests.RequestException:
        return None
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "lxml")
    og = soup.find("meta", property="og:title")
    if not og or not og.get("content"):
        return None
    title = og["content"].strip()
    if PLACEHOLDER_RE.match(title) or not title:
        return None  # nevazeci/obrisan clanak
    # Mozzart (kladionica) ima promo "SPECIJAL"/kvote clanke - nisu prave vesti
    if title.upper().startswith("SPECIJAL"):
        return None
    # Napomena: rubrika se ne moze pouzdano dobiti iz ID-a (og:url ne preusmerava
    # na pravu kategoriju kod placeholder prefiksa), pa je ostavljamo praznom.
    return Headline(
        naslov=title, izvor="mozzart", url=u, datum="",
        rubrika="", datum_scrape=today,
    )


def scrape(broj: int, start: int | None, pause: float = 0.6) -> list[Headline]:
    today = _dt.date.today().isoformat()
    idnum = start or detect_max_id()
    print(f"  pocetni ID: {idnum}")
    rows: list[Headline] = []
    misses = 0
    while len(rows) < broj and idnum > 0:
        h = fetch_one(idnum, today)
        if h:
            rows.append(h)
            misses = 0
            if len(rows) % 50 == 0:
                print(f"  prikupljeno {len(rows)} (trenutni ID {idnum})")
        else:
            misses += 1
        # zaustavi ako predugo nema validnih (kraj arhive / rupa)
        if misses > 200:
            print(f"  prekid: 200 uzastopnih promasaja kod ID {idnum}")
            break
        idnum -= 1
        time.sleep(pause)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--broj", type=int, default=1500)
    ap.add_argument("--start", type=int, default=None, help="pocetni ID (default: auto iz RSS-a)")
    ap.add_argument("--pause", type=float, default=0.6)
    args = ap.parse_args()

    rows = scrape(args.broj, args.start, args.pause)
    today = _dt.date.today().isoformat()
    out = DATA_RAW / f"mozzart_bulk_{today}.csv"
    save_csv(rows, out)
    print(f"\nSnimljeno {len(rows)} naslova -> {out}")


if __name__ == "__main__":
    main()
