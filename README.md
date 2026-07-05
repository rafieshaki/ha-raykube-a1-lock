# Serrure RAYKUBE A1 — Home Assistant

Integration cloud Tuya dediee a la serrure RAYKUBE A1 (Ultra / Pro Max, categorie `jtmspro`).

## Fonctions
- Verrouillage (cloud, `door-operate` open=false)
- Deverrouillage (cloud, `door-operate` open=true)
- Etat verrouille/deverrouille (DP 47 `lock_motor_state`)
- Niveau de batterie (DP 9)
- Alerte batterie faible / coupure (DP 21)

## Prerequis
1. Un projet Tuya Cloud (iot.tuya.com) avec le service **Smart Lock Open Service** active.
2. Le device_id de la serrure lie au projet.
3. Client ID (Access ID) et Access Secret du projet.

## Installation
1. Copier `custom_components/serrure_raykube` dans votre dossier `config/custom_components/`, ou ajouter ce depot dans HACS.
2. Redemarrer Home Assistant.
3. Parametres -> Appareils et services -> Ajouter une integration -> "Serrure RAYKUBE A1".
4. Saisir Client ID, Access Secret, Device ID, Region.

## Securite
Les identifiants sont saisis dans la fenetre de configuration et stockes localement par Home Assistant. Ils ne figurent jamais dans le code et ne sont pas publies.

## Note technique
La methode lock/unlock reprend l'approche de xtend_tuya (validee par l'usage) :
`password-ticket` -> `smart-lock/.../password-free/door-operate`.
