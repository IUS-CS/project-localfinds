import pytest 
import tempfile
import os
import time
from src.localfinds.models.accounts import initialize_accounts, store_account, get_account, get_account_by_username, get_all_accounts, update_account, delete_account, clear_accounts

# Run 'pytest -v' to run test functions in this file. Make sure to have pytest is installed.

# Temporary databased stored in OS's temp directory, automatically deleted after testing.
@pytest.fixture(autouse=True)
def temp_db():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = temp_file.name
    temp_file.close()
    initialize_accounts(db_path)
    yield db_path  
    os.remove(db_path)


def test_store_account(temp_db):
    store_account(temp_db, "user1", "password2")
    account = get_account(temp_db, 1)
    assert account["username"] == "user1"
    assert account["password"] == "password2"

def test_get_account(temp_db):
    store_account(temp_db, "user1", "password2")
    account = get_account(temp_db, 1)
    assert account is not None
    assert account["username"] == "user1"
    assert account["password"] == "password2" 

def test_get_account_by_username(temp_db):
    store_account(temp_db, "user1", "password2")
    account = get_account_by_username(temp_db, "user1")
    assert account is not None
    assert account["username"] == "user1"
    assert account["password"] == "password2"       

def test_get_all_accounts(temp_db):
    store_account(temp_db, "user1", "password2")
    # Ensure diferent timestamp.
    time.sleep(1)
    store_account(temp_db, "user2", "password3")
    accounts = get_all_accounts(temp_db)
    assert len(accounts) == 2
    # Check order by updated_at DESC
    assert accounts[0]["username"] == "user1"
    assert accounts[1]["username"] == "user2" 

def test_update_account(temp_db):
    store_account(temp_db, "user1", "password2")
    update_account(temp_db, 1, "user2", "password3")
    account = get_account(temp_db, 1)
    assert account["username"] == "user2"
    assert account["password"] == "password3"


def test_delete_account(temp_db):
    store_account(temp_db, "user1", "password2")
    delete_account(temp_db, 1)
    accounts = get_all_accounts(temp_db)
    assert len(accounts) == 0

def test_clear_posts(temp_db):
    store_account(temp_db, "user1", "password2")
    store_account(temp_db, "user2", "password3")
    clear_accounts(temp_db)
    accounts = get_all_accounts(temp_db)
    assert len(accounts) == 0
