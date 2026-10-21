# VLA × 世界模型 調研

面向工程師的 VLA（Vision-Language-Action）與世界模型（World Model）科普網站，整理起源、架構、流派、訓練與評估、世界模型的角色、業界產品與案例分析。所有論文與來源都附上原文連結。

**線上閱讀**：https://weizhi727.github.io/VLA-World-Model-Research/

**離線版下載**：[VLA-World-Model-Research-offline.zip](https://github.com/Weizhi727/VLA-World-Model-Research/releases/download/offline-latest/VLA-World-Model-Research-offline.zip)（打不開 github.io 時使用：解壓縮後打開 `index.html`。每次網站更新會自動重新打包。）

## 章節

| # | 章節 | 檔案 |
|---|---|---|
| 01 | 起源與歷史 | `content/origins.md` |
| 02 | 主流模型架構 | `content/architectures.md` |
| 03 | 流派怎麼分 | `content/taxonomy.md` |
| 04 | 訓練、資料與評估 | `content/training.md` |
| 05 | 世界模型四類與五種角色 | `content/world-model-roles.md` |
| 06 | 訓練時 vs 推論時 | `content/train-vs-inference.md` |
| 07 | 具身基礎模型與合成資料 | `content/synthetic-data.md` |
| 08 | 業界產品盤點 | `content/industry.md` |
| 09 | 案例：智平方 | `content/ai2-robotics.md` |
| 10 | 經典世界模型論文精讀 | `content/classic-world-models.md` |
| 11 | 名詞速查 | `content/glossary.md` |
| 12 | 參考資料 | `content/references.md` |

## 怎麼修改與重建

純靜態網站，不需要任何前端框架。

```bash
pip install -r requirements.txt
python3 build.py          # 讀 content/*.md，套 template.html，輸出到 docs/
python3 -m http.server -d docs 8000   # 本地預覽 http://localhost:8000
```

- 內容寫在 `content/*.md`（Markdown，可內嵌 SVG 圖）。
- 重點框語法：`!!! key "標題"`、`!!! note`、`!!! warn`，內文縮排四格。
- 新增章節：在 `build.py` 的 `PAGES` 清單加一行。
- 樣式與互動：`docs/assets/style.css`、`docs/assets/site.js`（深色模式、手機選單、目錄高亮）。

## 站內問答

每一頁右下角有「問答」按鈕（`docs/assets/qa.js`）：

- **站內檢索（預設，免金鑰）**：`build.py` 會把每頁依 h2/h3 切段、名詞速查逐列切開，輸出 `docs/assets/search-index.js`；瀏覽器端用中文二字組 + 英文詞的 BM25 找出最相關段落，附連結與摘錄。
- **Claude 生成（選用）**：讀者在 ⚙ 填入自己的 Anthropic API 金鑰後，會把檢索到的段落交給 Claude 整理成有 [編號] 出處的回答。金鑰只存在該瀏覽器的 localStorage，直接送到 api.anthropic.com，網站本身不保存任何金鑰。

## 部署

GitHub Pages 從 `main` 分支的 `/docs` 資料夾發布。修改後執行 `python3 build.py` 再 commit，推上 `main` 即自動更新。

## 參數量資料

`data/params.json` 是所有模型參數量的唯一來源（只收官方明寫的數字）。`build.py` 會用它產生〈參數量總表〉，並在各章末尾自動附上「本頁提到的模型參數量」。新增模型時改這個檔案再重建即可；`update_notes.py` 可把同一份資料同步到專案的研究筆記。
