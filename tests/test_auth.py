from psycopg2 import IntegrityError
import pytest





def test_root(client):
    res = client.get("/")
    # print(res)
    # print(res.json())
    # print(res.json().get('message'))
    assert res.status_code == 200
    assert res.json().get('message') == 'running'

def test_create_user(client):
    res = client.post("/auth/register",json={"email": "heri@example.com", "password": "password123"})
    assert res.status_code == 201
    assert res.json().get('status') == "success"

@pytest.mark.parametrize("email, password, status_code",[
    ("heri@example.com", "password123", 403),
])
def test_create_user_exception(client, email, test_user, password, status_code):
    res = res = client.post("/auth/register",json={"email": email, "password": password})
    assert res.status_code == status_code
   

def test_login_user(client, test_user):
    res = client.post("/auth/login",data=test_user)
    assert res.status_code == 200
    assert res.json().get('status') == "success"
    assert res.json().get('token_type') == "Bearer"

@pytest.mark.parametrize("username, password, status_code",[
    ("heri@example.com", "password", 403),
    ("i@example.com", "password123", 403),
    ("i@example.com", "password", 403),
    (None, "password123", 403),
    ("heri@example.com", None, 403),
])
def test_login_exception(client, test_user, username, password, status_code):
    res = client.post("/auth/login", data={"username": username,"password": password})
    assert res.status_code == status_code