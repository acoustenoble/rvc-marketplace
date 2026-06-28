# Modèles de mails et compte rendu Slack

Tous les mails : vouvoiement, ton professionnel et chaleureux, phrases courtes,
signature **« L'équipe RVC Immobilier »**. Adapter les éléments entre crochets.
Ne jamais promettre de visite ni laisser entendre que le dossier est accepté.

---

## Cas A — Réponse à un renseignement

**Objet : [reprendre l'objet] — [adresse / référence du bien]**

Bonjour [Madame/Monsieur + nom si connu],

Nous vous remercions de votre intérêt pour [le bien : type + adresse].

[Réponse directe à la question posée. Ex. : « Le loyer s'élève à X € charges
comprises, dont Y € de provision pour charges. » / « Le logement se situe au
[étage] et fait [surface] m². » Si une information manque : « Nous ne disposons
pas encore de cette information, mais reviendrons vers vous dès que possible. »]

Si vous souhaitez visiter le logement, sachez que nous étudions au préalable
chaque dossier de candidature ; nous proposons une visite lorsque le dossier
correspond aux attentes du propriétaire. N'hésitez pas à nous le faire savoir,
nous vous indiquerons les pièces à constituer.

Bien cordialement,
L'équipe RVC Immobilier

---

## Cas B — Accusé de réception + demande de pièces

**Objet : Votre candidature — [adresse / référence du bien]**

Bonjour [Madame/Monsieur + nom],

Nous vous remercions de l'intérêt que vous portez à [le bien : type + adresse,
loyer X € CC].

Afin d'organiser au mieux la sélection, nous étudions chaque dossier **avant**
toute visite. **Si votre dossier correspond aux attentes du propriétaire, nous
vous proposerons une visite et reviendrons vers vous.** Cette étape nous évite,
comme à vous, des visites inutiles.

Pour étudier votre candidature, merci de nous transmettre **en un seul envoi**
(idéalement un PDF), en réponse à ce mail, les pièces suivantes :

**Pour vous (et chaque co-locataire) :**
- une pièce d'identité en cours de validité ;
- un justificatif de domicile (3 dernières quittances de loyer, ou attestation
  d'hébergement, ou taxe foncière, ou attestation d'assurance habitation de
  moins de 3 mois) ;
- un justificatif de situation professionnelle (contrat de travail ou
  attestation employeur, Kbis, ou carte/certificat d'étudiant) ;
- un justificatif de ressources (3 derniers bulletins de salaire **et** votre
  dernier avis d'imposition).

**Si vous êtes étudiant :** à la place du justificatif professionnel, votre
**carte d'étudiant ou certificat de scolarité** de l'année en cours ; un
**garant est alors requis** (voir ci-dessous).

**Pour votre garant** (obligatoire pour les étudiants, recommandé sinon) :
- les mêmes pièces (identité, domicile, situation professionnelle, ressources).
  Pour un étudiant, les garants doivent justifier de revenus suffisants
  (à plusieurs, leurs revenus s'additionnent).

Dès réception d'un dossier complet, nous l'étudions et revenons vers vous.

Restant à votre disposition,
Bien cordialement,
L'équipe RVC Immobilier

> Note interne : n'ajouter aucune pièce hors de cette liste — voir
> `pieces-justificatives.md` (pièces interdites).

---

## Cas C — Mails de suite possibles (selon décision de l'utilisateur)

Ces mails ne partent **que** sur instruction de l'utilisateur (la décision
revient au propriétaire). Les proposer, ne pas les envoyer d'office.

**Dossier complet, on propose une visite :**
> Bonjour [nom], nous avons bien étudié votre dossier et avons le plaisir de
> vous proposer une visite de [le bien]. Seriez-vous disponible [créneaux] ?
> Bien cordialement, L'équipe RVC Immobilier

**Dossier incomplet, relance :**
> Bonjour [nom], merci pour votre envoi. Pour finaliser l'étude de votre dossier,
> il nous manque : [liste précise]. Pourriez-vous nous les transmettre en réponse
> à ce mail ? Bien cordialement, L'équipe RVC Immobilier

**Réponse négative (courtoise, sans détailler la fraude) :**
> Bonjour [nom], nous vous remercions pour votre candidature. Après étude, le
> propriétaire a retenu un autre dossier. Nous vous souhaitons une bonne
> continuation dans vos recherches. Bien cordialement, L'équipe RVC Immobilier

---

## Compte rendu Slack à Garance (DM)

Message direct, format mrkdwn Slack, concis et classé du meilleur au moins bon.

Gabarit :

```
:house: *Dossiers — [adresse / référence du bien] — loyer [X] € CC*
Reçu(s) : [N] dossier(s) ce [jour].

:large_green_circle: *[Nom candidat]* — *[note]/100* — À retenir
   [raison clé : ratio, garant, complétude]
:large_orange_circle: *[Nom candidat]* — *[note]/100* — À examiner
   [raison clé + point à lever]
:red_circle: *[Nom candidat]* — *[note]/100* — À écarter
   [raison clé]

:dart: Reco : [ex. « 2 dossiers à présenter au propriétaire : Dupont et Martin.
Le dossier Durand est à écarte