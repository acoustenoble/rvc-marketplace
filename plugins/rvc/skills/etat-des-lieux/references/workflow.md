# Workflow opérationnel — état des lieux

Détail des étapes du `SKILL.md`. Toutes les commandes shell sont à exécuter
dans le sandbox via `mcp__workspace__bash`. Les chemins sont donnés en VM
(`/sessions/...`) — adapter selon la session courante.

## Variables de session

```bash
SRC="<chemin_du_brouillon.docx>"            # Brouillon fourni par Antoine
WORK="/sessions/<id>/edl_work"              # Répertoire de travail
UNPACK="$WORK/unpacked"                     # Source dépaquetée
PHOTOS="$WORK/photos"                       # Photos extraites pré-traitées
OUT_DIR="/sessions/<id>/mnt/outputs"        # Dossier de livraison
```

## Étape 0 — Préparation

```bash
mkdir -p "$WORK" "$UNPACK" "$PHOTOS"
python3 /sessions/<id>/mnt/.claude/skills/docx/scripts/office/unpack.py "$SRC" "$UNPACK"
```

Vérifier la présence des marqueurs d'EDL :

```bash
grep -E "(me mandate pour dresser l'état des lieux|^Sol :|^Murs :|^Plafond :|^Équipement :)" \
  "$UNPACK/word/document.xml" | head -20
```

Si aucun marqueur n'est trouvé → **arrêt** : ce n'est pas un EDL, ne pas
exécuter ce skill.

## Étape 1 — Extraction du brouillon

Lancer le script d'extraction :

```bash
python3 scripts/extract_brouillon.py "$UNPACK" --out "$WORK/extracted.json"
```

Le JSON produit doit contenir :

```json
{
  "bailleur": {
    "denomination": "Établissement public local à caractère industriel ou commercial MANCHE HABITAT",
    "rcs": "275 000 024",
    "adresse_siege": "5 Rue Emile Enault, 50000 SAINT-LO",
    "type_personne": "morale"
  },
  "locataire": {
    "civilite": "Monsieur",
    "identite": "Frédéric MORTELECQ",
    "nom_famille": "MORTELECQ"
  },
  "bail": {
    "date": "29/07/2021"
  },
  "logement": {
    "adresse": "Appartement 111, 7 HLM Le Peuplier 50400 GRANVILLE",
    "type_edl": "sortie"
  },
  "presence": {
    "civilite": "Madame",
    "nom": "DENIAU",
    "qualite": "Gestionnaire Manche Habitat"
  },
  "gps": {
    "latitude": "-1.5680247545242",
    "longitude": "48.837442864228"
  },
  "pieces": [
    {
      "titre_brut": "Entrée / Couloir",
      "phrase_acces": null,
      "sol": "linoléum dégradé avec traces de griffures, ensemble très sale, taches indélébiles",
      "murs": "tapisserie dégradée en très mauvais état, parties déchirées à multiples endroits, trous de chevilles",
      "plafond": "peint en blanc",
      "equipement": [
        "Porte depuis le palier, ouvrant et fermant correctement",
        "Quatre interrupteurs",
        "..."
      ],
      "mobilier": [],
      "photos": [
        {"numero": 1, "fichier": "image2.jpeg", "horodatage": "08/04/2026 10:39:04", "gps": "48.837548989289 -1.5679130147446"},
        {"numero": 2, "fichier": "image3.jpeg", "horodatage": "08/04/2026 10:39:11", "gps": "48.837548989289 -1.5679130147446"}
      ]
    },
    "..."
  ],
  "compteurs": {
    "electrique": {"index": "9096", "unite": "kWh", "photo": 80},
    "eau_froide": {"index": "185", "unite": "m³", "photo": 81}
  },
  "boite_aux_lettres": {
    "description": "Boîte aux lettres accessible depuis les parties communes, traces d'adhésif sur la façade métallique, absence de clé",
    "photo": 82
  },
  "cles": [
    "2 badges",
    "3 clés de logement",
    "3 clés de porte PVC de la cuisine"
  ]
}
```

Vérifier visuellement la structure produite avant de continuer.

## Étape 2 — Questions interactives

Poser à Antoine, en une seule interaction (en utilisant `AskUserQuestion`) :

1. **Identité complète du locataire** (avec civilité). Ex. : *« Monsieur Frédéric MORTELECQ »*.
2. **Date du bail**. Ex. : `29/07/2021`. Format `JJ/MM/AAAA`.
3. **Date du constat** (jour de la visite). Ex. : `08/04/2026`. Le skill la convertira en lettres.
4. **Date d'envoi de la convocation** (LRAR + lettre simple). Ex. : `30/03/2026`.
5. **Statut de l'AR** :
   - `signé` → demander aussi la date de signature.
   - `pli revenu non réclamé`
   - `pas encore de retour de la poste`
6. **Civilité du requérant** uniquement si l'extraction du brouillon n'a pas pu trancher.

Stocker les réponses dans `$WORK/answers.json` :

```json
{
  "locataire": {
    "civilite": "Monsieur",
    "identite_complete": "Monsieur Frédéric MORTELECQ",
    "nom_famille": "MORTELECQ"
  },
  "bail": {"date": "29/07/2021"},
  "constat": {"date": "08/04/2026", "date_lettres": "L'AN DEUX-MILLE-VINGT-SIX ET LE HUIT AVRIL"},
  "convocation": {"date_envoi": "30/03/2026", "ar_status": "signe", "ar_date": "02/04/2026"},
  "requerant_civilite": "morale"
}
```

## Étape 3 — Lecture des photos

Pour chaque photo extraite dans `$UNPACK/word/media/`, appliquer le
pré-traitement (rotation EXIF + redimensionnement) puis demander une lecture
visuelle.

