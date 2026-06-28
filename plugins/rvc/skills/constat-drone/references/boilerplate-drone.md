# Boilerplate des sections drone — texte de référence paramétré

Ce fichier est la **source de vérité** du texte juridique fixe inséré dans un constat drone.
Le texte ci-dessous reproduit fidèlement l'export du logiciel Juris Drone (PDF « expédition »).
Les valeurs variables d'un vol à l'autre sont entre `{{ACCOLADES}}`. Tout le reste est figé.

> **Règle d'or** : ne jamais paraphraser ni « améliorer » ce texte juridique. Il est rédigé pour
> sa valeur probatoire. On remplace seulement les `{{placeholders}}`. Si une valeur est inconnue
> et non déductible (ex. METAR), suivre la consigne de la section concernée (souvent : retirer la
> phrase qui la contient, jamais laisser le placeholder brut visible).

---

## Tableau des variables (`{{placeholder}}` → où la trouver dans le PDF)

### A. Identité exploitant / office (quasi constantes pour l'étude)
| Placeholder | Valeur d'exemple (dossier Gauthier) | Emplacement PDF |
|---|---|---|
| `{{EXPLOITANT_NOM}}` | S.C.P. FLORENCE ROIS, MATHILDE VAUPRES & ANTOINE COUSTENOBLE COMMISSAIRES DE JUSTICE ASSOCIES | p.2 requête, p.7 marquage |
| `{{OFFICE_RESIDENCE}}` | AVRANCHES (50300) | p.2 |
| `{{OFFICE_ADRESSE}}` | 12 Place Carnot 50300 AVRANCHES | p.7 |
| `{{OFFICE_TEL}}` | 0233580841 | p.7 |
| `{{NUM_EXPLOITANT}}` | FRAb1xg7j1ne682t | p.2, p.3, p.7 |
| `{{NUM_ENREGISTREMENT}}` | UAS-FR-604829 | p.3, p.7 |
| `{{DATE_DECLA_DGAC}}` | 21/05/2026 | p.7 |
| `{{DATE_DECLA_DGAC_FIN}}` | 20/05/2031 | p.7 |
| `{{TELEPILOTE_NOM}}` | Antoine COUSTENOBLE | p.2, p.16 |
| `{{CERT_TELEPILOTE}}` | FRA-RP-000000051282 | p.2, p.16 |
| `{{CERT_TELEPILOTE_FIN}}` | 04/03/2029 | p.2, p.16 |
| `{{ASSUREUR}}` | AXA | p.8 |
| `{{POLICE_ASSURANCE}}` | 11326543004 | p.8 |
| `{{ASSURANCE_FIN}}` | 31/12/2026 | p.8 |
| `{{JURIS_DRONE_SIEGE}}` | 8 Rue Rabelais - 66280 SALEILLES | p.16 |
| `{{CONTACT_EMAIL}}` | a.coustenoble@rvc-etude.fr | p.16 |

### B. Caractéristiques de l'aéronef (constantes tant que le drone ne change pas)
| Placeholder | Valeur d'exemple | Emplacement PDF |
|---|---|---|
| `{{DRONE_MODELE}}` | DJI Matrice 4E | p.3, p.14 |
| `{{DRONE_SN}}` | 1581F7FVC263R00D6YZG | p.3 |
| `{{SIGNALEMENT_ELEC_ID}}` | 1581E1581F7FVC263R00D6YZG | p.3, p.8 |
| `{{ID_DIRECTE_DISTANCE}}` | FRAb1xg7j1ne682t-usd | p.3, p.8 |
| `{{CAMERA_SN}}` | 10.00.17.19 | p.3 |
| `{{RADIOCOMMANDE_MODELE}}` | DJI RC PLUS 2 | p.3 |
| `{{RADIOCOMMANDE_SN}}` | 9N9UP3L001XQ3X | p.3 |
| `{{DRONE_CLASSE}}` | C2 | p.3, p.14 |
| `{{DRONE_MASSE}}` | 1229 grammes | p.8 |

