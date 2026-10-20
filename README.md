# VLA × 世界模型 調研

面向工程師的 VLA（Vision-Language-Action）與世界模型（World Model）科普網站，整理起源、架構、流派、訓練與評估、世界模型的角色、業界產品與案例分析。所有論文與來源都附上原文連結。

**線上閱讀**：https://weizhi727.github.io/VLA-World-Model-Research/

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
| 10 | 名詞速查 | `content/glossary.md` |
| 11 | 參考資料 | `content/references.md` |

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

## 部署

GitHub Pages 從 `main` 分支的 `/docs` 資料夾發布。修改後執行 `python3 build.py` 再 commit，推上 `main` 即自動更新。
