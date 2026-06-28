---
name: candidatures-location-rvc
description: >-
  Traite les mails de candidats locataires de RVC IMMOBILIER (gestion locative).
  À DÉCLENCHER dès que l'utilisateur colle ou transfère un mail de prospect
  locataire, parle d'« un candidat à la location », « intéressé pour la
  location », « demande de visite », « dossier de location reçu », « pièces /
  justificatifs d'un candidat », ou demande de « noter un dossier », « répondre
  à un candidat », « trier les dossiers », « prévenir Garance ». Le skill décide
  seul s'il s'agit (A) d'un simple renseignement à traiter, (B) d'un candidat
  intéressé / qui veut visiter / demande quoi fournir → mail de retour expliquant
  la procédure + liste légale des pièces, ou (C) d'un dossier avec pièces jointes
  → analyse de complétude, détection de faux/montages, calcul de solvabilité,
  note sur 100, fiche de synthèse PDF et compte rendu Slack à Garance. Utiliser
  même sans demande explicite : tout mail de prospect locatif RVC déclenche ce
  skill. Ne pas confondre avec mandat-gestion ni estimation-immobiliere.
---

# Traitement des candidatures locatives — RVC IMMOBILIER

RVC IMMOBILIER est le département immobilier d'une étude de commissaires de
justice. La règle d'or fixée par la direction : **aucune visite n'est organisée
sans dossier fiable et complet déjà étudié.** Ce skill sert à filtrer les
prospects en amont, à répondre proprement, et à ne faire remonter à Garance
(en charge des dossiers) que les candidatures sérieuses, déjà notées.

Tout le travail se fait à partir d'un mail que l'utilisateur colle dans la
conversation (éventuellement avec des pièces jointes).

## Étape 0 — Récupérer le contexte du bien

Avant de répondre ou de noter, il faut connaître les paramètres de l'annonce
concernée. Si l'utilisateur ne les a pas déjà donnés dans la conversation,
demander en une fois (et seulement ce qui manque) :

- **Loyer hors charges** et **montant des charges** (donc le loyer **charges
  comprises**, dit « CC » — c'est la base de tous les calculs).
- Type et adresse du bien (pour personnaliser les mails).
- Éventuels **critères du propriétaire** (ex. : « CDI exigé », « pas de
  colocation », « garant obligatoire », revenu minimum particulier).

Si ces critères propriétaires existent, ils priment sur le barème standard pour
décider d'écarter un dossier (un dossier excellent mais qui ne respecte pas une
exigence ferme du propriétaire doit être signalé comme tel).

## Étape 1 — Classer le mail

Lire le mail et le ranger dans **un seul** des trois cas :

- **Cas A — Renseignement simple.** Le prospect pose une question factuelle
  (disponibilité, surface, étage, charges, animaux acceptés, date de
  disponibilité…) sans demander à visiter ni à candidater. → Voir *Cas A*.
- **Cas B — Candidat intéressé.** Le prospect se dit intéressé, demande une
  visite, demande « quoi fournir », « comment constituer le dossier », ou
  envoie quelques infos sur sa situation sans pièces. → Voir *Cas B*.
- **Cas C — Dossier avec pièces.** Le prospect a joint des justificatifs
  (identité, bulletins, avis d'imposition, contrat de travail, pièces du
  garant…). Même un dossier partiel relève du Cas C dès qu'il y a au moins une
  pièce à analyser. → Voir *Cas C*.

En cas d'hésitation entre B et C : s'il y a des pièces jointes exploitables,
c'est C. S'il n'y a que du texte, c'est B.

## Cas A — Répondre à un renseignement

Rédiger une réponse courte, professionnelle, au vouvoiement, signée
**« L'équipe RVC Immobilier »**. Répondre à la question posée à partir des
informations de l'annonce. Si une donnée manque, le dire honnêtement et inviter
le prospect à se manifester s'il souhaite candidater. Toujours rappeler en une
phrase la procédure : pour une visite, un dossier complet est étudié au
préalable. Voir les tournures dans `references/modeles-mail.md`.

Présenter la réponse à l'utilisateur (en texte, ou en brouillon Gmail si la
boîte est connectée) ; ne pas l'envoyer sans validation.

## Cas B — Candidat intéressé : expliquer la procédure et demander le dossier

Objectif : transformer l'intérêt en dossier complet, sans promettre de visite.

Produire **deux choses** :

