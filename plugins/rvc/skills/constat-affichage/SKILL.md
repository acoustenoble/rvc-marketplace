---
name: constat-affichage
description: "Met en forme un procès-verbal de constat d'AFFICHAGE d'autorisation d'urbanisme (.docx de commissaire de justice) — permis de construire/d'aménager/de démolir ou déclaration préalable. Déclencher dès qu'un .docx contient « constat d'affichage », « affichage régulier », un panneau d'urbanisme avec ses mentions (Bénéficiaire, Architecte, N° PC/PA/PD/DP, Nature du projet, Superficie, Surface de plancher, Hauteur, Chantier interdit au public), les articles A424-15/16/17/18, R424-15 ou R600-2 du Code de l'urbanisme, ou des sections « 1er/2ème/3ème passage ». Reformate les mentions au format à libellés gras, structure les passages (panneau décrit une fois + photos groupées par passage daté), ajoute les encadrés « Chantier interdit au public » et « Droit de recours », conserve le bloc d'articles, applique la mise en page RVC (sauts de page, sommaire) et livre le .docx final. Déclencher même sans demande explicite. Ne pas confondre avec constat-reecriture, etat-des-lieux, constat-inventaire ni constat-drone."
---

# Constat d'affichage — mise en forme (permis / déclaration préalable)

Ce skill transforme un brouillon de **constat d'affichage d'autorisation
d'urbanisme** (exporté depuis l'app constats-huissiers.fr ou dicté à la voix)
en un procès-verbal de constat professionnel conforme à la charte RVC et au
modèle de référence (PDF « PROCÈS-VERBAL DE CONSTAT D'AFFICHAGE »).

Le constat d'affichage atteste qu'un panneau réglementaire (permis de
construire, d'aménager, de démolir, ou décision de non-opposition à déclaration
préalable) est **affiché, visible et lisible depuis la voie publique**, et ce
**pendant une période continue** vérifiée par plusieurs visites (« passages »)
espacées dans le temps — ce qui fait courir le délai de recours des tiers
(art. R. 600-2 du Code de l'urbanisme).

## Quand déclencher

Le document est un constat d'affichage si **l'un** des critères suivants est
rempli :

- Il contient **« constate l'affichage régulier »**, **« CONSTAT D'AFFICHAGE »**
  ou **« affichage … répond aux exigences … du Code de l'Urbanisme »**.
- Il décrit **un panneau** d'autorisation d'urbanisme avec les mentions
  canoniques : *Bénéficiaire*, *Nom de l'architecte*, *Date de délivrance*,
  *N° (PC/PA/PD/DP)*, *Nature du projet*, *Superficie du terrain*, *Surface de
  plancher*, *Hauteur de la construction*, *Chantier interdit au public*.
- Il cite les articles **A424-15, A424-16, A424-17, A424-18, R424-15** ou
  **R600-2 / R600-1** du Code de l'urbanisme.
- Il contient des sections **« 1er passage »**, **« 2ème passage »**,
  **« 3ème passage »** (visites successives du même affichage).

Déclencher **même si Antoine ne demande pas explicitement de mise en forme** —
l'intention implicite lorsqu'il livre un brouillon de constat d'affichage est
qu'il soit retravaillé selon ses règles.

**Ne pas confondre avec :**

- `constat-reecriture` : constat narratif descriptif (humidité, voisinage…),
  sans panneau ni articles d'urbanisme.
- `etat-des-lieux` : logement loué, structure Sol/Murs/Plafond/Équipement.
- `constat-inventaire` : inventaire mobilier en tableau.
- `constat-drone` : constat réalisé par aéronef (présence d'un PDF Juris Drone).

## Ce que ce skill fait

1. **Extrait** l'en-tête juridique : requérant (bénéficiaire), autorisation
   (type + numéro), adresse du terrain, et **la liste des dates de passage**.
2. **Vérifie / pose les questions** manquantes : type d'autorisation (PC, PA,
   PD, DP), nombre et dates des passages, civilité du requérant.
3. **Reformate les mentions du panneau** : passe du bloc brut « Label : valeur »
   au format RVC à **libellés en gras** (un libellé par ligne), dans l'ordre
   réglementaire (art. A424-16).
4. **Ajoute les encadrés** « Chantier interdit au public » et « Droit de
   recours » (bordures), conformes au modèle.
5. **Structure les passages multiples** : la description du panneau est faite
   **une seule fois** ; les photographies sont **groupées par passage daté**
   (titre `1er passage`, `2ème passage`, `3ème passage`), chaque groupe pouvant
   contenir des vues de la rue (panneau dans son environnement) et des gros
   plans (panneau lisible).
6. **Réécrit la mention de visite** (« CERTIFIE M'ÊTRE RENDU CE JOUR, AUX DATES
   INDIQUÉES EN TÊTE DE L'ACTE ») et rappelle les passages antérieurs.
7. **Conserve le bloc d'articles** du Code de l'urbanisme en fin d'acte (ou
   l'ajoute s'il manque — cf. `references/boilerplate-articles.md`).
8. **Lit chaque photo** pour confirmer/corriger les mentions relevées sur le
   panneau (numéro, dates, surfaces) — sans rien inventer.
9. **Applique la mise en page** RVC : page de garde conservée, sommaire à
   mettre à jour, `Heading1` + saut de page sur chaque passage, justification,
   conclusion, signature/cachet.
10. **Repack le .docx final** et le présente.

## Ce que ce skill ne fait PAS

- N'**ajoute pas** de mention que le panneau ne porte pas (le panneau et les
  photos délimitent strictement le périmètre).
- Ne **corrige pas silencieusement** un numéro de permis, une surface ou une
  date : en cas de divergence entre le texte dicté et la photo du panneau,
  **signaler à Antoine** (commentaire Word) plutôt que trancher.
- N'**émet aucune conclusion juridique** sur la régularité (« l'affichage est
  régulier ») au-delà de la formule type — le constat est descriptif.
