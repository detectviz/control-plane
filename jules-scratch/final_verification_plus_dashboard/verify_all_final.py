import os
import time
from playwright.sync_api import sync_playwright, expect

def run_verification(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1280, "height": 900})

    file_path = os.path.abspath('demo-page.html')
    page.goto(f'file://{file_path}')

    # --- Login ---
    page.get_by_label("帳號").fill("admin")
    page.locator("#login-form").get_by_label("密碼").fill("admin")
    page.get_by_role("button", name="登入").click()
    expect(page.locator("#app")).to_be_visible()
    print("Login successful.")
    page.wait_for_timeout(500)

    # 1. Verify new Dashboard layout is populated
    print("Verifying new dashboard layout...")
    expect(page.locator("#page-dashboard")).to_be_visible()
    group_container = page.locator("#group-status-container")
    expect(group_container).to_be_visible()
    # Verify that the container is NOT empty by checking for the first group's card
    expect(group_container.get_by_text("核心交換器")).to_be_visible()
    expect(group_container.get_by_text("總公司防火牆")).to_be_visible()
    page.screenshot(path="jules-scratch/final_verification_plus_dashboard/1_dashboard_final.png")
    print("  - Screenshot of final dashboard saved.")

    # 2. Verify Logs page dropdowns
    print("Verifying Logs page dropdowns...")
    page.get_by_role("link", name="告警紀錄").click()
    expect(page.locator("#page-logs")).to_be_visible()
    page.screenshot(path="jules-scratch/final_verification_plus_dashboard/2_logs_page_final.png")
    print("  - Screenshot of Logs page saved.")

    # 3. Verify Profile page editability
    print("Verifying Profile page editability...")
    # Log out as admin first
    page.locator("#logout-btn").click()
    expect(page.locator("#login-page")).to_be_visible()

    # Log in as a different user to verify the logic works for others
    page.get_by_label("帳號").fill("member")
    page.locator("#login-form").get_by_label("密碼").fill("member")
    page.get_by_role("button", name="登入").click()
    expect(page.locator("#app")).to_be_visible()

    page.get_by_role("link", name="個人資料").click()
    expect(page.locator("#page-profile")).to_be_visible()

    # Check initial state
    expect(page.locator("#profile-name-input")).to_have_value("王工程師")

    # Change name and team
    page.locator("#profile-name-input").fill("王大明")
    team_select = page.locator("#profile-teams-select")
    team_select.select_option(label="伺服器團隊")

    page.get_by_role("button", name="更新資訊").click()
    expect(page.locator("#feedback-modal")).to_be_visible()

    # Check sidebar for updated name
    expect(page.locator("#user-name")).to_have_text("王大明")

    page.screenshot(path="jules-scratch/final_verification_plus_dashboard/3_profile_page_final.png")
    print("  - Screenshot of updated Profile page saved.")

    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)

print("Final verification script executed.")
