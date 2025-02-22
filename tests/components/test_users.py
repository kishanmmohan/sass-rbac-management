import json


def test_create_user(test_app_with_db):
    response = test_app_with_db.post("/users/", content=json.dumps(
        {"username": "test_user", "email": "test@test.com", "is_active": True}))

    assert response.status_code == 201
    assert response.json()["username"] == "test_user"
    assert response.json()["email"] == "test@test.com"
    assert response.json()["is_active"] == True


def test_create_user_with_existing_username(test_app_with_db):
    test_app_with_db.post("/users/", content=json.dumps(
        {"username": "test_user", "email": "test@test.com", "is_active": True}))
    response = test_app_with_db.post("/users/", content=json.dumps(
        {"username": "test_user", "email": "newemail@test.com", "is_active": True}))
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_read_users_with_default_pagination(test_app_with_db):
    test_app_with_db.post("/users/", content=json.dumps(
        {"username": "user1", "email": "user1@test.com", "is_active": True}))
    test_app_with_db.post("/users/", content=json.dumps(
        {"username": "user2", "email": "user2@test.com", "is_active": True}))
    response = test_app_with_db.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


def test_read_users_with_custom_pagination(test_app_with_db):
    for i in range(15):
        test_app_with_db.post("/users/", content=json.dumps(
            {"username": f"user{i}", "email": f"user{i}@test.com", "is_active": True}))
    response = test_app_with_db.get("/users/?skip=10&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5


def test_read_users_with_invalid_pagination(test_app_with_db):
    test_app_with_db.post("/users/", content=json.dumps(
        {"username": "user1", "email": "user1@test.com", "is_active": True}))
    response = test_app_with_db.get("/users/?skip=-1&limit=5")
    assert response.status_code == 422


def test_read_user_success(test_app_with_db):
    response = test_app_with_db.post("/users/", content=json.dumps(
        {"username": "user1", "email": "user1@test.com", "is_active": True}))
    user_id = response.json()["id"]
    response = test_app_with_db.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "user1"
    assert response.json()["email"] == "user1@test.com"


def test_read_user_not_found(test_app_with_db):
    response = test_app_with_db.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
