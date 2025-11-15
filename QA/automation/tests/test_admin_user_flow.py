import time
import pytest
from playwright.sync_api import Page, expect
from QA.automation.pages.admin_page import AdminPage
from QA.automation.pages.login_page import LoginPage


# FIXTURE: Login + AdminPage

@pytest.fixture(scope="session")
def admin_page(browser) -> AdminPage:
    context = browser.new_context()
    page: Page = context.new_page()

    # Login
    page.goto("https://opensource-demo.orangehrmlive.com/")
    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("**/dashboard/index", timeout=30000)

    print(" Logged in successfully")

    yield AdminPage(page)

    context.close()
    print("ℹ Browser context closed")



# Test 1: Add User

@pytest.mark.dependency()
def test_add_user(admin_page):
    username = admin_page.add_user()
    assert username is not None

    pytest.shared_username = username
    print(f" User created: {username}")



# Test 2: Search User

@pytest.mark.dependency(depends=["test_add_user"])
def test_search_user(admin_page):
    username = getattr(pytest, "shared_username", None)
    assert username, "Add user must run first"

    admin_page.search_user(username)
    print(f" User search verified: {username}")



# Test 3: Edit User

@pytest.mark.dependency(depends=["test_search_user"])
def test_edit_user(admin_page):
    username = getattr(pytest, "shared_username", None)
    assert username, "Add user must run first"

    admin_page.edit_user(username)   # just edit status
    print(f" User edited successfully: {username}")



# Test 4: Delete User + Verify

@pytest.mark.dependency(depends=["test_edit_user"])
def test_delete_user(admin_page):
    username = getattr(pytest, "shared_username", None)
    assert username, "Edit user must run first"

    admin_page.delete_user(username)
    print(f" User deleted: {username}")

    # Verify deletion
    admin_page.navigate_to_admin()
    field = admin_page.page.locator("//label[text()='Username']/../following-sibling::div/input")
    field.fill(username)

    admin_page.page.click("button:has-text('Search')")
    admin_page.page.wait_for_timeout(2000)

    no_record = admin_page.page.locator("span:has-text('No Records Found')")
    assert no_record.is_visible(), " Deleted user still appears!"

    print(" User deletion confirmed")



