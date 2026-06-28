# Règles cardinales — état des lieux

Ces règles régissent **toute** réécriture d'un brouillon d'EDL. Elles dérivent
de la valeur probatoire d'un procès-verbal de constat : un constat qui
contient une interprétation, une conclusion ou une inférence causale perd sa
valeur devant un tribunal.

## Règle 1 — Strictement descriptif

Le constat décrit ce que **l'œil observe**, rien d'autre.

- ✅ *« Tapisserie déchirée à multiples endroits, trous de chevilles »*
- ❌ *« Le locataire a manifestement maltraité les murs »*
- ❌ *« Tapisserie ancienne et abîmée, à refaire »*

Le commissaire de justice **constate**. Il ne **juge** pas. Il ne **conclut**
pas. Il ne **prescrit** pas.

## Règle 2 — Aucun lien de causalité

Ne jamais écrire : *« dû à »*, *« causé par »*, *« provenant de »*,
*« résultant de »*, *« en raison de »*, *« faute de »*…

- ✅ *« Receveur en très mauvais état, joints noircis, trous de chevilles »*
- ❌ *« Receveur dégradé en raison d'un défaut d'entretien »*
- ❌ *« Joints noircis du fait de moisissures »*

Si la cause d'un désordre est visible et indéniable (ex. fientes de pigeons
sur un balcon), décrire la cause **et** sa conséquence séparément, sans les
relier par un lien causal.

## Règle 3 — Périmètre strict du brouillon

**Le brouillon dicté par Antoine délimite le périmètre des constatations.**

- Les photos servent à **préciser** (matériau exact, défaut visible, marque)
  et à **corriger** les erreurs de dictée vocale.
- Les photos ne servent **pas** à introduire des éléments d'équipement ou des
  défauts qu'Antoine n'a pas dictés.

**Exemple** : si le brouillon dit *« quatre prises électriques »* et que la
photo en montre cinq, **rester sur quatre** (ou demander à Antoine).

**Exemple** : si la photo montre un défaut visible (fissure) qui n'est pas
mentionné au brouillon, **ne pas l'ajouter**. Antoine décidera après lecture
s'il faut le compléter.

## Règle 4 — Doute = abstention

Si le skill n'est pas certain à 100 % d'une lecture (matériau ambigu,
caractère illisible sur une étiquette, marque non identifiable, état entre
deux qualifications), **ne pas l'inscrire**.

- ✅ *« Linoléum dégradé »*
- ❌ *« Linoléum ou dalles PVC, état dégradé »* (le skill hésite — il doit
  trancher ou s'abstenir).

Quand l'hésitation porte sur une donnée que le skill ne peut pas trancher
seul (civilité d'une personne, lecture d'un index de compteur), **demander
à Antoine** plutôt que d'inventer.

## Règle 5 — Vocabulaire technique

Utiliser le vocabulaire technique du métier, pas la langue courante.

- ✅ *« Toile à peindre »*, ❌ *« papier blanc »*
- ✅ *« Tête thermostatique »*, ❌ *« bouton du radiateur »*
- ✅ *« Trous de chevilles »*, ❌ *« petits trous »*
- ✅ *« Joints dégradés »*, ❌ *« joints qui font sale »*
- ✅ *« Ouvrant et fermant correctement »*, ❌ *« qui marche bien »*

Voir `vocabulary.md` pour le lexique complet.

## Règle 6 — Civilité explicite, jamais supposée

- Le **requérant** : sa civilité (Le / La / La société) est déterminée par sa
  dénomination (cf. `templates.md` § 2). En cas d'ambiguïté, **demander**.
- Le **locataire** : sa civilité (Monsieur / Madame / Madame et Monsieur)
  doit être reprise telle qu'elle figure dans le brouillon. Si elle est
  absente, **demander**.
- Ne jamais supposer un genre sur la base d'un prénom seul (Camille,
  Dominique, Claude, Frédérique…).

## Règle 7 — Ordre des rubriques INTANGIBLE

Pour chaque pièce : `Sol → Murs → Plafond → Équipement → Mobilier (si dicté)`.

Aucune liberté de réordonnancement à l'intérieur d'une pièce.

## Règle 8 — Ordre des pièces selon la logique d'Antoine

L'ordre est imposé (cf. `SKILL.md` étape 7) :

```
1. Convocation
2. Entrée / Couloir
3. Pièces de vie (Salon, Salle à manger, Séjour)
4. Cuisine + annexes attenantes (Séchoir, Cellier)
5. Pièces d'eau (Salle de bain ou Salle de douche, WC)
6. Chambres
7. Annexes (Balcon, Placard, Cave, Garage)
8. Compteurs
9. Boîte aux lettres
10. Clés
```

Si le brouillon présente les pièces dans un ordre différent, **réordonner**.

## Règle 9 — Photos : ordre et légende préservés

Les photos d'une pièce sont conservées **dans leur ordre d'apparition** dans
le brouillon, avec leur légende horodatée intacte (numéro / date / heure /
GPS).

La numérotation des photographies est continue sur l'ensemble du document
(`Photographie n° 1` à `Photographie n° N`), pas remise à zéro par pièce.

Si le réordonnancement des pièces change la position de certaines photos,
**renuméroter** les photographies pour que la numérotation reste continue
dans l'ordre du document final.

## Règle 10 — Aucune conclusion finale

La conclusion est la phrase fixe :

> *« Telles sont les constatations faites ce jour au [adresse] de tout quoi
> j'ai dressé et rédigé le présent procès-verbal de constat, avec
> photographies pour servir et valoir ce que de droit. »*

**Aucune** synthèse globale, aucun bilan, aucune recommandation.

## Règle 11 — Préservation de l'en-tête juridique

Bloc fixe (`PROCES-VERBAL DE CONSTAT DE COMMISSAIRE DE JUSTICE`, mention
`L'AN …`, bloc `A LA DEMANDE DE`, bloc `DEFERANT À CETTE REQUISITION`,
mention `ME SUIS RENDU CE JOUR`, page de garde RVC, signature) :

- **Page de garde RVC** : préservée à l'identique.
- **Signature finale** : préservée à l'identique (avec cachet).
- **Bloc DEFERANT À CETTE REQUISITION** : phrase fixe RVC, conservée mot pour mot.
- **Bloc A LA DEMANDE DE** : reprendre l'identification du bailleur depuis le brouillon, sans la modifier sauf coquille évidente.
- **Bloc ME SUIS RENDU CE JOUR** : reprendre l'adresse + la personne présente (si présence) + GPS + carte (si présents dans le brouillon).

Seuls **deux blocs** sont rédigés par le skill :

1. L'**introduction de la requête** (entre `LEQUEL M'EXPOSE` et `DEFERANT`).
2. La **section Convocation**.

Le reste du squelette juridique est repris du brouillon ou du modèle RVC.

## Règle 12 — Renommage de pièce uniquement pour fautes/casse

Le skill peut **corriger** un titre de pièce en cas de :

- Faute de frappe (`Cuisne` → `Cuisine`, `Sechoir` → `Séchoir`).
- Casse incorrecte (`salle de douche` → `Salle de douche`, `Wc` → `WC`).
- Espacement incorrect (`Entrée/Couloir` → `Entrée / Couloir`).

Le skill **ne peut pas** :

- Renommer une pièce vers un type différent (`Pièce 1` → `Bureau`, sauf si Antoine l'indique explicitement).
- Fusionner deux pièces du brouillon en une seule.
- Scinder une pièce du brouillon en deux.

En cas d'ambiguïté sur un titre, **demander**.
