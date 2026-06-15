# Faza 1 — Scraping (uputstvo za pokretanje)

## Setup (jednom)
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Bulk prikupljanje (preporučeno — daje hiljade odjednom)
```bash
# SportKlub preko WordPress REST API-ja (~449k clanaka dostupno)
.venv/bin/python src/scraping/sportklub_api.py --broj 1500

# Mozzart preko enumeracije ID-eva clanaka (og:title)
.venv/bin/python src/scraping/mozzart_bulk.py --broj 1500
```
Sa po 1500 sirovih iz svakog izvora (=3000) ima dovoljno rezerve da posle
anotacije i balansiranja izađe 2200 (1100 klikbejt + 1100 regularnih).
**B92 nije potreban.**

## (Alternativa) Dnevni RSS snapshot
```bash
.venv/bin/python src/scraping/rss_scraper.py            # svi RSS izvori
```
Daje samo ~300/dan; koristiti samo za sveže dopune, ne kao glavni izvor.

## Spajanje + deduplikacija
```bash
.venv/bin/python src/scraping/merge.py           # spoji sve iz data/raw/
.venv/bin/python src/scraping/merge.py --prag 90 # stroziji fuzzy dedup
```
Snima `data/interim/headlines.csv` (spreman za anotaciju) i `data/metadata.csv`.

---

## Status izvora
| Izvor | Metod | Status | Kapacitet |
|---|---|---|---|
| **SportKlub** | WP REST API (`/wp-json/wp/v2/posts`) | ✅ radi | ~449.000 članaka, sa rubrikom |
| **Mozzart Sport** | enumeracija ID-eva (`og:title`) | ✅ radi | gusti sekvencijalni ID-jevi, bez rubrike |
| B92 sport | — | ❌ **izbačen** (nema API/RSS, ne treba) | — |

> Dva izvora su dovoljna — broj izvora nije propisan postavkom. Domen
> (sportske vesti) i klasni balans 1100/1100 su ono što je bitno.

## Sledeći koraci u Fazi 1
- [ ] Puni run: `sportklub_api.py --broj 1500` + `mozzart_bulk.py --broj 1500`
- [ ] `merge.py` → proveriti da `data/interim/headlines.csv` ima ~3000 jedinstvenih
- [ ] Ručno pregledati ~50 nasumičnih naslova (kontrola kvaliteta)
- [ ] Predati `data/interim/headlines.csv` u Fazu 2 (anotacija)
