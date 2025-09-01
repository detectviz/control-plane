# 自動化截圖腳本說明

這個目錄包含了三個 Python 腳本，用於自動化截取 `demo-page.html` 的各個頁面和彈出視窗。

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

---

## 3. `create_gif.py` (產生 demo.gif)

這個腳本用於完整地產生 `demo.gif` 動畫，它會自動執行以下操作：
1.  模擬使用者登入、操作平台各項核心功能。
2.  在 `jules-scratch/gif_frames/` 目錄下產生一系列操作畫面的 `.png` 格式截圖。

### 如何更新 `demo.gif`

更新 `demo.gif` 包含兩個步驟：

#### 步驟一：產生畫面幀

首先，執行 `create_gif.py` 腳本來產生所有動畫需要的畫面。

```bash
python3 jules-scratch/create_gif.py
```

#### 步驟二：合成 GIF 動畫

產生完畫面後，需要使用 `ImageMagick` 工具來將所有 `.png` 圖片合成為一個 GIF 檔案。

**依賴工具**：請先確保您已安裝 ImageMagick。
- **macOS (Homebrew)**: `brew install imagemagick`
- **Debian/Ubuntu**: `sudo apt-get install imagemagick`

執行以下指令來合成 `demo.gif`，這個指令會將 `gif_frames` 目錄中的所有圖片打包成 `demo.gif` 並存放在專案根目錄。

```bash
convert -delay 80 -loop 0 jules-scratch/gif_frames/frame_*.png -resize 1440x900 demo.gif
```
