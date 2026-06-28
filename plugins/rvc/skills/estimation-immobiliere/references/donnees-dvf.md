# Récupérer les données de marché (DVF & autres)

## 1. Trouver le code INSEE de la commune
Le code INSEE (5 chiffres, ≠ code postal) est la clé de toutes les requêtes DVF.
- Si l'utilisateur ne le donne pas, le déduire de la commune + code postal.
- Exemple : Saint-James (50240) → INSEE **50487**. Le code département est constitué des 2 (ou 3) premiers chiffres : **50** (Manche).
- En cas de doute, chercher « code INSEE <commune> <code postal> » via WebSearch, ou interroger l'API geo : la commune est identifiable par son nom dans la base DVF (colonne `libelle_geo`).

## 2. Statistiques de prix au m² (commune / département / secteur)
Source : data.gouv MCP, dataset **« Statistiques DVF »**.
- Resource ID interrogeable (Tabular API) : `851d342f-9c96-41c1-924a-11a7a7aae8a6`
- Outil : `mcp__ea729888-...__query_resource_data`

Pour la **commune** : `filter_column="code_geo"`, `filter_value="<INSEE>"` (ex. `50487`).
Pour le **département** : `filter_value="<dépt>"` (ex. `50`).
Pour le **secteur** (section cadastrale, granularité plus fine que la commune) : les sections ont `code_parent = <INSEE commune>` et `echelle_geo = section`. Si l'utilisateur connaît la section, filtrer sur son `code_geo` ; sinon ce niveau peut rester vide.

Colonnes utiles renvoyées :
- `libelle_geo` — nom lisible
- `med_prix_m2_whole_maison`, `moy_prix_m2_whole_maison`, `nb_ventes_whole_maison`
- `med_prix_m2_whole_appartement`, `moy_prix_m2_whole_appartement`, `nb_ventes_whole_appartement`

→ alimente la section `marche` du JSON (commune / departement / secteur).

⚠️ Une cellule vide signifie « pas assez de ventes » — laisser le champ à `null`, ne pas inventer.

## 3. Transactions comparables vendues (cartes « Vendu »)
La base de stats ci-dessus ne donne pas le détail des ventes individuelles. Pour les cartes « Vendu » (adresse approximative, surface, prix, date), deux options :
1. **Demander à l'utilisateur** s'il a déjà des références de ventes récentes du quartier (le plus fiable).
2. **Utiliser des transactions DVF connues** fournies par l'utilisateur ou repérées via une recherche.
Garder 3 à 5 ventes comparables : même type de bien, surface proche (±30 %), commune ou secteur identique, vente récente (< 24 mois). Renseigner `prix` et `prix_m2` (prix / surface).

Si aucune transaction individuelle fiable n'est disponible, ne pas fabriquer de fausses ventes : se reposer sur les statistiques agrégées de la section 2 et l'indiquer.

## 4. Annonces en cours (cartes « À vendre »)
Tenter via **Claude in Chrome** (l'utilisateur a choisi cette option) sur Le Bon Coin / SeLoger / Leboncoin Immobilier.
- Charger les outils Chrome via ToolSearch (`query: "chrome"`).
- Naviguer vers une recherche filtrée (commune, type, nb pièces), lire la page (`get_page_text`).
- Ces sites ont des protections anti-robot : si l'accès échoue, **demander à l'utilisateur de coller 2-4 annonces** ; ne pas insister ni contourner.
Retenir 2-6 annonces comparables : `surface`, `pieces`, `prix`, `prix_m2`, `jours` en ligne si visible, courte `note`.

## 5. Socio-économie (facultatif)
Section `socio` du JSON : population, foyers, actifs, retraités, revenu médian, par département / code postal / secteur.
Si l'utilisateur n'a pas ces chiffres et qu'aucune source fiable n'est trouvée rapidement, **omettre la section** (le rapport reste cohérent) plutôt que d'inventer. Données INSEE (RP, Filosofi) disponibles sur data.gouv si besoin d'aller plus loin.

## 6. Points d'intérêt, urbanisme, permis
Ces éléments (écoles, commerces, transports, santé ; permis de construire) viennent en priorité des informations fournies par l'utilisateur, ou d'une recherche web ciblée. Les lister sobrement dans `points_interet`. Ne pas bloquer le rapport s'ils manquent.

## Règle d'or
Toujours privilégier une donnée vérifiable (DVF, info client) à une estimation « de tête ». Tout chiffre affiché doit être traçable. En l'absence de donnée, omettre la section concernée plutôt que de remplir avec du fictif.
