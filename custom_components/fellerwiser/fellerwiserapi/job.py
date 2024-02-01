from  fellerwiser.fellerwiserapi.auth import Auth

from typing import Any

class Job:
    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a Wiser Load object."""
        self._raw_data = raw_data
        self._auth = auth

    @property
    def id(self) -> str:
        """Return the ID of the Wiser Load."""
        return str(self._raw_data["id"])