"""Zajednicke funkcije i sema podataka za prikupljanje naslova (Faza 1).

Sema jednog reda (kolone u CSV-u):
    id, naslov, izvor, url, datum, rubrika, datum_scrape, labela

`labela` ostaje prazna u Fazi 1 (popunjava se rucno u Fazi 2 - anotacija).
"""
from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

# Koren projekta = dva nivoa iznad ovog fajla (.../OPJ)
ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"

COLUMNS = ["id", "naslov", "izvor", "url", "datum", "rubrika", "datum_scrape", "labela"]

# Razuman User-Agent (ne lazemo da nismo bot bez razloga, ali saljemo standardan UA)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
    )
}


@dataclass
class Headline:
    naslov: str
    izvor: str
    url: str
    datum: str = ""
    rubrika: str = ""
    datum_scrape: str = ""
    labela: str = ""
    id: str = field(default="")

    def __post_init__(self):
        if not self.id:
            self.id = make_id(self.izvor, self.naslov)
        self.naslov = clean_title(self.naslov)


def make_id(izvor: str, naslov: str) -> str:
    """Stabilan ID: prefiks izvora + hash normalizovanog naslova."""
    norm = normalize_for_dedup(naslov)
    h = hashlib.sha1(norm.encode("utf-8")).hexdigest()[:10]
    return f"{izvor}_{h}"


def clean_title(t: str) -> str:
    """Lagano ciscenje: trim, kolaps razmaka, skidanje sufiksa portala.

    VAZNO: NE diramo uzvicnike, velika slova, navodnike, emoji - to su
    potencijalni klikbejt signali. Prava normalizacija ide tek u Fazi 3.
    """
    t = t.replace("\xa0", " ").strip()
    t = re.sub(r"\s+", " ", t)
    # cesti sufiksi portala
    t = re.sub(r"\s*[|\-–—]\s*(Mozzart Sport|SportKlub|Sport Klub|B92).*$", "", t, flags=re.I)
    return t.strip()


def normalize_for_dedup(t: str) -> str:
    """Agresivnija normalizacija SAMO za poredjenje/dedup i ID (ne za cuvanje)."""
    t = t.lower()
    t = re.sub(r"[^\w\sčćžšđ]", " ", t, flags=re.UNICODE)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def save_csv(rows: list[Headline], path: Path) -> int:
    """Snima listu Headline u UTF-8 CSV. Vraca broj redova."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({k: getattr(r, k) for k in COLUMNS})
    return len(rows)
