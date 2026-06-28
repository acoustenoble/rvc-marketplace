---
name: constat-reecriture
description: "Réécrit techniquement les constatations d'un procès-verbal de constat (.docx) de commissaire de justice. À déclencher IMPÉRATIVEMENT dès que l'utilisateur fournit ou mentionne un .docx de constat, procès-verbal, constat d'huissier, constat de commissaire de justice, PV de constat, ou tout document contenant la formule 'J'ai procédé aux constatations suivantes'. Le skill nettoie la dictée vocale, applique le style 'Je constate' strictement descriptif, corrige la civilité des demandeurs, réécrit l'introduction de la requête, corrige les titres, applique la mise en page (sauts de page, justification, sommaire) et livre directement le .docx final. Utiliser même si l'utilisateur ne dit pas explicitement 'réécris' — toute remise d'un .docx de constat déclenche ce skill."
---

# Constat — réécriture technique

## Étape directrice — Finalité du constat (À FAIRE AVANT TOUT)

Avant toute réécriture, **demander à Antoine à quoi le constat doit servir** (preuve avant travaux ; mise en cause d'un constructeur/assureur ; pièce d'expertise/référé ; dossier dommages-ouvrage ; trouble de voisinage ; affichage ; occupation…). Puis **adapter le document pour qu'il serve parfaitement cet objectif** :

- **Structure** : regroupement le plus parlant pour le destinataire (par unité, par type de désordre, chronologique…) — règle 22.
- **Emphase / repérage** : mettre en avant (plan annoté, photos cerclées, ordre) les éléments utiles à l'objectif — règles 25-26.
- **Niveau de détail** : approfondir ce qui sert l'objectif, rester sobre ailleurs.
- **Registre / lexique** : vocabulaire technique adapté à l'objet (pathologie du bâtiment, baux, urbanisme…), cohérent avec le dictionnaire de référence.

**Garde-fou impératif** : adapter organisation, emphase et vocabulaire ne doit **jamais** introduire de conclusion, de lien causal ni d'appréciation (règles 2, 3, 4). On adapte la présentation et la précision descriptive à l'objectif, **pas** la portée probatoire.

## Mode réorganisation (sur demande)

Si Antoine demande une remise en forme structurelle (au-delà de la réécriture) : réorganiser par unité logique (règle 22), renuméroter les photographies (règle 23), déplacer/annoter le plan de repérage (règle 25), cercler sélectivement les désordres peu visibles après validation d'un échantillon (règle 26), gérer le demandeur personne morale (règle 24), rendre les déclarations de tiers au style indirect (règle 27).


## Quand utiliser ce skill

Déclencheurs (tout .docx répondant à l'un des critères suivants) :

- Contient la phrase « **J'ai procédé aux constatations suivantes** » (marqueur canonique d'un constat de commissaire de justice).
- Contient les blocs « **A LA DEMANDE DE :** », « **EN PRESENCE DE :** », « **LEQUEL M'EXPOSE CE QUI SUIT :** », « **DEFERANT A CETTE REQUISITION :** ».
- Titré « procès-verbal de constat », « PV de constat », « constat d'huissier », « constat de commissaire de justice ».

Si l'un de ces critères est présent, déclencher ce skill **même si l'utilisateur ne demande pas explicitement de réécriture** — l'intention implicite d'Antoine lorsqu'il livre un constat est qu'il soit retravaillé selon ses règles.

## Ce que ce skill fait

1. **Corrige la civilité** des demandeurs dans le bloc « A LA DEMANDE DE » (ajoute « Madame/Monsieur » + accorde « domicilié(e) »).
2. **Rédige l'introduction courte** (3 paragraphes de prose) entre « LEQUEL M'EXPOSE » et « DÉFÉRANT », en synthèse générale.
3. **Réécrit chaque chapitre de constatations** dans le style « Je constate », strictement descriptif, sans lien causal ni conclusion, en nettoyant la dictée vocale.
4. **Corrige les coquilles de titres** récurrentes (Vmc → VMC, Nuissances → Nuisances, Lesions → Lésions…).
5. **Applique la mise en page** : saut de page sur les grands chapitres, sauts individuels sur les sous-chapitres (sauf le premier de chaque chapitre), texte justifié, sommaire mis à jour à l'ouverture.
6. **Repack le .docx final** et le présente à l'utilisateur.

