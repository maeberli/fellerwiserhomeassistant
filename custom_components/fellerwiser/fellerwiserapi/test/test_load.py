"""Test the Job Class."""
from fellerwiser.fellerwiserapi.auth import Auth
from fellerwiser.fellerwiserapi.load import Load

from . import constants

from aiohttp import web
import pytest
import json
import logging

LOGGER = logging.getLogger(__name__)

_raw_data1 = {
    "name": "00005341_0",
    "device": "00005341",
    "channel": 0,
    "type": "dim",
    "id": 14,
    "unused": False,
}
_raw_data2 = {
  "status": "success",
  "data": {
    "id": 14,
    "name": "00005341_0",
    "unused": True,
    "type": "dim",
    "sub_type": "",
    "device": "0000072d",
    "channel": 0,
    "room": 123,
    "kind": 0,
    "state": {
      "bri": 10000
    }
  }
}

_target_state1 = {
    "status": "success",
    "data": {"id": 2, "target_state": {"bri": 500}},
}


async def _get_api_loads_id(request):
    return web.Response(text=json.dumps(_raw_data2), content_type="application/json")


async def _put_api_loads_id_target_state(request):
    return web.Response(text=json.dumps(_target_state1), content_type="application/json")


def _create_app():
    app = web.Application()
    app.router.add_route("GET", "/api/loads/14", _get_api_loads_id)
    app.router.add_route(
        "PUT", "/api/loads/14/target_state", _put_api_loads_id_target_state
    )
    return app

@pytest.fixture
@pytest.mark.asyncio
async def _auth_fixture(aiohttp_client):
    client = await aiohttp_client(_create_app())
    auth = Auth(client.session, client.make_url(""), constants.AUTH_TOKEN)
    return auth

@pytest.mark.asyncio
async def test_init(_auth_fixture):
    """Test the Load Constructor."""
    load = Load(_raw_data1, await _auth_fixture)

    assert load.name == "00005341_0"
    assert load.id == "14"
    assert load.type == "dim"
    assert load.unused is False
    assert load.raw_state is None

@pytest.mark.asyncio
async def test_async_update(_auth_fixture):
    """Test the Load Constructor."""
    load = Load(_raw_data1, await _auth_fixture)

    await load.async_update()

    assert load.name == "00005341_0"
    assert load.id == "14"
    assert load.type == "dim"
    assert load.unused is True


@pytest.mark.asyncio
async def test_async_set_target_state(_auth_fixture):
    """Test the Load Constructor."""
    load = Load(_raw_data1, await _auth_fixture)

    await load.async_set_target_state({"bri": 500})
