# 自動化截圖腳本說明

這個目錄包含了兩個 Python 腳本，用於自動化截取 `demo-page.html` 的各個頁面和彈出視窗。

## 環境設定

在執行腳本之前，請確保您已經安裝了 Playwright。

```bash
pip install playwright
playwright install
```

## 腳本說明

### 1. `screenshot_pages.py`

這個腳本會登入應用程式，並逐一訪問側邊欄中的每一個主要頁面，然後進行截圖。所有截圖都會儲存在目前的目錄 (`final_run`) 中。

**如何執行：**
```bash
python screenshot_pages.py
```

### 2. `screenshot_modals.py`

這個腳本會登入應用程式，並透過特定的操作來觸發各種彈出視窗（例如：新增、刪除、查看詳情等），然後對這些彈窗進行截圖。所有截圖同樣會儲存在目前的目錄中。

**如何執行：**
```bash
python screenshot_modals.py
```

## 注意事項

- 腳本預設會以 `headless` (無頭) 模式執行瀏覽器。
- 兩個腳本都依賴於 `demo-page.html` 檔案必須存在於它們執行的上一層目錄中。
