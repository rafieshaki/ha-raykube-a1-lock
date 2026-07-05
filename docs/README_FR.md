# Serrure RAYKUBE A1 — Intégration Home Assistant

> **État : Alpha 1 (`v1.0.0-alpha`) — en test, pas encore stable.**

Intégration cloud (Tuya) dédiée à la serrure **RAYKUBE A1 Ultra / Pro Max** (catégorie Tuya `jtmspro`, BLE + passerelle).

## Fonctions

- **Verrouillage** — API cloud Tuya Smart Lock (`door-operate`, `open=false`)
- **Déverrouillage** — API cloud Tuya Smart Lock (`door-operate`, `open=true`)
- **État du verrou** — verrouillé / déverrouillé (DP 47 `lock_motor_state`)
- **Niveau de batterie** — % (DP 9 `battery_state`)
- **Événement d'alerte** — batterie faible / coupure (DP 21 `alarm_lock`)

Configuration via l'interface — aucun YAML requis. Les identifiants sont saisis dans la fenêtre de configuration et stockés localement par Home Assistant.

## Prérequis

1. Un projet Tuya IoT Cloud (iot.tuya.com) avec le **Smart Lock Open Service** activé.
2. Le `device_id` de la serrure, lié au projet.
3. Le **Client ID (Access ID)** et l'**Access Secret** du projet.

## Installation

1. HACS -> menu -> *Dépôts personnalisés* -> ajouter l'URL du dépôt, catégorie *Intégration*.
2. Installer, puis redémarrer Home Assistant.
3. *Paramètres -> Appareils et services -> Ajouter une intégration ->* chercher **RAYKUBE A1**.
4. Saisir Client ID, Access Secret, Device ID et région.

Ou copier `custom_components/serrure_raykube` dans `config/custom_components/` puis redémarrer.

## Architecture

100% cloud (même approche que `xtend_tuya`, pris comme référence) :

| Fonction | Endpoint / DP Tuya |
|---|---|
| Verrouillage / Déverrouillage | `door-lock/password-ticket` -> `smart-lock/.../password-free/door-operate` |
| État | `GET /v1.0/devices/{id}/status` -> DP 47 `lock_motor_state` |
| Batterie | DP 9 `battery_state` |
| Alerte | DP 21 `alarm_lock` |

## Limitations connues (Alpha 1)

- Polling de l'état toutes les 30 s (configurable dans `const.py`). Pas encore de push temps réel.
- Comportement intermittent en cours d'analyse : `door-operate` peut renvoyer `success: true` sans que la serrure bouge physiquement à chaque fois. Cause non confirmée — ne pas utiliser cette version pour un usage critique de sécurité.

## Sécurité

Les identifiants sont saisis via l'interface et stockés localement par Home Assistant. Jamais codés en dur, jamais publiés.

## Licence

MIT
