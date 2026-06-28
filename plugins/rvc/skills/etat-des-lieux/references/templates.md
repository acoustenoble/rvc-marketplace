# Templates — état des lieux

Ce fichier centralise toutes les formulations à trous utilisées pour générer
l'EDL. Toute évolution de ces templates doit être faite ici (pas dans les
scripts), pour que le skill reste contrôlable par Antoine sans toucher au code.

## 1. En-tête juridique du constat

Bloc fixe (page 3 du PV de référence). Tous les éléments en `[CROCHETS]` sont à
remplir.

```
PROCES-VERBAL DE CONSTAT
DE COMMISSAIRE DE JUSTICE


L'AN [DATE EN LETTRES]


A LA DEMANDE DE :

[Bloc bailleur identique au brouillon : forme juridique + dénomination
+ RCS + adresse]


LEQUEL M'EXPOSE CE QUI SUIT :

[Voir § 2 — introduction de la requête]


DEFERANT A CETTE REQUISITION :

Nous SCP Florence ROIS, Mathilde VAUPRES, Antoine COUSTENOBLE,
Commissaires de Justice associés, titulaires des offices de
SAINT-PAIR-SUR-MER, 181 rue Marie Curie, AVRANCHES, 12 Place Carnot et
de VIRE, 4 Rue René Chatel, l'un d'eux soussigné


ME SUIS RENDU CE JOUR :

[ADRESSE DU LOGEMENT], où là étant, [SI PRÉSENCE : et en présence de
CIVILITÉ NOM, QUALITÉ]
```

### Date en lettres

Format : `L'AN DEUX-MILLE-VINGT-SIX ET LE HUIT AVRIL`

Le millésime et le jour sont en toutes lettres en majuscules, le mois est en
minuscules dans la source RVC mais en majuscules dans cet exemple — **suivre la
casse du modèle fourni** (majuscules partout). Trait d'union sur le millésime
(`DEUX-MILLE-VINGT-SIX`).

Ne pas inscrire le mois en chiffres (« 04 ») ni le jour en chiffres (« 8 »).

## 2. Introduction de la requête (entre LEQUEL M'EXPOSE et DEFERANT)

Template à 2 phrases, accord de la civilité du requérant en première position.

### Variante A — personne morale (société, EPIC, SCI, OPH, association…)

> Que **la société requérante** a donné à bail d'habitation principale à
> [CIVILITÉ + IDENTITÉ DU LOCATAIRE] en date du [DATE DU BAIL], un logement sis
> [ADRESSE COMPLÈTE].
>
> Que je suis mandaté pour dresser l'état des lieux [d'entrée | de sortie].

### Variante B — personne physique femme

> Que **la requérante** a donné à bail d'habitation principale à
> [CIVILITÉ + IDENTITÉ DU LOCATAIRE] en date du [DATE DU BAIL], un logement sis
> [ADRESSE COMPLÈTE].
>
> Que je suis mandaté pour dresser l'état des lieux [d'entrée | de sortie].

### Variante C — personne physique homme

> Que **le requérant** a donné à bail d'habitation principale à
> [CIVILITÉ + IDENTITÉ DU LOCATAIRE] en date du [DATE DU BAIL], un logement sis
> [ADRESSE COMPLÈTE].
>
> Que je suis mandaté pour dresser l'état des lieux [d'entrée | de sortie].

### Détection automatique de la civilité du requérant

Heuristique à appliquer sur la dénomination du bailleur extraite du brouillon :

| Indice dans la dénomination                                                                      | Civilité retenue   |
|--------------------------------------------------------------------------------------------------|--------------------|
| Contient `SARL`, `SAS`, `SA`, `SCI`, `EURL`, `SASU`, `OPH`, `EPIC`, `Établissement public`, `Association`, `Société`, `Office`, `Habitat`, `Immobilière` | Personne morale (A) |
| Commence par `Madame `, `Mme `                                                                  | Femme (B)          |
| Commence par `Monsieur `, `M. `                                                                 | Homme (C)          |
| Aucun marqueur clair                                                                            | **Demander**       |

### Date du bail

Format conservé tel quel depuis le brouillon (ex. `29/07/2021`). Si non
mentionnée dans le brouillon, demander à Antoine.

### Adresse du logement

Reprendre exactement la formulation du brouillon (numéro d'appartement, numéro
de rue, voie, code postal, ville). Corriger les fautes de dictée évidentes
(`si 7 les Peupliers` → `sis 7 les Peupliers`, `Hlm` → `HLM`…) mais ne pas
réinterpréter la voie.

## 3. Section Convocation (§ 1 du corps des constatations)

Toujours numérotée **1** et toujours placée juste après la mention
« J'AI PROCEDE AUX CONSTATATIONS SUIVANTES : ».

### Variante 1 — AR signé

