# Modèle de fichier de données pour le script

Le script `build_constat_inventaire.py` attend un fichier Python qui définit
deux objets : `ROOMS` et `ITEMS`.

## Format

```python
"""Données de l'inventaire : pièce, n° item, photos, description, état."""

# Liste ordonnée des pièces — elles seront imprimées dans cet ordre
# (saut de page avant chaque pièce). Les noms doivent être exactement
# ceux qui figurent dans le constat original.
ROOMS = [
    "Couloir", "Salon", "Séchoir", "Cuisine", "Placard",
    "Chambre", "Salle de douche", "Local annexe"
]

# Liste des items, dans l'ordre voulu pour le tableau.
# Tuple : (room, item_no, [photo_nos], description, etat)
#   - room        : str, le nom EXACT de la pièce (doit figurer dans ROOMS)
#   - item_no     : int, numéro d'item (1, 2, 3… continu sur toute l'habitation
#                   ou réinitialisé par pièce, au choix — l'utilisateur décide)
#   - photo_nos   : list[int], numéros des photos associées (telles que
#                   « Photographie n°X » dans le constat original).
#                   Liste vide [] si l'item n'a pas de photo (cas du local
#                   inaccessible).
#   - description : str, description retravaillée à partir de la lecture des
#                   photos. Phrases descriptives, neutres, factuelles.
#   - etat        : str, conservé pour compatibilité, NON imprimé dans le
#                   tableau actuel — laisser une chaîne vide "" suffit.
ITEMS = [
    # COULOIR
    ("Couloir", 1, [1], "Petit meuble d'angle de rangement en bois teinté foncé...", ""),
    ("Couloir", 2, [2], "Meuble colonne en bois clair à rideau coulissant...", ""),
    ("Couloir", 4, [4, 5], "Contenu de placards : photo 4 — étagères chargées de linge plié...", ""),

    # SALON
    ("Salon", 5, [6], "Téléviseur écran plat de marque Philips...", ""),
    # ... etc.

    # LOCAL ANNEXE (inaccessible)
    ("Local annexe", 61, [],
     "Local annexe inaccessible faute de clé : aucune constatation ni "
     "photographie n'a pu être effectuée à l'intérieur.",
     ""),
]
```

## Conseils de rédaction des descriptions

- **Toujours** privilégier ce que la photo montre sur ce que la dictée
  affirme. La dictée peut transformer « AYA » en « Haier », « marbre » en
  « su mineral », « Marc'Innov » en « Marc Innov SA ».
- **Toujours** signaler une divergence dictée/photo de façon neutre :
  *« le requérant indique X ; la lecture du logo donne Y »*.
- **Décrire** plutôt que **qualifier** :
  - ❌ « Belle commode en parfait état »
  - ✅ « Commode 4 tiroirs en mélaminé blanc, poignées chromées, propre,
       sans marque visible »
- **Mentionner** les défauts visibles factuellement :
  jaunissement, taches, déchirure, éclat, manque de pièce, encombrement.
- **Indiquer** quand le fonctionnement n'a pas été testé (« fonctionnement
  non testé ») — la photo ne prouve que l'état esthétique extérieur.
- **Ne pas confondre** un meuble avec son contenu. Si la dictée énumère
  papiers, vêtements, vaisselle… ces éléments font partie du bien inventorié
  (le meuble) ou de son contenu, à mentionner sans les détailler exhaustivement
  sauf intérêt particulier.

## Photos multiples par item

Si un même bien est documenté par plusieurs photos consécutives (par exemple
une table prise en gros plan + une chaise tachée), regrouper les numéros
dans la même liste : `[10, 11]`. Le tableau les empilera dans la cellule
photographie et la cellule « Photo n° ».

## Numéros d'items

L'usage le plus simple : numérotation continue (1, 2, 3… sur toute la maison)
et l'ordre suit la progression des pièces dans le constat. Cela évite d'avoir
deux items « n° 1 » dans des pièces différentes lorsqu'on parle de l'item
« n° 1 » sans préciser la pièce.

## Ordre des pièces

L'ordre dans `ROOMS` et l'ordre dans `ITEMS` doivent être cohérents : le
script regroupe par pièce mais respecte l'ordre de `ROOMS` pour l'affichage
final. Tout item dont la pièce n'est pas dans `ROOMS` est ignoré.
