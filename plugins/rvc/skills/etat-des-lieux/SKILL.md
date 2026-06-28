---
name: etat-des-lieux
description: "Met en forme un état des lieux (.docx d'huissier/commissaire de justice) — entrée ou sortie. À DÉCLENCHER dès qu'un .docx contient des constatations pièce par pièce structurées Sol/Murs/Plafond/Équipement, un PV listant les pièces d'un logement loué (Entrée, Cuisine, Salon, WC, Salle de douche, Chambre, Compteurs, Boîte aux lettres, Clés…), ou la mention « me mandate pour dresser l'état des lieux ». Le skill structure chaque pièce en Sol/Murs/Plafond/Équipement, lit chaque photo pour enrichir les descriptions, applique Heading1 avec saut de page, gère la convocation (3 variantes AR), réordonne les pièces (entrée → vie → eau → chambres → annexes → compteurs → BAL → clés) et marque le sommaire pour mise à jour. Utiliser même sans « mets en forme » explicite. Ne pas confondre avec 'constat-reecriture' (constat narratif) ni 'constat-inventaire' (inventaire mobilier en tableau)."
---

# État des lieux — mise en forme entrée / sortie

Ce skill transforme un brouillon d'état des lieux dicté à la voix (descriptions
imprécises, fautes de frappe, désordre des pièces) en un procès-verbal de
constat professionnel, structuré pièce par pièce avec décomposition stricte
**Sol / Murs / Plafond / Équipement**, photos relues pour enrichir les
descriptions, et mise en page conforme à la charte RVC.

## Quand déclencher

Le document est un état des lieux si **l'un** des critères suivants est rempli :

- Le brouillon contient la phrase **« me mandate pour dresser l'état des lieux »** (de sortie ou d'entrée).
- Le brouillon est organisé pièce par pièce avec les rubriques canoniques **« Sol : … »**, **« Murs : … »**, **« Plafond : … »**, **« Équipement : … »**.
- Le brouillon liste des pièces typiques d'un logement loué (Entrée / Couloir, Cuisine, Séchoir, Salon, Balcon, Placard, WC, Salle de douche, Chambre 1, Chambre 2…) suivies des sections **« Compteurs »**, **« Boîte aux lettres »**, **« Clés »**.
- Le brouillon mentionne une convocation type **« par lettre recommandée avec demande d'avis de réception et par lettre simple »**.

Si l'un de ces critères est présent, déclencher ce skill **même si l'utilisateur ne demande pas explicitement de mise en forme** — l'intention implicite d'Antoine lorsqu'il livre un brouillon d'EDL est qu'il soit retravaillé selon ses règles.

**Ne pas confondre avec :**

- `constat-reecriture` : constat narratif (humidité, voisinage, dégât des eaux). Pas de structure Sol/Murs/Plafond/Équipement, pas de section convocation/compteurs/clés.
- `constat-inventaire` : inventaire mobilier mis en forme en **tableau** N°/Photo/Description. L'EDL n'utilise pas de tableau, mais une décomposition Sol/Murs/Plafond + liste à puces pour l'équipement.

## Ce que ce skill fait

