"""
Mise en forme d'un constat d'inventaire.

Reprend le constat original, conserve TOUTE la structure (en-tete, sommaire,
requete, formules, signature) et remplace UNIQUEMENT la partie 'constatations'
par un tableau a 4 colonnes par piece :
  N item | Photo n | Description (amelioree) | Photographie

Chaque piece :
  - titre style 'Titre11' (du document original) avec saut de page avant
  - numerotation auto via numId=3
  - niveau hierarchique 1 + signet pour le sommaire (TOC)

Le sommaire est marque pour mise a jour automatique a l'ouverture
(updateFields=true et fldChar dirty=true).

Usage :
    python build_constat_inventaire.py \\
        --src   <constat_original.docx> \\
        --photos-dir <dossier_photos_pretraitees> \\
        --data  <fichier_python_avec_ITEMS_et_ROOMS> \\
        --out   <sortie.docx>

Le fichier --data doit definir deux variables : ROOMS (liste de noms de pieces)
et ITEMS (liste de tuples (room, item_no, [photo_nos], description, etat)).
Les fichiers du dossier --photos-dir doivent etre nommes 'photo_NN.jpg'
(ex. photo_01.jpg, photo_02.jpg, ...).
"""
import sys
import os
import argparse
import importlib.util
from collections import defaultdict

from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.table import WD_ALIGN_VERTICAL, WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

# ---------- Helpers ----------
def set_cell_bg(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tc_pr.append(shd)


def set_cell_borders(cell, color='B0B0B0', size='4'):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        b = OxmlElement('w:' + edge)
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), size)
        b.set(qn('w:color'), color)
        tc_borders.append(b)
    tc_pr.append(tc_borders)


def set_repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader')
    th.set(qn('w:val'), 'true')
    tr_pr.append(th)


