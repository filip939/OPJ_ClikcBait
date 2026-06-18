#!/usr/bin/env python3
"""Generiše sve dijagrame za 'Vodic-kroz-projekat.pdf' (objašnjenja za pocetnike).

Svaki dijagram je samostalna PNG slika sa srpskim oznakama. Pokretanje:
    .venv/bin/python docs/assets_vodic/make_diagrams.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["svg.fonttype"] = "none"

OUT = os.path.dirname(os.path.abspath(__file__))

# paleta
C_KB   = "#E74C3C"   # klikbejt (crveno)
C_REG  = "#27AE60"   # regularan (zeleno)
C_BLUE = "#2E86DE"
C_PURP = "#8E44AD"
C_BOX  = "#EAF2FB"
C_BORD = "#34495E"
C_GRAY = "#95A5A6"
C_YELL = "#F39C12"


def box(ax, x, y, w, h, text, fc=C_BOX, ec=C_BORD, fs=11, bold=False, tc="#1A1A1A",
        rounding=0.02, lw=1.6):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.01,rounding_size={rounding}",
                       fc=fc, ec=ec, lw=lw, zorder=2)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color=tc, zorder=3, wrap=True)


def arrow(ax, x1, y1, x2, y2, color=C_BORD, lw=2.2, style="-|>", ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=18,
                        color=color, lw=lw, linestyle=ls, zorder=1,
                        shrinkA=2, shrinkB=2)
    ax.add_patch(a)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  +", name)


# ---------------------------------------------------------------- 1. PIPELINE
def d_pipeline():
    fig, ax = plt.subplots(figsize=(11, 2.7))
    ax.set_xlim(0, 11); ax.set_ylim(0, 2.7); ax.axis("off")
    steps = [
        ("FAZA 1\nPrikupljanje\npodataka", "2994 naslova\nsa SportKlub", C_BLUE),
        ("FAZA 2\nAnotacija\n(rucno)", "1=klikbejt / 0=reg.\nκ=0.64", C_PURP),
        ("FAZA 3\nModeli\n(obuka+test)", "baseline / BERT /\nClaude", C_KB),
        ("FAZA 4\nDokumentacija", "izvestaj +\ngrafici", C_REG),
    ]
    w = 2.3; gap = 0.5; x = 0.2
    for i, (t, sub, c) in enumerate(steps):
        box(ax, x, 0.9, w, 1.3, t, fc="white", ec=c, fs=12, bold=True, tc=c, lw=2.4)
        ax.text(x + w / 2, 0.5, sub, ha="center", va="center", fontsize=9, color="#444")
        if i < 3:
            arrow(ax, x + w, 1.55, x + w + gap, 1.55, color=C_GRAY, lw=2.6)
        x += w + gap
    ax.text(5.5, 2.55, "Tok celog projekta", ha="center", fontsize=13, fontweight="bold")
    save(fig, "01_pipeline.png")


# ---------------------------------------------------- 2. KLIKBEJT VS REGULARAN
def d_klikbejt():
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.set_xlim(0, 11); ax.set_ylim(0, 4.2); ax.axis("off")
    # klikbejt
    box(ax, 0.3, 2.5, 5.0, 1.4, "", fc="#FDEDEC", ec=C_KB, lw=2.4)
    ax.text(2.8, 3.6, "✗ KLIKBEJT (1)", ha="center", fontsize=13, fontweight="bold", color=C_KB)
    ax.text(2.8, 3.05, '„Nećete verovati šta je\nkapiten uradio posle meča!"',
            ha="center", fontsize=11, style="italic", color="#7B241C")
    # regularan
    box(ax, 5.7, 2.5, 5.0, 1.4, "", fc="#EAFAF1", ec=C_REG, lw=2.4)
    ax.text(8.2, 3.6, "✓ REGULARAN (0)", ha="center", fontsize=13, fontweight="bold", color=C_REG)
    ax.text(8.2, 3.05, '„Partizan pobedio Zvezdu\n2:1 u 165. derbiju"',
            ha="center", fontsize=11, style="italic", color="#196F3D")
    # 4 mehanizma
    ax.text(5.5, 2.15, "4 mehanizma manipulacije (dovoljan je 1 za oznaku „klikbejt”):",
            ha="center", fontsize=11, fontweight="bold")
    mech = [
        ("Kognitivni jaz", "krije ključnu\ninformaciju"),
        ("Preuveličavanje", "rutina = senzacija"),
        ("Emocionalni naboj", "veštačka napetost"),
        ("Senzac. fraza", "„a onda se desilo…"),
    ]
    w = 2.45; x = 0.3
    for t, s in mech:
        box(ax, x, 0.5, w, 1.2, f"{t}\n\n{s}", fc="#FEF9E7", ec=C_YELL, fs=10, lw=1.8)
        x += w + 0.2
    save(fig, "02_klikbejt.png")


# ------------------------------------------------------------- 3. ANOTACIJA/KAPPA
def d_kappa():
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.6); ax.axis("off")
    ax.text(5, 3.4, "Kalibracija: 220 naslova oba člana ocenila NEZAVISNO",
            ha="center", fontsize=12, fontweight="bold")
    # dva anotatora
    box(ax, 0.4, 1.9, 2.0, 0.9, "Filip\nocenjuje", fc="white", ec=C_BLUE, fs=11, bold=True, tc=C_BLUE)
    box(ax, 0.4, 0.5, 2.0, 0.9, "Danilo\nocenjuje", fc="white", ec=C_PURP, fs=11, bold=True, tc=C_PURP)
    arrow(ax, 2.4, 2.35, 3.6, 1.95, color=C_GRAY)
    arrow(ax, 2.4, 0.95, 3.6, 1.55, color=C_GRAY)
    # poredjenje
    box(ax, 3.7, 1.2, 2.4, 1.2, "Poredimo\nodgovore", fc="#F4ECF7", ec=C_PURP, fs=11, bold=True)
    arrow(ax, 6.1, 1.8, 7.0, 1.8, color=C_GRAY)
    # rezultat
    box(ax, 7.05, 1.85, 2.7, 0.95, "Slaganje: 182/220\n= 82.7 %", fc="#EAFAF1", ec=C_REG, fs=11, bold=True, tc="#196F3D")
    box(ax, 7.05, 0.7, 2.7, 0.95, "Cohen κ = 0.640\n(„dobro”, ≥0.6 ✓)", fc="#EBF5FB", ec=C_BLUE, fs=11, bold=True, tc=C_BLUE)
    ax.text(5, 0.15, "κ je strože od procenta: oduzima slaganje koje bi se desilo i čistim nagađanjem.",
            ha="center", fontsize=9.5, color="#555", style="italic")
    save(fig, "03_kappa.png")


# ------------------------------------------------------------- 4. BAG OF WORDS
def d_bow():
    fig, ax = plt.subplots(figsize=(10.5, 3.4))
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 3.4); ax.axis("off")
    ax.text(5.25, 3.2, "Kako računar „vidi” naslov: vreća reči (bag-of-words)",
            ha="center", fontsize=12, fontweight="bold")
    box(ax, 0.3, 2.1, 3.3, 0.8, '„Real ozvaničio\nveliko pojačanje"', fc="white", ec=C_BORD, fs=11)
    arrow(ax, 3.65, 2.5, 4.45, 2.5, color=C_GRAY)
    # tokeni
    toks = ["real", "ozvaničio", "veliko", "pojačanje"]
    x = 4.5
    for t in toks:
        box(ax, x, 2.15, 1.45, 0.7, t, fc="#FEF9E7", ec=C_YELL, fs=9.5)
        x += 1.5
    ax.text(2.0, 1.7, "naslov", ha="center", fontsize=9, color="#888")
    ax.text(7.4, 1.7, "tokeni (reči)", ha="center", fontsize=9, color="#888")
    # vektor
    arrow(ax, 5.2, 2.1, 5.2, 1.35, color=C_GRAY)
    ax.text(5.25, 0.95, "vektor brojeva (koliko se koja reč javlja u celom rečniku):",
            ha="center", fontsize=10)
    vocab = ["…", "pojačanje", "real", "transfer", "veliko", "…"]
    vals  = ["", "1", "1", "0", "1", ""]
    x = 2.0
    for vname, v in zip(vocab, vals):
        fc = "#D5F5E3" if v not in ("", "0") else "white"
        box(ax, x, 0.25, 1.1, 0.55, v if v else "…", fc=fc, ec=C_BORD, fs=11, bold=bool(v))
        ax.text(x + 0.55, 0.05, vname, ha="center", fontsize=7.5, color="#777")
        x += 1.15
    ax.text(9.7, 0.5, "→ ovo\nide u\nmodel", ha="center", fontsize=9, color="#555")
    save(fig, "04_bow.png")


# ------------------------------------------------------------------- 5. TF-IDF
def d_tfidf():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.2); ax.axis("off")
    ax.text(5, 3.0, "TF-IDF: koliko je reč VAŽNA (ne samo koliko je česta)",
            ha="center", fontsize=12, fontweight="bold")
    box(ax, 0.4, 1.5, 2.7, 1.0, "TF\nučestalost u\nnaslovu ↑", fc="#EBF5FB", ec=C_BLUE, fs=11, bold=True, tc=C_BLUE)
    ax.text(3.5, 2.0, "×", ha="center", fontsize=22, fontweight="bold")
    box(ax, 3.9, 1.5, 2.7, 1.0, "IDF\nretkost u celom\nkorpusu ↑", fc="#F4ECF7", ec=C_PURP, fs=11, bold=True, tc=C_PURP)
    ax.text(6.95, 2.0, "=", ha="center", fontsize=22, fontweight="bold")
    box(ax, 7.3, 1.5, 2.3, 1.0, "TF-IDF\ntežina reči", fc="#EAFAF1", ec=C_REG, fs=11, bold=True, tc="#196F3D")
    ax.text(5, 1.0, 'Česte i svuda prisutne reči („je", „u") → mala težina.', ha="center", fontsize=10, color="#555")
    ax.text(5, 0.6, 'Retke, karakteristične reči → velika težina.', ha="center", fontsize=10, color="#555")
    ax.text(5, 0.15, "Na kratkim naslovima razlika je mala — reči se retko ponavljaju.",
            ha="center", fontsize=9.5, color="#999", style="italic")
    save(fig, "05_tfidf.png")


# -------------------------------------------------- 6. UNDER/OVER FITTING
def d_fitting():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.3))
    rng = np.random.default_rng(0)
    x = np.linspace(0, 1, 18)
    y = np.sin(2 * np.pi * x) + rng.normal(0, 0.22, x.size)
    titles = ["NEDOVOLJNO (underfitting)", "TAMAN (dobro)", "PRETERANO (overfitting)"]
    degs = [1, 3, 14]
    cols = [C_GRAY, C_REG, C_KB]
    for ax, t, d, c in zip(axes, titles, degs, cols):
        ax.scatter(x, y, s=22, color="#34495E", zorder=3)
        xx = np.linspace(0, 1, 200)
        cf = np.polyfit(x, y, d)
        ax.plot(xx, np.polyval(cf, xx), color=c, lw=2.6)
        ax.set_title(t, fontsize=11, color=c, fontweight="bold")
        ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-2, 2)
        for s in ax.spines.values():
            s.set_edgecolor("#ccc")
    axes[0].set_ylabel("podaci + naučena kriva", fontsize=9)
    fig.suptitle("Cilj obuke: model koji uhvati pravilo, a ne i šum",
                 fontsize=12, fontweight="bold", y=1.02)
    save(fig, "06_fitting.png")


# ----------------------------------------------------------- 7. K-FOLD CV
def d_kfold():
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.2); ax.axis("off")
    ax.text(5, 4.0, "10-struka unakrsna validacija (ovde prikazano 5 radi jasnoće)",
            ha="center", fontsize=12, fontweight="bold")
    n = 5; cell_w = 1.5; x0 = 1.6; top = 3.4; h = 0.5
    for row in range(n):
        y = top - row * (h + 0.12)
        for col in range(n):
            x = x0 + col * cell_w
            test = (col == row)
            fc = C_KB if test else "#D6EAF8"
            box(ax, x, y, cell_w - 0.1, h, "TEST" if test else "obuka",
                fc=fc, ec=C_BORD, fs=8.5, bold=test, tc="white" if test else "#1A5276")
        ax.text(x0 - 0.15, y + h / 2, f"prolaz {row+1}", ha="right", va="center", fontsize=9)
    ax.text(5, 0.45, "Svaki deo jednom bude TEST. Rezultat = prosek svih prolaza →\n"
                     "pouzdanija ocena, koristi sve podatke.",
            ha="center", fontsize=10, color="#555")
    save(fig, "07_kfold.png")


# ----------------------------------------------------------- 8. NESTED CV
def d_nested():
    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.4); ax.axis("off")
    ax.text(5, 3.2, "Ugnežđena (nested) CV — pošten izbor hiperparametara",
            ha="center", fontsize=12, fontweight="bold")
    box(ax, 0.3, 0.4, 4.4, 2.3, "", fc="#EBF5FB", ec=C_BLUE, lw=2.2)
    ax.text(2.5, 2.4, "SPOLJNA petlja\n(ocena modela)", ha="center", fontsize=11, fontweight="bold", color=C_BLUE)
    box(ax, 0.7, 0.6, 3.6, 1.5, "", fc="#F4ECF7", ec=C_PURP, lw=2.0)
    ax.text(2.5, 1.85, "UNUTRAŠNJA petlja", ha="center", fontsize=10, fontweight="bold", color=C_PURP)
    ax.text(2.5, 1.25, "isproba vrednosti\nhiperparametara\n(npr. C, alpha)\ni izabere najbolju",
            ha="center", fontsize=9.5, color="#444")
    arrow(ax, 4.9, 1.5, 5.7, 1.5, color=C_GRAY)
    box(ax, 5.8, 0.9, 3.9, 1.3, "Test fold se NE koristi\nza izbor → nema curenja\ninformacija (poštena ocena)",
        fc="#EAFAF1", ec=C_REG, fs=10, bold=True, tc="#196F3D")
    save(fig, "08_nested.png")


# ------------------------------------------------------- 9. CONFUSION MATRIX
def d_confusion():
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    ax.set_xlim(0, 8.5); ax.set_ylim(0, 4.4); ax.axis("off")
    ax.text(4.25, 4.2, "Matrica zabune (klikbejt = pozitivna klasa)",
            ha="center", fontsize=12, fontweight="bold")
    cells = [
        (2.2, 2.3, "TP\ntačno klikbejt", C_REG),
        (4.5, 2.3, "FN\nklikbejt promašen", C_KB),
        (2.2, 0.7, "FP\nlažna uzbuna", C_KB),
        (4.5, 0.7, "TN\ntačno regularan", C_REG),
    ]
    for x, y, t, c in cells:
        box(ax, x, y, 2.1, 1.4, t, fc="white", ec=c, fs=11, bold=True, tc=c, lw=2.2)
    ax.text(3.25, 3.85, "Predviđeno", ha="center", fontsize=10, fontweight="bold")
    ax.text(3.25, 3.78, "", ha="center")
    ax.text(2.0, 3.4, "klikbejt", rotation=0, ha="center", fontsize=9, color="#555")
    ax.text(0.55, 1.5, "Stvarno", rotation=90, va="center", fontsize=10, fontweight="bold")
    # formule
    ax.text(7.0, 2.7, "Preciznost =\nTP / (TP+FP)", ha="center", fontsize=10, color=C_BLUE, fontweight="bold")
    ax.text(7.0, 1.6, "Odziv =\nTP / (TP+FN)", ha="center", fontsize=10, color=C_PURP, fontweight="bold")
    ax.text(7.0, 0.6, "F1 = balans\noba (harm. sred.)", ha="center", fontsize=10, color="#196F3D", fontweight="bold")
    save(fig, "09_confusion.png")


# -------------------------------------------------------- 10. BERT ARCH
def d_bert():
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.set_xlim(0, 11); ax.set_ylim(0, 5.2); ax.axis("off")
    ax.text(5.5, 5.0, "Kako radi BERT (enkoderski transformer)", ha="center",
            fontsize=13, fontweight="bold")
    toks = ["[CLS]", "real", "ozvaničio", "poja-", "##čanje", "[SEP]"]
    cols = [C_PURP, C_BORD, C_BORD, C_BORD, C_BORD, C_PURP]
    x0 = 0.7; w = 1.55; y = 0.4
    xs = []
    for i, (t, c) in enumerate(zip(toks, cols)):
        x = x0 + i * (w + 0.12); xs.append(x + w / 2)
        box(ax, x, y, w, 0.55, t, fc="white", ec=c, fs=9.5, bold=(i in (0, 5)), tc=c)
    ax.text(x0 - 0.1, y + 0.27, "ulaz", ha="right", va="center", fontsize=9, color="#888")
    ax.text(5.5, 1.15, "1) Tokenizacija (WordPiece): reči se dele na podreči; [CLS]/[SEP] su posebni tokeni",
            ha="center", fontsize=9.5, color="#555")
    # embeddings row
    ye = 1.5
    for x in xs:
        box(ax, x - 0.6, ye, 1.2, 0.45, "vektor", fc="#FEF9E7", ec=C_YELL, fs=8)
        arrow(ax, x, y + 0.55, x, ye, color=C_GRAY, lw=1.6)
    ax.text(5.5, 2.1, "2) Embedding: svaki token → vektor (+ pozicija u rečenici)",
            ha="center", fontsize=9.5, color="#555")
    # transformer block
    box(ax, 1.2, 2.45, 8.6, 1.1, "", fc="#EBF5FB", ec=C_BLUE, lw=2.2)
    ax.text(5.5, 3.25, "TRANSFORMER SLOJEVI (×12)  —  self-attention",
            ha="center", fontsize=11, fontweight="bold", color=C_BLUE)
    ax.text(5.5, 2.75, "svaka reč „gleda” sve ostale i gradi KONTEKST (značenje zavisi od okoline)",
            ha="center", fontsize=9.5, color="#1A5276")
    for x in xs:
        arrow(ax, x, ye + 0.45, x, 2.45, color=C_GRAY, lw=1.6)
    # CLS out -> classifier
    arrow(ax, xs[0], 3.55, xs[0], 4.15, color=C_PURP, lw=2.4)
    box(ax, xs[0] - 0.9, 4.15, 1.8, 0.55, "[CLS] vektor\n= sažetak naslova", fc="#F4ECF7", ec=C_PURP, fs=8.5, bold=True, tc=C_PURP)
    arrow(ax, xs[0] + 0.9, 4.42, 6.5, 4.42, color=C_BORD, lw=2.2)
    box(ax, 6.6, 4.1, 3.6, 0.7, "Klasifikator → 1 (klikbejt) / 0 (reg.)",
        fc="#EAFAF1", ec=C_REG, fs=10.5, bold=True, tc="#196F3D")
    ax.text(5.5, 3.9, "3) [CLS] vektor sažima ceo naslov i ide u mali klasifikacioni sloj",
            ha="center", fontsize=9.5, color="#555")
    save(fig, "10_bert.png")


# -------------------------------------------------------- 11. SELF-ATTENTION
def d_attention():
    fig, ax = plt.subplots(figsize=(10, 3.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.0); ax.axis("off")
    ax.text(5, 2.85, "Self-attention: reč „verovati” dobija kontekst od ostalih reči",
            ha="center", fontsize=12, fontweight="bold")
    words = ["Nećete", "verovati", "šta", "je", "uradio"]
    weights = [0.9, None, 0.5, 0.2, 0.8]  # pažnja ka 'verovati'
    x0 = 1.0; w = 1.6; y = 1.3
    centers = []
    for i, wd in enumerate(words):
        x = x0 + i * w; centers.append(x)
        focus = (wd == "verovati")
        box(ax, x - 0.7, y, 1.4, 0.6, wd, fc=(C_PURP if focus else "white"),
            ec=C_PURP if focus else C_BORD, fs=10.5, bold=focus, tc="white" if focus else "#1A1A1A")
    cx = centers[1]
    for i, ww in enumerate(weights):
        if ww is None:
            continue
        a = FancyArrowPatch((centers[i], y + 0.62 if i != 1 else y), (cx, y + 0.62),
                            connectionstyle="arc3,rad=0.45", arrowstyle="-|>",
                            mutation_scale=14, color=C_BLUE, lw=1 + 3 * ww, alpha=0.5 + 0.4 * ww)
        ax.add_patch(a)
    ax.text(5, 0.5, "Deblja strelica = veća „pažnja”. Tako model shvata da je „Nećete verovati”\n"
                    "manipulativna konstrukcija — a ne samo skup nezavisnih reči.",
            ha="center", fontsize=9.5, color="#555")
    save(fig, "11_attention.png")


# -------------------------------------------------- 12. TRANSFER LEARNING
def d_transfer():
    fig, ax = plt.subplots(figsize=(11, 3.2))
    ax.set_xlim(0, 11); ax.set_ylim(0, 3.2); ax.axis("off")
    ax.text(5.5, 3.0, "Transferno učenje: ne učimo jezik od nule",
            ha="center", fontsize=12, fontweight="bold")
    box(ax, 0.3, 1.1, 3.4, 1.4, "1) PRETRENING\n(neko drugi, unapred)\n\nogroman tekst,\nuči „šta je srpski”\nbez naših labela",
        fc="#EBF5FB", ec=C_BLUE, fs=9.8, bold=False, tc="#1A5276")
    arrow(ax, 3.75, 1.8, 4.55, 1.8, color=C_GRAY, lw=2.6)
    box(ax, 4.6, 1.1, 3.4, 1.4, "2) FINE-TUNING\n(mi)\n\n2200 naših naslova\nsa labelama →\nblago doteramo model",
        fc="#F4ECF7", ec=C_PURP, fs=9.8, bold=False, tc="#6C3483")
    arrow(ax, 8.05, 1.8, 8.85, 1.8, color=C_GRAY, lw=2.6)
    box(ax, 8.9, 1.25, 1.9, 1.1, "3) GOTOV\nklasifikator\nklikbejta", fc="#EAFAF1", ec=C_REG, fs=10, bold=True, tc="#196F3D")
    ax.text(5.5, 0.55, "Zato je dovoljno malo primera i samo 3–4 epohe (prolaza kroz podatke).",
            ha="center", fontsize=10, color="#555")
    save(fig, "12_transfer.png")


# -------------------------------------------------- 13. ENCODER VS DECODER
def d_encdec():
    fig, ax = plt.subplots(figsize=(10.5, 3.4))
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 3.4); ax.axis("off")
    ax.text(5.25, 3.2, "Dve vrste velikih jezičkih modela koje smo koristili",
            ha="center", fontsize=12, fontweight="bold")
    # encoder
    box(ax, 0.3, 0.4, 4.7, 2.5, "", fc="#EBF5FB", ec=C_BLUE, lw=2.2)
    ax.text(2.65, 2.6, "ENKODER (BERTić, mBERT)", ha="center", fontsize=11, fontweight="bold", color=C_BLUE)
    ax.text(2.65, 1.9, "• čita CEO naslov odjednom\n  (gleda levo i desno)\n"
                       "• mi ga DOTRENIRAVAMO\n• daje verovatnoću klase\n• radi lokalno, besplatno",
            ha="center", fontsize=10, color="#1A5276")
    # decoder
    box(ax, 5.5, 0.4, 4.7, 2.5, "", fc="#FDEDEC", ec=C_KB, lw=2.2)
    ax.text(7.85, 2.6, "DEKODER (Claude)", ha="center", fontsize=11, fontweight="bold", color=C_KB)
    ax.text(7.85, 1.9, "• generiše tekst reč-po-reč\n• ogroman, zatvoren →\n  NE može se dotrenirati\n"
                       "• samo ga PITAMO (prompt)\n• plaća se po pozivu",
            ha="center", fontsize=10, color="#7B241C")
    save(fig, "13_encdec.png")


# -------------------------------------------------- 14. ZERO-SHOT PROMPT
def d_prompt():
    fig, ax = plt.subplots(figsize=(10.5, 3.2))
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 3.2); ax.axis("off")
    ax.text(5.25, 3.0, "Zero-shot: pitamo model bez ijednog primera za obuku",
            ha="center", fontsize=12, fontweight="bold")
    box(ax, 0.3, 0.5, 4.3, 2.1, "PROMPT (uputstvo):\n\n„Odredi da li je ovaj\nsportski naslov\n"
        "KLIKBEJT (1) ili\nREGULARAN (0).\n[definicija…]\nNaslov: …"  ,
        fc="white", ec=C_BORD, fs=10)
    arrow(ax, 4.65, 1.55, 5.55, 1.55, color=C_GRAY, lw=2.6)
    box(ax, 5.6, 0.9, 2.5, 1.3, "CLAUDE\n(jezički model)", fc="#FDEDEC", ec=C_KB, fs=11, bold=True, tc=C_KB)
    arrow(ax, 8.15, 1.55, 9.0, 1.55, color=C_GRAY, lw=2.6)
    box(ax, 9.05, 1.15, 1.2, 0.8, "1", fc="#EAFAF1", ec=C_REG, fs=18, bold=True, tc="#196F3D")
    ax.text(5.25, 0.2, "Testirali smo prompt na srpskom i na engleskom (naslovi su uvek srpski) — rezultat skoro isti.",
            ha="center", fontsize=9.5, color="#555", style="italic")
    save(fig, "14_prompt.png")


# -------------------------------------------------- 15. REZULTATI BAR
def d_results():
    fig, ax = plt.subplots(figsize=(9.5, 4.3))
    models = ["Baseline\n(MNB)", "mBERT", "BERTić", "Claude\n(EN)"]
    f1 = [0.646, 0.690, 0.703, 0.715]
    cols = [C_GRAY, C_BLUE, C_PURP, C_KB]
    bars = ax.bar(models, f1, color=cols, width=0.6, zorder=3, edgecolor="white", lw=1.5)
    for b, v in zip(bars, f1):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.004, f"{v:.3f}",
                ha="center", fontsize=12, fontweight="bold")
    ax.axhline(0.646, color=C_GRAY, ls="--", lw=1.3, zorder=1)
    ax.text(3.4, 0.652, "nivo baseline-a", fontsize=9, color=C_GRAY)
    ax.set_ylim(0.6, 0.74)
    ax.set_ylabel("F1 na klikbejt klasi (više = bolje)", fontsize=11)
    ax.set_title("Svi modeli su bolji od baseline-a; kontekstualni modeli vode",
                 fontsize=12, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25)
    save(fig, "15_results.png")


if __name__ == "__main__":
    print("Generišem dijagrame u:", OUT)
    for fn in [d_pipeline, d_klikbejt, d_kappa, d_bow, d_tfidf, d_fitting,
               d_kfold, d_nested, d_confusion, d_bert, d_attention, d_transfer,
               d_encdec, d_prompt, d_results]:
        fn()
    print("Gotovo.")
