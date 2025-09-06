# AGENTS.md - 給 AI Agent 的專案說明

這份文件旨在提供 AI Agent 在本專案中執行任務時所需的核心背景資訊與必須遵守的規則。

## 核心規則

### 1. 架構與實作同步

**檔案關聯:**
- `ARCHITECTURE.md` (架構設計文件)
- `demo-page.html` (前端實作原型)

**規則描述:**
`demo-page.html` 是 `ARCHITECTURE.md` 文件中定義之架構的視覺化原型。任何對其中一個檔案的修改，都必須確保另一個檔案的內容與之一致。

- **若修改 `ARCHITECTURE.md`**：必須檢查 `demo-page.html` 是否需要對應更新，以符合新的架構設計。
- **若修改 `demo-page.html`**：必須檢查 `ARCHITECTURE.md`、 `USER_GUIDE.md` 的規格是否需要更新，以反映實作上的變更。

### 2. 前端變更後的截圖更新

**檔案關聯:**
- `demo-page.html`
- `jules-scratch/` 目錄下的截圖腳本

**規則描述:**
在對 `demo-page.html` 進行任何可能影響 UI 畫面的修改後，**必須** 重新產生所有相關的頁面截圖，以確保圖片檔案與最新畫面同步。

**執行步驟:**
請參考 `jules-scratch/README.md` 的說明來執行截圖腳本。主要步驟如下：

1.  確保已安裝 `playwright`。
2.  從專案根目錄執行以下三個腳本：

```bash
python jules-scratch/screenshot_pages.py    ＃ 產生頁面截圖
python jules-scratch/screenshot_modals.py   ＃ 產生彈窗截圖
python jules-scratch/screenshot_by_role.py  ＃ 產生角色不同狀態的截圖
python jules-scratch/create_gif.py          ＃ 產生 GIF 動畫
```

## 程式碼風格
- 執行計劃、Commit Message 使用「繁體中文」。
- 盡可能遵循現有檔案的程式碼風格。
- 若無特定風格，請採用簡潔、易讀的寫法。
