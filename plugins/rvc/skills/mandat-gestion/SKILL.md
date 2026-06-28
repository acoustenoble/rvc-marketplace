---
name: mandat-gestion
description: >
  Génère un MANDAT DE GESTION (gérance / gestion locative) à la charte de
  RVC IMMOBILIER, département immobilier d'une étude de commissaires de justice.
  Produit un fichier .docx prêt à compléter et à signer, à partir des
  informations du dossier fournies dans la discussion (propriétaire/mandant,
  désignation du bien, conditions de location, honoraires). À DÉCLENCHER dès que
  l'utilisateur demande un « mandat de gestion », un « mandat de gérance », un
  « mandat de gestion locative », d'établir/rédiger un mandat pour confier un
  bien en gestion, ou donne les coordonnées d'un propriétaire et d'un bien à
  gérer en vue d'un mandat. Utiliser même si l'utilisateur ne dit pas
  explicitement « rédige le mandat » : toute demande de mise sous gestion d'un
  bien pour le compte d'un propriétaire déclenche ce skill. Ne pas confondre
  avec 'etat-des-lieux', 'constat-reecriture' ni 'estimation-immobiliere'.
---

# Mandat de gestion RVC — génération du .docx

Ce skill produit un **mandat de gestion (gérance locative)** au format Word
(.docx), aux couleurs et à l'identité de **RVC IMMOBILIER**, à partir des
informations du dossier. Le but : un contrat propre, juridiquement structuré et
prêt à être complété/signé par le mandant et le mandataire.

La trame ci-dessous reprend la structure complète d'un mandat de gestion de
place (désignation, conditions de location, durée + loi Chatel, obligations du
mandant, décence, pouvoirs détaillés du mandataire, reddition, honoraires,
transmission, non-discrimination, notifications électroniques, RGPD), **adaptée
aux spécificités de RVC** :

- RVC IMMOBILIER est le **département immobilier d'une étude de commissaires de
  justice** (officiers ministériels) ;
- l'activité d'administration de biens est exercée **sans carte professionnelle
  Hoguet** (dérogation liée au statut de commissaire de justice) ;
- la **garantie financière** des fonds et l'**assurance de responsabilité civile
  professionnelle** sont apportées par la **Chambre Nationale des Commissaires
  de Justice, 44 rue de Douai, 75009 Paris** (et non par une caisse de type
  GALIAN/Hoguet).

---

## Déroulé

1. **Recueillir** les informations du dossier (poser les questions manquantes,
   idéalement en une question structurée groupée).
