#!/usr/bin/env python3
"""
apply_layout.py — Finalisation de la mise en page d'un état des lieux

Opère sur un .docx déjà construit par build_etat_des_lieux.py et applique :

  1. Saut de page avant chaque Heading1 (pièce) → <w:pageBreakBefore/>
  2. Solidarité avec le paragraphe suivant → <w:keepNext/>
  3. Justification des paragraphes Sol/Murs/Plafond → <w:jc w:val="both"/>
  4. Activation de la mise à jour automatique du sommaire à l'ouverture
  5. Marquage des champs TOC comme "dirty" pour forcer le rafraîchissement

Le script modifie le .docx in-place (ou produit une copie via --out).

Usage :
    python3 apply_layout.py <input.docx>                 # in-place
    python3 apply_layout.py <input.docx> --out <out.docx>  # nouvelle copie
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path


# --------------------------------------------------------------------------
#  Transformations
# --------------------------------------------------------------------------

def patch_styles_xml(styles_xml: str) -> str:
    """
    Renforce le style Heading1 :
        - <w:pageBreakBefore/>
        - <w:keepNext/>
        - <w:keepLines/>
        - <w:outlineLvl w:val="1"/>
    """
    rx = re.compile(
        r'(<w:style[^>]*w:styleId="Heading1"[^>]*>.*?<w:pPr>)(.*?)(</w:pPr>)',
        re.DOTALL,
    )

    def repl(m):
        before, ppr, after = m.group(1), m.group(2), m.group(3)
        # Ne dupliquer aucun élément déjà présent
        additions = []
        if "<w:pageBreakBefore" not in ppr:
            additions.append("<w:pageBreakBefore/>")
        if "<w:keepNext" not in ppr:
            additions.append("<w:keepNext/>")
        if "<w:keepLines" not in ppr:
            additions.append("<w:keepLines/>")
        if "<w:outlineLvl" not in ppr:
            additions.append('<w:outlineLvl w:val="1"/>')
        return before + ppr + "".join(additions) + after

    new_styles = rx.sub(repl, styles_xml, count=1)

    # Ajouter la justification au style HOParagraphe si absente
    rx_ho = re.compile(
        r'(<w:style[^>]*w:styleId="HOParagraphe"[^>]*>.*?<w:pPr>)(.*?)(</w:pPr>)',
        re.DOTALL,
    )

    def repl_ho(m):
        before, ppr, after = m.group(1), m.group(2), m.group(3)
        if "<w:jc " not in ppr:
            ppr = ppr + '<w:jc w:val="both"/>'
        return before + ppr + after

    new_styles = rx_ho.sub(repl_ho, new_styles, count=1)
    return new_styles


def patch_settings_xml(settings_xml: str) -> str:
    """Active la mise à jour automatique des champs (sommaire) à l'ouverture."""
    if "<w:updateFields" in settings_xml:
        return settings_xml
    if "</w:settings>" in settings_xml:
        return settings_xml.replace(
            "</w:settings>",
            '<w:updateFields w:val="true"/></w:settings>',
        )
    return settings_xml


def patch_document_xml(doc_xml: str) -> str:
    """
    1. Pose <w:pageBreakBefore/> et <w:keepNext/> individuellement sur chaque
       paragraphe Heading1, SAUF le premier (la section Convocation, qui doit
       suivre immédiatement "J'AI PROCEDE AUX CONSTATATIONS SUIVANTES :").
    2. Marque le premier <w:fldChar begin> comme dirty=true (pour le sommaire).
    """
    # Trouver tous les paragraphes Heading1
    rx_para = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.DOTALL)
    paragraphs = list(rx_para.finditer(doc_xml))

    headings_indices = []
    for i, m in enumerate(paragraphs):
        if 'w:val="Heading1"' in m.group(1):
            headings_indices.append(i)

    if not headings_indices:
        return doc_xml

    # On garde le premier Heading1 sans saut de page (Convocation suit
    # directement "J'AI PROCEDE AUX CONSTATATIONS SUIVANTES :").
    headings_to_patch = headings_indices[1:]

    # Patcher chaque paragraphe individuellement (ajouter pageBreakBefore +
    # keepNext dans son <w:pPr>).
    # On opère de la fin vers le début pour ne pas invalider les indices.
    new_doc = doc_xml
    for i in reversed(headings_to_patch):
        m = paragraphs[i]
        body = m.group(0)
        # Trouver ou créer <w:pPr>
        if "<w:pPr>" in body:
            new_body = body.replace(
                "<w:pPr>",
                '<w:pPr><w:pageBreakBefore/><w:keepNext/>',
                1,
            )
        else:
            new_body = body.replace(
                "<w:p>",
                '<w:p><w:pPr><w:pageBreakBefore/><w:keepNext/></w:pPr>',
                1,
            )
        # Remplacer dans le doc complet
        new_doc = new_doc[: m.start()] + new_body + new_doc[m.end():]
        # Note : on doit recalculer paragraphs si on continue, mais comme on
        # itère en sens inverse, les indices supérieurs ne sont pas affectés.
        # On ne ré-extrait pas paragraphs ici par simplicité.

    # Marquer le sommaire comme dirty
    new_doc = re.sub(
        r'<w:fldChar w:fldCharType="begin"\s*/>',
        r'<w:fldChar w:fldCharType="begin" w:dirty="true"/>',
        new_doc,
        count=1,
    )

    return new_doc


# --------------------------------------------------------------------------
#  CLI
# --------------------------------------------------------------------------

def apply_layout(src: Path, dst: Path) -> int:
    if src != dst:
        shutil.copy(src, dst)

    # Lire les fichiers à patcher
    with zipfile.ZipFile(dst) as zin:
        styles_xml = zin.read("word/styles.xml").decode("utf-8")
        settings_xml = zin.read("word/settings.xml").decode("utf-8")
        doc_xml = zin.read("word/document.xml").decode("utf-8")
        names = zin.namelist()

    # Patcher
    new_styles = patch_styles_xml(styles_xml)
    new_settings = patch_settings_xml(settings_xml)
    new_doc = patch_document_xml(doc_xml)

    # Réécrire l'archive
    tmp = dst.with_suffix(dst.suffix + ".tmp")
    with zipfile.ZipFile(dst) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.namelist():
            if item == "word/styles.xml":
                zout.writestr(item, new_styles)
            elif item == "word/settings.xml":
                zout.writestr(item, new_settings)
            elif item == "word/document.xml":
                zout.writestr(item, new_doc)
            else:
                zout.writestr(item, zin.read(item))
    shutil.move(str(tmp), str(dst))

    print(f"OK — mise en page appliquée : {dst}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help=".docx à patcher")
    parser.add_argument("--out", type=Path, default=None,
                        help="Si fourni, écrit dans ce chemin au lieu de in-place")
    args = parser.parse_args()

    src = args.input
    dst = args.out or src

    if not src.exists():
        print(f"ERREUR : fichier introuvable : {src}", file=sys.stderr)
        return 1

    try:
        return apply_layout(src, dst)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"ERREUR : {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
