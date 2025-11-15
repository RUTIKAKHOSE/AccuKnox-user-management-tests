import pytest
from playwright.sync_api import sync_playwright
from QA.automation.pages.login_page import LoginPage
from QA.automation.pages.admin_page import AdminPage

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope="session")
def page(context):
    page = context.new_page()

    # Login once
    page.goto("https://opensource-demo.orangehrmlive.com/")
    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "admin123")
    page.click("button[type='submit']")
    page.wait_for_url("**/dashboard/index", timeout=30000)

    return page

@pytest.fixture(scope="session")
def admin_page(page) -> AdminPage:
    return AdminPage(page)
