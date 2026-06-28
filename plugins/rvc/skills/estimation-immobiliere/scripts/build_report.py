#!/usr/bin/env python3
"""build_report_v2.py — identique à build_report.py (copie de synchro)."""
import sys, json, os, base64, html, mimetypes
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


def e(x):
    return html.escape(str(x)) if x is not None else ""

def eur(n):
    try:
        return f"{int(round(float(n))):,}".replace(",", " ") + " €"
    except (TypeError, ValueError):
        return e(n)

def eurm2(n):
    try:
        return f"{int(round(float(n))):,}".replace(",", " ") + " €/m²"
    except (TypeError, ValueError):
        return e(n)

def num(n):
    try:
        return f"{int(round(float(n))):,}".replace(",", " ")
    except (TypeError, ValueError):
        return e(n)

def asset_data_uri(*names):
    for nm in names:
        p = ASSETS / nm
        if p.exists():
            mime = mimetypes.guess_type(str(p))[0] or "image/png"
            data = base64.b64encode(p.read_bytes()).decode()
            return f"data:{mime};base64,{data}"
    return ""

def img_data_uri(path):
    if not path:
        return ""
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / path
    if not p.exists():
        return ""
    mime = mimetypes.guess_type(str(p))[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


LOGO_COLOR = asset_data_uri("logo-rvc-color.png", "logo-rvc-color.svg")
LOGO_WHITE = asset_data_uri("logo-rvc-white.png", "logo-rvc-white.svg")


def footer(meta):
    ag = meta.get("agence", {})
    return f"""<div class="footer">
      <div class="f-left"><b>{e(ag.get('nom','RVC IMMOBILIER'))}</b><br>{e(ag.get('tel',''))}<br>{e(ag.get('email',''))}</div>
      <div class="f-right">Propriété de {e(meta.get('client',''))}<br>Située à {e(meta.get('ville',''))}<br>DATE : {e(meta.get('date',''))}</div>
    </div>"""

def band(title, kicker="Étude de marché"):
    logo = f'<img class="logo-mini" src="{LOGO_WHITE}">' if LOGO_WHITE else ""
    return f"""<div class="band"><div><div class="kicker">{e(kicker)}</div><h2>{e(title)}</h2></div>{logo}</div>"""

def page(title, body, meta, kicker="Étude de marché"):
    return f"""<section class="page">
      {band(title, kicker)}
      <div class="content">{body}</div>
      {footer(meta)}
    </section>"""


def cover(meta, bien):
    logo = f'<img class="cover-logo" src="{LOGO_WHITE}">' if LOGO_WHITE else ""
    return f"""<section class="page cover">
      <div class="cover-top">
        {logo}
        <div class="cover-kicker">Étude de marché</div>
        <h1>ESTIMATION<br>IMMOBILIÈRE</h1>
        <div class="cover-rule"></div>
      </div>
      <div class="cover-mid">
        <div class="cover-sub">Évaluation du {e(meta.get('date_longue', meta.get('date','')))}</div>
        <div class="cover-addr">{e(bien.get('adresse',''))}</div>
        <div class="cover-addr" style="font-size:15pt">{e(bien.get('cp',''))} {e(bien.get('commune',''))}</div>
        <div class="cover-client">À la demande de {e(meta.get('client',''))}</div>
      </div>
      <div class="cover-foot">
        <b>{e(meta.get('agence',{}).get('nom','RVC IMMOBILIER'))}</b> — {e(meta.get('agence',{}).get('adresse',''))}<br>
        {e(meta.get('agence',{}).get('tel',''))} &nbsp;·&nbsp; {e(meta.get('agence',{}).get('email',''))}
      </div>
    </section>"""

DEFAULT_AGENCE_DESC = (
    "RVC IMMOBILIER est le département immobilier d'une étude de commissaires de "
    "justice présente sur trois sites : Avranches, Saint-Pierre et Vire. Nous "
    "gérons, administrons et évaluons les biens avec la rigueur, l'indépendance et "
    "l'impartialité propres aux officiers ministériels."
)

def page_identite(meta, bien):
    ag = meta.get("agence", {})
    desc = ag.get("description") or DEFAULT_AGENCE_DESC
    body = f"""
      <h3 class="section">Votre bien & notre étude</h3>
      <div class="blocks">
        <div class="block">
          <div class="b-title">Le bien</div>
          <div class="b-name">{e(bien.get('titre',''))}</div>
          <div class="li"><b>Adresse :</b> {e(bien.get('adresse',''))}, {e(bien.get('cp',''))} {e(bien.get('commune',''))}</div>
          <div class="li"><b>Type :</b> {e(bien.get('type',''))}</div>
          <div class="li"><b>Surface :</b> {e(bien.get('surface_carrez',''))} m²</div>
          <div class="li"><b>Propriétaire :</b> {e(meta.get('client',''))}</div>
        </div>
        <div class="block">
          <div class="b-title">Notre étude</div>
          <div class="b-name">{e(ag.get('nom','RVC IMMOBILIER'))}</div>
          <p style="font-size:9.3pt;margin:2mm 0">{e(desc)}</p>
          <div class="li"><b>Adresse :</b> {e(ag.get('adresse',''))}</div>
          <div class="li"><b>Tél :</b> {e(ag.get('tel',''))}</div>
          <div class="li"><b>Email :</b> {e(ag.get('email',''))}</div>
        </div>
      </div>
      <div class="callout navy">{e(meta.get('intro',''))}</div>
    """
    return page("Votre bien & notre étude", body, meta)

ICONS = {
    "administration": "<path d='M3 9 12 3 21 9' /><path d='M5 9v9M9 9v9M15 9v9M19 9v9' /><path d='M3 18h18' />",
    "enseignement": "<path d='M12 4 2 9l10 5 10-5-10-5z' /><path d='M6 11v5c0 1 3 3 6 3s6-2 6-3v-5' />",
    "commerces": "<circle cx='9' cy='20' r='1.4'/><circle cx='17' cy='20' r='1.4'/><path d='M2 3h3l2.4 12.4a1 1 0 0 0 1 .8h8.6a1 1 0 0 0 1-.8L21 7H6' />",
    "transports": "<rect x='4' y='4' width='16' height='12' rx='2'/><path d='M4 11h16'/><circle cx='8' cy='19' r='1.3'/><circle cx='16' cy='19' r='1.3'/>",
    "sante": "<path d='M10 3h4v7h7v4h-7v7h-4v-7H3v-4h7z' />",
    "loisirs": "<path d='M12 2 5 12h4l-3 6h12l-3-6h4z' /><path d='M11 18h2v4h-2z' />",
}

def svg_icon(key):
    g = ICONS.get(key, "")
    if not g:
        return ""
    return ("<svg class='poi-svg' viewBox='0 0 24 24' fill='none' "
            "stroke='#B8975A' stroke-width='1.7' stroke-linecap='round' "
            "stroke-linejoin='round'>" + g + "</svg>")

POI_CATS = [
    ("Administration", "administration"),
    ("Enseignement", "enseignement"),
    ("Commerces", "commerces"),
    ("Transports", "transports"),
    ("Santé", "sante"),
    ("Loisirs", "loisirs"),
]

def page_poi(meta, poi):
    cards = ""
    for label, key in POI_CATS:
        items = poi.get(key) or []
        if not items:
            continue
        lis = "".join(f"<div class='poi-li'>{e(i)}</div>" for i in items)
        cards += f"""<div class='poi-cat'>
            <div class='poi-head'><span class='poi-ico'>{svg_icon(key)}</span>{e(label)}</div>
            {lis}</div>"""
    grid = f"<div class='poi-grid'>{cards}</div>" if cards else ""

    carte = img_data_uri(poi.get("carte"))
    rayon = poi.get("rayon_km")
    map_block = ""
    if carte:
        cap = f"Commerces et services dans un rayon de {e(rayon)} km autour du bien." if rayon else "Localisation du bien et des services à proximité."
        map_block = f"<div class='map-wrap'><img class='map-img' src='{carte}'><div class='map-cap'>{cap}</div></div>"
    elif rayon:
        map_block = f"<div class='callout'>Tous ces services sont accessibles dans un rayon d'environ {e(rayon)} km autour du bien.</div>"

    body = f"""
      <h3 class="section">Les points d'intérêt à proximité</h3>
      {map_block}
      {grid}
      <div class="callout">{e(poi.get('commentaire',''))}</div>
    """
    return page("Points d'intérêt à proximité", body, meta)

def comparison_bars(items):
    rows = ""
    for it in items:
        b = it.get("bien"); s = it.get("secteur")
        try:
            mx = max(float(b), float(s)) or 1
        except (TypeError, ValueError):
            continue
        unite = it.get("unite", "")
        wb = max(6, round(float(b) / mx * 100))
        ws = max(6, round(float(s) / mx * 100))
        rows += f"""<div class='cmp-row'>
            <div class='cmp-label'>{e(it.get('label',''))}</div>
            <div class='cmp-bars'>
              <div class='cmp-line'><div class='cmp-bar bien' style='width:{wb}%'></div><span class='cmp-val'>{e(b)}{e(unite)}</span></div>
              <div class='cmp-line'><div class='cmp-bar sect' style='width:{ws}%'></div><span class='cmp-val'>{e(s)}{e(unite)}</span></div>
            </div></div>"""
    legend = """<div class='legend'><span><i style='background:#1B2A4A'></i>Votre bien</span><span><i style='background:#B8975A'></i>Moyenne du secteur</span></div>"""
    return f"<div class='cmp'>{rows}</div>{legend}"

def page_descriptif(meta, bien):
    specs = [
        ("Type de bien", bien.get("type")),
        ("Année de construction", bien.get("annee")),
        ("Nombre de pièces", bien.get("pieces")),
        ("Nombre de chambres", bien.get("chambres")),
        ("Surface habitable (Carrez)", f"{bien.get('surface_carrez','')} m²" if bien.get("surface_carrez") else None),
        ("Surface du terrain", f"{bien.get('terrain','')} m²" if bien.get("terrain") else None),
        ("DPE / Classe énergie", bien.get("dpe")),
        ("GES", bien.get("ges")),
        ("État général", bien.get("etat")),
        ("Occupation", bien.get("occupation")),
    ]
    spec_html = "".join(
        f"<div class='spec'><span>{e(l)}</span><span>{e(v)}</span></div>"
        for l, v in specs if v not in (None, "", "None"))

    annexes = bien.get("annexes") or []
    annexes_rows = "".join(
        f"<tr><td>{e(a.get('designation',''))}</td><td class='t-num'>{e(a.get('surface',''))} m²</td></tr>"
        for a in annexes)
    annexes_tbl = ""
    if annexes_rows:
        annexes_tbl = f"""<h4>Les surfaces et annexes</h4>
          <table><tr><th>Désignation</th><th class='t-num'>Surface</th></tr>
          <tr><td>Le bien</td><td class='t-num'>{e(bien.get('surface_carrez',''))} m² loi Carrez</td></tr>
          {annexes_rows}</table>"""

    equip = bien.get("equipements") or []
    equip_html = ""
    if equip:
        equip_html = "<h4>Équipements & prestations</h4><div class='blocks'><div class='block' style='flex:1'>" + \
            "".join(f"<div class='li'>· {e(x)}</div>" for x in equip) + "</div></div>"

    fin = ""
    if bien.get("charges_annuelles") is not None:
        fin = f"""<h4>Les éléments financiers</h4>
          <div class='spec'><span>Charges annuelles</span><span>{eur(bien.get('charges_annuelles'))}</span></div>"""

    photos = bien.get("photos") or []
    pimgs = [img_data_uri(p) for p in photos]
    pimgs = [p for p in pimgs if p]
    photos_html = ""
    if pimgs:
        photos_html = "<h4>Photographies</h4><div class='photos'>" + \
            "".join(f"<img src='{p}'>" for p in pimgs[:6]) + "</div>"

    comp = bien.get("comparaison") or {}
    comp_html = ""
    if comp.get("items"):
        comp_html = f"""<h4>Votre bien face au secteur</h4>
          {comparison_bars(comp['items'])}
          <div class="callout">{e(comp.get('commentaire',''))}</div>"""

    body = f"""
      <h3 class="section">État descriptif du bien</h3>
      <div class="specs">{spec_html}</div>
      {annexes_tbl}
      {fin}
      {equip_html}
      <div class="callout">{e(bien.get('commentaire',''))}</div>
      {comp_html}
      {photos_html}
    """
    return page("État descriptif du bien", body, meta)

def card_vendu(c):
    metas = []
    if c.get("surface"): metas.append(f"{e(c['surface'])} m²")
    if c.get("pieces"): metas.append(f"{e(c['pieces'])} pièces")
    if c.get("terrain"): metas.append(f"terrain {e(c['terrain'])} m²")
    if c.get("date"): metas.append(f"vendu {e(c['date'])}")
    meta_html = "".join(f"<span>{m}</span>" for m in metas)
    note = c.get("note") or f"Vente enregistrée (source DVF) d'un bien comparable situé à {e(c.get('ville',''))}."
    return f"""<div class="card vendu">
      <div class="c-head">Vendu</div>
      <div class="c-body">
        <div class="c-type">{e(c.get('type','Maison'))}</div>
        <div class="c-loc">{e(c.get('ville',''))}</div>
        <div class="c-meta">{meta_html}</div>
        <div class="c-note">{note}</div>
        <div class="c-price"><span class="p-tot">{eur(c.get('prix'))}</span><span class="p-m2">{eurm2(c.get('prix_m2'))}</span></div>
      </div></div>"""

def card_vente(c):
    metas = []
    if c.get("surface"): metas.append(f"{e(c['surface'])} m²")
    if c.get("pieces"): metas.append(f"{e(c['pieces'])} pièces")
    if c.get("jours"): metas.append(f"{e(c['jours'])} j en ligne")
    meta_html = "".join(f"<span>{m}</span>" for m in metas)
    note = c.get("note") or ""
    return f"""<div class="card vente">
      <div class="c-head">À vendre</div>
      <div class="c-body">
        <div class="c-type">{e(c.get('type','Maison'))}</div>
        <div class="c-loc">{e(c.get('ville',''))}</div>
        <div class="c-meta">{meta_html}</div>
        <div class="c-note">{note}</div>
        <div class="c-price"><span class="p-tot">{eur(c.get('prix'))}</span><span class="p-m2">{eurm2(c.get('prix_m2'))}</span></div>
      </div></div>"""

def page_comparables(meta, vendus, ventes):
    pages = []
    if ventes:
        body = f"""<h3 class="section">Les éléments de comparaison — en vente</h3>
          <p class="lead">Annonces de biens comparables actuellement proposés à la vente sur le secteur.</p>
          <div class="cards">{''.join(card_vente(c) for c in ventes[:6])}</div>"""
        pages.append(page("Éléments de comparaison — en vente", body, meta))
    if vendus:
        body = f"""<h3 class="section">Les éléments de comparaison — vendus (DVF)</h3>
          <p class="lead">Transactions réelles enregistrées (base publique « Demandes de valeurs foncières »).</p>
          <div class="cards">{''.join(card_vendu(c) for c in vendus[:6])}</div>"""
        pages.append(page("Éléments de comparaison — vendus", body, meta))
    return "".join(pages)

def kpi(val, lab, alt=False):
    return f"<div class='kpi{' alt' if alt else ''}'><div class='k-val'>{val}</div><div class='k-lab'>{e(lab)}</div></div>"

def trend(v):
    try:
        f = float(v)
        cls = "up" if f >= 0 else "down"
        arrow = "▲" if f >= 0 else "▼"
        return f"<span class='{cls}'>{arrow} {f:+.2f} %</span>"
    except (TypeError, ValueError):
        return e(v)

def page_marche(meta, marche):
    comm = marche.get("commune", {})
    dep = marche.get("departement", {})
    sect = marche.get("secteur", {})

    krow = ""
    if comm.get("maison_med"): krow += kpi(eurm2(comm["maison_med"]), f"Prix médian maison — {comm.get('libelle','commune')}")
    if comm.get("appt_med"): krow += kpi(eurm2(comm["appt_med"]), f"Prix médian appart. — {comm.get('libelle','commune')}", alt=True)
    if dep.get("maison_med"): krow += kpi(eurm2(dep["maison_med"]), f"Médian maison — dépt {dep.get('libelle','')}", alt=True)

    def row(label, key, fmt=num):
        cells = ""
        for sc in (dep, comm, sect):
            cells += f"<td class='t-num'>{fmt(sc.get(key)) if sc.get(key) is not None else '—'}</td>"
        return f"<tr><td>{e(label)}</td>{cells}</tr>"

    tbl = f"""<table>
      <tr><th>Indicateur</th><th class='t-num'>Département</th><th class='t-num'>Commune</th><th class='t-num'>Secteur</th></tr>
      {row('Prix médian maison (€/m²)', 'maison_med', eurm2)}
      {row('Prix moyen maison (€/m²)', 'maison_moy', eurm2)}
      {row('Nb de ventes maisons', 'maison_nb')}
      {row('Prix médian appartement (€/m²)', 'appt_med', eurm2)}
      {row('Nb de ventes appartements', 'appt_nb')}
    </table>"""

    extra = ""
    if marche.get("prix_offre_maison") or marche.get("evol_prix_maison") is not None:
        extra = f"""<h4>Le marché de l'offre (mises en vente)</h4>
          <table>
            <tr><th>Indicateur</th><th class='t-num'>Maison</th><th class='t-num'>Appartement</th></tr>
            <tr><td>Prix constaté des mises en vente</td><td class='t-num'>{eurm2(marche.get('prix_offre_maison')) if marche.get('prix_offre_maison') else '—'}</td><td class='t-num'>{eurm2(marche.get('prix_offre_appt')) if marche.get('prix_offre_appt') else '—'}</td></tr>
            <tr><td>Évolution mensuelle du prix de l'offre</td><td class='t-num'>{trend(marche.get('evol_prix_maison'))}</td><td class='t-num'>{trend(marche.get('evol_prix_appt'))}</td></tr>
          </table>"""

    pbar = ""
    scales = [("Département "+e(dep.get('libelle','')), dep.get("maison_med"), False),
              ("Commune "+e(comm.get('libelle','')), comm.get("maison_med"), True),
              ("Secteur", sect.get("maison_med"), False)]
    vals = [v for _, v, _ in scales if v]
    if vals:
        mx = max(vals)
        rws = ""
        for lab, v, hl in scales:
            if not v:
                continue
            w = max(12, round(float(v) / mx * 100))
            cls = "gold" if hl else ""
            rws += f"<div class='pbar-row'><div class='pbar-lab'>{lab}</div><div class='pbar-track'><div class='pbar-fill {cls}' style='width:{w}%'>{eurm2(v)}</div></div></div>"
        pbar = f"<h4>Prix médian des maisons (€/m²)</h4><div class='pbar'>{rws}</div>"

    body = f"""
      <h3 class="section">Le marché immobilier local</h3>
      <div class="kpis">{krow}</div>
      {pbar}
      {tbl}
      {extra}
      <div class="callout">{e(marche.get('commentaire',''))}</div>
      <p class="small">Source : base publique DVF (Demandes de valeurs foncières) agrégée — statistiques sur la période disponible. Données présentées hors frais d'agence et de mutation.</p>
    """
    return page("Le marché immobilier", body, meta)

def page_socio(meta, socio):
    if not socio:
        return ""
    def row(label, key, fmt=num):
        cells = ""
        for sc in ("departement","code_postal","secteur"):
            v = socio.get(sc, {}).get(key)
            cells += f"<td class='t-num'>{fmt(v) if v is not None else '—'}</td>"
        return f"<tr><td>{e(label)}</td>{cells}</tr>"
    tbl = f"""<table>
      <tr><th>Indicateur</th><th class='t-num'>Département</th><th class='t-num'>Code postal</th><th class='t-num'>Secteur</th></tr>
      {row('Population','population')}
      {row('Foyers','foyers')}
      {row("Nombre d'actifs",'actifs')}
      {row('Part de retraités','retraites', lambda x: f"{e(x)} %")}
      {row('Revenu médian','revenu_median', eur)}
    </table>"""
    body = f"""
      <h3 class="section">Les éléments socio-économiques</h3>
      {tbl}
      <div class="callout">{e(socio.get('commentaire',''))}</div>
    """
    return page("Environnement socio-économique", body, meta)

def page_estimation(meta, est):
    eds = []
    if est.get("prix_m2_retenu"): eds.append((eurm2(est["prix_m2_retenu"]), "Prix retenu au m²"))
    if est.get("valeur_bien"): eds.append((eur(est["valeur_bien"]), "Valeur du bâti"))
    if est.get("valorisation_annexes"): eds.append((eur(est["valorisation_annexes"]), "Valorisation annexes / terrain"))
    detail = ""
    if eds:
        detail = "<div class='estim-detail'>" + "".join(
            f"<div class='ed'><div class='v'>{v}</div><div class='l'>{e(l)}</div></div>" for v, l in eds) + "</div>"

    body = f"""
      <h3 class="section">Notre étude de marché — estimation</h3>
      <p class="lead">{e(est.get('preambule','Cette estimation prend en considération les caractéristiques du bien et les données réelles du marché local.'))}</p>
      <div class="estim">
        <div class="e-lab">Valeur de marché estimée</div>
        <div class="e-val">{eur(est.get('valeur_moyenne'))}</div>
        <div class="e-range">Fourchette : <b>{eur(est.get('valeur_basse'))}</b> &nbsp;—&nbsp; <b>{eur(est.get('valeur_haute'))}</b></div>
      </div>
      {detail}
      <div class="callout navy"><b>Méthodologie.</b> {e(est.get('methodo',''))}</div>
      <div class="callout">{e(est.get('conclusion',''))}</div>
    """
    return page("Notre étude de marché", body, meta)

def page_mentions(meta):
    body = f"""
      <h3 class="section">Conditions générales d'usage</h3>
      <div class="mentions">
        <p>La présente étude de marché « valeur immobilière » est établie à titre indicatif et informatif à destination du propriétaire. Elle ne constitue ni une expertise au sens réglementaire, ni un engagement de prix.</p>
        <p>La valeur de marché du bien dépend des évolutions et fluctuations du contexte économique et réglementaire, de l'offre et de la demande et plus généralement du marché. La valeur déterminée ne saurait être transposée ni dans l'espace, ni dans le temps.</p>
        <p>Les données de marché sont issues de sources publiques (base DVF — Demandes de valeurs foncières) et, le cas échéant, d'annonces en cours de commercialisation citées à titre de comparaison. Toute information fournie par le client qui aurait été déformée, cachée ou tronquée pourrait influencer les résultats de cette étude.</p>
        <p>Propriété de : {e(meta.get('client',''))} &gt; Située à : {e(meta.get('ville',''))} &gt; Date : {e(meta.get('date',''))}.</p>
        <p>Document établi par {e(meta.get('agence',{}).get('nom','RVC IMMOBILIER'))}. Toute reproduction, même partielle, est interdite sans autorisation.</p>
      </div>
    """
    return page("Mentions & conditions", body, meta)


def build(data):
    meta = data.get("meta", {})
    bien = data.get("bien", {})
    parts = [cover(meta, bien), page_identite(meta, bien)]
    if data.get("points_interet"):
        parts.append(page_poi(meta, data["points_interet"]))
    parts.append(page_descriptif(meta, bien))
    parts.append(page_comparables(meta, data.get("comparables_vendus") or [], data.get("comparables_vente") or []))
    if data.get("socio"):
        parts.append(page_socio(meta, data["socio"]))
    if data.get("marche"):
        parts.append(page_marche(meta, data["marche"]))
    if data.get("estimation"):
        parts.append(page_estimation(meta, data["estimation"]))
    parts.append(page_mentions(meta))
    css = (ASSETS / "styles.css").read_text(encoding="utf-8")
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css}</style></head><body>{''.join(parts)}</body></html>"""


def main():
    if len(sys.argv) < 3:
        print("Usage: python build_report.py donnees.json sortie.pdf"); sys.exit(1)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    htmldoc = build(data)
    out = sys.argv[2]
    if os.environ.get("RVC_DEBUG_HTML"):
        Path(os.environ["RVC_DEBUG_HTML"]).write_text(htmldoc, encoding="utf-8")
    from weasyprint import HTML
    HTML(string=htmldoc, base_url=str(ROOT)).write_pdf(out)
    print(f"PDF généré : {out} ({os.path.getsize(out)} octets)")


if __name__ == "__main__":
    main()
