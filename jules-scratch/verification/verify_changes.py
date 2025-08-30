import os
from playwright.sync_api import sync_playwright, Page, expect

# Define user roles and credentials
USERS = {
    "admin": {"username": "admin", "password": "admin"},
    "manager": {"username": "manager", "password": "manager"},
    "member": {"username": "member", "password": "member"},
}

# Define the absolute path to the HTML file
# Using os.path.abspath is more robust
file_path = f"file://{os.path.abspath('demo-page.html')}"
output_dir = "jules-scratch/verification"

def run_verification():
    """
    Launches Playwright, logs in as each user, and takes screenshots
    of the dashboard and profile pages.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for role, credentials in USERS.items():
            print(f"--- Verifying as role: {role} ---")

            # 1. Login
            print("Navigating to login page...")
            page.goto(file_path)

            print("Entering credentials...")
            # Scope the locators to the login form to avoid ambiguity
            login_form = page.locator("#login-form")
            login_form.get_by_label("帳號").fill(credentials["username"])
            login_form.get_by_label("密碼").fill(credentials["password"])
            login_form.get_by_role("button", name="登入").click()

            # Wait for the main application to load by checking for the breadcrumb
            expect(page.locator("#breadcrumb")).to_have_text("總覽儀表板", timeout=10000)
            print("Login successful.")

            # 2. Screenshot Dashboard
            dashboard_screenshot_path = os.path.join(output_dir, f"dashboard-{role}.png")
            print(f"Taking screenshot of dashboard: {dashboard_screenshot_path}")
            page.screenshot(path=dashboard_screenshot_path)

            # 3. Navigate to Profile and Screenshot
            print("Navigating to profile page...")
            # Use the sidebar link to navigate
            profile_link = page.get_by_role("link", name="個人資料")
            profile_link.click()

            # Wait for the profile page to load
            expect(page.get_by_role("heading", name="個人資訊")).to_be_visible(timeout=10000)

            profile_screenshot_path = os.path.join(output_dir, f"profile-{role}.png")
            print(f"Taking screenshot of profile page: {profile_screenshot_path}")
            page.screenshot(path=profile_screenshot_path)

            # 4. Logout
            print("Logging out...")
            logout_button = page.get_by_title("登出")
            logout_button.click()

            # Wait for the login form to be visible again
            expect(page.get_by_role("heading", name="網管監控平台")).to_be_visible(timeout=10000)
            print(f"Logout successful for {role}.")

        browser.close()
        print("\nVerification complete for all roles.")

if __name__ == "__main__":
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    run_verification()
