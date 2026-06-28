#!/usr/bin/env python3
"""Moteur d'assemblage du constat drone enrichi.

Injecte, dans un brouillon Juris Drone DÉJÀ dépaqueté (et dont les constatations ont déjà été
réécrites, la civilité corrigée et l'intro rédigée), les sections drone du PDF (placeholders résolus)
puis les ANNEXES (cartes). C'est la forme EXÉCUTABLE de references/boilerplate-drone.md — les deux
doivent rester synchronisés.

Ordre produit :
  … ME SUIS RENDU → INFORMATION SUR L'APPAREIL (titre + encadré lien) → CONSTATATIONS (chapitre,
  nouvelle page) → constatations réécrites → clôture + signature → COMPTE-RENDU DE VOL →
  CERTIFICATIONS TECHNIQUES → TRAVAUX PRÉPARATOIRES → AUTORISATIONS… → VÉRIFICATIONS… → ANNEXES.

Pilotage par un fichier JSON :
  { "vars": {...}, "include_metar": false, "annexes": [ {"file":..., "caption":..., "width":, "height":}, ... ] }

Usage:
    python3 build_constat_drone.py <unpacked_dir> <config.json> <annexes_dir>
"""
import sys, os, json, re, shutil

EMU_PER_CM = 360000
CONTENT_WIDTH_CM = 16.0


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def p_h1(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')


def p_body(text, bold=False, italic=False):
    rpr = '<w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="24"/>'
    if bold:
        rpr += '<w:b/>'
    if italic:
        rpr += '<w:i/>'
    rpr += '</w:rPr>'
    return (f'<w:p><w:pPr><w:pStyle w:val="HOParagraphe"/></w:pPr>'
            f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')


def p_li(text):
    return (f'<w:p><w:pPr><w:pStyle w:val="HOParagraphe"/>'
            f'<w:ind w:left="397" w:hanging="397"/></w:pPr>'
            f'<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="24"/></w:rPr>'
            f'<w:t xml:space="preserve">—\t{esc(text)}</w:t></w:r></w:p>')


def make_box(lines):
    """Encadré mis en avant (tableau 1 cellule, bordure bleu nuit, fond bleu clair).
    lines = liste de (variant, texte) avec variant ∈ {'b','n','i'}."""
    paras = []
    for variant, txt in lines:
        rpr = '<w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="24"/>'
        if variant == 'b':
            rpr += '<w:b/>'
        if variant == 'i':
            rpr += '<w:i/><w:color w:val="7F7F7F"/>'
        rpr += '</w:rPr>'
        paras.append('<w:p><w:pPr><w:spacing w:after="60"/><w:jc w:val="center"/></w:pPr>'
                     f'<w:r>{rpr}<w:t xml:space="preserve">{esc(txt)}</w:t></w:r></w:p>')
    inner = ''.join(paras)
    return (
        '<w:tbl><w:tblPr>'
        '<w:tblW w:w="9072" w:type="dxa"/><w:jc w:val="center"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="12" w:space="0" w:color="1F3A5F"/>'
        '<w:left w:val="single" w:sz="12" w:space="0" w:color="1F3A5F"/>'
        '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="1F3A5F"/>'
        '<w:right w:val="single" w:sz="12" w:space="0" w:color="1F3A5F"/>'
        '</w:tblBorders>'
        '<w:tblCellMar><w:top w:w="140" w:type="dxa"/><w:left w:w="180" w:type="dxa"/>'
        '<w:bottom w:w="140" w:type="dxa"/><w:right w:w="180" w:type="dxa"/></w:tblCellMar>'
        '</w:tblPr><w:tblGrid><w:gridCol w:w="9072"/></w:tblGrid>'
        '<w:tr><w:tc><w:tcPr><w:tcW w:w="9072" w:type="dxa"/>'
        '<w:shd w:val="clear" w:color="auto" w:fill="EAF0F6"/></w:tcPr>'
        f'{inner}</w:tc></w:tr></w:tbl>'
        '<w:p><w:pPr><w:pStyle w:val="HOParagraphe"/></w:pPr></w:p>'
    )


def render(blocks):
    out = []
    for kind, text in blocks:
        if kind == "h1":
            out.append(p_h1(text))
        elif kind == "sub":
            out.append(p_body(text, bold=True))
        elif kind == "li":
            out.append(p_li(text))
        elif kind == "box":
            out.append(make_box(text))
        elif kind == "spacer":
            out.append(p_body(""))
        else:
            out.append(p_body(text))
    return "".join(out)


# ---------------------------------------------------------------- SECTIONS
def sections(v, include_metar):
    f = lambda s: s.format(**v)
    S = {}

    S["info_appareil"] = [
        ("h1", "INFORMATION SUR L'APPAREIL UTILISÉ"),
        ("box", [
            ("b", "Le présent constat est réalisé au moyen d'un aéronef télépiloté sans équipage à bord (drone)."),
            ("n", "L'ensemble des données numériques capturées au cours de la mission — visite virtuelle à 360°, photographies et/ou séquences vidéo selon le support — sont consultables au(x) lien(s) suivant(s) :"),
            ("i", "[ lien(s) à insérer ]"),
        ]),
        ("sub", "Aéronef sans équipage à bord utilisé pour établir mes constatations :"),
        ("li", f("Aéronef sans équipage à bord {DRONE_MODELE} dont le numéro de série est le : {DRONE_SN} portant le numéro d'enregistrement {NUM_ENREGISTREMENT}.")),
        ("li", f("L'identifiant du signalement électronique est le {SIGNALEMENT_ELEC_ID} et le système d'identification directe à distance porte quant à lui le numéro : {ID_DIRECTE_DISTANCE}.")),
        ("li", f("L'aéronef est équipé d'une caméra DJI portant le numéro de série {CAMERA_SN}.")),
        ("li", f("La radiocommande {RADIOCOMMANDE_MODELE} porte le numéro de série : {RADIOCOMMANDE_SN}.")),
        ("li", f("L'aéronef est de classe {DRONE_CLASSE} tel que défini dans l'annexe du règlement délégué (UE) 2019/945.")),
    ]

    S["compte_rendu"] = [
        ("h1", "COMPTE-RENDU DE VOL"),
        ("sub", "Bilan des vols :"),
        ("p", "De retour à l'étude, j'ai extrait du logiciel de contrôle de vol la boîte noire sous forme de log correspondant à ma mission sous forme de fichier .txt lequel est archivé sur le serveur interne dédié de l'étude, ainsi que sur le serveur sécurisé de la SAS Juris Drone, et disponible sur simple demande des autorités compétentes. Les certifications techniques du présent vol sont également disponibles sur simple demande."),
    ]

    S["certifications"] = [
        ("h1", "CERTIFICATIONS TECHNIQUES"),
        ("sub", "AUDIT DU MATÉRIEL UTILISÉ"),
        ("p", "Les conditions suivantes s'appliquent à tous les aéronefs non captifs :"),
        ("li", "Le télépilote dispose d'une information d'altitude ou de hauteur basée sur un capteur barométrique."),
        ("li", "Un dispositif automatique empêche l'aéronef de dépasser une altitude ou une hauteur maximale programmable, même en cas de commande du télépilote ou d'activation d'un plan de vol automatique."),
        ("li", "Le télépilote peut à tout moment forcer un atterrissage d'urgence par arrêt des moteurs et la commande de cette fonction peut être testée au sol par le télépilote avant le vol."),
        ("li", "La perte de la liaison de commande et de contrôle entraîne la mise en œuvre d'une procédure d'atterrissage minimisant le risque de dysfonctionnement supplémentaire."),
        ("p", f("L'appareil est déclaré auprès de la Direction Générale de l'Aviation Civile depuis le {DATE_DECLA_DGAC} sous le numéro {NUM_ENREGISTREMENT}. Cette déclaration est valable jusqu'au {DATE_DECLA_DGAC_FIN}.")),
        ("sub", "Marquage sur l'appareil :"),
        ("p", "Sur l'aéronef utilisé pour les opérations de constatations est apposée une plaquette rectangulaire d'une dimension de 5 cm de long et de 3 cm de large, ou ayant une surface totale supérieure ou égale à 15 cm², comportant :"),
        ("li", f("Le nom de l'exploitant : {EXPLOITANT_NOM}")),
        ("li", f("Le numéro d'exploitation : {NUM_EXPLOITANT}")),
        ("li", f("L'adresse : {OFFICE_ADRESSE}")),
        ("li", f("Le numéro de téléphone : {OFFICE_TEL}")),
        ("li", f("Le numéro d'enregistrement : {NUM_ENREGISTREMENT}")),
        ("sub", "Masse, dispositif de signalement électronique et lumineux et identification à distance :"),
        ("p", "Pour les aéronefs d'une masse totale inférieure à 800 grammes, aucun dispositif de signalement électronique n'est nécessaire. En revanche, les aéronefs d'une masse totale supérieure à 800 grammes, conformément au décret du 30 octobre 2019 et à l'arrêté du 27 décembre 2019, doivent être équipés d'un dispositif de signalement lumineux et d'un dispositif de signalement électronique, et faire l'objet d'un enregistrement auprès de la Direction Générale de l'Aviation Civile."),
        ("p", f("En l'espèce, l'aéronef présente une masse nette avec batterie de {DRONE_MASSE} et respecte les dispositions susmentionnées.")),
        ("p", f("En conformité avec les points susmentionnés, l'identifiant de signalement électronique à distance de l'aéronef utilisé est : {SIGNALEMENT_ELEC_ID}. Il présente un format d'identification de type ANSI/CTA/2063-A (PSN).")),
        ("p", f("En complément du dispositif de signalement électronique relevant d'une exigence nationale, les aéronefs de classe C1, C2 et C3 sans équipage à bord doivent être équipés d'un système d'identification directe à distance au regard de la règlementation européenne. En l'espèce le drone utilisé est de classe {DRONE_CLASSE} tel que défini dans l'annexe du règlement délégué (UE) 2019/945 et son numéro d'identification directe à distance est le {ID_DIRECTE_DISTANCE}. Il est donc en conformité avec le règlement susmentionné.")),
        ("sub", "Assurance responsabilité civile professionnelle :"),
        ("p", f("L'entité exploitante {EXPLOITANT_NOM} fait l'objet d'une assurance en responsabilité civile professionnelle souscrite auprès de la compagnie {ASSUREUR}, avec un numéro de police d'assurance {POLICE_ASSURANCE}, valable jusqu'au {ASSURANCE_FIN}.")),
    ]

    legals = [
        "La convention relative à l'aviation civile internationale de Chicago du 7 décembre 1944, publiée par le décret n° 47-974 du 31 mai 1947 et l'ensemble des protocoles qui l'ont modifiée.",
        "Le décret n° 2022-1397 du 2 novembre 2022.",
        "Le règlement délégué (UE) 2019/945.",
        "Le règlement d'exécution (UE) 2019/947.",
        "L'arrêté du 23 décembre 2025 modifiant l'arrêté du 3 décembre 2020 relatif à l'utilisation de l'espace aérien par les aéronefs sans équipage à bord.",
        "L'arrêté du 3 décembre 2020 relatif aux exigences applicables aux pilotes à distance dans le cadre d'opérations relevant de la catégorie « ouverte ».",
        "Le décret n° 2018-882 du 11 octobre 2018 relatif à l'enregistrement des aéronefs civils circulant sans personne à bord.",
        "L'arrêté du 19 octobre 2018 relatif à l'enregistrement des aéronefs civils circulant sans personne à bord.",
        "L'arrêté du 27 décembre 2019 définissant les caractéristiques techniques des dispositifs de signalement électronique et lumineux des aéronefs circulant sans personne à bord.",
        "Le décret n° 2022-1397 du 2 novembre 2022 portant application de l'article L. 6224-1 du code des transports relatif au régime encadrant la captation et le traitement des données recueillies depuis un aéronef dans certaines zones.",
        "L'article L6211-3 du Code des transports.",
        "Les articles D. 6214-3 à D. 6214-14 du Code des transports.",
        "Le décret n° 2025-1449 du 31 décembre 2025 modifiant diverses dispositions du code des transports relatives aux télépilotes et aux aéronefs sans équipage à bord.",
        "L'article L.34-9-2 du Code des postes et des communications électroniques.",
        "L'arrêté du 17 novembre 2025 fixant la liste des zones interdites à la captation et au traitement des données recueillies depuis un aéronef.",
    ]
    travaux = [
        ("h1", "TRAVAUX PRÉPARATOIRES"),
        ("p", "À titre liminaire, il est indiqué que le présent constat effectué par assistance aérienne avec un aéronef circulant sans équipage à bord, est réalisé conformément aux dispositions de :"),
    ]
    travaux += [("li", t) for t in legals]
    travaux += [
        ("sub", "Description des obligations générales de l'exploitant et des normes de sécurité :"),
        ("p", "Les obligations générales de l'exploitant peuvent figurer dans le manuel d'exploitation (MANEX) qui est tenu à jour en cas de survol en catégorie spécifique. Ledit manuel décrivant les modalités de mise en œuvre des obligations règlementaires, consultable sur demande du requérant. De plus l'aéronef dispose d'un manuel d'utilisation et un manuel d'entretien à jour."),
    ]
    if include_metar:
        travaux += [
            ("sub", "Certification de contrôle des bonnes conditions de vol :"),
            ("p", f("Lors de mes opérations de constatation, le METAR publié le {METAR_DATETIME} de {METAR_AIRPORT} m'indique le code suivant : {METAR_CODE}")),
        ]
    travaux += [
        ("sub", "Certification de contrôle de la zone de vol :"),
        ("p", "Avant le vol, le site www.sia.aviation-civile.fr a été consulté afin de vérifier les cartes aériennes de la zone de survol, connaître les AIP, Sup AIP et NOTAM pour identifier les éventuelles restrictions, y compris temporaires, de vol sur le site survolé lors de la mission et, le cas échéant, obtenir les accords des gestionnaires de sites concernés."),
        ("p", "Les cartes aéronautiques, la carte de la zone de vol, les cartes de protection drone et les cartes OACI 1/500 000 correspondantes sont reportées en ANNEXES du présent constat."),
        ("sub", "Espace aérien survolé :"),
        ("p", "Toujours à l'aide du site internet du service de l'information aéronautique, www.sia.aviation-civile.fr, j'ai vérifié également que la zone d'évolution de l'aéronef s'inscrivait dans une zone d'aviation autorisée, ne comportant aucune limitation ou restriction particulière quant à la hauteur de vol ou la zone de survol. En l'espèce la zone survolée se trouve en dehors d'une CTR et ne tombe pas sous l'emprise d'un aérodrome, un héliport, une zone militaire, ou d'une autre zone dont l'accès serait soumis à autorisation ou déclaration."),
        ("sub", "Détermination de la sous-catégorie et de l'environnement de vol :"),
        ("p", "Un aéronef est dit évoluer « en vue directe » lorsque ses évolutions se situent à une distance du télépilote telle que celui-ci conserve une vue directe sur l'aéronef et une vue dégagée sur l'environnement aérien permettant de détecter tout rapprochement d'aéronef et de prévenir les collisions. En l'espèce, le drone a été conservé dans mon champ de vision direct durant toute la durée des opérations."),
        ("p", "Conformément au règlement d'exécution (UE) 2019/947 de la Commission du 24 mai 2019 (annexe, partie A, catégorie « ouverte »), les opérations en catégorie ouverte sont réparties en sous-catégories A1, A2 et A3. L'opération en sous-catégorie A2 est réalisée avec un aéronef de classe C2 uniquement, impose une absence de survol de personnes non impliquées ainsi qu'une distance horizontale de sécurité supérieure ou égale à 30 m par rapport à ces personnes, réductible à 5 m si le mode « basse vitesse » à 3 m/s est actif."),
        ("p", f("En l'espèce, l'aéronef utilisé est un drone de la marque DJI modèle {DRONE_MODELE} de classe {DRONE_CLASSE} tel que défini dans l'annexe du règlement délégué (UE) 2019/945.")),
        ("p", f("En l'espèce le survol a lieu sur la commune de {COMMUNE} et s'effectue en dehors de tout rassemblement de personnes tel que défini par la Direction générale de l'aviation civile et sur une zone privée.")),
        ("sub", "Règles applicables au présent vol :"),
        ("p", f("En application des précédentes règles visées, le présent constat s'effectue selon les règles de la sous-catégorie {SOUS_CATEGORIE}, avec un drone de classe {DRONE_CLASSE} et la hauteur maximum de survol sera de {HAUTEUR_MAX} par rapport au sol.")),
    ]
    S["travaux"] = travaux

    S["autorisations"] = [
        ("h1", "AUTORISATIONS ET DÉCLARATIONS ADMINISTRATIVES DE VOL"),
        ("p", f("Afin de pouvoir effectuer le présent constat avec un aéronef circulant sans équipage à bord, il est rappelé que M. {TELEPILOTE_NOM}, Commissaire de justice associé en charge des opérations, ayant « le contrôle et la maîtrise direct de l'aéronef » et procédant aux prises de vues ainsi qu'à leur interprétation, est titulaire du certificat de télépilote théorique n°{CERT_TELEPILOTE} délivré par la RDW et expirant le {CERT_TELEPILOTE_FIN}.")),
        ("p", f("Concernant les prises de vues, l'entité exploitante de l'aéronef est enregistrée auprès de la Direction générale de l'aviation civile en tant qu'exploitant de drone, sous le numéro {NUM_EXPLOITANT}.")),
        ("sub", "Déclaration de vol :"),
        ("p", f("La présente mission s'effectuant en sous-catégorie {SOUS_CATEGORIE}, le survol ne s'effectue pas au-dessus de la voie publique au sein d'une zone peuplée ou à proximité d'un rassemblement de personnes. En conséquence, aucune déclaration préfectorale n'est requise.")),
        ("sub", "CNIL :"),
        ("p", f("Les informations recueillies font l'objet d'un traitement informatique destiné à la création et à la pré-rédaction du présent constat. Les données sont uniquement destinées au service Juris Drone, ayant son siège {JURIS_DRONE_SIEGE}. Elles seront conservées le temps nécessaire pour répondre aux obligations légales en matière de suivi du constat.")),
        ("p", "Conformément à la Loi « Informatique et Libertés » n°78-17 du 06 Janvier 1978 modifiée et au Règlement Général sur la Protection des Données, vous disposez d'un droit d'accès aux données vous concernant ou pouvez demander leur effacement. Vous disposez également d'un droit d'opposition, de rectification, à la portabilité et à la limitation du traitement de vos données (cf. cnil.fr)."),
        ("p", f("Pour exercer ces droits, sous réserve de justifier de votre identité, vous pouvez contacter notre étude : {CONTACT_EMAIL} — {OFFICE_ADRESSE}. Si vous estimez après nous avoir contactés que vos droits ne sont pas respectés, vous pourrez à tout moment saisir l'autorité de contrôle (CNIL).")),
    ]

    S["verifications"] = [
        ("h1", "VÉRIFICATIONS TECHNIQUES PRÉALABLES"),
        ("p", "Avant le vol, j'ai effectué le contrôle des points suivants."),
        ("sub", "Paramètres de sécurité et de restriction de vol (application DJI PILOT 2) :"),
        ("p", "J'ai fixé la hauteur de vol du retour automatique au point de décollage (Return To Home) et défini une hauteur de vol maximum par rapport au sol."),
        ("sub", "Étalonnage des capteurs :"),
        ("p", "J'ai vérifié que les différents capteurs dont l'IMU (accéléromètre et gyroscope) du drone, ainsi que le compas, les moteurs, les capteurs de proximité, les batteries, le signal radio et la caméra, étaient tous dans un état dit « normal »."),
        ("sub", "Retour automatique au point de décollage :"),
        ("p", "J'ai activé la fonction smart RTH (retour au point de départ intelligent) permettant à l'appareil de retourner à ce point lorsque le niveau de batterie restant ne suffit plus ou que ce dernier perd la connexion avec la radiocommande."),
        ("sub", "Versions des firmwares :"),
        ("p", "J'ai vérifié que les firmwares de l'appareil, de la radiocommande et de la base de données « Fly Safe » soient bien à jour."),
        ("sub", "État visuel du drone :"),
        ("p", "Le drone ne présente aucun dégât apparent, aucune fissure, aucune trace de réparation. Les hélices sont en parfait état et ne sont ni ébréchées, ni fissurées. Avant le décollage, j'ai contrôlé que le drone était dans les conditions optimales pour décoller et disposait d'une connexion avec suffisamment de satellites."),
    ]
    return S


# ---------------------------------------------------------------- IMAGES
def add_image_rels_and_media(unpacked, annexes, annexes_dir):
    rels_path = os.path.join(unpacked, "word", "_rels", "document.xml.rels")
    media_dir = os.path.join(unpacked, "word", "media")
    os.makedirs(media_dir, exist_ok=True)
    with open(rels_path, encoding="utf-8") as fh:
        rels = fh.read()
    rid_nums = [int(m) for m in re.findall(r'Id="rId(\d+)"', rels)]
    next_rid = (max(rid_nums) + 1) if rid_nums else 1
    existing = set(os.listdir(media_dir))
    new_rels = []
    for a in annexes:
        src = os.path.join(annexes_dir, a["file"])
        target = a["file"]
        while target in existing:
            target = "drone_" + target
        shutil.copy(src, os.path.join(media_dir, target))
        existing.add(target)
        rid = f"rId{next_rid}"
        next_rid += 1
        a["_rid"] = rid
        new_rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{target}"/>')
    rels = rels.replace("</Relationships>", "".join(new_rels) + "</Relationships>")
    with open(rels_path, "w", encoding="utf-8") as fh:
        fh.write(rels)


def p_image(a, docpr_id):
    cx = int(CONTENT_WIDTH_CM * EMU_PER_CM)
    ratio = a.get("height", 700) / a.get("width", 1200)
    cy = int(cx * ratio)
    rid = a["_rid"]
    return (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{docpr_id}" name="Annexe{docpr_id}"/><wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr>'
        f'<pic:cNvPr id="{docpr_id}" name="Annexe{docpr_id}"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        '<a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr>'
        f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
        '</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
    )


# ---------------------------------------------------------------- INJECTION
def insert_before(xml, marker_text, fragment):
    pos = xml.find(marker_text)
    if pos == -1:
        raise SystemExit(f"Marqueur introuvable : {marker_text!r}")
    p_start = max(xml.rfind("<w:p>", 0, pos), xml.rfind("<w:p ", 0, pos))
    return xml[:p_start] + fragment + xml[p_start:]


def main():
    unpacked, config_path, annexes_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    cfg = json.load(open(config_path, encoding="utf-8"))
    v = cfg["vars"]
    S = sections(v, cfg.get("include_metar", False))

    doc_path = os.path.join(unpacked, "word", "document.xml")
    xml = open(doc_path, encoding="utf-8").read()

    # INFORMATION SUR L'APPAREIL (+ encadré lien) PUIS chapitre CONSTATATIONS, avant la lead-in.
    xml = insert_before(xml, "J'AI PROCEDE AUX CONSTATATIONS",
                        render(S["info_appareil"]) + p_h1("CONSTATATIONS"))

    # Appendices après la signature : COMPTE-RENDU -> CERTIFICATIONS -> TRAVAUX -> AUTORISATIONS -> VERIFICATIONS -> ANNEXES
    annexes = cfg.get("annexes", [])
    if annexes:
        add_image_rels_and_media(unpacked, annexes, annexes_dir)
    annexes_xml = render([
        ("h1", "ANNEXES"),
        ("p", "Les pièces ci-après illustrent le cadre de la mission de vol (zone de survol, cartes aéronautiques et cartes de protection drone consultées avant le vol). Elles sont annexées au présent procès-verbal pour en préciser les conditions de réalisation."),
    ])
    docpr = 9001
    for a in annexes:
        annexes_xml += p_body(a["caption"], bold=True)
        annexes_xml += p_image(a, docpr)
        annexes_xml += p_body("")
        docpr += 1

    appendix = (render(S["compte_rendu"]) + render(S["certifications"]) + render(S["travaux"]) +
                render(S["autorisations"]) + render(S["verifications"]) + annexes_xml)

    m = re.search(r"<w:sectPr[ >]", xml)
    if not m:
        raise SystemExit("sectPr final introuvable")
    cut = max(xml.rfind("<w:p>", 0, m.start()), xml.rfind("<w:p ", 0, m.start()))
    if cut == -1 or cut < xml.rfind("</w:tbl>", 0, m.start()):
        cut = m.start()
    xml = xml[:cut] + appendix + xml[cut:]

    open(doc_path, "w", encoding="utf-8").write(xml)
    print("Sections drone injectées. Annexes:", len(annexes))


if __name__ == "__main__":
    main()
