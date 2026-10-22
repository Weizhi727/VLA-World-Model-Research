# 情境內模仿學習（In-Context Imitation Learning）

<p class="lede">回答五個問題：In-context imitation learning（簡稱 ICIL，情境內模仿學習）要解決什麼？用了哪些技術方法？代表論文的「資料 → 模型 → 輸出」長什麼樣？它跟 VLA 是什麼關係？現在誰在做？<b>每個數字都附原始論文或官方頁連結；論文沒寫的標「未寫」，查不到的標「未公開」。</b>整理日期 2026-10-22。</p>

## 重點先講

!!! key "七句話看懂 In-Context 模仿學習"
    1. **一句話定義**：把幾條「示範」直接放進模型的輸入（context），模型看完就照著做新任務，**權重完全不更新**。這就是大型語言模型「few-shot 提示」的機器人版：提示詞從文字換成示範（[Instant Policy](https://arxiv.org/abs/2411.12633)、[ICRT](https://arxiv.org/abs/2408.15980)）。
    2. **要解決的問題**：現在的 VLA 學新任務，通常要再收幾十到幾千條示範、重新微調。ICIL 想把這一步變成「示範 1～20 次，馬上會做」，而且示範比語言更能說清楚「怎麼做」。
    3. **技術上分四條路**：A 用元學習專門訓練一個「會看示範」的策略（[ICRT](https://arxiv.org/abs/2408.15980)、[Instant Policy](https://arxiv.org/abs/2411.12633)）；B 把畫面與動作寫成文字，直接借 GPT-4 的 few-shot 能力（[KAT](https://arxiv.org/abs/2403.19578)、[RoboPrompt](https://arxiv.org/abs/2410.12782)）；C 從示範庫檢索最相近的片段塞進現成 VLA（[RICL](https://arxiv.org/abs/2508.02062)、[ICI-VLA](https://arxiv.org/abs/2609.07581)）；D 靠大規模預訓練讓能力自己長出來（[Generalist GEN-1.5](https://generalistai.com/blog/gen-1.5)、[Skild S1](https://www.skild.ai/blogs/s1)）。
    4. **和 VLA 的關係**：一般 VLA 用「語言」指定任務；ICIL 改用「示範」指定任務，或兩者並用。2025 年起開始有人把它**直接裝到 VLA 上**：RICL 讓 π0-FAST 在不更新權重的情況下，完整任務成功率從 2.5% 提到 31.25%。
    5. **2026 年進入產品**：Skild AI 的 S1（2026-08）宣稱是「從頭設計成情境內學習者」，看一段人類影片就能做長達約 10 分鐘的任務；Generalist 的 GEN-1.5（2026-08）宣稱 3～12 秒的示範就能做新任務。兩者都只有官方部落格，**沒有論文、參數量未公開**。
    6. **context 也可以拿來「認識系統」**：[ICWM](https://arxiv.org/abs/2606.26025)（2026-06）不放示範，而是讓機器人先隨機試動幾下，把「動作→畫面變化」放進 context，VLA 就能推出相機換了角度，不微調就適應新視角（LIBERO-Long 新視角 25.0% vs 多視角基線 19.8%）。
    7. **還沒解決的**：學不到訓練時沒見過的「動作原語」（[ICRT](https://arxiv.org/abs/2408.15980)、[BPP](https://arxiv.org/abs/2606.30457) 都承認）；示範越多不一定越好（[KAT](https://arxiv.org/abs/2403.19578)、[MimicDroid](https://arxiv.org/abs/2509.09769)）；目前情境內學出來的技能仍比微調脆弱（[GEN-1.5](https://generalistai.com/blog/gen-1.5)）。

## 一張圖看懂：微調 vs 情境內模仿

<figure class="dg">
<svg viewBox="0 0 800 226" role="img" aria-label="一般 VLA 學新任務的兩條路：微調 vs 情境內模仿">
<text x="125" y="24" text-anchor="middle" class="h">新任務來了</text>
<rect class="n" x="10" y="40" width="231" height="88" rx="12"/>
<text x="125" y="64" text-anchor="middle" class="b">語言指令</text>
<text x="125" y="84" text-anchor="middle" class="s">「把杯子放進抽屜」</text>
<text x="125" y="102" text-anchor="middle" class="s">說得出做什麼</text>
<text x="125" y="120" text-anchor="middle" class="s">說不清怎麼做</text>
<rect class="n" x="10" y="144" width="231" height="70" rx="12"/>
<text x="125" y="168" text-anchor="middle" class="b">幾條示範</text>
<text x="125" y="188" text-anchor="middle" class="s">人或遙操作做 1～20 次</text>
<text x="125" y="206" text-anchor="middle" class="s">影片、軌跡或點雲</text>
<text x="400" y="24" text-anchor="middle" class="h">怎麼讓模型學會</text>
<rect class="n ghost" x="285" y="49" width="231" height="70" rx="12"/>
<text x="400" y="73" text-anchor="middle" class="b">路線一：微調</text>
<text x="400" y="93" text-anchor="middle" class="s">再收幾十到幾千條示範</text>
<text x="400" y="111" text-anchor="middle" class="s">跑梯度更新、存新權重</text>
<rect class="n vla" x="285" y="135" width="231" height="70" rx="12"/>
<text x="400" y="159" text-anchor="middle" class="b vla">路線二：情境內模仿</text>
<text x="400" y="179" text-anchor="middle" class="s">示範直接放進輸入</text>
<text x="400" y="197" text-anchor="middle" class="s">權重完全不動</text>
<text x="675" y="24" text-anchor="middle" class="h">機器人做出來</text>
<rect class="n key" x="559" y="92" width="231" height="70" rx="12"/>
<text x="675" y="116" text-anchor="middle" class="b">動作序列</text>
<text x="675" y="136" text-anchor="middle" class="s">當下畫面＋本體狀態</text>
<text x="675" y="154" text-anchor="middle" class="s">→ 未來幾步動作</text>
<path class="ar dash" d="M241,84 C262,84 262,84 283,84"/>
<path class="ar dash" d="M241,179 C262,179 262,84 283,84"/>
<path class="ar vla" d="M241,179 C262,179 262,170 283,170"/>
<path class="ar dash" d="M515,84 C536,84 536,127 557,127"/>
<path class="ar vla" d="M515,170 C536,170 536,127 557,127"/>
</svg>
<figcaption>情境內模仿學習（ICIL）把「示範」當成提示詞（prompt），推論時讀進模型，不做梯度更新。對比：微調要額外收資料並重新訓練。示範數量取自 <a href="https://arxiv.org/abs/2508.02062">RICL</a>（10～20 條）與 <a href="https://arxiv.org/abs/2411.12633">Instant Policy</a>（1～2 條）。</figcaption>
</figure>

## 三篇重點論文速覽

| | [ICLR 視覺推理](#iclr-visual-reasoning) | [ICWM](#icwm) | [Instant Policy](#instant-policy) |
|---|---|---|---|
| 一句話 | 示範裡加「意圖軌跡」，模型先畫軌跡再出動作 | context 放機器人自己試動的紀錄，推出相機與身體設定 | 示範、當下、動作全畫成圖，用圖擴散出動作 |
| context 裡放什麼 | 3 條示範＋每步的 5 點夾爪軌跡 | 5 段（起始畫面、動作、結束畫面） | 1～2 條示範，每條 10 個路徑點的點雲圖 |
| 要適應的是 | 新**任務**（看懂意圖） | 新**系統設定**（新視角、新身體） | 新**任務**（幾何關係） |
| 訓練資料 | LIBERO＋真機 825 條遙操作 | LIBERO-Long 多視角＋真機 12 相機 | 全部是模擬生成的偽示範（約 70 萬條） |
| 輸出 | 推理軌跡 → 16 步動作 | 連續動作 | 未來 8 步 SE(3)＋夾爪 |
| 代表成績 | 真機抓放 60.0%（ICRT 22.5%） | 新視角 25.0%（多視角基線 19.8%） | 真機 16 任務 88.75%（Vid2Robot 40.63%） |
| 屬於哪條路線 | A＋中間表徵 | 延伸：情境內系統辨識 | A |

## 一、它要解決什麼問題

| 痛點 | 具體情況 | 出處 |
|---|---|---|
| **新任務要大量示範** | 一般模仿學習每個任務要幾百到幾千條示範 | [Instant Policy](https://arxiv.org/abs/2411.12633) |
| **微調又慢又貴** | Skild 自己估：一條情境內示範約等於 380 條後訓練示範，而收 380 條長任務示範要 50～100 小時遙操作；後訓練 VLA 用 2,000 條示範才到 86% | [Skild S1](https://www.skild.ai/blogs/s1) |
| **語言說不清「怎麼做」** | 「示範能明確說明任務要怎麼做」；同一個場景可以做好幾種任務，語言或目標圖都可能有歧義 | [Skild S1](https://www.skild.ai/blogs/s1)、[ICRT](https://arxiv.org/abs/2408.15980)、[ICLR 視覺推理](https://arxiv.org/abs/2603.07530) |
| **現場的人不會訓練模型** | 讓終端使用者只要提供 10～20 條示範，不必調參數 | [RICL](https://arxiv.org/abs/2508.02062) |
| **VLA 天生不會情境內學習** | 用模仿學習預訓練的 VLA，不像語言模型那樣會從提示學新任務，要專門的配方才補得上 | [RICL](https://arxiv.org/abs/2508.02062) |

!!! note "跟幾個相近名詞的差別"
    - **One-shot / Few-shot 模仿學習**：只看示範數量。ICIL 是其中「**不做梯度更新**」的那一種；用少量示範微調也叫 few-shot，但不算情境內學習。
    - **元學習（meta-learning）**：ICIL 最常見的訓練方式。[One-Shot Imitation Learning（2017）](https://arxiv.org/abs/1703.07326) 就是用「拿一條示範、預測另一條示範的動作」來訓練。
    - **多模態提示**：[VIMA](https://arxiv.org/abs/2210.03094) 把「模仿一段示範」當成多種提示中的一種，是 ICIL 的近親。
    - **檢索增強（RAG）**：從示範庫找最像的片段放進 context，是 ICIL 的一種實作方式（[REGENT](https://arxiv.org/abs/2412.04759)、[RICL](https://arxiv.org/abs/2508.02062)）。

## 二、技術方法：四條路線

<figure class="dg">
<svg viewBox="0 0 800 380" role="img" aria-label="四條技術路線怎麼取得「看示範就會做」的能力">
<text x="194" y="24" text-anchor="middle" class="h">能力從哪來</text>
<rect class="n vla" x="10" y="40" width="368" height="70" rx="12"/>
<text x="194" y="64" text-anchor="middle" class="b vla">A 元學習專用策略</text>
<text x="194" y="84" text-anchor="middle" class="s">Vid2Robot、ICRT、</text>
<text x="194" y="102" text-anchor="middle" class="s">Instant Policy、BPP</text>
<rect class="n" x="10" y="126" width="368" height="70" rx="12"/>
<text x="194" y="150" text-anchor="middle" class="b">B 借用 LLM</text>
<text x="194" y="170" text-anchor="middle" class="s">KAT、RoboPrompt</text>
<text x="194" y="188" text-anchor="middle" class="s">動作寫成文字</text>
<rect class="n mix" x="10" y="212" width="368" height="70" rx="12"/>
<text x="194" y="236" text-anchor="middle" class="b">C 檢索增強</text>
<text x="194" y="256" text-anchor="middle" class="s">REGENT、RICL、</text>
<text x="194" y="274" text-anchor="middle" class="s">ICI-VLA</text>
<rect class="n key" x="10" y="298" width="368" height="70" rx="12"/>
<text x="194" y="322" text-anchor="middle" class="b">D 規模湧現</text>
<text x="194" y="342" text-anchor="middle" class="s">Skild S1、</text>
<text x="194" y="360" text-anchor="middle" class="s">Generalist GEN-1.5</text>
<text x="606" y="24" text-anchor="middle" class="h">要付出什麼</text>
<rect class="n" x="422" y="76" width="368" height="52" rx="12"/>
<text x="606" y="100" text-anchor="middle" class="b">自己訓一個策略</text>
<text x="606" y="120" text-anchor="middle" class="s">資料要按任務分組</text>
<rect class="n" x="422" y="144" width="368" height="52" rx="12"/>
<text x="606" y="168" text-anchor="middle" class="b">不用訓練</text>
<text x="606" y="188" text-anchor="middle" class="s">慢、只能出關鍵幀</text>
<rect class="n" x="422" y="212" width="368" height="52" rx="12"/>
<text x="606" y="236" text-anchor="middle" class="b">在現成 VLA 上後訓練</text>
<text x="606" y="256" text-anchor="middle" class="s">要建示範檢索庫</text>
<rect class="n" x="422" y="280" width="368" height="52" rx="12"/>
<text x="606" y="304" text-anchor="middle" class="b">大規模預訓練</text>
<text x="606" y="324" text-anchor="middle" class="s">細節多半未公開</text>
<path class="ar" d="M378,75 C399,75 399,102 420,102"/>
<path class="ar" d="M378,161 C399,161 399,170 420,170"/>
<path class="ar" d="M378,247 C399,247 399,238 420,238"/>
<path class="ar" d="M378,333 C399,333 399,306 420,306"/>
</svg>
<figcaption>分類是本站依各論文的訓練方式整理，不是某篇綜述的官方分法。</figcaption>
</figure>

| 路線 | 核心想法 | 代表 | 示範長什麼樣 | 優點 | 代價 |
|---|---|---|---|---|---|
| **A 元學習專用策略** | 訓練時把同一任務的多條示範接成一條序列，前面當提示、最後一條當題目 | [One-Shot IL](https://arxiv.org/abs/1703.07326)、[Vid2Robot](https://arxiv.org/abs/2403.12943)、[ICRT](https://arxiv.org/abs/2408.15980)、[Instant Policy](https://arxiv.org/abs/2411.12633)、[MimicDroid](https://arxiv.org/abs/2509.09769)、[BPP](https://arxiv.org/abs/2606.30457) | 影像＋本體＋動作序列、點雲圖、人類影片 | 可以閉環、頻率高（ICRT 39.6 Hz） | 要自己收「按任務分組」的資料 |
| **B 借用 LLM** | 把觀測（關鍵點或物體位姿）與動作寫成數字文字，讓現成 LLM 續寫 | [KAT](https://arxiv.org/abs/2403.19578)、[RoboPrompt](https://arxiv.org/abs/2410.12782) | 文字化的關鍵點、位姿、關鍵幀動作 | 完全不用訓練 | 每次推論要好幾秒，只能出關鍵幀，做不了高頻控制 |
| **C 檢索增強** | 從使用者的示範庫找最相近的片段放進 context，再跟模型輸出插值 | [REGENT](https://arxiv.org/abs/2412.04759)、[RICL](https://arxiv.org/abs/2508.02062)、[ICI-VLA](https://arxiv.org/abs/2609.07581) | 檢索出的短片段（影像、本體、動作 chunk） | 能裝在現成 VLA 上 | 要先做一次後訓練；context 變長、推論變慢 |
| **D 規模湧現** | 大規模連續預訓練，示範（physical prompt）當提示 | [GEN-1.5](https://generalistai.com/blog/gen-1.5)、[Skild S1](https://www.skild.ai/blogs/s1) | 手持夾爪示範、機器人軌跡、人類第一人稱影片 | 可做長任務、跨形體 | 只有官方部落格，無法重現 |
| **延伸：情境內系統辨識** | context 放的不是示範，而是機器人自己試動的紀錄，用來推出相機視角、身體等系統設定 | [ICWM](https://arxiv.org/abs/2606.26025) | （起始畫面、動作、結束畫面）轉移 | 不用示範、不用獎勵就能適應新視角 | 絕對成功率仍低，部署前要先試探 |

### 幾個反覆出現的技術要點

**怎麼訓練：同任務多條示範拼成一條序列**（路線 A 的共同套路）：

<figure class="dg">
<svg viewBox="0 0 800 208" role="img" aria-label="元學習式訓練：同一任務的多條示範拼成一條序列">
<text x="125" y="24" text-anchor="middle" class="h">訓練資料怎麼組</text>
<rect class="n" x="10" y="83" width="231" height="70" rx="12"/>
<text x="125" y="107" text-anchor="middle" class="b">同一任務的示範池</text>
<text x="125" y="127" text-anchor="middle" class="s">示範 1、2、3……</text>
<text x="125" y="145" text-anchor="middle" class="s">場景或物體位置不同</text>
<text x="400" y="24" text-anchor="middle" class="h">一條訓練序列</text>
<rect class="n vla" x="285" y="40" width="231" height="70" rx="12"/>
<text x="400" y="64" text-anchor="middle" class="b vla">前 k 條：當提示</text>
<text x="400" y="84" text-anchor="middle" class="s">影像、本體狀態、動作</text>
<text x="400" y="102" text-anchor="middle" class="s">不算 loss（多數做法）</text>
<rect class="n key" x="285" y="126" width="231" height="70" rx="12"/>
<text x="400" y="150" text-anchor="middle" class="b">最後 1 條：當題目</text>
<text x="400" y="170" text-anchor="middle" class="s">只在這段算動作 loss</text>
<text x="400" y="188" text-anchor="middle" class="s">學會「照著前面做」</text>
<text x="675" y="24" text-anchor="middle" class="h">測試時</text>
<rect class="n vla" x="559" y="83" width="231" height="70" rx="12"/>
<text x="675" y="107" text-anchor="middle" class="b vla">換成新任務的示範</text>
<text x="675" y="127" text-anchor="middle" class="s">不更新權重</text>
<text x="675" y="145" text-anchor="middle" class="s">直接輸出新任務動作</text>
<path class="ar" d="M241,118 C262,118 262,75 283,75"/>
<path class="ar" d="M241,118 C262,118 262,161 283,161"/>
<path class="ar vla" d="M515,75 C536,75 536,118 557,118"/>
<path class="ar vla" d="M515,161 C536,161 536,118 557,118"/>
</svg>
<figcaption>這是 <a href="https://arxiv.org/abs/1703.07326">One-Shot Imitation Learning</a>（2017）以來的共同訓練套路；<a href="https://arxiv.org/abs/2408.15980">ICRT</a> 實驗顯示 loss 也算在提示段反而變差（平均成功率 79.2% → 22.5%）。</figcaption>
</figure>

1. **只在「題目」那段算 loss**：ICRT 實驗發現 loss 也算在提示段會讓平均成功率從 79.2% 掉到 22.5%（[ICRT](https://arxiv.org/abs/2408.15980)）；RICL 也只對 query 的動作算 loss（[RICL](https://arxiv.org/abs/2508.02062)）。
2. **防止直接抄答案**：檢索到的示範和當下太像時，模型容易直接複製動作。ICI-VLA 用「Target Action Masking」故意破壞 context，逼模型看當下觀測（[ICI-VLA](https://arxiv.org/abs/2609.07581)）。
3. **示範怎麼表示決定上限**：影像 token（ICRT、Vid2Robot）、點雲圖（Instant Policy）、DINO 關鍵點文字（KAT）、物體位姿文字（RoboPrompt）、視覺推理軌跡（[ICLR 視覺推理](https://arxiv.org/abs/2603.07530)）。表示越接近「幾何」，越少示範就夠，但越吃感知前處理（分割、位姿估計）。
4. **跨形體：拿人類影片當示範**：Vid2Robot、MimicDroid、BPP、Skild S1、GEN-1.5 都讓人類示範（影片或手持夾爪）當提示；MimicDroid 用手部姿態估計＋重定向＋隨機遮擋來縮小人與機器人的差距。

## 三、代表論文逐篇拆解

依時間排。每篇都畫「資料 → 模型 → 輸出」；圖中虛線是訓練資料，實線是推論時的資料流。

### 3.1 One-Shot Imitation Learning（2017）：起點

- **論文**：[arXiv:1703.07326](https://arxiv.org/abs/1703.07326)，Yan Duan、Pieter Abbeel、Ilya Sutskever、Wojciech Zaremba 等（OpenAI／UC Berkeley）。
- **想法**：訓練時拿同一任務的「一對示範」，網路讀第一條示範＋當下狀態，預測第二條示範的動作；測試時給一條新任務的示範就能做。用 soft attention 幫助泛化。
- **地位**：後面所有路線 A 的論文都沿用這個訓練套路，只是把網路換成 Transformer、把資料換成真實機器人。

### 3.2 Vid2Robot（2024）：看人類影片做動作

<figure class="dg">
<svg viewBox="0 0 800 258" role="img" aria-label="Vid2Robot：影片提示 → 交叉注意力 → 動作">
<text x="125" y="24" text-anchor="middle" class="h">資料</text>
<rect class="n" x="10" y="40" width="231" height="52" rx="12"/>
<text x="125" y="64" text-anchor="middle" class="b">提示影片 16 幀</text>
<text x="125" y="84" text-anchor="middle" class="s">人或機器人做一次任務</text>
<rect class="n" x="10" y="108" width="231" height="52" rx="12"/>
<text x="125" y="132" text-anchor="middle" class="b">機器人當下 8 幀</text>
<text x="125" y="152" text-anchor="middle" class="s">目前與前幾幀畫面</text>
<rect class="n" x="10" y="176" width="231" height="70" rx="12"/>
<text x="125" y="200" text-anchor="middle" class="b">訓練配對</text>
<text x="125" y="220" text-anchor="middle" class="s">約 10 萬機器人影片</text>
<text x="125" y="238" text-anchor="middle" class="s">約 1 萬人類影片</text>
<text x="400" y="24" text-anchor="middle" class="h">模型</text>
<rect class="n vla" x="285" y="40" width="231" height="52" rx="12"/>
<text x="400" y="64" text-anchor="middle" class="b vla">ViT-B/16 共用編碼</text>
<text x="400" y="84" text-anchor="middle" class="s">Perceiver 壓成 64 token</text>
<rect class="n vla" x="285" y="108" width="231" height="52" rx="12"/>
<text x="400" y="132" text-anchor="middle" class="b vla">交叉注意力 4 層</text>
<text x="400" y="152" text-anchor="middle" class="s">當下狀態 query 提示影片</text>
<rect class="n" x="285" y="176" width="231" height="70" rx="12"/>
<text x="400" y="200" text-anchor="middle" class="b">輔助 loss</text>
<text x="400" y="220" text-anchor="middle" class="s">影片對齊 TCC</text>
<text x="400" y="238" text-anchor="middle" class="s">影片–文字對比</text>
<text x="675" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n key" x="559" y="108" width="231" height="70" rx="12"/>
<text x="675" y="132" text-anchor="middle" class="b">11 維動作</text>
<text x="675" y="152" text-anchor="middle" class="s">每維 256 格離散</text>
<text x="675" y="170" text-anchor="middle" class="s">一次預測 4 步</text>
<path class="ar" d="M241,66 C262,66 262,66 283,66"/>
<path class="ar" d="M241,134 C262,134 262,66 283,66"/>
<path class="ar dash" d="M241,211 C262,211 262,211 283,211"/>
<path class="ar vla" d="M400,92 V106"/>
<path class="ar vla" d="M515,134 C536,134 536,143 557,143"/>
<path class="ar dash" d="M400,176 V162"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2403.12943">Vid2Robot（arXiv:2403.12943）</a>，Google DeepMind、CMU、多倫多大學，RSS 2024。</figcaption>
</figure>

- **資料**：正文寫約 10 萬條機器人影片、1 萬條人類影片（附錄另列 12 萬機器人、5 千人類、5 千人機同場軌跡，論文前後數字不一致）。
- **模型**：共用 ViT-B/16 → Perceiver Resampler 壓縮 → 4 層交叉注意力（當下 query 提示影片）→ 4 層動作解碼器。另加三個輔助 loss：影片時間對齊、提示–機器人影片對比、影片–文字對比；拿掉後成功率 61% → 45%。
- **成績**：人類影片當提示時 52.8%，對照 BC-Z 30.6%；機器人影片當提示時 54.9% vs 52.6%（[論文](https://arxiv.org/abs/2403.12943)）。
- **參數量**：論文未寫總數。

### 3.3 ICRT（2024）：用「下一個 token 預測」做情境內模仿

<figure class="dg">
<svg viewBox="0 0 800 294" role="img" aria-label="ICRT：示範與當下觀測接成一條 token 序列，下一個 token 預測動作">
<text x="125" y="24" text-anchor="middle" class="h">資料</text>
<rect class="n" x="10" y="40" width="231" height="70" rx="12"/>
<text x="125" y="64" text-anchor="middle" class="b">預訓練：DROID 子集</text>
<text x="125" y="84" text-anchor="middle" class="s">依長度與指令相似度</text>
<text x="125" y="102" text-anchor="middle" class="s">篩選、同任務分組</text>
<rect class="n" x="10" y="126" width="231" height="70" rx="12"/>
<text x="125" y="150" text-anchor="middle" class="b">微調：ICRT-MT</text>
<text x="125" y="170" text-anchor="middle" class="s">1,098 條、29 任務</text>
<text x="125" y="188" text-anchor="middle" class="s">6 種動作原語</text>
<rect class="n" x="10" y="212" width="231" height="70" rx="12"/>
<text x="125" y="236" text-anchor="middle" class="b">測試時提示</text>
<text x="125" y="256" text-anchor="middle" class="s">新任務的遙操作示範</text>
<text x="125" y="274" text-anchor="middle" class="s">＋當下影像與本體</text>
<text x="400" y="24" text-anchor="middle" class="h">模型</text>
<rect class="n" x="285" y="83" width="231" height="70" rx="12"/>
<text x="400" y="107" text-anchor="middle" class="b">ViT-Base（凍結）</text>
<text x="400" y="127" text-anchor="middle" class="s">CrossMAE 預訓練</text>
<text x="400" y="145" text-anchor="middle" class="s">影像＋本體 → 狀態 token</text>
<rect class="n vla" x="285" y="169" width="231" height="70" rx="12"/>
<text x="400" y="193" text-anchor="middle" class="b vla">Llama2 式因果 Transformer</text>
<text x="400" y="213" text-anchor="middle" class="s">12 層、768 維，從頭訓</text>
<text x="400" y="231" text-anchor="middle" class="s">另有 Llama2-7B LoRA 版</text>
<text x="675" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n key" x="559" y="83" width="231" height="70" rx="12"/>
<text x="675" y="107" text-anchor="middle" class="b">16 步動作 chunk</text>
<text x="675" y="127" text-anchor="middle" class="s">末端位姿增量＋夾爪</text>
<text x="675" y="145" text-anchor="middle" class="s">時間集成執行</text>
<rect class="n" x="559" y="169" width="231" height="70" rx="12"/>
<text x="675" y="193" text-anchor="middle" class="b">速度</text>
<text x="675" y="213" text-anchor="middle" class="s">ICRT 39.6 Hz</text>
<text x="675" y="231" text-anchor="middle" class="s">7B 版 10.7 Hz</text>
<path class="ar dash" d="M241,75 C262,75 262,204 283,204"/>
<path class="ar dash" d="M241,161 C262,161 262,204 283,204"/>
<path class="ar" d="M241,247 C262,247 262,118 283,118"/>
<path class="ar vla" d="M400,153 V167"/>
<path class="ar vla" d="M515,204 C536,204 536,118 557,118"/>
<path class="ar dash" d="M515,204 C536,204 536,204 557,204"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2408.15980">ICRT（arXiv:2408.15980）</a>，UC Berkeley（Ken Goldberg 組）與 Autodesk Research。虛線是訓練資料，實線是推論時的資料流。</figcaption>
</figure>

- **提示格式**：每條軌跡是（影像、本體狀態、動作）的序列；狀態是 10 維絕對末端位姿，動作是末端位姿增量＋夾爪。訓練序列長 512 步，裡面放好幾條同任務軌跡，前 k 條當提示。
- **為什麼要 ICRT-MT 資料集**：同一個場景可以做好幾種任務，逼模型**一定要看提示**才知道要做哪個。
- **成績**（真實 Franka，每類 30 次）：

| 模型 | 抓取放置 | 戳（poke） | 平均 |
|---|---|---|---|
| **ICRT** | **65.0** | **93.3** | **79.2** |
| 目標條件策略 | 33.3 | 6.7 | 20.0 |
| OpenVLA | 11.7 | 3.3 | 7.5 |
| Octo | 5.0 | 13.3 | 9.2 |

- **消融重點**：只用 DROID 預訓練、不用 ICRT-MT → 0.0；一階段混訓 → 6.7；換 Llama2-7B → 58.3（推論太慢，10.7 Hz）。
- **局限**：完全沒見過的動作原語能否學會不明；固定一種機械臂；同色不同形的干擾物容易抓錯（[論文](https://arxiv.org/abs/2408.15980)、[程式碼](https://github.com/max-fu/icrt)）。

### 3.4 KAT（2024）：不訓練，直接讓 GPT-4 模仿

<figure class="dg">
<svg viewBox="0 0 800 208" role="img" aria-label="KAT：把畫面與動作都寫成數字文字，讓 GPT-4 Turbo 照樣接下去">
<text x="91" y="24" text-anchor="middle" class="h">資料</text>
<rect class="n" x="10" y="49" width="162" height="70" rx="12"/>
<text x="91" y="73" text-anchor="middle" class="b">10 條示範</text>
<text x="91" y="93" text-anchor="middle" class="s">俯視 RGB-D 影像</text>
<text x="91" y="111" text-anchor="middle" class="s">末端位姿軌跡（4 Hz）</text>
<rect class="n" x="10" y="135" width="162" height="52" rx="12"/>
<text x="91" y="159" text-anchor="middle" class="b">新場景</text>
<text x="91" y="179" text-anchor="middle" class="s">一張俯視 RGB-D</text>
<text x="297" y="24" text-anchor="middle" class="h">轉成 token</text>
<rect class="n" x="216" y="40" width="162" height="70" rx="12"/>
<text x="297" y="64" text-anchor="middle" class="b">DINO-ViT 關鍵點</text>
<text x="297" y="84" text-anchor="middle" class="s">挑 10 個對應點</text>
<text x="297" y="102" text-anchor="middle" class="s">升成 3D 座標文字</text>
<rect class="n" x="216" y="126" width="162" height="70" rx="12"/>
<text x="297" y="150" text-anchor="middle" class="b">動作 token</text>
<text x="297" y="170" text-anchor="middle" class="s">每個位姿 = 3 個 3D 點</text>
<text x="297" y="188" text-anchor="middle" class="s">＋夾爪開合，每條 20 個</text>
<text x="503" y="24" text-anchor="middle" class="h">LLM</text>
<rect class="n vla" x="422" y="83" width="162" height="70" rx="12"/>
<text x="503" y="107" text-anchor="middle" class="b vla">GPT-4 Turbo</text>
<text x="503" y="127" text-anchor="middle" class="s">不微調</text>
<text x="503" y="145" text-anchor="middle" class="s">讀示範 → 續寫動作</text>
<text x="709" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n key" x="628" y="83" width="162" height="70" rx="12"/>
<text x="709" y="107" text-anchor="middle" class="b">動作 token</text>
<text x="709" y="127" text-anchor="middle" class="s">轉回末端位姿</text>
<text x="709" y="145" text-anchor="middle" class="s">機器人照軌跡執行</text>
<path class="ar" d="M172,84 C193,84 193,75 214,75"/>
<path class="ar" d="M172,84 C193,84 193,161 214,161"/>
<path class="ar" d="M172,161 C193,161 193,75 214,75"/>
<path class="ar vla" d="M378,75 C399,75 399,118 420,118"/>
<path class="ar vla" d="M378,161 C399,161 399,118 420,118"/>
<path class="ar vla" d="M584,118 C605,118 605,118 626,118"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2403.19578">Keypoint Action Tokens（arXiv:2403.19578）</a>，Imperial College London，RSS 2024。</figcaption>
</figure>

- **關鍵想法**：純文字訓練的 Transformer 也學過「看幾個例子、照規律接下去」，只要把畫面與動作都寫成數字序列就能用。
- **成績**（Sawyer，9 個任務，各 10 條示範）：KAT 0.68；原版影像 Diffusion Policy 0.10；用同樣關鍵點表示的 Diffusion Policy（KeyAct-DP）0.59。KAT 不用訓練，對照組每個任務約要訓練 10 分鐘。
- **局限**：示範加到 40 條時，KeyAct-DP 在部分任務反超，代表 LLM 的情境內學習**不會隨示範變多而一直變好**；每回合只看開頭一張觀測（[論文](https://arxiv.org/abs/2403.19578)）。

### 3.5 RoboPrompt（2024）：關鍵幀＋物體位姿的文字提示

<figure class="dg">
<svg viewBox="0 0 800 208" role="img" aria-label="RoboPrompt：關鍵幀 + 物體位姿寫成文字提示">
<text x="91" y="24" text-anchor="middle" class="h">資料</text>
<rect class="n" x="10" y="40" width="162" height="70" rx="12"/>
<text x="91" y="64" text-anchor="middle" class="b">10 條示範</text>
<text x="91" y="84" text-anchor="middle" class="s">每條 200 多幀</text>
<text x="91" y="102" text-anchor="middle" class="s">挑成 5～15 個關鍵幀</text>
<rect class="n" x="10" y="126" width="162" height="70" rx="12"/>
<text x="91" y="150" text-anchor="middle" class="b">新場景第一幀</text>
<text x="91" y="170" text-anchor="middle" class="s">FoundationPose＋</text>
<text x="91" y="188" text-anchor="middle" class="s">GroundingDINO 估位姿</text>
<text x="297" y="24" text-anchor="middle" class="h">文字提示</text>
<rect class="n" x="216" y="83" width="162" height="70" rx="12"/>
<text x="297" y="107" text-anchor="middle" class="b">每條示範寫成一行</text>
<text x="297" y="127" text-anchor="middle" class="s">物體名＋離散化位姿</text>
<text x="297" y="145" text-anchor="middle" class="s">＋指令 → 關鍵幀動作</text>
<text x="503" y="24" text-anchor="middle" class="h">LLM</text>
<rect class="n vla" x="422" y="83" width="162" height="70" rx="12"/>
<text x="503" y="107" text-anchor="middle" class="b vla">GPT-4 Turbo（預設）</text>
<text x="503" y="127" text-anchor="middle" class="s">也試過 GPT-4o、</text>
<text x="503" y="145" text-anchor="middle" class="s">Qwen2-7B、Llama3-8B</text>
<text x="709" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n key" x="628" y="83" width="162" height="70" rx="12"/>
<text x="709" y="107" text-anchor="middle" class="b">關鍵幀末端位姿</text>
<text x="709" y="127" text-anchor="middle" class="s">平移 100 格、旋轉 5°</text>
<text x="709" y="145" text-anchor="middle" class="s">＋夾爪開合</text>
<path class="ar" d="M172,75 C193,75 193,118 214,118"/>
<path class="ar" d="M172,161 C193,161 193,118 214,118"/>
<path class="ar vla" d="M378,118 C399,118 399,118 420,118"/>
<path class="ar vla" d="M584,118 C605,118 605,118 626,118"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2410.12782">RoboPrompt（arXiv:2410.12782）</a>，UC Berkeley（Trevor Darrell、Roei Herzig）。</figcaption>
</figure>

- **成績**：RLBench 16 個任務平均 51.8%，同為免訓練的 KAT、VoxPoser 都是 21.0%；但仍低於監督式訓練的 RVT-2（81.4%）。真機 6 個任務分別 90／80／90／50／50／80%（平均約 73%）。
- **換 LLM**：GPT-4o 56.3%、GPT-4 Turbo 51.8%、Qwen2-7B 48.8%、GPT-4o mini 44.8%、Llama3-8B 28.3%。
- **局限**：LLM 每幾秒才出一次動作，做不到 10 Hz 以上的控制；每個物體只用一個位姿，沒有形狀資訊（[論文](https://arxiv.org/abs/2410.12782)）。

### 3.6 Instant Policy（2024，ICLR 2025 oral）：用模擬「偽示範」無限量訓練 {#instant-policy}

<figure class="dg">
<svg viewBox="0 0 800 208" role="img" aria-label="Instant Policy：示範與當下都畫成圖，用圖擴散生成動作">
<text x="91" y="24" text-anchor="middle" class="h">資料</text>
<rect class="n" x="10" y="49" width="162" height="70" rx="12"/>
<text x="91" y="73" text-anchor="middle" class="b">測試：1～2 條示範</text>
<text x="91" y="93" text-anchor="middle" class="s">每條取 10 個路徑點</text>
<text x="91" y="111" text-anchor="middle" class="s">分割後的點雲</text>
<rect class="n" x="10" y="135" width="162" height="52" rx="12"/>
<text x="91" y="159" text-anchor="middle" class="b">當下觀測</text>
<text x="91" y="179" text-anchor="middle" class="s">分割點雲＋夾爪位姿</text>
<text x="297" y="24" text-anchor="middle" class="h">建圖</text>
<rect class="n" x="216" y="40" width="162" height="70" rx="12"/>
<text x="297" y="64" text-anchor="middle" class="b">局部圖</text>
<text x="297" y="84" text-anchor="middle" class="s">點雲 → 約 16 個節點</text>
<text x="297" y="102" text-anchor="middle" class="s">夾爪 → 6 個關鍵點節點</text>
<rect class="n" x="216" y="126" width="162" height="70" rx="12"/>
<text x="297" y="150" text-anchor="middle" class="b">情境圖</text>
<text x="297" y="170" text-anchor="middle" class="s">示範沿時間串起</text>
<text x="297" y="188" text-anchor="middle" class="s">再連到當下夾爪</text>
<text x="503" y="24" text-anchor="middle" class="h">模型</text>
<rect class="n ghost" x="422" y="40" width="162" height="70" rx="12"/>
<text x="503" y="64" text-anchor="middle" class="b">訓練：模擬偽示範</text>
<text x="503" y="84" text-anchor="middle" class="s">ShapeNet 物體＋隨機</text>
<text x="503" y="102" text-anchor="middle" class="s">路徑點，邊訓邊生成</text>
<rect class="n vla" x="422" y="126" width="162" height="70" rx="12"/>
<text x="503" y="150" text-anchor="middle" class="b vla">異質圖 Transformer</text>
<text x="503" y="170" text-anchor="middle" class="s">擴散去噪動作節點</text>
<text x="503" y="188" text-anchor="middle" class="s">平移、旋轉分開預測</text>
<text x="709" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n key" x="628" y="83" width="162" height="70" rx="12"/>
<text x="709" y="107" text-anchor="middle" class="b">未來 8 步動作</text>
<text x="709" y="127" text-anchor="middle" class="s">SVD 對齊回 SE(3)</text>
<text x="709" y="145" text-anchor="middle" class="s">＋夾爪開合</text>
<path class="ar dash" d="M503,110 V124"/>
<path class="ar" d="M172,84 C193,84 193,75 214,75"/>
<path class="ar" d="M172,161 C193,161 193,75 214,75"/>
<path class="ar" d="M297,110 V124"/>
<path class="ar vla" d="M378,161 C399,161 399,161 420,161"/>
<path class="ar vla" d="M584,161 C605,161 605,118 626,118"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2411.12633">Instant Policy（arXiv:2411.12633）</a>，Imperial College London，ICLR 2025 oral。</figcaption>
</figure>

**一句話**：把「示範＋當下＋要預測的動作」全部畫成一張圖，用圖擴散模型一次生成未來 8 步夾爪動作；訓練資料全部是模擬裡隨機生成的「偽示範」，測試時給 1～2 條真實示範就能做新任務。

**資料：為什麼偽示範就夠**

- 在模擬裡隨機放兩個 ShapeNet 物體，隨機產生 2～6 個「以物體為中心」的路徑點，讓虛擬 Robotiq 2F-85 夾爪走一遍（約一半樣本是抓取／放置型路徑，其餘完全隨機），用三台模擬深度相機拍點雲。
- 作者的想法是：模型要學的不是「某個任務」，而是「**怎麼把示範裡夾爪和物體的相對幾何關係，搬到新場景**」，所以任務語意不重要，幾何多樣就好。
- 邊訓練邊生成，每個樣本大約只看一次；250 萬步約等於 70 萬條不重複軌跡。訓練時每個樣本放 1～5 條示範。另加 30% 軌跡局部擾動、10% 夾爪狀態翻轉，模擬示範的雜訊與恢復動作。

**模型：三段式圖網路**

| 子網路 | 做什麼 |
|---|---|
| 幾何編碼器（凍結） | 預訓練佔用網路（occupancy network）的編碼器，把 2,048 點的點雲壓成 16 個節點、每個 512 維特徵 |
| σ 局部編碼 | 在每個時間點的局部圖上，把點雲資訊傳給 6 個夾爪關鍵點節點 |
| φ 情境聚合 | 沿示範時間軸傳遞資訊，把「該怎麼做」匯聚到當下的夾爪節點（資訊瓶頸） |
| ψ 動作預測 | 從瓶頸傳到「假設夾爪已經移動後」的動作節點，輸出每個節點的去噪方向 |

三個子網路都是 2 層、隱藏維度 1024、16 頭的異質圖 Transformer。作者實驗發現，拆成三段比一個大網路好很多。動作的平移與旋轉分開去噪，最後用 SVD 把節點位移對齊回一個 SE(3) 變換。

**消融：哪些設計最關鍵**（相對基準的成功率變化，[論文 Table 2](https://proceedings.iclr.cc/paper_files/paper/2025/file/5692c7dbc4abcaa50f9ce609819212e5-Paper-Conference.pdf)）

| 改動 | 成功率變化 | 解讀 |
|---|---|---|
| 示範只取 1 個路徑點（L=1） | −71% | 示範必須保留過程，不能只給終點 |
| 只預測 1 步（T=1） | −52% | 一次預測多步很重要 |
| 不用擴散，直接回歸 | −29% | 擴散處理多種可能的動作 |
| 推論只去噪 1 步／2 步 | −16%／−2% | 2 步就夠，推論可以很快 |
| 示範從 2 條減為 1 條 | −12% | 多 1 條示範幫助大，再多則持平 |

**成績**

| 設定 | Instant Policy | BC-Z | Vid2Robot | GPT2 式 |
|---|---|---|---|---|
| RLBench 24 任務，只用偽示範 | **0.71** | 0.36 | 0.38 | 0.34 |
| 再加 12 個 RLBench 任務各 20 條示範：見過的任務 | **0.97** | 0.59 | 0.60 | 0.65 |
| 同上：沒見過的任務 | **0.82** | 0.43 | 0.37 | 0.31 |
| 真機 Sawyer 16 任務（開氣炸鍋、掛線、開收銀機等） | **88.75%** | 34.38% | 40.63% | 36.88% |

（基線都是作者用同樣資料重新實作的版本。）新形狀物體：示範 1→2→3→4 條，成功率 40%→52.5%→85%→90%，作者稱為湧現行為。

- **規模**：69M→117M 參數明顯變好，178M 只小幅提升；作者認為下一步要的是更多樣的資料。主模型大小論文未明寫。
- **延伸**：用 MediaPipe 把人手關鍵點映射成夾爪位姿，人手示範在簡單抓放可用；用 Sentence-BERT 把語言對齊到瓶頸，可做零示範的語言控制。兩者都只有定性結果。
- **局限**：要分割好的點雲、沒有顏色與語意；只適合短、近似馬可夫的任務；對示範品質與降採樣敏感；沒有避障與完整手臂控制；精度不夠做高接觸任務（[論文](https://arxiv.org/abs/2411.12633)、[程式碼與影片](https://www.robot-learning.uk/instant-policy)）。

### 3.7 REGENT（2024，ICLR 2025 oral）與 RICL（2025）：把情境內學習裝到 VLA 上

**REGENT** 先證明「檢索」是很強的歸納偏置：只用 1-最近鄰檢索的代理就已經很強；REGENT 用 19 個檢索鄰居當 context，參數 138.6M，比 JAT（192.7M）少，預訓練資料也少 5～10 倍，卻在沒見過的 Metaworld、Atari 等環境勝過 JAT／Gato（[論文](https://arxiv.org/abs/2412.04759)）。

**RICL** 把同一套配方搬到真實機器人與現成 VLA：

<figure class="dg">
<svg viewBox="0 0 800 276" role="img" aria-label="RICL：替現成的 π0-FAST 補上「檢索＋情境內學習」">
<text x="91" y="24" text-anchor="middle" class="h">資料</text>
<rect class="n" x="10" y="40" width="162" height="70" rx="12"/>
<text x="91" y="64" text-anchor="middle" class="b">後訓練（priming）</text>
<text x="91" y="84" text-anchor="middle" class="s">20 個任務 × 20 條</text>
<text x="91" y="102" text-anchor="middle" class="s">共約 400 條 DROID 示範</text>
<rect class="n" x="10" y="126" width="162" height="70" rx="12"/>
<text x="91" y="150" text-anchor="middle" class="b">使用者給的示範</text>
<text x="91" y="170" text-anchor="middle" class="s">新任務 10～20 條</text>
<text x="91" y="188" text-anchor="middle" class="s">存成檢索庫</text>
<rect class="n" x="10" y="212" width="162" height="52" rx="12"/>
<text x="91" y="236" text-anchor="middle" class="b">當下觀測</text>
<text x="91" y="256" text-anchor="middle" class="s">3 張影像＋本體＋指令</text>
<text x="297" y="24" text-anchor="middle" class="h">檢索</text>
<rect class="n" x="216" y="108" width="162" height="88" rx="12"/>
<text x="297" y="132" text-anchor="middle" class="b">DINOv2 + FAISS</text>
<text x="297" y="152" text-anchor="middle" class="s">用頂視角影像找</text>
<text x="297" y="170" text-anchor="middle" class="s">最近的 4 個片段</text>
<text x="297" y="188" text-anchor="middle" class="s">&lt; 1 毫秒</text>
<text x="503" y="24" text-anchor="middle" class="h">模型</text>
<rect class="n vla" x="422" y="65" width="162" height="88" rx="12"/>
<text x="503" y="89" text-anchor="middle" class="b vla">π0-FAST</text>
<text x="503" y="109" text-anchor="middle" class="s">LLM 全微調</text>
<text x="503" y="127" text-anchor="middle" class="s">影像編碼器凍結</text>
<text x="503" y="145" text-anchor="middle" class="s">4 個鄰居放 query 前</text>
<rect class="n" x="422" y="169" width="162" height="70" rx="12"/>
<text x="503" y="193" text-anchor="middle" class="b">動作插值</text>
<text x="503" y="213" text-anchor="middle" class="s">依距離混合鄰居動作</text>
<text x="503" y="231" text-anchor="middle" class="s">權重 e^(−10d)</text>
<text x="709" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n key" x="628" y="117" width="162" height="70" rx="12"/>
<text x="709" y="141" text-anchor="middle" class="b">15 步 × 8 維動作</text>
<text x="709" y="161" text-anchor="middle" class="s">FAST 解碼</text>
<text x="709" y="179" text-anchor="middle" class="s">比原版慢約 1.33 倍</text>
<path class="ar dash" d="M172,75 C296,75 296,109 420,109"/>
<path class="ar" d="M172,161 C193,161 193,152 214,152"/>
<path class="ar" d="M172,238 C193,238 193,152 214,152"/>
<path class="ar vla" d="M378,152 C399,152 399,109 420,109"/>
<path class="ar vla" d="M503,153 V167"/>
<path class="ar vla" d="M584,204 C605,204 605,152 626,152"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2508.02062">RICL（arXiv:2508.02062）</a>，賓州大學與 UBC。方法沿用同組的 <a href="https://arxiv.org/abs/2412.04759">REGENT（ICLR 2025）</a>，但改成在現成 VLA 上後訓練。</figcaption>
</figure>

| 方法 | 完整任務成功率 | 是否更新權重 |
|---|---|---|
| π0-FAST-DROID | 2.5% | 否 |
| **RICL-π0-FAST-DROID（只檢索＋情境內）** | **31.25%** | **否** |
| π0-FAST-DROID 在 20 條示範上微調 | 31.67% | 是 |
| RICL-π0-FAST-DROID 再微調 | 61.67% | 是 |

- **一句話結論**：不更新權重的 RICL，成績約等於直接微調原版；再加微調還能翻倍。原本會做的任務沒有退步（3 個原有任務成功率 80%，與原版相同）。
- **代價**：context 變 4 倍，推論慢約 1.33 倍（[論文](https://arxiv.org/abs/2508.02062)）。

### 3.8 MimicDroid（2025，ICRA 2026）：人形機器人＋人類 play 影片

<figure class="dg">
<svg viewBox="0 0 800 208" role="img" aria-label="MimicDroid：用人類隨手玩的影片訓練人形機器人的情境內模仿">
<text x="125" y="24" text-anchor="middle" class="h">資料</text>
<rect class="n" x="10" y="40" width="231" height="70" rx="12"/>
<text x="125" y="64" text-anchor="middle" class="b">人類 play 影片</text>
<text x="125" y="84" text-anchor="middle" class="s">模擬 8 小時（約 32 萬步）</text>
<text x="125" y="102" text-anchor="middle" class="s">真實 45 分鐘</text>
<rect class="n" x="10" y="126" width="231" height="70" rx="12"/>
<text x="125" y="150" text-anchor="middle" class="b">自動配對</text>
<text x="125" y="170" text-anchor="middle" class="s">相似片段檢索 top-10</text>
<text x="125" y="188" text-anchor="middle" class="s">DINOv2 特徵＋動作</text>
<text x="400" y="24" text-anchor="middle" class="h">模型</text>
<rect class="n" x="285" y="49" width="231" height="52" rx="12"/>
<text x="400" y="73" text-anchor="middle" class="b">手部估計 WiLoR</text>
<text x="400" y="93" text-anchor="middle" class="s">手腕未來位姿 = 動作標籤</text>
<rect class="n vla" x="285" y="117" width="231" height="70" rx="12"/>
<text x="400" y="141" text-anchor="middle" class="b vla">情境內策略</text>
<text x="400" y="161" text-anchor="middle" class="s">RGB＋本體＋10 個情境片段</text>
<text x="400" y="179" text-anchor="middle" class="s">隨機遮擋 patch（p=0.8）</text>
<text x="675" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n key" x="559" y="83" width="231" height="70" rx="12"/>
<text x="675" y="107" text-anchor="middle" class="b">32 步人手腕動作</text>
<text x="675" y="127" text-anchor="middle" class="s">重定向到 GR1 人形</text>
<text x="675" y="145" text-anchor="middle" class="s">逆運動學求關節角</text>
<path class="ar" d="M241,75 C262,75 262,75 283,75"/>
<path class="ar" d="M125,110 V124"/>
<path class="ar" d="M400,101 V115"/>
<path class="ar vla" d="M241,161 C262,161 262,152 283,152"/>
<path class="ar vla" d="M515,152 C536,152 536,118 557,118"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2509.09769">MimicDroid（arXiv:2509.09769）</a>，UT Austin（Yuke Zhu 組），ICRA 2026。遮擋 patch 用來縮小人手與機器人手外觀的差距。</figcaption>
</figure>

- **為什麼重要**：前面的方法大多要遙操作示範當訓練資料，MimicDroid 改用人類隨手玩的連續影片（每段 10～20 分鐘），不用標註，資料便宜很多。
- **成績**（真實 GR1 人形，三個泛化難度 L1／L2／L3）：MimicDroid 0.53／0.23／0.08，Vid2Robot 0.28／0.08／0.00。模擬中也勝過 Vid2Robot、測試時微調（PEFT）與 H2R。
- **局限**：最難的 L3 仍很低；情境示範超過 3 條就不再進步（作者歸因於訓練時的 context 長度）（[論文](https://arxiv.org/abs/2509.09769)、[專案頁](https://rpl.cs.utexas.edu/publications/2026/06/01/shah-icra26-mimicdroid/)）。

### 3.9 ICLR 視覺推理（2026-03）：示範裡加「意圖」 {#iclr-visual-reasoning}

<figure class="dg">
<svg viewBox="0 0 800 276" role="img" aria-label="ICLR（視覺推理）：示範裡多一條「意圖軌跡」，先推理再出動作">
<text x="125" y="24" text-anchor="middle" class="h">資料</text>
<rect class="n" x="10" y="40" width="231" height="70" rx="12"/>
<text x="125" y="64" text-anchor="middle" class="b">提示示範 3 條</text>
<text x="125" y="84" text-anchor="middle" class="s">影像＋狀態＋動作</text>
<text x="125" y="102" text-anchor="middle" class="s">＋每步的推理軌跡</text>
<rect class="n" x="10" y="126" width="231" height="70" rx="12"/>
<text x="125" y="150" text-anchor="middle" class="b">推理軌跡怎麼來</text>
<text x="125" y="170" text-anchor="middle" class="s">模擬：真值相機參數</text>
<text x="125" y="188" text-anchor="middle" class="s">真機：Molmo2 VLM 標</text>
<rect class="n" x="10" y="212" width="231" height="52" rx="12"/>
<text x="125" y="236" text-anchor="middle" class="b">當下觀測</text>
<text x="125" y="256" text-anchor="middle" class="s">影像＋本體狀態</text>
<text x="400" y="24" text-anchor="middle" class="h">模型</text>
<rect class="n" x="285" y="74" width="231" height="70" rx="12"/>
<text x="400" y="98" text-anchor="middle" class="b">凍結 ViT＋MLP 編碼</text>
<text x="400" y="118" text-anchor="middle" class="s">軌跡 = 5 個夾爪像素點</text>
<text x="400" y="136" text-anchor="middle" class="s">攤平成向量再嵌入</text>
<rect class="n vla" x="285" y="160" width="231" height="70" rx="12"/>
<text x="400" y="184" text-anchor="middle" class="b vla">Llama2 式 Transformer</text>
<text x="400" y="204" text-anchor="middle" class="s">沿用 ICRT</text>
<text x="400" y="222" text-anchor="middle" class="s">L = L動作 + 0.3 L推理</text>
<text x="675" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n mix" x="559" y="74" width="231" height="70" rx="12"/>
<text x="675" y="98" text-anchor="middle" class="b">① 推理軌跡</text>
<text x="675" y="118" text-anchor="middle" class="s">未來 5 個夾爪點</text>
<text x="675" y="136" text-anchor="middle" class="s">Dropout 版可跳過</text>
<rect class="n key" x="559" y="160" width="231" height="70" rx="12"/>
<text x="675" y="184" text-anchor="middle" class="b">② 16 步動作</text>
<text x="675" y="204" text-anchor="middle" class="s">末端位姿增量</text>
<text x="675" y="222" text-anchor="middle" class="s">真機 30 Hz</text>
<path class="ar" d="M241,75 C262,75 262,109 283,109"/>
<path class="ar dash" d="M125,126 V112"/>
<path class="ar" d="M241,238 C262,238 262,109 283,109"/>
<path class="ar vla" d="M400,144 V158"/>
<path class="ar vla" d="M515,195 C536,195 536,109 557,109"/>
<path class="ar vla" d="M675,144 V158"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2603.07530">ICLR: In-Context Imitation Learning with Visual Reasoning（arXiv:2603.07530）</a>；致謝提到 USC Physical Superintelligence Lab。</figcaption>
</figure>

- **論文**：[ICLR: In-Context Imitation Learning with Visual Reasoning（arXiv:2603.07530）](https://arxiv.org/abs/2603.07530)。注意它的縮寫也叫 ICLR，與會議同名。
- **要解決的問題**：ICRT 這類方法只看「狀態–動作」軌跡。場景一亂（多個干擾物、多個容器），同一段動作可能對應好幾種目標，模型看不出示範的**意圖**。
- **做法**：
    1. 每條提示示範的每一步，都附上一條**視覺推理軌跡**：從當下到回合結束，均勻取 5 個未來夾爪位置，投影到第三人稱畫面成為 5 個像素點。軌跡是數值向量，不是文字，用 MLP 編成推理 token。
    2. 骨幹沿用 ICRT（凍結 ViT＋Llama2 式因果 Transformer）；對題目軌跡先預測推理軌跡、再預測 16 步動作。loss = 動作 L1 ＋ 0.3 × 推理 L1。
    3. 訓練時隨機遮掉 0～100% 的推理 token；「Dropout 版」推論時直接跳過推理，只出動作。
    4. 推理軌跡的標籤：模擬用真值相機參數投影；真機用 Molmo2 VLM 標。
- **測試設定**：LIBERO 每個沒見過的任務給 3 條示範（50 個初始化 × 3 個提示 = 150 回合）；真機 Franka 每個任務 3 條示範（無干擾、1 個干擾物、干擾容器），每回合隨機挑 1 條。真機 30 Hz。

| 方法（成功率 %） | LIBERO-Object | LIBERO-90 廚房 | 客廳 | 書房 | LIBERO 平均 | 真機戳 | 真機抓放 |
|---|---|---|---|---|---|---|---|
| ICRT | 44.44 | 0.89 | 18.93 | 0.83 | 16.27 | 48.33 | 22.50 |
| TO（提示不給軌跡、題目仍預測） | 54.44 | 12.11 | 12.80 | 29.33 | 27.17 | 51.67 | 40.83 |
| **ICLR 完整版** | 70.00 | 20.00 | 11.20 | 32.17 | 33.34 | **71.67** | **60.00** |
| **ICLR Dropout 版** | **70.89** | **60.22** | **38.93** | **46.17** | **54.05** | 65.00 | 46.67 |

- **兩個重點結論**：①提示示範本身要帶軌跡（TO 明顯不如完整版），代表模型真的是從示範讀意圖；②模擬中 Dropout 版較好、真機則完整版較好，作者歸因於 LIBERO 訓練與測試差異較小。
- **失敗分析**：各 20 次失敗中，軌跡預測錯佔 40%（抓放）與 45%（戳）；其餘多是抓不穩、戳偏，作者認為**低階執行比推理更是瓶頸**。
- **局限**：只測兩類任務、一種推理表示；訓練仍需遙操作資料，人類影片與跨形體示範尚未做；雙手、靈巧手、長任務未涉及。
- **在本站分類中的位置**：路線 A（元學習專用策略），再加上〈[VLA 流派怎麼分](vla-taxonomy.html)〉軸 C 的「中間表徵」（先出軌跡、再出動作）。

### 3.10 Behavior Prompting Policy（2026-06）：一條人類示範就當提示

<figure class="dg">
<svg viewBox="0 0 800 276" role="img" aria-label="Behavior Prompting Policy：一條人類示範當「行為提示」">
<text x="125" y="24" text-anchor="middle" class="h">資料</text>
<rect class="n" x="10" y="40" width="231" height="70" rx="12"/>
<text x="125" y="64" text-anchor="middle" class="b">一條人類示範</text>
<text x="125" y="84" text-anchor="middle" class="s">iPhUMI：iPhone 手持</text>
<text x="125" y="102" text-anchor="middle" class="s">ARKit 記錄軌跡</text>
<rect class="n" x="10" y="126" width="231" height="52" rx="12"/>
<text x="125" y="150" text-anchor="middle" class="b">當下觀測</text>
<text x="125" y="170" text-anchor="middle" class="s">影像＋本體狀態</text>
<rect class="n" x="10" y="194" width="231" height="70" rx="12"/>
<text x="125" y="218" text-anchor="middle" class="b">訓練</text>
<text x="125" y="238" text-anchor="middle" class="s">同任務：一條當提示，</text>
<text x="125" y="256" text-anchor="middle" class="s">其他條當題目</text>
<text x="400" y="24" text-anchor="middle" class="h">模型</text>
<rect class="n vla" x="285" y="74" width="231" height="70" rx="12"/>
<text x="400" y="98" text-anchor="middle" class="b vla">提示編碼器 57M</text>
<text x="400" y="118" text-anchor="middle" class="s">降到約 1 Hz、每段池化</text>
<text x="400" y="136" text-anchor="middle" class="s">當下觀測交叉注意提示</text>
<rect class="n vla" x="285" y="160" width="231" height="70" rx="12"/>
<text x="400" y="184" text-anchor="middle" class="b vla">U-Net 擴散解碼 151M</text>
<text x="400" y="204" text-anchor="middle" class="s">改自 Diffusion Policy</text>
<text x="400" y="222" text-anchor="middle" class="s">FiLM 條件</text>
<text x="675" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n key" x="559" y="117" width="231" height="70" rx="12"/>
<text x="675" y="141" text-anchor="middle" class="b">閉環動作</text>
<text x="675" y="161" text-anchor="middle" class="s">6-DoF 末端動作</text>
<text x="675" y="179" text-anchor="middle" class="s">提示嵌入每回合算一次</text>
<path class="ar" d="M241,75 C262,75 262,109 283,109"/>
<path class="ar" d="M241,152 C262,152 262,109 283,109"/>
<path class="ar dash" d="M241,229 C262,229 262,195 283,195"/>
<path class="ar vla" d="M400,144 V158"/>
<path class="ar vla" d="M515,195 C536,195 536,152 557,152"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2606.30457">Behavior Prompting Policy（arXiv:2606.30457）</a>，Stanford（Shuran Song 組）與 UC Berkeley。</figcaption>
</figure>

- **成績**：原版 LIBERO 97.48%，與微調過的 π0.5（97.15%）相當，但 BPP **沒有任何基礎模型預訓練**。DrawAnything 模擬中，沒見過的圖形誤差比 ICRT 少 33.3%。
- **最重要的發現**：固定資料預算下，**任務多樣性比每個任務的示範數更重要**。
- **局限**：沒有證據顯示一條提示能教會全新的動作原語；摺衣服這種任務少的場景，BPP 不如語言條件策略（[論文](https://arxiv.org/abs/2606.30457)）。

### 3.11 ICI-VLA（2026-09）：在 VLA 上檢索「對齊時空」的微示範

- **論文**：[arXiv:2609.07581](https://arxiv.org/abs/2609.07581)。
- **做法**：保留 VLM 原本的「文字生成」介面輸出動作，不加額外融合模組；把長軌跡切成有語意標籤的短「微示範」，用 DTW 挖正樣本訓練檢索編碼器，確保檢索到的示範跟當下處在同一個子任務階段；再用 Target Action Masking 減少直接抄動作。
- **成績**：LIBERO 平均 97.7%；RoboTwin 2.0 平均 60.4%（比最強基線高 19.3 個百分點）；4 個真機任務 83.2%。
- **未寫**：底座 VLM 名稱與參數量摘要未寫。

### 3.12 In-Context World Modeling／ICWM（2026-06）：context 拿來認識「系統」，而不是指定任務 {#icwm}

<figure class="dg">
<svg viewBox="0 0 800 208" role="img" aria-label="ICWM：先隨機「試動」幾下，讓 VLA 從 context 推出相機與身體設定">
<text x="91" y="24" text-anchor="middle" class="h">部署前：試探</text>
<rect class="n mix" x="10" y="40" width="162" height="70" rx="12"/>
<text x="91" y="64" text-anchor="middle" class="b">任務無關的試探動作</text>
<text x="91" y="84" text-anchor="middle" class="s">在安全區隨機移動</text>
<text x="91" y="102" text-anchor="middle" class="s">不碰任務物體</text>
<rect class="n" x="10" y="126" width="162" height="70" rx="12"/>
<text x="91" y="150" text-anchor="middle" class="b">記錄轉移</text>
<text x="91" y="170" text-anchor="middle" class="s">（起始畫面、動作、</text>
<text x="91" y="188" text-anchor="middle" class="s">結束畫面）×N</text>
<text x="297" y="24" text-anchor="middle" class="h">context</text>
<rect class="n" x="216" y="49" width="162" height="70" rx="12"/>
<text x="297" y="73" text-anchor="middle" class="b">挑幾段當 context</text>
<text x="297" y="93" text-anchor="middle" class="s">真機：收 20 段約 5～6 秒</text>
<text x="297" y="111" text-anchor="middle" class="s">取 5 段放進輸入</text>
<rect class="n" x="216" y="135" width="162" height="52" rx="12"/>
<text x="297" y="159" text-anchor="middle" class="b">當下觀測＋指令</text>
<text x="297" y="179" text-anchor="middle" class="s">影像＋語言</text>
<text x="503" y="24" text-anchor="middle" class="h">模型</text>
<rect class="n vla" x="422" y="74" width="162" height="88" rx="12"/>
<text x="503" y="98" text-anchor="middle" class="b vla">VLA（同一組權重）</text>
<text x="503" y="118" text-anchor="middle" class="s">先讀試探 → 推出設定 ψ</text>
<text x="503" y="136" text-anchor="middle" class="s">再讀任務 → 出動作</text>
<text x="503" y="154" text-anchor="middle" class="s">不更新權重</text>
<text x="709" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n key" x="628" y="83" width="162" height="70" rx="12"/>
<text x="709" y="107" text-anchor="middle" class="b">連續動作</text>
<text x="709" y="127" text-anchor="middle" class="s">適應新視角</text>
<text x="709" y="145" text-anchor="middle" class="s">（與新形體）</text>
<path class="ar" d="M91,110 V124"/>
<path class="ar" d="M172,161 C193,161 193,84 214,84"/>
<path class="ar vla" d="M378,84 C399,84 399,118 420,118"/>
<path class="ar vla" d="M378,161 C399,161 399,118 420,118"/>
<path class="ar vla" d="M584,118 C605,118 605,118 626,118"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2606.26025">In-Context World Modeling for Robotic Control（arXiv:2606.26025）</a>，復旦大學、上海創智學院、同濟大學（OpenMOSS，邱錫鵬組）。重點：context 告訴模型的是「這套系統怎麼動」，不是「要做什麼任務」。</figcaption>
</figure>

- **論文**：[In-Context World Modeling for Robotic Control（arXiv:2606.26025）](https://arxiv.org/abs/2606.26025)，Siyin Wang、邱錫鵬等；機構為復旦大學、上海創智學院、同濟大學（[alphaXiv 整理](https://www.alphaxiv.org/overview/2606.26025)）。
- **要解決的問題**：VLA 只看當下畫面與指令，默認「相機擺位、機器人身體」跟訓練時一樣；相機一換角度，預訓練 VLA 在沒見過的視角常接近 0% 成功，每換一個環境就得重新收資料微調。
- **核心想法：把「系統辨識」變成情境內學習**。
    - 一般 ICIL：context 放**示範**，告訴模型「要做什麼任務」。
    - ICWM：context 放**機器人自己隨便動幾下的紀錄**（起始畫面、動作、結束畫面），讓模型從「我這樣動，畫面會怎麼變」推出目前的相機視角、身體等**不隨時間變的系統設定 ψ**，再去做任務。
    - 推出設定和輸出動作是**同一個 VLA、同一次前向**，不加額外網路，也不更新權重；論文說的「世界模型」是**隱式**的，沒有另外的前向／逆向動力學頭。
- **資料與訓練**：
    - 真機：UR5e＋Robotiq 夾爪＋12 台相機，6 台訓練、6 台留作零樣本測試；4 個任務各 100～150 條遙操作示範。
    - 模擬：LIBERO-Long，8 個相機方位角訓練、6 個沒見過的方位角測試。
    - 訓練時從所有任務與視角的「試探片段池」隨機抽 N 段，接在每條完整示範前面，用下一步動作預測訓練。
    - 部署：真機收 20 段試探轉移（約 5～6 秒），挑 5 段當 context。
- **成績**（LIBERO-Long，6 個沒見過的視角平均，[alphaXiv 整理](https://www.alphaxiv.org/overview/2606.26025)）：

| 設定 | 成功率 |
|---|---|
| 多視角行為複製（MV，基線） | 19.8% |
| **ICWM（正確 context）** | **25.0%**（相對提升 26.3%） |
| ICWM 不給 context | 22.0% |
| ICWM 給「錯的」context（偏 180° 視角拍的） | 18.9%（比不給還差） |
| 消融：context 拿掉動作 token | 21.6% |
| 消融：context 拿掉影像 token | 10.9% |

- **怎麼解讀**：給錯 context 比不給還差、拿掉影像就崩，說明模型真的在讀「動作→畫面變化」來推系統設定。四種試探策略都勝過基線，所以關鍵是「轉移紀錄」這個格式，而不是某種特定動作。真機在 4 個任務上也是 ICWM 平均最好（數字在論文表格中，我讀到的版本未列出）。
- **局限**：絕對成功率仍低（25%），135° 視角幾乎全滅（ICWM 2.2% vs MV 1.2%）；仍需在很多種設定上訓練；部署前多一個試探步驟；作者也承認結果只是「與推出系統設定一致」，不證明模型學到唯一的內部世界模型。
- **未寫**：我能讀到的版本（arXiv 摘要、[alphaXiv](https://www.alphaxiv.org/overview/2606.26025) 與 [hyper.ai](https://hyper.ai/en/papers/2606.26025) 的全文整理）沒寫底座 VLA 名稱與參數量；arXiv 全文頁在整理時無法讀取。
- **在本站分類中的位置**：不屬於前面四條「用示範指定任務」的路線，而是**情境內學習的另一個用途：情境內系統辨識**。它和世界模型的關係是「把世界模型該知道的系統動力學，用 context 臨時推出來」，可對照〈[世界模型四類與五種角色](world-model-roles.html)〉。

### 3.13 延伸：Zero-WAM（2026-08）：情境內模仿＋世界–動作模型

<figure class="dg">
<svg viewBox="0 0 800 294" role="img" aria-label="Zero-WAM：人類影片當提示的世界–動作模型">
<text x="125" y="24" text-anchor="middle" class="h">資料</text>
<rect class="n" x="10" y="40" width="231" height="70" rx="12"/>
<text x="125" y="64" text-anchor="middle" class="b">HumanGen</text>
<text x="125" y="84" text-anchor="middle" class="s">74.2K 組人–機配對</text>
<text x="125" y="102" text-anchor="middle" class="s">8.6K 任務，人影片為生成</text>
<rect class="n" x="10" y="126" width="231" height="70" rx="12"/>
<text x="125" y="150" text-anchor="middle" class="b">任務多樣的影片–動作</text>
<text x="125" y="170" text-anchor="middle" class="s">5 個公開資料集</text>
<text x="125" y="188" text-anchor="middle" class="s">6,000+ 任務</text>
<rect class="n" x="10" y="212" width="231" height="70" rx="12"/>
<text x="125" y="236" text-anchor="middle" class="b">測試提示</text>
<text x="125" y="256" text-anchor="middle" class="s">一段人類影片</text>
<text x="125" y="274" text-anchor="middle" class="s">或一句語言</text>
<text x="400" y="24" text-anchor="middle" class="h">模型</text>
<rect class="n wm" x="285" y="83" width="231" height="70" rx="12"/>
<text x="400" y="107" text-anchor="middle" class="b">Wan 2.2 TI2V-5B 改造</text>
<text x="400" y="127" text-anchor="middle" class="s">因果影片–動作模型</text>
<text x="400" y="145" text-anchor="middle" class="s">影片、動作兩支 Transformer</text>
<rect class="n" x="285" y="169" width="231" height="70" rx="12"/>
<text x="400" y="193" text-anchor="middle" class="b">IFP 輔助頭（只訓練用）</text>
<text x="400" y="213" text-anchor="middle" class="s">預測未來 4 段機器人影片</text>
<text x="400" y="231" text-anchor="middle" class="s">逼模型看提示影片</text>
<text x="675" y="24" text-anchor="middle" class="h">輸出</text>
<rect class="n wm" x="559" y="101" width="231" height="52" rx="12"/>
<text x="675" y="125" text-anchor="middle" class="b">下一段機器人影片</text>
<text x="675" y="145" text-anchor="middle" class="s">自回歸預測</text>
<rect class="n key" x="559" y="169" width="231" height="52" rx="12"/>
<text x="675" y="193" text-anchor="middle" class="b">對齊的動作 chunk</text>
<text x="675" y="213" text-anchor="middle" class="s">直接執行</text>
<path class="ar dash" d="M241,75 C262,75 262,118 283,118"/>
<path class="ar dash" d="M241,161 C262,161 262,118 283,118"/>
<path class="ar" d="M241,247 C262,247 262,118 283,118"/>
<path class="ar dash" d="M400,169 V155"/>
<path class="ar wm" d="M515,118 C536,118 536,127 557,127"/>
<path class="ar vla" d="M515,118 C536,118 536,195 557,195"/>
</svg>
<figcaption>來源：<a href="https://arxiv.org/abs/2608.26103">Zero-WAM（arXiv:2608.26103）</a>，Robbyant、港科大（廣州）、港科大。</figcaption>
</figure>

- **論文**：[Zero-WAM（arXiv:2608.26103）](https://arxiv.org/abs/2608.26103)，Robbyant、港科大（廣州）、港科大。
- **為什麼放在這裡**：它把 ICIL 和世界模型直接結合，提示是一段**人類影片**，模型同時預測下一段**機器人影片**和對應的**動作**。
- **防止忽略提示**：只靠動作 loss，模型容易無視提示影片；IFP（in-context future chunk prediction）輔助頭要求預測未來 4 段機器人影片，推論時拿掉。加了 IFP，7 個沒見過任務平均從 28.55% 升到 46.95%。
- **成績**：RoboTwin 2.0 的 7 個沒見過任務平均 46.95%，對照 LingBot-VA 17.45%、WAN-Action 10.98%；真機雙臂 Franka：物體放容器 53.3% vs 43.3%、三物體依序操作 33.3% vs 10.0%、插兩根桌腳 16.7% vs 0.0%。

## 四、它跟 VLA 是什麼關係？

| | 一般 VLA（語言條件） | VLA＋微調 | 情境內模仿（ICIL） |
|---|---|---|---|
| 怎麼指定任務 | 一句語言指令 | 語言指令＋新權重 | **示範**（可再加語言） |
| 新任務要什麼 | 預訓練時見過才會 | 幾十到幾千條示範＋訓練 | 1～20 條示範，不訓練 |
| 部署時權重 | 固定 | 每個任務一份 | 固定，一份走天下 |
| 代表 | [π0](https://arxiv.org/abs/2410.24164)、[OpenVLA](https://arxiv.org/abs/2406.09246) | [OpenVLA-OFT](https://arxiv.org/abs/2502.19645) | [RICL-π0-FAST](https://arxiv.org/abs/2508.02062)、[ICI-VLA](https://arxiv.org/abs/2609.07581)、[Skild S1](https://www.skild.ai/blogs/s1) |

1. **ICIL 不是取代 VLA，而是換一種「任務介面」**：語言說「做什麼」，示範說「怎麼做」。Skild 實驗顯示，在 1k 小時預訓練的小規模下，語言條件 VLA（53%）其實比 ICL（43%）好；但在 10 萬小時規模、沒見過的任務上，語言提示只有 9%，ICL 有 66%（[Skild S1](https://www.skild.ai/blogs/s1)）。
2. **三種「裝進 VLA」的方式**：
    - 從頭把 VLA 訓練成情境內學習者：Skild S1 自稱這樣做，訓練資料是「任務只透過一段示範給出」的分集資料。
    - 在現成 VLA 上後訓練：RICL（π0-FAST）、ICI-VLA；ICRT 也試過把骨幹換成 Llama2-7B。
    - 不特別訓練、靠規模湧現：Generalist 說 GEN-1.5「沒有為了情境內學習改架構，也沒用元學習或輔助目標」（[GEN-1.5](https://generalistai.com/blog/gen-1.5)）。
3. **評測上的直接比較**：ICRT 在同一套真機任務上大幅勝過 OpenVLA、Octo；BPP 在 LIBERO 追平 π0.5。注意這些都是「新任務、不微調 VLA」的設定，對 VLA 本來就不利。
4. **跟世界模型的關係**：多數 ICIL 方法**不預測未來畫面**，所以不是世界模型；兩者原本是互補的「快速適應」手段：世界模型靠想像生成資料或在想像中 RL（見〈[訓練時 vs 推論時](train-vs-inference.html)〉），ICIL 靠讀示範。2026 年開始有兩種交會：[ICWM](#icwm) 用 context **隱式**推出系統動力學（相機、身體），等於「情境內的世界模型」；[Zero-WAM](https://arxiv.org/abs/2608.26103) 則把影片生成模型改成世界–動作模型，看人類影片後同時預測機器人影片與動作。

## 五、現在誰在做？

### 業界

| 公司 | 產品 | 時間 | 官方說法 | 能驗證的程度 |
|---|---|---|---|---|
| **Skild AI** | **S1** | 2026-08 | 「從頭設計成情境內學習者」；一段人類第一人稱影片當提示，可做約 5～25 秒的原子技能到約 10 分鐘的長任務（種盆栽、翻鬆餅、手沖咖啡、組裝套件）；10 萬小時預訓練下，沒見過的任務 ICL 66% vs 語言提示 9%；從示範到自主執行 11 分鐘 | 🎤 只有[官方部落格](https://www.skild.ai/blogs/s1)；架構、參數量、資料組成未公開；作者自承基線 VLA 有人工介入救援 |
| **Generalist AI** | **GEN-1.5** | 2026-08-19 | 「3～12 秒示範就能情境內學會新任務」；示範可來自手持夾爪、機器人、模擬；10 個任務一次示範平均 59%；另一條路是 10 步梯度、5 分鐘資料微調到 83%；輸出 100 Hz 動作、記憶約 30 秒影片 | 🎤 只有[官方部落格](https://generalistai.com/blog/gen-1.5)；參數量未公開；作者自承任務「簡單、短」、技能比微調脆弱 |

!!! warn "沒查到的"
    Physical Intelligence（π 系列）、Google DeepMind（Gemini Robotics）、NVIDIA（GR00T）、Figure、Tesla 的官方頁面，目前都沒有把「不更新權重的情境內模仿」當產品功能發表；它們的快速適應仍以少量示範微調為主。這裡只寫查得到的，沒查到不代表沒在做。

### 學界主要團隊

| 團隊 | 作品 | 方向 |
|---|---|---|
| **Imperial College London**（Edward Johns，Robot Learning Lab） | [KAT](https://arxiv.org/abs/2403.19578)、[Instant Policy](https://arxiv.org/abs/2411.12633) | 免訓練 LLM、模擬偽示範＋圖擴散 |
| **UC Berkeley**（Ken Goldberg） | [ICRT](https://arxiv.org/abs/2408.15980) | 下一個 token 預測的情境內策略 |
| **UC Berkeley**（Trevor Darrell、Roei Herzig） | [RoboPrompt](https://arxiv.org/abs/2410.12782) | 用 LLM 文字提示做動作 |
| **賓州大學**（Dinesh Jayaraman、Insup Lee） | [REGENT](https://arxiv.org/abs/2412.04759)、[RICL](https://arxiv.org/abs/2508.02062) | 檢索增強，裝到 π0-FAST |
| **UT Austin**（Yuke Zhu） | [MimicDroid](https://arxiv.org/abs/2509.09769)；早期 [VIMA](https://arxiv.org/abs/2210.03094) | 人形＋人類影片 |
| **Stanford**（Shuran Song） | [Behavior Prompting Policy](https://arxiv.org/abs/2606.30457) | 一條人類示範當提示、iPhUMI 收集 |
| **Google DeepMind**、CMU、多倫多大學 | [Vid2Robot](https://arxiv.org/abs/2403.12943) | 影片條件策略 |
| **USC 等** | [ICLR 視覺推理](https://arxiv.org/abs/2603.07530) | 示範加上意圖（推理軌跡） |

## 六、成績總覽

| 論文 | 年份 | 路線 | 示範數 | 輸出 | 主要成績 |
|---|---|---|---|---|---|
| [Vid2Robot](https://arxiv.org/abs/2403.12943) | 2024 | A | 1 段影片 | 11 維離散動作，4 步 | 人類影片提示 52.8%（BC-Z 30.6%） |
| [ICRT](https://arxiv.org/abs/2408.15980) | 2024 | A | 數條遙操作 | 16 步 chunk | 真機平均 79.2%（OpenVLA 7.5%） |
| [KAT](https://arxiv.org/abs/2403.19578) | 2024 | B | 10 | 位姿軌跡 | 9 任務 0.68（DP 0.10） |
| [RoboPrompt](https://arxiv.org/abs/2410.12782) | 2024 | B | 10 | 關鍵幀位姿 | RLBench 51.8%（KAT 21.0%） |
| [Instant Policy](https://arxiv.org/abs/2411.12633) | 2024 | A | 1～2 | 8 步 SE(3) | 真機 88.75%（Vid2Robot 40.63%） |
| [RICL](https://arxiv.org/abs/2508.02062) | 2025 | C | 10～20（檢索 4 個） | 15 步 chunk | 2.5% → 31.25%（不更新權重） |
| [MimicDroid](https://arxiv.org/abs/2509.09769) | 2025 | A | 最多 10 段影片 | 32 步 chunk | GR1 真機 L1 0.53（Vid2Robot 0.28） |
| [ICLR 視覺推理](https://arxiv.org/abs/2603.07530) | 2026 | A | 數條 | 推理軌跡＋16 步 | 真機抓放 60.0%（ICRT 22.5%） |
| [BPP](https://arxiv.org/abs/2606.30457) | 2026 | A | 1 | 擴散動作 | LIBERO 97.48%（π0.5 97.15%） |
| [ICWM](https://arxiv.org/abs/2606.26025) | 2026 | 延伸 | 5 段試探轉移（非示範） | 連續動作 | LIBERO-Long 新視角 25.0%（MV 19.8%） |
| [Zero-WAM](https://arxiv.org/abs/2608.26103) | 2026 | A＋世界模型 | 1 段人類影片 | 機器人影片＋動作 chunk | RoboTwin 2.0 新任務 46.95%（LingBot-VA 17.45%） |
| [ICI-VLA](https://arxiv.org/abs/2609.07581) | 2026 | C | 檢索微示範 | 文字化動作 | LIBERO 97.7%、RoboTwin 2.0 60.4% |
| [GEN-1.5](https://generalistai.com/blog/gen-1.5) 🎤 | 2026 | D | 1 段 3～12 秒 | 100 Hz 動作 | 10 任務一次示範 59% |
| [Skild S1](https://www.skild.ai/blogs/s1) 🎤 | 2026 | D | 1 段人類影片 | 動作 | 沒見過的任務 66% |

各論文的任務、機器人、基線都不同，**數字只能在同一列內比較**，不能跨列比。🎤 = 只有官方部落格，沒有可重現的論文。

## 七、局限與開放問題

1. **學不到新的動作原語**：目前的情境內學習比較像「在已會的技能裡，看示範挑出要做哪個、對到哪個物體」（ICRT、BPP 都這樣承認）。
2. **示範變多不一定變好**：KAT 到 40 條就被微調方法反超；MimicDroid 超過 3 條就持平。context 長度與訓練分佈限制了上限。
3. **速度**：借用 LLM 的路線每次推論要幾秒；RICL 的 context 變長也讓推論變慢 1.33 倍。
4. **資料要「按任務分組」**：路線 A、C 都需要知道哪些軌跡屬於同一任務，大型開放資料集多半沒有這種結構（ICRT 用指令相似度去湊；MimicDroid 用相似片段檢索自動配對）。
5. **評估不統一**：真機任務、機器人、基線都不同；產品端只有部落格數字。

## 來源

**論文**

- [One-Shot Imitation Learning（arXiv:1703.07326）](https://arxiv.org/abs/1703.07326)
- [VIMA（arXiv:2210.03094）](https://arxiv.org/abs/2210.03094)
- [Vid2Robot（arXiv:2403.12943）](https://arxiv.org/abs/2403.12943)
- [Keypoint Action Tokens／KAT（arXiv:2403.19578）](https://arxiv.org/abs/2403.19578)
- [ICRT（arXiv:2408.15980）](https://arxiv.org/abs/2408.15980)、[程式碼](https://github.com/max-fu/icrt)
- [RoboPrompt（arXiv:2410.12782）](https://arxiv.org/abs/2410.12782)
- [Instant Policy（arXiv:2411.12633）](https://arxiv.org/abs/2411.12633)
- [REGENT（arXiv:2412.04759）](https://arxiv.org/abs/2412.04759)
- [RICL（arXiv:2508.02062）](https://arxiv.org/abs/2508.02062)
- [MimicDroid（arXiv:2509.09769）](https://arxiv.org/abs/2509.09769)
- [In-Context Imitation Learning with Visual Reasoning（arXiv:2603.07530）](https://arxiv.org/abs/2603.07530)
- [Behavior Prompting Policy（arXiv:2606.30457）](https://arxiv.org/abs/2606.30457)
- [ICI-VLA（arXiv:2609.07581）](https://arxiv.org/abs/2609.07581)
- [In-Context World Modeling for Robotic Control／ICWM（arXiv:2606.26025）](https://arxiv.org/abs/2606.26025)
- [Zero-WAM（arXiv:2608.26103）](https://arxiv.org/abs/2608.26103)
- [Instant Policy 程式碼與影片](https://www.robot-learning.uk/instant-policy)

**業界官方頁**

- [Skild AI：Introducing S1: In-Context Learning for Robotics](https://www.skild.ai/blogs/s1)
- [Generalist AI：GEN-1.5: Embodied Foundation Models are One-Shot Learners](https://generalistai.com/blog/gen-1.5)
