"""Config flow for Feller Wiser integration."""
from __future__ import annotations

import socket
from typing import Any

import asyncio
import voluptuous as vol
import aiohttp
import async_timeout


from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import DOMAIN, LOGGER

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(
            "host", default="wiser-00079973.local.aeberli.me"
        ): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT),
        ),
        vol.Required(
            "apikey", default="cd87f1b7-777f-4db8-add3-f7302a138912"
        ): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
    }
)


class FellerWiserApiClientError(Exception):
    """Exception to indicate a general API error."""


class FellerWiserApiClientCommunicationError(FellerWiserApiClientError):
    """Exception to indicate a communication error."""


class FellerWiserApiClientAuthenticationError(FellerWiserApiClientError):
    """Exception to indicate an authentication error."""


class FellerWiserApiClient:
    """Sample API Client."""

    def __init__(
        self,
        host: str,
        apikey: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._host = host
        self._apikey = apikey
        self._session = session

    async def async_get_data(self) -> any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url="http://" + self._host + "/api/info",
            headers={"authorization": "Bearer " + self._apikey},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise FellerWiserApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            raise FellerWiserApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise FellerWiserApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise FellerWiserApiClientError(
                "Something really wrong happened!"
            ) from exception

    async def authenticated(self) -> bool:
        """Test if we can authenticate with the host."""

        resp_json = await self._api_wrapper(
            method="get",
            url="http://" + self._host + "/api/info",
            headers={"authorization": "Bearer " + self._apikey},
        )

        LOGGER.error("##################")
        LOGGER.error(resp_json)

        return True

    def get_host(self) -> str:
        """Host Name of the client."""
        return self._host


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    client = FellerWiserApiClient(
        data["host"], data["apikey"], session=async_create_clientsession(hass)
    )

    if not await client.authenticated():
        raise InvalidAuth

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    return {"title": "Registered Host " + client.get_host()}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Feller Wiser."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
