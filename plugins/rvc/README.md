# Plugin RVC

Regroupe les skills metier des deux entites RVC pour une installation et une mise a jour centralisees.

## Contenu

### RVC Commissaire de justice
- **constat-reecriture** — reecriture technique des constatations d'un PV de constat
- **constat-inventaire** — mise en forme d'un constat d'inventaire mobilier (tableau + photos)
- **constat-affichage** — PV de constat d'affichage d'autorisation d'urbanisme
- **constat-drone** — constat realise par drone (fusion DOCX + PDF Juris Drone)
- **etat-des-lieux** — mise en forme d'un etat des lieux d'entree ou de sortie

### RVC Immobilier
- **mandat-gestion** — mandat de gestion locative a la charte RVC (.docx)
- **estimation-immobiliere** — etude de marche / avis de valeur en PDF (donnees DVF)
- **candidatures-location-rvc** — traitement des mails et dossiers de candidats locataires
- **ecritures-comptables** — generation des ecritures comptables (PCG + plan de comptes gerance)

## Installation
Installer le fichier `rvc.plugin` depuis Reglages > Capabilities, ou via la marketplace interne.

## Mise a jour
Modifier un skill, incrementer la version dans `.claude-plugin/plugin.json`, republier le plugin. Les comptes qui suivent la marketplace recoivent la nouvelle version.
