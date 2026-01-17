import pytest
import requests
from config import BASE_URL, API_TOKEN


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    })
    return session


@pytest.fixture(scope="module")
def base_url():

    return BASE_URL
