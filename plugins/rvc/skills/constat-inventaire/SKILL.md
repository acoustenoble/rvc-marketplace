---
name: constat-inventaire
description: Met en forme un constat d'inventaire (.docx d'huissier / commissaire de justice) en remplaçant la dictée vocale par un tableau N° / Photo n° / Description améliorée par lecture des photos / Photographie. À DÉCLENCHER dès que l'utilisateur fournit un .docx contenant des constatations d'inventaire mobilier avec photos numérotées (« Photographie n°X »), un PV d'huissier listant des biens pièce par pièce (Couloir, Salon, Cuisine, Chambre, Salle de douche, Garage…), ou la formule « J'AI PROCEDE AUX CONSTATATIONS SUIVANTES » couplée à plusieurs photos par pièce. Le skill conserve TOUTE la structure du PV original (en-tête, sommaire, requête, signature), lit chaque photo pour améliorer la description et corriger les erreurs de dictée, applique le style 'Titre11' à chaque pièce avec saut de page, et marque le sommaire pour mise à jour automatique. Utiliser même si l'utilisateur ne dit pas explicitement « mets en forme ». Ne pas confondre avec 'constat-reecriture' (constatations textuelles non-inventaire).
---

# Constat d'inventaire — mise en forme en tableau

Ce skill transforme un constat d'inventaire dicté à la voix (avec descriptions
imprécises et erreurs de transcription) en un document professionnel avec un
tableau pièce par pièce, photos intégrées, descriptions améliorées par
relecture visuelle.

## Quand déclencher

Le document est un constat d'inventaire si :

- Il contient la formule **« J'AI PROCEDE AUX CONSTATATIONS SUIVANTES »**
- Il contient plusieurs paragraphes du type **« Photographie n°X — DD/MM/YYYY HH:MM:SS — coordonnées GPS »**
- Les constatations sont organisées par **pièces** (Couloir, Salon, Cuisine, Chambre, Salle de douche, Garage, etc.) — souvent sous le style `Titre11`
- Il liste des **biens mobiliers** (meubles, électroménager, vêtements, vaisselle, etc.) avec une photo associée à chaque bien

Si le document est un constat textuel non-inventaire (état des lieux narratif,
trouble de voisinage, dégât des eaux, etc.), utiliser plutôt `constat-reecriture`.

## Workflow

### Étape 1 — Extraire les images du .docx

