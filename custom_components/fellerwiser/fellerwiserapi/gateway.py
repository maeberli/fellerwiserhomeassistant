"""Feller Wiser Gateway Implementation."""
from  fellerwiser.fellerwiserapi.auth import Auth
from  fellerwiser.fellerwiserapi.load import Load

class FellerWiserGatewayAPI:
    """Class to communicate with the Feller Wiser Gateway API."""

    def __init__(self, auth: Auth):
        """Initialize the API and store the auth so we can make requests."""
        self._auth = auth

    async def async_get_loads(self) -> list[Load]:
        """Return the Loads."""
        resp = await self.auth.request("get", "api/loads")
        resp.raise_for_status()
        return [Load(raw_data, self._auth) for raw_data in await resp.json()]