1. **Un mail de retour** (modèle « accusé + demande de pièces » dans
   `references/modeles-mail.md`). Il doit :
   - remercier de l'intérêt et accuser réception ;
   - expliquer clairement la procédure RVC : *le dossier est d'abord étudié ; si
     le dossier correspond aux attentes du propriétaire, une visite est proposée
     et nous revenons vers le candidat* — donc **ne jamais garantir de visite** ;
   - lister les pièces à fournir pour le **locataire** (et le **garant** si la
     situation l'exige), en renvoyant à la liste légale ;
   - préciser de répondre à ce mail en joignant l'ensemble des pièces en un seul
     envoi (PDF de préférence) ;
   - être signé « L'équipe RVC Immobilier ».
2. **Une fiche dossier vierge** récapitulant les pièces attendues (sert de
   check-list interne quand les pièces arriveront). Format simple en Markdown,
   tirée de la liste de `references/pieces-justificatives.md`.

Important : ne demander que des pièces **autorisées par la loi**. La liste
exacte, et surtout la liste des pièces **interdites** à réclamer (RIB de compte,
relevés bancaires, photo, carte vitale…), est dans
`references/pieces-justificatives.md`. Réclamer une pièce interdite expose
l'agence à une sanction — c'est non négociable.

## Cas C — Analyser, détecter les faux, noter le dossier

C'est le cœur du skill. Procéder dans cet ordre.

1. **Inventaire des pièces.** Lire chaque pièce jointe (utiliser le skill `pdf`
   pour extraire texte/images si besoin, et lire les images directement).
   Pointer chaque pièce reçue contre la check-list de
   `references/pieces-justificatives.md`. Noter ce qui est **présent**,
   **manquant**, ou **non conforme** (ex. justificatif de domicile de plus de
   3 mois, avis d'imposition tronqué).

2. **Contrôle de cohérence et détection de faux.** Suivre la checklist de
   `references/detection-fraude.md` : cohérence des noms/prénoms entre toutes
   les pièces, cohérence salaire ↔ avis d'imposition, cumuls de bulletins,
   employeur identique entre contrat et bulletins, dates de validité de la pièce
   d'identité, indices de retouche (polices incohérentes, montants trop ronds,
   numéro fiscal incohérent…). Tout indice est consigné comme **alerte** avec son
   niveau (faible / sérieux / bloquant). Ne jamais affirmer « c'est un faux » de
   façon catégorique : signaler des **incohérences à vérifier**.

3. **Solvabilité.** Calculer le ratio **revenus nets mensuels du foyer candidat
   ÷ loyer charges comprises**. La cible RVC est **≥ 3×** le loyer CC. Un garant
   solide assouplit le seuil (détail du calcul et de la compensation dans
   `references/notation.md`).

4. **Notation /100.** Appliquer le barème de `references/notation.md`
   (solvabilité, garant, stabilité professionnelle, complétude, fiabilité des
   pièces). En sortir une **note sur 100**, un **niveau** (À retenir / À examiner
   / À écarter) et 2-3 phrases de justification.

5. **Fiche de synthèse PDF.** Générer une fiche par candidat selon le gabarit de
   `references/fiche-synthese.md` (utiliser le skill `pdf` pour produire le
   .pdf). Enregistrer dans le dossier de sortie.

6. **Compte rendu Slack à Garance.** Voir *Compte rendu Slack* ci-dessous.

Si plusieurs dossiers sont fournis d'un coup, traiter chacun puis faire **un
seul** compte rendu Slack récapitulatif et classé du meilleur au moins bon.

## Compte rendu Slack à Garance

Après analyse, envoyer un message direct (DM) à **Garance** sur Slack.

1. Trouver l'utilisatrice : `slack_search_users` avec « Garance ». S'il y a
   ambiguïté (plusieurs résultats), demander confirmation à l'utilisateur.
2. Composer le message selon le format de `references/modeles-mail.md`
   (section « Compte rendu Slack ») : nombre de dossiers reçus, puis pour chaque
   candidat une ligne avec nom, note /100, niveau, et la raison clé (ex. « 82/100
   — À retenir, CDI + garant solide » / « 41/100 — À écarter, revenus 2,1× sans
   garant »). Terminer par une recommandation d'action.
3. **Montrer le message à l'utilisateur avant l'envoi**, puis envoyer le DM avec
   `slack_send_message`. Les fiches PDF restent dans le dossier de sortie ;
   mentionner dans le message qu'elles sont disponibles.

## Principes transverses

- **Vouvoiement, ton professionnel et chaleureux** dans tous les mails ;
  signature « L'équipe RVC Immobilier ».
- **Ne jamais promettre de visite** ni laisser entendre que le dossier est
  accepté : la décision appartient au propriétaire.
- **Protéger les données personnelles** : le dossier contient des données
  sensibles ; rester factuel, ne pas les diffuser au-delà du nécessaire (fiche
  interne + Garance).
- **Rester prudent sur la fraude** : signaler des doutes à vérifier, pas des
  accusations.
- En cas de doute sur un critère du propriétaire, demander à l'utilisateur
  plutôt que de supposer.

## Fichiers de référence

- `references/pieces-justificatives.md` — liste légale des pièces (locataire +
  garant) et pièces interdites à réclamer.
- `references/notation.md` — barème de notation /100 et calcul de solvabilité.
- `references/detection-fraude.md` — checklist de cohérence et d'indices de faux.
- `references/modeles-mail.md` — modèles de mails (cas A et B) et format du
  compte rendu Slack.
- `references/fiche-synthese.md` — gabarit de la fiche de synthèse PDF.
                                                                                                                                                                                                                                                      