### C. Variables propres au vol (changent à chaque constat)
| Placeholder | Valeur d'exemple | Emplacement PDF / déduction |
|---|---|---|
| `{{COMMUNE}}` | JULLOUVILLE | p.12, p.14 — sinon déduire de l'adresse mission |
| `{{ADRESSE_MISSION}}` | 170 Route de Vaumoisson, 50610 JULLOUVILLE | p.2 / DOCX |
| `{{SOUS_CATEGORIE}}` | A2 | p.14, p.15 |
| `{{HAUTEUR_MAX}}` | 49 mètres | p.15 « Règles applicables au présent vol » |
| `{{METAR_DATETIME}}` `{{METAR_AIRPORT}}` `{{METAR_CODE}}` | (souvent vide) | p.9 — si vide, **retirer la phrase METAR** |

> **Identité (nom, requérants, date) : le DOCX brouillon fait foi.** Le PDF peut diverger
> (ex. « GAUTIER » vs « GAUTHIER », 1 vs 2 requérants). Toujours aligner sur le DOCX et corriger
> la page de garde / la requête en conséquence. Voir `rules-drone.md` règle D1.

---

## SECTION 1 — Enrichissement du bloc « DÉFÉRANT À CETTE RÉQUISITION »

Dans le DOCX brouillon, le bloc « Nous SCP … l'un d'eux soussigné » est complété pour mentionner
la qualité d'exploitant d'aéronef et de télépilote. Texte à fusionner (style des constats d'Antoine) :

> Nous SCP Florence ROIS, Mathilde VAUPRES, Antoine COUSTENOBLE, Commissaires de Justice
> associés, titulaires des offices de SAINT-PAIR-SUR-MER, AVRANCHES et de VIRE, l'un d'eux
> soussigné, **exploitant d'aéronefs télépilotés sans équipage à bord sous le numéro
> {{NUM_EXPLOITANT}} et le commissaire de justice en charge des opérations étant titulaire du
> certificat de télépilote théorique n°{{CERT_TELEPILOTE}} délivré par la RDW et expirant le
> {{CERT_TELEPILOTE_FIN}}.**

---

## SECTION 2 — INFORMATION SUR L'APPAREIL UTILISÉ
*(Titre de niveau 1. Inséré juste avant le chapitre CONSTATATIONS.)*

**ENCADRÉ (juste sous le titre, mis en avant : cadre bleu nuit + fond bleu clair, centré).**
Terme volontairement générique car le lien peut pointer vers une visite virtuelle 360°, une galerie de
photos ou des vidéos, et il peut y en avoir plusieurs. Laisser un emplacement libre pour le(s) lien(s) :

> **Le présent constat est réalisé au moyen d'un aéronef télépiloté sans équipage à bord (drone).**
>
> L'ensemble des données numériques capturées au cours de la mission — visite virtuelle à 360°,
> photographies et/ou séquences vidéo selon le support — sont consultables au(x) lien(s) suivant(s) :
>
> *[ lien(s) à insérer ]*  ← Antoine colle ici le ou les liens

Sous-titre : **Aéronef sans équipage à bord utilisé pour établir mes constatations :**

- Aéronef sans équipage à bord {{DRONE_MODELE}} dont le numéro de série est le : {{DRONE_SN}} portant le numéro d'enregistrement {{NUM_ENREGISTREMENT}}.
- L'identifiant du signalement électronique est le {{SIGNALEMENT_ELEC_ID}} et le système d'identification directe à distance porte quant à lui le numéro : {{ID_DIRECTE_DISTANCE}}.
- L'aéronef est équipé d'une caméra DJI portant le numéro de série {{CAMERA_SN}}.
- La radiocommande {{RADIOCOMMANDE_MODELE}} porte le numéro de série : {{RADIOCOMMANDE_SN}}.
- L'aéronef est de classe {{DRONE_CLASSE}} tel que défini dans l'annexe du règlement délégué (UE) 2019/945.

**Puis chapitre `CONSTATATIONS` (titre niveau 1, nouvelle page, visible au sommaire)**, suivi de la ligne « J'AI PROCÉDÉ AUX CONSTATATIONS SUIVANTES : » et des constatations réécrites.

---

## SECTION 3 — COMPTE-RENDU DE VOL
*(Titre de niveau 1. Placé APRÈS la clôture et la signature, juste avant CERTIFICATIONS TECHNIQUES.)*

Sous-titre : **Bilan des vols :**

> De retour à l'étude, j'ai extrait du logiciel de contrôle de vol la boîte noire sous forme de log
> correspondant à ma mission sous forme de fichier .txt lequel est archivé sur le serveur interne
> dédié de l'étude, ainsi que sur le serveur sécurisé de la SAS Juris Drone, et disponible sur simple
> demande des autorités compétentes. Les certifications techniques du présent vol sont également
> disponibles sur simple demande.

---

## SECTION 4 — CERTIFICATIONS TECHNIQUES
*(Titre de niveau 1. Appendice technique, après la signature.)*

Sous-titre : **AUDIT DU MATÉRIEL UTILISÉ**

> Les conditions suivantes s'appliquent à tous les aéronefs non captifs :
>
> a) Le télépilote dispose d'une information d'altitude ou de hauteur basée sur un capteur barométrique.
> b) Un dispositif automatique empêche l'aéronef de dépasser une altitude ou une hauteur maximale programmable, même en cas de commande du télépilote ou d'activation d'un plan de vol automatique.
> c) Le télépilote peut à tout moment forcer un atterrissage d'urgence par arrêt des moteurs et la commande de cette fonction peut être testée au sol par le télépilote avant le vol.
> d) La perte de la liaison de commande et de contrôle entraîne la mise en œuvre d'une procédure d'atterrissage, dans les conditions suivantes :
> - Cet atterrissage peut être précédé d'une procédure d'attente en vue du rétablissement de la liaison.
> - Cette procédure ne conduit pas à une sortie du volume maximal de vol, sauf éventuellement dans le cas d'un aéronef à voilure fixe, sous réserve de minimiser en temps et en distance la sortie du volume maximal de vol ;
> - Le délai total entre la perte de liaison et l'atterrissage est suffisamment court pour minimiser le risque d'occurrence d'un dysfonctionnement supplémentaire.
>
> L'appareil est déclaré auprès de la Direction Générale de l'Aviation Civile depuis le {{DATE_DECLA_DGAC}} sous le numéro {{NUM_ENREGISTREMENT}}. Cette déclaration est valable jusqu'au {{DATE_DECLA_DGAC_FIN}}.

