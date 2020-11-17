import pytest
from fastapi.exceptions import HTTPException

from app.core.security.auth.tacacs import TacacsAuth


def test_tacacs_obj_init():
    auth = TacacsAuth(username="admin", password="admin")

    assert isinstance(auth, TacacsAuth)
    assert auth.username == "admin"
    assert auth.password == "admin"


def test_tacacs_obj_init_no_password_fail():
    with pytest.raises(HTTPException):
        TacacsAuth(username="admin", password="")


def test_tacacs_authenticate_failed_connection(tacacs_auth_obj):
    with pytest.raises(HTTPException):
        tacacs_auth_obj.authenticate()


def test_tacacs_auth(monkeypatch, tacacs_auth_obj):
    def mock_auth():
        return True

    monkeypatch.setattr(tacacs_auth_obj, "authenticate", mock_auth)
    tacacs_auth_obj.authenticate()