## Ce que ce skill ne fait PAS

- Ne modifie **pas** la structure de pages d'en-tête (demandeur, présences, mentions obligatoires) sauf la civilité.
- Ne modifie **pas** les photos ni leur ordre.
- Ne modifie **pas** la signature, la clôture, la mise en forme globale.
- N'ajoute **pas** d'observations que l'utilisateur n'a pas formulées dans le texte brut (le texte brut délimite strictement le périmètre descriptif — les photos servent à *préciser*, pas à *étendre*).

## Règles cardinales (lecture obligatoire)

Avant toute réécriture, lire **`references/rules.md`** — il contient les 19 règles de rédaction, leur motivation juridique et leur mode d'application. La règle la plus importante est la règle 2 (**aucun lien de causalité**) : un constat qui contient une conclusion ou une inférence causale perd sa valeur probatoire.

Lire également **`references/vocabulary.md`** — journal des préférences terminologiques validées ; à consulter systématiquement et à enrichir au fil des constats.

Pour le vocabulaire technique du bâtiment, s'appuyer sur le dictionnaire de référence `/sessions/inspiring-relaxed-cori/mnt/Agent Constat/publication (1).pdf` (source terminologique : matériaux, composants, typologies de désordres).

## Workflow

Suivre scrupuleusement les étapes suivantes. Chaque étape est détaillée dans **`references/workflow.md`**.

### Étape 0 — Préparation

1. Vérifier que le .docx fourni contient bien les marqueurs d'un constat.
2. Créer un répertoire de travail : `mkdir -p /sessions/inspiring-relaxed-cori/constat_work/unpacked`.
3. Dépaqueter le .docx : `python3 /sessions/inspiring-relaxed-cori/mnt/.claude/skills/docx/scripts/office/unpack.py <input.docx> /sessions/inspiring-relaxed-cori/constat_work/unpacked`.

### Étape 1 — Lecture du contenu