Sous-titre : **Marquage sur l'appareil :**

> Sur l'aéronef utilisé pour les opérations de constatations est apposée une plaquette rectangulaire
> d'une dimension de 5 cm de long et de 3 cm de large, ou ayant une surface totale supérieure ou égale
> à 15 cm², comportant :
> - Le nom de l'exploitant : {{EXPLOITANT_NOM}}
> - Le numéro d'exploitation : {{NUM_EXPLOITANT}}
> - L'adresse : {{OFFICE_ADRESSE}}
> - Le numéro de téléphone : {{OFFICE_TEL}}
> - Le numéro d'enregistrement : {{NUM_ENREGISTREMENT}}

Sous-titre : **Masse, dispositif de signalement électronique et lumineux et Identification à distance :**

> Pour les aéronefs d'une masse totale inférieure à 800 grammes, aucun dispositif de signalement
> électronique n'est nécessaire.
>
> En revanche, les aéronefs d'une masse totale supérieure à 800 grammes, conformément au décret du
> 30 octobre 2019 et à l'arrêté du 27 décembre 2019, doivent être équipés d'un dispositif de
> signalement lumineux et d'un dispositif de signalement électronique, et faire l'objet d'un
> enregistrement auprès de la Direction Générale de l'Aviation Civile.
>
> En l'espèce, l'aéronef présente une masse nette avec batterie de {{DRONE_MASSE}} et respecte les
> dispositions susmentionnées.
>
> En conformité avec les points susmentionnés, l'identifiant de signalement électronique à distance
> de l'aéronef utilisé est : {{SIGNALEMENT_ELEC_ID}}. Il présente un format d'identification de type
> ANSI/CTA/2063-A (PSN).
>
> En complément du dispositif de signalement électronique relevant d'une exigence nationale, les
> aéronefs de classe C1, C2 et C3 sans équipage à bord doivent être équipés d'un système
> d'identification directe à distance au regard de la règlementation européenne et notamment des
> exigences relatives aux classes de drone. Ce dernier système poursuit des objectifs de sécurité et
> de respect de la vie privée. En l'espèce le drone utilisé est de classe {{DRONE_CLASSE}} tel que
> défini dans l'annexe du règlement délégué (UE) 2019/945 et son numéro d'identification directe à
> distance est le {{ID_DIRECTE_DISTANCE}}. Il est donc en conformité avec le règlement susmentionné.

