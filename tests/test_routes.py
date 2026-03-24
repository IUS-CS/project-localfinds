import pytest
from src.localfinds.app import app, accounts_db, posts_db
from werkzeug.security import generate_password_hash
from src.localfinds.database.accounts_db import clear_accounts, store_account, update_account, delete_account
from src.localfinds.database.posts_db import clear_posts, store_post, get_all_posts, update_post, delete_post

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        # Clear databases before each test
        clear_accounts(accounts_db)
        clear_posts(posts_db)
        # Setup default account and post
        store_account(accounts_db, "admin", generate_password_hash("password"))
        store_post(posts_db, "Test Post", "Test content", "admin", "123 Main St", "tag1, tag2")
        yield client

def login(client, username, password):
    return client.post("/auth/login", data=dict(username=username, password=password), follow_redirects=True)

def test_create_post_authorized(client):
    login(client, "admin", "password")
    response = client.post("/posts/create", data={
        "subject": "New Post",
        "content": "Content here",
        "address": "456 Road St",
        "tags": "test"
    }, follow_redirects=True)
    assert b"New Post" in response.data

def test_create_post_unauthorized(client):
    response = client.post("/posts/create", data={
        "subject": "New Post",
        "content": "Content here",
        "address": "456 Road St",
        "tags": "test"
    }, follow_redirects=True)
    assert response.status_code == 403

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Test Post" in response.data

def test_view_post(client):
    posts = get_all_posts(posts_db)
    post_id = posts[0]["id"]
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert b"Test Post" in response.data

def test_edit_post_unauthorized(client):
    posts = get_all_posts(posts_db)
    post_id = posts[0]["id"]

    response = client.get(f"/posts/{post_id}/edit")
    assert response.status_code == 403

def test_edit_post_authorized(client):
    login(client, "admin", "password")
    posts = get_all_posts(posts_db)
    post_id = posts[0]["id"]

    response = client.post(f"/posts/{post_id}/edit", data={
        "subject": "Edited Post",
        "content": "Edited content",
        "address": "123 Main St",
        "tags": "welcome, intro"
    }, follow_redirects=True)

    assert b"Edited Post" in response.data

def test_remove_post_unauthorized(client):
    posts = get_all_posts(posts_db)
    post_id = posts[0]["id"]
    
    response = client.get(f"/posts/{post_id}/delete")
    assert response.status_code == 403

def test_remove_post_authorized(client):
    login(client, "admin", "password")

    posts = get_all_posts(posts_db)
    post_id = posts[0]["id"]
    
    response = client.get(f"/posts/{post_id}/delete", follow_redirects=True)
    assert b"Test Post" not in response.data

def test_create_account(client):
    response = client.post("/accounts/create", data={"username": "alice", "password": "pass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"alice" in response.data

def test_view_account(client):
    response = client.get("/accounts/admin")
    assert response.status_code == 200
    assert b"admin" in response.data

def test_edit_account_unauthorized(client):
    response = client.get("/accounts/admin/edit")
    assert response.status_code == 403

def test_edit_account_authorized(client):
    login(client, "admin", "password")
    response = client.post("/accounts/admin/edit", data={"username": "admin2", "password": "newpass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"admin2" in response.data

def test_delete_account_unauthorized(client):
    response = client.get("/accounts/admin/delete")
    assert response.status_code == 403

def test_delete_account_authorized(client):
    login(client, "admin", "password")

    posts = get_all_posts(posts_db)
    post_id = posts[0]["id"]
    
    response = client.get(f"/posts/{post_id}/delete", follow_redirects=True)
    
    response = client.post("/accounts/admin/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"admin" not in response.data

def test_login(client):
    response = login(client, "admin", "password")
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess["username"] == "admin"
    
def test_logout(client):
    response = client.get("/auth/logout", follow_redirects=True)
    with client.session_transaction() as sess:
        assert "username" not in sess





