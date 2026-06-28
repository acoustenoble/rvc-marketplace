#!/usr/bin/env python3
"""Garantit la présence des styles Heading1 / Heading2 dans un .docx dépaqueté.

Le brouillon Juris Drone est « plat » (seul style HOParagraphe, pas de Heading). Or les titres des
sections drone doivent alimenter le Sommaire (champ TOC \\o "1-4") et démarrer en haut de page.
Ce script ajoute, s'ils sont absents, des styles Heading1 (outlineLvl 0) et Heading2 (outlineLvl 1)
au look des constats RVC : Arial, gras, bleu nuit (#1F3A5F), centré, pageBreakBefore sur Heading1.
Idempotent.

Usage:
    python3 add_heading_style.py <unpacked_dir>
"""
import sys, os, re

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

HEADING1 = '''<w:style w:type="paragraph" w:styleId="Heading1">
<w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="HOParagraphe"/>
<w:uiPriority w:val="9"/><w:qFormat/>
<w:pPr><w:keepNext/><w:pageBreakBefore/><w:spacing w:before="240" w:after="240"/>
<w:jc w:val="center"/><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:b/>
<w:color w:val="1F3A5F"/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
</w:style>'''

HEADING2 = '''<w:style w:type="paragraph" w:styleId="Heading2">
<w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="HOParagraphe"/>
<w:uiPriority w:val="9"/><w:qFormat/>
<w:pPr><w:keepNext/><w:spacing w:before="160" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:b/>
<w:color w:val="1F3A5F"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
</w:style>'''


def main():
    unpacked = sys.argv[1]
    path = os.path.join(unpacked, "word", "styles.xml")
    with open(path, encoding="utf-8") as f:
        xml = f.read()

    added = []
    for sid, frag in (("Heading1", HEADING1), ("Heading2", HEADING2)):
        if f'w:styleId="{sid}"' in xml:
            continue
        frag1 = re.sub(r">\s+<", "><", frag).strip()
        xml = xml.replace("</w:styles>", frag1 + "</w:styles>")
        added.append(sid)

    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    print("Styles ajoutés :", ", ".join(added) if added else "(aucun — déjà présents)")


if __name__ == "__main__":
    main()
