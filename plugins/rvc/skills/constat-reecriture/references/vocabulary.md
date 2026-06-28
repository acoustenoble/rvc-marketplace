# Vocabulaire validé et corrections

Journal vivant des préférences terminologiques d'Antoine. **À consulter systématiquement avant une réécriture et à enrichir après chaque constat.**

## Source terminologique principale

Dictionnaire du bâtiment : `/sessions/inspiring-relaxed-cori/mnt/Agent Constat/publication (1).pdf`

Ce PDF contient le vocabulaire technique que Antoine souhaite voir utilisé : matériaux, composants, typologies de désordres, éléments d'ouvrage. **À consulter dès qu'un doute terminologique surgit** (plutôt que d'inventer ou de chercher ailleurs).

---

## Corrections et préférences établies

### Parties communes d'immeuble

- **Boîtes aux lettres** : si Antoine n'en précise pas l'habillage, **ne pas le décrire**. Ne pas inférer « stratifié imitation bois » même si cela semble visible sur photo.
- **Portes de placards techniques / gaines techniques dans un couloir d'immeuble** : ne pas supposer qu'elles sont métalliques. Sauf précision explicite d'Antoine, **ne pas décrire leur matériau ni leur couleur**.
- **Accès aux caves dans un constat de copropriété** : c'est généralement **la demanderesse qui ouvre sa propre cave**. Toujours vérifier le nom contre la liste des demandeurs avant d'écrire un nom étranger.

### Tournures récurrentes d'Antoine

- **« Présence de X sur d'importants pans »** : signifie que X (tache, humidité, désordre) couvre d'importants pans d'une surface. **Ne PAS lire cela comme « X est partiellement absent » ou « arrachement »**.

### Reformulations de scories de dictée vocale

- **« Leurs de spongique »** → « spongieux » / « aspect spongieux » selon contexte.
- **« Facturiez RUAULT »** (et variantes similaires) → scorie typique dans la zone d'introduction ; à supprimer et remplacer par la rédaction d'introduction (règle 16).
- **« Untegar. »** (ou autres pseudo-mots isolés en fin de paragraphe) → scorie de reconnaissance vocale ; à supprimer.

### Coquilles de titres récurrentes

- « Vmc » → « **VMC** »
- « Nuissances » → « **Nuisances** »
- « Lesions » → « **Lésions** »

La liste est encodée dans `scripts/correct_titles.py` et s'enrichit au fil des constats.

---

## Règle méta

**Why** : Antoine est responsable du contenu juridique de son constat. Ajouter des observations non formulées par lui = risque d'introduire des éléments qu'il n'a pas réellement constatés lui-même au moment du constat.

**How to apply** : à chaque réécriture, se demander pour chaque ajout de détail :
> *« Est-ce une précision technique sur ce qu'Antoine a décrit, ou est-ce une observation nouvelle ? »*

Si observation nouvelle → **ne pas écrire**.

---

## Comment enrichir ce fichier

Après chaque constat, si une nouvelle préférence est validée (ou si Antoine corrige un choix terminologique), ajouter une entrée dans la section correspondante ci-dessus. Format :

```
### <Contexte / type d'élément>
- **<élément>** : <règle ou préférence>.
```

Dater les entrées si la règle est propre à un constat ou à une période (ex. *Corrections du 2026-04-20 — constat RUAULT/TANGUY*).


---

## Constats « ossature bois » / chantiers (humidité, moisissures)

*Corrections du 2026-06-15 — constat CENTRE HOSPITALIER SAINT-JAMES*

### Scories de reconnaissance vocale (à supprimer)
- **« This is »**, **« Did you ? »**, **« Israël »**, **« Nantes »**, **« citadelle »** : débuts/incrustations parasites → supprimer.
- **« lunes »**, **« l'une »** employé comme localisant flou → relire selon le contexte (souvent « l'aile » → « la maisonnée »).

### Reformulations techniques validées
- **« aile »** / **« elle »** (désignation d'une unité du bâtiment) → **« maisonnée »**.
- **« saturbois »**, **« seturbois »**, **« mur de Saturne »**, **« eau saturée »** (contexte structure) → **« ossature bois »**.
- **« phobes »**, **« fobes »** → **« façades »**.
- **« montants en placo »** → **« montants en plaque de plâtre »**.

### Doutes terminologiques à signaler (ne pas trancher seul)
- **« pare-feu » vs « pare-vapeur »** : si la dictée hésite, harmoniser sur le terme dominant MAIS le signaler à Antoine pour validation.
- **Pathogène nommé (mérule, etc.)** : ne jamais l'affirmer ; le rendre comme une **déclaration** (règle 27) et le faire confirmer.

### Désordres — vocabulaire descriptif
- Bois atteint : « montants **piquetés** », « **taches noirâtres / verdâtres / brunâtres** », « **traces fongiques** », « formations **de type fongique** », « **spores** ».
- Membrane : « taches qui **transpirent / apparaissent à travers le pare-vapeur** » (en l'absence de dépose).
- Opérations : « **dépose** » (pare-vapeur, isolant), « **carottage** ».