1. **Extrait** depuis le brouillon : bailleur requérant, locataire, adresse, date du bail, type d'EDL (entrée/sortie), personne présente sur place, liste des pièces et leurs descriptions brutes, photos numérotées avec leurs métadonnées.
2. **Pose les questions interactives** dont les réponses ne sont pas dans le brouillon (date du constat, date de convocation, statut AR, date de l'AR si signé).
3. **Réécrit l'introduction de la requête** avec la formule type à trous, en accordant la civilité du requérant (Le requérant / La requérante / La société requérante).
4. **Rédige la section Convocation** selon l'une des 3 variantes (AR signé / pli revenu non réclamé / pas encore de retour).
5. **Lit chaque photo** pour enrichir et corriger les descriptions Sol/Murs/Plafond/Équipement (vocabulaire technique, sans interprétation, sans conclusion).
6. **Réordonne les pièces** selon la logique : Convocation → Entrée/Couloir → Pièces de vie (Salon, Salle à manger) → Cuisine + annexes (Séchoir, Cellier) → Pièces d'eau (Salle de bain/douche, WC) → Chambres → Annexes (Balcon, Placard, Cave) → Compteurs → Boîte aux lettres → Clés.
7. **Renomme les titres** si fautes ou casse incorrecte (« Wc » → « WC », « salle de douche » → « Salle de douche »…).
8. **Applique la mise en page** : page de garde, sommaire à mettre à jour, style `Heading1` + saut de page sur chaque pièce, conclusion, signature.
9. **Repack le .docx final** et le présente à l'utilisateur.

## Ce que ce skill ne fait PAS

- Ne **renomme** pas les pièces existantes vers un type qui n'est pas dans le brouillon (jamais d'invention de pièce).
- N'**ajoute** pas d'observations qu'Antoine n'a pas dictées dans le brouillon. Les photos servent à *préciser* (matériau exact, défaut visible) et *corriger les erreurs de dictée*, **pas** à étendre l'inventaire.
- Ne **modifie** pas les photos elles-mêmes ni leur ordre interne à une pièce.
- N'**émet** pas d'interprétation, de conclusion, ni de jugement de valeur (« ce logement est dans un état déplorable », « le locataire n'a manifestement pas entretenu »…). Strictement descriptif.
- Ne **suppose** pas la civilité du locataire ou du requérant si elle n'est pas explicite dans le brouillon — demander à Antoine en cas de doute.

## Règles cardinales (lecture obligatoire)

Avant toute mise en forme, lire :

- **`references/rules.md`** — règles de rédaction strictement descriptive (zéro interprétation, zéro conclusion, doute = abstention, périmètre du brouillon).
- **`references/templates.md`** — modèles à trous pour l'introduction, les 3 variantes de convocation, la conclusion.
- **`references/vocabulary.md`** — lexique technique validé par Antoine (toile à peindre, linoléum à l'état d'usage, tête thermostatique, bouche d'aération VMC encrassée, trous de chevilles, joint dégradé…).
- **`references/piece_structure.md`** — format strict d'une pièce (ordre des rubriques, formulation, liste à puces de l'équipement).

## Workflow

Suivre scrupuleusement les étapes ci-dessous. Le détail opérationnel de chaque étape est dans **`references/workflow.md`**.

### Étape 0 — Préparation

1. Vérifier que le `.docx` fourni contient bien les marqueurs d'un EDL (cf. critères de déclenchement).
2. Créer un répertoire de travail.
3. Dépaqueter le `.docx` (c'est un `.zip`) pour accéder à `word/document.xml`, `word/media/` et `word/_rels/document.xml.rels`.

### Étape 1 — Extraction du brouillon

Lire le document pour extraire :

- **Bailleur requérant** : dénomination + forme juridique + RCS + adresse (bloc « A LA DEMANDE DE »).
- **Locataire** : civilité + identité + (éventuellement) date du bail + adresse du logement (bloc « LEQUEL M'EXPOSE CE QUI SUIT »).
- **Type d'EDL** : entrée ou sortie (lire la formule « me mandate pour dresser l'état des lieux de … »).
- **Personne présente sur place** : civilité + nom + qualité (bloc « ME SUIS RENDU CE JOUR »).
- **Liste des pièces** : titres + texte brut Sol/Murs/Plafond/Équipement de chacune.
- **Photos** : pour chaque pièce, lister les `r:embed` de l'XML, les rapprocher des `rels` pour obtenir les fichiers JPG dans `word/media/`, et conserver leur ordre d'apparition.

### Étape 2 — Questions interactives

Poser à Antoine les questions suivantes (en bloc, via une seule interaction) :

1. **Identité complète du locataire** (ex. *« Monsieur Frédéric MORTELECQ »* ou *« Madame Sophie SAFFRE »*) — l'information n'est pas dans le brouillon.
2. **Date du bail** au format `JJ/MM/AAAA` (ex. *« 29/07/2021 »*) — l'information n'est pas dans le brouillon.
3. **Date du constat** (jour de la visite) — sera convertie en lettres pour la mention « L'AN … ET LE … ».
4. **Date d'envoi de la convocation** (LRAR + lettre simple).
5. **Statut de l'accusé de réception** :
   - `signé` → demander la date de signature de l'AR
   - `pli revenu non réclamé`
   - `pas encore de retour`
6. **Civilité du requérant** uniquement si ambiguë dans le brouillon (personne morale, Monsieur, Madame).

### Étape 3 — Civilité du requérant et introduction

Sur la base de la civilité détectée/confirmée, rédiger l'introduction de la requête entre « LEQUEL M'EXPOSE CE QUI SUIT : » et « DEFERANT A CETTE REQUISITION : » avec le template :

> *« Que [Le requérant | La requérante | La société requérante] a donné à bail d'habitation principale à [identité du locataire] en date du [date du bail], un logement sis [adresse complète].
> Que je suis mandaté pour dresser l'état des lieux [d'entrée | de sortie]. »*

Voir `references/templates.md` pour les variantes complètes.

### Étape 4 — Section Convocation

Insérer la section **1 Convocation** au tout début des constatations, avant la première pièce, avec l'une des 3 variantes (cf. `references/templates.md`) :

- **AR signé** : « Que le locataire a été convoqué par lettre recommandée avec demande d'avis de réception signée le [date AR] et par lettre simple en date du [date envoi]. »
- **Pli revenu non réclamé** : « Que le locataire a été convoqué par lettre recommandée avec demande d'avis de réception, dont le pli est revenu non réclamé, et par lettre simple en date du [date envoi]. »
- **Pas encore de retour** : « Que le locataire a été convoqué par lettre recommandée avec demande d'avis de réception et par lettre simple en date du [date envoi]. »

### Étape 5 — Lecture des photos et enrichissement des descriptions

**Étape la plus importante.** Pour chaque pièce, lire chaque photo associée et corriger / enrichir le brouillon :

- Corriger les erreurs de dictée vocale (ex. « toile a peindre » dicté pour « toile à peindre », « lino » pour « linoléum »).
- Préciser le matériau exact (linoléum, parquet stratifié, carrelage, dalles PVC, toile à peindre, tapisserie, peinture mate/satinée…).
- Identifier les défauts factuels visibles (taches indélébiles, fissures en ramification, trous de chevilles, écaillements de peinture, joints noircis, plinthes dégradées, traces de moisissure…) **uniquement si Antoine les a déjà mentionnés dans le brouillon ou s'ils sont indubitables**.
- Vérifier la cohérence de la liste d'équipements (porte / fenêtre / volet / interrupteur / prise / radiateur / point lumineux / sanitaire / robinetterie / VMC).
- Reformuler dans le vocabulaire technique du métier (cf. `references/vocabulary.md`).

**Doute = abstention.** Si une mention du brouillon n'est pas confirmée par la photo et ne relève pas du vocabulaire courant, ne pas l'inscrire.

**Périmètre strict.** Les photos précisent ou corrigent ce qu'Antoine a dicté ; elles n'introduisent pas d'éléments nouveaux non mentionnés.

### Étape 6 — Structuration pièce par pièce

Pour chaque pièce, produire un bloc strictement conforme :

```
[Titre Heading1 avec numérotation auto, saut de page avant]

[Optionnel : phrase d'accès — « J'accède à [pièce] depuis [autre pièce] par une porte » — uniquement si pertinent]

Sol : [description]

Murs : [description]

Plafond : [description]

Équipement :
  ● [élément 1]
  ● [élément 2]
  ● [...]

[Photos numérotées de la pièce, avec leur légende horodatée + GPS, conservées telles quelles]
```

Voir `references/piece_structure.md` pour le détail.

### Étape 7 — Réordonnancement et titres

Réordonner les pièces selon la logique :

1. **Convocation**
2. **Entrée / Couloir** (point d'entrée du logement)
3. **Pièces de vie** : Salon, Salle à manger, Séjour
4. **Cuisine** + annexes attenantes (Séchoir, Cellier, Arrière-cuisine)
5. **Pièces d'eau** : Salle de bain ou Salle de douche, WC
6. **Chambres** (Chambre 1, Chambre 2…)
7. **Annexes du logement** : Balcon, Loggia, Terrasse, Placard, Dressing, Cave, Garage
8. **Compteurs**
9. **Boîte aux lettres**
10. **Clés** (toujours en dernier)

Corriger les coquilles de titres récurrentes :

- `Wc` → `WC`
- `salle de douche` → `Salle de douche`
- `Sechoir` → `Séchoir`
- `Cuisne` → `Cuisine`
- etc. (liste extensible dans `scripts/apply_layout.py`)

### Étape 8 — Mise en page

Appliquer en une passe :

- **Style `Heading1`** sur chaque titre de pièce avec `pageBreakBefore`, `keepNext`, `outlineLvl=1`, `numId=3` (pour la numérotation auto 1, 2, 3…) et un signet `_Toc_<piece>` pour le sommaire.
- **Justification** sur les paragraphes Sol/Murs/Plafond.
- **Liste à puces** (`●` U+25CF) pour la rubrique Équipement.
- **Sommaire** : `<w:updateFields w:val="true"/>` dans `settings.xml` pour forcer la mise à jour à l'ouverture du document.
- **Conservation de la page de garde** RVC et de la zone signature.

### Étape 9 — Repack et livraison

**Convention de nommage du fichier de sortie (RÈGLE OBLIGATOIRE)** :

> `PV CONSTAT <NOM CLIENT> date <JJ.MM.AAAA>.docx`

- `<NOM CLIENT>` : nom du bailleur requérant (client de l'étude), en majuscules. Pour une personne morale, retenir la dénomination courte sans la forme juridique (ex. `MANCHE HABITAT` et non `EPIC MANCHE HABITAT`). Pour une personne physique, retenir le nom de famille (ex. `DUPONT`).
- `<JJ.MM.AAAA>` : date du constat au format jour.mois.année avec des points séparateurs (ex. `08.04.2026`).

Exemples :

- `PV CONSTAT MANCHE HABITAT date 08.04.2026.docx`
- `PV CONSTAT DUPONT date 15.05.2026.docx`

Repacker le `.docx` en préservant les images et les relations depuis le fichier source, puis présenter le `.docx` final via un lien `computer://`.

## Mode livraison par défaut

**Direct le `.docx` final** — pas d'étape intermédiaire de tableau comparatif. Antoine relit ensuite le document et demande des ajustements ciblés.

Si Antoine demande explicitement un avant/après, livrer un comparatif Markdown pièce par pièce dans un fichier séparé pour validation, puis générer le `.docx`.

## En cas de doute

- Civilité du requérant ou du locataire ambiguë → **demander**, ne pas supposer.
- Détail visible sur photo mais non mentionné dans le brouillon → **ne pas l'ajouter**.
- Pièce dont le titre du brouillon est techniquement discutable (« Pièce 1 ») → demander à Antoine plutôt que d'inventer un nom.
- Formulation ambiguë du brouillon → reformuler de manière neutre et descriptive, sans inférence.

## Enrichissement continu

À chaque EDL, si de nouvelles préférences terminologiques sont validées par Antoine, enrichir **`references/vocabulary.md`** pour la prochaine exécution.
