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
    page.get_by_label("帳號").fill("admin")
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
    page.screenshot(path="jules-scratch/modal_notifications.png")
    page.locator("#notification-btn").click() # 關閉它
    print("  - 完成。")

    # 2. 新增設備彈窗
    print("正在截取「新增設備」彈窗...")
    page.get_by_role("link", name="設備管理").click()
    page.get_by_role("button", name="新增設備").click()
    expect(page.locator("#form-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/modal_add_device.png")
    page.locator("#form-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 3. 刪除確認彈窗
    print("正在截取「刪除確認」彈窗...")
    # 這會點擊設備列表中的第一個刪除按鈕
    page.locator(".delete-device-btn").first.click()
    expect(page.locator("#confirm-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/modal_confirm_delete.png")
    page.locator("#cancel-action-btn").click()
    print("  - 完成。")

    # 4. 編輯團隊彈窗
    print("正在截取「編輯團隊」彈窗...")
    page.get_by_role("link", name="團隊管理").click()
    page.locator(".edit-team-btn").first.click()
    expect(page.locator("#form-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/modal_edit_team.png")
    page.locator("#form-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 5. 編輯人員彈窗
    print("正在截取「編輯人員」彈窗...")
    page.get_by_role("link", name="人員管理").click()
    page.locator(".edit-user-btn").first.click()
    expect(page.locator("#form-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/modal_edit_personnel.png")
    page.locator("#form-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 6. 編輯通知管道彈窗
    print("正在截取「編輯通知管道」彈窗...")
    page.get_by_role("link", name="通知管道").click()
    page.locator(".edit-channel-btn").first.click()
    expect(page.locator("#form-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/modal_edit_channel.png")
    page.locator("#form-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 7. 事件詳情彈窗
    print("正在截取「事件詳情」彈窗...")
    page.get_by_role("link", name="告警紀錄").click()
    # 點擊告警紀錄列表中的第一個項目
    page.locator("#logs-table-body tr.log-row").first.click()
    expect(page.locator("#incident-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/modal_incident_details.png")
    page.locator("#incident-modal .close-modal-btn").first.click()
    print("  - 完成。")

    # 8. Gemini AI 分析報告彈窗
    print("正在截取「Gemini AI 分析報告」彈窗...")
    page.locator("#select-all-logs").check()
    page.get_by_role("button", name="✨ 生成事件報告").click()
    expect(page.locator("#gemini-modal")).to_be_visible()
    # 等待載入動畫結束且內容出現
    expect(page.locator("#gemini-modal-content h3")).to_be_visible(timeout=5000)
    page.screenshot(path="jules-scratch/modal_gemini_report.png")
    page.locator("#close-gemini-modal").click()
    print("  - 完成。")

    # 9. 操作成功反饋提示
    print("正在截取「操作成功反饋」提示...")
    page.get_by_role("link", name="個人資料").click()
    page.locator("#profile-name-input").fill("Test Name")
    page.get_by_role("button", name="更新資訊").click()
    expect(page.locator("#feedback-modal")).to_be_visible()
    page.screenshot(path="jules-scratch/modal_feedback.png")
    print("  - 完成。")

    print("已完成所有彈出視窗的截圖。")
    browser.close()

with sync_playwright() as playwright:
    run_verification(playwright)

print("彈出視窗截圖腳本執行成功。")
