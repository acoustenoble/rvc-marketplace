# Schéma du fichier `donnees.json`

Le script `scripts/build_report.py` lit ce JSON et génère le PDF. **Toute section absente est omise** — le rapport reste cohérent. Ne jamais inventer de valeurs ; mettre `null` ou retirer la clé si l'info manque.

Voir `examples/exemple-saint-james.json` pour un exemple complet et réel.

```jsonc
{
  "meta": {
    "date": "30/05/2026",                 // requis
    "date_longue": "samedi 30 mai 2026",  // facultatif (page de garde)
    "client": "SCI TROIS D",              // propriétaire / demandeur
    "ville": "SAINT-JAMES",
    "intro": "Texte d'introduction (page bien/agence).",
    "agence": {
      "nom": "RVC IMMOBILIER", "adresse": "...", "tel": "...", "email": "...",
      "description": "Département immobilier d'une étude de commissaires de justice (Avranches, Saint-Pierre, Vire)..."
    }
    // PAS de bloc "conseiller" : le bas de page cite uniquement l'étude RVC.
  },

  "bien": {
    "type": "Maison",                     // Maison / Appartement / ...
    "titre": "Maison 5 pièces à SAINT-JAMES",
    "adresse": "3 Rue des Lilas", "cp": "50240", "commune": "SAINT-JAMES", "insee": "50487",
    "surface_carrez": 95,                 // m² habitables — base du calcul
    "terrain": 500, "pieces": 5, "chambres": 3, "annee": 2009,
    "dpe": "D", "ges": "D",
    "etat": "Bon état général", "occupation": "Libre de toute occupation",
    "charges_annuelles": 1200,
    "equipements": ["Pompe à chaleur", "Double vitrage", "..."],
    "annexes": [ { "designation": "Combles utilisables", "surface": 80 } ],
    "commentaire": "Positionnement du bien vs le parc local.",
    "comparaison": {                      // graphique « bien vs moyenne du secteur »
      "items": [
        { "label": "Nombre de pièces", "bien": 5, "secteur": 4, "unite": "" },
        { "label": "Surface habitable", "bien": 95, "secteur": 82, "unite": " m²" },
        { "label": "Année de construction", "bien": 2009, "secteur": 1955, "unite": "" }
      ],
      "commentaire": "..."
    },
    "photos": ["/chemin/photo1.jpg"]      // chemins (absolus ou relatifs au skill). Omis si vide.
  },

  "points_interet": {                     // facultatif
    "rayon_km": 6.9,
    "carte": "/chemin/carte-google-maps.png",  // capture Maps (via Chrome) — facultatif
    "administration": ["..."], "enseignement": ["..."],
    "transports": ["..."], "sante": ["..."], "commerces": ["..."],
    "commentaire": "..."
  },

  "comparables_vente": [                  // « À vendre » (annonces). Facultatif.
    { "type": "Maison", "ville": "SAINT-JAMES (50240)", "surface": 106, "pieces": 5,
      "jours": 80, "prix": 167000, "prix_m2": 1575, "note": "..." }
  ],

  "comparables_vendus": [                 // « Vendu » (DVF). Facultatif.
    { "type": "Maison", "ville": "SAINT-JAMES (50240)", "surface": 133, "pieces": 5,
      "terrain": 699, "date": "31/03/2025", "prix": 120000, "prix_m2": 902 }
  ],

  "socio": {                              // facultatif (omettre si non fiable)
    "departement": { "population": 499529, "foyers": 221502, "actifs": 221527, "retraites": 41, "revenu_median": 24706 },
    "code_postal": { "...": 0 },
    "secteur":     { "...": 0 },
    "commentaire": "..."
  },

  "marche": {                             // données DVF — voir references/donnees-dvf.md
    "commune":     { "libelle": "Saint-James", "maison_med": 1240, "maison_moy": 1305, "maison_nb": 351, "appt_med": 2792, "appt_nb": 9 },
    "departement": { "libelle": "Manche", "maison_med": 1798, "maison_moy": 1956, "maison_nb": 31893, "appt_med": 2148, "appt_nb": 5010 },
    "secteur":     {},                    // peut rester vide
    "prix_offre_maison": 1200, "prix_offre_appt": 2030,   // facultatif (offre)
    "evol_prix_maison": 0.84, "evol_prix_appt": 1.5,      // % (facultatif)
    "commentaire": "..."
  },

  "estimation": {                         // voir references/methodologie-estimation.md
    "preambule": "...",
    "prix_m2_retenu": 1240,
    "valeur_bien": 117819,
    "valorisation_annexes": 71891,
    "valeur_moyenne": 188000, "valeur_basse": 176000, "valeur_haute": 200000,
    "methodo": "Détail chiffré du calcul (obligatoire).",
    "conclusion": "..."
  }
}
```

## Ordre des pages produites
Garde → Votre bien & agence → Points d'intérêt → Descriptif → Comparables (en vente, vendus) → Socio-économie → Marché → Estimation → Mentions.
