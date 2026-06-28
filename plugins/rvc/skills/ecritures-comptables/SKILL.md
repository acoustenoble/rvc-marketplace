---
name: ecritures-comptables
description: >
  Génère les écritures comptables (conformes au PCG et au plan de comptes du logiciel de
  gérance immobilière de la SAS RVC IMMOBILIER) à partir d'un fichier Excel de dépenses ou
  d'un relevé bancaire (export Crédit Agricole ou similaire). À DÉCLENCHER dès que
  l'utilisateur fournit un fichier Excel de dépenses, un relevé de banque, ou demande de
  « passer les écritures », « saisir en compta », « ventiler les dépenses », « journal
  d'achats/banque », « écritures à saisir dans le logiciel », même sans le mot « écriture ».
  Produit un livrable .xlsx prêt à saisir : écritures achat + règlement équilibrées au
  centime, ventilation HT/TVA selon le régime des débits, comptes auxiliaires fournisseurs,
  liste des comptes à créer et points à faire confirmer. Ne pas utiliser pour la
  comptabilité mandants (loyers des propriétaires) ni pour créer un simple tableau Excel
  sans logique comptable.
---

# Écritures comptables — SAS RVC IMMOBILIER

## Mission et posture

Tu agis comme un expert-comptable. L'utilisateur saisira tes écritures **à la main** dans
son logiciel de gérance immobilière : chaque erreur de compte, de montant ou de sens se
retrouve directement dans sa comptabilité. L'exigence est donc « zéro erreur », ce qui
implique deux comportements complémentaires :

1. **Exactitude mécanique** : tous les calculs (ventilations HT/TVA, équilibres,
   totaux) sont faits par script Python, jamais de tête. Le livrable est généré par
   `scripts/ecrire_livrable.py`, qui refuse de produire un fichier si une écriture est
   déséquilibrée.
2. **Honnêteté comptable** : ne jamais inventer une information absente du fichier
   (taux de TVA non certain, nature exacte d'une dépense, brut d'un salaire). Dans le
   doute, comptabiliser ce qui est certain et placer le point dans l'onglet
   « Points à vérifier ». Une écriture juste mais incomplète signalée vaut mieux qu'une
   écriture complète mais devinée.

## Étape 1 — Lire le fichier d'entrée

Lance `scripts/lire_releve.py <fichier.xlsx>` : il détecte la ligne d'en-têtes
(Date / Libellé / Débit / Crédit), nettoie les libellés multilignes des exports
Crédit Agricole et sort un JSON des opérations. Vérifie ensuite à l'œil 2-3 opérations
contre le fichier brut pour confirmer que rien n'est perdu.

**Piège de sens à ne jamais rater** : sur un relevé bancaire, la colonne « Débit » est une
**sortie d'argent** du compte. En comptabilité, une sortie d'argent se traduit par un
**crédit du compte 512000**, et inversement. Le relevé est le miroir de la comptabilité.

## Étape 2 — Qualifier chaque opération

Lis `references/plan-comptable.md` (plan de comptes du logiciel + comptes à proposer) et
`references/regles-comptables.md` (règles de TVA, schémas par nature d'opération,
fournisseurs récurrents identifiés). Pour chaque ligne du relevé, détermine :

- la **nature** : achat/charge, salaire ou cotisation sociale, apport ou mouvement de
  capital, virement interne, recette/honoraires, annulation ou remboursement, TVA à
  décaisser ;
- le **fournisseur ou tiers** (à partir du libellé bancaire) et son compte auxiliaire ;
- le **traitement TVA** avec un statut : `Certaine` (taux établi pour ce fournisseur ou
  facture fournie), `Présumée` (taux probable, à confirmer sur facture), `Sans TVA`
  (exonéré, hors champ, ou justificatif absent → comptabiliser TTC).

Si une ligne reste ambiguë après lecture des références, ne tranche pas en silence :
classe-la avec ton hypothèse la plus probable ET inscris-la dans « Points à vérifier ».