Lire le document pour identifier :
- Les demandeurs (bloc « A LA DEMANDE DE ») + leur genre (nécessaire pour l'accord).
- Les personnes présentes (bloc « EN PRESENCE DE ») — à contre-vérifier contre les noms cités dans les constatations (la dictée vocale corrompt souvent les patronymes).
- La structure chapitrée des constatations (Heading1 pour les grands chapitres, Heading2 pour les sous-chapitres).
- Le texte brut de chaque sous-chapitre.

### Étape 2 — Civilité des demandeurs

Pour chaque demandeur, exécuter :

```bash
python3 scripts/fix_demandeurs.py \
  /sessions/inspiring-relaxed-cori/constat_work/unpacked/word/document.xml \
  --demandeur "Céline RUAULT:F:1 Rue Du Lin, 35510 CESSON-SÉVIGNÉ" \
  --demandeur "Vanessa TANGUY:F:1 Rue Du Lin, 35510 CESSON-SÉVIGNÉ"
```

Format : `"PRENOM NOM:G:ADRESSE"` où `G` vaut `M` (Monsieur / domicilié) ou `F` (Madame / domiciliée). **Ne jamais supposer le genre** ; si un prénom est ambigu (Camille, Dominique…), demander à l'utilisateur.

### Étape 3 — Introduction de la requête

Remplacer le paragraphe orphelin (souvent une scorie de dictée type « Facturiez RUAULT ») qui se trouve entre « LEQUEL M'EXPOSE CE QUI SUIT » et « DÉFÉRANT À CETTE RÉQUISITION » par **3 paragraphes courts de prose** :

- **§1** : identification des demandeurs et de leur situation générale.
- **§2** : formulation générale du problème (une phrase synthétique, ex. : « désordres liés principalement à l'humidité, à un défaut de ventilation… »). **Ne pas lister les désordres** — c'est le rôle des constatations.
- **§3** : formulation de la réquisition (« me requièrent… de dresser procès-verbal de constat… »).

Utiliser le script générique `scripts/replace_paragraph_by_anchor.py` si disponible, ou manipuler le XML à la main avec `Edit`.

### Étape 4 — Réécriture chapitre par chapitre

Pour chaque sous-chapitre (Heading2), réécrire le texte en appliquant **toutes les règles de `references/rules.md`**, en particulier :

- Style première personne (« Je constate… », « Je relève… »).
- Descriptif uniquement (matériau, localisation, dimension approximative, orientation, couleur, état visible).
- **Zéro lien causal** (jamais « dû à », « causé par », « provenant de »…).
- **Périmètre strict** : ne décrire que ce qu'Antoine a mentionné dans le brut. Les photos précisent, n'étendent pas.
- **Doute = abstention** : ne pas écrire un détail si le skill n'est pas certain à 100 %.
- **Paragraphes aérés** : une idée = un paragraphe court, saut de ligne entre blocs d'observation.

Remplacer chaque bloc de paragraphes source par sa version réécrite via `Edit` sur `document.xml`, ou via un script batch si plusieurs remplacements sont à faire.

### Étape 5 — Correction des titres

```bash
python3 scripts/correct_titles.py /sessions/inspiring-relaxed-cori/constat_work/unpacked/word/document.xml
```

Corrige les coquilles récurrentes sur les titres de chapitres/sous-chapitres. Les corrections sont listées dans le script (extensible).

### Étape 6 — Mise en page

```bash
python3 scripts/apply_layout.py /sessions/inspiring-relaxed-cori/constat_work/unpacked
```

Ce script applique en une passe :

- `styles.xml` : `<w:pageBreakBefore/>` sur `Heading1`, `<w:keepNext/>` sur `Heading2` (et retire `<w:pageBreakBefore/>` de Heading2 s'il y était), `<w:jc w:val="both"/>` sur `HOParagraphe`.
- `document.xml` : `<w:pageBreakBefore/>` individuel sur chaque `Heading2` **sauf le premier de chaque `Heading1`** (le premier sous-chapitre reste collé au titre de chapitre).
- `settings.xml` : `<w:updateFields w:val="true"/>` pour forcer la mise à jour du sommaire à l'ouverture.

### Étape 7 — Repack et livraison

**Convention de nommage du fichier de sortie (RÈGLE OBLIGATOIRE)** :

> `PV CONSTAT <NOM REQUERANT> <JJ.MM.AAAA>.docx`

- `<NOM REQUERANT>` : nom de famille du demandeur, en majuscules. S'il y a plusieurs demandeurs, les juxtaposer séparés par un tiret (ex. : `RUAULT-TANGUY`).
- `<JJ.MM.AAAA>` : date du constat (extraite de la mention « L'AN … » ou des photos), au format jour.mois.année avec des points séparateurs (ex. : `28.04.2026`).

Exemples :
- `PV CONSTAT VAGNER 28.04.2026.docx`
- `PV CONSTAT RUAULT-TANGUY 20.04.2026.docx`
- `PV CONSTAT DUPONT 03.06.2026.docx`

```bash
python3 /sessions/inspiring-relaxed-cori/mnt/.claude/skills/docx/scripts/office/pack.py \
  /sessions/inspiring-relaxed-cori/constat_work/unpacked \
  "/sessions/inspiring-relaxed-cori/mnt/Agent Constat/PV CONSTAT VAGNER 28.04.2026.docx" \
  --original "<input.docx>"
```

Le flag `--original` garantit que les parties binaires (images, relations) sont préservées depuis le fichier source.

Puis présenter le .docx final via `present_files` (ou un lien `computer://`).

## Mode livraison par défaut

**Direct le .docx final** — pas d'étape intermédiaire de tableau comparatif. Antoine relit ensuite le document et demande les ajustements ciblés.

Si Antoine demande explicitement un avant/après (« fais-moi d'abord un comparatif »), livrer un tableau Markdown avant/après chapitre par chapitre dans un fichier séparé, pour validation, puis générer le .docx.

## En cas de doute

- Nom propre ambigu / prénom à genre incertain → **demander**, ne pas supposer.
- Détail visible sur photo mais non mentionné dans le brut → **ne pas l'ajouter**.
- Titre techniquement discutable → signaler via commentaire Word (`<w:comment>`) plutôt que modifier silencieusement.
- Formulation ambiguë du brut dictée → reformuler de manière neutre et descriptive.

## Enrichissement continu

À chaque constat, si de nouvelles préférences terminologiques sont validées par Antoine, enrichir **`references/vocabulary.md`** pour la prochaine exécution.
