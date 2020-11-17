import pytest
from fastapi.exceptions import HTTPException

from tests.conftest import get_settings_override_tacacs
from app.core.security.auth.tacacs import TacacsAuth
from app.core.security.utils import create_access_token, get_auth_mode, get_current_user


def test_create_access_token():
    token = create_access_token(data={"sub": "user"}, expiry=10, key="its_shhhhuuuper_secret", algorithm="HS256")

    assert isinstance(token, bytes)


@pytest.mark.parametrize(
    "auth_mode_input, auth_obj",
    [["tacacs", TacacsAuth]],
)
def test_get_auth_mode_pass(auth_mode_input, auth_obj):
    auth_mode = get_auth_mode(auth_mode_input)

    assert auth_mode is auth_obj


def test_get_auth_mode_fail():
    with pytest.raises(HTTPException):
        get_auth_mode("bogus_mode")


@pytest.mark.parametrize("username, settings", [["admin", get_settings_override_tacacs]])
@pytest.mark.asyncio
async def test_get_current_user_valid(get_access_token, username, settings):
    access_token = get_access_token(username)
    user = await get_current_user(access_token, settings())

    assert user == username


@pytest.mark.parametrize(
    "settings",
    [
        get_settings_override_tacacs,
    ],
)
@pytest.mark.asyncio
async def test_get_current_user_invalid_token(settings):
    access_token = "this_is_not_a_token"

    with pytest.raises(HTTPException):
        await get_current_user(access_token, settings())
