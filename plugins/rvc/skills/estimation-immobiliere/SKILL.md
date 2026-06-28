---
name: estimation-immobiliere
description: >
  Produit une étude de marché / estimation immobilière complète en PDF, à la
  charte de l'agence RVC IMMOBILIER (page de garde design, présentation de
  l'agence, environnement du bien, marché local DVF, comparables vendus et en
  vente, état descriptif, et estimation chiffrée valeur basse/moyenne/haute).
  À DÉCLENCHER dès que l'utilisateur demande d'estimer, d'évaluer ou de chiffrer
  un bien immobilier (maison, appartement, terrain), de faire une « étude de
  marché », un « avis de valeur », un « rapport d'estimation », ou donne les
  caractéristiques d'un bien (adresse, surface, DPE, état, équipements) en vue
  d'en déterminer le prix. Utiliser même si l'utilisateur ne dit pas
  explicitement « fais une estimation » : toute demande de valeur d'un bien, de
  prix au m² d'un secteur, ou de rapport immobilier branché RVC déclenche ce
  skill. Les données de prix proviennent de la base publique DVF via data.gouv.
---

# Estimation immobilière RVC — étude de marché en PDF

Ce skill génère un rapport PDF soigné (type plaquette), aux couleurs RVC
IMMOBILIER, à partir des caractéristiques d'un bien + des données réelles du
marché (DVF). Le but : un livrable client présentable, traçable et cohérent.

## Vue d'ensemble du déroulé
1. **Recueillir** les informations sur le bien (poser les questions manquantes).
2. **Résoudre** le code INSEE de la commune.
3. **Récupérer les données de marché** DVF (prix médian €/m², nb de ventes) →
   commune, département, secteur.
4. **Comparables** : ventes DVF + annonces en cours (tentative via Chrome).
5. **Calculer l'estimation** (valeur bâti + annexes → moyenne + fourchette).
6. **Écrire `donnees.json`** puis lancer le script de génération.
7. **Présenter le PDF** au client et proposer des ajustements.

Garde toujours en tête : **chaque chiffre affiché doit être justifiable**. En
l'absence de donnée fiable, on omet la section plutôt que d'inventer.

---

## Étape 1 — Recueillir les informations
Si l'utilisateur n'a pas déjà tout fourni, demander (idéalement via une question
structurée groupée) les éléments manquants. Liste d'intake :

**Identité du bien** — type (maison/appartement), adresse complète, code postal,
commune ; propriétaire / demandeur (nom à afficher).
**Caractéristiques** — surface habitable (loi Carrez, m²), surface terrain,
nombre de pièces, de chambres, année de construction.
**Qualité** — état général, DPE et GES, équipements/prestations notables,
travaux éventuels à prévoir.
**Annexes** — combles/sous-sol/dépendances aménageables (avec surfaces), garage,
piscine, etc.
**Divers** — occupation (libre/loué), charges annuelles, photos (chemins de
fichiers si disponibles), références de ventes du quartier connues de l'étude.
**Comparaison au secteur** (pour les graphiques) — moyennes du secteur pour le
nombre de pièces, la surface et l'année de construction, afin de positionner le
bien (champ `bien.comparaison`).

Le bloc agence a des valeurs par défaut RVC (voir `examples/`) ; les réutiliser
sauf indication contraire. **Ne jamais nommer un conseiller individuel** : le bas
de page et les mentions citent uniquement l'étude RVC IMMOBILIER, car différents
collaborateurs produiront ces rapports. Reprendre le nom du demandeur fourni.

## Étape 2 — Code INSEE
Déterminer le code INSEE (5 chiffres) de la commune et le code département.
Détails et méthode : voir `references/donnees-dvf.md` (§1).

## Étape 3 — Données de marché DVF
Suivre `references/donnees-dvf.md` (§2) : interroger via le MCP data.gouv le
resource `851d342f-9c96-41c1-924a-11a7a7aae8a6` avec `filter_column="code_geo"`
sur le code commune, le code département (et la section si pertinente).
Récupérer prix médian/moyen €/m² maison & appartement + nombre de ventes →
remplir `marche`. Une cellule vide ⇒ `null` (pas assez de ventes).

## Étape 4 — Comparables
- **Vendus (DVF)** : 3-5 ventes réelles comparables (§3 de la référence). Si
  l'utilisateur en a, les utiliser ; sinon s'appuyer sur les stats agrégées.
- **En vente** : tenter via Claude in Chrome (Le Bon Coin / SeLoger). Charger
  les outils Chrome via ToolSearch (`query: "chrome"`). En cas de blocage
  anti-robot, demander à l'utilisateur de coller quelques annonces — ne pas
  contourner les protections. Détails §4.

