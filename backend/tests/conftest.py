from typing import Generator

import pytest
from starlette.testclient import TestClient

from app.config import Settings, get_settings
from app.core.security.auth.tacacs import TacacsAuth
from app.core.security.utils import create_access_token
from app.main import create_application

AUTH_KEY = "testingkey123"


def get_settings_override_tacacs():
    return Settings(
        AUTH_KEY=AUTH_KEY,
        TOKEN_ALGORITHM="HS256",
        AUTH_MODE="tacacs",
        TACACS_SVR="tacacs",
        TACACS_KEY="tac_plus_key",
    )


@pytest.fixture(scope="session")
def test_app_tacacs() -> Generator:
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override_tacacs
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def get_access_token() -> str:
    def _create_access_token(username: str, expiry: int = 150):
        return create_access_token(data={"sub": username}, expiry=expiry, key=AUTH_KEY, algorithm="HS256").decode(
            "utf-8"
        )

    return _create_access_token


@pytest.fixture(scope="module")
def tacacs_auth_obj() -> TacacsAuth:
    return TacacsAuth(username="admin", password="admin")
