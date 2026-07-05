"""Constantes pour l'integration Serrure RAYKUBE A1."""

DOMAIN = "serrure_raykube"

# Cles de configuration (saisies dans l'UI, jamais en dur)
CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"
CONF_DEVICE_ID = "device_id"
CONF_REGION = "region"

# Regions Tuya -> endpoint API
TUYA_ENDPOINTS = {
    "eu": "https://openapi.tuyaeu.com",
    "us": "https://openapi.tuyaus.com",
    "cn": "https://openapi.tuyacn.com",
    "in": "https://openapi.tuyain.com",
}
DEFAULT_REGION = "eu"

# DP codes de la serrure (verifies sur hc7n0urm)
DP_LOCK_MOTOR_STATE = "lock_motor_state"  # DP 47 : true=deverrouille, false=verrouille
DP_BATTERY = "battery_state"              # DP 9  : high/medium/low/poweroff
DP_ALARM = "alarm_lock"                   # DP 21 : low_battery/power_off

# Mapping batterie enum -> pourcentage
BATTERY_MAP = {
    "high": 90,
    "medium": 60,
    "low": 30,
    "poweroff": 0,
}

# Intervalle de polling de l'etat (secondes)
SCAN_INTERVAL_SECONDS = 30

# Rafraichissements apres une action (secondes) pour rattraper l'etat
REFRESH_AFTER_ACTION = [3, 8]
