#!/usr/bin/env python3
"""apply_layout.py — Mise en page RVC d'un constat d'affichage.

- styles.xml : keepNext sur Heading1 (le titre de passage reste avec sa date/photo).
- document.xml :
    * dé-justifie les blocs à retours-ligne (dates, mentions) ;
    * justifie la prose longue ;
    * SAUTS DE PAGE explicites avant les ancres :
        - "CERTIFIE M'ÊTRE RENDU ..."        (visite + adresse + GPS + carte sur leur page)
        - "J'AI PROCEDE AUX CONSTATATIONS"   (constatations en tête de page)
        - "Photographies effectuées ..."     (intro photos en tête de page)
      et avant chaque passage SAUF le 1er (le 1er passage reste collé à l'intro photos).
- settings.xml : updateFields (sommaire).
"""
from __future__ import annotations
import re, sys
from pathlib import Path

_RX_SEG_TEXT = re.compile(r"<w:t\b[^>]*>([^<]*)</w:t>")

PAGEBREAK_ANCHORS = (
    "CERTIFIE M'ÊTRE RENDU",
    "J'AI PROCEDE AUX CONSTATATIONS",
    "Photographies effectuées",
)

def patch_styles(path: Path) -> None:
    xml = path.read_text(encoding="utf-8")
    m = re.search(r'(<w:style [^>]*w:styleId="Heading1".*?</w:style>)', xml, re.DOTALL)
    if not m:
        print("  styles.xml : Heading1 introuvable, ignoré."); return
    style = m.group(1); new = style
    # retirer un pageBreakBefore éventuel au niveau du STYLE (on gère page par page)
    new = new.replace("<w:pageBreakBefore/>", "")
    if "<w:pPr>" in new:
        if "w:keepNext" not in new:
            new = new.replace("<w:pPr>", "<w:pPr><w:keepNext/>", 1)
    else:
        new = new.replace("<w:name", "<w:pPr><w:keepNext/></w:pPr><w:name", 1)
    xml = xml.replace(style, new, 1)
    path.write_text(xml, encoding="utf-8")
    print("  styles.xml : Heading1 -> keepNext (pas de saut auto)")

def _text_line_count(p: str) -> int:
    segs = re.split(r"<w:br\s*/>", p)
    return sum(1 for s in segs if "".join(_RX_SEG_TEXT.findall(s)).strip())

def _add_pagebreak(p: str) -> str:
    if "<w:pageBreakBefore/>" in p:
        return p
    m = re.search(r"<w:pPr\b[^>]*>", p)
    if m:
        return p[:m.end()] + "<w:pageBreakBefore/>" + p[m.end():]
    return re.sub(r"(<w:p\b[^>]*>)", r"\1<w:pPr><w:pageBreakBefore/></w:pPr>", p, count=1)

def strip_manual_page_breaks(xml: str) -> tuple[str, int]:
    """Retire les sauts de page MANUELS (<w:br w:type="page"/>) insérés par l'app,
    SAUF le premier (séparateur Sommaire -> titre). On repose ensuite nos propres
    sauts par ancre."""
    positions = [m.start() for m in re.finditer(r'<w:br w:type="page"/>', xml)]
    if len(positions) <= 1:
        return xml, 0
    # garder le premier, retirer les suivants
    keep = positions[0]
    out = []
    last = 0
    removed = 0
    for m in re.finditer(r'<w:br w:type="page"/>', xml):
        if m.start() == keep:
            continue
        out.append(xml[last:m.start()])
        last = m.end()
        removed += 1
    out.append(xml[last:])
    return "".join(out), removed


def patch_document(path: Path) -> None:
    xml = path.read_text(encoding="utf-8")
    xml, n_strip = strip_manual_page_breaks(xml)
    n_left = n_just = n_break = 0
    paras = re.findall(r"<w:p\b[^>]*>.*?</w:p>", xml, re.DOTALL)
    passage_seen = 0
    for p in paras:
        txt = "".join(_RX_SEG_TEXT.findall(p))
        stripped = txt.strip()
        newp = p

        # 1) justification
        if "Commissaire de Justice" not in txt:
            if _text_line_count(newp) >= 2:
                if '<w:jc w:val="both"/>' in newp:
                    newp = newp.replace('<w:jc w:val="both"/>', '<w:jc w:val="left"/>'); n_left += 1
            elif 'w:pStyle w:val="HOParagraphe"' in newp and "<w:jc " not in newp and len(txt) >= 120:
                cand = re.sub(r'(<w:pStyle w:val="HOParagraphe"/>)', r'\1<w:jc w:val="both"/>', newp, count=1)
                if cand != newp:
                    newp = cand; n_just += 1

        # 2) sauts de page
        is_heading = 'w:val="Heading1"' in newp
        do_break = any(stripped.startswith(a) for a in PAGEBREAK_ANCHORS)
        if is_heading and re.search(r"passage", stripped, re.I):
            passage_seen += 1
            do_break = passage_seen >= 2  # 1er passage : pas de saut
        if do_break:
            cand = _add_pagebreak(newp)
            if cand != newp:
                newp = cand; n_break += 1

        if newp != p:
            xml = xml.replace(p, newp, 1)
    path.write_text(xml, encoding="utf-8")
    print(f"  document.xml : {n_strip} saut(s) manuel(s) retiré(s), {n_left} dé-justifié(s), {n_just} prose justifié(s), {n_break} saut(s) de page posé(s)")

def patch_settings(path: Path) -> None:
    if not path.exists():
        print("  settings.xml : absent, ignoré."); return
    xml = path.read_text(encoding="utf-8")
    if "w:updateFields" in xml:
        print("  settings.xml : updateFields déjà présent"); return
    xml = re.sub(r"(<w:settings\b[^>]*>)", r'\1<w:updateFields w:val="true"/>', xml, count=1)
    path.write_text(xml, encoding="utf-8")
    print("  settings.xml : updateFields ajouté")

def main() -> int:
    root = Path(sys.argv[1]); word = root / "word"
    print("Mise en page RVC :")
    patch_styles(word / "styles.xml")
    patch_document(word / "document.xml")
    patch_settings(word / "settings.xml")
    print("Terminé."); return 0

if __name__ == "__main__":
    sys.exit(main())
