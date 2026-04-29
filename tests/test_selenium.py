import importlib
import os
import socket
import tempfile
import threading

import pytest


selenium = pytest.importorskip("selenium")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def live_server(monkeypatch):
    accounts_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    posts_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    accounts_db.close()
    posts_db.close()

    monkeypatch.setenv("LOCALFINDS_ACCOUNTS_DB", accounts_db.name)
    monkeypatch.setenv("LOCALFINDS_POSTS_DB", posts_db.name)
    monkeypatch.setenv("LOCALFINDS_SEED_DATA", "0")

    import src.localfinds.app as app_module

    app_module = importlib.reload(app_module)

    from src.localfinds.models.posts import store_post

    store_post(
        app_module.posts,
        "Welcome to LocalFinds!",
        "This is a seeded post for UI testing.",
        "admin",
        "123 Main St, Anytown, USA",
        "welcome, intro",
    )

    port = get_free_port()
    base_url = f"http://127.0.0.1:{port}"

    from werkzeug.serving import make_server

    server = make_server("127.0.0.1", port, app_module.app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield base_url
    finally:
        server.shutdown()
        server.server_close()
        os.unlink(accounts_db.name)
        os.unlink(posts_db.name)


@pytest.fixture
def driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")

    try:
        d = webdriver.Chrome(options=options)
    except Exception as e:
        pytest.skip(f"Chrome WebDriver unavailable: {e}")

    try:
        yield d
    finally:
        d.quit()


def test_home_page_shows_posts(driver, live_server):
    driver.get(f"{live_server}/")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".posts-table"))
    )
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "Newest Finds" in body
    assert "Welcome to LocalFinds!" in body


def test_search_finds_posts(driver, live_server):
    driver.get(f"{live_server}/")
    search = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "search"))
    )
    search.clear()
    search.send_keys("Welcome")
    driver.find_element(By.CSS_SELECTOR, "form.search-bar button.btn").click()

    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Welcome to LocalFinds!")
    )


def test_create_account_and_post(driver, live_server):
    username = f"user_{os.getpid()}"

    driver.get(f"{live_server}/accounts/create")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.CSS_SELECTOR, "button.btn").click()

    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), username)
    )

    driver.get(f"{live_server}/posts/create")
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "subject"))
    )
    driver.find_element(By.NAME, "subject").send_keys("Selenium Post")
    driver.find_element(By.NAME, "address").send_keys("456 Road St")
    driver.find_element(By.NAME, "tags").send_keys("test")
    driver.find_element(By.NAME, "content").send_keys("Created by selenium test.")
    driver.find_element(By.CSS_SELECTOR, "button.btn").click()

    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Selenium Post")
    )
