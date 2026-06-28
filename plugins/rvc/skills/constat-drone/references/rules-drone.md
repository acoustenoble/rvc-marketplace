# Règles spécifiques au constat drone

Ce skill **hérite intégralement** des 21 règles de `constat-reecriture` (réécriture des
constatations : style « Je constate », zéro lien de causalité, périmètre strict, doute = abstention,
civilité des demandeurs, mise en page, nommage). Lire ce fichier de règles en complément, pas à la place.

Les règles ci-dessous s'ajoutent et concernent l'**enrichissement drone**.

---

## A — Réécriture des constatations (rappel + spécificité drone)

**A1. Vocabulaire technique Dicobat.** Les constatations sont réécrites en langage technique du
bâtiment (matériaux, ouvrages, désordres) en s'appuyant sur le dictionnaire Dicobat. Antoine vise la
**précision maximale**. Le périmètre reste strictement borné par ce qu'il a dicté (règle 11 de
constat-reecriture) : on précise et on corrige la dictée, on n'invente pas d'éléments.

**A2. Vue aérienne.** Les constatations d'un constat drone décrivent typiquement des éléments vus du
ciel ou en survol (toitures, façades en hauteur, emprises, limites séparatives). Conserver le repérage
par orientation (sud-ouest, nord-ouest, nord-est…) et par ouvrage (mur, muret, pignon, couverture)
exactement comme dicté ; préciser le vocabulaire (ex. « couverture en zinc », « solin », « arase »,
« descente d'eaux pluviales » plutôt que « descente de P »).

**A3. Zéro lien causal — même en survol.** Ne pas écrire qu'un désordre « provient » d'un élément voisin.
Décrire chaque ouvrage séparément.

---

## B — Enrichissement drone

**B1. Texte juridique figé.** Le texte des sections drone (`references/boilerplate-drone.md`) ne se
réécrit pas, ne se paraphrase pas, ne se « fluidifie » pas. On remplace uniquement les `{{placeholders}}`.
C'est du texte à valeur probatoire/réglementaire.

**B2. Source des valeurs = le PDF.** Toutes les valeurs variables (n° de série, enregistrement,
certificat, classe, masse, sous-catégorie, hauteur max, commune, assurance…) sont extraites du PDF
fourni. Ne jamais inventer une valeur réglementaire. Si une valeur attendue est absente du PDF, le
signaler à Antoine.

**B3. Cohérence sous-catégorie / hauteur.** La sous-catégorie ({{SOUS_CATEGORIE}}) et la hauteur max
({{HAUTEUR_MAX}}) doivent être reprises telles quelles de la page « Règles applicables au présent vol »
du PDF. Ne pas confondre la hauteur réglementaire générale (120 m) avec la hauteur effective du vol
(ex. 49 m).

**B4. METAR absent.** Si le PDF ne contient pas de code METAR rempli (placeholder `data.metars.*`),
**retirer entièrement** la phrase « Certification de contrôle des bonnes conditions de vol » plutôt
que de laisser un placeholder visible.

---

## C — Placeholders du PDF

**C1. Suppression des placeholders non résolus.** Le PDF brut contient des champs logiciel non
substitués (`data.report_date_verbal`, `data.report_time`, `project.requesters_entity.intro`,
`[DATE EN LETTRES]`, `[Numéro de référence]`, « Date de naissance », « Ville de naissance », honoraires
vides…). Ces informations proviennent du DOCX brouillon ou sont inutiles : **ne jamais les recopier**.
La page de garde, la date, l'identité et l'intro de requête viennent du DOCX.

**C2. Émolument / honoraires.** Laisser le bloc émolument du DOCX brouillon tel quel (Antoine le remplit
à la main). Ne pas importer le bloc honoraires vide du PDF.

---

## D — Réconciliation PDF ↔ DOCX

**D1. Le DOCX brouillon fait foi pour l'identité.** En cas de divergence de nom, de nombre de
requérants ou de date entre le PDF et le DOCX, **le DOCX prime**. Exemple du dossier de référence :
le PDF dit « GAUTIER », 1 requérant, 02.06.2026 ; le DOCX dit « GAUTHIER », 2 requérants (Eric +
Valérie ALEXIS), 05.06.2026 → on retient **GAUTHIER, 2 requérants, 05.06.2026**, et on aligne toute
mention du PDF (page de garde reconstruite, requête) sur ces valeurs.

**D2. Civilité.** Appliquer la règle 15 de constat-reecriture : « M. Eric GAUTHIER domicilié(e) … » →
« Monsieur Eric GAUTHIER, domicilié au … » ; « Mme Valérie ALEXIS domicilié(e) … » → « Madame Valérie
ALEXIS, domiciliée au … ». Prénom ambigu → demander.

---

## E — Structure du document final

**E1. Ordre des sections** (un seul .docx enrichi, éditable) :

1. Page de garde + Sommaire (du DOCX, identité alignée DOCX)
2. Requête (demande / civilité / intro 3 §) — bloc « DÉFÉRANT » enrichi de la qualité d'exploitant + télépilote (SECTION 1)
3. **INFORMATION SUR L'APPAREIL UTILISÉ** (titre niveau 1) avec, juste sous le titre, un **ENCADRÉ** mis en avant (cadre + fond clair) : phrase générique indiquant que le constat est réalisé au drone et que les données numériques (visite 360°, photos, vidéos selon le support) sont consultables au(x) lien(s) suivant(s), suivi d'un emplacement « [ lien(s) à insérer ] » qu'Antoine remplit (SECTION 2)
4. **CONSTATATIONS** (titre niveau 1 — apparaît dans le sommaire et démarre toujours en haut de page) → ligne « J'AI PROCÉDÉ AUX CONSTATATIONS SUIVANTES : » → **constatations réécrites**
5. Clôture « Telles sont les constatations… » + bloc signature/émolument (du DOCX)
6. **COMPTE-RENDU DE VOL** (SECTION 3) — placé APRÈS la signature, juste avant les certifications
7. **CERTIFICATIONS TECHNIQUES** (SECTION 4)
8. **TRAVAUX PRÉPARATOIRES** (SECTION 5)
9. **AUTORISATIONS ET DÉCLARATIONS ADMINISTRATIVES DE VOL** (SECTION 6)
10. **VÉRIFICATIONS TECHNIQUES PRÉALABLES** (SECTION 7)
11. **ANNEXES** — images du PDF + légendes (SECTION 8)

**E2. Titres de section = niveau 1.** Chaque titre majuscule (INFORMATION SUR L'APPAREIL,
CERTIFICATIONS TECHNIQUES, ANNEXES…) reçoit le style `Heading1` (créé par le skill s'il n'existe pas),
afin d'alimenter automatiquement le Sommaire (champ TOC niveaux 1-4) et de démarrer en haut de page.

**E3. Images en annexes uniquement.** Aucune carte n'est insérée dans le corps : toutes vont en
ANNEXES, décrites par une légende neutre (pas de conclusion, pas d'interprétation juridique de la carte).

**E4. Nommage de sortie.** Convention héritée : `PV CONSTAT <NOM REQUERANT> <JJ.MM.AAAA>.docx`
(nom du DOCX, requérants joints par tiret, date du DOCX). Ex. `PV CONSTAT GAUTHIER 05.06.2026.docx`.
