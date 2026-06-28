# Workflow détaillé — constat-drone

Pipeline pour produire un constat drone enrichi (.docx) à partir de **deux entrées** :
- un **DOCX brouillon** (dictée des constatations, format constat-reecriture — fait foi pour l'identité) ;
- un **PDF « expédition »** Juris Drone (toutes les données et le texte drone, + cartes).

Chemins (adapter `<session>`) :
```bash
SKILL="/sessions/<session>/mnt/.claude/skills/constat-drone"
REECR="/sessions/<session>/mnt/.claude/skills/constat-reecriture"
DOCXSK="/sessions/<session>/mnt/.claude/skills/docx/scripts/office"
WORK="/sessions/<session>/constat_drone_work"
```

## Étape 0 — Préparation
```bash
rm -rf "$WORK" && mkdir -p "$WORK/unpacked" "$WORK/annexes"
python3 "$DOCXSK/unpack.py" "<brouillon>.docx" "$WORK/unpacked"
```

## Étape 1 — Lire les deux sources
1. Lire le DOCX (`document.xml`) : demandeurs + genre, date (« L'AN … »), adresse mission, paragraphes
   de constatations (après « J'AI PROCÉDÉ AUX CONSTATATIONS SUIVANTES »), clôture, position du bloc signature.
2. Lire le PDF (Read natif, page à page) : remplir le **tableau des variables** de
   `references/boilerplate-drone.md` (n° série, enregistrement, certificat télépilote, classe, masse,
   sous-catégorie, hauteur max, commune, assurance, dates DGAC, METAR si présent…).
3. **Réconcilier** (règle D1) : l'identité du DOCX prime. Noter les divergences.

## Étape 2 — Extraire les images du PDF (annexes)
```bash
python3 "$SKILL/scripts/extract_pdf_images.py" "<pdf>" "$WORK/annexes" --min-size 400
```
Produit `annexe_1.png … annexe_N.png` (logo et vignettes filtrés par `--min-size`) + un `manifest.json`
(page, dimensions) pour aider à rédiger les légendes.

## Étape 3 — Réécrire les constatations
Appliquer **toutes les règles de constat-reecriture** + `rules-drone.md` (A1–A3) : style « Je constate »,
Dicobat, descriptif, zéro lien causal, périmètre = dictée. Remplacer les paragraphes bruts dans
`document.xml` (via `Edit` ou script de bornes `<w:p>`).

## Étape 4 — Civilité + intro de requête + enrichissement « DÉFÉRANT »
- Civilité des demandeurs (règle 15 / `fix_demandeurs.py` de constat-reecriture).
- Intro 3 paragraphes (règle 16) à la place de la phrase orpheline (« Constat avant travaux »).
- Compléter le bloc « DÉFÉRANT » avec la qualité d'exploitant + télépilote (SECTION 1 du boilerplate).

## Étape 5 — Préparer le style Heading1 + injecter les sections drone
```bash
python3 "$SKILL/scripts/add_heading_style.py" "$WORK/unpacked"   # crée Heading1 si absent, pageBreakBefore
```
Puis injecter, **aux bons emplacements** (ordre E1 de rules-drone.md), les sections du boilerplate avec
`{{placeholders}}` résolus :
- SECTION 2 avant « J'AI PROCÉDÉ AUX CONSTATATIONS »
- SECTION 3 après les constatations, avant la clôture
- SECTIONS 4→7 après le bloc signature
- SECTION 8 (ANNEXES) tout à la fin, avec les images extraites + légendes

L'injection se fait en construisant des `<w:p>` (titres = `Heading1`, corps = `HOParagraphe`, listes à
puces = style liste ou tiret « — » en début de ligne) et en les insérant dans `document.xml`.
Pour les images : ajouter le binaire dans `word/media/`, déclarer la relation dans
`word/_rels/document.xml.rels`, référencer via `<w:drawing>` (voir helper `scripts/insert_image.py`).

## Étape 6 — Mise en page
```bash
python3 "$REECR/scripts/apply_layout.py" "$WORK/unpacked"      # pageBreakBefore Heading1, justif HOParagraphe, updateFields
```
Le Sommaire (TOC \o "1-4") se peuplera automatiquement à l'ouverture avec les nouveaux titres Heading1.

## Étape 7 — Validation + repack
```bash
python3 -c "import xml.etree.ElementTree as ET; [ET.parse(f'$WORK/unpacked/word/{f}') for f in ['document.xml','styles.xml','settings.xml']]; print('XML OK')"
python3 "$DOCXSK/pack.py" "$WORK/unpacked" "<out>/PV CONSTAT <NOM> <JJ.MM.AAAA>.docx" --original "<brouillon>.docx"
```

## Étape 8 — Livraison
`present_files` sur le .docx final. Message court : rappeler l'ordre des sections drone ajoutées, le
nombre d'annexes, les divergences PDF/DOCX réconciliées, et laisser Antoine relire.

## Itération
Ajustement ciblé → modifier les `<w:p>` concernés, ne pas tout régénérer ; repack.
Si une nouvelle préférence terminologique est validée, l'ajouter à `constat-reecriture/references/vocabulary.md`.