```python
from PIL import Image, ImageOps

def preprocess(src_path, dst_path, target=900):
    img = Image.open(src_path)
    img = ImageOps.exif_transpose(img)  # CRITIQUE — sinon photos couchées
    w, h = img.size
    if max(w, h) > target:
        if w >= h:
            nw, nh = target, int(h * target / w)
        else:
            nw, nh = int(w * target / h), target
        img = img.resize((nw, nh), Image.LANCZOS)
    img.convert('RGB').save(dst_path, 'JPEG', quality=85, optimize=True)
```

Pour chaque pièce, lire chaque photo et **enrichir / corriger** les rubriques
Sol, Murs, Plafond, Équipement du JSON `extracted.json` selon les règles de
`rules.md` (notamment règle 3 : périmètre strict, doute = abstention).

Sauvegarder le JSON enrichi dans `$WORK/extracted.enriched.json`.

## Étape 4 — Réordonnancement et titres

Appliquer l'ordre logique des pièces (cf. `rules.md` règle 8). Implémentation
dans `scripts/build_etat_des_lieux.py` :

```python
ORDER = [
    "Convocation",
    "Entrée / Couloir",
    "Salon",
    "Salle à manger",
    "Séjour",
    "Cuisine",
    "Séchoir",
    "Cellier",
    "Arrière-cuisine",
    "Salle de bain",
    "Salle de douche",
    "WC",
    "Chambre 1",
    "Chambre 2",
    "Chambre 3",
    "Chambre 4",
    "Bureau",
    "Balcon",
    "Loggia",
    "Terrasse",
    "Placard",
    "Dressing",
    "Cave",
    "Garage",
    "Compteurs",
    "Boîte aux lettres",
    "Clés",
]

def piece_rank(titre):
    titre_norm = normalize(titre)
    for i, ref in enumerate(ORDER):
        if normalize(ref) == titre_norm:
            return i
    return 999  # Pièce inconnue → en fin de liste
```

Appliquer également les corrections de coquilles :

```python
TITLE_FIXES = {
    "wc": "WC",
    "salle de douche": "Salle de douche",
    "salle de bain": "Salle de bain",
    "sechoir": "Séchoir",
    "cuisne": "Cuisine",
    "entree / couloir": "Entrée / Couloir",
    "entrée/couloir": "Entrée / Couloir",
    "boite aux lettres": "Boîte aux lettres",
    "compteurs": "Compteurs",
    "cles": "Clés",
    # Liste extensible
}
```

## Étape 5 — Construction du document final

Lancer le script :

```bash
python3 scripts/build_etat_des_lieux.py \
  --src "$SRC" \
  --extracted "$WORK/extracted.enriched.json" \
  --answers "$WORK/answers.json" \
  --photos-dir "$PHOTOS" \
  --out "$OUT_DIR/PV CONSTAT <NOM CLIENT> date <JJ.MM.AAAA>.docx"
```

Le script doit :

1. Ouvrir le `.docx` original (préserve TOUT : page de garde, sommaire, marges, polices, signature…).
2. Réécrire le bloc `LEQUEL M'EXPOSE CE QUI SUIT` selon `templates.md` § 2.
3. Insérer la section `1 Convocation` avec la variante choisie (`templates.md` § 3).
4. Pour chaque pièce dans l'ordre, créer un titre `Heading1` (numérotation auto, saut de page avant) puis poser les rubriques `Sol :`, `Murs :`, `Plafond :`, `Équipement :` (+ `Mobilier :` si présent), suivies des photos avec leur légende.
5. Insérer les sections `Compteurs`, `Boîte aux lettres`, `Clés` (cf. `templates.md` § 5-7).
6. Insérer la conclusion fixe (cf. `templates.md` § 8).
7. Marquer tous les champs de TOC comme `dirty=true`.
8. Activer `updateFields=true` dans `settings.xml`.

## Étape 6 — Mise en page finale

Lancer le script de finalisation :

```bash
python3 scripts/apply_layout.py "$WORK/built.unpacked"
```

Ce script applique en une passe :

- `styles.xml` : `<w:pageBreakBefore/>` et `<w:keepNext/>` sur `Heading1`, `<w:jc w:val="both"/>` sur le style des paragraphes Sol/Murs/Plafond.
- `document.xml` : reposer `<w:pageBreakBefore/>` individuel sur chaque `Heading1`.
- `settings.xml` : `<w:updateFields w:val="true"/>`.

## Étape 7 — Repack et livraison

```bash
python3 /sessions/<id>/mnt/.claude/skills/docx/scripts/office/pack.py \
  "$WORK/built.unpacked" \
  "$OUT_DIR/PV CONSTAT MANCHE HABITAT date 08.04.2026.docx" \
  --original "$SRC"
```

Le flag `--original` garantit que les parties binaires (images, relations,
police embarquée, page de garde RVC) sont préservées depuis le fichier
source.

Présenter le `.docx` final via `present_files` ou un lien `computer://`.

## Vérifications post-build

Avant de livrer, vérifier que le document final contient bien :

- ✅ Page de garde RVC intacte
- ✅ Sommaire qui se met à jour à l'ouverture (Word propose le rafraîchissement)
- ✅ Section `1 Convocation` avec la variante AR correcte
- ✅ Pièces dans l'ordre logique (Entrée → … → Clés)
- ✅ Chaque pièce avec ses 4 rubriques (`Sol :`, `Murs :`, `Plafond :`, `Équipement :`)
- ✅ Photos numérotées de manière continue (1 → N)
- ✅ Conclusion fixe + signature + cachet
- ✅ Nom du fichier conforme à la convention `PV CONSTAT <NOM CLIENT> date <JJ.MM.AAAA>.docx`

Si l'un de ces points fait défaut, corriger avant livraison.
