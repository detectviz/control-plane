import os
import time
from playwright.sync_api import sync_playwright, expect

def navigate_to_page(page, page_id, wait_for_selector):
    """Helper function to navigate to a page, opening accordion and waiting for a specific element."""
    print(f"正在導航至頁面: {page_id}")
    link_locator = page.locator(f'nav .sidebar-link[data-page="{page_id}"]')

    if not link_locator.is_visible():
        toggle_button = page.locator(f'button.submenu-toggle:has(+ .submenu:has(a[data-page="{page_id}"]))')
        if toggle_button.count() > 0:
            print(f"  - 連結不可見，正在嘗試展開父層選單...")
            is_open = "open" in (toggle_button.get_attribute("class") or "")
            if not is_open:
                toggle_button.click()
                page.wait_for_timeout(400) # Wait for animation

    link_locator.dispatch_event('click')
    # Wait for a specific element on the new page to ensure it has loaded
    expect(page.locator(wait_for_selector)).to_be_visible()
    print(f"  - 頁面 {page_id} 載入成功。")

def run_verification(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1440, "height": 900})

    # 取得 HTML 檔案的絕對路徑
    file_path = os.path.abspath('demo-page.html')
    page.goto(f'file://{file_path}')

    # --- 登入 ---
    page.locator("#login-form").get_by_label("帳號").fill("admin")
    page.locator("#login-form").get_by_label("密碼").fill("admin")
    page.get_by_role("button", name="登入").click()
    expect(page.locator("#app")).to_be_visible()
    print("登入成功。")
    page.wait_for_timeout(500) # 等待儀表板載入

    # --- 截圖各個彈出視窗 ---

    # 1. 通知中心下拉選單
    print("正在截取「通知中心」下拉選單...")
    page.locator("#notification-btn").click()
    expect(page.locator("#notification-dropdown")).to_be_visible()
    page.screenshot(path="jules-scratch/screenshot_modals/modal_notifications.png")
    page.locator("#notification-btn").click() # 關閉它
    print("  - 完成。")

    # 2. 新增設備彈窗
    print("正在截取「新增設備」彈窗...")
    navigate_to_page(page, "devices", "#devices-table-body")
    page.get_by_role("button", name="新增資源").click()
    expect(page.locator("#form-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/screenshot_modals/modal_add_device.png")
    page.locator("#form-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 3. 刪除確認彈窗
    print("正在截取「刪除確認」彈窗...")
    page.locator(".delete-device-btn").first.click()
    expect(page.locator("#confirm-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/screenshot_modals/modal_confirm_delete.png")
    page.locator("#cancel-action-btn").click()
    print("  - 完成。")

    # 4. 編輯團隊彈窗
    print("正在截取「編輯團隊」彈窗...")
    navigate_to_page(page, "teams", "#teams-table-body")
    page.locator(".edit-team-btn").first.click()
    expect(page.locator("#form-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/screenshot_modals/modal_edit_team.png")
    page.locator("#form-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 5. 編輯人員彈窗
    print("正在截取「編輯人員」彈窗...")
    navigate_to_page(page, "personnel", "#personnel-table-body")
    page.locator(".edit-user-btn").first.click()
    expect(page.locator("#form-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/screenshot_modals/modal_edit_personnel.png")
    page.locator("#form-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 6. 編輯通知管道彈窗
    print("正在截取「編輯通知管道」彈窗...")
    navigate_to_page(page, "channels", "#channels-table-body")
    page.locator(".edit-channel-btn").first.click()
    expect(page.locator("#form-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/screenshot_modals/modal_edit_channel.png")
    page.locator("#form-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 7. 新增告警規則彈窗
    print("正在截取「新增告警規則」彈窗...")
    navigate_to_page(page, "rules", "#rules-table-body")
    page.get_by_role("button", name="新增告警規則").click()
    expect(page.locator("#form-modal")).to_be_visible()
    page.wait_for_timeout(500) # Wait for modal animation
    page.screenshot(path="jules-scratch/screenshot_modals/modal_add_rule_collapsed.png")

    # Click to expand the second section
    page.locator(".accordion-header").nth(1).click()
    page.wait_for_timeout(500) # Wait for accordion animation
    page.screenshot(path="jules-scratch/screenshot_modals/modal_add_rule_expanded.png")

    page.locator("#form-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 8. 事件詳情彈窗
    print("正在截取「事件詳情」彈窗...")
    navigate_to_page(page, "logs", "#logs-table-body")
    page.locator("#logs-table-body tr.log-row").first.click()
    expect(page.locator("#incident-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/screenshot_modals/modal_incident_details.png")
    page.locator("#incident-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 9. Gemini AI 分析報告彈窗
    print("正在截取「Gemini AI 分析報告」彈窗...")
    page.locator("#select-all-logs").check()
    page.get_by_role("button", name="✨ 生成事件報告").click()
    expect(page.locator("#gemini-modal")).to_be_visible()
    expect(page.locator("#gemini-modal-content h3")).to_be_visible(timeout=5000)
    page.screenshot(path="jules-scratch/screenshot_modals/modal_gemini_report.png")
    page.locator("#close-gemini-modal").click()
    print("  - 完成。")

    # 10. 操作成功反饋提示
    print("正在截取「操作成功反饋」提示...")
    navigate_to_page(page, "profile", "#profile-name-input")
    page.locator("#profile-name-input").fill("Test Name")
    page.get_by_role("button", name="更新資訊").click()
    expect(page.locator("#feedback-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/screenshot_modals/modal_feedback.png")
    print("  - 完成。")

    print("已完成所有彈出視窗的截圖。")
    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)

print("彈出視窗截圖腳本執行成功。")
