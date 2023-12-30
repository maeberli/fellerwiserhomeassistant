"""Feller Wiser Scene Integration, which loads Scenes and make them availlable as HomeAssstant Scene Entity."""
from __future__ import annotations
from homeassistant.components.scene import Scene

import logging
import requests

_LOGGER = logging.getLogger(__name__)


def get_feller_wiser_scenes(host: str, apikey: str):
    """Retrieve all current Scenes from Feller Wiser Gateway."""
    ip = host
    key = apikey
    return requests.get(
        "http://" + ip + "/api/jobs", headers={"authorization": "Bearer " + key}
    )


async def async_setup_entry(hass, entry, async_add_entities):
    """Load Scenes from Wiser."""
    host = entry.data["host"]
    apikey = entry.data["apikey"]

    response = await hass.async_add_executor_job(get_feller_wiser_scenes, host, apikey)
    _LOGGER.info(f"Feller Wiser Scenes from Gateway > {response}")

    scenes = response.json()

    feller_scenes = []
    for value in scenes["data"]:
        feller_scenes.append(FellerScene(value, host, apikey))

    async_add_entities(feller_scenes, True)


class FellerScene(Scene):
    """Representation of an Awesome Scene."""

    def __init__(self, data: object, host: str, apikey: str) -> None:
        """Initialize an Feller Scene."""
        # {'name': '00005341_0', 'device': '00005341', 'channel': 0, 'type': 'dim', 'id': 14, 'unused': False}
        _LOGGER.info(f"new feller Wiser Scene > {data}")
        _LOGGER.debug(f"new feller Wiser Scene > {data}")

        self._id = str(data["id"])
        self._name = "Feller Wiser Scene " + self._id

        self._host = host
        self._apikey = apikey

    @property
    def name(self) -> str:
        """Return the display name of this Scene."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique id of this Scene."""
        return "feller-wiser-scene-" + self._id

    def activate(self, **kwargs: Any) -> None:
        """Activate scene. Try to get entities into requested state."""
        _LOGGER.debug(f"Activate Feller Scene with id > {self._id}")
        requests.get(
            "http://" + self._host + "/api/jobs/" + self._id + "/trigger",
            headers={"authorization": "Bearer " + self._apikey},
        )
        return None

    async def async_activate(self, **kwargs: Any) -> None:
        """Activate scene. Try to get entities into requested state."""
        _LOGGER.debug(f"Async Activate Feller Scene with id > {self._id}")
        await self.hass.async_add_executor_job(self.activate)
        return None
