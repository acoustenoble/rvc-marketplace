# Structure d'une pièce — format strict

Chaque pièce du logement (hors Convocation, Compteurs, Boîte aux lettres et
Clés qui ont leurs propres formats — voir `templates.md`) doit suivre **à la
lettre** le gabarit ci-dessous. Aucune liberté n'est laissée au skill sur
l'ordre, le nommage ou la ponctuation des rubriques.

## Gabarit canonique

```
[N°] [Titre de la pièce]               ← Style Heading1, saut de page avant

[Phrase d'accès — OPTIONNELLE]

Sol : [description en une phrase, sans point final si pas nécessaire]

Murs : [description en une phrase, sans point final si pas nécessaire]

Plafond : [description en une phrase, sans point final si pas nécessaire]

Équipement :

  ● [élément 1]
  ● [élément 2]
  ● [élément 3]
  ● [...]

Mobilier : [RUBRIQUE OPTIONNELLE — uniquement si du mobilier a été dicté
            dans le brouillon, typiquement pour les EDL d'entrée en
            location meublée]

  ● [meuble 1]
  ● [meuble 2]
  ● [...]

[Photographies de la pièce, dans leur ordre, avec leur légende horodatée]
```

## Règles d'écriture par rubrique

### Titre de la pièce

- Style Word : `Heading1`.
- Numérotation automatique (`numId=3`) — ne pas écrire le numéro à la main.
- Casse : majuscule à l'initiale, minuscules ensuite (`Salle de douche`, pas `SALLE DE DOUCHE` ni `salle de douche`).
- Cas spéciaux : `WC` (toujours en majuscules), `Entrée / Couloir` (avec espaces autour du `/`), `Chambre 1`, `Chambre 2` (chiffre arabe collé après un espace).
- Saut de page avant chaque pièce (sauf la première qui suit `J'AI PROCEDE AUX CONSTATATIONS SUIVANTES :` — celle-ci, c'est `Convocation`).

### Phrase d'accès (optionnelle)

À insérer **uniquement** quand la pièce n'est pas accessible directement depuis
le couloir/l'entrée et que cette information apporte une précision utile à la
lecture (cf. `templates.md` § 4).

À **ne pas insérer** pour les pièces accessibles directement depuis le couloir
(WC, Salle de douche, Cuisine en général, Chambres). Dans ce cas la pièce
démarre directement par `Sol : …`.

### Sol

Ouvre la pièce. Une seule rubrique « Sol », jamais au pluriel. Toujours suivie
de deux-points + espace.

Décrire dans cet ordre :

1. **Matériau** (linoléum, parquet stratifié, parquet flottant, carrelage, dalles PVC, moquette, dalle béton, faïence…)
2. **État général** (à l'état d'usage, dégradé, en mauvais état, en très mauvais état)
3. **Défauts factuels visibles** (taches indélébiles, traces de griffures, brûlures, déchirures, plinthes écaillées, joints noircis, fissures, auréoles, fientes…)
4. **Niveau de propreté** (propre, sale, très sale, ensemble très sale, poussiéreux)

Exemples validés (issus du PV de référence) :

> *« Sol : linoléum dégradé avec traces de griffures, ensemble très sale, taches indélébiles »*
>
> *« Sol : linoléum, ensemble très sale »*
>
> *« Sol : dalle béton en très mauvais état avec importante présence de fientes de pigeons et fissuration au pied du garde-corps, ensemble très sale »*
>
> *« Sol : linoléum poussiéreux à l'état d'usage »*

### Murs

Ouvre la deuxième rubrique. Toujours **« Murs »** au pluriel (jamais « Mur »
au singulier, même si une seule paroi est traitée — l'usage du métier impose le
pluriel).

Décrire dans cet ordre :

1. **Revêtement** (tapisserie, papier peint, toile à peindre, peinture mate, peinture satinée, faïence, lambris, à nu/dégarni)
2. **État** (à l'état d'usage, dégradé, en mauvais état, en très mauvais état)
3. **Défauts factuels visibles** (déchirures, parties déchirées, trous de chevilles, trous de vis, fissures en ramification, écaillements, taches, auréoles à la jonction avec le plafond, traces de moisissure, traces d'enduit, parties brutes, inscriptions…)

Exemples validés :

> *« Murs : tapisserie dégradée en très mauvais état, parties déchirées à multiples endroits, trous de chevilles »*
>
> *« Murs : toile à peindre avec de nombreuses taches, plinthe écaillée, trous de chevilles »*
>
> *« Murs : très mauvais état avec fissurations en ramification, trous de chevilles laissant apparaître le béton »*
>
> *« Murs : dégradés, parties brutes avec inscriptions, tapisserie déchirée »*

### Plafond

Toujours **« Plafond »** au singulier.

Décrire dans cet ordre :

1. **Revêtement** (peint en blanc, toile à peindre, toile à peindre blanche, dalles, plaques de plâtre, à nu)
2. **État** (à l'état d'usage, dégradé)
3. **Défauts factuels visibles** (taches indélébiles, auréoles, fissures, autocollants, traces de moisissure…)

Exemples validés :

> *« Plafond : peint en blanc »*
>
> *« Plafond : toile à peindre blanche dégradée avec de nombreuses taches indélébiles »*
>
> *« Plafond : toile à peindre blanche à l'état d'usage »*
>
> *« Plafond : toile à peindre blanche avec autocollants en forme d'étoiles »*

**Cas particulier — pas de plafond visible** : pour le balcon, la loggia, la
terrasse, la rubrique Plafond peut être **omise** si elle n'a pas de sens. La
décision se prend au cas par cas selon le contenu du brouillon.

### Équipement

Ouvre la dernière rubrique de la pièce, sur sa propre ligne, suivie de
deux-points + espace puis d'un saut de ligne.

Format : **liste à puces** avec le caractère **`●` (U+25CF, BLACK CIRCLE)**.
Pas de tiret, pas de point final, pas de bullet Word standard.

Ordre logique recommandé pour énumérer les éléments d'équipement (à adapter au
contenu de la pièce) :

1. **Porte(s)** d'entrée et de communication
2. **Interrupteur(s)**
3. **Combiné interphone / visiophone**
4. **Prise(s) électrique(s)** classique(s)
5. **Prise(s) spéciale(s)** : 32 A, antenne TV, téléphone, RJ45
6. **Disjoncteur / tableau électrique**
7. **Chauffage** : radiateur (préciser tête thermostatique, fonte, panneaux), sèche-serviettes
8. **Ventilation** : bouche d'aération VMC, grille
9. **Fenêtre(s) / porte-fenêtre(s)** : préciser le type (simple battant, deux battants, châssis fixe), l'état du bâti / vitrage, la présence et le fonctionnement du volet roulant (manuel / électrique / fonctionnel / cassé)
10. **Éclairage** : néon, douille + ampoule, douille dépourvue d'ampoule, suspension, applique
11. **Sanitaire** : WC, lave-mains, évier, vasque, baignoire, cabine de douche, receveur
12. **Robinetterie** : robinet mitigeur, robinet mélangeur, douchette, flexible métallique, bonde, joint
13. **Mobilier intégré / cuisine** : meuble sous évier, plan de travail, hotte, plaque, four
14. **Sécurité** : détecteur incendie, socle de détecteur
15. **Divers** : butée de porte, miroir, porte-serviettes, étagère

Pour chaque élément, indiquer son **état de fonctionnement** quand pertinent
(`ouvrant et fermant correctement`, `cassé`, `descellé`, `arraché`, `dégondé`,
`ne fermant pas correctement`) et ses **défauts factuels visibles** (`très
sale`, `dégradé`, `taché`, `cassé`, `joint dégradé`, `dépourvu de [pièce]`).

Exemples validés (issus du PV de référence) :

```
Équipement :

  ● Porte depuis le palier, ouvrant et fermant correctement
  ● Quatre interrupteurs
  ● Combiné interphone très sale
  ● Butée de porte au sol cassée
  ● Prise électrique
  ● Disjoncteur
  ● Deux douilles dépourvues d'ampoules au plafond
  ● Socle de détecteur incendie dépourvu du détecteur
```

```
Équipement :

  ● Porte depuis le couloir ouvrant et fermant correctement, dégradée avec taches et rayures, pourtour de poignée avec traces d'enduit
  ● Interrupteur très sale
  ● Quatre prises électriques
  ● Bouche d'aération VMC très encrassée
  ● Radiateur très sale avec tête thermostatique
  ● Porte PVC très sale ouvrant et fermant correctement, équipée d'un volet roulant manuel fonctionnel
  ● Fenêtre à châssis fixe, vitrage et bâti très sales, importante présence de salissures
  ● Néon
  ● Évier dégradé avec robinet mitigeur, absence de bonde, joint dégradé
  ● Meuble sous évier ouvrant à deux portes, ensemble très sale, dégradé avec écaillements de peinture
  ● Douille et ampoule au plafond
  ● Prise 32 A sous plan de travail arrachée avec dominos apparents
```

### Photographies

À placer après l'équipement, dans leur ordre d'apparition dans le brouillon.

Conserver leur **légende horodatée** au format :

```
Photographie n° [N] - [JJ/MM/AAAA HH:MM:SS] - [LATITUDE] [LONGITUDE].
```

Exemple :

> *Photographie n° 1 - 08/04/2026 10:39:04 - 48.837548989289 -1.5679130147446.*

Le numéro de photographie est continu sur l'ensemble du document (pas de
remise à zéro par pièce). Il suit l'ordre d'apparition d'origine.