## Étape 4 bis — Carte de localisation (recommandé)
Pour la page « points d'intérêt », une carte vaut mieux qu'une liste. Le rapport
affiche l'image dont le chemin est donné dans `points_interet.carte` ; à défaut,
il indique seulement le rayon d'accessibilité. Deux façons d'obtenir l'image :

**A. Capture Google Maps (le plus simple).** Via Claude in Chrome :
`navigate` vers `https://www.google.com/maps/place/<ADRESSE+URL-encodée>`,
attendre ~5 s le chargement des tuiles, prendre une capture d'écran et
l'enregistrer dans le dossier de travail. Recadrer pour ne garder que la carte
(retirer le panneau latéral et les barres d'outils). Passer le chemin du fichier
dans `points_interet.carte`. Si l'enregistrement de capture sur disque n'est pas
possible, demander à l'utilisateur de déposer une capture d'écran de la carte.

**B. Carte OpenStreetMap composée (sans capture).** Toujours dans Chrome, sur une
page ouverte (p. ex. openstreetmap.org), exécuter du JavaScript qui récupère les
tuiles `https://tile.openstreetmap.org/{z}/{x}/{y}.png` (CORS autorisé), les
dessine sur un canvas centré sur les coordonnées du bien, ajoute un repère, puis
renvoie `canvas.toDataURL('image/jpeg')`. Enregistrer cette image (data-URI ou
fichier) et la référencer dans `points_interet.carte`. Toujours conserver
l'attribution « © OpenStreetMap contributors ». Géocoder l'adresse au préalable
(coordonnées lat/lon) ; zoom 15 donne un bon cadrage de quartier.

Les catégories de services sont illustrées automatiquement par des icônes SVG
intégrées (pas d'émoji : ceux-ci ne s'impriment pas de façon fiable en PDF).

## Étape 5 — Estimation
Appliquer la méthode de `references/methodologie-estimation.md` : prix médian
DVF de référence → ajustements qualitatifs (année, état, DPE, prestations,
emplacement) → valeur du bâti sur la surface Carrez → valorisation séparée des
annexes/terrain → valeur moyenne arrondie → fourchette ±5-8 %. Renseigner
`methodo` avec le **calcul réel** (chiffres employés), pas une formule générique.
Vérifier la cohérence avec le nuage des comparables.

## Étape 6 — Générer le rapport
1. Écrire le fichier de données suivant `references/schema-donnees.md`
   (s'inspirer de `examples/exemple-saint-james.json`).
2. Lancer le script :
   ```bash
   python3 scripts/build_report.py <donnees.json> <sortie.pdf>
   ```
   (Le script utilise WeasyPrint. Si absent : `pip install weasyprint --break-system-packages`.)
   Pour déboguer le HTML : variable d'env `RVC_DEBUG_HTML=debug.html`.
3. Sauvegarder le PDF dans le dossier de sortie et le présenter à l'utilisateur
   avec `present_files`. Résumer en une phrase la valeur estimée et la fourchette.

## Étape 7 — Itérer
Proposer d'ajuster (ajout de photos, pondération des comparables, texte des
commentaires, sections à enrichir). C'est un outil d'aide à la décision de
l'étude, pas une boîte noire.

---

## Logos & charte
Les couleurs (bleu marine `#1B2A4A`, doré `#B8975A`) et la mise en page sont dans
`assets/styles.css`. Les logos sont chargés depuis `assets/` :
`logo-rvc-color.(png|svg)` et `logo-rvc-white.(png|svg)`. Des **logos SVG de
secours** sont fournis ; pour un rendu officiel, déposer les fichiers PNG
définitifs de RVC dans `assets/` sous ces noms (le `.png` est prioritaire sur le
`.svg`). Le logo blanc sert sur fond foncé (garde + bandeaux), le logo couleur
sur fond clair.

## Garde-fous
- Étude **indicative**, jamais présentée comme une expertise réglementaire (la
  page « Mentions » le rappelle).
- Sources de prix = DVF (public) + annonces citées en comparaison.
- Ne pas fabriquer de ventes, d'annonces ou de statistiques. Donnée manquante ⇒
  section omise.

## Structure du skill
```
estimation-immobiliere/
├── SKILL.md
├── assets/        styles.css + logos (png/svg)
├── scripts/       build_report.py  (JSON → PDF via WeasyPrint)
├── references/    donnees-dvf.md, methodologie-estimation.md, schema-donnees.md
└── examples/      exemple-saint-james.json (cas réel complet)
```
