# Workflow détaillé — constat-reecriture

Ce fichier détaille étape par étape le pipeline de traitement d'un .docx de constat. Le SKILL.md donne la vue d'ensemble ; ce fichier donne les commandes exactes et les pièges connus.

## Prérequis

- Un .docx de constat fourni par l'utilisateur (idéalement dans `/sessions/<session>/mnt/<folder>/`).
- Python 3 disponible (déjà présent en Cowork).
- Le skill `docx` installé (pour `unpack.py` et `pack.py`) — chemin standard : `/sessions/inspiring-relaxed-cori/mnt/.claude/skills/docx/scripts/office/`.

## Variables utiles

```bash
INPUT_DOCX="/sessions/inspiring-relaxed-cori/mnt/Agent Constat/<nom>.docx"
WORK_DIR="/sessions/inspiring-relaxed-cori/constat_work"
OUTPUT_DOCX="/sessions/inspiring-relaxed-cori/mnt/Agent Constat/<nom_final>.docx"
DOCX_SKILL="/sessions/inspiring-relaxed-cori/mnt/.claude/skills/docx/scripts/office"
CONSTAT_SKILL="/sessions/inspiring-relaxed-cori/mnt/.claude/skills/constat-reecriture"
# (pendant le développement : CONSTAT_SKILL="/sessions/inspiring-relaxed-cori/constat-reecriture")
```

## Étape 0 — Préparation

```bash
rm -rf "$WORK_DIR" && mkdir -p "$WORK_DIR"
python3 "$DOCX_SKILL/unpack.py" "$INPUT_DOCX" "$WORK_DIR/unpacked"
```

Vérifier que `$WORK_DIR/unpacked/word/document.xml`, `styles.xml`, `settings.xml` existent.

## Étape 1 — Lecture du contenu

- Lire `document.xml` pour extraire la structure globale.
- Repérer les Heading1 via `grep -n '<w:pStyle w:val="Heading1"/>' "$WORK_DIR/unpacked/word/document.xml"` et les Heading2 de la même façon.
- Extraire le texte brut de chaque sous-chapitre (entre deux `<w:pStyle w:val="Heading2"/>` ou entre un Heading2 et le Heading1 suivant).

Astuce : pour une lecture plus confortable, générer un Markdown intermédiaire avec pandoc :
```bash
pandoc "$INPUT_DOCX" -t markdown -o "$WORK_DIR/brut.md"
```

## Étape 2 — Civilité des demandeurs

Pour chaque demandeur identifié dans le bloc « A LA DEMANDE DE », exécuter une fois `fix_demandeurs.py` avec les arguments `--demandeur "PRENOM NOM:G:ADRESSE"` (un par demandeur).

Le script remplace :
- `PRENOM NOM domicilié(e) ADRESSE.` → `Madame/Monsieur PRENOM NOM, domiciliée/domicilié au ADRESSE.`

**Piège** : si un prénom est ambigu (Camille, Dominique, Claude, Alex, Sacha, Sam, Gabriel(le) dicté Gabriel…), **demander à l'utilisateur**.

## Étape 3 — Introduction

Repérer la zone entre « LEQUEL M'EXPOSE CE QUI SUIT : » et « DEFERANT A CETTE REQUISITION : ». Elle contient typiquement :
- soit un paragraphe orphelin (« Facturiez RUAULT » ou similaire, scorie de dictée) ;
- soit du vide.

La remplacer par 3 paragraphes de prose selon règle 16 (références/rules.md).

Pour le remplacement XML : repérer le `<w:p>…</w:p>` contenant la phrase orpheline, et le substituer par 3 nouveaux `<w:p>` au style `HOParagraphe`. Template recommandé pour chaque paragraphe :

```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="HOParagraphe"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
      <w:sz w:val="24"/>
    </w:rPr>
    <w:t xml:space="preserve">[TEXTE DU PARAGRAPHE]</w:t>
  </w:r>
</w:p>
```

Note : la justification viendra automatiquement via la règle 19 (style HOParagraphe enrichi par `apply_layout.py`).

## Étape 4 — Réécriture des constatations

**Approche recommandée** : pour chaque sous-chapitre, extraire le bloc complet de `<w:p>` entre deux headings, lire attentivement le texte brut + la description visuelle des photos s'il y en a (photos typiquement encodées dans `<w:drawing>` immédiatement après les paragraphes textuels), puis produire la version réécrite.

**Points de vigilance** :

