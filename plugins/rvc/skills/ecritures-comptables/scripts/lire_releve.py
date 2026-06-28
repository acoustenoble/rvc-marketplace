#!/usr/bin/env python3
"""Lit un relevé bancaire Excel (export Crédit Agricole ou similaire) et sort un JSON.

Usage : python3 lire_releve.py <releve.xlsx> [sortie.json]

Détecte automatiquement la ligne d'en-têtes (Date / Libellé / Débit / Crédit),
nettoie les libellés multilignes et imprime les totaux de contrôle.
"""
import json
import re
import sys
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

import openpyxl  # noqa: E402


def to_amount(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return round(float(v), 2)
    s = str(v).replace(" ", "").replace("€", "").replace(" ", "").replace(",", ".")
    s = re.sub(r"[^0-9.\-]", "", s)
    return round(float(s), 2) if s not in ("", "-", ".") else None


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: lire_releve.py <releve.xlsx> [sortie.json]")
    path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "operations.json"

    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))

    header_idx = None
    for i, row in enumerate(rows):
        cells = [str(c).strip().lower() if c else "" for c in row]
        if any("date" in c for c in cells) and any("bit" in c for c in cells):
            header_idx = i
            break
    if header_idx is None:
        sys.exit("ERREUR : ligne d'en-têtes (Date/Débit/Crédit) introuvable.")

    header = [str(c).strip().lower() if c else "" for c in rows[header_idx]]
    col = {}
    for j, h in enumerate(header):
        if "date" in h and "date" not in col:
            col["date"] = j
        elif "libell" in h:
            col["libelle"] = j
        elif "débit" in h or "debit" in h:
            col["debit"] = j
        elif "crédit" in h or "credit" in h:
            col["credit"] = j
    missing = {"date", "libelle", "debit", "credit"} - set(col)
    if missing:
        sys.exit(f"ERREUR : colonnes manquantes : {missing}")

    ops = []
    for row in rows[header_idx + 1:]:
        date, lib = row[col["date"]], row[col["libelle"]]
        deb, cre = to_amount(row[col["debit"]]), to_amount(row[col["credit"]])
        if date is None and lib is None:
            continue
        if deb is None and cre is None:
            continue
        if isinstance(date, datetime):
            date_s = date.strftime("%d/%m/%Y")
        else:
            date_s = str(date).strip()
        lib_clean = re.sub(r"\s+", " ", str(lib or "")).strip()
        ops.append({
            "n": len(ops) + 1,
            "date": date_s,
            "libelle": lib_clean,
            "libelle_brut": str(lib or ""),
            "sortie": deb,   # colonne Débit du relevé = sortie d'argent = crédit 512000
            "entree": cre,   # colonne Crédit du relevé = entrée d'argent = débit 512000
        })

    total_sorties = round(sum(o["sortie"] or 0 for o in ops), 2)
    total_entrees = round(sum(o["entree"] or 0 for o in ops), 2)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "fichier": path,
            "nb_operations": len(ops),
            "total_sorties": total_sorties,
            "total_entrees": total_entrees,
            "operations": ops,
        }, f, ensure_ascii=False, indent=2)

    print(f"{len(ops)} opérations lues.")
    print(f"Total sorties (débits relevé)  : {total_sorties:.2f} €")
    print(f"Total entrées (crédits relevé) : {total_entrees:.2f} €")
    print(f"JSON écrit : {out}")


if __name__ == "__main__":
    main()
