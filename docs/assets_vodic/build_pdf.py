#!/usr/bin/env python3
"""Sastavlja 'Vodic-kroz-projekat' HTML (sa ugradjenim slikama) i sprema za PDF.

HTML se renderuje u PDF preko headless Chrome-a (vidi build komandu ispod).
Sve slike se ugradjuju kao base64 da PDF bude samostalan.
"""
import base64
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ASSETS = os.path.join(ROOT, "docs", "assets_vodic")
FIGS = os.path.join(ROOT, "report", "figures")
OUT_HTML = os.path.join(ROOT, "docs", "assets_vodic", "_vodic_build.html")


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def img(path, caption="", width="100%"):
    src = f"data:image/png;base64,{b64(path)}"
    cap = f'<div class="cap">{caption}</div>' if caption else ""
    return f'<figure style="width:{width}"><img src="{src}"/>{cap}</figure>'


A = lambda n: os.path.join(ASSETS, n)
F = lambda n: os.path.join(FIGS, n)

CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
* { box-sizing: border-box; }
body { font-family: -apple-system, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
       color: #1f2d3d; line-height: 1.55; font-size: 11.2pt; }
h1,h2,h3 { color: #1a2733; line-height: 1.2; }
h1 { font-size: 22pt; }
h2 { font-size: 16.5pt; border-bottom: 3px solid #2E86DE; padding-bottom: 5px; margin-top: 4px; }
h3 { font-size: 12.8pt; color: #2E86DE; margin-bottom: 2px; }
p { margin: 7px 0; text-align: justify; }
figure { margin: 14px auto; text-align: center; page-break-inside: avoid; }
figure img { width: 100%; border: 1px solid #e3e8ee; border-radius: 6px; }
.cap { font-size: 9.3pt; color: #66707a; margin-top: 4px; font-style: italic; }
.section { page-break-before: always; }
.lead { font-size: 12pt; color: #3a4a5a; }
.note { background: #EBF5FB; border-left: 5px solid #2E86DE; padding: 9px 13px; border-radius: 4px; margin: 11px 0; }
.warn { background: #FEF9E7; border-left: 5px solid #F39C12; padding: 9px 13px; border-radius: 4px; margin: 11px 0; }
.good { background: #EAFAF1; border-left: 5px solid #27AE60; padding: 9px 13px; border-radius: 4px; margin: 11px 0; }
.key  { background: #F4ECF7; border-left: 5px solid #8E44AD; padding: 9px 13px; border-radius: 4px; margin: 11px 0; }
b, strong { color: #14202b; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10.3pt; page-break-inside: avoid; }
th, td { border: 1px solid #d4dae1; padding: 6px 9px; text-align: center; }
th { background: #2E86DE; color: white; }
tr:nth-child(even) td { background: #f6f9fc; }
.win { background: #d5f5e3 !important; font-weight: bold; }
ul { margin: 6px 0 6px 0; padding-left: 22px; }
li { margin: 3px 0; }
.cover { text-align: center; padding-top: 60px; }
.cover .t { font-size: 27pt; font-weight: 800; color: #1a2733; margin-bottom: 6px; }
.cover .s { font-size: 14pt; color: #2E86DE; margin-bottom: 40px; }
.cover .meta { font-size: 11pt; color: #66707a; margin-top: 8px; }
.toc { font-size: 11.5pt; }
.toc li { margin: 5px 0; }
.q { color:#8E44AD; font-weight:bold; }
"""

HTML = f"""<!doctype html><html lang="sr"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>

<!-- ===================== KORICE ===================== -->
<div class="cover">
  <div class="t">Detekcija klikbejta<br>u srpskim sportskim naslovima</div>
  <div class="s">Vodič kroz projekat — objašnjeno od nule, uz slike</div>
  {img(A('01_pipeline.png'), '', '92%')}
  <div class="meta"><b>Obrada prirodnih jezika 2025/2026 — ETF</b></div>
  <div class="meta">Filip Nikolić (25/3234) &nbsp;·&nbsp; Danilo Nikolić (25/3235)</div>
  <div class="meta">Ovaj dokument objašnjava <i>šta</i> smo radili, <i>kako</i> to radi i <i>zašto</i> baš tako —
  pretpostavljajući da o oblasti ne znate ništa unapred.</div>
</div>

<!-- ===================== SADRŽAJ ===================== -->
<div class="section">
<h2>Sadržaj</h2>
<ol class="toc">
  <li>Šta uopšte pravimo? (problem na jednom primeru)</li>
  <li>Ceo tok projekta u 4 koraka</li>
  <li>Faza 1 — odakle podaci</li>
  <li>Faza 2 — kako smo „naučili" računar šta je klikbejt</li>
  <li>Kako mašina uopšte uči (osnovni pojmovi)</li>
  <li>Kako merimo da li je model dobar</li>
  <li>Faza 3a — jednostavni modeli (vreća reči)</li>
  <li>Faza 3b — neuronska mreža (BERT): srce projekta</li>
  <li>Faza 3c — veliki jezički model (Claude) bez obuke</li>
  <li>Rezultati i zaključak</li>
</ol>
</div>

<!-- ===================== 1 ===================== -->
<div class="section">
<h2>1 · Šta uopšte pravimo?</h2>
<p class="lead">Pravimo program koji pročita <b>naslov sportske vesti</b> i kaže da li je to
<b>„klikbejt"</b> (naslov koji vas vara da kliknete) ili <b>„regularan"</b> naslov
(pošteno vam kaže šta se desilo).</p>

<p><b>Klikbejt</b> (od engleskog <i>click</i> = klik, <i>bait</i> = mamac) je naslov napravljen
tako da vas <b>natera na klik</b>, a ne da vas informiše. Tipičan trik: sakrije ključnu
informaciju da biste morali da otvorite članak. Naš zadatak je da to automatski prepoznamo.
U informatici se ovakav zadatak zove <b>klasifikacija teksta</b> — svrstavanje teksta u jednu
od unapred poznatih grupa (ovde: dve grupe, „klikbejt" i „regularan").</p>

{img(A('02_klikbejt.png'), 'Primer: levo klikbejt (krije ko/šta), desno regularan naslov. Klikbejt prepoznajemo po 4 mehanizma manipulacije.')}

<div class="note"><b>Zašto je ovo teško?</b> Klikbejt nije samo uzvičnik ili velika slova.
Često je suptilan — ista rečenica može biti i poštena i manipulativna, zavisno od toga
<i>šta krije</i>. Zato program mora da razume <b>smisao</b>, ne samo da prebroji reči.</div>
</div>

<!-- ===================== 2 ===================== -->
<div class="section">
<h2>2 · Ceo tok projekta u 4 koraka</h2>
<p>Svaki ovakav projekat ide istim redom: prvo skupiš podatke, pa ih ručno označiš,
pa naučiš program da pogađa, pa sve to opišeš. To su naše četiri faze:</p>
{img(A('01_pipeline.png'), 'Četiri faze: prikupljanje → ručno označavanje → modeli (obuka i provera) → dokumentacija.', '95%')}
<ul>
  <li><b>Faza 1 – Prikupljanje:</b> skupili smo skoro 3000 naslova sa sajta SportKlub.</li>
  <li><b>Faza 2 – Anotacija:</b> ručno smo svakom naslovu dodelili oznaku 1 (klikbejt) ili 0 (regularan).</li>
  <li><b>Faza 3 – Modeli:</b> naučili smo tri vrste programa da pogađaju oznaku i izmerili ko je najbolji.</li>
  <li><b>Faza 4 – Dokumentacija:</b> napisali izveštaj sa rezultatima (ovaj dokument je deo toga).</li>
</ul>
</div>

<!-- ===================== 3 ===================== -->
<div class="section">
<h2>3 · Faza 1 — odakle podaci</h2>
<p>Da bi program nešto naučio, mora da vidi <b>mnogo primera</b>. Skupili smo
<b>2994 različita naslova</b> sa portala <b>SportKlub</b> (automatski, preko njihovog
veb interfejsa), uklonili duplikate i za svaki zapisali odakle je (link, rubrika, datum).</p>
<div class="note"><b>Zašto samo jedan sajt?</b> Da program uči razliku <i>klikbejt vs regularno</i>,
a ne razliku <i>SportKlub vs neki drugi portal</i>. Kad su svi naslovi sa istog mesta,
jedina razlika koju može da nauči je upravo ona koja nas zanima.</div>
</div>

<!-- ===================== 4 ===================== -->
<div class="section">
<h2>4 · Faza 2 — kako smo „naučili" računar šta je klikbejt</h2>
<p>Računar ne zna unapred šta je klikbejt. Mi mu to pokazujemo tako što <b>sami</b>
označimo hiljade naslova. Ali da bismo bili sigurni da je naša definicija jasna,
prvo smo uradili <b>kalibraciju</b>: oba člana tima su <b>nezavisno</b> (svako za sebe,
bez dogovaranja) ocenila istih 220 naslova. Pa smo uporedili koliko se slažemo.</p>

{img(A('03_kappa.png'), 'Kalibracija: dva čoveka nezavisno ocene iste naslove, pa merimo slaganje. Visoko slaganje = definicija je jasna.')}

<p>Slagali smo se u <b>82.7%</b> slučajeva. Ali postoji bolji način merenja od pukog procenta —
<b>Cohen-ova kapa (κ)</b>. Ona je stroža jer oduzima slaganje koje bi se desilo i čistim
nagađanjem. Dobili smo <b>κ = 0.64</b>, što spada u „dobro" slaganje (cilj je bio ≥ 0.6).</p>

<div class="good"><b>Šta nam to govori?</b> Naša neslaganja bila su na <i>suptilnim</i>,
graničnim naslovima — ne na očiglednim. To znači da zadatak nije trivijalan i da je naša
definicija dovoljno dobra da se na nju oslonimo.</div>

<p>Nakon kalibracije, podelili smo ostatak posla na pola i označili sve. Konačni skup za
treniranje je <b>balansiran</b>: <b>1100 klikbejt + 1100 regularnih = 2200 naslova</b>.</p>

{img(F('raspodela_klasa.png'), 'Konačni skup je namerno 50:50. Balans je važan da program ne bi „švercovao" tako što uvek pogađa češću klasu.', '62%')}

<div class="note"><b>Zašto baš 50:50?</b> Ako bi 95% naslova bilo regularno, program koji
uvek kaže „regularno" imao bi 95% tačnost — a zapravo ništa ne bi naučio. Balansiran skup
sprečava ovu varku i čini merenje uspeha poštenim.</div>
</div>

<!-- ===================== 5 ===================== -->
<div class="section">
<h2>5 · Kako mašina uopšte uči (osnovni pojmovi)</h2>
<p>Pre nego što opišemo modele, evo tri pojma koja sve objašnjavaju. Zamislite učenika
koji se sprema za ispit iz zbirke zadataka.</p>

<h3>Premalo vs taman vs previše učenja</h3>
{img(A('06_fitting.png'), 'Tačkice su podaci, linija je ono što je model naučio. Levo: presimplifikovano. Sredina: taman. Desno: model je „nabubao" i šum.')}
<ul>
  <li><b>Premalo (underfitting):</b> učenik je naučio premalo pravila — greši čak i na poznatom.</li>
  <li><b>Taman:</b> uhvatio je pravo pravilo — dobro radi i na novim zadacima.</li>
  <li><b>Previše (overfitting):</b> učenik je <i>napamet nabubao</i> baš te zadatke, uključujući
  i slučajne detalje — na novom zadatku se izgubi. Ovo je glavna opasnost.</li>
</ul>

<h3>Zašto se ne sme proveravati na istim zadacima na kojima se učilo</h3>
<p>Ako učenika ispitate baš iz zadataka koje je vežbao, dobićete lažno visoku ocenu.
Zato uspeh merimo na <b>novim</b> naslovima koje model nije video tokom učenja.</p>

<h3>Unakrsna validacija — pošteno merenje sa malo podataka</h3>
<p>Imamo „samo" 2200 naslova. Da iskoristimo svaki, koristimo <b>10-struku unakrsnu validaciju</b>:
podelimo podatke na 10 delova; u 10 prolaza svaki put 9 delova služi za učenje, a 1 (uvek drugi)
za proveru. Konačna ocena je prosek svih 10 prolaza.</p>
{img(A('07_kfold.png'), 'Svaki deo jednom postane „test". Tako je svaki naslov bar jednom proveren, a ocena je stabilnija.', '78%')}

<h3>Ugnežđena validacija — da izbor podešavanja ne „vara"</h3>
<p>Modeli imaju „dugmiće" (npr. jačina regularizacije) koje treba podesiti. Ako bismo ih
podešavali gledajući isti test, varali bismo. Zato se podešavanje radi u <b>unutrašnjoj</b>
petlji, odvojeno od konačne provere u <b>spoljnoj</b> petlji.</p>
{img(A('08_nested.png'), 'Test deo nikad ne učestvuje u biranju podešavanja → poštena, neiskvarena ocena.', '88%')}
</div>

<!-- ===================== 6 ===================== -->
<div class="section">
<h2>6 · Kako merimo da li je model dobar</h2>
<p>Kad model pogađa, postoje četiri ishoda. Skupljamo ih u <b>matricu zabune</b>:</p>
{img(A('09_confusion.png'), 'Pogodci i greške. „Pozitivna" klasa nam je klikbejt — to je ono što želimo da uhvatimo.', '80%')}
<ul>
  <li><b>Preciznost:</b> kad model kaže „klikbejt", koliko često je u pravu? (malo lažnih uzbuna)</li>
  <li><b>Odziv (recall):</b> od svih pravih klikbejtova, koliko ih je uhvatio? (malo promašenih)</li>
  <li><b>F1:</b> jedan broj koji balansira preciznost i odziv — naša glavna ocena.</li>
  <li><b>ROC-AUC:</b> meri koliko dobro model <i>rangira</i> klikbejt iznad regularnog;
  pokazuje kvalitet „sigurnosti" modela, ne samo konačnu odluku.</li>
</ul>
<div class="note">Sve modele merimo <b>istim metrikama</b> i <b>istim postupkom</b> —
samo tako je poređenje pošteno.</div>
</div>

<!-- ===================== 7 ===================== -->
<div class="section">
<h2>7 · Faza 3a — jednostavni modeli („vreća reči")</h2>
<p>Prvo pravimo <b>najjednostavnije moguće</b> modele kao <b>donju lestvicu</b> (baseline).
Bez njih ne bismo znali da li je složeni model stvarno dobar ili samo deluje tako.</p>

<h3>Korak 1: pretvoriti reči u brojeve</h3>
<p>Računar ne razume slova — razume brojeve. Najjednostavniji način: <b>vreća reči</b>.
Naslov pretvorimo u listu reči, a zatim u vektor koji broji koja se reč javlja.
Redosled reči se <b>ignoriše</b> — otud „vreća".</p>
{img(A('04_bow.png'), 'Naslov → reči → vektor brojeva. Ovo je ulaz za jednostavne modele.', '95%')}

<h3>Korak 2: nisu sve reči podjednako važne (TF-IDF)</h3>
<p>Reč „je" se javlja svuda i ne govori ništa; retka, karakteristična reč govori mnogo.
<b>TF-IDF</b> daje veću težinu retkim, informativnim rečima.</p>
{img(A('05_tfidf.png'), 'TF-IDF = koliko je reč česta u naslovu × koliko je retka u celom skupu.', '90%')}

<h3>Modeli koje smo probali</h3>
<p>Dva klasična: <b>logistička regresija</b> (uči težinu svake reči) i <b>naivni Bajes</b>
(računa verovatnoće na osnovu toga koje se reči javljaju u kojoj klasi). Najbolji rezultat
dao je naivni Bajes.</p>

<div class="warn"><b>Iskren nalaz:</b> ovi modeli gledaju reči <i>izolovano</i>, pa hvataju samo
površinske obrasce. Klikbejt koji zavisi od konstrukcije rečenice im izmiče. Najbolji
baseline ima <b>F1 = 0.646</b> — to je lestvica koju složeniji modeli treba da preskoče.</div>
</div>

<!-- ===================== 8 ===================== -->
<div class="section">
<h2>8 · Faza 3b — neuronska mreža (BERT): srce projekta</h2>
<p class="lead">Ovo je najvažniji deo. Umesto da gleda reči izolovano, ovaj model čita
<b>ceo naslov u kontekstu</b> — razume da „Nećete verovati šta…" jeste manipulacija,
bez obzira na pojedinačne reči.</p>

<h3>Dve vrste „velikih jezičkih modela"</h3>
{img(A('13_encdec.png'), 'Enkoder (BERT) razume tekst i može se dotrenirati kod nas. Dekoder (Claude) generiše tekst i samo ga pitamo.', '95%')}

<h3>Šta je BERT i kako „misli"</h3>
<p><b>BERT</b> je neuronska mreža (mreža sloj-na-sloj povezanih „neurona") posebno napravljena
za jezik. Naslov prolazi kroz nekoliko koraka:</p>
{img(A('10_bert.png'), 'Put naslova kroz BERT: tokenizacija → vektori → slojevi pažnje (kontekst) → [CLS] sažetak → odluka.', '98%')}
<ul>
  <li><b>Tokenizacija:</b> tekst se iseče na delove reči (npr. „pojačanje" → „poja-" + „##čanje").
  Dodaju se posebne oznake [CLS] (početak) i [SEP] (kraj).</li>
  <li><b>Vektori (embedding):</b> svaki delić dobije svoj niz brojeva + informaciju o poziciji.</li>
  <li><b>Self-attention (pažnja):</b> srce mreže — svaka reč „pogleda" sve ostale i pokupi
  kontekst od njih. Tako značenje reči zavisi od okoline.</li>
  <li><b>Odluka:</b> poseban [CLS] vektor sažme ceo naslov i mali završni sloj kaže 1 ili 0.</li>
</ul>
{img(A('11_attention.png'), 'Mehanizam pažnje: reč „verovati" pokuplja jak signal od „Nećete" i „uradio" → prepoznaje manipulativnu frazu.', '85%')}

<h3>Trik: ne učimo jezik od nule (transferno učenje)</h3>
<p>Naučiti mrežu „šta je srpski" zahteva milijarde rečenica i ogromne računare. Zato uzimamo
mrežu koju je <b>neko već unapred istrenirao</b> na ogromnom tekstu, pa je samo <b>blago
doteramo</b> na našim 2200 naslova. To se zove <b>fine-tuning</b>.</p>
{img(A('12_transfer.png'), 'Pretrening (tuđi, skup) + fino doterivanje (naš, jeftin) = gotov klasifikator. Zato je dovoljno malo primera.', '95%')}

<h3>Dva modela koja smo poredili</h3>
<ul>
  <li><b>BERTić</b> — istreniran <b>baš za srpski</b> (i srodne jezike).</li>
  <li><b>mBERT</b> — „višejezični", zna 104 jezika odjednom, pa nijedan savršeno.</li>
</ul>
<p>Probali smo i različit broj „prolaza kroz podatke" (epoha): 2, 3 i 4.</p>
{img(F('kriva_ucenja.png'), 'Sa 2 epohe model je nedovoljno istreniran; 3–4 epohe daju najbolji rezultat. Dalje nema dobitka.', '70%')}

<table>
<tr><th>Model</th><th>Epohe</th><th>F1 (klikbejt)</th><th>Tačnost</th><th>ROC-AUC</th></tr>
<tr><td>BERTić</td><td>2</td><td>0.681</td><td>0.680</td><td>0.760</td></tr>
<tr class="win"><td>BERTić</td><td>3–4</td><td>0.703</td><td>0.704</td><td>0.788</td></tr>
<tr><td>mBERT</td><td>2</td><td>0.651</td><td>0.664</td><td>0.736</td></tr>
<tr><td>mBERT</td><td>3</td><td>0.690</td><td>0.687</td><td>0.753</td></tr>
</table>

<div class="good"><b>Zaključak faze:</b> <b>BERTić &gt; mBERT</b> (namenski srpski model je bolji),
a <b>oba ubedljivo nadmašuju baseline</b>. To je glavni dokaz projekta: razumevanje konteksta
hvata suptilni klikbejt koji „vreća reči" ne može.</div>
</div>

<!-- ===================== 9 ===================== -->
<div class="section">
<h2>9 · Faza 3c — veliki jezički model (Claude) bez obuke</h2>
<p>Modeli tipa <b>ChatGPT / Claude</b> su ogromni i zatvoreni — ne možemo ih dotrenirati.
Ali možemo ih jednostavno <b>pitati</b>. To zovemo <b>zero-shot</b>: damo uputstvo i naslov,
i tražimo odgovor 1 ili 0 — <b>bez ijednog primera za obuku</b>.</p>
{img(A('14_prompt.png'), 'Damo modelu uputstvo (prompt) i naslov; on vrati 1 ili 0. Nema treniranja — samo pitanje i odgovor.', '95%')}

<p>Postavka traži da uporedimo <b>jezik uputstva</b>: srpski vs engleski prompt.
Važno: <b>naslovi su uvek srpski</b> — menja se samo jezik instrukcije modelu.</p>
<table>
<tr><th>Varijanta upita</th><th>F1 (klikbejt)</th><th>Tačnost</th><th>Preciznost</th><th>Odziv</th></tr>
<tr><td>Srpski prompt</td><td>0.710</td><td>0.695</td><td>0.676</td><td>0.748</td></tr>
<tr class="win"><td>Engleski prompt</td><td>0.715</td><td>0.691</td><td>0.664</td><td>0.775</td></tr>
</table>
<p><b>Nalaz:</b> srpski i engleski prompt daju gotovo isti rezultat. Model bez ijednog primera
za obuku postiže <b>najviši F1 u celom projektu (0.715)</b> — impresivno.</p>
<div class="note">Koristili smo <b>Claude</b> (jeftin, ~$1 za ceo skup) jer besplatni Gemini nije
bio dostupan, a postavka izričito dozvoljava „i druge" generativne modele.</div>
</div>

<!-- ===================== 10 ===================== -->
<div class="section">
<h2>10 · Rezultati i zaključak</h2>
<p>Konačno poređenje svih pristupa po glavnoj metrici (F1 na klikbejt klasi):</p>
{img(A('15_results.png'), 'Svi modeli su iznad baseline-a. Kontekstualni modeli (BERTić, Claude) jasno vode.', '78%')}
{img(F('poredjenje_modela.png'), 'Isti zaključak, prikaz iz zvaničnog izveštaja.', '70%')}

<table>
<tr><th>Model</th><th>Tip</th><th>F1 (kb)</th><th>Tačnost</th><th>ROC-AUC</th></tr>
<tr><td>Naivni Bajes</td><td>baseline (vreća reči)</td><td>0.646</td><td>0.622</td><td>0.676</td></tr>
<tr><td>mBERT</td><td>neuronska mreža (višejezična)</td><td>0.690</td><td>0.687</td><td>0.753</td></tr>
<tr class="win"><td>BERTić</td><td>neuronska mreža (srpska)</td><td>0.703</td><td>0.704</td><td>0.788</td></tr>
<tr class="win"><td>Claude (EN)</td><td>generativni, bez obuke</td><td>0.715</td><td>0.691</td><td>—</td></tr>
</table>

<h3>Šta smo naučili</h3>
<ul>
  <li><b>Svi modeli su bolji od baseline-a</b> — razumevanje konteksta pobeđuje brojanje reči.</li>
  <li><b>Claude</b> ima najviši F1 iako nije ni treniran — snaga ogromnih jezičkih modela.</li>
  <li><b>BERTić</b> je najbolji po tačnosti i jedini daje pouzdane „verovatnoće" (ROC-AUC),
  a uz to je mali, besplatan i radi lokalno.</li>
  <li>Za srpski je <b>namenski model bolji</b> od višejezičnog.</li>
</ul>

<div class="key"><b>Preporuka:</b> za stvarnu upotrebu → <b>BERTić</b> (besplatan, lokalan,
pouzdan). Kada nema podataka za obuku → <b>Claude</b> u zero-shot režimu. Jednostavni modeli
ostaju korisni kao brza, providna referenca.</div>

<p style="margin-top:18px; color:#66707a; font-size:10pt;"><i>Kraj vodiča. Za tehničke detalje i
komande videti <b>docs/Sve-o-projektu.md</b> i <b>docs/Radni-izvestaj.md</b>.</i></p>
</div>

</body></html>
"""

if __name__ == "__main__":
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(HTML)
    print("HTML napisan:", OUT_HTML, f"({len(HTML)//1024} KB)")
