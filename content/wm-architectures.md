# 世界模型路線與流派：四大類

<p class="lede">世界模型的路線差在「在哪個空間預測未來」：輸出影片、在潛空間推演、只預測表徵，或直接生成 3D 場景。本頁先一張圖看完四類，再逐類拆解，最後整理綜述用的其他切法。全站提到世界模型的 ①②③④ 都是這套編號。</p>

!!! key "一句話結論"
    世界模型分成「**像素空間影片生成**（給模擬、造資料用）」與「**潛空間動力學**（給 RL、規劃用）」兩大陣營，**JEPA** 與 **3D 空間模型**是兩條快速成長的支線。

## 四大類一張圖

<figure class="dg">
<svg viewBox="0 0 800 330" role="img" aria-label="世界模型四條路線的差別">
<rect class="n" x="10" y="130" width="130" height="70" rx="10"/>
<text x="75" y="160" text-anchor="middle" class="b">觀測＋動作</text>
<text x="75" y="182" text-anchor="middle" class="s">或文字、相機路徑</text>
<rect class="n wm" x="180" y="130" width="130" height="70" rx="10"/>
<text x="245" y="160" text-anchor="middle" class="b wm">預測下一步</text>
<text x="245" y="182" text-anchor="middle" class="s">動力學骨幹</text>
<path class="ar" d="M140,165 H178"/>
<path class="ar wm" d="M310,150 C350,150 350,45 388,45"/>
<path class="ar wm" d="M310,160 C360,160 360,125 388,125"/>
<path class="ar wm" d="M310,170 C360,170 360,205 388,205"/>
<path class="ar wm" d="M310,180 C350,180 350,285 388,285"/>
<rect class="n wm" x="390" y="15" width="400" height="60" rx="10"/>
<text x="405" y="40" class="b">① 影片生成：像素／影片潛空間</text>
<text x="405" y="62" class="s">Genie 3、Cosmos、GAIA-2 → 互動環境、合成資料、評估</text>
<rect class="n wm" x="390" y="95" width="400" height="60" rx="10"/>
<text x="405" y="120" class="b">② 潛在動力學：任務專用潛狀態＋獎勵</text>
<text x="405" y="142" class="s">DreamerV3／4、TD-MPC2 → RL 想像訓練、MPC 規劃</text>
<rect class="n wm" x="390" y="175" width="400" height="60" rx="10"/>
<text x="405" y="200" class="b">③ JEPA：自監督表徵，不重建像素</text>
<text x="405" y="222" class="s">V-JEPA 2、DINO-WM → 零樣本目標條件規劃</text>
<rect class="n wm" x="390" y="255" width="400" height="60" rx="10"/>
<text x="405" y="280" class="b">④ 3D 空間：顯式 3D 場景或佔據柵格</text>
<text x="405" y="302" class="s">Marble、OccWorld → 場景模擬、數位孿生、自駕</text>
<text x="20" y="300" class="s">要「做決策」選 ②③；</text>
<text x="20" y="318" class="s">要「造世界、造資料」選 ①④</text>
</svg>
<figcaption>差別在「把未來預測成什麼」。② 和 ③ 都在潛空間，差在要不要重建畫面；① 輸出人看得懂的影片；④ 輸出可走進去的 3D 場景。</figcaption>
</figure>

## ① 影片生成式世界模型

**核心想法：世界模型＝可以接受動作輸入的影片生成器。** 給過去幀與動作（鍵盤、方向盤、關節指令或文字），生成未來幀。這是目前規模最大、最受關注的路線，主要用於遊戲與互動環境、自駕與機器人的合成資料、策略評估。

