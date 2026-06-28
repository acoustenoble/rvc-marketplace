#!/usr/bin/env python3
"""
fix_demandeurs.py — civilité et accord pour le bloc « A LA DEMANDE DE » (règle 15).

Usage :
    python3 fix_demandeurs.py <document.xml> \
        --demandeur "PRENOM NOM:G:ADRESSE" \
        [--demandeur "PRENOM NOM:G:ADRESSE" ...]

    où G ∈ {M, F}

Effet : remplace pour chaque demandeur un motif pré-existant type
    "PRENOM NOM domicilié(e) ADRESSE."
par
    "Madame PRENOM NOM, domiciliée au ADRESSE."    (si G=F)
    "Monsieur PRENOM NOM, domicilié au ADRESSE."   (si G=M)

Idempotent : si la ligne est déjà au bon format (Madame/Monsieur X, domicilié(e)
au Y), aucune modification.

Remarques :
    - Si le motif exact n'est pas trouvé, le script tente plusieurs variantes
      courantes (avec ou sans « au », avec ou sans virgule) avant d'échouer.
    - En cas de prénom ambigu (Camille, Dominique, Claude, Alex...),
      ne pas appeler ce script — demander d'abord le genre à l'utilisateur.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def civilite_pour(genre: str) -> tuple[str, str]:
    g = genre.strip().upper()
    if g == 'F':
        return 'Madame', 'domiciliée'
    if g == 'M':
        return 'Monsieur', 'domicilié'
    raise ValueError(f"Genre inconnu : '{genre}' (attendu 'M' ou 'F')")


def fix_one(xml: str, ident: str, adresse: str, civ: str, dom: str) -> tuple[str, str]:
    """Retourne (nouveau_xml, message).

    Stratégie :
    1. Si le format cible est déjà présent, on ne touche pas.
    2. Sinon, on tente plusieurs patterns source et on remplace le premier trouvé.
    """
    cible = f'{civ} {ident}, {dom} au {adresse}.'

    if cible in xml:
        return xml, f'  [{ident}] déjà au bon format — skip'

    # Patterns source essayés dans l'ordre
    candidats = [
        f'{ident} domicilié(e) {adresse}.',
        f'{ident} domiciliée {adresse}.',
        f'{ident} domicilié {adresse}.',
        f'{ident} domicilié(e) au {adresse}.',
        f'{ident} domiciliée au {adresse}.',
        f'{ident} domicilié au {adresse}.',
        f'{ident}, domicilié(e) {adresse}.',
        f'{ident}, domicilié(e) au {adresse}.',
    ]
    for src in candidats:
        if src in xml:
            new_xml = xml.replace(src, cible, 1)
            return new_xml, f'  [{ident}] remplacé : "{src}" → "{cible}"'

    # Dernier recours : tentative regex souple (adresse pattern-matchée librement)
    pat = re.compile(
        re.escape(ident) + r',?\s+domicili[ée]\(?e?\)?\s+(?:au\s+)?' + re.escape(adresse) + r'\s*\.',
    )
    m = pat.search(xml)
    if m:
        new_xml = xml[: m.start()] + cible + xml[m.end() :]
        return new_xml, f'  [{ident}] remplacé (regex souple) : "{m.group(0)}" → "{cible}"'

    return xml, f'  [{ident}] AUCUN PATTERN TROUVÉ — vérifier manuellement'


def main() -> None:
    ap = argparse.ArgumentParser(description='Civilité + accord dans A LA DEMANDE DE.')
    ap.add_argument('document_xml', help='Chemin vers word/document.xml')
    ap.add_argument(
        '--demandeur',
        action='append',
        required=True,
        help='"PRENOM NOM:G:ADRESSE" — G=M ou F',
    )
    args = ap.parse_args()

    doc_path = Path(args.document_xml).resolve()
    if not doc_path.exists():
        raise FileNotFoundError(doc_path)

    xml = doc_path.read_text(encoding='utf-8')
    before_len = len(xml)

    for raw in args.demandeur:
        parts = raw.split(':', 2)
        if len(parts) != 3:
            raise ValueError(
                f"Format attendu 'PRENOM NOM:G:ADRESSE', reçu : {raw!r}"
            )
        ident, genre, adresse = parts
        ident = ident.strip()
        adresse = adresse.strip()
        civ, dom = civilite_pour(genre)
        xml, msg = fix_one(xml, ident, adresse, civ, dom)
        print(msg)

    doc_path.write_text(xml, encoding='utf-8')
    print(f'\ndocument.xml : {before_len} → {len(xml)} octets ({len(xml) - before_len:+d})')


if __name__ == '__main__':
    main()
