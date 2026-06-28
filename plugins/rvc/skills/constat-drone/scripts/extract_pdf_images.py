#!/usr/bin/env python3
"""Extrait les images-cartes d'un PDF d'expédition Juris Drone pour les annexes du constat.

Filtre les vignettes/logos via --min-size (plus petite dimension en px). Écrit annexe_1.png …
annexe_N.png dans le dossier de sortie + un manifest.json (page source, dimensions) pour aider à
rédiger les légendes.

Usage:
    python3 extract_pdf_images.py <input.pdf> <out_dir> [--min-size 400]

Dépendances: PyMuPDF (fitz).  pip install pymupdf --break-system-packages
"""
import sys, os, json, argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("out_dir")
    ap.add_argument("--min-size", type=int, default=400,
                    help="Plus petite dimension (px) en deçà de laquelle l'image est ignorée (logos/vignettes).")
    args = ap.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit("PyMuPDF requis : pip install pymupdf --break-system-packages")

    os.makedirs(args.out_dir, exist_ok=True)
    doc = fitz.open(args.pdf)
    manifest, idx, seen = [], 0, set()

    for pno in range(len(doc)):
        for img in doc[pno].get_images(full=True):
            xref = img[0]
            if xref in seen:
                continue
            seen.add(xref)
            try:
                pix = fitz.Pixmap(doc, xref)
            except Exception:
                continue
            if min(pix.width, pix.height) < args.min_size:
                continue  # logo / vignette
            if pix.n >= 5:  # CMYK / alpha → RGB
                pix = fitz.Pixmap(fitz.csRGB, pix)
            idx += 1
            name = f"annexe_{idx}.png"
            pix.save(os.path.join(args.out_dir, name))
            manifest.append({"file": name, "page": pno + 1,
                             "width": pix.width, "height": pix.height})
            print(f"{name}  (page {pno+1}, {pix.width}x{pix.height})")

    with open(os.path.join(args.out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\n{idx} image(s) extraite(s) → {args.out_dir}")


if __name__ == "__main__":
    main()
