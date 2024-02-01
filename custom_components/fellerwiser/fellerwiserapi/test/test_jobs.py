"""Test the Scene Class."""
from fellerwiser.fellerwiserapi.auth import Auth
from fellerwiser.fellerwiserapi.job import Job

from . import constants

from aiohttp import web
import pytest
import json

_raw_get_jobs_data = {
    "status": "success",
    "data": [
        {
            "id": 7,
            "target_states": [{"load": 9, "bri": 7500}],
            "flag_values": [{"flag": 39, "value": True}],
            "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
            "scripts": ["test.py"],
            "blocked_by": 10,
            "triggers": [5],
        }
    ],
}

_raw_job_raw1 = {
    "id": 7,
    "target_states": [{"load": 9, "bri": 7500}],
    "flag_values": [{"flag": 39, "value": True}],
    "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
    "scripts": ["test.py"],
    "blocked_by": 10,
    "triggers": [5],
}

async def _get_api_jobs(request):
    return web.Response(text=json.dumps(_raw_get_jobs_data), content_type="application/json")

async def _get_api_jobs_id(request):
    return web.Response(text=json.dumps(_raw_job_raw1), content_type="application/json")

def _create_app():
    app = web.Application()
    app.router.add_route("GET", "/jobs", _get_api_jobs)
    app.router.add_route("GET", "/jobs/7", _get_api_jobs_id)
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
    job = Job(_raw_job_raw1, await _auth_fixture)
    assert job.id == "7"
