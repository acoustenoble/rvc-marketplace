#!/usr/bin/env python3
"""
format_mentions.py — Met en forme le bloc de mentions du panneau d'affichage.

Le brouillon (export constats-huissiers.fr) regroupe toutes les mentions du
panneau dans UN seul paragraphe, une mention par run séparée par <w:br/>, au
format « Label : valeur ». Ce script transforme chaque ligne en :

    [LIBELLÉ EN GRAS MAJUSCULES] : [valeur en normal]

conformément au modèle RVC (PDF de référence). Il ne touche qu'au paragraphe
contenant la première mention (« Bénéficiaire … »).

Usage :
    python3 format_mentions.py <document.xml> [--no-upper] [--anchor "Bénéficiaire"]
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

RX_PARA = re.compile(r"<w:p\b[^>]*>.*?</w:p>", re.DOTALL)
RX_RUN = re.compile(r"<w:r\b(?:>|\s[^>]*>).*?</w:r>", re.DOTALL)
RX_RPR = re.compile(r"<w:rPr\b[^>]*>.*?</w:rPr>", re.DOTALL)
RX_TEXT = re.compile(r"(<w:t\b[^>]*>)([^<]*)(</w:t>)")


def upper_fr(s: str) -> str:
    """Majuscule en conservant les accents (É, È, Ç…)."""
    return s.upper()


def make_run(rpr: str, text: str, bold: bool) -> str:
    """Construit un <w:r> avec rPr donné, en forçant/retirant le gras."""
    if rpr:
        body = rpr
        # retirer un <w:b/> ou <w:b .../> existant
        body = re.sub(r"<w:b\b[^>]*/>", "", body)
        body = re.sub(r"<w:bCs\b[^>]*/>", "", body)
        if bold:
            # insérer <w:b/> juste après <w:rPr ...>
            body = re.sub(r"(<w:rPr\b[^>]*>)", r"\1<w:b/>", body, count=1)
    else:
        body = "<w:rPr><w:b/></w:rPr>" if bold else ""
    # protéger les espaces de début/fin
    space = ' xml:space="preserve"'
    return f"<w:r>{body}<w:t{space}>{text}</w:t></w:r>"


def split_line(rpr: str, line: str, upper: bool) -> str:
    """« Label : valeur » -> run gras (label :) + run normal ( valeur)."""
    # accepte « : » avec ou sans espace ; coupe au premier deux-points
    m = re.match(r"^(.*?)(\s*:\s*)(.*)$", line, re.DOTALL)
    if not m:
        # pas de deux-points : laisser en gras (sous-libellé type "Rue Semallé")
        return make_run(rpr, line, bold=False)
    label, sep, value = m.group(1), m.group(2), m.group(3)
    label_out = upper_fr(label) if upper else label
    out = make_run(rpr, f"{label_out} :", bold=True)
    if value.strip():
        out += make_run(rpr, f" {value}", bold=False)
    return out


def process_paragraph(p: str, upper: bool) -> str:
    runs = RX_RUN.findall(p)
    if not runs:
        return p
    # rPr de référence (premier run)
    first_rpr_m = RX_RPR.search(runs[0])
    ref_rpr = first_rpr_m.group(0) if first_rpr_m else ""

    # Reconstituer les LIGNES : on parcourt les runs, chaque <w:br/> = nouvelle
    # ligne. Le texte de chaque run est concaténé.
    lines: list[str] = [""]
    for r in runs:
        if "<w:br/>" in r or "<w:br " in r or "<w:br>" in r:
            # un run peut contenir un br seul
            t = "".join(t for _, t, _ in RX_TEXT.findall(r))
            if t:
                lines[-1] += t
            lines.append("")
            continue
        t = "".join(t for _, t, _ in RX_TEXT.findall(r))
        lines[-1] += t
    lines = [ln for ln in lines if ln.strip()]

    # Reconstruire le contenu : runs séparés par <w:br/>
    new_runs = []
    for i, ln in enumerate(lines):
        new_runs.append(split_line(ref_rpr, ln, upper))
        if i != len(lines) - 1:
            new_runs.append("<w:r><w:br/></w:r>")

    # pPr conservé
    ppr_m = re.search(r"<w:pPr\b[^>]*>.*?</w:pPr>", p, re.DOTALL)
    ppr = ppr_m.group(0) if ppr_m else ""
    return f"<w:p>{ppr}{''.join(new_runs)}</w:p>"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("document", type=Path)
    ap.add_argument("--anchor", default="Bénéficiaire",
                    help="texte de début du paragraphe à reformater")
    ap.add_argument("--no-upper", action="store_true",
                    help="ne pas mettre les libellés en majuscules")
    args = ap.parse_args()

    xml = args.document.read_text(encoding="utf-8")
    upper = not args.no_upper

    done = False

    def repl(m: re.Match) -> str:
        nonlocal done
        p = m.group(0)
        txt = "".join(t for _, t, _ in RX_TEXT.findall(p))
        if not done and txt.strip().startswith(args.anchor):
            done = True
            return process_paragraph(p, upper)
        return p

    new_xml = RX_PARA.sub(repl, xml)
    if not done:
        print(f"ATTENTION : aucun paragraphe ne commence par « {args.anchor} ». "
              "Rien modifié.", file=sys.stderr)
        return 1
    args.document.write_text(new_xml, encoding="utf-8")
    print("OK — mentions du panneau reformatées (libellés en gras"
          + (" majuscules)." if upper else ")."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
