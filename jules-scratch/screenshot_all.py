import os
import shutil
import time
from playwright.sync_api import sync_playwright, expect

def run_all_screenshots(playwright):
    # --- Setup ---
    # Create directories for screenshots
    dirs = {
        "gif_frames": "jules-scratch/gif_frames",
        "pages": "jules-scratch/screenshot_pages",
        "modals": "jules-scratch/screenshot_modals",
        "roles": "jules-scratch/screenshot_by_role/verification"
    }
    for d in dirs.values():
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)

    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1440, "height": 900})
    file_path = f"file://{os.path.abspath('demo-page.html')}"

    frame_count = 0
    def take_gif_frame(name):
        nonlocal frame_count
        page.screenshot(path=os.path.join(dirs["gif_frames"], f"frame_{frame_count:03d}_{name}.png"))
        frame_count += 1
        page.wait_for_timeout(500)

    def login(user, password):
        page.goto(file_path)
        if page.locator("#login-page").is_visible():
            page.locator("#login-form").get_by_label("帳號").fill(user)
            page.locator("#login-form").get_by_label("密碼").fill(password)
            page.get_by_role("button", name="登入").click()
        expect(page.locator("#app")).to_be_visible()
        print(f"Logged in as {user}.")
        page.wait_for_timeout(500)

    def navigate_to_page(page_id, wait_for_selector):
        print(f"Navigating to page: {page_id}")
        link_locator = page.locator(f'nav .sidebar-link[data-page="{page_id}"]')
        if not link_locator.is_visible():
            toggle_button = page.locator(f'button.submenu-toggle:has(+ .submenu:has(a[data-page="{page_id}"]))')
            if toggle_button.count() > 0 and "open" not in (toggle_button.get_attribute("class") or ""):
                toggle_button.click()
                page.wait_for_timeout(400)
        link_locator.dispatch_event('click')
        expect(page.locator(wait_for_selector).first).to_be_visible()
        print(f"  - Page {page_id} loaded.")
        page.wait_for_timeout(200)

    # --- Start Admin User Flow for GIF and most screenshots ---
    login("admin", "admin")

    # --- GIF Frames ---
    print("\n--- Starting GIF Frame Capture ---")
    take_gif_frame("01_login_page_filled")
    take_gif_frame("02_dashboard")
    navigate_to_page("resources", "#resources-table-body tr")
    take_gif_frame("03_resources_page")
    page.locator('.resource-checkbox[data-resource-id="1"]').check()
    page.locator('.resource-checkbox[data-resource-id="2"]').check()
    page.locator('.resource-checkbox[data-resource-id="5"]').check()
    take_gif_frame("04_resources_batch_selection")
    # ... other gif frames ...
    print("Finished GIF frames.")

    # --- Page Screenshots ---
    print("\n--- Starting Page Screenshots ---")
    pages_to_visit = [
        "dashboard", "resources", "groups", "teams", "rules", "personnel",
        "channels", "maintenance", "automation", "capacity", "logs",
        "profile", "settings"
    ]
    for page_id in pages_to_visit:
        navigate_to_page(page_id, f"#page-{page_id}")
        page.screenshot(path=os.path.join(dirs["pages"], f"{page_id}.png"))
        print(f"  - Saved page screenshot: {page_id}.png")
    print("Finished page screenshots.")

    # --- Modal Screenshots ---
    print("\n--- Starting Modal Screenshots ---")
    navigate_to_page("resources", "#resources-table-body tr")
    page.evaluate("document.getElementById('add-resource-btn').click()")
    page.wait_for_selector("#form-modal", state="visible")
    page.screenshot(path=os.path.join(dirs["modals"], "modal_add_resource.png"))
    page.locator("#form-modal .close-modal-btn").first.click()
    # ... other modal screenshots ...
    print("Finished modal screenshots.")

    # --- Role-Based Screenshots ---
    print("\n--- Starting Role-Based Verification Screenshots ---")
    roles_config = {
        "admin": {"user": "admin", "pass": "admin", "pages": ["dashboard", "settings", "profile"]},
        "manager": {"user": "manager", "pass": "manager", "pages": ["dashboard", "profile"]},
        "member": {"user": "member", "pass": "member", "pages": ["dashboard", "profile"]}
    }
    for role, config in roles_config.items():
        login(config["user"], config["pass"])
        for page_id in config["pages"]:
            navigate_to_page(page_id, f"#page-{page_id}")
            page.screenshot(path=os.path.join(dirs["roles"], f"{page_id}-{role}.png"))
            print(f"  - Saved role-based screenshot: {page_id}-{role}.png")
    print("Finished role-based screenshots.")

    browser.close()

with sync_playwright() as playwright:
    run_all_screenshots(playwright)

print("\n\nAll screenshots captured successfully.")
