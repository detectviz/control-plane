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
        link_locator = page.locator(f'nav > a.sidebar-link[data-page="{page_id}"]')

        if link_locator.is_visible():
            link_locator.click()
            # 等待一小段時間確保頁面內容載入
            page.wait_for_timeout(500)
            page.screenshot(path=f"jules-scratch/{page_id}.png")
            print(f"  - 已儲存截圖: {page_id}.png")

            # 特別處理「自動化」頁面的頁籤
            if page_id == 'automation':
                execution_logs_tab = page.locator("#execution-logs-tab")
                execution_logs_tab.click()
                page.wait_for_timeout(500)
                page.screenshot(path=f"jules-scratch/automation_execution_logs.png")
                print(f"  - 已儲存截圖: automation_execution_logs.png")
        else:
            print(f"頁面連結 {page_id} 不可見，已跳過。")

    print("已完成所有主要頁面的截圖。")
    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)

print("頁面截圖腳本執行成功。")
