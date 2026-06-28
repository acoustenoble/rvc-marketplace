# Règles comptables et fiscales

## TVA — régime des débits

La société est à la TVA sur les débits : la TVA est déductible dès la facture, biens et
services confondus, via le compte 445660. La vraie difficulté n'est pas l'exigibilité mais
la **preuve** : la TVA n'est déductible que sur facture la mentionnant (art. 271 CGI). Un
relevé bancaire n'est pas une facture. D'où la règle des trois statuts :

- **Certaine** : la facture est fournie, ou le fournisseur figure dans la table des
  fournisseurs récurrents ci-dessous avec un taux établi. Ventiler HT / 445660 / TTC.
- **Présumée** : le taux est très probable (prestataire français assujetti classique →
  20 %) mais non prouvé. Ventiler quand même, et inscrire la ligne dans « Points à
  vérifier » avec la mention « confirmer sur facture ». L'utilisateur préfère une
  ventilation proposée et vérifiable à un TTC muet.
- **Sans TVA** : comptabiliser le TTC en charge. S'applique aux opérations exonérées,
  hors champ, ou dont la TVA n'est pas récupérable.

Cas à connaître :

- **Frais et cotisations bancaires** : exonérés de TVA (art. 261 C CGI) sauf option de la
  banque ; les cotisations type « Compte à composer » sont sans TVA → 617100 TTC.
  Les commissions sur mouvements/cartes peuvent être soumises : statut Présumée seulement
  si le libellé indique clairement une commission taxable.
- **Salaires, cotisations sociales, impôts** : hors champ, jamais de TVA.
- **Restaurants / réceptions** : TVA récupérable si facture au nom de la société, mais
  taux mixte (10 % nourriture, 20 % alcool) → statut Sans TVA par défaut, ligne en
  « Points à vérifier » pour récupération si facture disponible.
- **Carburant** : véhicule de tourisme = TVA récupérable à 80 % sur gazole/E85 et
  essence ; véhicule utilitaire = 100 % ; statut Présumée avec mention du prorata.
- **Cadeaux clients** : TVA récupérable seulement si ≤ 73 € TTC/an/bénéficiaire.
- **Trains (SNCF), péages d'autoroute** : transport de voyageurs = TVA non récupérable ;
  péages = récupérable sur reçu.
- Calcul : HT = TTC / 1,20 (ou 1,10 / 1,055), TVA = TTC − HT, arrondis à 2 décimales,
  l'écart d'arrondi s'impute sur le HT pour que HT + TVA = TTC exactement.

## Fournisseurs récurrents identifiés (relevés Crédit Agricole de l'étude)

| Libellé bancaire contient | Tiers / auxiliaire | Compte de charge | TVA |
|---|---|---|---|
| ORISHA PROPERTY MANAGEMENT | ORISHAPM | 627000 Logiciels | 20 % Certaine |
| ORISHA TRANSACTION | ORISHATR | 627000 Logiciels | 20 % Certaine |
| COTISATION / Offre Compte à composer | — (pas d'auxiliaire, charge directe) | 617100 | Sans TVA |
| FRAIS (banque), Facture Crédit Agricole | — | 617100 | Sans TVA (Présumée si commission taxable explicite) |
| URSSAF | URSSAF | 431000 (dette sociale, pas une charge) | Hors champ |
| MALAKOFF HUMANIS | MALAKOFF | 437100 | Hors champ |
| CARCO | CARCO | 437200 | Hors champ |
| Salaire / Acompte salaire + nom | — | 421000 (ou 425000 si « acompte ») | Hors champ |
| GROUPEMENT DES COMMI / GCJAI | GCJAI | 623100 Annonces et insertions — association du groupement des commissaires de justice qui publie les annonces de l'étude sur Leboncoin (confirmé 10/06/2026) | 20 % Certaine |
| SARL PAGESS | PAGESS | 622600 Honoraires — gestionnaire de paie, édite les bulletins (confirmé 10/06/2026) | 20 % Certaine |
| JMG | JMG | 622600 Honoraires — avocat de la société (a réalisé la constitution, fact. F2601202 ; confirmé 10/06/2026) | 20 % Présumée |
| SOUSCRIPTION + agence CA | — | 271000 Titres immobilisés — parts sociales Crédit Agricole souscrites par la société (confirmé 10/06/2026) | Sans TVA |
| Facture Crédit Agricole (mensuelle) | — | 617100 | Sans TVA (confirmé 10/06/2026) |
| LA DINETTE et autres restaurants | — | 625700 Réceptions | Sans TVA (cf. règle restaurants) |

Les trois associés de la SAS (R-V-C) et leurs comptes courants, confirmés le 10/06/2026 :
Florence ROIS (455300), Antoine COUSTENOBLE (455200), Mme SIMON VAUPRET (455100). Apport
initial de 9 000 € chacun en mars-avril 2026, déjà comptabilisé dans le livrable du relevé
2026 — ne pas les repasser. Le virement émis de 88,00 € du 21/04/2026 « remboursement
erreur compte » est volontairement en compte d'attente 471000 (l'utilisateur ne sait pas
encore ce que c'est) : demander s'il a été identifié.

Cette table s'enrichit : si l'utilisateur confirme un compte pour un fournisseur lors d'une
session, le mentionner pour qu'il puisse être ajouté ici.

## Schémas par nature d'opération

**Achat fournisseur (cas général)** — deux écritures :
AC : D 6xxxxx (HT) + D 445660 (TVA) / C 419401-AUX (TTC) ; puis
BQ : D 419401-AUX / C 512000 (TTC).

**Avoir ou remboursement fournisseur** (crédit sur le relevé venant d'un fournisseur) :
même schéma en sens inverse (AC : D 419401-AUX / C 6xxxxx + C 445660 ; BQ : D 512000 /
C 419401-AUX). C'est la contrepassation exacte de l'achat d'origine — mêmes comptes.

**Annulation de frais bancaires** (ex. « REDRESSEMENT FACTURATION » qui rembourse des
FRAIS du même montant) : BQ : D 512000 / C 617100. Rapprocher explicitement les deux
lignes dans les libellés.

**Salaire net payé** : BQ : D 421000 / C 512000. Acompte : D 425000. Ne jamais débiter
641000 depuis la banque : la charge (brut + patronales) vient du journal de paie (OD),
que l'on propose de passer si les bulletins sont fournis. Sans OD de paie, les comptes
421/431/437 présentent des soldes débiteurs — le signaler dans « Points à vérifier ».

**Cotisations sociales payées** (URSSAF, retraite) : BQ : D 431000/437xxx / C 512000.
Même logique : la charge 645xxx vient du journal de paie.

**Apport d'un associé en compte courant** (virement reçu d'un associé ou d'un proche
identifié) : BQ : D 512000 / C 455x00 (compte courant de l'associé concerné, un compte
par personne). Ne jamais créditer un compte de produit.

**Libération de capital** : BQ : D 512000 / C 456100, puis OD : D 456100 / C 101300 si la
souscription n'a pas déjà été constatée — vérifier le solde de 101300 et poser la question
plutôt que de doubler le capital. *Historique RVC : le capital