"""Load entity from Feller Wiser."""
from  fellerwiser.fellerwiserapi.auth import Auth

from typing import Any

class Load:
    """Class that represents a Load object in the Feller Wiser Gateway API."""

    """{'name': '00005341_0', 'device': '00005341', 'channel': 0, 'type': 'dim', 'id': 14, 'unused': False}"""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a Wiser Load object."""
        self._raw_data = raw_data
        self._auth = auth

    @property
    def id(self) -> str:
        """Return the ID of the Wiser Load."""
        return str(self._raw_data["id"])

    @property
    def name(self) -> str:
        """Return the name of the Wiser Load."""
        return self._raw_data["name"]

    @property
    def type(self) -> str:
        """Return the type of the Wiser Load."""
        return self._raw_data["type"]

    @property
    def unused(self) -> str:
        """Return the information if the Wiser Load is unused or not."""
        return self._raw_data["unused"]

    @property
    def raw_state(self) -> dict:
        """Return the rawstate of the load."""
        return self._raw_data["state"] if "state" in self._raw_data else None

    async def async_set_target_state(self, target_state: Any):
        """Set the target state of the load the light."""
        resp = await self._auth.request(
            "PUT", f"api/loads/{self.id}/target_state", json=target_state
        )
        resp.raise_for_status()

    async def async_update(self):
        """Update the Load data."""
        resp = await self._auth.request("GET", f"api/loads/{self.id}")
        resp.raise_for_status()
        json_response = await resp.json()
        self._raw_data = json_response["data"]
