# Marketplace interne RVC

Ce depot contient les plugins metier de RVC, installables dans Claude.

## Pour les collaborateurs
Ajoutez cette marketplace dans Claude (voir le guide d'installation fourni par Antoine),
puis installez le plugin **rvc**.

## Plugins disponibles
- **rvc** — 9 skills metier (commissaire de justice + immobilier).

## Pour le responsable (mise a jour)
1. Modifier le skill concerne dans `plugins/rvc/skills/...`
2. Incrementer `version` dans `plugins/rvc/.claude-plugin/plugin.json`
3. Enregistrer les modifications sur GitHub (commit + push)
Les comptes abonnes recoivent la nouvelle version au rafraichissement.
