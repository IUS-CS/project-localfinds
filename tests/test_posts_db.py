import pytest 
import tempfile
import os
import time
from src.localfinds.database.posts_db import initialize_db, store_post, get_post, get_all_posts, update_post, delete_post, clear_posts

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


def test_store_post(temp_db):
    store_post(temp_db, "Hello", "First post", "user1", "123 Street", "intro")
    post = get_post(temp_db, 1)
    assert post["subject"] == "Hello"
    assert post["content"] == "First post"
    assert post["author_id"] == "user1"
    assert post["address"] == "123 Street"
    assert post["tags"] == "intro"

def test_get_post(temp_db):
    store_post(temp_db,"Test Post", "This is the content", "user1", "123 Street", "test, sample")
    post = get_post(temp_db, 1) 
    assert post is not None
    assert post["subject"] == "Test Post"           
    assert post["content"] == "This is the content" 
    assert post["author_id"] == "user1"               
    assert post["address"] == "123 Street"          
    assert post["tags"] == "test, sample"        


def test_get_all_posts(temp_db):
    store_post(temp_db, "Post A", "Content A", "user1", "Addr1")
    # Ensure diferent timestamp.
    time.sleep(1)
    store_post(temp_db, "Post B", "Content B", "user2", "Addr2")
    posts = get_all_posts(temp_db)
    assert len(posts) == 2
    # Check order by updated_at DESC
    assert posts[0]["subject"] == "Post B"
    assert posts[1]["subject"] == "Post A"


def test_update_post(temp_db):
    store_post(temp_db, "Old Title", "Old Content", "user1", "Addr1")
    update_post(temp_db, 1, "New Title", "New Content", "New Addr", "tag1")
    post = get_post(temp_db, 1)
    assert post["subject"] == "New Title"
    assert post["content"] == "New Content"
    assert post["address"] == "New Addr"
    assert post["tags"] == "tag1"


def test_delete_post(temp_db):
    store_post(temp_db, "Temp", "Temp Content", "user1", "Addr1")
    delete_post(temp_db, 1)
    posts = get_all_posts(temp_db)
    assert len(posts) == 0

def test_clear_posts(temp_db):
    store_post(temp_db, "Temp1", "Temp Content 1", "user1", "Addr1")
    store_post(temp_db, "Temp2", "Temp Content 2", "user2", "Addr2")
    clear_posts(temp_db)
    posts = get_all_posts(temp_db)
    assert len(posts) == 0
