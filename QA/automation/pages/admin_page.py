import time
import re
from playwright.sync_api import expect

class AdminPage:
    def __init__(self, page):
        self.page = page

    # ---------------------------
    # Get existing employee name
    # ---------------------------
    def get_existing_employee(self):
        self.page.click("a[href*='pim/viewPimModule']")
        expect(self.page.locator("h6:has-text('PIM')")).to_be_visible()
        self.page.wait_for_timeout(2000)

        rows = self.page.locator("div.oxd-table-card div.oxd-table-cell div")
        count = rows.count()

        for i in range(count):
            try:
                text = rows.nth(i).inner_text().strip()
            except:
                text = ""

            if text and re.search(r"[A-Za-z]", text) and len(text) > 3 and not text.isdigit():
                return text

        return "Admin A"   # fallback

    # ---------------------------
    # Navigate to Admin page
    # ---------------------------
    def navigate_to_admin(self):
        self.page.click("a[href*='admin/viewAdminModule']")
        expect(self.page.locator("h6:has-text('Admin')")).to_be_visible()
        self.page.wait_for_timeout(1500)

    # ---------------------------
    # Add User
    # ---------------------------
    def add_user(self):
        employee_name = self.get_existing_employee()

        self.navigate_to_admin()
        self.page.click("button:has-text('Add')")
        expect(self.page.locator("h6:has-text('Add User')")).to_be_visible()

        # Role
        self.page.locator("div.oxd-select-text-input").nth(0).click()
        self.page.locator("div[role='option']:has-text('ESS')").click()

        # Status
        self.page.locator("div.oxd-select-text-input").nth(1).click()
        self.page.locator("div[role='option']:has-text('Enabled')").click()

        # Employee auto-suggest
        emp_input = self.page.locator("input[placeholder='Type for hints...']")
        emp_input.fill(employee_name)
        self.page.wait_for_timeout(1500)

        options = self.page.locator("div[role='listbox'] div[role='option']")
        if options.count() > 0:
            options.first.click()

        # Username
        username = f"user_{int(time.time())}"
        self.page.locator("//label[text()='Username']/../following-sibling::div/input").fill(username)

        # Passwords
        pwd = "Admin@123"
        self.page.locator("//label[text()='Password']/../following-sibling::div/input").fill(pwd)
        self.page.locator("//label[text()='Confirm Password']/../following-sibling::div/input").fill(pwd)

        # Save
        self.page.click("button:has-text('Save')")
        expect(self.page.locator("div.oxd-toast")).to_be_visible(timeout=15000)

        return username

    # ---------------------------
    # Search User
    # ---------------------------
    def search_user(self, username):
        self.navigate_to_admin()
        field = self.page.locator("//label[text()='Username']/../following-sibling::div/input")
        field.fill(username)
        self.page.click("button:has-text('Search')")
        self.page.wait_for_timeout(2000)
        expect(self.page.locator(f"text={username}")).to_be_visible(timeout=15000)

    # ---------------------------
    # Edit User
    # ---------------------------
    def edit_user(self, username):
        # Search the existing user
        self.search_user(username)

        # Click the edit icon
        self.page.locator("i.oxd-icon.bi-pencil-fill").first.click()

        # Ensure Edit User page is loaded
        self.page.wait_for_selector("h6:has-text('Edit User')", timeout=10000)

        # Status dropdown wrapper based on the label "Status"
        status_wrapper = self.page.locator("//label[text()='Status']/../following-sibling::div")

        # Click on dropdown arrow
        status_wrapper.locator("div.oxd-select-text--after").click()

        # Wait for dropdown menu
        self.page.wait_for_selector("div[role='option']", timeout=5000)
        options = self.page.locator("div[role='option']")

        # Toggle status
        if options.filter(has_text="Enabled").count() > 0:
            options.filter(has_text="Enabled").first.click()
        else:
            options.filter(has_text="Disabled").first.click()

        # Save
        self.page.click("button:has-text('Save')")

        # Wait for success toast
        self.page.wait_for_selector("div.oxd-toast", timeout=15000)

        print(f"Status updated successfully for {username}")


    # ---------------------------
    # Delete User
    # ---------------------------
    def delete_user(self, username):
        self.search_user(username)

        rows = self.page.locator("div.oxd-table-body div.oxd-table-card")
        if rows.count() == 0:
            raise Exception(f"User '{username}' not found for deletion")

        self.page.locator("i.bi-trash").first.click()
        self.page.click("button:has-text('Yes, Delete')")

        expect(self.page.locator("div.oxd-toast")).to_be_visible()

