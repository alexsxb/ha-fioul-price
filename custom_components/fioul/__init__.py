from __future__ import annotations

from datetime import timedelta
import logging

import requests
from bs4 import BeautifulSoup

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, PLATFORMS, CONF_POLLRATE, DEFAULT_POLLRATE

_LOGGER = logging.getLogger(__name__)

URL = "https://www.fioulreduc.com/prix-fioul"


def _fetch_fioul_data() -> dict:
    """Synchronously fetch fioul price and return a data dict."""
    resp = requests.get(URL, timeout=15)
    resp.raise_for_status()

    from bs4 import BeautifulSoup  # already imported, but keeps fn standalone
    soup = BeautifulSoup(resp.text, "html.parser")

    block = soup.find("div", class_="price-sticker-left")
    if block is None:
        raise RuntimeError("price-sticker-left block not found in HTML")

    header = block.find("div", class_="price-sticker-header")
    strong = block.find("strong")

    if header is None or strong is None:
        raise RuntimeError("Could not find header or price strong element")

    date = header.get_text(strip=True)
    price_raw = strong.get_text(strip=True)
    price = float(price_raw.replace("€", "").replace(",", ".").strip())

    return {"price": price, "date": date}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Fioul from a config entry."""
    pollrate = entry.data.get(CONF_POLLRATE, DEFAULT_POLLRATE)
    try:
        pollrate = int(pollrate)
        if pollrate <= 0:
            pollrate = DEFAULT_POLLRATE
    except (TypeError, ValueError):
        pollrate = DEFAULT_POLLRATE

    hours = 24 / pollrate
    update_interval = timedelta(hours=hours)

    async def _async_update_data():
        try:
            return await hass.async_add_executor_job(_fetch_fioul_data)
        except Exception as err:
            raise UpdateFailed(f"Error updating fioul data: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="fioul_price",
        update_interval=update_interval,
        update_method=_async_update_data,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok and DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