def load_data(data_path):
    """Charge un fichier Python qui definit ITEMS et ROOMS."""
    spec = importlib.util.spec_from_file_location("inventaire_data", data_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ITEMS, mod.ROOMS


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--src', required=True, help='Constat original (.docx)')
    ap.add_argument('--photos-dir', required=True,
                    help='Dossier contenant les photos pretraitees (photo_NN.jpg)')
    ap.add_argument('--data', required=True,
                    help='Fichier Python definissant ITEMS et ROOMS')
    ap.add_argument('--out', required=True, help='Document de sortie (.docx)')
    args = ap.parse_args()

    items, rooms = load_data(args.data)
    print("Items charges : " + str(len(items)) + " ; pieces : " + str(len(rooms)))

    doc = Document(args.src)
    body = doc.element.body

    bookmark_counter = [1000]

    def insert_heading_before(target_elem, text, style_id='Titre11'):
        """Insere un titre de piece avec :
        - style 'Titre11' du document original
        - numerotation auto (numId=3, ilvl=0)
        - niveau hierarchique 1 (sommaire detecte au rafraichissement)
        - signet pour la cible du TOC
        - saut de page avant + lignes/paragraphes solidaires
        - formatage gras + souligne
        """
        bm_id = bookmark_counter[0]
        bookmark_counter[0] += 1
        bm_name = '_Toc_' + text.replace(' ', '_')

        p = OxmlElement('w:p')
        pPr = OxmlElement('w:pPr')
        pStyle = OxmlElement('w:pStyle')
        pStyle.set(qn('w:val'), style_id)
        pPr.append(pStyle)
        # Saut de page avant
        pPr.append(OxmlElement('w:pageBreakBefore'))
        pPr.append(OxmlElement('w:keepNext'))
        pPr.append(OxmlElement('w:keepLines'))
        # Numerotation auto
        numPr = OxmlElement('w:numPr')
        ilvl = OxmlElement('w:ilvl'); ilvl.set(qn('w:val'), '0'); numPr.append(ilvl)
        numId = OxmlElement('w:numId'); numId.set(qn('w:val'), '3'); numPr.append(numId)
        pPr.append(numPr)
        # Niveau hierarchique explicite
        olvl = OxmlElement('w:outlineLvl')
        olvl.set(qn('w:val'), '1')
        pPr.append(olvl)
        p.append(pPr)

        bm_start = OxmlElement('w:bookmarkStart')
        bm_start.set(qn('w:id'), str(bm_id))
        bm_start.set(qn('w:name'), bm_name)
        p.append(bm_start)

        r = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')
        rPr.append(OxmlElement('w:b'))
        u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rPr.append(u)
        r.append(rPr)
        t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve')
        r.append(t)
        p.append(r)

        bm_end = OxmlElement('w:bookmarkEnd')
        bm_end.set(qn('w:id'), str(bm_id))
        p.append(bm_end)

        target_elem.addprevious(p)
        return p

    # 1) Reperer la zone a remplacer
    paragraphs = list(doc.paragraphs)
    start_idx = None
    end_idx = None
    for i, p in enumerate(paragraphs):
        txt = p.text.strip()
        if start_idx is None and "J'AI PROCEDE AUX CONSTATATIONS SUIVANTES" in txt.upper():
            start_idx = i
        if start_idx is not None and txt.lower().startswith("telles sont les constatations"):
            end_idx = i
            break

    if start_idx is None or end_idx is None:
        sys.exit("Bornes du PV introuvables. Le document n'est probablement pas "
                 "un constat d'inventaire au format attendu.")
    print("Borne debut #" + str(start_idx) + " ; Borne fin #" + str(end_idx))

    start_p = paragraphs[start_idx]._p
    end_p = paragraphs[end_idx]._p

    to_remove = []
    node = start_p.getnext()
    while node is not None and node is not end_p:
        to_remove.append(node)
        node = node.getnext()
    for n in to_remove:
        n.getparent().remove(n)
    print("Elements supprimes entre les bornes : " + str(len(to_remove)))

    # 2) Inserer les sections par piece
    items_by_room = defaultdict(list)
    for it in items:
        items_by_room[it[0]].append(it)

    COL_WIDTHS_CM = [1.0, 1.4, 8.2, 6.4]  # N, Photo n, Description, Photo

    def insert_table_before(target_elem, items_):
        table = doc.add_table(rows=1, cols=4)
        table.autofit = False
        table.allow_autofit = False
        hdr = table.rows[0]
        headers = ["N", "Photo n", "Description du bien", "Photographie"]
        for i, c in enumerate(hdr.cells):
            c.text = ''
            para = c.paragraphs[0]
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            rr = para.add_run(headers[i])
            rr.bold = True
            rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            rr.font.size = Pt(10.5)
            set_cell_bg(c, '1F3A5F')
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_borders(c, color='1F3A5F', size='8')
            c.width = Cm(COL_WIDTHS_CM[i])
        set_repeat_header(hdr)

        for idx, item in enumerate(items_):
            room, item_no, photos, descr, etat = item
            row = table.add_row()
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
            for i, c in enumerate(row.cells):
                c.width = Cm(COL_WIDTHS_CM[i])
                set_cell_borders(c, color='B0B0B0', size='4')
                c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                if idx % 2 == 1:
                    set_cell_bg(c, 'F5F7FA')
            # Col 0 : N item
            c0 = row.cells[0]; c0.text = ''
            p = c0.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            rrr = p.add_run(str(item_no)); rrr.bold = True; rrr.font.size = Pt(11)
            # Col 1 : numero(s) de photo
            c1 = row.cells[1]; c1.text = ''
            p = c1.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            txt = "\n".join(str(n) for n in photos) if photos else "-"
            rrr = p.add_run(txt); rrr.font.size = Pt(9.5); rrr.italic = True
            # Col 2 : description
            c2 = row.cells[2]; c2.text = ''
            p = c2.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            rrr = p.add_run(descr); rrr.font.size = Pt(10)
            # Col 3 : photographie(s)
            c3 = row.cells[3]; c3.text = ''
            p = c3.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if photos:
                n_photos = len(photos)
                for i, photo_n in enumerate(photos):
                    fp = os.path.join(args.photos_dir,
                                       "photo_" + ("%02d" % photo_n) + ".jpg")
                    if os.path.exists(fp):
                        if i > 0:
                            p = c3.add_paragraph()
                            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        run = p.add_run()
                        if n_photos == 1:
                            run.add_picture(fp, width=Cm(5.7))
                        else:
                            run.add_picture(fp, width=Cm(5.5))
                    else:
                        rrr = p.add_run("[photo n " + str(photo_n) + " manquante]")
                        rrr.italic = True
            else:
                rrr = p.add_run("(aucune photographie)")
                rrr.italic = True
                rrr.font.size = Pt(9.5)

        tbl_elem = table._tbl
        tbl_elem.getparent().remove(tbl_elem)
        target_elem.addprevious(tbl_elem)
        target_elem.addprevious(OxmlElement('w:p'))

    for room in rooms:
        if room in items_by_room:
            insert_heading_before(end_p, room, style_id='Titre11')
            insert_table_before(end_p, items_by_room[room])

    # 3) Forcer la mise a jour du sommaire a l'ouverture
    fld_dirty = 0
    for fld in body.iter('{' + W_NS + '}fldChar'):
        if fld.get('{' + W_NS + '}fldCharType') == 'begin':
            fld.set('{' + W_NS + '}dirty', 'true')
            fld_dirty += 1
    print("Champs (TOC, etc.) marques dirty : " + str(fld_dirty))

    settings = doc.settings.element
    upd = settings.find(qn('w:updateFields'))
    if upd is None:
        upd = OxmlElement('w:updateFields')
        upd.set(qn('w:val'), 'true')
        settings.append(upd)
    else:
        upd.set(qn('w:val'), 'true')
    print("settings.xml : updateFields = true")

    doc.save(args.out)
    size_mb = os.path.getsize(args.out) / 1024 / 1024
    print("OK : " + args.out)
    print("Taille : " + ("%.2f" % size_mb) + " Mo")


if __name__ == '__main__':
    main()