- Ne **modifie pas** les photos ni leur horodatage/GPS.
- Ne **suppose pas** la civilité du requérant si elle est ambiguë → demander.

## Règles cardinales (lecture obligatoire)

Avant toute mise en forme, lire :

- **`references/rules.md`** — règles de rédaction descriptive et spécificités
  du constat d'affichage (périmètre, doute = abstention, divergences à signaler).
- **`references/templates.md`** — modèles à trous : en-tête, requête (1 ou
  plusieurs passages), mentions du panneau, encadrés, conclusion.
- **`references/boilerplate-articles.md`** — bloc fixe des articles du Code de
  l'urbanisme à conserver/ajouter en fin d'acte.

## Workflow

Détail opérationnel dans **`references/workflow.md`**. Étapes :

### Étape 0 — Préparation
Vérifier les marqueurs, créer un répertoire de travail, dépaqueter le `.docx`
(`docx/scripts/office/unpack.py`).

### Étape 1 — Extraction
Lire `document.xml` pour extraire : requérant, autorisation (type + n°),
adresse du terrain, dates de passage (paragraphe « L'AN … »), mentions du
panneau (paragraphe « Bénéficiaire : … »), photos (rId → media) et leur
rattachement aux passages.

### Étape 2 — Questions interactives
Poser en bloc ce qui n'est pas déductible : type d'autorisation si ambigu,
nombre/dates des passages si le brouillon est incomplet, civilité du requérant
si ambiguë.

### Étape 3 — Requête et mention de visite
Rédiger l'introduction (« LAQUELLE M'EXPOSE… » / « M'AYANT EXPOSÉ… ») et la
mention de visite multi-passages (cf. `templates.md`).

### Étape 4 — Mentions du panneau
Reformater le bloc de mentions au format à libellés gras (script
`scripts/format_mentions.py`), dans l'ordre de l'art. A424-16. Ajouter les
encadrés « Chantier interdit au public » et « Droit de recours ».

### Étape 5 — Lecture des photos
Pour chaque photo, confirmer les mentions et la qualité de l'affichage (panneau
visible/lisible). Signaler toute divergence, ne rien inventer.

### Étape 6 — Passages
Conserver une **seule** description du panneau, puis grouper les photos par
passage (`Heading1` : `1er passage`, `2ème passage`, `3ème passage`), chacun
introduit par sa date.

### Étape 7 — Articles
Vérifier la présence du bloc d'articles ; le conserver ou l'insérer depuis
`references/boilerplate-articles.md`.

### Étape 8 — Mise en page
`scripts/apply_layout.py` : `pageBreakBefore` sur `Heading1`, justification des
`HOParagraphe`, `<w:updateFields/>` pour le sommaire, conservation page de
garde + footer + signature.

### Étape 9 — Repack et livraison
Repacker en préservant images/relations (`--original`), puis présenter le `.docx`.

## Convention de nommage du fichier de sortie (OBLIGATOIRE)

> `PV CONSTAT AFFICHAGE <NOM REQUERANT> <JJ.MM.AAAA>.docx`

- `<NOM REQUERANT>` : nom du bénéficiaire en majuscules, sans forme juridique
  (`JEAN CHEREAU`, pas `SAS JEAN CHEREAU`).
- `<JJ.MM.AAAA>` : date du **dernier** passage (le plus récent), points
  séparateurs.

Exemples :
- `PV CONSTAT AFFICHAGE JEAN CHEREAU 08.06.2026.docx`
- `PV CONSTAT AFFICHAGE ROY ENERGIE 16.12.2025.docx`

## Mode livraison par défaut

**Direct le `.docx` final.** Antoine relit et demande les ajustements ciblés.

## En cas de doute

- Type d'autorisation ambigu (PC vs DP) → lire la photo du panneau, sinon demander.
- Mention illisible sur la photo et absente du texte → ne pas l'inscrire.
- Divergence texte dicté / photo (n° de permis, surface) → **signaler**, ne pas trancher.
- Civilité du requérant ambiguë → demander.

## Enrichissement continu

À chaque constat, enrichir `references/templates.md` si Antoine valide une
nouvelle formulation, et `references/boilerplate-articles.md` si le bloc
d'articles évolue.
                                                                                                                                                                                                                                                                                                                                                                                          