Sous-titre : **Assurance responsabilité civile professionnelle :**

> L'entité exploitante {{EXPLOITANT_NOM}} fait l'objet d'une assurance en responsabilité civile
> professionnelle souscrite auprès de la compagnie {{ASSUREUR}}, avec un numéro de police d'assurance
> {{POLICE_ASSURANCE}}, valable jusqu'au {{ASSURANCE_FIN}}.

---

## SECTION 5 — TRAVAUX PRÉPARATOIRES
*(Titre de niveau 1. Appendice technique.)*

> À titre liminaire, il est indiqué que le présent constat effectué par assistance aérienne avec un
> aéronef circulant sans équipage à bord, est réalisé conformément aux dispositions de :
> - La convention relative à l'aviation civile internationale de Chicago du 7 décembre 1944, publiée par le décret n° 47-974 du 31 mai 1947 et l'ensemble des protocoles qui l'ont modifiée.
> - Le décret n° 2022-1397 du 2 novembre 2022.
> - Le règlement délégué (UE) 2019/945.
> - Le règlement d'exécution (UE) 2019/947.
> - L'arrêté du 23 décembre 2025 modifiant l'arrêté du 3 décembre 2020 relatif à l'utilisation de l'espace aérien par les aéronefs sans équipage à bord.
> - L'arrêté du 3 décembre 2020 relatif aux exigences applicables aux pilotes à distance dans le cadre d'opérations relevant de la catégorie « ouverte ».
> - Le décret n° 2018-882 du 11 octobre 2018 relatif à l'enregistrement des aéronefs civils circulant sans personne à bord.
> - L'arrêté du 19 octobre 2018 relatif à l'enregistrement des aéronefs civils circulant sans personne à bord.
> - L'arrêté du 27 décembre 2019 définissant les caractéristiques techniques des dispositifs de signalement électronique et lumineux des aéronefs circulant sans personne à bord.
> - Le décret n° 2022-1397 du 2 novembre 2022 portant application de l'article L. 6224-1 du code des transports relatif au régime encadrant la captation et le traitement des données recueillies depuis un aéronef dans certaines zones.
> - L'article L6211-3 du Code des transports.
> - Les articles D. 6214-3 à D. 6214-14 du Code des transports.
> - Le décret n° 2025-1449 du 31 décembre 2025 modifiant diverses dispositions du code des transports relatives aux télépilotes et aux aéronefs sans équipage à bord.
> - L'article L.34-9-2 du Code des postes et des communications électroniques.
> - L'arrêté du 17 novembre 2025 fixant la liste des zones interdites à la captation et au traitement des données recueillies depuis un aéronef.

Sous-titre : **Description des obligations générales de l'exploitant et des normes de sécurité :**

> Les obligations générales de l'exploitant peuvent figurer dans le manuel d'exploitation (MANEX) qui
> est tenu à jour en cas de survol en catégorie spécifique. Ledit manuel décrivant les modalités de
> mise en œuvre des obligations règlementaires, consultable sur demande du requérant. De plus l'aéronef
> dispose d'un manuel d'utilisation et un manuel d'entretien à jour.

Sous-titre : **Certification de contrôle des bonnes conditions de vol :**
*(METAR — si `{{METAR_CODE}}` est vide/inconnu, RETIRER ce paragraphe entièrement.)*

> Lors de mes opérations de constatation, le METAR publié le {{METAR_DATETIME}} de {{METAR_AIRPORT}}
> m'indique le code suivant : {{METAR_CODE}}

Sous-titre : **Certification de contrôle de la zone de vol :**

> Avant le vol, le site www.sia.aviation-civile.fr a été consulté afin de vérifier les cartes aériennes
> de la zone de survol, connaître les AIP, Sup AIP et NOTAM pour identifier les éventuelles restrictions,
> y compris temporaires, de vol sur le site survolé lors de la mission et, le cas échéant, obtenir les
> accords des gestionnaires de sites concernés.
>
> *(Les cartes aéronautiques, la carte de la zone de vol, les cartes de protection drone et les cartes
> OACI 1/500 000 correspondantes sont reportées en ANNEXES du présent constat.)*

Sous-titre : **Espace aérien survolé :**