2. **Remplir** la trame : substituer chaque `{{champ}}` par la valeur fournie.
   Tout champ non renseigné reste affiché `[À COMPLÉTER : libellé]`
   (ne jamais inventer une donnée du dossier, ni un montant d'honoraires).
3. **Générer le .docx** via le skill `docx` (voir « Génération »), à la charte
   RVC : en-tête avec logo, bleu marine `#1B2A4A`, doré `#B8975A`.
4. **Présenter** le fichier avec `present_files` et proposer les ajustements.

---

## Étape 1 — Recueillir les informations

Demander, si non fournis :

**LE MANDANT (propriétaire)** — personne physique : civilité, nom, prénom(s),
date et lieu de naissance, nationalité, profession, situation matrimoniale,
adresse, téléphone, e-mail. Personne morale : dénomination, forme, capital,
siège, ville + n° RCS, représentant et qualité. **Lister tous les co-mandants**
(indivision, SCI : gérant + associés, couple).

**LE BIEN** — adresse complète, nature (appartement/maison/local), étage,
n° de lot(s) et tantièmes, surface habitable, nombre de pièces principales,
année/période de construction, description (pièce par pièce si fournie),
dépendances (garage, cave, terrain + superficie), équipements, usage
(habitation / mixte / pro).

**CONDITIONS DE LA LOCATION** — régime juridique (bail loi n° 89-462 du 6 juillet
1989 nue ; meublé ; code civil ; bail commercial), durée du bail, loyer mensuel
HC, modalités et jour de paiement, charges (mode), révision (IRL), dépôt de
garantie, date à laquelle le bien sera libre / locataire en place.

**HONORAIRES** — taux de gestion courante, GLI proposée ou non (+ taux),
honoraires de location/relocation (répartition bailleur/locataire dans les
plafonds), barème des frais annexes (contentieux, sinistre, PNO, diagnostics…).
Utiliser le **barème RVC** ci-dessous ; à défaut laisser `[À COMPLÉTER]`.

**PARAMÈTRES DU MANDAT** — n° au registre des mandats, date d'effet, durée
initiale (souvent 1 an), préavis de résiliation (souvent 3 mois LRAR), seuil de
travaux sans accord, lieu et date de signature, mandat signé hors établissement
ou non (si oui : ajouter le droit de rétractation 14 jours + bordereau).

Reprendre le nom du demandeur. Le mandataire est toujours la société
RVC IMMOBILIER représentée par son Président.

---

## Étape 2 — Trame du mandat (à remplir)

> Reproduire fidèlement les titres et clauses. Substituer les `{{champs}}`.
> Répéter les blocs « mandant » et les désignations autant que nécessaire.

---

**MANDAT DE GESTION**
*(Articles 1984 et suivants du Code civil)*

**Mandat n° {{numero_mandat}}** — inscrit au registre des mandats de RVC IMMOBILIER

### ENTRE LES SOUSSIGNÉS

**Le mandant**
{{civilite}} {{nom}} {{prenom}}, né(e) le {{date_naissance}} à {{lieu_naissance}},
de nationalité {{nationalite}}, {{profession}}, {{situation_matrimoniale}},
demeurant {{adresse_mandant}}. Téléphone : {{tel_mandant}} — Courriel :
{{email_mandant}}.
*(Pour une personne morale : « La société {{denomination}}, {{forme}} au capital
de {{capital}} €, siège {{siege}}, RCS {{ville_rcs}} n° {{rcs}}, représentée par
{{representant_mandant}} en qualité de {{qualite_mandant}}. » Ajouter les associés
le cas échéant.)*

Ci-après « **le MANDANT** », d'une part,

**Le mandataire**
La société **RVC IMMOBILIER**, **Société par actions simplifiée (SAS)** au capital
de **1 500 €**, dont le siège social est **12 Place Carnot, 50300 AVRANCHES**,
immatriculée au **RCS de Coutances sous le numéro 100 666 650**, département
immobilier de l'étude de commissaires de justice, représentée par **Monsieur
Antoine COUSTENOBLE**, en sa qualité de **Président**, ayant tous pouvoirs à
l'effet des présentes.

Activité d'administration de biens exercée en qualité de **commissaire de
justice**, officier ministériel : à ce titre, le mandataire **n'est pas soumis à
l'obligation de carte professionnelle** prévue par la loi n° 70-9 du 2 janvier
1970. La **garantie financière** des fonds détenus pour le compte des mandants et
l'**assurance de responsabilité civile professionnelle** sont assurées par la
**Chambre Nationale des Commissaires de Justice, 44 rue de Douai, 75009 Paris**.

Ci-après « **le MANDATAIRE** » ou « l'Agence », d'autre part,

### IL A ÉTÉ FAIT ET CONVENU CE QUI SUIT

Le MANDANT confère par les présentes au MANDATAIRE, qui l'accepte, le mandat
**d'administrer les biens désignés ci-après**.

#### Désignation des biens
{{designation_bien}}
Adresse : {{adresse_bien}}. Nature : {{nature_bien}}. Surface habitable :
{{surface}} m². Nombre de pièces principales : {{pieces}}. Construction :
{{annee}}. {{lots_copropriete}}
Dépendances / autres parties : {{dependances}}. Terrain : {{terrain}}.
Éléments d'équipement : {{equipements}}.
**Usage :** les biens sont destinés à un usage {{usage}}.

#### Conditions de la location
- **Régime juridique** : {{regime_bail}} (à défaut, bail soumis à la loi
  n° 89-462 du 6 juillet 1989 et à ses textes d'application).
- **Durée du bail** : {{duree_bail}}.
- **Loyer** : montant mensuel initial de {{loyer}} €, payable d'avance le
  {{jour_paiement}} de chaque mois entre les mains du MANDATAIRE.
- **Charges** : {{modalite_charges}}.
- **Révision** : indexation annuelle sur l'indice de référence des loyers (IRL)
  publié par l'INSEE.
- **Dépôt de garantie** : {{depot_garantie}} €.

#### Durée du mandat
Le présent mandat est donné pour une durée initiale de **{{duree_mandat}}** à
compter de sa signature. Il se renouvelle ensuite par tacite reconduction par
périodes de même durée, sans que sa durée totale ne puisse excéder trente ans.
Chaque partie peut y mettre fin pour le terme de chaque période en avisant
l'autre par **lettre recommandée avec accusé de réception**, moyennant un préavis
de **{{preavis}}** courant à compter de la première présentation de la lettre.

Par dérogation expresse à l'article 2003 du Code civil, le décès du MANDANT
n'emporte pas la résiliation de plein droit du mandat, lequel se poursuit avec
ses ayants droit.

En application de l'article L. 215-4 du Code de la consommation, les articles
L. 215-1 à L. 215-3 et L. 241-3 du même code sont reproduits ci-après :

> **Art. L. 215-1** — Pour les contrats de prestations de services conclus pour
> une durée déterminée avec une clause de reconduction tacite, le professionnel
> prestataire de services informe le consommateur par écrit, par lettre
> nominative ou courrier électronique dédiés, au plus tôt trois mois et au plus
> tard un mois avant le terme de la période autorisant le rejet de la
> reconduction, de la possibilité de ne pas reconduire le contrat qu'il a conclu
> avec une clause de reconduction tacite. Cette information, délivrée dans des
> termes clairs et compréhensibles, mentionne, dans un encadré apparent, la date
> limite de non-reconduction. Lorsque cette information ne lui a pas été adressée
> conformément au premier alinéa, le consommateur peut mettre gratuitement un
> terme au contrat à tout moment à compter de la date de reconduction. Les
> avances effectuées après la dernière date de reconduction ou, s'agissant des
> contrats à durée indéterminée, après la date de transformation du contrat
> initial à durée déterminée, sont dans ce cas remboursées dans un délai de
> trente jours à compter de la date de résiliation, déduction faite des sommes
> correspondant, jusqu'à celle-ci, à l'exécution du contrat. Les dispositions du
> présent article s'appliquent sans préjudice de celles qui soumettent légalement
> certains contrats à des règles particulières concernant l'information du
> consommateur.
>
> **Art. L. 215-2** — Les dispositions du présent chapitre ne sont pas
> applicables aux exploitants des services d'eau potable et d'assainissement.
>
> **Art. L. 215-3** — Les dispositions du présent chapitre sont également
> applicables aux contrats conclus entre des professionnels et des
> non-professionnels.
>
> **Art. L. 241-3** — Lorsque le professionnel n'a pas procédé au remboursement
> dans les conditions prévues à l'article L. 215-1, les sommes dues sont
> productives d'intérêts au taux légal.

#### Déclarations et obligations du mandant
Le MANDANT déclare avoir la capacité juridique de disposer des biens et ne faire
l'objet d'aucune mesure restreignant sa capacité à agir (tutelle, curatelle…).
Il s'engage à informer le MANDATAIRE de tout élément nouveau, juridique ou
matériel, susceptible d'affecter l'exécution du mandat, et à lui communiquer sans
délai tout congé reçu. Il déclare n'avoir opté pour aucun régime fiscal
spécifique ni conventionnement, sauf mention contraire. Il déclare que les biens
seront libres de toute occupation à la date convenue et s'engage à remettre au
MANDATAIRE un exemplaire du bail en cours le cas échéant. S'il souhaite donner
congé pour vente, il devra mandater expressément le MANDATAIRE à cet effet, en
précisant prix et conditions. En cas de locations nouvelles, le MANDANT dispense
le MANDATAIRE de l'envoi de la lettre recommandée prévue à l'article 67 du décret
n° 72-678 du 20 juillet 1972, sous réserve que le détail des versements figure au
compte rendu de gestion. Compte tenu de l'étendue de la mission, le MANDANT
s'interdit de confier tout pouvoir concurrent à un tiers.

#### Conformité aux normes de décence
Le MANDANT reconnaît être tenu de mettre à disposition du locataire un logement
décent ne portant pas atteinte à la santé et à la sécurité des occupants. Si le
logement ne répond pas aux normes de décence et d'habitabilité en vigueur, il
s'engage à réaliser les travaux de mise en conformité avant la prise de
possession par le locataire.

#### Pouvoirs du mandataire
Le MANDANT donne au MANDATAIRE le pouvoir d'accomplir, pour son compte, tous les
actes relatifs à l'administration des biens, et notamment :
- percevoir et encaisser les loyers, charges et accessoires, dont le MANDATAIRE
  demeure détenteur ; percevoir le dépôt de garantie ;
- donner quittance, reçu et décharge, et donner mainlevée de toute saisie,
  opposition et cautionnement ;
- réviser les loyers et ajuster les provisions ;
- encaisser indemnités d'occupation et d'assurance, et toute somme relative aux
  biens ;
- procéder à tous règlements (charges de copropriété, et, sur demande expresse
  du MANDANT, impositions et taxes), récupérables le cas échéant sur les
  locataires ;
- en cas de défaut de paiement, après mise en demeure et commandement de payer
  infructueux, engager les **procédures en paiement et expulsion** — le
  MANDATAIRE étant attaché à une étude de commissaires de justice — le cas
  échéant avec le concours d'un avocat dont les honoraires auront été acceptés
  par le MANDANT ;
- accepter les congés ; réaliser ou faire réaliser les états des lieux d'entrée
  et de sortie ;
- rechercher des locataires et louer aux prix, charges et conditions jugés
  opportuns ; mener les actions commerciales utiles à la (re)location ;
- sélectionner les locataires **dans le strict respect de l'interdiction de toute
  discrimination** ;
- faire réaliser, aux frais du MANDANT, les diagnostics imposés par la
  réglementation ; rédiger et signer les baux et avenants ;
- faire exécuter, sans autorisation préalable, les réparations et travaux
  d'entretien courant dont le montant n'excède pas **300 € TTC** ; au-delà, le
  MANDATAIRE soumet un ou plusieurs **devis à l'accord préalable du MANDANT**
  avant exécution, **sauf urgence** touchant à la sécurité des occupants ou à la
  jouissance du bien (fuite, panne de chauffage, sinistre…), où il fait procéder
  sans délai aux mesures conservatoires et en informe aussitôt le MANDANT ;
- sur demande du MANDANT, souscrire/résilier les contrats d'assurance de gestion
  courante, déclarer les sinistres et percevoir les indemnités.
Les frais et débours sont supportés par le MANDANT et prélevés sur les sommes
détenues pour son compte, le solde restant dû étant réglé à première demande sous
quinzaine.

#### Reddition des comptes
Le MANDATAIRE rend compte de sa gestion **mensuellement** par l'envoi d'un
relevé de gérance détaillant recettes et dépenses. Les comptes sont soldés
chaque mois, déduction faite des frais, honoraires et avances. Le versement
du solde au MANDANT s'effectue par virement bancaire **sur le compte bancaire
communiqué par le MANDANT** (le RIB est recueilli via le formulaire ; ne pas
faire figurer de n° de compte à remplir dans le mandat).

#### Honoraires du mandataire
- **Gestion courante** : **7 % HT, soit 8,40 % TTC** (au taux de TVA de 20 %) du
  montant quittancé ; toute évolution du taux de TVA s'applique immédiatement.
  Honoraires à la charge exclusive du MANDANT, prélevés sur chaque relevé.
- **Location / relocation** (régime loi du 6 juillet 1989) : honoraires fixés au
  **maximum légal, à la charge du propriétaire comme du locataire**. Part
  locataire plafonnée (art. 5, loi du 6 juillet 1989) : visite + constitution du
  dossier + rédaction du bail à {{plafond_zone}} €/m² de surface habitable
  (**barème 2026** : 8,07 €/m² zone non tendue, 10,09 €/m² zone tendue,
  12,10 €/m² zone très tendue) et état des lieux d'entrée à **3,03 €/m²** ; part
  bailleur d'un montant au moins équivalent. **Plafonds indexés annuellement sur
  l'IRL — à vérifier chaque année.** Détail chiffré pour ce bien ({{surface}} m²)
  : {{honoraires_location_calcul}}.
- **Prestation sur devis** : toute prestation ne figurant ni au mandat ni au
  barème fait l'objet d'un devis préalablement accepté par le MANDANT.
- **Suivi de travaux sur devis** (hors entretien courant) : **5 % HT** du montant
  TTC des travaux, dès le 1er euro de travaux faisant l'objet d'un devis.
- **Frais de dossier contentieux locataire** : 120 € TTC. **Gestion de sinistre**
  d'assurance : 120 € TTC. **Transmission de dossier à un confrère** : 120 € TTC.
  **Constitution d'un dossier ANAH** : 250 € TTC. **Demande de diagnostics** :
  10 € TTC.
- *GLI et PNO : non proposées par RVC.*

#### Transmission du mandat
En cas de transmission par le MANDATAIRE de son activité, le présent mandat se
poursuit au profit du successeur remplissant les conditions légales d'exercice,
ce que le MANDANT accepte. Le MANDANT en est avisé par LRAR dans les meilleurs
délais et, au plus tard, dans les six mois ; il peut, dans le mois de la
réception, résilier dans les mêmes formes, la résiliation prenant effet un mois
après réception.

#### Engagement de non-discrimination
Les parties s'engagent à n'opposer à aucun candidat à la location un refus fondé
sur un motif discriminatoire (origine, sexe, situation de famille, grossesse,
apparence physique, handicap, état de santé, mœurs, orientation sexuelle, âge,
opinions, activités syndicales, appartenance vraie ou supposée à une ethnie, une
nation, une prétendue race ou une religion). Toute discrimination est pénalement
sanctionnée. Le MANDANT s'interdit de donner au MANDATAIRE toute directive en ce
sens.

#### Notifications électroniques
Le MANDANT accepte que les lettres recommandées du MANDATAIRE lui soient adressées
par **envoi recommandé électronique** avec accusé de réception à l'adresse mail
indiquée ci-avant (art. 1126 du Code civil et L. 100 du Code des postes et des
communications électroniques), via un tiers de confiance agréé. Il lui appartient
de vérifier ses courriers indésirables et garantit la maîtrise exclusive de son
compte e-mail.

#### Protection des données (RGPD)
Les données personnelles collectées sont traitées pour l'exécution du présent
mandat, la gestion de la relation, le respect des obligations légales (dont la
lutte contre le blanchiment) et conservées pendant la durée légale. Le MANDANT
dispose d'un droit d'accès, de rectification, d'effacement et d'opposition en
s'adressant à RVC IMMOBILIER, 12 Place Carnot, 50300 AVRANCHES —
contact@rvc-immobilier.fr. Toute réclamation peut être portée devant la CNIL
(www.cnil.fr).

#### Médiation de la consommation
Les différends relatifs à la validité, l'interprétation, l'exécution ou la
résiliation du présent contrat pourront être soumis au médiateur de la
consommation (art. L. 612-1 du Code de la consommation). Le MANDANT consommateur
devra au préalable justifier avoir tenté de résoudre son litige directement
auprès du MANDATAIRE par une réclamation écrite adressée par lettre recommandée
avec accusé de réception. Si la réponse ne le satisfait pas, ou en l'absence de
réponse sous trente (30) jours, il pourra saisir gratuitement le médiateur
compétent inscrit sur la liste des médiateurs agréés :
- **Nom** : Le Centre de la Médiation de la Consommation des Conciliateurs de
  Justice (**CM2C**) ;
- **Adresse** : 14 rue Saint-Jean, 75017 Paris ;
- **Date d'obtention du label médiateur** : 18/04/2026 ;
- **Contact** : cm2c@cm2c.net — www.cm2c.net.

Les parties restent libres d'accepter ou de refuser le recours à la médiation ;
la solution proposée ne s'impose pas à elles.

Le MANDANT est par ailleurs informé qu'il peut s'opposer à l'utilisation de ses
coordonnées téléphoniques à des fins de prospection commerciale en s'inscrivant
sur la liste d'opposition au démarchage téléphonique : par courrier à Worldline —
Service Bloctel — CS 61311 — 41013 BLOIS Cedex, ou en ligne sur
https://www.bloctel.gouv.fr.

#### Élection de domicile
Les parties font élection de domicile en leurs adresses respectives indiquées en
tête des présentes.

#### Signature électronique
Le mandat peut être conclu et signé sous **forme électronique**, au moyen d'un
procédé conforme au **règlement (UE) n° 910/2014 « eIDAS »** et aux **articles
1366 et 1367 du Code civil**. Le procédé identifie le signataire, garantit son
consentement et l'intégrité de l'acte, conservé sur support durable. La signature
électronique a la **même valeur juridique que la signature manuscrite** ; le
fichier de preuve, l'horodatage et le certificat sont opposables aux parties, qui
reçoivent chacune un exemplaire électronique de l'acte signé.

### DATE ET SIGNATURES
Fait à {{lieu_signature}}, en deux exemplaires originaux, le {{date_signature}}.

*(Mentions manuscrites : côté mandant « Lu et approuvé — Bon pour mandat » ; côté
mandataire « Lu et approuvé — Bon pour acceptation de mandat ». Parapher chaque
page.)*

| **Pour le MANDANT** | **Pour le MANDATAIRE** |
|---|---|
| {{civilite}} {{nom}} {{prenom}} | RVC IMMOBILIER — A. COUSTENOBLE, Président |

---

## Identité RVC (constantes de l'agence — à jour KBis 03/02/2026)
- **Dénomination** : RVC IMMOBILIER — département immobilier d'une étude de
  commissaires de justice, p