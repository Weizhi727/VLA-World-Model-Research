# 經典世界模型論文精讀

<p class="lede">挑出 8 篇定義了世界模型這個領域的論文，每篇用同一個框架拆解：背景、要解決的問題、核心解法、模型結構、資料怎麼建、怎麼評估、作者自己承認的局限，最後說明它對 VLA 的意義。數字都取自論文原文，連結附在每篇開頭。</p>

!!! key "8 篇論文的一條主線"
    **世界模型一直在回答同一個問題：「要預測未來的什麼？」**
    World Models 和 DreamerV3 預測壓縮後的**潛狀態**；MuZero 更極端，只預測**規劃需要的價值與獎勵**；GAIA-1、UniSim、Genie、Cosmos 直接預測**畫面**，換來可以當模擬器用；V-JEPA 2 回到**表徵空間**，主張不必畫出每個像素也能規劃。這條取捨（預測得越具體越像模擬器，但越貴、越容易錯在不重要的細節上）貫穿整個領域。

## 一張表看完 8 篇

| 論文 | 年份 | 預測什麼 | 動作從哪來 | 訓練資料 | 規模 | 主要用途 |
|---|---|---|---|---|---|---|
| [World Models](#world-models) | 2018 | 潛向量 z（VAE 壓縮） | 遊戲按鍵 | 1 萬條隨機策略軌跡 | 約 500 萬參數 | 在「夢境」中訓練控制器 |
| [MuZero](#muzero) | 2019 | 獎勵、價值、策略（不預測畫面） | 遊戲動作 | 自我對弈 | 16 個殘差塊 | MCTS 規劃 |
| [DreamerV3](#dreamerv3) | 2023 | 離散潛狀態 + 獎勵 + 是否結束 | 環境動作 | 線上互動 | 12M–400M | 想像中強化學習 |
| [GAIA-1](#gaia-1) | 2023 | 下一幀的影像 token | 車速、曲率 | 4,700 小時倫敦行車 | 約 9.4B | 自駕情境生成 |
| [UniSim](#unisim) | 2023 | 下一段影片 | 文字、馬達指令、相機 | 14 個資料集混合 | 5.6B | 訓練 VLM 與 RL 策略 |
| [Genie](#genie) | 2024 | 下一幀的影像 token | **從影片自學的 8 個潛動作** | 3 萬小時平台遊戲影片 | 10.7B | 可互動的生成世界 |
| [Cosmos](#cosmos) | 2025 | 未來影片（擴散或自迴歸） | 文字、影片，後訓練加動作 | 2,000 萬小時 → 1 億段 | 4B–14B | 物理 AI 的基礎模型 |
| [V-JEPA 2](#v-jepa-2) | 2025 | 未來的**表徵** | 機械手臂末端位移 | 100 萬小時影片 + 62 小時 DROID | 1B + 300M | 零樣本機器人規劃 |

<figure class="dg">
<svg viewBox="0 0 800 300" role="img" aria-label="8 篇經典世界模型論文的時間線與三條路線">
<line x1="40" y1="150" x2="770" y2="150" class="ar"/>
<text x="60" y="176" class="s">2018</text><text x="200" y="176" class="s">2019</text><text x="400" y="176" class="s">2023</text><text x="560" y="176" class="s">2024</text><text x="700" y="176" class="s">2025</text>
<rect class="n wm" x="20" y="40" width="130" height="56" rx="10"/>
<text x="85" y="64" text-anchor="middle" class="b wm">World Models</text>
<text x="85" y="84" text-anchor="middle" class="s">潛空間夢境</text>
<rect class="n wm" x="165" y="40" width="110" height="56" rx="10"/>
<text x="220" y="64" text-anchor="middle" class="b wm">MuZero</text>
<text x="220" y="84" text-anchor="middle" class="s">只預測價值</text>
<rect class="n wm" x="290" y="40" width="130" height="56" rx="10"/>
<text x="355" y="64" text-anchor="middle" class="b wm">DreamerV3</text>
<text x="355" y="84" text-anchor="middle" class="s">想像中 RL</text>
<rect class="n key" x="330" y="200" width="100" height="56" rx="10"/>
<text x="380" y="224" text-anchor="middle" class="b">GAIA-1</text>
<text x="380" y="244" text-anchor="middle" class="s">自駕影片</text>
<rect class="n key" x="440" y="200" width="100" height="56" rx="10"/>
<text x="490" y="224" text-anchor="middle" class="b">UniSim</text>
<text x="490" y="244" text-anchor="middle" class="s">通用模擬器</text>
<rect class="n key" x="550" y="200" width="100" height="56" rx="10"/>
<text x="600" y="224" text-anchor="middle" class="b">Genie</text>
<text x="600" y="244" text-anchor="middle" class="s">自學潛動作</text>
<rect class="n key" x="660" y="200" width="110" height="56" rx="10"/>
<text x="715" y="224" text-anchor="middle" class="b">Cosmos</text>
<text x="715" y="244" text-anchor="middle" class="s">基礎模型平台</text>
<rect class="n vla" x="640" y="40" width="140" height="56" rx="10"/>
<text x="710" y="64" text-anchor="middle" class="b vla">V-JEPA 2</text>
<text x="710" y="84" text-anchor="middle" class="s">表徵空間規劃</text>
<text x="230" y="124" text-anchor="middle" class="s wm">上排綠：潛空間 / 強化學習路線</text>
<text x="550" y="290" text-anchor="middle" class="s">下排橘：生成畫面的模擬器路線</text>
<text x="710" y="124" text-anchor="middle" class="s vla">藍：JEPA 表徵路線</text>
</svg>
<figcaption>三條路線不是互相取代，而是對「要預測什麼」的不同答案。2023 年以後生成式路線因為影片模型成熟而爆發，但潛空間與表徵路線在需要快速規劃時仍佔優勢。</figcaption>
</figure>

**建議閱讀順序**：World Models（建立直覺）→ DreamerV3（潛空間路線的集大成）→ MuZero（「不預測畫面也能規劃」）→ Genie（從無標註影片學動作）→ UniSim、GAIA-1（生成式模擬器怎麼用）→ Cosmos（工業級資料與訓練）→ V-JEPA 2（回到表徵、接上真實機器人）。

## World Models {#world-models}

**David Ha、Jürgen Schmidhuber，2018**｜[arXiv:1803.10122](https://arxiv.org/abs/1803.10122)｜[互動版論文](https://worldmodels.github.io/)｜NeurIPS 2018 版本題為 *Recurrent World Models Facilitate Policy Evolution*

!!! key "精髓"
    **把「看、記、做」拆開：大模型（約 500 萬參數）用無監督方式學會壓縮畫面與預測未來，只用 867 個參數的線性控制器做決策；控制器甚至可以完全在模型的「夢境」裡訓練，再搬回真實環境。**

### 背景與問題

- 人腦會建立外界的內部模型並預測感官輸入，例如打者在球飛到之前就揮棒。強化學習也需要「對過去的好表徵 + 對未來的預測」。
- 但無模型強化學習很難訓練大網路：獎勵訊號稀疏，信用分配（credit assignment）困難，所以典型策略網路只有 10³–10⁶ 個參數。
- **要解決的問題**：怎麼讓智能體從原始像素學到好用的環境表徵，同時又不讓決策部分大到難以用獎勵訓練？

### 解法：V、M、C 三個元件

<figure class="dg">
<svg viewBox="0 0 800 250" role="img" aria-label="World Models 的 V、M、C 架構">
<rect class="n" x="10" y="90" width="110" height="60" rx="10"/>
<text x="65" y="116" text-anchor="middle" class="b">畫面</text>
<text x="65" y="136" text-anchor="middle" class="s">64×64×3</text>
<rect class="n wm" x="160" y="80" width="150" height="80" rx="12"/>
<text x="235" y="110" text-anchor="middle" class="b wm">V：VAE</text>
<text x="235" y="132" text-anchor="middle" class="s">壓成 z（32／64 維）</text>
<rect class="n wm" x="360" y="80" width="170" height="80" rx="12"/>
<text x="445" y="110" text-anchor="middle" class="b wm">M：MDN-RNN</text>
<text x="445" y="132" text-anchor="middle" class="s">LSTM + 5 個高斯混合</text>
<rect class="n vla" x="590" y="80" width="190" height="80" rx="12"/>
<text x="685" y="110" text-anchor="middle" class="b vla">C：線性控制器</text>
<text x="685" y="132" text-anchor="middle" class="s">a = W[z, h] + b，867 參數</text>
<path class="ar" d="M120,120 H158"/>
<path class="ar wm" d="M310,120 H358"/>
<path class="ar wm" d="M530,120 H588"/>
<path class="ar wm" d="M235,160 V200 H640 V162"/>
<text x="440" y="218" text-anchor="middle" class="s">z 也直接送給 C</text>
<path class="ar vla dash" d="M685,80 V40 H445 V78"/>
<text x="565" y="32" text-anchor="middle" class="s">動作 a 回饋給 M，預測下一個 z</text>
</svg>
<figcaption>V 管「看」、M 管「記與預測」、C 管「做」。世界模型（V + M）完全沒看過獎勵，只有 C 用到獎勵。資料來源：<a href="https://arxiv.org/abs/1803.10122">arXiv:1803.10122</a>。</figcaption>
</figure>

| 元件 | 結構 | 參數量（賽車／VizDoom） | 訓練方式 |
|---|---|---|---|
| **V**：視覺 | 4 層卷積編碼器 + 4 層反卷積解碼器的 VAE；z 維度 32／64 | 4,348,547／4,446,915 | 重建 L2 + KL，1 個 epoch |
| **M**：記憶 | LSTM（256／512 隱藏單元）+ 混合密度網路，5 個對角高斯；VizDoom 版另外預測「是否死亡」 | 422,368／1,678,785 | 預測下一個 z，20 個 epoch |
| **C**：控制器 | 單層線性 + tanh | 867／1,088 | **CMA-ES 演化策略**，族群 64，每個候選跑 16 局取平均 |

**為什麼控制器這麼小**：把複雜度全部放進可以無監督訓練的 V 和 M，獎勵只需要調一個極小的搜尋空間，所以能用不需要梯度的演化策略。

### 資料怎麼來

- 兩個環境都用**隨機策略跑 10,000 局**收集畫面與動作，先訓練 V，再把畫面轉成 z 訓練 M。
- V 和 M 在單張 GPU 上各不到一小時。

### 評估與結果

**CarRacing-v0**（隨機生成賽道，100 局平均分數，900 分算解決）：

| 方法 | 分數 |
|---|---|
| DQN | 343 ± 18 |
| A3C（連續動作） | 591 ± 45 |
| Gym 排行榜最佳 | 838 ± 11 |
| 只用 V（控制器只看 z） | 632 ± 251 |
| **完整世界模型（V + M）** | **906 ± 21**，首個解決此任務的方法 |

只看 z 的控制器會左右搖擺、過不了急彎；加入 M 的隱藏狀態 h（等於「對未來的預期」）後駕駛穩定許多。

**VizDoom Take Cover，完全在夢裡訓練**：控制器只在 M 生成的潛空間裡練習，搬回真實遊戲平均存活約 1,100 步（及格線 750 步）。

| 夢境溫度 τ | 夢裡分數 | 真實分數 |
|---|---|---|
| 0.10 | 2086 ± 140 | 193 ± 58（比隨機策略還差） |
| 1.00 | 1145 ± 690 | 868 ± 511 |
| **1.15** | 918 ± 546 | **1092 ± 556** |
| 1.30 | 732 ± 269 | 753 ± 139 |

!!! warn "這張表是整個領域最重要的教訓之一"
    溫度太低時，夢裡的火球根本不出現，控制器在夢中拿高分、在真實世界一敗塗地，這就是**策略鑽世界模型漏洞（model exploitation）**。提高溫度讓夢「更難、更不確定」，反而讓策略更穩健。後來 Dreamer、DreamGen、WMPO 都在處理同一個問題。

### 局限（作者自述）

- VAE 不知道任務是什麼，可能把容量浪費在無關細節（Doom 的牆面花紋），卻漏掉重要的東西（賽車的路面）。
- 模型容量小，換到更複雜的環境需要更大的模型，也可能有災難性遺忘。
- M 只會一步一步預測，沒有分層規劃或抽象推理。

### 對 VLA 的意義

確立了「**先無監督學世界、再用少量獎勵或示範學決策**」的分工，以及「在世界模型裡訓練策略」的可行性與風險。今天 VLA 用世界模型做資料工廠或想像中 RL，問題框架都源自這篇。

## MuZero {#muzero}

**Julian Schrittwieser 等，DeepMind，2019（Nature 2020）**｜[arXiv:1911.08265](https://arxiv.org/abs/1911.08265)

!!! key "精髓"
    **世界模型不必重建畫面，只要預測「規劃真正需要的三個量」：獎勵、價值、策略。** 不給規則，MuZero 在圍棋、西洋棋、將棋追平 AlphaZero，在 Atari 超越當時最強的無模型方法。

### 背景與問題

- AlphaGo／AlphaZero 的樹搜尋很強，但前提是**知道遊戲規則**，可以完美模擬下一步。真實世界（機器人、工業控制）沒有規則可給。
- 當時的模型式強化學習多半學著**重建畫面或真實狀態**，在 Atari 這種視覺複雜的環境裡遠遠落後無模型方法。
- **要解決的問題**：不給規則，能不能靠學到的模型做規劃，同時在需要精準推演的棋類和視覺複雜的 Atari 都拿到頂尖成績？

### 解法：三個函數 + 在潛空間做 MCTS

<figure class="dg">
<svg viewBox="0 0 800 250" role="img" aria-label="MuZero 的表徵、動力學、預測三個函數">
<rect class="n" x="10" y="90" width="120" height="60" rx="10"/>
<text x="70" y="116" text-anchor="middle" class="b">過去的觀測</text>
<text x="70" y="136" text-anchor="middle" class="s">32 幀 + 32 個動作</text>
<rect class="n wm" x="160" y="90" width="110" height="60" rx="10"/>
<text x="215" y="116" text-anchor="middle" class="b wm">表徵 h</text>
<text x="215" y="136" text-anchor="middle" class="s">→ 根狀態 s⁰</text>
<rect class="n wm" x="320" y="90" width="130" height="60" rx="10"/>
<text x="385" y="116" text-anchor="middle" class="b wm">動力學 g</text>
<text x="385" y="136" text-anchor="middle" class="s">(sᵏ⁻¹, aᵏ) → rᵏ, sᵏ</text>
<rect class="n wm" x="500" y="90" width="130" height="60" rx="10"/>
<text x="565" y="116" text-anchor="middle" class="b wm">動力學 g</text>
<text x="565" y="136" text-anchor="middle" class="s">再往下推一步…</text>
<rect class="n key" x="320" y="190" width="310" height="50" rx="10"/>
<text x="475" y="220" text-anchor="middle" class="b">預測 f：每個 sᵏ → 策略 pᵏ、價值 vᵏ</text>
<rect class="n vla" x="660" y="90" width="130" height="60" rx="10"/>
<text x="725" y="116" text-anchor="middle" class="b vla">MCTS</text>
<text x="725" y="136" text-anchor="middle" class="s">挑出要做的動作</text>
<path class="ar" d="M130,120 H158"/>
<path class="ar wm" d="M270,120 H318"/>
<path class="ar wm" d="M450,120 H498"/>
<path class="ar vla" d="M630,120 H658"/>
<path class="ar dash" d="M385,150 V188"/>
<path class="ar dash" d="M565,150 V188"/>
<text x="400" y="40" text-anchor="middle" class="s">潛狀態 sᵏ 沒有固定意義：只被訓練成「能預測好 r、v、p」</text>
</svg>
<figcaption>和 World Models 最大的不同：<b>不解碼回畫面</b>。資料來源：<a href="https://arxiv.org/abs/1911.08265">arXiv:1911.08265</a>。</figcaption>
</figure>

- **表徵函數 h**：把過去觀測編碼成搜尋樹的根狀態。
- **動力學函數 g**：給定潛狀態與動作，輸出即時獎勵與下一個潛狀態（確定性的）。
- **預測函數 f**：從潛狀態輸出策略與價值。
- **規劃**：類似 AlphaZero 的 MCTS，每次模擬只呼叫一次 g 和一次 f；Q 值用樹中看到的最小最大值正規化到 [0, 1]，所以能處理沒有上下界的分數。

### 訓練

- 從回放資料中取一個時間點，把模型**往後展開 K = 5 步**，端到端反向傳播。
- 三個目標：策略對齊 MCTS 搜尋出的策略；價值對齊 n 步回報（Atari n = 10）；獎勵對齊真實觀測到的獎勵。
- 網路沿用 AlphaZero 的殘差結構（16 個殘差塊、256 通道）；Atari 輸入是最近 32 幀 96×96 畫面加 32 個動作，壓到 6×6 的潛狀態。
- 算力：棋類用 16 顆 TPU 訓練、1,000 顆 TPU 自我對弈；Atari 用 8 顆訓練、32 顆自我對弈。
- **MuZero Reanalyze**：用最新參數重新搜尋舊資料當訓練目標，大幅提升樣本效率。

### 評估與結果

**棋類**：在圍棋、西洋棋、將棋上達到 AlphaZero 的超人水準（AlphaZero 有規則可用）；圍棋略勝，而且每次評估用的殘差塊更少（16 vs 20）。學到的模型讓搜尋時間放大到約 10 秒仍持續變強，表現和完美模擬器一樣。

**Atari 57 款遊戲**（人類正規化分數）：

| 方法 | 中位數 | 平均 | 使用的環境幀數 |
|---|---|---|---|
| R2D2（無模型） | 1920.6% | 4024.9% | 375 億 |
| **MuZero** | **2041.1%** | **4999.2%** | 200 億 |
| MuZero Reanalyze | 731.1% | 2168.9% | 2 億 |

### 局限

- 動力學是確定性的，不直接處理隨機環境；也不處理撲克這類不完全資訊遊戲。
- Atari 上搜尋帶來的提升遠小於圍棋（約 100 次模擬後就飽和），作者歸因於模型不夠準。
- 部分遊戲表現很差（Montezuma's Revenge、Venture 拿 0 分），而且訓練需要成百上千顆 TPU。

### 對 VLA 的意義

MuZero 證明「**只學對決策有用的部分**」就夠規劃。今天推論時用世界模型挑候選動作的方法（V-JEPA 2-AC、VLA-Reasoner），以及「是否需要生成像素」的爭論，都可以追溯到這裡。

## DreamerV3 {#dreamerv3}

**Danijar Hafner、Jurgis Pasukonis、Jimmy Ba、Timothy Lillicrap，2023（Nature 2025）**｜[arXiv:2301.04104](https://arxiv.org/abs/2301.04104)｜[程式碼](https://github.com/danijar/dreamerv3)

!!! key "精髓"
    **一組固定的超參數，橫跨 150 多個任務都打贏各領域的專門演算法，並且第一次不靠人類資料或課程，從零在 Minecraft 挖到鑽石。** 關鍵不是新架構，而是一整套讓世界模型「對數值大小不敏感」的穩定化技巧。

### 背景與問題

- 強化學習演算法換個領域就要重新調參，PPO 雖然穩健，但需要大量經驗且常輸給專門方法。
- 各領域差異很大：獎勵尺度與稀疏程度、離散或連續動作、像素或向量輸入、2D 或 3D。
- **要解決的問題**：做出一個「不用調參就能用」的通用演算法，核心難點是讓世界模型在預測**大小未知的數值**時也穩定。

### 解法：世界模型 + 評論家 + 演員，三者一起訓練

<figure class="dg">
<svg viewBox="0 0 800 270" role="img" aria-label="DreamerV3 的 RSSM 世界模型與想像中訓練">
<rect class="n band" x="10" y="10" width="440" height="250" rx="14"/>
<text x="230" y="36" text-anchor="middle" class="h">世界模型（RSSM），從真實回放資料學</text>
<rect class="n" x="30" y="60" width="110" height="50" rx="8"/>
<text x="85" y="90" text-anchor="middle" class="b">觀測 xₜ</text>
<rect class="n wm" x="170" y="60" width="120" height="50" rx="8"/>
<text x="230" y="82" text-anchor="middle" class="b wm">編碼器</text>
<text x="230" y="100" text-anchor="middle" class="s">→ 離散潛變數 zₜ</text>
<rect class="n wm" x="170" y="140" width="120" height="50" rx="8"/>
<text x="230" y="162" text-anchor="middle" class="b wm">序列模型</text>
<text x="230" y="180" text-anchor="middle" class="s">GRU，狀態 hₜ</text>
<rect class="n wm" x="310" y="140" width="125" height="50" rx="8"/>
<text x="372" y="162" text-anchor="middle" class="b wm">動力學預測器</text>
<text x="372" y="180" text-anchor="middle" class="s">只看 hₜ 猜 zₜ</text>
<rect class="n" x="30" y="200" width="250" height="44" rx="8"/>
<text x="155" y="227" text-anchor="middle" class="s">解碼器、獎勵預測器、是否結束預測器</text>
<path class="ar" d="M140,85 H168"/>
<path class="ar wm" d="M230,110 V138"/>
<path class="ar wm" d="M290,165 H308"/>
<path class="ar dash" d="M230,190 V198"/>
<rect class="n band" x="480" y="10" width="310" height="250" rx="14"/>
<text x="635" y="36" text-anchor="middle" class="h">在想像中學決策</text>
<rect class="n wm" x="500" y="60" width="270" height="50" rx="8"/>
<text x="635" y="82" text-anchor="middle" class="b wm">用動力學預測器往前想像 15 步</text>
<text x="635" y="100" text-anchor="middle" class="s">不需要任何真實觀測</text>
<rect class="n key" x="500" y="130" width="125" height="50" rx="8"/>
<text x="562" y="152" text-anchor="middle" class="b">評論家</text>
<text x="562" y="170" text-anchor="middle" class="s">預測回報分布</text>
<rect class="n vla" x="645" y="130" width="125" height="50" rx="8"/>
<text x="707" y="152" text-anchor="middle" class="b vla">演員</text>
<text x="707" y="170" text-anchor="middle" class="s">選動作</text>
<text x="635" y="215" text-anchor="middle" class="s">λ-return，H = 15、λ = 0.95</text>
<text x="635" y="235" text-anchor="middle" class="s">γ = 0.997（約 333 步的視野）</text>
<path class="ar wm" d="M435,165 H460 V85 H498"/>
<path class="ar" d="M635,110 V128"/>
</svg>
<figcaption>「動力學預測器只看 hₜ」是能在想像中滾動的關鍵：不需要真實畫面就能猜下一個潛狀態。資料來源：<a href="https://arxiv.org/abs/2301.04104">arXiv:2301.04104</a>。</figcaption>
</figure>

**世界模型的損失**：

| 損失 | 作用 | 權重 |
|---|---|---|
| 預測損失 | 重建觀測、預測獎勵與是否結束 | 1 |
| 動力學損失 | KL，讓序列模型學會預測下一個潛變數（編碼器側停止梯度） | 1 |
| 表徵損失 | 反方向 KL，讓潛變數更容易被預測（動力學側停止梯度） | 0.1 |

兩個 KL 都設 **free bits**（低於 1 nat 就不再懲罰），避免潛變數塌縮成沒資訊的解。

**讓一組超參數通用的穩定化技巧**：

- **symlog 轉換**：`sign(x)·ln(|x|+1)`，把很大的數值壓小、接近零時幾乎不變，用在向量觀測與解碼目標。
- **symexp twohot 損失**：獎勵與評論家不直接回歸數值，而是在 255 個指數間距的格子上做分類，梯度大小因此和目標數值大小無關。
- **百分位回報正規化**：用批次中回報的第 95 與第 5 百分位差當尺度，只把大回報縮小、小回報不放大，稀疏獎勵也不會被雜訊放大。
- 1% 均勻分布混入（unimix）、自適應梯度裁剪、LaProp 最佳化器、RMSNorm + SiLU。

**模型大小**：12M、25M、50M、100M、200M（預設）、400M，對應隱藏維度 256 到 1536。

### 資料與評估

全部在單張 A100 上跑，固定超參數。評估就是各基準的標準分數：

| 基準 | 任務數 | 預算 | DreamerV3 | 對照 |
|---|---|---|---|---|
| Atari | 57 | 2 億幀 | 中位數 830%、平均 3381% | MuZero 693%、3054% |
| ProcGen | 16 | 5,000 萬步 | 66.01 | PPG 64.89、PPO 42.80 |
| DMLab | 30 | 1 億步 | 71.4% | IMPALA 用 10 億步才 66.3% |
| Atari100k | 26 | 40 萬步 | 平均 125% | 勝過 IRIS、SimPLe，輸 EfficientZero（190%） |
| 本體感知控制 | 18 | 50 萬步 | 871 | D4PG 792、PPO 94 |
| 視覺控制 | 20 | 100 萬步 | 861 | DrQ-v2 770 |
| Minecraft 鑽石 | 1 | 1 億步 | 回報 9.1 | IMPALA 7.1、PPO 5.1 |

**擴展性**：模型從 12M 加大到 400M，表現單調上升，而且越大的模型需要越少的環境互動。

### 局限

- Minecraft 在 1 億步時只有約 0.4% 的回合挖到鑽石，任務本身也用了簡化的方塊破壞設定。
- BSuite 的探索類別幾乎得 0 分（0.01，Boot DQN 為 0.68）。
- DMLab 的對照組是用 10 倍資料的已發表結果，比較不完全公平。

### 對 VLA 的意義

DreamerV3 是「**想像中強化學習**」的標準答案。WMPO、VLA-RFT 這類讓 VLA 在世界模型裡做 RL 的方法，以及 Dreamer 4 在 Minecraft 純離線學習，都建立在它的穩定化技巧上。

## GAIA-1 {#gaia-1}

**Anthony Hu 等，Wayve，2023**｜[arXiv:2309.17080](https://arxiv.org/abs/2309.17080)

!!! key "精髓"
    **把自駕的世界模型當成「下一個 token 預測」：影像、文字、車輛動作全部變成 token 交錯排列，用 65 億參數的 Transformer 學會「如果我這樣開，世界會怎麼變」，再用擴散解碼器畫成高畫質影片。**

### 背景與問題

- 自駕車必須預測場景會如何隨自己的動作演變；但過去的世界模型常依賴難以擴展的標註資料，模擬器又缺乏真實世界的複雜度。
- 一般影片生成模型畫得逼真，但不一定學到精確的動態，也不能用動作控制。
- **要解決的問題**：用大量未標註的真實行車影片，學出一個可用動作與文字控制、能生成多種合理未來的駕駛世界模型。

### 解法：三段式架構

<figure class="dg">
<svg viewBox="0 0 800 230" role="img" aria-label="GAIA-1 的影像 tokenizer、世界模型與影片解碼器">
<rect class="n" x="10" y="30" width="130" height="44" rx="8"/>
<text x="75" y="57" text-anchor="middle" class="b">影片</text>
<rect class="n" x="10" y="90" width="130" height="44" rx="8"/>
<text x="75" y="117" text-anchor="middle" class="b">文字</text>
<rect class="n" x="10" y="150" width="130" height="44" rx="8"/>
<text x="75" y="172" text-anchor="middle" class="b">動作</text>
<text x="75" y="188" text-anchor="middle" class="s">車速、曲率</text>
<rect class="n wm" x="175" y="20" width="150" height="64" rx="8"/>
<text x="250" y="46" text-anchor="middle" class="b wm">影像 tokenizer</text>
<text x="250" y="68" text-anchor="middle" class="s">每幀 576 個 token</text>
<rect class="n" x="175" y="94" width="150" height="40" rx="8"/>
<text x="250" y="119" text-anchor="middle" class="s">T5：每步 32 個 token</text>
<rect class="n" x="175" y="150" width="150" height="44" rx="8"/>
<text x="250" y="177" text-anchor="middle" class="s">線性層：2 個 token</text>
<rect class="n key" x="365" y="60" width="200" height="100" rx="12"/>
<text x="465" y="94" text-anchor="middle" class="b">世界模型 6.5B</text>
<text x="465" y="118" text-anchor="middle" class="s">自迴歸 Transformer</text>
<text x="465" y="138" text-anchor="middle" class="s">預測下一個影像 token</text>
<rect class="n wm" x="600" y="60" width="190" height="100" rx="12"/>
<text x="695" y="94" text-anchor="middle" class="b wm">影片擴散解碼器 2.6B</text>
<text x="695" y="118" text-anchor="middle" class="s">3D U-Net</text>
<text x="695" y="138" text-anchor="middle" class="s">補幀到 25 Hz</text>
<path class="ar" d="M140,52 H173"/>
<path class="ar" d="M140,112 H173"/>
<path class="ar" d="M140,172 H173"/>
<path class="ar" d="M325,52 H345 V100 H363"/>
<path class="ar" d="M325,114 H363"/>
<path class="ar" d="M325,172 H345 V130 H363"/>
<path class="ar wm" d="M565,110 H598"/>
<text x="465" y="200" text-anchor="middle" class="s">每個時間步 32 + 576 + 2 = 610 個 token，交錯排列</text>
</svg>
<figcaption>世界模型負責「推理場景結構與動態」，解碼器負責「畫得好看」。資料來源：<a href="https://arxiv.org/abs/2309.17080">arXiv:2309.17080</a>。</figcaption>
</figure>

| 元件 | 參數 | 細節 |
|---|---|---|
| 影像 tokenizer | 約 0.3B | 全卷積 U-Net 自編碼器，288×512 輸入下採樣 16 倍 → 18×32 = 576 個 token，詞彙 8,192；另加 **DINO 蒸餾損失**讓 token 帶語意 |
| 世界模型 | 6.5B | 自迴歸 Transformer，影片從 25 Hz 降到 6.25 Hz，每段 26 步（約 4 秒）共 15,860 個 token；訓練時 20% 無條件、40% 動作條件、40% 文字條件 |
| 影片解碼器 | 2.6B | 3D U-Net 擴散模型，同時訓練生成、補幀等 4 種任務，DDIM 50 步 |

### 資料集構建

- **4,700 小時**倫敦行車影片（2019–2023），約 4.2 億張不重複影像，25 Hz。
- **平衡取樣**：依經緯度、天氣、轉向與速度行為的分布，用「反比於經驗分布的 0.5 次方」加權，避免模型只學到最常見的直線巡航。
- **驗證集**：400 小時未參與訓練的行程，刻意包含**訓練中從未出現的地理區域**，用來看泛化。

### 評估

- **定量**：在驗證集上的交叉熵。用 0.65M 到 650M 的小模型擬合冪律，準確預測了完整模型的最終損失，說明**駕駛世界模型也有類似語言模型的擴展定律**。
- **取樣策略**：argmax 會陷入重複，完全隨機會取到不可靠的長尾 token；top-k = 50 最接近真實資料的困惑度。
- **定性能力**：生成數分鐘長的影片、從同一段起始影片生成多種未來（讓行或轉彎）、用文字改天氣與時段、做**反事實駕駛**（例如故意開出車道，其他車會合理反應）、湧現出幾何理解（過減速帶時車身俯仰）。
- 訓練算力：tokenizer 32 張 A100 4 天、世界模型 64 張 A100 15 天、解碼器 32 張 A100 15 天。

### 局限

- 自迴歸生成無法即時。
- 文字與標註來源不完美，需要 classifier-free guidance，且要依用途調參。
- **沒有下游駕駛表現的評估**，主要靠交叉熵與定性範例。

### 對 VLA 的意義

GAIA-1 示範了**把動作當 token 混進生成模型**的做法，也是自駕「世界模型當資料工廠與反事實測試」的起點。後續 GAIA-2（多鏡頭）、Waymo 基於 Genie 3 的世界模型都是同一條路。

## UniSim {#unisim}

**Sherry Yang 等，Google DeepMind、UC Berkeley、MIT，2023（ICLR 2024 傑出論文）**｜[arXiv:2310.06114](https://arxiv.org/abs/2310.06114)｜[專案頁](https://universal-simulator.github.io/unisim/)

!!! key "精髓"
    **沒有單一資料集同時有豐富的場景、動作和物理細節，所以把 14 種資料集（模擬、真機、人類影片、全景掃描、網路圖文）統一成「給動作、出影片」的格式，訓練一個通用模擬器；在裡面訓練的策略能零樣本搬到真實機器人。**

### 背景與問題

- 不同資料各缺一塊：圖文資料場景豐富但沒有動作；影片字幕資料只有高層描述；人類活動資料動作豐富但缺機械細節；機器人資料動作精確但量少。
- **要解決的問題**：怎麼把這些異質資料合成一個「什麼動作都能模擬」的真實世界模擬器，並證明它真的能拿來訓練策略？

### 解法：統一的「動作進、影片出」介面

<figure class="dg">
<svg viewBox="0 0 800 260" role="img" aria-label="UniSim 把不同資料統一成動作與影片">
<rect class="n" x="10" y="20" width="200" height="40" rx="8"/>
<text x="110" y="45" text-anchor="middle" class="s">網路圖文：圖片說明當動作</text>
<rect class="n" x="10" y="70" width="200" height="40" rx="8"/>
<text x="110" y="95" text-anchor="middle" class="s">人類活動：標籤轉成文字動作</text>
<rect class="n" x="10" y="120" width="200" height="40" rx="8"/>
<text x="110" y="145" text-anchor="middle" class="s">機器人：馬達指令離散成 4096 格</text>
<rect class="n" x="10" y="170" width="200" height="40" rx="8"/>
<text x="110" y="195" text-anchor="middle" class="s">全景掃描：相機位姿轉成「左轉」等</text>
<rect class="n wm" x="270" y="70" width="220" height="110" rx="12"/>
<text x="380" y="104" text-anchor="middle" class="b wm">UniSim 5.6B</text>
<text x="380" y="128" text-anchor="middle" class="s">影片擴散（3D U-Net）</text>
<text x="380" y="148" text-anchor="middle" class="s">條件：最近 4 幀 + 動作</text>
<rect class="n vla" x="550" y="30" width="240" height="56" rx="10"/>
<text x="670" y="54" text-anchor="middle" class="b vla">訓練高層 VLM 策略</text>
<text x="670" y="74" text-anchor="middle" class="s">長任務成功率約 3–4 倍</text>
<rect class="n vla" x="550" y="100" width="240" height="56" rx="10"/>
<text x="670" y="124" text-anchor="middle" class="b vla">在模擬器裡做 RL</text>
<text x="670" y="144" text-anchor="middle" class="s">成功率 0.58 → 0.81</text>
<rect class="n" x="550" y="170" width="240" height="56" rx="10"/>
<text x="670" y="194" text-anchor="middle" class="b">生成資料訓練影片字幕</text>
<text x="670" y="214" text-anchor="middle" class="s">跨資料集泛化更好</text>
<path class="ar" d="M210,40 H240 V110 H268"/>
<path class="ar" d="M210,90 H240"/>
<path class="ar" d="M210,140 H268"/>
<path class="ar" d="M210,190 H240 V150 H268"/>
<path class="ar wm" d="M490,110 H520 V58 H548"/>
<path class="ar wm" d="M490,128 H548"/>
<path class="ar wm" d="M490,150 H520 V198 H548"/>
<text x="380" y="240" text-anchor="middle" class="s">自迴歸滾動：把生成的影片接回去當下一步的歷史</text>
</svg>
<figcaption>文字動作用 T5 編碼；低階控制先正規化再離散成 4096 格，和語言嵌入串接。資料來源：<a href="https://arxiv.org/abs/2310.06114">arXiv:2310.06114</a>。</figcaption>
</figure>

- **模型**：影片擴散模型（預測雜訊、cosine 排程），動作用 classifier-free guidance 注入；最近 4 幀以通道方式串接當歷史條件。基礎模型生成 24×40，再經兩級超解析度到 192×320。
- **規模與算力**：5.6B 參數，512 顆 TPU-v3 訓練約 20 天、100 萬步。

### 資料集構建（14 個資料集混合）

| 類別 | 資料集（筆數） | 取樣權重 |
|---|---|---|
| 模擬 | Habitat HM3D（710）、Language Table 模擬（16 萬） | 0.1、0.05 |
| 真實機器人 | Bridge（2 千）、RT-1（7 萬）、Language Table 真機（44 萬）、其他（13.3 萬） | 0.05–0.1 |
| 人類活動 | Ego4D（350 萬）、Something-Something V2（16 萬）、EPIC-KITCHENS（2.5 萬）、其他（5 萬） | 0.05–0.1 |
| 全景掃描 | Matterport Room-to-Room（350 萬） | 0.1 |
| 網路 | LAION-400M、ALIGN（各 4 億）、其他影片（1,300 萬） | 各 0.05 |

作者坦承權重沒有仔細調（只用 0.1 或 0.05）。

### 評估指標與結果

- **影片品質**：FVD、FID、Inception Score、CLIP 分數。消融顯示：條件用最近 4 幀比只用 1 幀好很多（FVD 315.7 → 211.3）；拿掉網路資料 FVD 變差到 307.8；模型從 500M 到 5.6B 持續改善但趨緩。
- **長任務 VLM 策略**（Language Table，指標是「與目標距離的縮減量 RDG」）：一般行為克隆 0.11，用模擬器生成 1 萬條長軌跡做 hindsight 標註後 **0.34**，並零樣本在真機上完成任務。
- **RL 策略**（48 個任務成功率）：行為克隆 0.58，在 UniSim 裡用 REINFORCE 微調後 **0.81**；指向類任務從 0.12 升到 0.71，同樣零樣本搬到真機。
- **影片字幕**：只用生成影片微調，在 ActivityNet 上達到真實資料約 84% 的效果，在另外三個資料集上反而更好。

### 局限

- **幻覺**：要求不合理的動作（叫桌面機器人「洗手」）時會生成荒謬結果，而不是拒絕。
- **記憶有限**：只看最近幾幀，記不住長期狀態。
- 機器人形態只有約 4 種，跨形態泛化有限；只模擬視覺，沒有力、聲音。

### 對 VLA 的意義

UniSim 是第一個系統性證明「**在生成式世界模型裡訓練的 VLA 策略可以零樣本搬到真機**」的工作，直接啟發了 DreamGen、Cosmos 的資料工廠路線，以及用世界模型做 VLA 強化學習的研究。

## Genie {#genie}

**Jake Bruce 等，Google DeepMind，2024（ICML 2024 最佳論文）**｜[arXiv:2402.15391](https://arxiv.org/abs/2402.15391)｜[專案頁](https://sites.google.com/view/genie-2024)

!!! key "精髓"
    **網路影片沒有動作標籤，Genie 就自己從影片裡「發明」動作：讓模型找出 8 個最能解釋前後幀變化的潛動作。只用 3 萬小時無標註的平台遊戲影片，就學會一個能逐幀操控的生成世界。**

### 背景與問題

- 可控的世界模型通常需要動作標註資料，但網路上海量影片幾乎都沒有動作標籤。
- **要解決的問題**：只用無標註影片，學出一個使用者可以逐幀操控的互動環境。

### 解法：三個元件，全部用時空 Transformer

<figure class="dg">
<svg viewBox="0 0 800 270" role="img" aria-label="Genie 的潛動作模型、影片 tokenizer 與動力學模型">
<rect class="n band" x="10" y="10" width="380" height="250" rx="14"/>
<text x="200" y="36" text-anchor="middle" class="h">訓練時：從影片自學動作</text>
<rect class="n" x="30" y="60" width="140" height="50" rx="8"/>
<text x="100" y="82" text-anchor="middle" class="b">前面各幀</text>
<text x="100" y="100" text-anchor="middle" class="s">+ 下一幀</text>
<rect class="n key" x="200" y="55" width="170" height="60" rx="10"/>
<text x="285" y="80" text-anchor="middle" class="b">潛動作模型 300M</text>
<text x="285" y="100" text-anchor="middle" class="s">VQ 壓成 8 個離散動作</text>
<rect class="n wm" x="30" y="150" width="140" height="56" rx="8"/>
<text x="100" y="174" text-anchor="middle" class="b wm">影片 tokenizer</text>
<text x="100" y="194" text-anchor="middle" class="s">ST-ViViT，200M</text>
<rect class="n wm" x="200" y="145" width="170" height="66" rx="10"/>
<text x="285" y="172" text-anchor="middle" class="b wm">動力學模型 10.1B</text>
<text x="285" y="194" text-anchor="middle" class="s">MaskGIT 預測下一幀 token</text>
<path class="ar" d="M170,85 H198"/>
<path class="ar" d="M170,178 H198"/>
<path class="ar dash" d="M285,115 V143"/>
<text x="330" y="133" class="s">潛動作</text>
<rect class="n band" x="420" y="10" width="370" height="250" rx="14"/>
<text x="605" y="36" text-anchor="middle" class="h">推論時：使用者就是潛動作</text>
<rect class="n" x="440" y="60" width="150" height="50" rx="8"/>
<text x="515" y="82" text-anchor="middle" class="b">一張提示圖</text>
<text x="515" y="100" text-anchor="middle" class="s">文字生成、照片、手繪</text>
<rect class="n vla" x="620" y="60" width="150" height="50" rx="8"/>
<text x="695" y="82" text-anchor="middle" class="b vla">使用者按鍵</text>
<text x="695" y="100" text-anchor="middle" class="s">0–7 其中一個</text>
<rect class="n wm" x="500" y="150" width="210" height="56" rx="10"/>
<text x="605" y="174" text-anchor="middle" class="b wm">動力學模型逐幀生成</text>
<text x="605" y="194" text-anchor="middle" class="s">潛動作模型此時丟掉不用</text>
<path class="ar" d="M515,110 V130 H580 V148"/>
<path class="ar vla" d="M695,110 V130 H630 V148"/>
</svg>
<figcaption>潛動作只有 8 個，逼模型把「最主要的變化」（往左、往右、跳）分配到不同代碼上，於是自然對應到可操控的動作。資料來源：<a href="https://arxiv.org/abs/2402.15391">arXiv:2402.15391</a>。</figcaption>
</figure>

| 元件 | 參數 | 做法 |
|---|---|---|
| **時空 Transformer（ST-transformer）** | — | 空間注意力只在同一幀內，時間注意力只沿時間軸且是因果的；計算量隨幀數線性而非平方成長 |
| **影片 tokenizer（ST-ViViT）** | 約 200M | VQ-VAE，patch 4、碼本 1,024 |
| **潛動作模型（LAM）** | 約 300M | 編碼器看過去幀與下一幀，輸出潛動作；解碼器用歷史 + 潛動作重建下一幀；VQ 碼本限制為 **8 個動作**；直接吃像素效果比吃 token 好 |
| **動力學模型** | 10.1B | decoder-only MaskGIT，動作以嵌入相加；推論每幀 25 步 MaskGIT |

### 資料集構建

- **平台遊戲資料**：用關鍵字篩出 5,500 萬段 16 秒影片（約 24.4 萬小時），10 FPS、160×90。
- **品質過濾**：人工標註 1 萬段影片（1–5 分），訓練 11M 參數的 ResNet18 分類器自動篩選，最後留下 **680 萬段（3 萬多小時）**。消融顯示篩過的資料讓 FVD 從 61.4 降到 54.8。**資料品質比數量更重要。**
- **機器人資料**：RT-1 約 13 萬條示範加其他真機資料，丟掉動作標籤，當純影片訓練。

### 評估指標與結果

- **FVD**：影片品質。
- **ΔtPSNR（可控性）**：用「從真實影片推出的潛動作」生成的畫面 PSNR，減去「隨機潛動作」生成的 PSNR。數值越大，代表動作對結果的影響越大、越可控。
- **擴展**：模型從 4,100 萬到 27 億參數，訓練損失穩定下降；最終模型在 256 顆 TPUv5p 上訓練，約 9,420 億 token。
- **tokenizer 消融**：ST-ViViT 的 FVD 81.4、ΔtPSNR 1.66，勝過一般 ViT（114.5、1.39）和 C-ViViT（272.7、1.37）。
- **泛化**：給它沒看過的文字生成圖、手繪草圖、真實照片都能操控，還湧現出前景背景的視差。
- **訓練智能體**：在 CoinRun 裡，用潛動作模型替專家影片標上潛動作，再用少量真實動作資料做對應，**只要 200 筆**就追平有完整動作標籤的行為克隆。

### 局限

- 約 **1 FPS**，太慢無法真正互動（後來的 Genie 3 做到 24 FPS）。
- 會產生不真實的未來；記憶只有 16 幀，長時間一致性差。

### 對 VLA 的意義

**潛動作（latent action）**是 VLA 利用網路影片的關鍵技術：LAPA、UniVLA、GR00T N1、智元 GO-1 都用類似方法，替沒有動作標籤的人類或網路影片補上偽動作來預訓練。

## Cosmos {#cosmos}

**NVIDIA，2025**｜[arXiv:2501.03575](https://arxiv.org/abs/2501.03575)｜[GitHub](https://github.com/nvidia-cosmos)｜[NVIDIA 技術部落格](https://developer.nvidia.com/blog/advancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform)

!!! key "精髓"
    **把世界模型當成「基礎模型」來做：先用 2,000 萬小時影片預訓練一個通用的世界基礎模型（WFM），再用少量特定環境的資料後訓練成機器人或自駕專用模型。論文最大的貢獻其實是工業級的資料管線與 tokenizer，而且全部開源。**

### 背景與問題

- 物理 AI（機器人、自駕）需要大量「觀測 + 動作」交錯的資料，但真實收集又貴又危險，探索性動作可能弄壞機器或周遭環境。
- 作者主張物理 AI 應該先在數位世界訓練：需要策略的數位分身，也需要**世界的數位分身**，也就是世界模型。
- **要解決的問題**：提供一個開放的平台，讓開發者不必從零訓練，就能做出自己場景專用的世界模型。

### 解法：五個元件的平台

<figure class="dg">
<svg viewBox="0 0 800 220" role="img" aria-label="Cosmos 平台：資料管線、tokenizer、預訓練、後訓練、防護">
<rect class="n" x="10" y="70" width="140" height="80" rx="10"/>
<text x="80" y="100" text-anchor="middle" class="b">影片資料管線</text>
<text x="80" y="122" text-anchor="middle" class="s">2,000 萬小時</text>
<text x="80" y="140" text-anchor="middle" class="s">→ 約 1 億段</text>
<rect class="n wm" x="175" y="70" width="140" height="80" rx="10"/>
<text x="245" y="100" text-anchor="middle" class="b wm">Cosmos Tokenizer</text>
<text x="245" y="122" text-anchor="middle" class="s">連續與離散</text>
<text x="245" y="140" text-anchor="middle" class="s">壓縮 8×8×8 等</text>
<rect class="n key" x="340" y="30" width="190" height="70" rx="10"/>
<text x="435" y="58" text-anchor="middle" class="b">擴散 WFM 7B／14B</text>
<text x="435" y="80" text-anchor="middle" class="s">DiT，Text2World、Video2World</text>
<rect class="n key" x="340" y="120" width="190" height="70" rx="10"/>
<text x="435" y="148" text-anchor="middle" class="b">自迴歸 WFM 4B–13B</text>
<text x="435" y="170" text-anchor="middle" class="s">Llama3 式 GPT，預測影片 token</text>
<rect class="n vla" x="560" y="70" width="140" height="80" rx="10"/>
<text x="630" y="100" text-anchor="middle" class="b vla">後訓練</text>
<text x="630" y="122" text-anchor="middle" class="s">相機控制、機器人</text>
<text x="630" y="140" text-anchor="middle" class="s">多鏡頭自駕</text>
<rect class="n" x="720" y="70" width="70" height="80" rx="10"/>
<text x="755" y="106" text-anchor="middle" class="b">防護</text>
<text x="755" y="126" text-anchor="middle" class="s">前後過濾</text>
<path class="ar" d="M150,110 H173"/>
<path class="ar wm" d="M315,100 H325 V65 H338"/>
<path class="ar wm" d="M315,120 H325 V155 H338"/>
<path class="ar" d="M530,65 H545 V100 H558"/>
<path class="ar" d="M530,155 H545 V120 H558"/>
<path class="ar" d="M700,110 H718"/>
</svg>
<figcaption>所有世界基礎模型在 10,000 張 H100 上訓練約三個月。資料來源：<a href="https://arxiv.org/abs/2501.03575">arXiv:2501.03575</a>。</figcaption>
</figure>

### 資料集構建：論文篇幅最多的部分

| 步驟 | 做法 |
|---|---|
| 原始資料 | 約 2,000 萬小時、720p 到 4K 的影片 |
| 切段 | 用 TransNetV2 做鏡頭切換偵測，丟掉短於 2 秒、切開長於 60 秒的片段 |
| 轉碼 | 統一成 mp4，換用 GPU 硬體編碼後吞吐量提升約 6.5 倍 |
| 過濾 | 光流分類器濾掉太靜或太晃的；品質分數最低 15% 丟掉；濾掉有大量疊字的；依類型分類器排除電玩、動畫並重新平衡類別 |
| 標註 | 內部 13B VILA 模型看 8 幀寫說明，平均 97 個英文字 |
| 去重 | 語意去重（k-means，k = 10,000），刪掉約 30% |
| 產出 | 約 1 億段預訓練片段（2–60 秒）、約 1,000 萬段微調片段 |

### 模型細節

- **Tokenizer**：連續版（給擴散模型，潛維度 16）與離散版（給自迴歸模型，FSQ 碼本 64,000），影片壓縮率 4×8×8、8×8×8、8×16×16。在 DAVIS 上比既有 tokenizer 高約 4 dB PSNR，編碼快最多 12 倍。
- **擴散 WFM**：DiT 架構，3D patch、3D RoPE，T5-XXL 文字以 cross-attention 注入；7B（28 層）與 14B（36 層）。漸進訓練：512p、57 幀 → 720p、121 幀 → 高品質子集微調。
- **自迴歸 WFM**：從零訓練的 Llama3 式 GPT（4B、12B），Video2World 版加入文字 cross-attention（5B、13B）；另用擴散解碼器把離散 token 轉回連續空間，減少失真。

### 評估指標與結果

**3D 一致性**（500 段靜態場景，生成影片能不能被當成真的 3D 場景重建）：

| 模型 | Sampson 誤差 ↓ | 相機位姿估計成功率 ↑ |
|---|---|---|
| VideoLDM（基線） | 0.841 | 4.4% |
| Cosmos 擴散 Text2World 7B | 0.355 | 62.6% |
| Cosmos 擴散 Video2World 7B | 0.473 | 68.4% |
| Cosmos 自迴歸 4B | 0.433 | 35.6% |
| 真實影片（參考） | 0.431 | 56.4% |

**物理對齊**：在 PhysX／Isaac Sim 裡建 8 種受控物理情境（掉落、碰撞等），比較生成影片與模擬器真值的 PSNR、SSIM、DreamSim、物體 IoU。給 9 幀條件時，擴散 Video2World 14B 的平均 IoU 最高（0.598），7B 從只給 1 幀的 0.332 升到 0.592。**條件幀越多越準，但模型變大不一定更符合物理。**

以上兩張表的數字取自 [NVIDIA 技術部落格](https://developer.nvidia.com/blog/advancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform)對論文表格的整理。

### 局限

- 仍有**物體恆存**問題（東西憑空出現或消失）、變形、違反重力等不合理行為。
- 論文自己說明：**沒有提供**把 Cosmos 用於策略評估、策略初始化、策略訓練、規劃或合成資料的實證結果，這些列為未來工作（後來由 DreamGen、Cosmos Policy 等論文補上）。

### 對 VLA 的意義

Cosmos 是目前「**世界模型當 VLA 資料工廠**」的主要基礎設施：DreamGen 用它微調後生成新任務的機器人影片訓練 GR00T，Cosmos-Transfer 負責把模擬畫面轉成真實感，Cosmos-Reason 負責過濾。細節見〈[具身基礎模型與合成資料](synthetic-data.html)〉。

## V-JEPA 2 {#v-jepa-2}

**Mido Assran 等，Meta FAIR，2025**｜[arXiv:2506.09985](https://arxiv.org/abs/2506.09985)｜[GitHub](https://github.com/facebookresearch/vjepa2)

!!! key "精髓"
    **不生成像素，只在表徵空間預測未來。先用 100 萬小時以上的網路影片學「世界怎麼動」，再用 62 小時沒有任何獎勵或成功標籤的機器人影片，學「我的動作會讓世界怎麼變」；結果在沒看過的實驗室裡零樣本完成抓放，每個動作的規劃時間是 Cosmos 的約 1/15。**

### 背景與問題

- 互動資料太少，難以單靠它學世界模型；影片生成式世界模型又太貴，而且把力氣花在像素細節上，不利於規劃。
- JEPA（聯合嵌入預測架構）的主張：只在學到的表徵空間預測，忽略本來就無法預測的像素細節。
- **要解決的問題**：結合網路規模的影片和少量機器人互動資料，做出能理解、預測並規劃的世界模型。

### 解法：兩階段

<figure class="dg">
<svg viewBox="0 0 800 280" role="img" aria-label="V-JEPA 2 預訓練與 V-JEPA 2-AC 規劃">
<rect class="n band" x="10" y="10" width="370" height="260" rx="14"/>
<text x="195" y="36" text-anchor="middle" class="h">階段一：無動作預訓練</text>
<rect class="n" x="30" y="60" width="150" height="50" rx="8"/>
<text x="105" y="82" text-anchor="middle" class="b">遮住部分的影片</text>
<text x="105" y="100" text-anchor="middle" class="s">2,200 萬段影片</text>
<rect class="n vla" x="210" y="60" width="150" height="50" rx="8"/>
<text x="285" y="82" text-anchor="middle" class="b vla">編碼器 ViT-g</text>
<text x="285" y="100" text-anchor="middle" class="s">1B 參數</text>
<rect class="n vla" x="210" y="140" width="150" height="50" rx="8"/>
<text x="285" y="162" text-anchor="middle" class="b vla">預測器</text>
<text x="285" y="180" text-anchor="middle" class="s">猜被遮住處的表徵</text>
<rect class="n" x="30" y="140" width="150" height="50" rx="8"/>
<text x="105" y="162" text-anchor="middle" class="b">EMA 目標編碼器</text>
<text x="105" y="180" text-anchor="middle" class="s">看完整影片給答案</text>
<path class="ar" d="M180,85 H208"/>
<path class="ar vla" d="M285,110 V138"/>
<path class="ar dash" d="M180,165 H208"/>
<text x="195" y="225" text-anchor="middle" class="s">損失：表徵之間的 L1，</text>
<text x="195" y="245" text-anchor="middle" class="s">不重建任何像素</text>
<rect class="n band" x="410" y="10" width="380" height="260" rx="14"/>
<text x="600" y="36" text-anchor="middle" class="h">階段二：V-JEPA 2-AC 與規劃</text>
<rect class="n" x="430" y="60" width="160" height="56" rx="8"/>
<text x="510" y="82" text-anchor="middle" class="b">凍結的編碼器</text>
<text x="510" y="102" text-anchor="middle" class="s">+ 末端狀態 + 動作</text>
<rect class="n wm" x="610" y="60" width="160" height="56" rx="8"/>
<text x="690" y="82" text-anchor="middle" class="b wm">動作條件預測器</text>
<text x="690" y="102" text-anchor="middle" class="s">300M，62 小時 DROID</text>
<rect class="n key" x="430" y="150" width="340" height="60" rx="10"/>
<text x="600" y="176" text-anchor="middle" class="b">CEM 搜尋動作序列</text>
<text x="600" y="196" text-anchor="middle" class="s">讓預測的表徵最接近「目標圖片」的表徵</text>
<path class="ar" d="M590,88 H608"/>
<path class="ar wm" d="M690,116 V148"/>
<text x="600" y="240" text-anchor="middle" class="s">只執行第一個動作，再重新規劃（MPC）</text>
</svg>
<figcaption>階段一學「世界怎麼動」，階段二只用少量無標註機器人影片學「動作造成什麼」。資料來源：<a href="https://arxiv.org/abs/2506.09985">arXiv:2506.09985</a>。</figcaption>
</figure>

**階段一：V-JEPA 2 預訓練**

- 目標：在表徵空間做「遮罩去噪」。編碼器看被遮住的影片，預測器猜被遮住部分的表徵，答案來自編碼器的 EMA 副本（防止表徵塌縮），損失是 L1。
- 四個擴展要素，各自帶來的提升（六項任務平均，從 V-JEPA 1 的 84.2 到 88.2）：
    1. **資料**：從 200 萬段擴到 2,200 萬段（VideoMix22M：HowTo100M、Kinetics、YT-Temporal-1B 篩選版、SSv2、ImageNet），+1.0；資料篩選另 +1.4。
    2. **模型**：ViT-L（300M）到 ViT-g（1B），+1.5。
    3. **訓練更久**：9 萬到 25.2 萬步，+0.8。
    4. **漸進解析度**：大部分時間用 16 幀 256×256，最後短暫拉到 64 幀 384×384，省下 8.4 倍 GPU 時間。

**階段二：V-JEPA 2-AC（動作條件世界模型）**

- 凍結編碼器，另訓練約 300M 參數的預測器（24 層、block-causal 注意力），輸入是每幀特徵、7 維末端狀態（位置、姿態、夾爪）與 7 維動作（末端位移）。
- **資料**：約 62 小時 DROID 影片，4 fps、256×256，**沒有任何獎勵或成功標籤**。
- 損失：teacher forcing 的 L1（15 步）加兩步自迴歸滾動的 L1，讓模型對自己的預測誤差更穩健。

**規劃**：給一張目標圖片，用交叉熵法（CEM）搜尋動作，讓預測出的表徵與目標表徵的 L1 距離最小；只執行第一步就重新規劃。

### 評估指標與結果

**理解**（凍結編碼器 + 注意力探針）：Something-Something v2 77.3%、Diving-48 90.2%。

**預測**：Epic-Kitchens-100 動作預判 recall@5 **39.7**，對比 8B 的 PlausiVL 27.6，相對提升約 44%。

**影片問答**（接 Llama 3.1 8B）：PerceptionTest 84.0、TempCompass 76.9，同級最佳。

**機器人零樣本操作**（兩個實驗室的 Franka 手臂，環境與物體都沒出現在訓練資料，各 10 次）：

| 方法 | 抓杯子 | 抓盒子 | 抓放杯子 | 抓放盒子 |
|---|---|---|---|---|
| Octo（VLA 基線） | 15% | 0% | 15% | 10% |
| **V-JEPA 2-AC** | **65%** | **25%** | **80%** | **65%** |

和 Cosmos 做同樣的規劃比較（實驗室 2）：Cosmos 抓杯子 0%、抓放都是 0%；V-JEPA 2-AC 是 60%、80%、50%。**規劃速度**：V-JEPA 2-AC 每個動作約 16 秒，Cosmos 約 4 分鐘。

### 局限

- **對相機位置敏感**：沒有相機校正，機械手臂底座常不在畫面中，相機位置要手動調。
- **長時程規劃難**：自迴歸誤差累積，搜尋空間隨步數指數成長；抓放任務需要人給中間子目標圖片。
- 目標只能用**圖片**指定，還不支援語言指令；模型只擴展到約 1B。

### 對 VLA 的意義

V-JEPA 2-AC 是「**推論時用世界模型挑動作**」（本站分級的 I3）最乾淨的例子，也證明非生成式世界模型在機器人規劃上可以比影片生成模型快一個數量級。它的弱點（需要目標圖片、不懂語言）正好是 VLA 的強項，所以兩者結合是很自然的下一步。

## 回頭看：8 篇共同留下的問題

| 問題 | 第一次被點出 | 後來怎麼處理 |
|---|---|---|
| 策略會鑽世界模型的漏洞 | World Models（溫度實驗） | 加隨機性、用真實資料拴住、最後以真機驗收（DreamGen、WMPO） |
| 要不要預測像素 | MuZero（完全不預測） vs GAIA-1（預測像素） | 依用途分工：要當模擬器就生成，要快速規劃就用表徵（V-JEPA 2） |
| 沒有動作標籤怎麼辦 | Genie（潛動作） | LAPA、UniVLA、GR00T N1 的潛動作預訓練 |
| 異質資料怎麼統一 | UniSim | Cosmos 的資料管線、GR00T 的資料金字塔 |
| 長時間一致性與記憶 | Genie（16 幀）、UniSim（4 幀） | Genie 3 做到數分鐘一致；仍是開放問題 |
| 物理正不正確 | Cosmos（物體恆存） | Physics-IQ 等基準、模擬器負責物理（見〈[合成資料](synthetic-data.html)〉） |