> Toujours à l'aide du site internet du service de l'information aéronautique, www.sia.aviation-civile.fr,
> j'ai vérifié également que la zone d'évolution de l'aéronef s'inscrivait dans une zone d'aviation
> autorisée, ne comportant aucune limitation ou restriction particulière quant à la hauteur de vol ou la
> zone de survol. En l'espèce la zone survolée se trouve en dehors d'une CTR et ne tombe pas sous
> l'emprise d'un aérodrome, un héliport, une zone militaire, ou d'une autre zone dont l'accès serait
> soumis à autorisation ou déclaration.

Sous-titre : **Détermination de la sous-catégorie et de l'environnement de vol :**

> *Un aéronef est dit évoluer « en vue directe » lorsque :* ses évolutions se situent à une distance du
> télépilote telle que celui-ci conserve une vue directe sur l'aéronef (sans l'aide d'aucun dispositif
> optique autre que ses lunettes ou lentilles de correction le cas échéant) et une vue dégagée sur
> l'environnement aérien permettant de détecter tout rapprochement d'aéronef et de prévenir les
> collisions.
>
> En l'espèce, le drone a été conservé dans mon champ de vision direct durant toute la durée des opérations.
>
> *Détermination de la sous-catégorie opérationnelle :* conformément au règlement d'exécution (UE)
> 2019/947 de la Commission du 24 mai 2019 (annexe, partie A, catégorie « ouverte »), les opérations en
> catégorie ouverte sont réparties en sous-catégories A1, A2 et A3. L'opération en sous-catégorie A2 est
> réalisée avec un aéronef de classe C2 uniquement, impose une absence de survol de personnes non
> impliquées ainsi qu'une distance horizontale de sécurité supérieure ou égale à 30 m par rapport à ces
> personnes (réductible à 5 m si le mode « basse vitesse » à 3 m/s est actif).
>
> En l'espèce, l'aéronef utilisé est un drone de la marque DJI modèle {{DRONE_MODELE}} de classe
> {{DRONE_CLASSE}} tel que défini dans l'annexe du règlement délégué (UE) 2019/945.
>
> *Un aéronef est dit évoluer « en zone peuplée »* lorsqu'il évolue à l'intérieur d'une agglomération
> identifiée sur les cartes aéronautiques OACI (en jaune ou en orange), ou à moins de 50 mètres
> horizontalement de ses limites, ou à une distance horizontale inférieure à 150 mètres d'un
> rassemblement de personnes.
>
> En l'espèce le survol a lieu sur la commune de {{COMMUNE}} et s'effectue en dehors de tout
> rassemblement de personnes tel que défini par la Direction générale de l'aviation civile et sur une
> zone privée.

Sous-titre : **Règles applicables au présent vol :**

> En application des précédentes règles visées, le présent constat s'effectuera selon les règles de la
> sous-catégorie {{SOUS_CATEGORIE}}, avec un drone de classe {{DRONE_CLASSE}} et la hauteur maximum de
> survol sera de {{HAUTEUR_MAX}} par rapport au sol.

---

## SECTION 6 — AUTORISATIONS ET DÉCLARATIONS ADMINISTRATIVES DE VOL
*(Titre de niveau 1. Appendice technique.)*

> Afin de pouvoir effectuer le présent constat avec un aéronef circulant sans équipage à bord, il est
> rappelé que M. {{TELEPILOTE_NOM}}, Commissaire de justice associé en charge des opérations, ayant
> « le contrôle et la maîtrise direct de l'aéronef » et procédant aux prises de vues ainsi qu'à leur
> interprétation, est titulaire du certificat de télépilote théorique n°{{CERT_TELEPILOTE}} délivré par
> la RDW et expirant le {{CERT_TELEPILOTE_FIN}}.
>
> Concernant les prises de vues, l'entité exploitante de l'aéronef est enregistrée auprès de la Direction
> générale de l'aviation civile en tant qu'exploitant de drone, sous le numéro {{NUM_EXPLOITANT}}.

Sous-titre : **Déclaration de vol :**

> La présente mission s'effectuant en sous-catégorie {{SOUS_CATEGORIE}}, le survol ne s'effectue pas
> au-dessus de la voie publique au sein d'une zone peuplée ou à proximité d'un rassemblement de personnes.
> En conséquence, aucune déclaration préfectorale n'est requise.

Sous-titre : **CNIL :**

