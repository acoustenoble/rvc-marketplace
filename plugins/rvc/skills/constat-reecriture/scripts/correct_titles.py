#!/usr/bin/env python3
"""
correct_titles.py — corrige les coquilles récurrentes dans les titres (règle 9).

Usage :
    python3 correct_titles.py <document.xml>

Stratégie :
    Pour ne pas risquer de toucher au corps du texte, on ne remplace que dans
    les `<w:t>` appartenant à un paragraphe de style Heading1/Heading2/Heading3.
    On repère ces paragraphes par regex de borne `<w:p>` et on remplace
    UNIQUEMENT à l'intérieur du texte des runs du titre.

Dictionnaire de corrections (extensible) :
    {"Vmc": "VMC", "Nuissances": "Nuisances", "Lesions": "Lésions", ...}

Idempotent : si le titre est déjà corrigé, aucune modification.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Corrections appliquées aux titres de Heading1/Heading2/Heading3
# Extensible : ajouter ici toute nouvelle coquille rencontrée sur un constat.
CORRECTIONS: dict[str, str] = {
    'Vmc': 'VMC',
    'VMC ': 'VMC ',  # no-op, conservé pour clarté
    'Nuissances': 'Nuisances',
    'Nuisssances': 'Nuisances',
    'Lesions': 'Lésions',
    'Lésiones': 'Lésions',
    'cave ': 'Cave ',  # souvent en minuscule après dictée
    'Sous sol': 'Sous-sol',
    'Sous-Sol': 'Sous-sol',
    'Salle de bain': 'Salle de bain',  # placeholder si on veut harmoniser
}


HEADING_STYLES = ('Heading1', 'Heading2', 'Heading3')


def iter_heading_paragraphs(xml: str):
    """Génère (start, end) de chaque <w:p>...</w:p> dont le pStyle est un Heading."""
    for style in HEADING_STYLES:
        pattern = re.compile(
            r'    <w:p>\s*<w:pPr>\s*<w:pStyle w:val="' + style + r'"/>',
            re.MULTILINE,
        )
        for m in pattern.finditer(xml):
            p_start = xml.rfind('    <w:p>', 0, m.start() + len('    <w:p>'))
            if p_start == -1:
                p_start = m.start()
            p_end = xml.find('    </w:p>', m.start())
            if p_end == -1:
                continue
            yield style, p_start, p_end + len('    </w:p>')


def apply_corrections_in_block(block: str) -> tuple[str, list[str]]:
    applied: list[str] = []
    new_block = block
    for wrong, right in CORRECTIONS.items():
        if wrong == right:
            continue
        if wrong in new_block:
            new_block = new_block.replace(wrong, right)
            applied.append(f'{wrong} → {right}')
    return new_block, applied


def main(doc_path: Path) -> None:
    xml = doc_path.read_text(encoding='utf-8')
    before_len = len(xml)

    # Collecte des paragraphes Heading dans l'ordre décroissant de position
    # pour pouvoir faire des remplacements sur les offsets sans les décaler
    blocks = []
    for style, start, end in iter_heading_paragraphs(xml):
        blocks.append((style, start, end))
    # Dédupliquer (un même <w:p> peut être attrapé deux fois via pattern chevauchant)
    blocks = list({(s, b, e): None for s, b, e in blocks}.keys())
    blocks.sort(key=lambda t: t[1])

    total_changes = 0
    # Appliquer du dernier au premier
    for style, start, end in reversed(blocks):
        original_block = xml[start:end]
        new_block, applied = apply_corrections_in_block(original_block)
        if applied:
            xml = xml[:start] + new_block + xml[end:]
            total_changes += len(applied)
            for a in applied:
                print(f'  [{style}] {a}')

    doc_path.write_text(xml, encoding='utf-8')
    print(
        f'\n{total_changes} correction(s) appliquée(s) — '
        f'{before_len} → {len(xml)} octets ({len(xml) - before_len:+d})'
    )


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage : correct_titles.py <document.xml>', file=sys.stderr)
        sys.exit(2)
    main(Path(sys.argv[1]).resolve())