**典型架構**：影片 tokenizer（連續 VAE 或離散 VQ）先把影片壓成時空潛在 → 主幹為 DiT（擴散）或自回歸 Transformer → 動作以 adaLN、cross-attention 或拼接 token 的方式條件化。要即時互動就必須逐幀自回歸，所以 [Diffusion Forcing](https://arxiv.org/abs/2407.01392) 與 [Self Forcing](https://arxiv.org/abs/2506.08009) 這類「每幀不同噪聲等級」的訓練技巧成為關鍵，用來抑制長序列誤差累積。

- **Genie 系列（Google DeepMind）**：[Genie 1](https://arxiv.org/abs/2402.15391)（2024）由影片 tokenizer、潛在動作模型、自回歸動力學模型三部分組成，從無標註的遊戲影片學出 8 種離散潛在動作；[Genie 2](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/)（2024）改用潛在擴散＋自回歸生成 3D 環境；[Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)（2025）以 720p、24 fps 即時生成，可維持數分鐘一致性，並支援文字「世界事件」。
- [NVIDIA Cosmos](https://arxiv.org/abs/2501.03575)（2025）：「物理 AI 的世界基礎模型平台」，提供擴散與自回歸兩種世界模型、開源 tokenizer，後續拆成 Predict、Transfer、Reason 三個系列，權重開放。
- [GAIA-2](https://arxiv.org/abs/2503.20523)（Wayve, 2025）：自駕專用、潛在擴散、多相機一致，可用自車動作、他車位置、天氣、地區等條件控制生成，用來合成罕見危險場景。
- [UniSim](https://arxiv.org/abs/2310.06114)（2023）與 [1X World Model](https://www.1x.tech/discover/1x-world-model)：用動作條件影片模型模擬機器人互動，用來評估策略或在模擬中訓練。
- [Sora](https://openai.com/index/video-generation-models-as-world-simulators/)（OpenAI, 2024）：時空 patch＋DiT 的代表，提出「影片生成模型即世界模擬器」，但本身不接受動作輸入，嚴格說不是可控世界模型。

**限制**：物理正確性不保證（物體穿透、憑空消失），長時間一致性與推論成本仍是主要瓶頸。

## ② 潛在動力學模型（給 RL 與規劃用）

**核心想法：把觀測壓成精簡的潛在狀態 z，學 p(z<sub>t+1</sub> | z<sub>t</sub>, a<sub>t</sub>) 與獎勵，然後在「想像」中訓練策略或做規劃。** 預測的是任務相關的抽象狀態，不是好看的畫面，所以便宜，可以一次展開上千條軌跡。

三個組件：**編碼器**（觀測 → z）、**動力學模型**（z, a → 下一個 z）、**預測頭**（獎勵、終止、價值）。差異在是否重建像素，以及用策略還是線上規劃決策。

- [DreamerV3](https://arxiv.org/abs/2301.04104)（2023，2025 年登上 Nature）：RSSM（確定性 GRU 狀態＋離散隨機潛在）加像素重建，在想像軌跡中訓練 actor-critic；一組超參數打通 150 多個任務，首次不靠人類資料在 Minecraft 挖到鑽石。
- [Dreamer 4](https://arxiv.org/abs/2509.24527)（2025）：改用可擴展的 Transformer 影片世界模型與 shortcut forcing 目標，可即時推論；只用離線資料在世界模型內訓練策略就能在 Minecraft 取得鑽石，是 ② 與 ① 的匯流。
- [TD-MPC2](https://arxiv.org/abs/2310.16828)（2023）：不重建像素的「隱式」世界模型，以潛在一致性＋獎勵＋價值損失訓練，用 MPPI 在潛空間做模型預測控制；單一 3.17 億參數模型涵蓋 80 個連續控制任務。
- 離散 token 變體：[IRIS](https://arxiv.org/abs/2209.00588)（VQ-VAE＋GPT）與 [DIAMOND](https://arxiv.org/abs/2405.12399)（擴散世界模型，證明視覺細節對 RL 很重要）。

**適合**：樣本效率導向的 RL、低維控制、線上規劃。**限制**：多半單一環境訓練，較少從網路規模資料取得常識。

## ③ JEPA 表徵預測

**核心想法：只在抽象表徵空間預測未來，不生成像素。** 這是 Yann LeCun 主張的路線：像素充滿不可預測的細節（樹葉、光影），生成它們浪費算力；在表徵空間預測可以自動丟掉雜訊。與 ② 的差別是：編碼器用自監督在大量影片上預訓練，而不是為單一任務訓練。

**訓練方式**：遮蔽影片的一部分時空區塊，讓預測器從可見部分的表徵去預測被遮部分的表徵；目標編碼器以 EMA 更新，防止表徵崩塌。

- [V-JEPA 2](https://arxiv.org/abs/2506.09985)（Meta, 2025）：兩階段。第一階段用超過 100 萬小時網路影片預訓練約 10 億參數的 ViT 編碼器；第二階段凍結編碼器，用不到 62 小時的 DROID 機器人資料訓練動作條件預測器（V-JEPA 2-AC）。部署時給一張目標影像，用 CEM 在表徵空間搜尋動作，實現零樣本抓放。
- [DINO-WM](https://arxiv.org/abs/2411.04983)（2024）：直接用凍結的 DINOv2 patch 特徵當狀態，在其上訓練 ViT 動力學預測器，不需獎勵即可在測試時做目標條件規劃。

**適合**：想便宜地做「想像式」規劃、不需要輸出畫面的機器人。**限制**：無法直接視覺化結果來除錯，長程規劃仍仰賴外部搜尋，統一的評測標準也還不成熟。

## ④ 3D／空間世界模型

**核心想法：輸出的不是一串 2D 影片幀，而是具有明確 3D 結構、可持久存在的場景。** 影片模型「轉個身回來場景就變了」的問題，在顯式 3D 表示（高斯潑濺、網格、點雲）中自然消失，生成的場景還能匯入物理引擎。

- [World Labs Marble](https://www.worldlabs.ai/blog/marble-world-model)（2025）：李飛飛團隊提出「空間智能」，從文字、圖片或影片生成可編輯、可匯出為高斯潑濺或網格的 3D 世界。
- 影片模型＋3D 記憶的混合：生成影片時維護一個 3D 場景快取或幾何條件，提升回訪一致性，是 2025 後互動世界模型常見的強化方式。
- 自駕領域的**佔據柵格（occupancy）世界模型**，如 [OccWorld](https://arxiv.org/abs/2311.16038)：在鳥瞰 3D 佔據空間預測未來，而非在相機影像空間。

**適合**：需要幾何一致的模擬、數位孿生、把生成場景送進 Isaac Sim 等物理模擬器訓練機器人。**限制**：多數仍是靜態場景，物體動態與互動仍要靠外部物理引擎。

## 四大類比較：用途與弱點

| 類別 | 在哪個空間預測 | 接受動作輸入 | 主要用途 | 代表 | 最大弱點 |
|---|---|---|---|---|---|
| ① 影片生成 | 像素／影片潛在 | 是（鍵盤、方向盤、文字、關節） | 互動環境、合成資料、策略評估 | Genie 3、Cosmos、GAIA-2 | 物理不可靠、算力昂貴 |
| ② 潛在動力學 | 任務專用潛在狀態 | 是（低維動作） | RL 想像訓練、MPC 規劃 | DreamerV3／4、TD-MPC2 | 難從網路資料取得常識 |
| ③ JEPA 表徵預測 | 自監督表徵空間 | 是（少量機器人資料後訓） | 零樣本目標條件規劃 | V-JEPA 2、DINO-WM | 無法視覺化、長程規劃昂貴 |
| ④ 3D 空間 | 顯式 3D 場景 | 部分（多為相機移動） | 模擬場景、數位孿生 | Marble、OccWorld | 動態與互動不足 |

## 四個流派：預測什麼、長處與代價

| 流派 | 預測什麼 | 代表作 | 長處／代價 |
|---|---|---|---|
| **① 影片／像素生成式** | 未來的影格。通常在影片 tokenizer 的 latent 裡生成，最後解碼成像素 | [Cosmos](https://arxiv.org/abs/2501.03575)、[Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)、[GAIA-2](https://arxiv.org/abs/2503.20523)、[UniSim](https://arxiv.org/abs/2310.06114) | 人看得懂、能當模擬器或造合成資料；但貴、慢，物理不一定對 |
| **② 潛空間動力學** | 低維潛狀態的下一步，通常仍保留重建像素的解碼器幫助學習 | [DreamerV3](https://arxiv.org/abs/2301.04104)、[Dreamer 4](https://arxiv.org/abs/2509.24527)、[TD-MPC2](https://arxiv.org/abs/2310.16828) | 快，適合在想像中做 RL 或規劃；但畫面細節少 |
| **③ JEPA 式表徵預測** | 在自監督表徵空間預測，**完全不生成、也不重建像素** | [V-JEPA 2／2-AC](https://arxiv.org/abs/2506.09985) | 不浪費算力在畫面細節，可零樣本規劃；但無法產出可看的影片，難直接檢查 |
| **④ 3D／4D 空間式** | 顯式 3D 場景（高斯潑濺、NeRF、佔據柵格、BEV） | [World Labs Marble](https://www.worldlabs.ai/blog/marble-world-model)、[OccWorld](https://arxiv.org/abs/2311.16038) | 幾何一致、可自由視角；但動態與拓撲變化難處理 |

!!! key "最常被混淆的一點"
    **② 和 ③ 都在潛空間，差別只在「要不要重建畫面」。** Dreamer 系列會訓練解碼器去重建畫面，JEPA 刻意不重建，這正是 LeCun「生成式 vs 非生成式」的核心。若只分兩派，常見說法是「生成式（①②④）vs 非生成式（③）」；若分三派，就是「影片、潛空間、JEPA」。

## 其他切法（綜述用的軸）

- **用途軸**：[A Comprehensive Survey on World Models for Embodied AI（arXiv:2510.16732）](https://arxiv.org/abs/2510.16732) 分成 **Decision-coupled**（為特定控制任務而學，如 Dreamer）與 **General-purpose**（通用模擬器，如 Cosmos、Genie）。
- **時間軸**：同一篇綜述再分成**逐步自回歸模擬**（適合閉環控制，但誤差會累積）與**一次平行預測整段未來**（延遲低，但互動性差）。
- **空間表徵軸**：同一篇綜述分成全域潛向量、token 特徵序列、空間潛柵格（BEV／voxel）、可渲染表徵（3DGS／NeRF），大致對應上表的 ②、①、④。
- **功能軸**：[Understanding World or Predicting Future?（arXiv:2411.14499）](https://arxiv.org/abs/2411.14499) 分成「理解世界」（建立內部表徵，如 LLM 內隱的世界知識）與「預測未來」（模擬未來以輔助決策）。

## 想動手實驗

- 研究世界模型規劃：[V-JEPA 2](https://github.com/facebookresearch/vjepa2) 或 [TD-MPC2](https://github.com/nicklashansen/tdmpc2)。
- 生成合成資料：[Cosmos](https://github.com/nvidia-cosmos)。
- 想看這四類各被哪些 VLA 與產品實際用到：〈[世界模型代表作的實際應用](wm-in-practice.html)〉。

## 來源

- 世界模型具身綜述：[arXiv:2510.16732](https://arxiv.org/abs/2510.16732)
- 世界模型理解 vs 預測綜述：[arXiv:2411.14499](https://arxiv.org/abs/2411.14499)
