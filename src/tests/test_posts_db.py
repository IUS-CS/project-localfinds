import sqlite3
import pytest 
import tempfile
import os
import time
from src.database.posts_db import initialize_db, create_post, get_post, get_all_posts, update_post, delete_post

# Run 'pytest -v' to run test functions in this file. Make sure to have pytest is installed.

# Temporary databased stored in OS's temp directory, automatically deleted after testing.
@pytest.fixture(autouse=True)
def temp_db():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = temp_file.name
    temp_file.close()
    initialize_db(db_path)
    yield db_path  
    os.remove(db_path)


def test_create_post(temp_db):
    create_post(temp_db, "Hello", "First post", "user1", "123 Street", "intro")
    post = get_post(temp_db, 1)
    assert post[1] == "Hello"
    assert post[2] == "First post"
    assert post[3] == "user1"
    assert post[4] == "123 Street"
    assert post[5] == "intro"

def test_get_post(temp_db):
    create_post(temp_db,"Test Post", "This is the content", "user1", "123 Street", "test, sample")
    post = get_post(temp_db, 1) 
    assert post is not None
    assert post[1] == "Test Post"           
    assert post[2] == "This is the content" 
    assert post[3] == "user1"               
    assert post[4] == "123 Street"          
    assert post[5] == "test, sample"        


def test_get_all_posts(temp_db):
    create_post(temp_db, "Post A", "Content A", "user1", "Addr1")
    # Ensure diferent timestamp.
    time.sleep(1)
    create_post(temp_db, "Post B", "Content B", "user2", "Addr2")
    posts = get_all_posts(temp_db)
    assert len(posts) == 2
    # Check order by updated_at DESC
    assert posts[0][1] == "Post B"
    assert posts[1][1] == "Post A"


def test_update_post(temp_db):
    create_post(temp_db, "Old Title", "Old Content", "user1", "Addr1")
    update_post(temp_db, 1, "New Title", "New Content", "New Addr", "tag1")
    post = get_post(temp_db, 1)
    assert post[1] == "New Title"
    assert post[2] == "New Content"
    assert post[4] == "New Addr"
    assert post[5] == "tag1"


def test_delete_post(temp_db):
    create_post(temp_db, "Temp", "Temp Content", "user1", "Addr1")
    delete_post(temp_db, 1)
    posts = get_all_posts(temp_db)
    assert len(posts) == 0
