# Méthodologie d'estimation

Objectif : produire une **valeur de marché** (moyenne) + une **fourchette basse/haute**, transparente et traçable. Le client doit pouvoir comprendre d'où vient le chiffre.

## Étape 1 — Prix de référence au m²
Partir du **prix médian DVF maison (ou appartement)** du niveau géographique le plus pertinent et suffisamment fourni :
- Privilégier le **secteur / commune** si `nb_ventes` y est suffisant (≥ ~15 ventes).
- Sinon, remonter au **département** et ajuster.

C'est le `prix_m2_retenu` de départ.

## Étape 2 — Ajustements qualitatifs
Le prix médian reflète le parc « moyen ». Ajuster en % selon les écarts du bien :

| Critère | Sens | Ordre de grandeur |
|---|---|---|
| Construction récente vs parc ancien | + | +5 à +20 % |
| Bon état / rénové vs à rafraîchir | ± | −15 % à +15 % |
| DPE favorable (A-C) vs passoire (F-G) | ± | −10 % à +10 % |
| Prestations supérieures (cuisine équipée, PAC, garage) | + | +3 à +10 % |
| Emplacement (centre, calme, vue) | ± | ±10 % |
| Travaux lourds à prévoir | − | −10 à −30 % |

Ces fourchettes sont des repères : les pondérer au cas par cas et **expliquer** le raisonnement dans le champ `methodo`. Ne pas empiler mécaniquement les maxima.

→ donne le **prix m² ajusté**, appliqué à la **surface habitable (Carrez)** = **valeur du bâti** (`valeur_bien`).

## Étape 3 — Valorisation des annexes et du terrain
À part du bâti :
- Combles aménageables / sous-sol / dépendances : valoriser à une fraction du prix habitable (souvent 20-50 % du €/m² selon l'usage).
- Terrain : selon le marché local du foncier et l'excédent par rapport à une parcelle « standard ».
- Garage, piscine, etc. : forfaits locaux.

→ `valorisation_annexes`.

## Étape 4 — Valeur moyenne et fourchette
`valeur_moyenne ≈ valeur_bien + valorisation_annexes`, arrondie (millier le plus proche, parfois 1 000-5 000 € près).

Fourchette : appliquer ±5 à ±8 % autour de la moyenne (cohérent avec le taux de négociation local observé dans DVF). `valeur_basse` et `valeur_haute`.

## Étape 5 — Cohérence
Vérifier que la valeur estimée tombe dans le nuage des comparables (ventes DVF + annonces). Si elle s'en écarte nettement, revoir les ajustements et l'expliquer. Croiser le €/m² implicite (valeur_moyenne / surface) avec le marché : il doit rester crédible.

## Toujours
- Renseigner `methodo` avec le calcul réel (chiffres utilisés), pas une formule générique.
- Ne jamais présenter l'estimation comme une expertise réglementaire : c'est une étude de marché indicative.
