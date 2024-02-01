"""Job entity from Feller Wiser."""
from  fellerwiser.fellerwiserapi.auth import Auth


class Job:
    """Class that represents a Job object in the Feller Wiser Gateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a Wiser Job object."""
        self._raw_data = raw_data
        self._auth = auth

    @property
    def id(self) -> str:
        """Return the ID of the Wiser Load."""
        return str(self._raw_data["id"])