- **Paragraphes multi-runs** : un paragraphe peut contenir plusieurs `<w:r>` séparés par un `<w:br/>`. La délimitation d'un paragraphe se fait toujours via les balises `<w:p>` / `</w:p>` — utiliser `xml.rfind('    <w:p>', 0, pos)` et `xml.find('    </w:p>', pos)` pour trouver les bornes.
- **Caractères spéciaux** : toujours échapper `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;` lors de la création de nouveaux `<w:t>`.
- **Remplacer du XML existant** : l'outil `Edit` fonctionne bien si on repère une chaîne unique ; sinon passer par un script Python qui manipule le XML via regex de bornes de paragraphes.

**Ordre des règles** à garder en tête pendant la réécriture : 1 (Je constate), 2 (zéro lien causal — le plus important), 3 (descriptif), 11 (périmètre Antoine), 12 (doute = abstention), 14 (paragraphes aérés).

## Étape 5 — Correction des titres

```bash
python3 "$CONSTAT_SKILL/scripts/correct_titles.py" "$WORK_DIR/unpacked/word/document.xml"
```

Applique les substitutions encodées dans le script. Sortie attendue : liste des corrections appliquées.

## Étape 6 — Mise en page

```bash
python3 "$CONSTAT_SKILL/scripts/apply_layout.py" "$WORK_DIR/unpacked"
python3 "$CONSTAT_SKILL/scripts/apply_intra_chapter_breaks.py" "$WORK_DIR/unpacked/word/document.xml"
```

`apply_layout.py` applique en une passe :
- `styles.xml` : Heading1 pageBreakBefore, Heading2 keepNext (suppression de pageBreakBefore si présent), HOParagraphe justify.
- `document.xml` : pageBreakBefore individuel sur chaque Heading2 sauf le premier de chaque chapitre (détection automatique via positions dans le XML).
- `settings.xml` : updateFields=true.

`apply_intra_chapter_breaks.py` applique la **règle « bloc = page »** (règle 20) :
- Dans chaque chapitre, détecte les blocs de commentaire (suites de paragraphes de texte descriptif hors photos/captions).
- Ajoute `<w:pageBreakBefore/>` au premier paragraphe de chaque bloc SAUF le tout premier bloc du chapitre (qui reste collé au titre).
- Objectif : chaque bloc de texte démarre en haut de page pour que les photos décrites s'enchaînent juste en dessous, sans coupure entre texte et illustrations.

Les deux scripts sont **idempotents** : si une modification a déjà été appliquée (ex. pageBreakBefore déjà présent), elle n'est pas redoublée.

## Étape 7 — Validation + Repack

**Convention de nommage obligatoire du fichier de sortie** :

> `PV CONSTAT <NOM REQUERANT> <JJ.MM.AAAA>.docx`

- `<NOM REQUERANT>` : nom de famille du demandeur en majuscules ; plusieurs demandeurs joints par un tiret (ex. `RUAULT-TANGUY`).
- `<JJ.MM.AAAA>` : date du constat avec points (ex. `28.04.2026`).

Définir `OUTPUT_DOCX` selon ce format :

```bash
OUTPUT_DOCX="/sessions/inspiring-relaxed-cori/mnt/Agent Constat/PV CONSTAT VAGNER 28.04.2026.docx"
```

```bash
# Validation XML pré-pack
python3 -c "
import xml.etree.ElementTree as ET
for f in ['document.xml', 'styles.xml', 'settings.xml']:
    ET.parse(f'$WORK_DIR/unpacked/word/{f}')
    print(f'{f} OK')
"

# Repack avec préservation des binaires via --original
python3 "$DOCX_SKILL/pack.py" \
  "$WORK_DIR/unpacked" \
  "$OUTPUT_DOCX" \
  --original "$INPUT_DOCX"
```

Le `pack.py` effectue lui-même une validation schema OOXML. Si « All validations PASSED! » apparaît, le .docx est bon.

## Étape 8 — Livraison

Utiliser l'outil `present_files` :

```
present_files(files=[{"file_path": "$OUTPUT_DOCX"}])
```

Message accompagnant court : rappeler les choix principaux (intro raccourcie, sauts de page, justification) et laisser Antoine relire.

## Itération ciblée

Si Antoine demande un ajustement sur un chapitre précis après livraison :
- Relire le brut original pour ce chapitre.
- Modifier uniquement les `<w:p>` concernés (via `Edit` sur document.xml).
- Ne pas repartir à zéro : pas besoin de ré-exécuter `apply_layout.py` ni `correct_titles.py` si ces étapes ont déjà été faites.
- Repack via la même commande.
