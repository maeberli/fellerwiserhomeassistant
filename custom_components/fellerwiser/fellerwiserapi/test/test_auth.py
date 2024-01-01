"""Test the Auth Class."""
from fellerwiser.fellerwiserapi.auth import Auth

import aiohttp
import pytest
import logging
from aiohttp import web



LOGGER = logging.getLogger(__name__)

_auth_token = "TOKEN"

async def _get_api_root(request: aiohttp.web.Request):
    assert request.headers["authorization"] == "Bearer TOKEN"
    return web.Response(text='{"Success": true}', content_type='application/json')

async def _get_api_hello(request: aiohttp.web.Request):
    assert request.headers["authorization"] == "Bearer TOKEN"
    return web.Response(text='{"hello": "world"}', content_type='application/json')

async def _get_api_hello_world(request: aiohttp.web.Request):
    assert request.headers["authorization"] == "Bearer TOKEN"
    return web.Response(text='{"welcome": "universe"}', content_type='application/json')

def _create_app():
    app = web.Application()
    app.router.add_route("GET", "/", _get_api_root)
    app.router.add_route("GET", "/hello", _get_api_hello)
    app.router.add_route("GET", "/hello/world", _get_api_hello_world)
    return app


@pytest.mark.asyncio
async def test_auth_token(aiohttp_client):
    """Test authentication token by invoking call on root."""
    client = await aiohttp_client(_create_app())
    auth = Auth(client.session, client.make_url(""), _auth_token)
    resp = await auth.request("GET", "")
    assert await resp.json() == {"Success": True}

@pytest.mark.asyncio
async def test_request(aiohttp_client):
    """Test authentication token by invoking call on root."""
    client = await aiohttp_client(_create_app())
    auth = Auth(client.session, client.make_url(""), _auth_token)

    resp = await auth.request("GET", "hello")
    assert await resp.json() == {"hello": "world"}

    resp = await auth.request("GET", "hello/world")
    assert await resp.json() == {"welcome": "universe"}

    with pytest.raises(ValueError):
        resp = await auth.request("GET", "/")
