#!/usr/bin/env python3
"""
extract_brouillon.py — Extraction structurée d'un brouillon d'état des lieux

Lit un .docx brouillon (dicté à la voix par Antoine via l'app
constats-huissiers.fr) et produit un JSON contenant :

- L'en-tête juridique (bailleur, adresse, présence sur place)
- La liste des pièces avec leur prose brute et leurs photos
- Les sections terminales : Compteurs, Boîte aux lettres, Clés

Le JSON produit est destiné à être ENRICHI par le LLM qui exécute le skill :
- Lecture des photos pour préciser les descriptions
- Restructuration de la prose en rubriques Sol/Murs/Plafond/Équipement
- Nettoyage des scories de dictée vocale

Le LLM fournit ensuite ce JSON enrichi à `build_etat_des_lieux.py` pour la
construction du .docx final.

Usage :
    python3 extract_brouillon.py <input.docx> --out <output.json>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


# --------------------------------------------------------------------------
#  Constantes et patterns
# --------------------------------------------------------------------------

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

# Patterns de détection des sections du brouillon
RX_PARAGRAPH = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.DOTALL)
RX_PSTYLE = re.compile(r'<w:pStyle\s+w:val="([^"]+)"')
RX_TEXT = re.compile(r"<w:t[^>]*>([^<]*)</w:t>")
RX_EMBED = re.compile(r'r:embed="([^"]+)"')
RX_REL = re.compile(
    r'Id="([^"]+)"\s+Type="[^"]*image[^"]*"\s+Target="([^"]+)"'
)

# Pattern de la légende d'une photo : "Photographie n° X - DD/MM/YYYY HH:MM:SS - LAT LON."
RX_PHOTO_LEGEND = re.compile(
    r"^Photographie\s+n[°º]\s*(\d+)\s*-\s*"          # numéro
    r"(\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{1,2}:\d{1,2})"  # horodatage
    r"\s*-\s*([\d.\-\s]+?)\.?\s*$"                    # GPS
)

# Marqueurs structurels du brouillon
MARK_DEMANDE = "A LA DEMANDE DE :"
MARK_EXPOSE = "LEQUEL M'EXPOSE CE QUI SUIT :"
MARK_DEFERANT = "DEFERANT A CETTE REQUISITION :"
MARK_RENDU = "ME SUIS RENDU CE JOUR :"
MARK_CONSTAT = "J'AI PROCEDE AUX CONSTATATIONS SUIVANTES :"
MARK_CONCLUSION = "Telles sont les constatations faites"

# Section finales connues (canoniques après normalisation)
TERMINAL_SECTIONS = {
    "compteurs",
    "boite aux lettres",
    "boîte aux lettres",
    "votre lettre",          # scorie de dictée vocale fréquente
    "cles",
    "clés",
}


# --------------------------------------------------------------------------
#  Structures de sortie
# --------------------------------------------------------------------------

@dataclass
class Photo:
    numero: int
    image_file: str       # ex. "image3.jpg"
    rId: str              # ex. "rId11"
    legende_brute: str
    horodatage: Optional[str] = None
    gps: Optional[str] = None


@dataclass
class Piece:
    titre_brut: str
    titre_normalise: str          # mis en forme par le script (casse, accents)
    phrase_acces: Optional[str] = None
    prose_brute: str = ""
    scories_detectees: list[str] = field(default_factory=list)
    photos: list[Photo] = field(default_factory=list)
    # Champs à remplir par le LLM lors de l'enrichissement :
    sol: Optional[str] = None
    murs: Optional[str] = None
    plafond: Optional[str] = None
    equipement: list[str] = field(default_factory=list)
    mobilier: list[str] = field(default_factory=list)


@dataclass
class Brouillon:
    bailleur_raw: str
    expose_raw: str                          # paragraphe entre EXPOSE et DEFERANT
    deferant_raw: str
    rendu_raw: str                           # bloc "ME SUIS RENDU CE JOUR"
    presence_raw: Optional[str] = None
    adresse_logement: Optional[str] = None
    type_edl: Optional[str] = None           # "entree" / "sortie" / None si indéterminé
    pieces: list[Piece] = field(default_factory=list)
    compteurs_brut: list[str] = field(default_factory=list)
    boite_aux_lettres_brut: str = ""
    cles_brut: str = ""
    photos_count: int = 0


# --------------------------------------------------------------------------
#  Helpers de parsing
# --------------------------------------------------------------------------

def read_docx_xml(path: Path) -> tuple[str, dict[str, str]]:
    """Retourne (document.xml content, rels {rId: image_file})."""
    with zipfile.ZipFile(path) as z:
        doc_xml = z.read("word/document.xml").decode("utf-8")
        rels_xml = z.read("word/_rels/document.xml.rels").decode("utf-8")
    rels = {
        m.group(1): m.group(2).replace("media/", "")
        for m in RX_REL.finditer(rels_xml)
    }
    return doc_xml, rels


def parse_paragraphs(doc_xml: str) -> list[dict]:
    """
    Tokenise document.xml en une liste de paragraphes :
        [{'style': str|None, 'text': str, 'embeds': [rId, ...]}]
    """
    out = []
    for m in RX_PARAGRAPH.finditer(doc_xml):
        body = m.group(1)
        style_m = RX_PSTYLE.search(body)
        style = style_m.group(1) if style_m else None
        text = "".join(RX_TEXT.findall(body))
        embeds = RX_EMBED.findall(body)
        out.append({"style": style, "text": text.strip(), "embeds": embeds})
    return out


def normalize_titre(raw: str) -> str:
    """
    Corrige les fautes de casse et de typographie courantes sur les titres
    de pièces. Liste extensible.
    """
    fixes = {
        # casse
        "wc": "WC",
        "salle de douche": "Salle de douche",
        "salle de bain": "Salle de bain",
        "salle de bains": "Salle de bain",
        "entree / couloir": "Entrée / Couloir",
        "entrée/couloir": "Entrée / Couloir",
        "entree/couloir": "Entrée / Couloir",
        # accents
        "sechoir": "Séchoir",
        "boite aux lettres": "Boîte aux lettres",
        "boîte aux lettres": "Boîte aux lettres",
        "cles": "Clés",
        "clés": "Clés",
        "cave": "Cave",
        "compteurs": "Compteurs",
        # scories de dictée
        "votre lettre": "Boîte aux lettres",
        # coquilles
        "cuisne": "Cuisine",
        "cusine": "Cuisine",
    }
    key = raw.strip().lower()
    if key in fixes:
        return fixes[key]
    # Default : capitaliser proprement
    return raw.strip()


def detect_type_edl(paragraphs: list[dict]) -> Optional[str]:
    """
    Tente de détecter automatiquement si l'EDL est d'entrée ou de sortie
    sur la base d'indices textuels. Renvoie None si indéterminé.
    """
    full_text = " ".join(p["text"] for p in paragraphs).lower()
    if "état des lieux de sortie" in full_text or "etat des lieux de sortie" in full_text:
        return "sortie"
    if "état des lieux d'entrée" in full_text or "etat des lieux d'entree" in full_text:
        # Référence à l'EDL d'entrée passé → c'est probablement une SORTIE
        # (un EDL d'entrée ne ferait pas référence à lui-même)
        if "lors de l'état des lieux d'entrée" in full_text or "lors de l'edl d'entrée" in full_text:
            return "sortie"
        return "entree"
    return None


def parse_photo_legend(text: str) -> Optional[tuple[int, str, str]]:
    """Renvoie (numero, horodatage, gps) ou None."""
    m = RX_PHOTO_LEGEND.match(text.strip())
    if not m:
        return None
    return int(m.group(1)), m.group(2), m.group(3).strip()


def is_terminal_section(titre: str) -> bool:
    return titre.strip().lower() in TERMINAL_SECTIONS


def is_compteurs(titre: str) -> bool:
    return titre.strip().lower() == "compteurs"


def is_boite(titre: str) -> bool:
    return titre.strip().lower() in {"boite aux lettres", "boîte aux lettres", "votre lettre"}


def is_cles(titre: str) -> bool:
    return titre.strip().lower() in {"cles", "clés"}


# --------------------------------------------------------------------------
#  Extraction principale
# --------------------------------------------------------------------------

def extract(docx_path: Path) -> Brouillon:
    doc_xml, rels = read_docx_xml(docx_path)
    paragraphs = parse_paragraphs(doc_xml)

    # --- 1. Localiser les marqueurs structurels ---
    idx = {
        "demande": -1,
        "expose": -1,
        "deferant": -1,
        "rendu": -1,
        "constat": -1,
        "conclusion": -1,
    }
    for i, p in enumerate(paragraphs):
        t = p["text"]
        if t.startswith(MARK_DEMANDE):
            idx["demande"] = i
        elif t.startswith(MARK_EXPOSE):
            idx["expose"] = i
        elif t.startswith(MARK_DEFERANT):
            idx["deferant"] = i
        elif t.startswith(MARK_RENDU):
            idx["rendu"] = i
        elif t.startswith(MARK_CONSTAT):
            idx["constat"] = i
        elif t.startswith(MARK_CONCLUSION):
            idx["conclusion"] = i

    if idx["constat"] == -1:
        raise ValueError(
            "Marqueur 'J'AI PROCEDE AUX CONSTATATIONS SUIVANTES :' introuvable. "
            "Le document n'est probablement pas un EDL au format attendu."
        )

    # --- 2. Extraire les blocs d'en-tête ---
    bailleur_raw = ""
    if idx["demande"] != -1 and idx["expose"] != -1:
        bailleur_raw = " ".join(
            p["text"] for p in paragraphs[idx["demande"] + 1 : idx["expose"]]
            if p["text"]
        )

    expose_raw = ""
    if idx["expose"] != -1 and idx["deferant"] != -1:
        expose_raw = " ".join(
            p["text"] for p in paragraphs[idx["expose"] + 1 : idx["deferant"]]
            if p["text"]
        )

    deferant_raw = ""
    if idx["deferant"] != -1 and idx["rendu"] != -1:
        deferant_raw = " ".join(
            p["text"] for p in paragraphs[idx["deferant"] + 1 : idx["rendu"]]
            if p["text"]
        )

    rendu_raw = ""
    presence_raw = None
    adresse_logement = None
    if idx["rendu"] != -1 and idx["constat"] != -1:
        rendu_paragraphs = [
            p["text"] for p in paragraphs[idx["rendu"] + 1 : idx["constat"]]
            if p["text"]
        ]
        rendu_raw = " ".join(rendu_paragraphs)
        # L'adresse est en général la première phrase, suivie de "où là étant"
        # puis "en présence de ..."
        if rendu_raw:
            # Tentative de scission adresse / présence
            m = re.search(r"(.+?)(?:,?\s*où là étant)", rendu_raw)
            if m:
                adresse_logement = m.group(1).strip(", ")
            m_pres = re.search(r"en présence de\s+(.+?)$", rendu_raw)
            if m_pres:
                presence_raw = m_pres.group(1).strip(",. ")

    # --- 3. Détection du type d'EDL (indicatif, sera confirmé par Antoine) ---
    type_edl = detect_type_edl(paragraphs[idx["constat"] :])

    # --- 4. Itérer sur les pièces, en s'arrêtant à la conclusion ---
    end_idx = idx["conclusion"] if idx["conclusion"] != -1 else len(paragraphs)
    body = paragraphs[idx["constat"] + 1 : end_idx]

    pieces: list[Piece] = []
    compteurs_brut: list[str] = []
    boite_brut = ""
    cles_brut = ""

    current: Optional[Piece] = None
    current_terminal: Optional[str] = None  # "compteurs" / "boite" / "cles" / None

    for p in body:
        style = p["style"]
        text = p["text"]
        embeds = p["embeds"]

        # --- détection d'un nouveau titre Heading1 ---
        if style == "Heading1":
            # finaliser la pièce précédente
            current = None
            current_terminal = None

            if not text:
                # Heading1 vide (scorie observée : "Cuisine" en doublon avec un titre vide)
                continue

            # Identifier les sections terminales
            if is_compteurs(text):
                current_terminal = "compteurs"
                continue
            if is_boite(text):
                current_terminal = "boite"
                continue
            if is_cles(text):
                current_terminal = "cles"
                continue

            # Pièce normale
            current = Piece(
                titre_brut=text,
                titre_normalise=normalize_titre(text),
            )
            pieces.append(current)
            continue

        # --- contenu sous le titre courant ---
        if not text and not embeds:
            continue

        # Photo ?
        photo_legend = parse_photo_legend(text) if text else None

        if current is not None:
            # Photo
            if photo_legend:
                numero, horodatage, gps = photo_legend
                # Tenter de récupérer le rId du paragraphe précédent (la photo
                # elle-même est dans le paragraphe avant la légende, ou dans
                # le même paragraphe selon le format).
                rId = embeds[0] if embeds else ""
                image_file = rels.get(rId, "")
                current.photos.append(
                    Photo(
                        numero=numero,
                        image_file=image_file,
                        rId=rId,
                        legende_brute=text,
                        horodatage=horodatage,
                        gps=gps,
                    )
                )
                continue

            # Texte de prose
            if text:
                if current.prose_brute:
                    current.prose_brute += "\n"
                current.prose_brute += text
            # On ignore les embeds non-légendés ici : ce sont les paragraphes
            # qui ne contiennent QUE la photo, leur légende suit dans le
            # paragraphe d'après et c'est elle qui crée l'objet Photo.
            # Cette stratégie peut perdre le rId de la photo. Pour le
            # rattraper, on inspecte le paragraphe précédent dans une seconde
            # passe en post-traitement (cf. ci-dessous).

        elif current_terminal == "compteurs":
            if photo_legend:
                continue  # photos des compteurs ignorées dans le brut texte
            if text:
                compteurs_brut.append(text)
        elif current_terminal == "boite":
            if photo_legend:
                continue
            if text:
                boite_brut += (" " if boite_brut else "") + text
        elif current_terminal == "cles":
            if photo_legend:
                continue
            if text:
                cles_brut += (" " if cles_brut else "") + text

    # --- 5. Post-traitement : rattacher les rIds des photos ---
    # Dans certains formats, la photo est dans un paragraphe N et sa légende
    # est dans le paragraphe N+1 (sans embed). Reconstituer le mappage en
    # ré-itérant.
    photos_seen = []
    for p in body:
        if p["embeds"]:
            for rId in p["embeds"]:
                photos_seen.append(rId)

    # Reparcourir les pièces et compléter les rId manquants dans l'ordre
    rid_iterator = iter(photos_seen)
    for piece in pieces:
        for photo in piece.photos:
            if not photo.rId:
                try:
                    rId = next(rid_iterator)
                    photo.rId = rId
                    photo.image_file = rels.get(rId, "")
                except StopIteration:
                    pass

    return Brouillon(
        bailleur_raw=bailleur_raw,
        expose_raw=expose_raw,
        deferant_raw=deferant_raw,
        rendu_raw=rendu_raw,
        presence_raw=presence_raw,
        adresse_logement=adresse_logement,
        type_edl=type_edl,
        pieces=pieces,
        compteurs_brut=compteurs_brut,
        boite_aux_lettres_brut=boite_brut,
        cles_brut=cles_brut,
        photos_count=sum(len(p.photos) for p in pieces),
    )


# --------------------------------------------------------------------------
#  Sérialisation JSON
# --------------------------------------------------------------------------

def to_dict(b: Brouillon) -> dict:
    """Convertit la dataclass en dict JSON-compatible."""
    return asdict(b)


# --------------------------------------------------------------------------
#  CLI
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Brouillon .docx à analyser")
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Chemin du JSON de sortie",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERREUR : fichier introuvable : {args.input}", file=sys.stderr)
        return 1

    try:
        brouillon = extract(args.input)
    except Exception as e:
        print(f"ERREUR pendant l'extraction : {e}", file=sys.stderr)
        return 2

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(to_dict(brouillon), f, ensure_ascii=False, indent=2)

    # Résumé console
    print(f"OK — {len(brouillon.pieces)} pièces extraites, "
          f"{brouillon.photos_count} photos.")
    print(f"Type EDL détecté : {brouillon.type_edl or 'INDÉTERMINÉ (à demander)'}")
    print(f"Adresse : {brouillon.adresse_logement or 'INDÉTERMINÉE'}")
    print(f"Présence : {brouillon.presence_raw or 'AUCUNE'}")
    print(f"JSON écrit dans : {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
