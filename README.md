# Fioul Price – Home Assistant Integration

![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)

Fetches the daily heating oil price (Fioul Domestique – 1000L) from FioulReduc and exposes it as a sensor in Home Assistant.

## Features

- Sensor: `sensor.fioul_price`
- Value: price in EUR per 1000L
- Attribute: date string from FioulReduc
- Polling frequency configurable via UI (Integrations)
  - Pollrate = number of updates per day
  - Example:
    - 1 → every 24h
    - 2 → every 12h
    - 3 → every 8h
    - 4 → every 6h

## Installation (HACS – Custom Repository)

1. Go to **HACS → Integrations → Custom repositories**
2. Add this repository URL: `https://github.com/USER/ha-fioul`
   - Category: `Integration`
3. Search for **Fioul Price** in HACS and install.
4. Restart Home Assistant.

## Configuration (UI)

1. Settings → Devices & Services → **Add Integration**
2. Search for **Fioul**
3. Enter the desired **Pollrate** (1–24)
4. Finish setup.

The sensor `sensor.fioul_price` will appear with the latest fetched value.

## Manual installation

1. Copy the `custom_components/fioul` directory into your Home Assistant `config/custom_components` folder.
2. Restart Home Assistant.
3. Add the integration via the UI as described above.
