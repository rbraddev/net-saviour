from typing import Generator

import pytest
from starlette.testclient import TestClient

from app.main import create_application

AUTH_SECRET_KEY = "testingkey123"


@pytest.fixture(scope="session")
def test_app() -> Generator:
    app = create_application()
    with TestClient(app) as test_client:
        yield test_client
