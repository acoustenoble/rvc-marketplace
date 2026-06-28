# Workflow détaillé — constat d'affichage

Chemins : adapter le préfixe de session. Les scripts `unpack.py` / `pack.py`
sont ceux du skill `docx` (`docx/scripts/office/`).

## Étape 0 — Préparation
```bash
mkdir -p <work>/unpacked
python3 <skills>/docx/scripts/office/unpack.py "<brouillon.docx>" <work>/unpacked
```
Vérifier les marqueurs de déclenchement (cf. SKILL.md « Quand déclencher »).

## Étape 1 — Extraction
Lire `<work>/unpacked/word/document.xml`. Repérer les paragraphes par leur
texte :
- **Dates** : paragraphe commençant par `L'AN ` (contient un `<w:br/>` par
  passage). Compter les passages.
- **Requérant** : bloc après `A LA DEMANDE DE :`.
- **Requête** : entre `M'EXPOSE CE QUI SUIT :` et `DEFERANT`.
- **Adresse terrain + GPS + carte** : après `RENDU CE JOUR` (image = carte de
  localisation, souvent un `.jpg` OpenStreetMap avec le cachet).
- **Mentions panneau** : paragraphe commençant par `Bénéficiaire :` (un
  `<w:br/>` par mention).
- **Recours** : paragraphe `Droit de recours` + texte.
- **Photos / passages** : titres `Heading1` `1er passage` / `2ème passage` /
  `3ème passage` ; les photos sont des paragraphes `Photographie n° X - …` avec
  `r:embed`. Rapprocher chaque `rId` du `word/_rels/document.xml.rels` pour le
  fichier média.
- **Articles** : bloc `Article A424-15 …` jusqu'à `… à démolir.`
- **Conclusion** : `Telles sont les constatations …`.

## Étape 2 — Questions interactives (en un seul bloc)
Ne demander que ce qui n'est pas déductible :
1. Type d'autorisation si le n° n'est pas explicite (PC / PA / PD / DP).
2. Confirmation du **nombre et des dates** de passages si le bloc « L'AN … » est
   incohérent ou incomplet.
3. Civilité du requérant si ambiguë.
> Si tout est déductible du brouillon + photos, ne rien demander.

## Étape 3 — Requête et mention de visite
Appliquer les templates §1 et §2. Conserver « CERTIFIE M'ÊTRE RENDU … AUX DATES
INDIQUÉES EN TÊTE DE L'ACTE » (formule multi-passages) plutôt que de lister les
passages en prose : les dates sont déjà en tête.

## Étape 4 — Mentions du panneau
```bash
python3 scripts/format_mentions.py <work>/unpacked/word/document.xml
```
Met en gras le libellé (avant le premier « : ») de chaque ligne du bloc de
mentions, et met les libellés en MAJUSCULES. Puis, via `Edit` :
- insérer l'encadré **CHANTIER INTERDIT AU PUBLIC** (paragraphe bordé centré
  gras) après les mentions ;
- s'assurer que le **Droit de recours** est dans un encadré bordé.
Voir `scripts/format_mentions.py --help` pour les options (`--no-upper`).

## Étape 5 — Lecture des photos
Lire chaque média rattaché. Confirmer que les mentions relevées correspondent au
panneau photographié (n°, bénéficiaire, surfaces). En cas de divergence →
commentaire Word, pas de correction silencieuse. Vérifier la cohérence
date EXIF ↔ passage.

## Étape 6 — Passages
Conserver une seule description du panneau. Vérifier que chaque `Heading1` de
passage est introduit par sa date (« Le 19 mars 2026 », etc.) et ne contient que
ses photos.

## Étape 7 — Articles
Si le bloc d'articles est présent → conserver. Sinon → insérer depuis
`references/boilerplate-articles.md` avant la conclusion.

## Étape 8 — Mise en page
```bash
python3 scripts/apply_layout.py <work>/unpacked
```
Applique :
- **Sauts de page manuels** : retire ceux insérés par l'app
  (`<w:br w:type="page"/>`) SAUF le premier (séparateur Sommaire → titre), qui
  isole sinon la carte GPS et crée des pages blanches.
- **Pagination par ancre** (`pageBreakBefore`) — règles figées avec Antoine :
  - « **CERTIFIE M'ÊTRE RENDU…** » → nouvelle page (visite + adresse + GPS +
    carte regroupés sur leur page, pas avec le titre).
  - « **J'AI PROCEDE AUX CONSTATATIONS…** » → nouvelle page