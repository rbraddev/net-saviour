from app.config import Settings


def test_ping(test_app_tacacs):
    response = test_app_tacacs.get("/ping")
    assert response.status_code == 200
    assert response.json() == {
        "ping": "pong",
        "project": Settings().PROJECT,
        "environment": "dev",
    }


def test_protected_ping_success(test_app_tacacs, get_access_token):
    access_token = get_access_token(username="admin")
    print(access_token)
    response = test_app_tacacs.get("/protected_ping", headers={"Authorization": f"Bearer {access_token}"})
    # assert response.status_code == 200
    assert response.json() == {
        "ping": "pong",
        "project": Settings().PROJECT,
        "environment": "dev",
        "username": "admin",
    }
