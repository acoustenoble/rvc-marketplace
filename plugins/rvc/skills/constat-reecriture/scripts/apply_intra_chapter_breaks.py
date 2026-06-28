#!/usr/bin/env python3
"""
apply_intra_chapter_breaks.py — Règle « bloc = page ».

Dans chaque chapitre (entre deux titres Heading1/Heading2), détecte les
"blocs de commentaire" (suites de paragraphes de texte descriptif, hors
photos et captions) et ajoute <w:pageBreakBefore/> au premier paragraphe
de chaque bloc SAUF le tout premier bloc du chapitre (qui reste collé
au titre).

Pourquoi : Antoine veut que chaque bloc de texte descriptif s'affiche
en haut d'une page afin que les photographies qui le suivent (et qu'il
décrit) s'enchaînent juste en dessous, sans coupure entre le texte et
ses illustrations.

Idempotent : si <w:pageBreakBefore/> est déjà présent, rien n'est ajouté.

Heuristiques de classification :
- 'heading' : paragraphe dont le <w:pStyle> est Heading1/2/3
- 'photo'   : paragraphe contenant <w:drawing>/<w:pict>, ou dont le
              texte concaténé commence par "Photographie n"
- 'empty'   : paragraphe sans texte réel (ou texte = ".")
- 'content' : tout le reste (paragraphes de constatation rédigés)

Un bloc de commentaire est une suite maximale de paragraphes 'content'.
Les paragraphes 'empty' à l'intérieur d'un bloc ne le brisent pas.

Usage :
    python3 apply_intra_chapter_breaks.py <chemin/vers/document.xml>
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


def iter_paragraphs(xml: str):
    """Yield (start, end, block) for each <w:p>...</w:p>."""
    for m in re.finditer(r'    <w:p>.*?    </w:p>', xml, flags=re.DOTALL):
        yield m.start(), m.end(), m.group(0)


def classify(block: str) -> str:
    ms = re.search(r'<w:pStyle w:val="([^"]+)"/>', block)
    style = ms.group(1) if ms else ''
    if style in ('Heading1', 'Heading2', 'Heading3'):
        return 'heading'
    if '<w:drawing' in block or '<w:pict' in block:
        return 'photo'
    texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', block)
    text = ''.join(texts).strip()
    if not text:
        return 'empty'
    if text.startswith('Photographie n'):
        return 'photo'
    if text == '.':
        return 'empty'
    return 'content'


def has_page_break_before(block: str) -> bool:
    ppr = re.search(r'<w:pPr>(.*?)</w:pPr>', block, flags=re.DOTALL)
    if not ppr:
        return False
    return '<w:pageBreakBefore' in ppr.group(1)


def inject_page_break_before(block: str) -> str:
    if has_page_break_before(block):
        return block
    ppr_m = re.search(r'<w:pPr>(.*?)</w:pPr>', block, flags=re.DOTALL)
    if ppr_m:
        inner = ppr_m.group(1)
        pstyle_m = re.search(r'(<w:pStyle w:val="[^"]+"/>)', inner)
        if pstyle_m:
            new_inner = inner[:pstyle_m.end()] + '<w:pageBreakBefore/>' + inner[pstyle_m.end():]
        else:
            new_inner = '<w:pageBreakBefore/>' + inner
        return block[:ppr_m.start()] + f'<w:pPr>{new_inner}</w:pPr>' + block[ppr_m.end():]
    return block.replace('    <w:p>', '    <w:p>\n      <w:pPr><w:pageBreakBefore/></w:pPr>', 1)


def main(document_xml: Path) -> int:
    xml = document_xml.read_text(encoding='utf-8')
    paras = list(iter_paragraphs(xml))
    kinds = [classify(b) for _, _, b in paras]

    to_break: set[int] = set()
    i = 0
    n = len(paras)
    while i < n:
        if kinds[i] == 'heading':
            chapter_start = i + 1
        else:
            chapter_start = i
        j = chapter_start
        while j < n and kinds[j] != 'heading':
            j += 1
        k = chapter_start
        block_count = 0
        while k < j:
            while k < j and kinds[k] != 'content':
                k += 1
            if k >= j:
                break
            block_first = k
            block_count += 1
            if block_count >= 2:
                to_break.add(block_first)
            while k < j and kinds[k] in ('content', 'empty'):
                k += 1
        i = j

    if not to_break:
        print("aucun saut intra-chapitre à ajouter")
        return 0

    added = 0
    for idx in sorted(to_break, reverse=True):
        start, end, block = paras[idx]
        new_block = inject_page_break_before(block)
        if new_block != block:
            xml = xml[:start] + new_block + xml[end:]
            added += 1

    document_xml.write_text(xml, encoding='utf-8')
    print(f"{added} saut(s) de page ajouté(s) sur bloc(s) de commentaire intra-chapitre")
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: apply_intra_chapter_breaks.py <document.xml>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(Path(sys.argv[1])))
