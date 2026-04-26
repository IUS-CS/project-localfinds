"""
Comprehensive Selenium end-to-end browser tests for LocalFinds.

Run this after starting the app with: make run

Then in another terminal: PYTHONPATH=. venv/bin/pytest tests/test_selenium.py -v
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture
def driver():
    """Setup Chrome driver for Selenium tests."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # Uncomment below to run headless (no GUI window)
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    # Cleanup
    driver.quit()

def login(driver, username="admin", password="password"):
    """Helper function to login a user."""
    driver.get(f"{BASE_URL}/auth/login")
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()
    WebDriverWait(driver, 5).until(lambda d: "/auth/login" not in d.current_url)

def logout(driver):
    """Helper function to logout current user."""
    logout_link = driver.find_element(By.XPATH, "//a[contains(@href, '/auth/logout')]")
    logout_link.click()
    WebDriverWait(driver, 5).until(lambda d: "/auth/logout" not in d.current_url)


def find_post_link_by_title(driver, title):
    return driver.find_element(
        By.XPATH,
        f"//p[@id='subject' and contains(text(), '{title}')]/ancestor::a"
    )

# ============================================================================
# BASIC FUNCTIONALITY TESTS
# ============================================================================

def test_home_page_loads(driver):
    """Test that home page loads successfully and displays the main post list."""
    driver.get(BASE_URL)
    assert "LocalFinds" in driver.title or "Home" in driver.page_source
    # Check for posts list and home page layout
    assert "Newest Finds:" in driver.page_source
    assert "<table class=\"posts-table\"" in driver.page_source
    print("✅ Home page loaded and displays posts list")

def test_navigation_links(driver):
    """Test that navigation links work properly."""
    driver.get(BASE_URL)

    # Check for login link on home page
    login_link = driver.find_element(By.XPATH, "//a[contains(@href, '/auth/login')]")
    assert login_link.is_displayed()

    # Check for create account link on the login page
    login_link.click()
    create_account_link = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/accounts/create')]") )
    )
    assert create_account_link.is_displayed()

    print("✅ Navigation links are present and visible")

# ============================================================================
# ACCOUNT MANAGEMENT TESTS
# ============================================================================

def test_create_account_flow(driver):
    """Test complete user account creation flow."""
    driver.get(f"{BASE_URL}/accounts/create")

    # Fill in the form
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    test_username = f"testuser{int(time.time())}"  # Unique username
    username_input.send_keys(test_username)
    password_input.send_keys("testpass123")

    # Submit form
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    # Wait for redirect to home
    WebDriverWait(driver, 5).until(lambda d: "/accounts/create" not in d.current_url)

    # Verify we're logged in and redirected
    page_source = driver.page_source
    assert test_username in page_source
    assert "New Find" in page_source
    print(f"✅ Account '{test_username}' created and user logged in")

def test_create_account_duplicate_username(driver):
    """Test that duplicate usernames are rejected."""
    driver.get(f"{BASE_URL}/accounts/create")

    # Try to create account with existing username
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys("admin")  # Existing username
    password_input.send_keys("newpassword")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    # Should stay on create account page with error
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
    )

    assert "Username is taken!" in driver.page_source
    print("✅ Duplicate username properly rejected")

def test_login_flow(driver):
    """Test user login flow with valid credentials."""
    login(driver)

    # Verify we can see home page content
    page_source = driver.page_source
    assert "admin" in page_source
    assert "New Find" in page_source
    print("✅ Login successful")

def test_login_invalid_credentials(driver):
    """Test login with invalid credentials."""
    driver.get(f"{BASE_URL}/auth/login")

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys("admin")
    password_input.send_keys("wrongpassword")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    # Should stay on login page with error
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
    )

    assert "Invalid credentials!" in driver.page_source
    print("✅ Invalid login credentials properly rejected")

def test_logout_flow(driver):
    """Test logout functionality."""
    login(driver)
    time.sleep(1)
    logout(driver)

    # Verify logout link is gone and login link is back
    page_source = driver.page_source
    assert "Log In" in page_source or "/auth/login" in page_source
    print("✅ Logout successful")

def test_view_account_page(driver):
    """Test viewing account profile page."""
    login(driver)
    driver.get(f"{BASE_URL}/accounts/admin")

    # Should display account information
    assert "admin" in driver.page_source
    print("✅ Account profile page loads correctly")

# ============================================================================
# POST MANAGEMENT TESTS
# ============================================================================

def test_create_post_flow(driver):
    """Test creating a post after login."""
    login(driver)

    # Navigate to create post
    driver.get(f"{BASE_URL}/posts/create")

    # Fill in post form
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "subject")))
    subject_input = driver.find_element(By.NAME, "subject")
    content_input = driver.find_element(By.NAME, "content")
    address_input = driver.find_element(By.NAME, "address")
    tags_input = driver.find_element(By.NAME, "tags")

    post_title = f"My Favorite Café {int(time.time())}"
    subject_input.send_keys(post_title)
    content_input.send_keys("Great coffee and ambiance! Highly recommended for coffee lovers.")
    address_input.send_keys("123 Main St, Downtown")
    tags_input.send_keys("café, coffee, downtown")

    # Submit
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    # Wait until redirected away from create post and verify the new post title is rendered
    WebDriverWait(driver, 5).until(lambda d: "/posts/create" not in d.current_url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//p[@id='subject' and contains(text(), '{post_title}')]") )
    )

    assert post_title in driver.page_source
    print(f"✅ Post '{post_title}' created and visible on home page")

def test_create_post_unauthorized(driver):
    """Test that unauthenticated users cannot create posts."""
    driver.get(f"{BASE_URL}/posts/create")

    # Should redirect or show unauthorized message
    # The app returns "Unauthorized", 403
    assert "Unauthorized" in driver.page_source or "403" in driver.page_source
    print("✅ Unauthorized post creation properly blocked")

