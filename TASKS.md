# TASKS

## 檔案為 [demo-page.html](demo-page.html)，以下任務需要執行，請先閱讀 [AGENTS.md](AGENTS.md) 再開始。

- [ ] 整合 Tom Select 套件，修復這些關鍵元素： 有一些 select 元素使用舊的樣式格式。
	附圖：[1.png](1.png) [2.png](2.png) [3.png](3.png) [4.png](4.png) [5.png](5.png) 

- [ ] 檢查是否還有其他使用不標準樣式的 select 元素需要修復，demo-page.html 的徹底技術債務清理

## 根本問題發現

問題根源：這些select元素使用了與標準化樣式不同的CSS類別：

/* 問題樣式 */
class="px-3 py-1.5 border border-slate-300 rounded-lg
focus:ring-blue-500 focus:border-blue-500 text-sm bg-white
	text-slate-800"

/* 標準樣式 */
class="mt-1 block w-full rounded-lg border
border-slate-300 bg-white px-3 py-1.5 text-sm
text-slate-800 focus:border-blue-500 focus:ring-blue-500"

✅ 徹底修復措施

1. 統一所有select元素樣式
2. 強化Tom Select CSS修復

- ✅ 統一樣式 - 使用相同的 Tailwind CSS 類別集合
- ✅ 單一邊框 - 消除 Tom Select 雙框線問題
- ✅ 正確初始化 - 移除skip邏輯，所有元素都能使用Tom Select
- ✅ 唯一ID - 沒有重複ID衝突
- ✅ 無視覺故障 - 被接管的原生select完全隱藏
