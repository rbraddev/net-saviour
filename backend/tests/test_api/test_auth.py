import pytest


def test_get_token_with_valid_credentials(test_app_tacacs):
    response = test_app_tacacs.post("/auth/token", auth=("admin", "admin"))

    assert response.status_code == 200
    assert "access_token" in response.json().keys()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.parametrize(
    "username, password",
    [
        ["username_no_pass", ""],
        ["", "no_username_with_pass"],
        ["bogus_user", "bogus_pass"],
    ],
)
def test_get_token_with_invalid_credentials(test_app_tacacs, username, password):
    response = test_app_tacacs.post("/auth/token", auth=(username, password))

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Basic"
    assert response.json()["detail"] == "Incorrect username or password"