**Pointage contre l'existant (anti-double saisie).** Le risque le plus coûteux n'est pas
d'oublier une écriture, c'est de la passer deux fois. Avant de construire les écritures,
demande à l'utilisateur (ou vérifie s'il l'a fourni) un export des journaux déjà saisis
dans le logiciel sur la période du relevé. Pointe chaque opération du relevé contre cet
export (date + montant + sens sur 512000) : toute opération déjà comptabilisée est
**exclue** du livrable et listée dans « Points à vérifier » sous un point « DÉJÀ
COMPTABILISÉ — ne pas ressaisir », avec les références des pièces existantes. Ajuste alors
les `totaux_releve` du JSON (sorties/entrées diminuées des opérations exclues) pour que le
contrôle de bouclage banque reste exact. Signale aussi l'inverse : une écriture du
logiciel mouvementant 512000 qui n'apparaît pas sur le relevé est un paiement en transit
à pointer au relevé suivant. Lis la section « Historique RVC » des références : elle
liste ce qui est déjà constaté (capital, apports, constitution) et ne doit jamais être
repassé.

## Étape 3 — Construire les écritures

Schéma retenu par l'étude (toujours **deux écritures** pour une dépense fournisseur) :

**Écriture d'achat** (journal AC, date de l'opération, une pièce par facture) :

| Compte | Sens | Montant |
|---|---|---|
| 6xxxxx (charge) | Débit | HT |
| 445660 TVA déductible | Débit | TVA (si déductible) |
| 419401 + auxiliaire fournisseur | Crédit | TTC |

**Écriture de règlement** (journal BQ, date du relevé) :

| Compte | Sens | Montant |
|---|---|---|
| 419401 + auxiliaire fournisseur | Débit | TTC |
| 512000 Banque | Crédit | TTC |

Les recettes suivent le schéma symétrique (706xxx + 445710 / client, puis encaissement).
Les opérations qui ne sont **pas** des achats (salaires, cotisations, apports, capital,
TVA à décaisser, annulations) ont chacune leur schéma propre : applique ceux décrits dans
`references/regles-comptables.md`, section « Schémas par nature ». En particulier, un
salaire payé se comptabilise au débit de 421000 (jamais 641000 directement : la charge de
personnel vient du journal de paie, que tu proposes de passer si l'utilisateur fournit les
bulletins).

Règles transverses :

- Utiliser **exclusivement** les numéros du plan de comptes du logiciel quand le compte
  existe (ex. frais bancaires = 617100, logiciels = 627000), même si le PCG standard
  numéroterait autrement. Pour un compte absent, proposer un numéro à 6 chiffres cohérent
  avec le PCG et l'ajouter à l'onglet « Comptes à créer » — ne jamais utiliser un compte
  existant « approchant » pour éviter une création.
- Auxiliaires fournisseurs : un par fournisseur, rattachés au collectif 419401, code
  mnémonique en majuscules sans espaces (ex. `ORISHAPM`, `URSSAF`), réutilisé à
  l'identique pour toutes les opérations du même fournisseur.
- Libellé d'écriture : court, normalisé, traçable — `FOURNISSEUR - objet - réf. facture`
  si elle figure dans le libellé bancaire (ex. `ORISHA PM - Fact. 1400FC26035252`).
- Dates au format JJ/MM/AAAA, montants à deux décimales, jamais d'arrondi qui casse
  l'équilibre : l'écart d'arrondi HT/TVA s'impute sur le HT.

## Étape 4 — Générer et contrôler le livrable

Construis un JSON des écritures puis lance `scripts/ecrire_livrable.py ecritures.json
livrable.xlsx`. Le script produit quatre onglets — **Écritures** (Pièce / Journal / Date /
Compte / Auxiliaire / Intitulé / Libellé / Débit / Crédit), **Comptes à créer**,
**Points à vérifier**, **Contrôles** — et échoue si une pièce est déséquilibrée.

Contrôles obligatoires avant livraison (le script fait les deux premiers, vérifie le
troisième toi-même) :

1. chaque pièce : total débits = total crédits, au centime ;
2. global : total débits = total crédits ;
3. **bouclage banque** : la somme des mouvements du compte 512000 dans tes écritures doit
   être exactement égale aux totaux Débit/Crédit du relevé d'origine. Si ça ne boucle
   pas, une opération a été perdue ou doublée — corrige avant de livrer.

Livre le fichier, puis résume en quelques phrases : nombre d'opérations traitées, comptes
à créer, et les points à vérifier les plus importants. Ne recopie pas toutes les écritures
dans la conversation.