Décompresser le .docx (c'est un .zip) et extraire les images depuis
`word/media/`. Les deux ou trois premières images (image1, image2 et parfois
la dernière) sont le logo / l'en-tête / la signature ; les **vraies
photographies** sont les images JPG numérotées.

Pour mapper proprement « Photographie n°N » → fichier image, il faut lire
l'ordre des `r:embed` dans `word/document.xml` et le rapprocher des `rels` :

```python
import zipfile, re
with zipfile.ZipFile(SRC_DOCX) as z:
    rels_xml = z.read('word/_rels/document.xml.rels').decode('utf-8')
    rels = {m.group(1): m.group(2).replace('media/', '')
            for m in re.finditer(r'Id="([^"]+)"\s+Type="[^"]*image[^"]*"\s+Target="([^"]+)"', rels_xml)}
    doc_xml = z.read('word/document.xml').decode('utf-8')
order = [rels[m.group(1)] for m in re.finditer(r'r:embed="([^"]+)"', doc_xml)
         if m.group(1) in rels]
# order[0..N] = images dans l'ordre d'apparition. Repérer la première image
# qui n'est ni un logo (PNG en début/fin) ni un en-tête, et faire correspondre
# avec « Photographie n°1 ».
```

### Étape 2 — Pré-traiter les photos

Pour chaque photo, **redimensionner à ~600 px de plus grand côté** et
**appliquer la rotation EXIF** (sinon les photos prises à la verticale
apparaissent couchées). Sauvegarder en JPEG qualité 82 dans un dossier de
travail.

```python
from PIL import Image, ImageOps
img = Image.open(src_path)
img = ImageOps.exif_transpose(img)  # CRITIQUE
# resize à 600 px max
w, h = img.size
target = 600
nw, nh = (target, int(h*target/w)) if w >= h else (int(w*target/h), target)
img.resize((nw, nh), Image.LANCZOS).convert('RGB').save(dst, 'JPEG', quality=82, optimize=True)
```

### Étape 3 — Lire chaque photo et améliorer la description

**C'est l'étape la plus importante.** La dictée vocale du commissaire
introduit régulièrement des erreurs qu'il faut corriger en regardant la photo :

- Marques mal entendues (« Haier » dicté pour « AYA », « Marc Innov » pour « Marc'Innov »…)
- Confusions d'objets (« machine à laver » dicté pour un sèche-linge condenseur)
- Phrases hachées : « table deux su mineral » = « table avec dessus en marbre »
- Détails manqués : matériau exact, état, nombre de portes, contenu visible…
- Indications de défauts visibles (skaï déchiré, jaunissement, taches, etc.) à intégrer dans la description

Lire chaque photo une par une avec l'outil de lecture d'image, puis rédiger
une description **précise, descriptive et neutre** :

- Type de meuble (commode 4 tiroirs, buffet 2 portes battantes, console…)
- Matériau et couleur (chêne foncé, mélaminé blanc, simili-cuir blanc…)
- Marque/modèle visible sur l'appareil (priorité à ce que dit la photo)
- Contenu visible si pertinent
- Défauts apparents factuels (déchirure, jaunissement, taches)

Conserver les écarts par rapport à la dictée dans la description, sous une
forme neutre du type : *« le requérant indique X ; la lecture du logo donne Y »*.
**Ne pas affirmer comme certain ce qui ne l'est pas.**

### Étape 4 — Construire la liste structurée

Préparer une liste Python d'items :

```python
ITEMS = [
    # (room, item_no, [photo_nos], description, etat)
    ("Couloir", 1, [1], "Petit meuble d'angle...", "..."),
    ("Couloir", 2, [2], "Meuble colonne...", "..."),
    ("Couloir", 4, [4, 5], "Contenu de placards : ...", "..."),
    # ...
]
ROOMS = ["Couloir", "Salon", "Séchoir", "Cuisine", "Placard",
         "Chambre", "Salle de douche", "Local annexe"]
```

Le champ `etat` est conservé dans la structure mais **n'est plus utilisé en sortie** (il a été retiré de la mise en forme finale ; on garde le champ pour rester compatible avec le script).

### Étape 5 — Lancer le script de mise en forme

Le script `scripts/build_constat_inventaire.py` se charge de tout :

- Ouvre le .docx original (préserve TOUT : en-tête, sommaire, marges, polices,
  numérotations, signature…)
- Repère la zone à remplacer (entre « J'AI PROCEDE AUX CONSTATATIONS… » et
  « Telles sont les constatations… »)
- Supprime le contenu intermédiaire
- Insère, pièce par pièce :
  - Un **titre** au style `Titre11` (le style original) avec
    `pageBreakBefore`, `keepNext`, `keepLines`, `outlineLvl=1`, `numId=3`
    et un **signet** `_Toc_<piece>` pour le sommaire
  - Un **tableau 4 colonnes** : N° item / Photo n° / Description / Photographie
- Marque tous les champs de TOC comme `dirty=true` et active
  `updateFields=true` dans `settings.xml` pour que Word propose la mise à
  jour du sommaire à l'ouverture

Lancer :

```bash
python scripts/build_constat_inventaire.py \
  --src "<chemin_du_constat_original>.docx" \
  --photos-dir "<dossier_des_photos_pretraitees>" \
  --data "<fichier_python_avec_ITEMS_et_ROOMS>" \
  --out "<chemin_de_sortie>.docx"
```

## Mise en forme cible

- **Format** : A4 portrait (préservé du document original)
- **Tableau par pièce** : 4 colonnes
  - **N°** (≈ 1,0 cm) — numéro d'item
  - **Photo n°** (≈ 1,4 cm) — numéro(s) de photographie ; empilés verticalement si plusieurs
  - **Description du bien** (≈ 8,2 cm) — description retravaillée
  - **Photographie** (≈ 6,4 cm) — image redimensionnée
- **En-tête de tableau** : fond bleu marine `#1F3A5F`, texte blanc gras
- **Lignes alternées** : fond `#F5F7FA` une ligne sur deux
- **Bordures** : gris clair `#B0B0B0`
- **Saut de page avant chaque pièce** + lignes solidaires + paragraphes solidaires
- **Sommaire** : conservé tel quel, prêt à être mis à jour ; les pièces
  apparaissent automatiquement avec numérotation auto (1. Couloir, 2. Salon…)

## Points d'attention

- **Ne jamais** réécrire l'en-tête, le sommaire, la requête ou la signature
  du PV — tout doit être préservé à l'identique du document source.
- **Toujours** préserver le style `Titre11` (**sans espace** dans l'ID — c'est
  un piège classique : le nom est « Titre 11 » mais l'ID est `Titre11`).
- **Toujours** poser le `numPr` avec `numId=3` sur les titres de pièces, sinon
  la numérotation automatique (1, 2, 3…) ne fonctionne pas et le sommaire
  affiche les pièces sans numéro.
- **Toujours** poser `outlineLvl=1` directement sur le paragraphe (pas seulement
  via le style), parce que le TOC du document utilise l'option `\u` qui se base
  sur le niveau hiérarchique appliqué au paragraphe.
- **Si le local annexe est inaccessible**, le mentionner explicitement dans une
  ligne du tableau correspondant (description : « Local annexe inaccessible
  faute de clé : aucune constatation ni photographie n'a pu être effectuée à
  l'intérieur. », photo n° vide).

## Modèle de fichier de données

Voir `references/data_template.md` pour la structure complète des `ITEMS` et
`ROOMS` à fournir au script.
                                                                                                                                                                                                                                                 