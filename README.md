# RAYKUBE A1 Smart Lock — Home Assistant Integration

> **Status: Alpha 1 (`v1.0.0-alpha`) — early testing, not yet stable.**

Cloud-based (Tuya) Home Assistant integration dedicated to the **RAYKUBE A1 Ultra / Pro Max** smart lock (Tuya category `jtmspro`, BLE + gateway).

## Features

- **Lock** — Tuya Smart Lock cloud API (`door-operate`, `open=false`)
- **Unlock** — Tuya Smart Lock cloud API (`door-operate`, `open=true`)
- **Lock state** — locked / unlocked (DP 47 `lock_motor_state`)
- **Battery level** — % (DP 9 `battery_state`)
- **Alert event** — low battery / power off (DP 21 `alarm_lock`)

UI config flow — no YAML required. Credentials are entered in the setup dialog and stored locally by Home Assistant.

## Requirements

1. A Tuya IoT Cloud project (iot.tuya.com) with the **Smart Lock Open Service** enabled.
2. The lock's `device_id`, linked to the project.
3. The project's **Client ID (Access ID)** and **Access Secret**.

## Installation (HACS custom repository)

1. HACS -> three dots -> *Custom repositories* -> add this repo URL, category *Integration*.
2. Install, then restart Home Assistant.
3. *Settings -> Devices & Services -> Add Integration ->* search **RAYKUBE A1**.
4. Enter Client ID, Access Secret, Device ID and region.

Or copy `custom_components/serrure_raykube` into your `config/custom_components/` folder manually and restart.

## Architecture

100% cloud (same approach as `xtend_tuya`, used as the reference implementation):

| Function | Tuya endpoint / DP |
|---|---|
| Lock / Unlock | `door-lock/password-ticket` -> `smart-lock/.../password-free/door-operate` |
| State | `GET /v1.0/devices/{id}/status` -> DP 47 `lock_motor_state` |
| Battery | DP 9 `battery_state` |
| Alert | DP 21 `alarm_lock` |

## Known limitations (Alpha 1)

- State polling every 30 s (configurable in `const.py`). No real-time push yet.
- Intermittent behaviour under investigation: `door-operate` may return `success: true` while the lock does not physically actuate every time. Root cause not yet confirmed — do **not** rely on this build for security-critical use.

## Security

Credentials are entered through the config UI and stored locally by Home Assistant. They are never hard-coded and never published.

## License

MIT