Quand deux ou trois photos sont présentées sur la même page, la légende est
posée sous chaque photo.

## Cas particulier — pièce avec absence d'élément

Si une pièce manque manifestement d'un élément attendu (ex. les deux portes du
salon ont été démontées, l'ampoule manque, le détecteur incendie a été
retiré), formuler à la rubrique Équipement avec :

- *« Absence de [élément] »*
- *« [Élément] dépourvu de [composant] »*
- *« [Composant] dépourvu du/de la [élément] »*

Exemples :

> *« Absence des deux portes (cuisine et entrée) »*
>
> *« Deux douilles dépourvues d'ampoules au plafond »*
>
> *« Socle de détecteur incendie dépourvu du détecteur »*
>
> *« Douille dépourvue d'ampoule au plafond »*

### Rubrique Mobilier (optionnelle)

À insérer **uniquement** quand Antoine a explicitement dicté du mobilier dans
le brouillon (cas typique : EDL d'entrée en location meublée). Format
identique à l'équipement : titre `Mobilier :` suivi d'une liste à puces avec
le caractère `●`.

Pour chaque meuble, indiquer :

1. **Type** (canapé, table, lit, armoire, commode, chaise, fauteuil, bureau, étagère…)
2. **Matériau et couleur** quand pertinent (chêne foncé, mélaminé blanc, simili-cuir noir…)
3. **Dimensions approximatives** quand pertinent (tiroirs, portes, places…)
4. **État factuel visible** (à l'état d'usage, dégradé, taché, déchiré, jaunissement…)

Exemples :

```
Mobilier :

  ● Canapé deux places en simili-cuir noir, à l'état d'usage
  ● Table basse en bois clair avec rayures sur le plateau
  ● Buffet deux portes battantes, mélaminé blanc, à l'état d'usage
```

**Si aucun meuble n'a été dicté pour la pièce, ne pas inscrire la rubrique
Mobilier.** Pour les EDL de sortie d'un logement vide (cas Manche Habitat
typique), cette rubrique sera systématiquement absente.

## Ordre des rubriques — INTANGIBLE

`Sol → Murs → Plafond → Équipement → Mobilier (optionnel)` dans cet ordre
exact, à chaque pièce, sans exception. **Ne jamais** inverser ni fusionner les
rubriques. Les seules omissions tolérées sont :

- Le **Plafond** pour les espaces extérieurs sans plafond visible (balcon, loggia, terrasse).
- Les **Murs** pour ces mêmes espaces extérieurs si le brouillon ne les décrit pas (cas du Balcon dans le PV de référence : seul le `Sol` est rempli).
- Le **Mobilier** s'il n'a pas été dicté.
