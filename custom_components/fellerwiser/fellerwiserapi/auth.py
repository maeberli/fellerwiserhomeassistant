"""Module implments the authentication for the Feller Wiser Gateway."""
from aiohttp import ClientSession, ClientResponse
from yarl import URL

class Auth:
    """Class to make authenticated requests."""

    def __init__(self, websession: ClientSession, host_url: URL, auth_token: str):
        """Initialize the auth."""
        self._websession = websession
        self._host_url = host_url
        self._auth_token = auth_token

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        headers["authorization"] = f"Bearer {self._auth_token}"

        return await self._websession.request(
            method,
            self._host_url / path,
            **kwargs,
            headers=headers,
        )
