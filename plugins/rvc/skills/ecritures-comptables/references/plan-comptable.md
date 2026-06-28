# Plan de comptes du logiciel de gérance — SAS RVC IMMOBILIER

Source : export du logiciel métier (juin 2026). Utiliser ces numéros tels quels,
même quand ils s'écartent du PCG standard.

## Comptes existants

| N° | Intitulé | Type |
|---|---|---|
| 101300 | Capital social | Général |
| 108000 | Compte de l'exploitant | Général |
| 110000 | Reprise de soldes | Général |
| 417110 | Honoraires de gestion | Honoraires / produits |
| 417120 | Honoraires forfaitaires | Honoraires / produits |
| 417130 | Honoraires de suivi de travaux | Honoraires / produits |
| 417210 | Honoraires de location | Honoraires / produits |
| 417220 | Honoraires d'état des lieux | Honoraires / produits |
| 417230 | Honoraires d'entremise | Honoraires / produits |
| 417310 | Honoraires garantie des loyers | Honoraires / produits |
| 417320 | Honoraires assurances PNO | Honoraires / produits |
| 418100 | Frais de rédaction d'actes | Honoraires / produits |
| 418300 | Frais administratifs | Honoraires / produits |
| 419401 | Fournisseurs gérance | **Collectif fournisseurs** (rattacher ici les auxiliaires) |
| 419402 | Factures à payer gérance | Collectif |
| 419601 | Mandants (Encours) | Collectif mandants |
| 419602 | Charges conservées | Collectif mandants |
| 419603 | Taxes conservées | Collectif mandants |
| 419604 | Trop perçus | Collectif mandants |
| 419605 | Dépôts de garantie conservés | Collectif mandants avec bail |
| 419606 | Travaux | Collectif mandants |
| 419607 | Sinistres | Collectif mandants |
| 419800 | Clients en attente d'imputation | Compte d'attente |
| 419801 | Aides CAF | Général |
| 419802 | Prélèvements | Général |
| 419900 | Remises sur honoraires | Honoraires / produits |
| 445510 | TVA à décaisser | Général |
| 445660 | TVA déductible sur biens et services | Général |
| 445710 | TVA collectée | Général |
| 512000 | Banque Compte Fonctionnement | Trésorerie |
| 530000 | Compte caisse | Remise |
| 542000 | Banque Compte Affecté | Trésorerie |
| 542110 | Remises de chèques gérance | Remise |
| 580000 | Transfert de fonds | Général |
| 617100 | Frais bancaires | Charges |
| 627000 | Logiciels | Charges |
| 706101 | Honoraires de gestion | Produits |
| 706102 | Honoraires d'entrée | Produits |
| 706109 | Autres honoraires | Produits |
| 911000 | Locataires | Collectif baux |
| 913100 | Quittances à recouvrer | Technique |
| 913200 | Honoraires et frais à recouvrer | Technique |
| 913300 | Trop-perçu locataire à rembourser | Technique |

Attention aux pièges de ce plan : les comptes 4171xx/418xxx sont des comptes de
**produits d'honoraires** propres au logiciel (pas des clients PCG), et les comptes 9xxxxx
sont des comptes techniques de gérance — ne jamais les mouvementer pour la comptabilité
générale de la société. Le compte 542000 (Compte Affecté) reçoit les fonds mandants : les
relevés du compte de fonctionnement passent par 512000.

## Comptes à proposer quand la dépense l'exige

Numéros à 6 chiffres cohérents PCG, à faire créer dans le logiciel (onglet « Comptes à
créer » du livrable). Réutiliser exactement ces numéros d'un fichier à l'autre.

| N° proposé | Intitulé | Usage typique |
|---|---|---|
| 421000 | Personnel — rémunérations dues | Paiement des salaires nets |
| 425000 | Personnel — avances et acomptes | Acomptes sur salaire |
| 431000 | URSSAF | Cotisations URSSAF |
| 437100 | MALAKOFF HUMANIS — retraite | Retraite complémentaire |
| 437200 | CARCO | Caisse de retraite CARCO |
| 455100 | Compte courant d'associé — [nom] | Apports/retraits des associés (un compte par associé : 455100, 455200…) |
| 456100 | Associés — capital souscrit appelé non versé | Libération du capital |
| 606300 | Fournitures d'entretien et petit équipement | Petit matériel |
| 606400 | Fournitures administratives | Papeterie |
| 616000 | Assurances | Primes d'assurance |
| 618300 | Documentation | Documentation, abonnements pro |
| 622700 | Frais d'actes et de contentieux | Actes, formalités |
| 625100 | Voyages et déplacements | Train, péage, hôtel |
| 625700 | Réceptions | Restaurants, repas d'affaires |
| 626000 | Frais postaux et télécommunications | Téléphone, internet, timbres |
| 628100 | Cotisations professionnelles | Cotisations d'organismes professionnels |
| 641000 | Salaires bruts | Uniquement via journal de paie |
| 645000 | Charges sociales patronales | Uniquement via journal de paie |
| 471000 | Compte d'attente | Opérations inqualifiables en attendant la réponse de l'utilisateur |

Si une dépense ne correspond à rien de tout cela, proposer le compte PCG adapté
(classe 60 à 68 pour les charges) avec un numéro à 6 chiffres et l'ajouter à la liste.
