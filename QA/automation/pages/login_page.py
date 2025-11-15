from playwright.sync_api import expect

class LoginPage:
    def __init__(self, page):
        self.page = page

    def login(self, username, password):
        self.page.goto("https://opensource-demo.orangehrmlive.com/")
        self.page.fill("input[name='username']", username)
        self.page.fill("input[name='password']", password)
        self.page.click("button[type='submit']")
        expect(self.page.locator("h6:has-text('Dashboard')")).to_be_visible()