> **1 Convocation**
>
> Que le locataire a été convoqué par lettre recommandée avec demande d'avis de
> réception signée le [DATE AR] et par lettre simple en date du [DATE ENVOI].

### Variante 2 — Pli revenu non réclamé

> **1 Convocation**
>
> Que le locataire a été convoqué par lettre recommandée avec demande d'avis de
> réception, dont le pli est revenu non réclamé, et par lettre simple en date
> du [DATE ENVOI].

### Variante 3 — Pas encore de retour de la poste

> **1 Convocation**
>
> Que le locataire a été convoqué par lettre recommandée avec demande d'avis de
> réception et par lettre simple en date du [DATE ENVOI].

### Format des dates de convocation

`JJ/MM/AAAA` (ex. `30/03/2026`) — format numérique avec barres obliques,
identique au modèle du PV de référence.

## 4. Phrases d'accès aux pièces (optionnelles)

Quand une pièce n'est pas accessible directement depuis le couloir/l'entrée
mais depuis une autre pièce, ouvrir la rubrique par une phrase d'accès courte.
Cette phrase doit figurer dans le brouillon ou être déductible sans ambiguïté
de la disposition du logement.

Modèles validés :

- *« J'accède au [PIÈCE] depuis [PIÈCE PRÉCÉDENTE] »* (ex. *« J'accède au séchoir depuis la cuisine »*).
- *« J'accède au [PIÈCE] depuis [PIÈCE PRÉCÉDENTE] par une porte »* (variante avec porte intermédiaire).
- *« J'accède au [PIÈCE] depuis [PIÈCE PRÉCÉDENTE] par une porte-fenêtre »* (variante balcon / loggia).
- *« J'accède au [PIÈCE] [POSITION] en entrant »* (ex. *« J'accède au placard à gauche en entrant »*).

Pour les pièces accessibles directement depuis le couloir (Cuisine, WC, Salle
de douche, Chambre 1, Chambre 2…), **ne pas** ajouter de phrase d'accès — la
pièce démarre directement par `Sol : …`.

## 5. Section Compteurs

Format strict (toujours présent en fin de logement, avant Boîte aux lettres).

```
12 Compteurs

  ● Compteur électrique : [INDEX] kWh
  ● Compteur d'eau froide : [INDEX] m³
  [● Compteur d'eau chaude : [INDEX] m³ — si présent]
  [● Compteur de gaz : [INDEX] m³ — si présent]

[Photographies des compteurs avec leur légende]
```

Les puces sont des points centrés `●` (U+25CF), pas des tirets ni des bullets
Word standard. Le numéro de section (12 dans l'exemple) est généré
automatiquement par la numérotation Word (`numId=3` sur Titre11).

## 6. Section Boîte aux lettres

Texte libre court, factuel.

```
13 Boîte aux lettres

[1 ou 2 phrases descriptives factuelles : localisation, état, présence/absence
de clé, étiquette, traces d'adhésif…]

[Photographie de la boîte aux lettres]
```

Exemple validé :

> *« Boîte aux lettres accessible depuis les parties communes, traces d'adhésif
> sur la façade métallique, absence de clé »*

## 7. Section Clés

Toujours en dernier, juste avant la conclusion.

```
14 Clés

  ● [QUANTITÉ] [TYPE]
  ● [QUANTITÉ] [TYPE]
  ● [...]
```

Exemples de types validés :

- `2 badges`
- `3 clés de logement`
- `3 clés de porte PVC de la cuisine`
- `1 clé de boîte aux lettres`
- `1 clé de cave`
- `1 clé de garage`

## 8. Conclusion (après la section Clés)

Phrase fixe, italique gras, centrée à droite avec la signature en dessous.

```
Telles sont les constatations faites ce jour au [ADRESSE COMPLÈTE DU
LOGEMENT] de tout quoi j'ai dressé et rédigé le présent procès-verbal de
constat, avec photographies pour servir et valoir ce que de droit.


                                              Commissaire de Justice
                                              Maître Antoine COUSTENOBLE

[Cachet de l'étude]
```

L'adresse reprise ici est l'adresse exacte qui figure dans la mention « ME
SUIS RENDU CE JOUR » en début de document.

## 9. Format du fichier de sortie

Convention de nommage **obligatoire** :

```
PV CONSTAT <NOM CLIENT> date <JJ.MM.AAAA>.docx
```

- `<NOM CLIENT>` : nom du bailleur requérant en majuscules, sans forme juridique (`MANCHE HABITAT`, pas `EPIC MANCHE HABITAT`). Pour une personne physique, le nom de famille seul.
- `<JJ.MM.AAAA>` : date du constat avec points séparateurs.

Exemples :

- `PV CONSTAT MANCHE HABITAT date 08.04.2026.docx`
- `PV CONSTAT DUPONT date 15.05.2026.docx`