> Les informations recueillies font l'objet d'un traitement informatique destiné à la création et à la
> pré-rédaction du présent constat. Les données sont uniquement destinées au service Juris Drone, ayant
> son siège {{JURIS_DRONE_SIEGE}}. Elles seront conservées le temps nécessaire pour répondre aux
> obligations légales en matière de suivi du constat.
>
> Conformément à la Loi « Informatique et Libertés » n°78-17 du 06 Janvier 1978 modifiée et au Règlement
> Général sur la Protection des Données, vous disposez d'un droit d'accès aux données vous concernant ou
> pouvez demander leur effacement. Vous disposez également d'un droit d'opposition, d'un droit de
> rectification, d'un droit à la portabilité et d'un droit à la limitation du traitement de vos données
> (cf. cnil.fr pour plus d'informations sur vos droits).
>
> Pour exercer ces droits ou pour toute question sur le traitement de vos données dans ce dispositif,
> sous réserve de justifier de votre identité, vous pouvez contacter notre étude :
> - Adresse de courrier électronique : {{CONTACT_EMAIL}}
> - Adresse de courrier postal : {{OFFICE_ADRESSE}}
>
> Si vous estimez après nous avoir contactés que vos droits ne sont pas respectés, vous pourrez à tout
> moment saisir l'autorité de contrôle (CNIL).

---

## SECTION 7 — VÉRIFICATIONS TECHNIQUES PRÉALABLES
*(Titre de niveau 1. Appendice technique.)*

> Avant le vol, j'ai effectué le contrôle des points suivants.
>
> **Sur l'application DJI PILOT 2 — paramètres de sécurité et de restriction de vol :** j'ai fixé la
> hauteur de vol du retour automatique au point de décollage (Return To Home) et défini une hauteur de
> vol maximum par rapport au sol.
>
> **Étalonnage des capteurs :** j'ai vérifié que les différents capteurs dont l'IMU (accéléromètre et
> gyroscope) du drone, ainsi que le compas, les moteurs, les capteurs de proximité, les batteries, le
> signal radio et la caméra, étaient tous dans un état dit « normal ».
>
> **Retour automatique au point de décollage :** j'ai activé la fonction smart RTH (retour au point de
> départ intelligent) permettant à l'appareil de retourner à ce point lorsque le niveau de batterie
> restant ne suffit plus ou que ce dernier perd la connexion avec la radiocommande.
>
> **Versions des firmwares :** j'ai vérifié que les firmwares de l'appareil, de la radiocommande et de
> la base de données « Fly Safe » soient bien à jour.
>
> **État visuel du drone :** le drone ne présente aucun dégât apparent, aucune fissure, aucune trace de
> réparation. Les hélices sont en parfait état et ne sont ni ébréchées, ni fissurées. Avant le décollage,
> j'ai contrôlé que le drone était dans les conditions optimales pour décoller et disposait d'une
> connexion avec suffisamment de satellites.

---

## SECTION 8 — ANNEXES
*(Titre de niveau 1. TOUT À LA FIN, après la signature et tous les appendices.)*

Phrase d'introduction des annexes :

> Les pièces ci-après illustrent le cadre de la mission de vol (zone de survol, cartes aéronautiques et
> cartes de protection drone consultées avant le vol). Elles sont annexées au présent procès-verbal pour
> en préciser les conditions de réalisation.

Pour chaque image extraite du PDF (voir `scripts/extract_pdf_images.py`), insérer un sous-titre + l'image +
une légende descriptive neutre. Légendes types :

- **Annexe 1 — Zone de vol (vue cartographique standard).** Représentation de l'emprise survolée, matérialisée par un polygone, en bordure de la {{VOIE}} sur la commune de {{COMMUNE}}.
- **Annexe 2 — Zone de vol (vue satellite).** Même emprise reportée sur fond orthophotographique.
- **Annexe 3 — Carte de protection drone (vue rapprochée).** Localisation du point de décollage au regard des zones réglementées environnantes.
- **Annexe 4 — Carte de protection drone (vue élargie).** Situation de la zone au sein du secteur, avec report des zones réglementées (restrictions, hauteurs).
- **Annexe 5 — Carte aéronautique OACI 1/500 000.** Espace aérien du secteur ; la zone de survol se situe hors CTR et hors emprise d'aérodrome.
- **Annexe 6 — Extrait OACI (vue rapprochée).** Détail de l'agglomération de {{COMMUNE}} et de ses abords.