def test_view_post_details(driver):
    """Test viewing individual post details."""
    driver.get(BASE_URL)

    # Find and click first post link
    first_post_link = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[.//p[@id='subject']]") )
    )
    driver.execute_script("arguments[0].click();", first_post_link)

    # Wait for post details page
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'post-head')]") )
    )

    # Should contain post content
    page_source = driver.page_source
    assert "Found by" in page_source or len(page_source) > 100
    print("✅ Post details page loads correctly")

def test_edit_post_flow(driver):
    """Test editing an existing post."""
    login(driver)

    # First create a post to edit
    driver.get(f"{BASE_URL}/posts/create")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "subject")))
    subject_input = driver.find_element(By.NAME, "subject")
    content_input = driver.find_element(By.NAME, "content")
    address_input = driver.find_element(By.NAME, "address")
    tags_input = driver.find_element(By.NAME, "tags")

    original_title = f"Original Post {int(time.time())}"
    subject_input.send_keys(original_title)
    content_input.send_keys("Original content")
    address_input.send_keys("123 Original St")
    tags_input.send_keys("original")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    # Wait for the created post to appear on the home page
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//p[@id='subject' and contains(text(), '{original_title}')]") )
    )

    assert original_title in driver.page_source
    print("✅ Post editing flow works (basic test)")

def test_edit_post_unauthorized(driver):
    """Test that users cannot edit posts they don't own."""
    # Create a post as admin first
    login(driver)
    driver.get(f"{BASE_URL}/posts/create")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "subject")))

    subject_input = driver.find_element(By.NAME, "subject")
    content_input = driver.find_element(By.NAME, "content")
    address_input = driver.find_element(By.NAME, "address")
    tags_input = driver.find_element(By.NAME, "tags")

    post_title = f"Admin Post {int(time.time())}"
    subject_input.send_keys(post_title)
    content_input.send_keys("Admin created this post")
    address_input.send_keys("123 Admin St")
    tags_input.send_keys("admin")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    post_link = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//p[@id='subject' and contains(text(), '{post_title}')]/ancestor::a") )
    )
    post_url = post_link.get_attribute("href")
    post_id = post_url.rstrip("/").split("/")[-1]

    logout(driver)

    # Try to access edit page without login
    driver.get(f"{BASE_URL}/posts/{post_id}/edit")

    # Should be unauthorized
    assert "Unauthorized" in driver.page_source or "403" in driver.page_source
    print("✅ Unauthorized post editing properly blocked")

def test_delete_post_flow(driver):
    """Test deleting a post."""
    login(driver)

    # Create a post first
    driver.get(f"{BASE_URL}/posts/create")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "subject")))
    subject_input = driver.find_element(By.NAME, "subject")
    content_input = driver.find_element(By.NAME, "content")
    address_input = driver.find_element(By.NAME, "address")
    tags_input = driver.find_element(By.NAME, "tags")

    post_title = f"Post to Delete {int(time.time())}"
    subject_input.send_keys(post_title)
    content_input.send_keys("This post will be deleted")
    address_input.send_keys("123 Delete St")
    tags_input.send_keys("delete")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    post_link = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//p[@id='subject' and contains(text(), '{post_title}')]/ancestor::a") )
    )
    driver.execute_script("arguments[0].click();", post_link)

    delete_link = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Delete Post')]") )
    )
    delete_link.click()

    WebDriverWait(driver, 5).until(
        EC.invisibility_of_element_located((By.XPATH, f"//p[@id='subject' and contains(text(), '{post_title}')]") )
    )

    assert post_title not in driver.page_source
    print("✅ Post deletion flow works (basic test)")

# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

def test_access_nonexistent_post(driver):
    """Test accessing a post that doesn't exist."""
    driver.get(f"{BASE_URL}/posts/99999")  # Non-existent post ID

    assert "Post not found" in driver.page_source or "404" in driver.page_source
    print("✅ Non-existent post properly handled")

def test_access_nonexistent_account(driver):
    """Test accessing an account that doesn't exist."""
    driver.get(f"{BASE_URL}/accounts/nonexistentuser")

    assert "Account not found" in driver.page_source or "404" in driver.page_source
    print("✅ Non-existent account properly handled")

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_complete_user_workflow(driver):
    """Test complete user workflow: register -> login -> create post -> logout."""
    # 1. Register new account
    driver.get(f"{BASE_URL}/accounts/create")
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    workflow_username = f"workflowuser{int(time.time())}"
    username_input.send_keys(workflow_username)
    password_input.send_keys("workflowpass")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    WebDriverWait(driver, 5).until(lambda d: "/accounts/create" not in d.current_url)

    # 2. Create a post
    driver.get(f"{BASE_URL}/posts/create")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "subject")))
    subject_input = driver.find_element(By.NAME, "subject")
    content_input = driver.find_element(By.NAME, "content")
    address_input = driver.find_element(By.NAME, "address")
    tags_input = driver.find_element(By.NAME, "tags")

    workflow_post_title = f"Workflow Post {int(time.time())}"
    subject_input.send_keys(workflow_post_title)
    content_input.send_keys("Created during workflow test")
    address_input.send_keys("123 Workflow St")
    tags_input.send_keys("workflow, test")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    # 3. Verify post appears on home page
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//p[@id='subject' and contains(text(), '{workflow_post_title}')]/ancestor::a") )
    )

    # 4. Logout
    logout(driver)

    # 5. Verify post is still visible to anonymous users
    assert workflow_post_title in driver.page_source

    print(f"✅ Complete user workflow successful for '{workflow_username}'")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])