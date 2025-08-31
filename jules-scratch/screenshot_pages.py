import os
import time
from playwright.sync_api import sync_playwright, expect

def run_verification(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1280, "height": 800})

    # 取得 HTML 檔案的絕對路徑
    file_path = os.path.abspath('demo-page.html')
    page.goto(f'file://{file_path}')

    # --- 登入 ---
    page.locator("#login-form").get_by_label("帳號").fill("admin")
    page.locator("#login-form").get_by_label("密碼").fill("admin")
    page.get_by_role("button", name="登入").click()
    expect(page.locator("#app")).to_be_visible()
    print("登入成功。")

    # --- 截圖各個主要頁面 ---
    # 這個列表確保了遍歷的順序並包含所有頁面
    pages_to_visit = [
        "dashboard", "devices", "groups", "teams", "rules", "personnel",
        "channels", "maintenance", "automation", "capacity", "logs",
        "profile", "settings"
    ]

    for page_id in pages_to_visit:
        print(f"正在導航至頁面: {page_id}")
        # Use a more specific selector to ensure we are only looking inside the main nav
        link_locator = page.locator(f'nav .sidebar-link[data-page="{page_id}"]')

        # If the link is not visible, it might be inside a closed accordion
        if not link_locator.is_visible():
            # Find the accordion toggle button that controls the submenu containing our link
            # The selector finds the button that is a preceding sibling of the submenu div
            toggle_button = page.locator(f'button.submenu-toggle:has(+ .submenu:has(a[data-page="{page_id}"]))')

            if toggle_button.count() > 0:
                print(f"  - 連結不可見，正在嘗試展開父層選單...")
                toggle_button.click()
                page.wait_for_timeout(400) # Wait for accordion animation
            else:
                print(f"頁面連結 {page_id} 不可見且找不到對應的摺疊選單，已跳過。")
                continue

        # After attempting to open the accordion, try clicking the link again
        if link_locator.is_visible():
            link_locator.click(force=True) # Force click to avoid interception issues
            page.wait_for_timeout(500)
            page.screenshot(path=f"jules-scratch/{page_id}.png")
            print(f"  - 已儲存截圖: {page_id}.png")

            # Special handling for the 'automation' page tabs
            if page_id == 'automation':
                execution_logs_tab = page.locator("#execution-logs-tab")
                if execution_logs_tab.is_visible():
                    execution_logs_tab.click()
                    page.wait_for_timeout(500)
                    page.screenshot(path=f"jules-scratch/automation_execution_logs.png")
                    print(f"  - 已儲存截圖: automation_execution_logs.png")
        else:
            print(f"頁面連結 {page_id} 在展開選單後依然不可見，已跳過。")

    print("已完成所有主要頁面的截圖。")
    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)

print("頁面截圖腳本執行成功。")
