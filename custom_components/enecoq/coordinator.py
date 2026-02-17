from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    CONF_TODAY_PATH, CONF_MONTH_PATH,
    CONF_SCAN_INTERVAL, CONF_STALE_MINUTES,
)

_LOGGER = logging.getLogger(__name__)

def _parse_ts(ts: str) -> datetime | None:
    try:
        ts = ts.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None

def _read_json_sync(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

async def _read_json(hass, path: str) -> dict:
    try:
        return await hass.async_add_executor_job(_read_json_sync, path)
    except FileNotFoundError as e:
        raise UpdateFailed(f"JSON not found: {path}") from e
    except json.JSONDecodeError as e:
        raise UpdateFailed(f"Invalid JSON: {path}") from e
    except Exception as e:
        raise UpdateFailed(f"Failed reading: {path} ({e})") from e

class EnecoqCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, entry):
        self.hass = hass
        self.entry = entry
        interval = int(entry.data[CONF_SCAN_INTERVAL])
        super().__init__(
            hass,
            _LOGGER,
            name="enecoQ",
            update_interval=timedelta(seconds=interval),
        )

    async def _async_update_data(self) -> dict:
        today_path = self.entry.data[CONF_TODAY_PATH]
        month_path = self.entry.data[CONF_MONTH_PATH]
        stale_minutes = int(self.entry.data[CONF_STALE_MINUTES])

        today = await _read_json(self.hass, today_path)
        month = await _read_json(self.hass, month_path)

        now = datetime.now(timezone.utc)
        stale_cutoff = now - timedelta(minutes=stale_minutes)

        def check_stale(d: dict, label: str):
            ts = d.get("timestamp")
            dt = _parse_ts(ts) if isinstance(ts, str) else None
            if dt is None:
                _LOGGER.warning("%s timestamp missing/invalid: %s", label, ts)
                return
            if dt < stale_cutoff:
                raise UpdateFailed(f"{label} data is stale: {dt.isoformat()}")

        check_stale(today, "today")
        check_stale(month, "month")

        return {"today": today, "month": month}
