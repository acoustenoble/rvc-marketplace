# Templates — constat d'affichage

Toutes les formulations à trous. `[CROCHETS]` = à remplir. Modifier les
formulations **ici**, jamais dans le code.

## 1. En-tête juridique

```
PROCES-VERBAL DE CONSTAT
DE COMMISSAIRE DE JUSTICE


[BLOC DATES — une ligne par passage, en toutes lettres :]
L'AN [MILLÉSIME] ET LE [JOUR PASSAGE 1]
L'AN [MILLÉSIME] ET LE [JOUR PASSAGE 2]
L'AN [MILLÉSIME] ET LE [JOUR PASSAGE 3]


A LA DEMANDE DE :

[Bloc requérant identique au brouillon : forme juridique + dénomination
+ RCS + adresse du siège]


LAQUELLE M'EXPOSE CE QUI SUIT :        ← « LEQUEL » si requérant masculin

[Voir § 2]


DEFERANT A CETTE REQUISITION,

Nous SCP Florence ROIS, Mathilde VAUPRES, Antoine COUSTENOBLE, Commissaires de
Justice associés, titulaires des offices de SAINT-PAIR-SUR-MER, 181 rue Marie
Curie, AVRANCHES, 12 Place Carnot et de VIRE, 4 Rue René Chatel, l'un d'eux
soussigné


CERTIFIE M'ÊTRE RENDU CE JOUR, AUX DATES INDIQUEES EN TETE DE L'ACTE :

[ADRESSE DU TERRAIN], où là étant,
GPS : [LAT, LON]            [+ image carte de localisation]


J'AI PROCEDE AUX CONSTATATIONS SUIVANTES :
```

### Date en lettres
`L'AN DEUX-MILLE-VINGT-SIX ET LE DIX-NEUF MARS`. Millésime avec traits d'union,
tout en majuscules. Une ligne (`<w:br/>`) par passage, dans l'ordre
chronologique. Le **premier** passage = le plus ancien.

## 2. Introduction de la requête (entre EXPOSE et DEFERANT)

Accord de la civilité du requérant.

### Variante A — personne morale
> Qu'[elle] a obtenu de la mairie de [COMMUNE] une autorisation d'urbanisme.
>
> Qu'[elle] me requiert afin que je constate l'affichage régulier de cette
> dernière à l'adresse suivante : [ADRESSE DU TERRAIN], conformément aux
> articles A 424-15 et suivants du Code de l'Urbanisme et R 600-2 et R 424-15
> du même Code.

### Variante B / C — personne physique
Remplacer « Qu'elle » par « Qu'il » / « Qu'elle » selon le genre, et
« la société requérante » par « le requérant » / « la requérante » le cas
échéant.

### Détection civilité requérant
| Indice dans la dénomination | Civilité |
|---|---|
| `SARL`, `SAS`, `SASU`, `SA`, `SCI`, `EURL`, `Société`, `Établissement`, `Office`, `Habitat`, `Commune`, `Mairie` | Personne morale (A) |
| Commence par `Madame`, `Mme` | Femme (B) |
| Commence par `Monsieur`, `M.` | Homme (C) |
| Aucun marqueur clair | **Demander** |

## 3. Phrase d'ouverture des constatations

> Il est affiché sur place, aux dates indiquées en tête de l'acte, un panneau
> rectangulaire visible et lisible depuis la voie publique, dont les dimensions
> sont supérieures à 80 centimètres de haut et à 80 centimètres de large.
>
> Sur ce panneau, outre les mentions publicitaires, je relève les mentions
> suivantes :

## 4. Mentions du panneau — format à libellés gras

Chaque mention sur sa propre ligne, **libellé en gras** (suivi de « : valeur »).
Ordre réglementaire (art. A424-16). Adapter selon les mentions réellement
portées (toutes ne sont pas toujours présentes) :

```
BÉNÉFICIAIRE : [valeur]
NOM DE L'ARCHITECTE AUTEUR DU PROJET ARCHITECTURAL : [valeur]
DATE DE DÉLIVRANCE : [valeur]
N° : [PC/PA/PD/DP n° …]
NATURE DU PROJET : [valeur]
SUPERFICIE DU TERRAIN : [valeur] m²
ADRESSE DE LA MAIRIE OÙ LE DOSSIER PEUT ÊTRE CONSULTÉ : [valeur]
SURFACE DE PLANCHER — À CRÉER : [valeur] m²  /  À DÉMOLIR : [valeur]
HAUTEUR DE LA CONSTRUCTION (en mètres par rapport au terrain naturel) : [valeur]
```

> Le script `scripts/format_mentions.py` met automatiquement le libellé (texte
> avant le premier « : » de chaque ligne) en gras.

### Encadré « Chantier interdit au public »
Encadré bordé, texte centré en gras :
```
┌─────────────────────────────────────────┐
│        CHANTIER INTERDIT AU PUBLIC        │
└─────────────────────────────────────────┘
```

### Encadré « Droit de recours »
Précédé de : *« Le panneau mentionne également : »*, puis encadré bordé :
> **Droit de recours**
> Le délai de recours contentieux est de deux mois. Il court à compter du
> premier jour d'une période continue de deux mois d'affichage du présent
> panneau sur le terrain (article R. 600-2 du Code de l'urbanisme). À peine
> d'irrecevabilité, tout recours — administratif ou contentieux — doit être
> notifié à l'auteur de la décision ainsi qu'au bénéficiaire du permis ou de la
> décision prise sur la déclaration préalable. Cette notification s'effectue par
> lettre recommandée avec accusé de réception, dans un délai de quinze jours
> francs à compter du dépôt du recours (article R. 600-1 du Code de
> l'urbanisme).

## 5. Photographies par passage (cœur de l'adaptation multi-passages)

Après la description du panneau et l'encadré recours, une phrase d'introduction :

> Photographies effectuées aux dates ci-dessous indiquées du panneau visible
> depuis la voie publique ou un espace privé ouvert au public :

Puis **un `Heading1` par passage**, avec saut de page, dans l'ordre
chronologique. **Règle figée : rappeler la date du passage en clair juste sous
le titre** (paragraphe `HOParagraphe`, ex. « Le 19 mars 2026 ») :

```
[Heading1]  1er passage
Le 19 mars 2026
[Photo(s) du passage avec leur légende horodatée / GPS]

[Heading1]  2ème passage
Le 29 avril 2026
[Photo(s)]

[Heading1]  3ème passage
Le 8 juin 2026
[Photo(s)]
```

Règles :
- La **description du panneau n'est faite qu'une fois** (avant les passages).
- La date sous chaque titre est reprise des **dates en tête de l'acte**, dans
  l'ordre chronologique (1er passage = date la plus ancienne). **Ne pas** se
  fier à l'horodatage EXIF des photos, qui correspond parfois à la date
  d'upload et peut diverger : en cas d'incohérence manifeste entre l'EXIF d'une
  photo et le passage auquel elle est rattachée, **le signaler à Antoine**.
- Chaque passage ne contient que **ses** photographies, conservées telles
  quelles (légende, horodatage, GPS).
- Si une photo est une **vue de la rue** (panneau dans son environnement) et une
  autre un **gros plan** (panneau lisible), les conserver dans l'ordre du
  brouillon ; on peut préfixer la légende par *« Vue depuis la rue »* /
  *« Gros plan du panneau »* uniquement si Antoine le valide.

## 6. Conclusion

> Telles sont les constatations faites aux jours indiqués en tête du présent
> acte au [ADRESSE DU TERRAIN], 