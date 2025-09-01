import os
import shutil
from playwright.sync_api import sync_playwright, expect

def run_gif_creation(playwright):
    # --- Setup ---
    frames_dir = "jules-scratch/gif_frames"
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir)

    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1280, "height": 800})
    file_path = os.path.abspath('demo-page.html')
    page.goto(f'file://{file_path}')

    frame_count = 0
    def take_screenshot(name):
        nonlocal frame_count
        page.screenshot(path=os.path.join(frames_dir, f"frame_{frame_count:03d}_{name}.png"))
        frame_count += 1
        page.wait_for_timeout(500) # Add a small delay between actions

    # --- Start Capture ---
    print("Starting GIF frame capture...")

    # 1. Login Page
    take_screenshot("01_login_page")
    page.locator("#login-form").get_by_label("帳號").fill("admin")
    page.locator("#login-form").get_by_label("密碼").fill("admin")
    page.get_by_role("button", name="登入").click()
    expect(page.locator("#app")).to_be_visible()
    print("- Logged in")

    # 2. Dashboard
    page.wait_for_timeout(1000) # Wait for charts to potentially load
    take_screenshot("02_dashboard")
    print("- Captured Dashboard")

    # 3. Navigate to Personnel
    page.get_by_text("組織").first.click()
    page.wait_for_timeout(500) # wait for animation
    page.locator('a[data-page="personnel"]').click()
    expect(page.locator("#personnel-table-body")).to_be_visible()
    take_screenshot("03_personnel_page")
    print("- Captured Personnel Page")

    # 4. Open "Add Personnel" Modal
    page.get_by_role("button", name="新增人員").click()
    expect(page.locator("#form-modal")).to_be_visible()
    page.wait_for_timeout(500) # Wait for modal animation
    take_screenshot("04_add_personnel_modal")
    print("- Captured Add Personnel Modal")

    # 5. Close Modal
    page.locator("#form-modal .close-modal-btn").first.click()
    page.wait_for_timeout(500)
    take_screenshot("05_modal_closed")
    print("- Closed modal")

    # 6. Navigate to Logs page
    page.locator('a[data-page="logs"]').click()
    expect(page.locator("#logs-table-body")).to_be_visible()
    take_screenshot("06_logs_page")
    print("- Captured Logs Page")

    # 7. Logout
    page.locator("#logout-btn").click()
    expect(page.locator("#login-page")).to_be_visible()
    take_screenshot("07_logout")
    print("- Logged out")

    print(f"\nCaptured {frame_count} frames in '{frames_dir}'")
    browser.close()

with sync_playwright() as playwright:
    run_gif_creation(playwright)

print("GIF frame capture script finished successfully.")
