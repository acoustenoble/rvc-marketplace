#!/usr/bin/env python3
"""
apply_layout.py — mise en page du constat (règles 17, 18, 19).

Usage :
    python3 apply_layout.py <chemin_vers_unpacked>

Effets (tous idempotents) :
    styles.xml :
        - Heading1 : ajoute <w:pageBreakBefore/> dans le pPr du style
        - Heading2 : ajoute <w:keepNext/> dans le pPr du style
                     retire <w:pageBreakBefore/> du pPr du style (s'il y était)
        - HOParagraphe : ajoute <w:jc w:val="both"/> dans le pPr du style
    document.xml :
        - Tous les Heading2 sauf le premier de chaque Heading1 reçoivent
          <w:pageBreakBefore/> individuellement, inséré APRÈS <w:pStyle w:val="Heading2"/>
          (l'ordre du schéma OOXML l'exige).
    settings.xml :
        - Ajoute <w:updateFields w:val="true"/> pour forcer la MAJ du sommaire.

Piège OOXML — ordre strict des enfants de <w:pPr> :
    pStyle → keepNext → keepLines → pageBreakBefore → framePr → widowControl
    → numPr → ... → spacing → ind → contextualSpacing → ... → jc → ...
    → outlineLvl → ...
    Le schéma refuse tout élément inséré hors séquence. Le script insère donc
    chaque nouvel élément à la bonne position par rapport aux éléments déjà
    présents dans le pPr.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Ordre canonique (partiel, couvrant ce qu'on manipule) des enfants de <w:pPr>
# Source : ECMA-376, CT_PPr. Plus le chiffre est bas, plus l'élément vient tôt.
PPR_ORDER: dict[str, int] = {
    'pStyle': 1,
    'keepNext': 2,
    'keepLines': 3,
    'pageBreakBefore': 4,
    'framePr': 5,
    'widowControl': 6,
    'numPr': 7,
    'suppressLineNumbers': 8,
    'pBdr': 9,
    'shd': 10,
    'tabs': 11,
    'suppressAutoHyphens': 12,
    'kinsoku': 13,
    'wordWrap': 14,
    'overflowPunct': 15,
    'topLinePunct': 16,
    'autoSpaceDE': 17,
    'autoSpaceDN': 18,
    'bidi': 19,
    'adjustRightInd': 20,
    'snapToGrid': 21,
    'spacing': 22,
    'ind': 23,
    'contextualSpacing': 24,
    'mirrorIndents': 25,
    'suppressOverlap': 26,
    'jc': 27,
    'textDirection': 28,
    'textAlignment': 29,
    'textboxTightWrap': 30,
    'outlineLvl': 31,
    'divId': 32,
    'cnfStyle': 33,
    'rPr': 34,  # en réalité extérieur, mais certains docs le mettent là
    'sectPr': 35,
    'pPrChange': 36,
}


# ------------------------------------------------------------------ utilitaires

def _style_block_pattern(style_id: str) -> re.Pattern[str]:
    return re.compile(
        r'<w:style\s+w:type="paragraph"[^>]*w:styleId="'
        + re.escape(style_id)
        + r'"[^>]*>.*?</w:style>',
        re.DOTALL,
    )


def _inject_into_pPr(
    block: str,
    new_element_tag: str,        # ex : 'jc'
    new_element_xml: str,         # ex : '<w:jc w:val="both"/>'
) -> tuple[str, bool]:
    """Insère `new_element_xml` dans le <w:pPr>...</w:pPr> de `block`, au bon
    rang schema. Idempotent."""
    ppr_open = block.find('<w:pPr>')
    ppr_close = block.find('</w:pPr>')

    if ppr_open == -1:
        # Créer un pPr minimal juste après <w:name .../>
        # (vaut mieux ne pas arriver ici : les styles sous suivi en ont tous un)
        injection = f'<w:pPr>\n      {new_element_xml}\n    </w:pPr>\n    '
        # Insérer juste avant <w:rPr> ou à défaut avant </w:style>
        idx = block.find('<w:rPr>')
        if idx == -1:
            idx = block.rfind('</w:style>')
        return block[:idx] + injection + block[idx:], True

    ppr_content = block[ppr_open + len('<w:pPr>') : ppr_close]

    # Idempotence : si l'élément-balise est déjà présent, ne rien faire
    if re.search(r'<w:' + re.escape(new_element_tag) + r'(\s|/|>)', ppr_content):
        return block, False

    new_order = PPR_ORDER[new_element_tag]

    # Trouver tous les enfants de pPr pour repérer la bonne position
    # Pattern : <w:TAG ... /> ou <w:TAG ...> ... </w:TAG>
    child_pattern = re.compile(r'<w:(\w+)([^/>]*)(/?)>')
    inserted = False
    for m in child_pattern.finditer(ppr_content):
        tag = m.group(1)
        if tag not in PPR_ORDER:
            continue
        if PPR_ORDER[tag] > new_order:
            # Insérer juste avant cet élément
            insert_rel = m.start()
            new_content = (
                ppr_content[:insert_rel]
                + new_element_xml
                + '\n      '
                + ppr_content[insert_rel:]
            )
            inserted = True
            break

    if not inserted:
        # Ajouter à la fin du pPr, juste avant </w:pPr>
        # Détecter l'indentation du dernier élément pour rester cohérent
        new_content = ppr_content.rstrip() + '\n      ' + new_element_xml + '\n    '

    new_block = (
        block[: ppr_open + len('<w:pPr>')]
        + new_content
        + block[ppr_close:]
    )
    return new_block, True


def style_inject(
    styles_xml: str,
    style_id: str,
    style_name: str,
    new_element_tag: str,
    new_element_xml: str,
) -> tuple[str, bool]:
    pattern = _style_block_pattern(style_id)
    m = pattern.search(styles_xml)
    if m is None:
        print(f'  [{style_name}] style introuvable — skip')
        return styles_xml, False

    block = m.group(0)
    new_block, changed = _inject_into_pPr(block, new_element_tag, new_element_xml)
    if not changed:
        print(f'  [{style_name}] déjà présent : {new_element_xml} — skip')
        return styles_xml, False

    styles_xml = styles_xml.replace(block, new_block, 1)
    print(f'  [{style_name}] ajouté : {new_element_xml}')
    return styles_xml, True


def style_remove_element(
    styles_xml: str,
    style_id: str,
    style_name: str,
    element_tag: str,
) -> tuple[str, bool]:
    """Retire tout enfant `<w:{tag} .../>` du <w:pPr> du style."""
    pattern = _style_block_pattern(style_id)
    m = pattern.search(styles_xml)
    if m is None:
        return styles_xml, False

    block = m.group(0)
    elem_re = re.compile(
        r'[ \t]*<w:' + re.escape(element_tag) + r'(?:\s[^/]*)?/>\s*\n?'
    )
    new_block = elem_re.sub('', block, count=1)
    if new_block == block:
        return styles_xml, False

    styles_xml = styles_xml.replace(block, new_block, 1)
    print(f'  [{style_name}] retiré : <w:{element_tag}/>')
    return styles_xml, True


# ------------------------------------------------------- mise en page document

def adjust_subchapter_breaks(doc_xml: str) -> tuple[str, int, int, int]:
    """Insère <w:pageBreakBefore/> après <w:pStyle w:val="Heading2"/> dans tous
    les paragraphes Heading2 SAUF le premier de chaque Heading1.

    Idempotent : un Heading2 qui contient déjà <w:pageBreakBefore/> est ignoré.
    """
    h1_pattern = re.compile(
        r'    <w:p>\s*<w:pPr>\s*<w:pStyle w:val="Heading1"/>',
        re.MULTILINE,
    )
    h2_pattern = re.compile(
        r'    <w:p>\s*<w:pPr>\s*<w:pStyle w:val="Heading2"/>',
        re.MULTILINE,
    )
    h1_positions = [m.start() for m in h1_pattern.finditer(doc_xml)]
    h2_matches = list(h2_pattern.finditer(doc_xml))

    first_h2_positions: set[int] = set()
    for h1_pos in h1_positions:
        for h2 in h2_matches:
            if h2.start() > h1_pos:
                first_h2_positions.add(h2.start())
                break

    PSTYLE = '<w:pStyle w:val="Heading2"/>'
    inserts: list[int] = []
    for h2 in h2_matches:
        if h2.start() in first_h2_positions:
            continue
        p_end = doc_xml.find('</w:p>', h2.start())
        block = doc_xml[h2.start() : p_end]
        if '<w:pageBreakBefore/>' in block:
            continue  # déjà cassé
        pstyle_pos = doc_xml.find(PSTYLE, h2.start())
        assert pstyle_pos != -1, 'pStyle Heading2 introuvable'
        inserts.append(pstyle_pos + len(PSTYLE))

    for pos in sorted(inserts, reverse=True):
        doc_xml = doc_xml[:pos] + '\n        <w:pageBreakBefore/>' + doc_xml[pos:]

    return doc_xml, len(h1_positions), len(h2_matches), len(inserts)


def settings_enable_updatefields(settings_xml: str) -> tuple[str, bool]:
    if '<w:updateFields' in settings_xml:
        return settings_xml, False
    if '<w:proofState' in settings_xml:
        return (
            re.sub(
                r'(<w:proofState[^/]*/>)',
                r'\1\n  <w:updateFields w:val="true"/>',
                settings_xml,
                count=1,
            ),
            True,
        )
    return (
        re.sub(
            r'(<w:settings[^>]*>)',
            r'\1\n  <w:updateFields w:val="true"/>',
            settings_xml,
            count=1,
        ),
        True,
    )


def validate_xml(path: Path) -> None:
    ET.parse(path)


# ------------------------------------------------------------------ main

def main(unpacked_dir: Path) -> None:
    word_dir = unpacked_dir / 'word'
    doc_path = word_dir / 'document.xml'
    styles_path = word_dir / 'styles.xml'
    settings_path = word_dir / 'settings.xml'

    for p in (doc_path, styles_path, settings_path):
        if not p.exists():
            raise FileNotFoundError(f'Fichier attendu introuvable : {p}')

    print('\n== styles.xml ==')
    styles_xml = styles_path.read_text(encoding='utf-8')
    styles_xml, _ = style_inject(
        styles_xml, 'Heading1', 'Heading1', 'pageBreakBefore', '<w:pageBreakBefore/>',
    )
    styles_xml, _ = style_remove_element(
        styles_xml, 'Heading2', 'Heading2', 'pageBreakBefore',
    )
    styles_xml, _ = style_inject(
        styles_xml, 'Heading2', 'Heading2', 'keepNext', '<w:keepNext/>',
    )
    styles_xml, _ = style_inject(
        styles_xml, 'HOParagraphe', 'HOParagraphe', 'jc', '<w:jc w:val="both"/>',
    )
    styles_path.write_text(styles_xml, encoding='utf-8')
    validate_xml(styles_path)
    print('  styles.xml : XML OK')

    print('\n== document.xml ==')
    doc_xml = doc_path.read_text(encoding='utf-8')
    doc_xml, n_h1, n_h2, n_inserted = adjust_subchapter_breaks(doc_xml)
    print(f'  Heading1 trouvés : {n_h1}')
    print(f'  Heading2 trouvés : {n_h2}')
    print(f'  Premiers Heading2 épargnés : {n_h1}')
    print(f'  pageBreakBefore insérés : {n_inserted}')
    doc_path.write_text(doc_xml, encoding='utf-8')
    validate_xml(doc_path)
    print('  document.xml : XML OK')

    print('\n== settings.xml ==')
    settings_xml = settings_path.read_text(encoding='utf-8')
    settings_xml, changed = settings_enable_updatefields(settings_xml)
    if changed:
        settings_path.write_text(settings_xml, encoding='utf-8')
        print('  updateFields=true ajouté')
    else:
        print('  updateFields déjà présent — skip')
    validate_xml(settings_path)
    print('  settings.xml : XML OK')

    print('\nMise en page appliquée avec succès.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage : apply_layout.py <chemin_vers_unpacked>', file=sys.stderr)
        sys.exit(2)
    main(Path(sys.argv[1]).resolve())
