"""
Extrait les photos d'un constat d'inventaire .docx et les pretraite
(rotation EXIF + redimensionnement) en photo_NN.jpg.

Usage :
    python extract_and_prepare_photos.py \\
        --src   <constat_original.docx> \\
        --out   <dossier_de_sortie>

Produit :
    <out>/photo_01.jpg
    <out>/photo_02.jpg
    ...

Le mapping 'Photographie n N -> image' est etabli en lisant l'ordre des
r:embed dans word/document.xml, en sautant les images qui sont des logos
(PNG en debut/fin du flux d'images).
"""
import sys
import os
import re
import zipfile
import argparse

from PIL import Image, ImageOps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True, help='Constat .docx source')
    ap.add_argument('--out', required=True, help='Dossier de sortie')
    ap.add_argument('--max-size', type=int, default=600,
                    help='Plus grand cote en pixels (defaut: 600)')
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    # 1) Determiner l'ordre des images dans le document
    with zipfile.ZipFile(args.src) as z:
        rels_xml = z.read('word/_rels/document.xml.rels').decode('utf-8')
        rels = {}
        for m in re.finditer(
                r'Id="([^"]+)"\s+Type="[^"]*image[^"]*"\s+Target="([^"]+)"',
                rels_xml):
            rels[m.group(1)] = m.group(2).replace('media/', '')
        doc_xml = z.read('word/document.xml').decode('utf-8')

        order = []
        for m in re.finditer(r'r:embed="([^"]+)"', doc_xml):
            rid = m.group(1)
            if rid in rels:
                order.append(rels[rid])

        # 2) Filtrer les logos : on saute les PNG du debut et le(s) PNG final(aux)
        photo_files = []
        i = 0
        while i < len(order) and order[i].lower().endswith('.png'):
            i += 1
        j = len(order)
        while j > i and order[j-1].lower().endswith('.png'):
            j -= 1
        photo_files = order[i:j]
        print("Images detectees dans l'ordre du document : " + str(len(order)))
        print("Logos en debut/fin ignores : " + str(i + (len(order) - j)))
        print("Photos retenues : " + str(len(photo_files)))

        # 3) Extraire et pretraiter
        for n, fname in enumerate(photo_files, start=1):
            data = z.read('word/media/' + fname)
        # Recharger pour iterer (les zip handles ne sont pas reentrants ici)
        # On refait la boucle proprement :
        for n, fname in enumerate(photo_files, start=1):
            with z.open('word/media/' + fname) as f:
                img = Image.open(f)
                img.load()
            img = ImageOps.exif_transpose(img)
            w, h = img.size
            target = args.max_size
            if w >= h:
                nw = target
                nh = max(1, int(h * target / w))
            else:
                nh = target
                nw = max(1, int(w * target / h))
            img = img.resize((nw, nh), Image.LANCZOS)
            dst = os.path.join(args.out, "photo_" + ("%02d" % n) + ".jpg")
            img.convert('RGB').save(dst, 'JPEG', quality=82, optimize=True)
            print("  photo_" + ("%02d" % n) + ".jpg  <- " + fname)

    print("OK : " + str(len(photo_files)) + " photos pretraitees dans " + args.out)


if __name__ == '__main__':
    main()
