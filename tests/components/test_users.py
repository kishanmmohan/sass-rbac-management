import json


def test_create_user(test_app_with_db):
    response = test_app_with_db.post("/users/", content=json.dumps(
        {"name": "test_user", "email": "test@test.com", "auth0_id": "123456", "is_active": True}))

    assert response.status_code == 201
    assert response.json()["name"] == "test_user"
    assert response.json()["email"] == "test@test.com"
    assert response.json()["auth0_id"] == "123456"
    assert response.json()["is_active"] == True


def test_read_users_with_default_pagination(test_app_with_db):
    test_app_with_db.post("/users/", content=json.dumps(
        {"name": "user1", "email": "user1@test.com", "auth0_id": "123456", "is_active": True}))
    test_app_with_db.post("/users/", content=json.dumps(
        {"name": "user2", "email": "user2@test.com", "auth0_id": "1234567", "is_active": True}))
    response = test_app_with_db.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


def test_read_users_with_custom_pagination(test_app_with_db):
    for i in range(15):
        test_app_with_db.post("/users/", content=json.dumps(
            {"name": f"user{i}", "email": f"user{i}@test.com", "auth0_id": f"123456{i}", "is_active": True}))
    response = test_app_with_db.get("/users/?skip=10&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5


def test_read_users_with_invalid_pagination(test_app_with_db):
    test_app_with_db.post("/users/", content=json.dumps(
        {"name": "user1", "email": "user1@test.com", "auth0_id": "1234567", "is_active": True}))
    response = test_app_with_db.get("/users/?skip=-1&limit=5")
    assert response.status_code == 422


def test_read_user_success(test_app_with_db):
    response = test_app_with_db.post("/users/", content=json.dumps(
        {"name": "user1", "email": "user1@test.com", "auth0_id": "123456", "is_active": True}))
    user_id = response.json()["id"]
    response = test_app_with_db.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "user1"
    assert response.json()["auth0_id"] == "123456"
    assert response.json()["email"] == "user1@test.com"


def test_read_user_not_found(test_app_with_db):
    response = test_app_with_db.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
