<div class="hero" markdown="1">
<p class="eyebrow">VLA and World Model Research · 2026.10</p>

# VLA 與世界模型：給工程師的完整調研整理

<p class="lede">這個網站把本專案從 2026-10-17 到 10-20 討論過的內容整理成一套可以從頭讀到尾的科普教材：起源、架構、流派、訓練與評估、世界模型怎麼被用、業界產品，以及智平方的案例。每個論文、產品都附上原始連結。</p>
</div>

## 一張圖看懂兩者的關係

<figure class="dg">
<svg viewBox="0 0 800 290" role="img" aria-label="VLA 與世界模型的關係圖">
<rect class="n" x="10" y="40" width="150" height="70" rx="10"/>
<text x="85" y="70" text-anchor="middle" class="b">相機影像</text>
<text x="85" y="92" text-anchor="middle" class="b">＋ 語言指令</text>
<rect class="n vla" x="210" y="30" width="170" height="90" rx="12"/>
<text x="295" y="68" text-anchor="middle" class="b vla">VLA（策略）</text>
<text x="295" y="92" text-anchor="middle" class="s">看懂、決定怎麼做</text>
<rect class="n" x="430" y="40" width="130" height="70" rx="10"/>
<text x="495" y="70" text-anchor="middle" class="b">動作序列</text>
<text x="495" y="92" text-anchor="middle" class="s">action chunk</text>
<rect class="n" x="610" y="40" width="180" height="70" rx="10"/>
<text x="700" y="70" text-anchor="middle" class="b">真實世界</text>
<text x="700" y="92" text-anchor="middle" class="s">機器人執行動作</text>
<path class="ar vla" d="M160,75 H208"/>
<path class="ar vla" d="M380,75 H428"/>
<path class="ar vla" d="M560,75 H608"/>
<path class="ar dash" d="M700,110 V140 H120 V112"/>
<text x="420" y="134" text-anchor="middle" class="s">拍到新的畫面（閉環）</text>
<rect class="n wm" x="300" y="190" width="240" height="80" rx="12"/>
<text x="420" y="224" text-anchor="middle" class="b wm">世界模型</text>
<text x="420" y="248" text-anchor="middle" class="s">給定現在＋動作，預測未來</text>
<rect class="n ghost" x="600" y="200" width="190" height="60" rx="10"/>
<text x="695" y="235" text-anchor="middle">想像的未來畫面／表徵</text>
<path class="ar wm dash" d="M495,112 V188"/>
<text x="505" y="170" class="s wm">動作</text>
<path class="ar wm dash" d="M50,112 V230 H298"/>
<text x="60" y="222" class="s wm">現在的觀測</text>
<path class="ar wm" d="M540,230 H598"/>
<path class="ar wm" d="M330,188 V122"/>
<text x="210" y="172" class="s wm">造資料、陪練、當考官</text>
</svg>
<figcaption>VLA 學的是「看到這個、聽到這句話，<b>該做什麼動作</b>」，也就是策略 π(a | o, l)。世界模型學的是「現在這樣、做了這個動作，<b>世界會變成怎樣</b>」，也就是動態 p(o′ | o, a)。目前業界多半把世界模型放在雲端，替 VLA 造資料、當練習場和考官。</figcaption>
</figure>

## 先記住這七件事

