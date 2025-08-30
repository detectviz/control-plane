import os
from playwright.sync_api import sync_playwright, Page, expect

# Define the absolute path to the HTML file
file_path = f"file://{os.path.abspath('demo-page.html')}"
output_dir = "jules-scratch"

def update_screenshots():
    """
    Logs in as admin and overwrites the main dashboard and profile screenshots.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("--- Updating main screenshots as admin ---")

        # 1. Login
        print("Navigating to login page...")
        page.goto(file_path)

        print("Entering credentials...")
        login_form = page.locator("#login-form")
        login_form.get_by_label("帳號").fill("admin")
        login_form.get_by_label("密碼").fill("admin")
        login_form.get_by_role("button", name="登入").click()

        expect(page.locator("#breadcrumb")).to_have_text("總覽儀表板", timeout=10000)
        print("Login successful.")

        # 2. Screenshot Dashboard
        dashboard_screenshot_path = os.path.join(output_dir, "dashboard.png")
        print(f"Updating screenshot: {dashboard_screenshot_path}")
        page.screenshot(path=dashboard_screenshot_path)

        # 3. Navigate to Profile and Screenshot
        print("Navigating to profile page...")
        profile_link = page.get_by_role("link", name="個人資料")
        profile_link.click()

        expect(page.get_by_role("heading", name="個人資訊")).to_be_visible(timeout=10000)

        profile_screenshot_path = os.path.join(output_dir, "profile.png")
        print(f"Updating screenshot: {profile_screenshot_path}")
        page.screenshot(path=profile_screenshot_path)

        browser.close()
        print("\nFinished updating screenshots.")

if __name__ == "__main__":
    update_screenshots()