!!! key "重點"
    1. **VLA 為了解決「機器人學不會泛化」而生**：2023 年 [RT-2](https://arxiv.org/abs/2307.15818) 把動作當成語言 token，借用網路規模的視覺語言知識，VLA 一詞由此而來。詳見 [起源與歷史](origins.html)。
    2. **世界模型為了解決「在真實世界試錯太貴、不會規劃」而生**：從 1943 年 Craik 的心智模型、1991 年 Dyna，到 2018 年 [World Models](https://arxiv.org/abs/1803.10122)，2024 年 Sora、Genie 把「影片生成＝世界模擬器」推向業界。
    3. **2026 年 VLA 的主流設計**是「預訓練 VLM 骨幹＋flow matching／擴散動作頭＋動作分塊」，人形機器人則普遍再加一層「慢腦＋快腦」雙系統。詳見 [VLA 主流架構](vla-architectures.html)。
    4. **「流派」其實是好幾條軸的組合**：VLA 至少有「系統架構」「動作怎麼解碼」「中間表徵是什麼」三條軸；世界模型最常見的切法是「在哪個空間預測未來」：影片、潛空間、JEPA、3D。詳見 [VLA 流派怎麼分](vla-taxonomy.html) 與 [世界模型路線與流派](wm-architectures.html)。
    5. **世界模型對 VLA 有五種角色**：資料引擎、輔助預測、想像中 RL、先想再做、評測模擬器。詳見 [世界模型四類與五種角色](world-model-roles.html)。
    6. **訓練時用世界模型已是主流，推論時用仍是少數**：量產機器人上幾乎只跑 VLA；推論時用到世界模型的，多是只跑一步取特徵，或在 VLA 沒把握時才拿來預演。詳見 [訓練時 vs 推論時](train-vs-inference.html)。
    7. **生成影片「看起來真」不等於「物理對」**：業界的做法是多層把關，最後以真機成功率驗收。詳見 [具身基礎模型與合成資料](synthetic-data.html)。

## 網站怎麼分

全站分成五區，側欄也照這個順序排：

| 分區 | 讀什麼 |
|---|---|
| **入門總覽** | 兩者為什麼出現、怎麼訓練與評估。VLA 與世界模型並排對照，適合先讀 |
| **VLA** | VLA 本身的架構路線與分類方法 |
| **世界模型** | 世界模型的四大類，以及 8 篇經典論文精讀 |
| **綜合應用：VLA × 世界模型** | 世界模型怎麼幫 VLA、在訓練還是推論時用、合成資料、業界產品與智平方案例 |
| **查詢工具** | 參數量總表、名詞速查、參考資料 |

## 建議閱讀順序

| 你想知道的 | 從這裡讀 |
|---|---|
| 完全沒概念，想先知道為什麼有這兩個東西 | [01 起源與歷史](origins.html) → [14 名詞速查](glossary.html) |
| 想懂 VLA 長什麼樣、怎麼選型 | [03 VLA 主流架構](vla-architectures.html) → [04 VLA 流派怎麼分](vla-taxonomy.html) |
| 想懂世界模型有哪幾類 | [05 世界模型路線與流派](wm-architectures.html) → [06 經典世界模型論文精讀](classic-world-models.html) |
| 要自己動手訓練或評估 | [02 訓練、資料與評估](training.html) |
| 想知道世界模型到底怎麼幫 VLA | [07 四類與五種角色](world-model-roles.html) → [08 訓練時 vs 推論時](train-vs-inference.html) → [09 合成資料](synthetic-data.html) |
| 想知道某個世界模型到底被誰用過 | [10 世界模型代表作的實際應用](wm-in-practice.html) |
| 想知道業界誰在做什麼 | [11 業界產品盤點](industry.html) → [12 案例：智平方](ai2-robotics.html) |
| 想查某個模型有多大 | [13 參數量總表](params.html) |

## 全部章節

{{CHAPTER_CARDS}}
## 關於資料來源

- **離線版**：公司網路打不開這個網站時，可以下載 [離線壓縮包](https://github.com/Weizhi727/VLA-World-Model-Research/releases/download/offline-latest/VLA-World-Model-Research-offline.zip)，解壓縮後打開 `index.html` 即可閱讀。

- 內容來自本專案的調研筆記與討論串，整理日期 2026-10-20。
- 論文一律連到 arXiv 摘要頁或官方頁；只有部落格、發表會或新聞來源的，會在文中註明。
- 參數量、資料量等數字以論文或官方頁為準；**查不到的標「未公開」，不猜**。少數早期整理中未逐篇核對的數字，會在該處標示「約」或另加說明。
