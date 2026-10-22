# 訓練時 vs 推論時：世界模型實際出現在哪裡

<p class="lede">回答四個問題：業界與學界訓練時怎麼用世界模型；機器人執行任務（推論）時，除了 VLA 之外有沒有讓世界模型的「部分」或「整體」參與；每種用法裡 VLA 和世界模型怎麼接線（輸入、輸出、世界模型的角色、數據量、參數量，各附一張流程圖）；這些世界模型的整體結構與參數量。數字都回到論文或官方頁核對過，查不到的標「未公開」。</p>

!!! key "重點先講"
    1. **訓練時用世界模型已是主流，推論時用還是少數。** 量產或接近量產的機器人（π0.5、GR00T N1.5、Figure Helix 等）在機器人身上跑的幾乎只有 VLA；世界模型留在雲端造資料、當 RL 訓練場、當考官。
    2. **推論時有參與的案例分三種程度**：
        - **只借「一部分」**：把影片擴散模型當視覺編碼器，只跑 **1 步去噪**拿特徵，不生成影片（VPP、智元 GE-Act），約 140–200 ms。
        - **整個世界模型先「想」再做**：先生成未來畫面，再轉成動作（UniPi、1X World Model、CoT-VLA）。最直觀但最慢：1X 一輪約 **12 秒**，CoT-VLA 慢約 **7 倍**。
        - **世界模型當「預演器」幫 VLA 挑動作**：VLA 先提候選，世界模型預測各自後果，再挑最好的（V-JEPA 2-AC、Cosmos Policy、VLA-Reasoner、FOREWARN、智元 τ0-VLA）。這是 2025–2026 最熱的方向，常被稱為「世界模型引導的測試時運算」。
    3. **很多「看起來有世界模型」的 VLA，推論時其實把它拿掉了**：DreamVLA 推論時跳過預測解碼器；GR00T N1.5 的 FLARE 只是訓練損失；WMPO、VLA-RFT、comma.ai 的世界模型只在訓練時存在。
    4. **結構幾乎都是同一個骨架**：影像壓縮器＋動力學骨幹＋條件輸入＋解碼器；機器人版再加「把畫面轉成動作」的頭。JEPA 例外：沒有解碼器。
    5. **參數量差距很大**：1 億級（138M、317M）、10 億級（1.5B、2B）到百億級（5.6B、8.4B、11B、14B）。**放進推論迴圈的通常是 2B 以下，或只跑一步。** Genie 3、Veo、Tesla、Waymo 的世界模型都未公開。

## 一張圖看懂：T1–T4 與 I0–I3

<figure class="dg">
<svg viewBox="0 0 800 300" role="img" aria-label="世界模型在訓練時與推論時的位置">
<rect class="n band" x="10" y="10" width="420" height="280" rx="14"/>
<rect class="n band" x="520" y="10" width="270" height="280" rx="14"/>
<text x="220" y="34" text-anchor="middle" class="h">訓練時（雲端）· 已是主流</text>
<text x="655" y="34" text-anchor="middle" class="h">推論時（機器人上）· 仍是少數</text>
<rect class="n" x="25" y="110" width="100" height="70" rx="10"/>
<text x="75" y="140" text-anchor="middle" class="b">網路影片</text>
<text x="75" y="162" text-anchor="middle" class="b">機器人資料</text>
<rect class="n wm" x="160" y="50" width="250" height="44" rx="8"/><text x="175" y="78" class="b">T1 預訓練或輔助目標</text>
<rect class="n wm" x="160" y="104" width="250" height="44" rx="8"/><text x="175" y="132" class="b">T2 資料工廠（造軌跡）</text>
<rect class="n wm" x="160" y="158" width="250" height="44" rx="8"/><text x="175" y="186" class="b">T3 想像中做 RL</text>
<rect class="n wm" x="160" y="212" width="250" height="44" rx="8"/><text x="175" y="240" class="b">T4 評估器（考官）</text>
<path class="ar" d="M125,145 H158"/>
<rect class="n vla" x="440" y="120" width="70" height="50" rx="8"/><text x="475" y="150" text-anchor="middle" class="b">VLA</text>
<path class="ar vla" d="M410,145 H438"/>
<path class="ar vla" d="M510,145 H530"/>
<rect class="n vla" x="535" y="50" width="245" height="44" rx="8"/><text x="550" y="70" class="b">I0 完全不參與</text><text x="550" y="87" class="s">大多數產品，只跑 VLA</text>
<rect class="n" x="535" y="104" width="245" height="44" rx="8"/><text x="550" y="124" class="b">I1 借一部分</text><text x="550" y="141" class="s">1 步去噪取特徵：VPP、GE-Act</text>
<rect class="n" x="535" y="158" width="245" height="44" rx="8"/><text x="550" y="178" class="b">I2 整體先想再做</text><text x="550" y="195" class="s">生成未來：UniPi、1X、CoT-VLA</text>
<rect class="n key" x="535" y="212" width="245" height="44" rx="8"/><text x="550" y="232" class="b">I3 預演候選、挑最好的</text><text x="550" y="249" class="s">V-JEPA 2-AC、Cosmos Policy、τ0</text>
</svg>
<figcaption>同一個模型可以同時屬於好幾格。例如智元 Genie Envisioner：GE-Base 是 T1，GE-Sim 是 T4，GE-Act 推論時屬於 I1。橘色的 I3 是 2025–2026 最熱的方向。</figcaption>
</figure>

## 速查：VLA 和世界模型怎麼「接線」

同一個問題問七次：世界模型吃什麼、吐什麼？吐出來的東西交給 VLA 的哪裡？它在整個系統裡扮演什麼角色？規模多大？下面每一列都在後文有一張流程圖和一張「連動卡」。

| 模式 | 世界模型在哪裡跑 | 世界模型：輸入 → 輸出 | VLA 從它拿到什麼 | 角色 | 代表的世界模型參數量 | 代表的數據量 |
|---|---|---|---|---|---|---|
| **T1** 預訓練／輔助目標 | 訓練時，和 VLA 同一張網 | 當前畫面 → 未來畫面或未來表徵 | 梯度：「先學會預測未來」的特徵 | 老師 | GR-2 230M（整個模型）；FLARE 分支在 GR00T N1.5（3B）內，未單列 | GR-2 預訓練 3,800 萬段影片 |
| **T2** 資料工廠 | 雲端離線 | 初始畫面＋新指令 → 機器人影片（再由 IDM 補動作） | 新的訓練軌跡 | 資料工廠 | DreamGen 用 WAN2.1（尺寸論文未寫） | 2,884 條示範 → RoboCasa 24 萬條神經軌跡 |
| **T3** 想像中做 RL | 雲端訓練迴圈 | 前幾幀＋VLA 的動作 → 接下來幾幀 | 想像的下一個觀測＋獎勵 | 練習場 | VLA-RFT 138M；UniSim 5.6B；WMPO 未公開 | VLA-RFT 400 次迭代；WMPO 128／1,280 條真機 |
| **T4** 評估器 | 雲端評估 | 初始畫面＋策略的動作 → 執行影片 | 不直接給，給工程師排名 | 考官 | Veo 未公開；GE-Sim 2B 級；Ctrl-World 1.5B | Veo：1,600 次以上真機對照 |
| **I0** 不參與 | 不在機器人上 | — | 只透過訓練好的權重 | — | — | — |
| **I1** 借一部分 | 機器人上，每步 1 次前向 | 當前畫面＋指令 → 中間特徵（不出影片） | 帶有「未來」的視覺特徵 | 視覺編碼器 | VPP 1.5B；GE-Base 2B 級＋GE-Act 160M | VPP 約 37 萬條軌跡；GE 2,967 小時 |
| **I2** 先想再做 | 機器人或伺服器上，每輪生成整段影片 | 當前畫面＋指令 → 數秒未來影片 | IDM 從影片抽出的動作 | 策略本體 | 1X 14B；CoT-VLA 7B；UniPi 未公開 | 1X：900 小時人類＋70 小時 NEO |
| **I3** 預演挑選 | 機器人上，沒把握時觸發 | 當前狀態＋候選動作 → 預測後果（＋價值） | 挑過的那一個動作 | 沙盤推演 | V-JEPA 2-AC 300M；VLA-Reasoner 600M；Cosmos Policy 2B | V-JEPA 2：100 萬小時以上影片＋62 小時 DROID |

!!! wm "一句話記住"
    **訓練時**世界模型給 VLA 的是「梯度、資料、練習場、成績單」；**推論時**給的是「特徵、整段想像、或對候選動作的預演」。越靠近即時控制，世界模型就得越小或跑得越少。

## 一、訓練時怎麼用世界模型（T1–T4）

### T1 預訓練或輔助目標：讓 VLA「學會預測未來」

先讓模型學「預測下一幀／未來表徵」，再接動作頭；或在訓練 VLA 時多加一個「預測未來」的損失。

<figure class="dg">
<svg viewBox="0 0 800 262" role="img" aria-label="T1：世界模型當 VLA 的預訓練或輔助目標">
<rect class="n " x="10" y="75" width="130" height="80" rx="10"/>
<text x="75" y="112.5" text-anchor="middle" class="b">當前畫面</text>
<text x="75" y="129.5" text-anchor="middle" class="s">＋語言指令</text>
<rect class="n vla" x="185" y="65" width="170" height="100" rx="10"/>
<text x="270" y="104" text-anchor="middle" class="b vla">VLA 骨幹</text>
<text x="270" y="121" text-anchor="middle" class="s">VLM＋動作專家</text>
<text x="270" y="138" text-anchor="middle" class="s">共用同一份特徵</text>
<rect class="n vla" x="410" y="15" width="170" height="64" rx="10"/>
<text x="495" y="44.5" text-anchor="middle" class="b vla">動作頭</text>
<text x="495" y="61.5" text-anchor="middle" class="s">→ 動作 chunk</text>
<rect class="n wm" x="410" y="150" width="170" height="64" rx="10"/>
<text x="495" y="179.5" text-anchor="middle" class="b wm">世界模型分支</text>
<text x="495" y="196.5" text-anchor="middle" class="s">預測未來畫面／表徵</text>
<rect class="n key" x="625" y="150" width="165" height="64" rx="10"/>
<text x="707.5" y="179.5" text-anchor="middle" class="b key">預測損失</text>
<text x="707.5" y="196.5" text-anchor="middle" class="s">和真實的未來比對</text>
<path class="ar" d="M140,115 H183"/>
<path class="ar vla" d="M355,95 H382 V47 H408"/>
<path class="ar wm dash" d="M355,135 H382 V182 H408"/>
<path class="ar wm dash" d="M580,182 H623"/>
<path class="ar wm dash" d="M707,214 V236 H270 V167"/>
<text x="600" y="52" text-anchor="start" class="s">推論時只留這條</text>
<text x="490" y="252" text-anchor="middle" class="s">梯度回傳：逼 VLA 的特徵先學會「世界接下來會怎樣」</text>
</svg>
<figcaption>虛線只在訓練時存在。代表：GR-2 先用 3,800 萬段影片做「預測未來畫面」預訓練；FLARE（GR00T N1.5）在動作 DiT 裡加 32 個未來 token、DreamVLA 預測動態區域／深度／語意，兩者推論時都把這條分支拿掉。</figcaption>
</figure>

**連動卡：代表模型的輸入、輸出與規模**

| | [GR-2](https://arxiv.org/abs/2410.06158) | [FLARE](https://arxiv.org/abs/2505.15659) → [GR00T N1.5](https://research.nvidia.com/labs/gear/gr00t-n1_5/) | [DreamVLA](https://arxiv.org/abs/2507.04447) |
|---|---|---|---|
| VLA（參數量） | GR-2 本身：預設 **230M**（可訓練 95M） | GR00T N1.5：**3B** | 骨幹約 **345M**（GPT-2 Medium）＋DiT-B 動作頭 |
| 世界模型在哪 | 同一個 GPT 式 Transformer：先學預測未來畫面，再一起出動作 | 動作 DiT 裡多 32 個「未來 token」 | VLA 內的預測分支與解碼器 |
| 世界模型：輸入 → 輸出 | 語言＋過去畫面 → 未來畫面 token | 當前觀測 → 未來觀測的嵌入（不生成畫面） | 當前觀測 → 動態區域、深度、語意（DINOv2／SAM 特徵） |
| 對 VLA 的作用 | 預訓練任務：先學會「世界會怎麼變」 | 輔助損失（權重 0.2） | 輔助預測，讓動作特徵帶有「世界知識」 |
| 數據量 | 預訓練 **3,800 萬段**網路影片（500 億 token） | 也能吃沒有動作標註的人類第一視角影片；總時數未公開 | CALVIN／LIBERO／真機 |
| 推論時還在嗎 | 論文未說明是否每步生成 | **不在** | **不在**（推論時跳過解碼器） |

| 案例 | 誰做的 | 怎麼用 | 推論時還在嗎 |
|---|---|---|---|
| [GR-2（arXiv:2410.06158）](https://arxiv.org/abs/2410.06158) | 字節 Seed | 先用 **3,800 萬段網路影片**（500 億 token）做 GPT 式「預測未來畫面」預訓練，再用機器人軌跡同時微調影片生成與動作（cVAE 動作頭） | 論文說能「和動作一起」生成影片，但未說明部署時是否每步都生成 |
| [FLARE（arXiv:2505.15659）](https://arxiv.org/abs/2505.15659) → [GR00T N1.5](https://research.nvidia.com/labs/gear/gr00t-n1_5/) | NVIDIA | 在動作 DiT 裡加 32 個「未來 token」，對齊未來觀測的嵌入（不生成畫面），損失權重 0.2；也能吃沒有動作標註的人類第一視角影片 | **不在**：官方頁只描述成訓練損失 |
| [DreamVLA（arXiv:2507.04447）](https://arxiv.org/abs/2507.04447) | 學界 | 訓練時預測三種「世界知識」：動態區域、深度、語意（DINOv2／SAM 特徵） | **不在**：論文原話「推論時完全跳過解碼器」 |
| [WorldVLA（arXiv:2506.21539）](https://arxiv.org/abs/2506.21539) | 阿里達摩院 | 同一個自回歸模型同時當動作模型和世界模型（預測下一幀），互相幫助：抓取成功率 +4%、FVD −10% | 主要是動作模型在跑；未明說世界模型分支是否部署 |

**一句話**：把世界模型當「老師」或「預訓練任務」。好處是不增加推論成本，代價是推論時享受不到「先預演」的好處。

### T2 資料工廠：用世界模型生成新的訓練軌跡

微調影片模型「想像」機器人做新任務的影片，再用逆動力學模型（IDM）或潛在動作模型補上動作標籤，當成 VLA 的訓練資料。

<figure class="dg">
<svg viewBox="0 0 800 290" role="img" aria-label="T2：世界模型當資料工廠">
<rect class="n " x="10" y="20" width="160" height="64" rx="10"/>
<text x="90" y="49.5" text-anchor="middle" class="b">少量真機示範</text>
<text x="90" y="66.5" text-anchor="middle" class="s">數條到數千條</text>
<rect class="n " x="10" y="110" width="160" height="64" rx="10"/>
<text x="90" y="139.5" text-anchor="middle" class="b">初始畫面</text>
<text x="90" y="156.5" text-anchor="middle" class="s">＋新任務指令</text>
<rect class="n wm" x="220" y="20" width="190" height="154" rx="10"/>
<text x="315" y="86" text-anchor="middle" class="b wm">影片世界模型</text>
<text x="315" y="103" text-anchor="middle" class="s">例：WAN2.1</text>
<text x="315" y="120" text-anchor="middle" class="s">LoRA 微調</text>
<rect class="n " x="460" y="20" width="160" height="64" rx="10"/>
<text x="540" y="49.5" text-anchor="middle" class="b">想像出的影片</text>
<text x="540" y="66.5" text-anchor="middle" class="s">只有畫面、沒有動作</text>
<rect class="n " x="660" y="20" width="130" height="64" rx="10"/>
<text x="725" y="49.5" text-anchor="middle" class="b">IDM</text>
<text x="725" y="66.5" text-anchor="middle" class="s">兩幀 → 中間動作</text>
<rect class="n key" x="660" y="140" width="130" height="64" rx="10"/>
<text x="725" y="169.5" text-anchor="middle" class="b key">神經軌跡</text>
<text x="725" y="186.5" text-anchor="middle" class="s">影片＋動作標籤</text>
<rect class="n vla" x="420" y="140" width="190" height="64" rx="10"/>
<text x="515" y="169.5" text-anchor="middle" class="b vla">訓練 VLA</text>
<text x="515" y="186.5" text-anchor="middle" class="s">GR00T N1、π0…</text>
<rect class="n " x="420" y="236" width="190" height="44" rx="10"/>
<text x="515" y="262.5" text-anchor="middle" class="s">真機資料（1:1 混訓）</text>
<path class="ar" d="M170,52 H218"/>
<path class="ar" d="M170,142 H218"/>
<path class="ar wm" d="M410,52 H458"/>
<path class="ar" d="M620,52 H658"/>
<path class="ar" d="M725,84 V138"/>
<path class="ar vla" d="M660,172 H612"/>
<path class="ar" d="M515,236 V206"/>
</svg>
<figcaption>世界模型只活在雲端，交給 VLA 的是「新的訓練資料」。DreamGen 只用 2,884 條人形抓放示範微調 WAN2.1，就讓 GR1 學會新行為；RoboCasa 產出 24 萬條神經軌跡（1,500 張 L40 跑 54 小時）。</figcaption>
</figure>

**連動卡：[DreamGen](https://arxiv.org/abs/2505.12705)（NVIDIA）**

| 項目 | 內容 |
|---|---|
| 世界模型（參數量） | **WAN2.1**，LoRA（rank 4）微調。論文沒寫用哪個尺寸；Wan 2.1 官方有 1.3B／14B 兩版 |
| 世界模型：輸入 → 輸出 | 初始畫面＋新任務指令 → 機器人執行影片（**沒有動作**） |
| 補動作標籤 | IDM（SigLIP-2＋flow matching DiT，**參數量未公開**）：兩幀 → 中間的動作 chunk；或 LAPA 潛在動作 |
| 接上哪些 VLA | Diffusion Policy、π0（約 **3.3B**）、GR00T N1（約 **2.2B**）；神經軌跡沒有本體感覺，訓練時狀態設為 0 |
| 世界模型的作用 | 資料工廠：把少量示範「擴寫」成大量新行為、新環境的軌跡 |
| 數據量 | 微調世界模型只用少量真機：GR1 人形 **2,884 條**抓放、RoboCasa **1,200 條**示範；產出 RoboCasa **24 萬條**神經軌跡（最多是原始示範的 333 倍，1,500 張 L40 跑 54 小時）；與真機 1:1 混訓 |
| 成果 | 已進入 GR00T N1.5 預訓練：12 個新動詞成功率 13.1% → 38.3%（[官方頁](https://research.nvidia.com/labs/gear/gr00t-n1_5/)） |

| 案例 | 細節 |
|---|---|
| [DreamGen（arXiv:2505.12705）](https://arxiv.org/abs/2505.12705)，NVIDIA | 主力影片模型是 **WAN2.1**（LoRA 微調），也比較了 Hunyuan、CogVideoX、Cosmos。動作標籤預設用 IDM（SigLIP-2＋flow matching），也可用 LAPA 潛在動作。訓練過 Diffusion Policy、π0、GR00T N1。RoboCasa 生成了 **24 萬條**神經軌跡。**已進入 GR00T N1.5 預訓練資料**：12 個新動詞的成功率從 N1 的 13.1% 升到 38.3%（[GR00T N1.5 官方頁](https://research.nvidia.com/labs/gear/gr00t-n1_5/)） |
| [UniSim（arXiv:2310.06114）](https://arxiv.org/abs/2310.06114)，Google DeepMind | 生成 1 萬條長任務軌跡訓練 PaLM-E 式高階策略，比只用原始資料好 3–4 倍；再用 IDM 把影片轉成機器人動作 |
| [Genie Envisioner GE-Sim（arXiv:2508.05635）](https://arxiv.org/abs/2508.05635)，智元 | 以動作為條件的影片模擬器，可大量產生 rollout |
| [Cosmos-Predict2.5（arXiv:2511.00062）](https://arxiv.org/abs/2511.00062)，NVIDIA | 官方定位之一就是合成資料與 Sim2Real 轉換（搭配 Cosmos-Transfer2.5） |

### T3 在世界模型裡做強化學習（想像中練習）

真機做 RL 太貴又危險，所以讓 VLA 在世界模型想像出的環境裡試錯，用學到的獎勵模型打分。

<figure class="dg">
<svg viewBox="0 0 800 262" role="img" aria-label="T3：在世界模型裡做強化學習">
<rect class="n vla" x="10" y="55" width="160" height="110" rx="10"/>
<text x="90" y="99" text-anchor="middle" class="b vla">VLA（策略）</text>
<text x="90" y="116" text-anchor="middle" class="s">看想像畫面</text>
<text x="90" y="133" text-anchor="middle" class="s">出下一段動作</text>
<rect class="n wm" x="290" y="40" width="210" height="80" rx="10"/>
<text x="395" y="69" text-anchor="middle" class="b wm">世界模型</text>
<text x="395" y="86" text-anchor="middle" class="s">前幾幀＋動作 chunk</text>
<text x="395" y="103" text-anchor="middle" class="s">→ 接下來幾幀</text>
<rect class="n key" x="290" y="160" width="210" height="64" rx="10"/>
<text x="395" y="189.5" text-anchor="middle" class="b key">獎勵模型</text>
<text x="395" y="206.5" text-anchor="middle" class="s">想像結果成功了嗎？</text>
<rect class="n " x="590" y="160" width="200" height="64" rx="10"/>
<text x="690" y="189.5" text-anchor="middle" class="b">RL 更新</text>
<text x="690" y="206.5" text-anchor="middle" class="s">GRPO／REINFORCE</text>
<rect class="n ghost" x="590" y="40" width="200" height="80" rx="10"/>
<text x="690" y="69" text-anchor="middle" class="b">真機資料</text>
<text x="690" y="86" text-anchor="middle" class="s">只用來訓練、校準</text>
<text x="690" y="103" text-anchor="middle" class="s">世界模型</text>
<path class="ar vla" d="M170,70 H288"/>
<text x="229" y="62" text-anchor="middle" class="s">動作 chunk</text>
<path class="ar wm" d="M290,100 H172"/>
<text x="229" y="118" text-anchor="middle" class="s">想像的下一幀</text>
<path class="ar wm" d="M395,120 V158"/>
<path class="ar" d="M500,192 H588"/>
<path class="ar" d="M690,224 V244 H90 V167"/>
<text x="390" y="258" text-anchor="middle" class="s">更新後的 VLA 再進世界模型想像一輪</text>
<path class="ar dash" d="M590,80 H502"/>
</svg>
<figcaption>真機只負責「教世界模型像真的」，VLA 的試錯全部在想像中完成。VLA-RFT 用 138M 的世界模型做 400 次迭代就勝過 15 萬步 SFT；WMPO 用 128 或 1,280 條真機 rollout 校準世界模型。</figcaption>
</figure>

**連動卡：三種「想像中練習」的接法**

| | [UniSim](https://arxiv.org/abs/2310.06114) | [VLA-RFT](https://arxiv.org/abs/2510.00406) | [WMPO](https://arxiv.org/abs/2511.09515) |
|---|---|---|---|
| VLA（參數量） | PaLI 式 VLA，**3B** | VLA-Adapter 輕量版（原版骨幹 **0.5B**；RFT 用的版本論文未另列） | OpenVLA-OFT（以 OpenVLA **7B** 為底，論文未另列） |
| 世界模型（參數量） | 影片擴散，**5.6B** | LLaMA 式自回歸，**138M** | OpenSora 改的影片擴散，**未公開** |
| 世界模型：輸入 → 輸出 | 畫面＋動作（以文字描述）→ 下一段影片 | 初始幀＋7 維動作序列 → 逐幀生成未來畫面 | 最近 4 幀＋1 個動作 chunk → 之後 8 幀 |
| 獎勵從哪來 | 學到的獎勵模型 | 想像畫面與真實離線畫面的 L1＋LPIPS 差距（越像越好） | VideoMAE 成功分類器（F1 > 0.95） |
| 數據量 | 多來源混合，論文未給單一總量 | 世界模型在 LIBERO 上預訓練（條數未寫）；RL 只做 **400 次**迭代 | OXE 預訓練；再用 **128 或 1,280 條**真機 rollout 校準 |
| 成果 | 48 個任務 0.58 → 0.81，零樣本上真機 | LIBERO 86.6% → 91.3%，勝過 15 萬步 SFT | Mimicgen 平均 33.6% → 47.1%（128 條）→ 57.6%（1,280 條） |

| 案例 | 世界模型 | 策略 | 結果 |
|---|---|---|---|
| [UniSim](https://arxiv.org/abs/2310.06114)（DeepMind，2023） | 5.6B 影片擴散 | PaLI 3B 的 VLA，REINFORCE | 48 個任務成功率 0.58 → 0.81，**零樣本直接上真機** |
| [WMPO（arXiv:2511.09515）](https://arxiv.org/abs/2511.09515) | 繼承 OpenSora 的像素級影片擴散（VAE 換成 SDXL 的 2D VAE） | OpenVLA-OFT，GRPO | Mimicgen 平均 33.6% → 47.1%（128 條真實軌跡）→ 57.6%（1,280 條） |
| [VLA-RFT（arXiv:2510.00406）](https://arxiv.org/abs/2510.00406) | **138M** 的 LLaMA 式自回歸世界模型 | VLA-Adapter，GRPO | 只做 **400 次**迭代，LIBERO 86.6% → 91.3%，勝過 15 萬步 SFT |
| [Ctrl-World（arXiv:2510.10125）](https://arxiv.org/abs/2510.10125) | 由 1.5B 的 Stable Video Diffusion 初始化 | π0／π0-FAST／π0.5 | 用想像出的成功軌跡做後訓練，下游任務 38.7% → 83.4% |
| [Dreamer 4（arXiv:2509.24527）](https://arxiv.org/abs/2509.24527)，DeepMind | 2B 潛空間世界模型 | 只在想像中訓練 | 只用離線資料就在 Minecraft 挖到鑽石（0.7% 回合） |
| [comma.ai（arXiv:2504.19077）](https://arxiv.org/abs/2504.19077) | 500M DiT（另有 250M／1B） | 小型駕駛策略，在世界模型裡 on-policy 學 | **已上線 openpilot**：約 500 位使用者、4 萬趟行程的測試 |

### T4 評估器：用世界模型代替真機測試

<figure class="dg">
<svg viewBox="0 0 800 228" role="img" aria-label="T4：世界模型當評估器">
<rect class="n vla" x="10" y="20" width="130" height="44" rx="10"/>
<text x="75" y="48" text-anchor="middle" class="b vla">待測策略 A</text>
<rect class="n vla" x="10" y="78" width="130" height="44" rx="10"/>
<text x="75" y="106" text-anchor="middle" class="b vla">待測策略 B</text>
<rect class="n vla" x="10" y="136" width="130" height="44" rx="10"/>
<text x="75" y="164" text-anchor="middle" class="b vla">待測策略 C</text>
<rect class="n wm" x="220" y="40" width="210" height="120" rx="10"/>
<text x="325" y="80.5" text-anchor="middle" class="b wm">世界模型模擬器</text>
<text x="325" y="97.5" text-anchor="middle" class="s">初始畫面＋策略的動作</text>
<text x="325" y="114.5" text-anchor="middle" class="s">→ 執行影片</text>
<text x="325" y="131.5" text-anchor="middle" class="s">策略看影片再出下一步</text>
<rect class="n " x="480" y="65" width="140" height="70" rx="10"/>
<text x="550" y="97.5" text-anchor="middle" class="b">判定成敗</text>
<text x="550" y="114.5" text-anchor="middle" class="s">人工或模型</text>
<rect class="n key" x="660" y="65" width="130" height="70" rx="10"/>
<text x="725" y="97.5" text-anchor="middle" class="b key">排名</text>
<text x="725" y="114.5" text-anchor="middle" class="s">挑出最好的版本</text>
<path class="ar vla" d="M140,42 H180 V75 H218"/>
<path class="ar vla" d="M140,100 H218"/>
<path class="ar vla" d="M140,158 H180 V125 H218"/>
<path class="ar wm" d="M430,100 H478"/>
<path class="ar" d="M620,100 H658"/>
<text x="400" y="214" text-anchor="middle" class="s">用少量真機評估確認排名一致即可（Veo：8 個檢查點、1,600 次以上真機）</text>
</svg>
<figcaption>世界模型不改 VLA 的權重，交給工程師的是「哪個版本比較好」。也可以做安全紅隊測試：在想像中故意擺出危險場景。</figcaption>
</figure>

**連動卡：三個評估器**

| | [Veo 世界模擬器](https://arxiv.org/abs/2512.10675)（Gemini Robotics） | [GE-Sim](https://arxiv.org/abs/2508.05635)（智元） | [Ctrl-World](https://arxiv.org/abs/2510.10125) |
|---|---|---|---|
| 被評估的 VLA | Gemini Robotics 系列（參數量**未公開**） | 智元自家策略 | π0／π0-FAST／π0.5 |
| 世界模型（參數量） | Veo，**未公開** | 以 GE-Base（**2B 級**）為骨幹 | **1.5B**（由 SVD 初始化） |
| 世界模型：輸入 → 輸出 | 初始畫面＋策略的動作 → 執行影片 | 動作軌跡（畫成姿態圖）＋歷史畫面 → 動作條件影片；每隻手臂 7 維 | 多視角畫面＋動作 → 未來多視角影片 |
| 數據量／規模 | 用 8 個檢查點、**1,600 次以上**真機評估驗證排名 | 叢集平行，每小時上千個 episode | DROID 訓練 |
| 局限 | 只保證「相對排名」可信 | — | 會低估實際成功率 |

| 案例 | 細節 |
|---|---|
| [Gemini Robotics 團隊（arXiv:2512.10675）](https://arxiv.org/abs/2512.10675) | 以 **Veo** 為基礎做策略評估，涵蓋一般表現、分布外泛化與安全紅隊測試；用 8 個檢查點、1,600 次以上真機評估驗證它能排出策略的相對好壞 |
| [Ctrl-World](https://arxiv.org/abs/2510.10125) | 在想像中評估 π0 系列；能反映「有沒有聽懂指令」，但會**低估**實際成功率 |
| [GE-Sim](https://arxiv.org/abs/2508.05635) | 叢集平行化後，每小時可跑上千個 episode 的評估 |
| 1X、Tesla、Waymo、理想 | 見 [08 業界產品盤點](industry.html)；Tesla 的神經模擬器同時用於 FSD 與 Optimus，整理見 [案例：Tesla](tesla.html) |

## 二、推論時：除了 VLA，世界模型有沒有上場？（I0–I3）

### I0 完全不參與（目前業界的大多數）

π0／π0.5、GR00T N1.5、Figure Helix、智平方 GOVLA 等商用 VLA，公開資料顯示機器人上只跑 VLA。上面的 DreamVLA、FLARE、WMPO、VLA-RFT、comma.ai 也都是「世界模型只活在訓練期」。

**原因很實際**：機器人控制要 10–50 Hz，影片世界模型生成一段畫面要幾秒到幾分鐘。

<figure class="dg">
<svg viewBox="0 0 800 150" role="img" aria-label="I0：推論時世界模型完全不參與">
<rect class="n band" x="10" y="10" width="500" height="130" rx="10"/>
<rect class="n band" x="570" y="10" width="220" height="130" rx="10"/>
<text x="260" y="34" text-anchor="middle" class="h">雲端（訓練時）</text>
<text x="680" y="34" text-anchor="middle" class="h">機器人上（推論時）</text>
<rect class="n wm" x="30" y="55" width="200" height="64" rx="10"/>
<text x="130" y="84.5" text-anchor="middle" class="b wm">世界模型</text>
<text x="130" y="101.5" text-anchor="middle" class="s">T1–T4 任一種</text>
<rect class="n vla" x="290" y="55" width="200" height="64" rx="10"/>
<text x="390" y="84.5" text-anchor="middle" class="b vla">訓練好的 VLA 權重</text>
<text x="390" y="101.5" text-anchor="middle" class="s">世界模型的知識在這裡</text>
<rect class="n vla" x="585" y="55" width="190" height="64" rx="10"/>
<text x="680" y="84.5" text-anchor="middle" class="b vla">只跑 VLA</text>
<text x="680" y="101.5" text-anchor="middle" class="s">10–50 Hz 控制</text>
<path class="ar wm" d="M230,87 H288"/>
<path class="ar vla" d="M490,87 H583"/>
</svg>
<figcaption>世界模型的貢獻只透過權重傳過去，機器人上看不到它。π0／π0.5、GR00T N1.5、Figure Helix、智平方 GOVLA 公開資料都屬於這類。</figcaption>
</figure>


### I1 只借世界模型的「一部分」：當視覺編碼器

<figure class="dg">
<svg viewBox="0 0 800 228" role="img" aria-label="I1：只借世界模型的一部分當視覺編碼器">
<rect class="n " x="10" y="40" width="130" height="80" rx="10"/>
<text x="75" y="77.5" text-anchor="middle" class="b">當前畫面</text>
<text x="75" y="94.5" text-anchor="middle" class="s">＋語言指令</text>
<rect class="n wm" x="180" y="20" width="200" height="120" rx="10"/>
<text x="280" y="69" text-anchor="middle" class="b wm">影片世界模型</text>
<text x="280" y="86" text-anchor="middle" class="s">只跑 1 次前向</text>
<text x="280" y="103" text-anchor="middle" class="s">（或 1 步去噪）</text>
<rect class="n " x="420" y="45" width="150" height="70" rx="10"/>
<text x="495" y="77.5" text-anchor="middle" class="b">中間特徵</text>
<text x="495" y="94.5" text-anchor="middle" class="s">帶有「未來」資訊</text>
<rect class="n vla" x="610" y="45" width="180" height="70" rx="10"/>
<text x="700" y="77.5" text-anchor="middle" class="b vla">動作頭</text>
<text x="700" y="94.5" text-anchor="middle" class="s">Video Former＋擴散頭</text>
<rect class="n vla" x="610" y="150" width="180" height="48" rx="10"/>
<text x="700" y="180" text-anchor="middle" class="b vla">動作 chunk</text>
<rect class="n ghost" x="180" y="160" width="200" height="48" rx="10"/>
<text x="280" y="188.5" text-anchor="middle" class="s">跳過：把影片畫出來</text>
<path class="ar" d="M140,80 H178"/>
<path class="ar wm" d="M380,80 H418"/>
<path class="ar" d="M570,80 H608"/>
<path class="ar vla" d="M700,115 V148"/>
<path class="ar dash" d="M280,140 V158"/>
</svg>
<figcaption>世界模型「心裡有想像，但不把影片畫出來」。VPP：1.5B SVD 只跑一次前向，約 140 ms、RTX 4090 上 7–10 Hz；GE-Act：2B 級 GE-Base 只跑 1 步去噪，160M 動作解碼器 200 ms 出 54 步（30 Hz）。</figcaption>
</figure>

**連動卡：VLA 怎麼「只借一部分」**

| | [VPP](https://arxiv.org/abs/2412.14803)（清華等） | [GE-Act](https://arxiv.org/abs/2508.05635)（智元） |
|---|---|---|
| 世界模型（參數量） | Stable Video Diffusion，**1.5B**，加上 CLIP 語言條件 | GE-Base，**2B 級**影片 DiT |
| 世界模型：輸入 → 輸出 | 當前畫面＋指令＋雜訊潛變量，只跑 1 次前向 → U-Net 上採樣層特徵（不出影片） | 多視角畫面（頭部＋左右腕）＋指令＋稀疏歷史記憶，只跑 1 步去噪 → 視覺潛特徵 |
| 動作端（參數量） | Video Former＋擴散策略頭（**論文未單列**）→ 10 步 action chunk | GE-Act 動作解碼器 **160M** → 54 步軌跡（30 Hz） |
| 延遲 | 約 140 ms（文中寫 < 160 ms），RTX 4090 上 7–10 Hz | 200 ms（機上 RTX 4090） |
| 數據量 | 世界模型微調：**19.4 萬條**人類操作影片（Something-Something v2）＋**17.9 萬條**機器人軌跡（OXE）＋下游 CALVIN／MetaWorld／真機；8 張 A100 約 2–3 天 | GE-Base：AgiBot-World 約 **100 萬條**、**2,967 小時**雙臂真機；換新平台只要約 **250 條**（約 1 小時）示範 |

| 案例 | 怎麼借 | 代價 |
|---|---|---|
| [VPP（arXiv:2412.14803）](https://arxiv.org/abs/2412.14803)，清華等 | 把 1.5B 的 SVD 微調成文字引導的影片預測模型，推論時**只跑一次前向（不去噪成影片）**，取 U-Net 上採樣層特徵 → Video Former 壓縮 → 擴散策略頭出動作 | 約 140 ms，RTX 4090 上 7–10 Hz |
| [GE-Act（arXiv:2508.05635）](https://arxiv.org/abs/2508.05635)，智元 | GE-Base（2B 影片 DiT）每次只跑 **1 步** flow-matching 去噪並快取特徵；160M 動作解碼器跑 5 步 | 影片 DiT 5 Hz、動作 30 Hz，200 ms（RTX 4090） |
| [Video2Act（arXiv:2512.03044）](https://arxiv.org/abs/2512.03044)，智平方 | 借影片擴散模型的特徵給 VLA 用（見 [09 案例：智平方](ai2-robotics.html)） | — |

**白話**：世界模型「心裡有想像，但不把影片畫出來」，只把想像的中間特徵交給動作頭。這是目前最務實的推論期整合。

### I2 整個世界模型先「想」再做

<figure class="dg">
<svg viewBox="0 0 800 200" role="img" aria-label="I2：整個世界模型先想再做">
<rect class="n " x="10" y="45" width="120" height="80" rx="10"/>
<text x="70" y="82.5" text-anchor="middle" class="b">當前畫面</text>
<text x="70" y="99.5" text-anchor="middle" class="s">＋語言指令</text>
<rect class="n wm" x="170" y="25" width="200" height="120" rx="10"/>
<text x="270" y="74" text-anchor="middle" class="b wm">世界模型</text>
<text x="270" y="91" text-anchor="middle" class="s">生成數秒的未來影片</text>
<text x="270" y="108" text-anchor="middle" class="s">1X：14B，約 11 秒</text>
<rect class="n " x="410" y="50" width="130" height="70" rx="10"/>
<text x="475" y="82.5" text-anchor="middle" class="b">想像影片</text>
<text x="475" y="99.5" text-anchor="middle" class="s">例：5 秒</text>
<rect class="n " x="575" y="50" width="100" height="70" rx="10"/>
<text x="625" y="82.5" text-anchor="middle" class="b">IDM</text>
<text x="625" y="99.5" text-anchor="middle" class="s">約 1 秒</text>
<rect class="n vla" x="705" y="50" width="85" height="70" rx="10"/>
<text x="747.5" y="82.5" text-anchor="middle" class="b vla">執行</text>
<text x="747.5" y="99.5" text-anchor="middle" class="s">開迴路</text>
<path class="ar" d="M130,85 H168"/>
<path class="ar wm" d="M370,85 H408"/>
<path class="ar" d="M540,85 H573"/>
<path class="ar vla" d="M675,85 H703"/>
<text x="400" y="182" text-anchor="middle" class="s">整段想完才動：最直觀，但每輪要秒到分鐘級</text>
</svg>
<figcaption>世界模型本身就是策略的一部分。UniPi 生成約 1 分鐘（蒸餾後快 16 倍）；1X 一輪約 12 秒；CoT-VLA 改成只生成一張子目標影像，仍比不生成慢約 7 倍。</figcaption>
</figure>

**連動卡：先想再做的三種做法**

| | [UniPi](https://arxiv.org/abs/2302.00111)（Google） | [1X World Model](https://1x.tech/discover/world-model-self-learning)（1X NEO） | [CoT-VLA](https://arxiv.org/abs/2503.22020) |
|---|---|---|---|
| 世界模型（參數量） | 文字條件影片擴散，**未公開** | 骨幹 **14B** | 與 VLA 是同一個模型（VILA-U），**7B** |
| 世界模型：輸入 → 輸出 | 畫面＋文字 → 未來影片 | 當前畫面＋文字指令 → 5 秒未來影片 | 畫面＋指令 → 256 個 token 的子目標影像 |
| 怎麼變成動作 | 小型 IDM，動作開迴路執行 | IDM（參數量**未公開**）抽出動作 → NEO 執行 | 同一模型接著出 10 步動作 |
| 速度 | 約 1 分鐘，蒸餾後快 16 倍 | 骨幹 11 秒＋IDM 1 秒 | 比不生成影像慢約 7 倍 |
| 數據量 | 1,400 萬影片-文字對＋Bridge | 網路影片＋**900 小時**人類第一視角＋**70 小時** NEO | OXE 等 |

| 案例 | 流程 | 速度 |
|---|---|---|
| [UniPi（arXiv:2302.00111）](https://arxiv.org/abs/2302.00111)，Google | 文字條件影片擴散先生成未來影片 → 小型 IDM 轉成動作 | 論文自承生成約一分鐘，蒸餾後快 16 倍；動作以開迴路執行 |
| [1X World Model](https://1x.tech/discover/world-model-self-learning)，1X（商用 NEO） | 14B 影片模型生成 5 秒未來影片 → IDM 抽出動作 → NEO 執行 | 骨幹 11 秒＋IDM 1 秒；官方承認對需要即時反應的接觸任務太慢 |
| [CoT-VLA（arXiv:2503.22020）](https://arxiv.org/abs/2503.22020)，NVIDIA／Stanford | 7B VLA 先自回歸生成 256 個 token 的子目標影像，再出 10 步動作 | 比不生成影像**慢約 7 倍** |
| [UnifoLM-WMA-0](https://github.com/unitreerobotics/unifolm-world-model-action)，宇樹 | 「決策模式」下世界模型搭配動作頭，預測未來再出動作；推論跑在伺服器，機器人當客戶端 | 未公開 |

### I3 世界模型當「預演器」：幫 VLA 挑動作（最新趨勢）


<figure class="dg">
<svg viewBox="0 0 800 190" role="img" aria-label="I3：世界模型預演候選動作">
<rect class="n vla" x="10" y="40" width="150" height="90" rx="10"/>
<text x="85" y="82.5" text-anchor="middle" class="b vla">VLA／提案器</text>
<text x="85" y="99.5" text-anchor="middle" class="s">提出 N 個候選動作</text>
<rect class="n wm" x="220" y="40" width="180" height="90" rx="10"/>
<text x="310" y="74" text-anchor="middle" class="b wm">世界模型</text>
<text x="310" y="91" text-anchor="middle" class="s">當前狀態＋候選動作</text>
<text x="310" y="108" text-anchor="middle" class="s">→ 預測的後果</text>
<rect class="n " x="460" y="40" width="150" height="90" rx="10"/>
<text x="535" y="82.5" text-anchor="middle" class="b">價值模型／VLM</text>
<text x="535" y="99.5" text-anchor="middle" class="s">替後果打分</text>
<rect class="n vla" x="670" y="40" width="120" height="90" rx="10"/>
<text x="730" y="82.5" text-anchor="middle" class="b vla">執行最好的</text>
<text x="730" y="99.5" text-anchor="middle" class="s">那一個</text>
<path class="ar" d="M160,85 H218"/>
<text x="190" y="76" text-anchor="middle" class="s">N 個</text>
<path class="ar wm" d="M400,85 H458"/>
<text x="430" y="76" text-anchor="middle" class="s">N 個未來</text>
<path class="ar" d="M610,85 H668"/>
<text x="640" y="76" text-anchor="middle" class="s">分數</text>
<text x="400" y="170" text-anchor="middle" class="s">只在 VLA 沒把握時觸發（τ0-VLA 的信心路由），或多 GPU 平行（Cosmos Policy），才壓得住延遲</text>
</svg>
<figcaption>VLA 仍然負責出動作，世界模型只當「沙盤推演」。候選可以來自 VLA 取樣（Cosmos Policy、VLA-Reasoner），也可以來自 CEM 這類搜尋器（V-JEPA 2-AC）。</figcaption>
</figure>

**連動卡：誰提案、誰預演、怎麼挑**

| | [V-JEPA 2-AC](https://arxiv.org/abs/2506.09985)（Meta） | [Cosmos Policy](https://arxiv.org/abs/2601.16163)（NVIDIA） | [VLA-Reasoner](https://arxiv.org/abs/2509.22643) | [τ0-VLA](https://arxiv.org/abs/2608.16885)（智元） |
|---|---|---|---|---|
| 誰提候選 | CEM 搜尋器（800 個樣本、10 輪） | 同一個模型取樣多組動作 | OpenVLA（**7B**）等 VLA | 高階 VLM（**9B**），低階策略 **2B** |
| 世界模型（參數量） | 動作條件預測器 **300M**（編碼器凍結） | 與策略是同一個 **2B** 模型（Cosmos-Predict2-2B 微調） | iVideoGPT 式，**600M** | 由 Step1X-Edit 初始化，**未公開** |
| 世界模型：輸入 → 輸出 | 當前畫面表徵＋候選動作（末端位移）→ 下一步表徵（不生成像素） | 本體感覺＋多相機畫面＋指令 → 動作 chunk、未來狀態、價值（都當潛空間影格） | 當前畫面＋候選動作 → 未來畫面 | 當前畫面＋子任務 → 子任務完成時的畫面 |
| 怎麼打分 | 和目標影像表徵的 L1 距離 | 每個候選查世界模型 3 次、價值 5 次，15 個分數取「多數平均」 | MCTS，最後和 VLA 動作加權混合 | 價值模型評分，信心不足才觸發 beam search |
| 數據量 | 預訓練 **100 萬小時以上**影片＋**62 小時** DROID | LIBERO 每套 500 條、RoboCasa 每任務 50 條、ALOHA 每任務 15–80 條示範；規劃模型另用 **648 條** rollout | LIBERO 等 | 低階策略 **40,115 小時** |
| 代價與成果 | 每個動作 16 秒；零樣本抓放 65–80% | 多 GPU 平行；真實困難任務完成率平均 +12.5% | LIBERO 76.0% → 81.0% | 分布外子任務 50% → 74% |

| 案例 | 世界模型 | 搜尋方式 | 效果 |
|---|---|---|---|
| [V-JEPA 2-AC（arXiv:2506.09985）](https://arxiv.org/abs/2506.09985)，Meta | 300M 動作條件預測器（表徵空間，不生成像素） | CEM：800 個樣本、10 輪 | 零樣本抓放 65–80%（Octo 只有 10–15%）；**每個動作 16 秒**，Cosmos 要 4 分鐘 |
| [TD-MPC2（arXiv:2310.16828）](https://arxiv.org/abs/2310.16828) | 最大 317M 的潛空間模型 | 在潛空間做 MPC 軌跡最佳化 | 單一代理人做 80 個任務 |
| [Cosmos Policy（arXiv:2601.16163）](https://arxiv.org/abs/2601.16163)，NVIDIA | 由 Cosmos-Predict2-2B 微調；動作、未來狀態、價值都當成「潛空間影格」生成 | Best-of-N，多 GPU 平行 | LIBERO 98.5%；真實困難任務上，規劃讓完成率平均 **+12.5%** |
| [VLA-Reasoner（arXiv:2509.22643）](https://arxiv.org/abs/2509.22643) | 600M 的 iVideoGPT 式世界模型 | MCTS，最後與 VLA 動作加權混合 | OpenVLA 在 LIBERO 76.0% → 81.0%；也測過 π0-FAST 真機 |
| [FOREWARN（arXiv:2502.01828）](https://arxiv.org/abs/2502.01828)，CMU | DreamerV3 潛空間模型預測 64 步後果 | 100 個候選聚成 6 類，由 Llama-3.2-11B-Vision 讀潛向量並挑一個 | 比基礎模仿策略好 30% 以上 |
| [τ0-VLA（arXiv:2608.16885）](https://arxiv.org/abs/2608.16885)，**智元 Agibot** | 由 Step1X-Edit 初始化的影像世界模型，預測子任務完成時的畫面 | 信心不足時才觸發 beam search（9B 高階 VLM 提案＋價值模型評分） | 分布外子任務準確率 50% → 74%；泡奶茶、整理房間成功率 5/10 → 7/10 |

**白話**：這一類不讓世界模型「直接開車」，而是讓它當「副駕駛的沙盤推演」。τ0-VLA 和 Cosmos Policy 代表業界已經開始往這條路走。

### 自駕的對照

- **comma.ai**：世界模型只在訓練，車上只跑策略（T3／I0）。
- **蔚來 NWM**：官方宣稱在車上推演多條未來路徑，屬於 I3，但**沒有論文**可以核實。
- **Tesla、華為、小鵬**：世界模型用在雲端訓練與評估，車端是蒸餾後的端到端模型。

## 三、世界模型的整體結構

<figure class="dg">
<svg viewBox="0 0 800 250" role="img" aria-label="世界模型的共通骨架">
<rect class="n" x="10" y="30" width="120" height="60" rx="10"/><text x="70" y="65" text-anchor="middle" class="b">觀測影像</text>
<rect class="n" x="10" y="150" width="120" height="60" rx="10"/><text x="70" y="178" text-anchor="middle" class="b">文字／動作</text><text x="70" y="198" text-anchor="middle" class="s">條件</text>
<rect class="n" x="170" y="20" width="160" height="80" rx="10"/>
<text x="250" y="50" text-anchor="middle" class="b">① 壓縮器</text>
<text x="250" y="72" text-anchor="middle" class="s">VAE／VQGAN／</text><text x="250" y="88" text-anchor="middle" class="s">影片 tokenizer／自監督編碼器</text>
<rect class="n wm" x="370" y="70" width="180" height="110" rx="12"/>
<text x="460" y="100" text-anchor="middle" class="b wm">② 動力學骨幹</text>
<text x="460" y="124" text-anchor="middle" class="s">擴散／flow：DiT、U-Net</text>
<text x="460" y="144" text-anchor="middle" class="s">自回歸：GPT 式</text>
<text x="460" y="164" text-anchor="middle" class="s">表徵預測：JEPA predictor</text>
<rect class="n" x="590" y="20" width="200" height="70" rx="10"/>
<text x="690" y="50" text-anchor="middle" class="b">③ 解碼器</text><text x="690" y="72" text-anchor="middle" class="s">潛狀態 → 像素（JEPA 沒有）</text>
<rect class="n vla" x="590" y="150" width="200" height="80" rx="10"/>
<text x="690" y="180" text-anchor="middle" class="b vla">④ 機器人才有</text><text x="690" y="202" text-anchor="middle" class="s">IDM／動作專家／價值頭</text>
<path class="ar" d="M130,60 H168"/><path class="ar" d="M330,60 H350 V100 H368"/><path class="ar" d="M130,180 H350 V150 H368"/>
<path class="ar wm" d="M550,110 H570 V55 H588"/><path class="ar wm" d="M550,150 H570 V190 H588"/>
</svg>
<figcaption>壓縮率從 8×8 到約 400 倍。機器人版會多一個把「想像」變成「動作」或「分數」的頭。</figcaption>
</figure>

**三種典型組合**

1. **生成式影片世界模型（最常見）**：①VAE＋②DiT（flow matching）＋③解碼器。例：Cosmos、GE-Base、GAIA-2、comma.ai。
2. **潛空間 RL 世界模型**：①小編碼器＋②RSSM 或 Transformer＋獎勵／價值頭，解碼器只輔助學習。例：DreamerV3、Dreamer 4、TD-MPC2。
3. **JEPA**：①大型自監督 ViT（凍結）＋②動作條件預測器，**不重建畫面**。例：V-JEPA 2-AC。

## 四、參數量總表

<figure class="dg">
<svg viewBox="0 0 800 556" role="img" aria-label="世界模型參數量比較（對數刻度）">
<path d="M210.0,32 V496" stroke="var(--line)" stroke-dasharray="3 3"/><text x="210.0" y="26" text-anchor="middle" class="s">0.1B</text>
<path d="M317.8,32 V496" stroke="var(--line)" stroke-dasharray="3 3"/><text x="317.8" y="26" text-anchor="middle" class="s">0.3B</text>
<path d="M436.0,32 V496" stroke="var(--line)" stroke-dasharray="3 3"/><text x="436.0" y="26" text-anchor="middle" class="s">1B</text>
<path d="M543.8,32 V496" stroke="var(--line)" stroke-dasharray="3 3"/><text x="543.8" y="26" text-anchor="middle" class="s">3B</text>
<path d="M662.0,32 V496" stroke="var(--line)" stroke-dasharray="3 3"/><text x="662.0" y="26" text-anchor="middle" class="s">10B</text>
<text x="202" y="56" text-anchor="end" class="s">VLA-RFT 世界模型</text>
<rect x="210" y="45" width="31.6" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="247.6" y="56" class="s">138M</text>
<text x="202" y="80" text-anchor="end" class="s">GR-2（預設）</text>
<rect x="210" y="69" width="81.7" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="297.7" y="80" class="s">230M</text>
<text x="202" y="104" text-anchor="end" class="s">V-JEPA 2-AC 預測器</text>
<rect x="210" y="93" width="107.8" height="14" rx="3" fill="var(--vla)" opacity=".85"/>
<text x="323.8" y="104" class="s">300M</text>
<text x="202" y="128" text-anchor="end" class="s">TD-MPC2</text>
<rect x="210" y="117" width="113.2" height="14" rx="3" fill="var(--vla)" opacity=".85"/>
<text x="329.2" y="128" class="s">317M</text>
<text x="202" y="152" text-anchor="end" class="s">DreamVLA 骨幹</text>
<rect x="210" y="141" width="121.5" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="337.5" y="152" class="s">345M</text>
<text x="202" y="176" text-anchor="end" class="s">comma.ai 世界模型</text>
<rect x="210" y="165" width="158.0" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="374.0" y="176" class="s">500M</text>
<text x="202" y="200" text-anchor="end" class="s">iVideoGPT（VLA-Reasoner）</text>
<rect x="210" y="189" width="175.9" height="14" rx="3" fill="var(--vla)" opacity=".85"/>
<text x="391.9" y="200" class="s">600M</text>
<text x="202" y="224" text-anchor="end" class="s">VPP 影片模型</text>
<rect x="210" y="213" width="265.8" height="14" rx="3" fill="var(--vla)" opacity=".85"/>
<text x="481.8" y="224" class="s">1.5B</text>
<text x="202" y="248" text-anchor="end" class="s">Ctrl-World</text>
<rect x="210" y="237" width="265.8" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="481.8" y="248" class="s">1.5B</text>
<text x="202" y="272" text-anchor="end" class="s">Genie Envisioner GE-Base</text>
<rect x="210" y="261" width="294.0" height="14" rx="3" fill="var(--vla)" opacity=".85"/>
<text x="510.0" y="272" class="s">2B</text>
<text x="202" y="296" text-anchor="end" class="s">Cosmos Policy</text>
<rect x="210" y="285" width="294.0" height="14" rx="3" fill="var(--vla)" opacity=".85"/>
<text x="510.0" y="296" class="s">2B</text>
<text x="202" y="320" text-anchor="end" class="s">Dreamer 4</text>
<rect x="210" y="309" width="294.0" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="510.0" y="320" class="s">2B</text>
<text x="202" y="344" text-anchor="end" class="s">UniSim</text>
<rect x="210" y="333" width="395.1" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="611.1" y="344" class="s">5.6B</text>
<text x="202" y="368" text-anchor="end" class="s">CoT-VLA</text>
<rect x="210" y="357" width="417.0" height="14" rx="3" fill="var(--vla)" opacity=".85"/>
<text x="633.0" y="368" class="s">7B</text>
<text x="202" y="392" text-anchor="end" class="s">GAIA-2</text>
<rect x="210" y="381" width="434.9" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="650.9" y="392" class="s">8.4B</text>
<text x="202" y="416" text-anchor="end" class="s">GAIA-1（相加）</text>
<rect x="210" y="405" width="445.9" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="661.9" y="416" class="s">9.4B</text>
<text x="202" y="440" text-anchor="end" class="s">Genie（第一代）</text>
<rect x="210" y="429" width="461.3" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="677.3" y="440" class="s">11B</text>
<text x="202" y="464" text-anchor="end" class="s">1X World Model 骨幹</text>
<rect x="210" y="453" width="485.0" height="14" rx="3" fill="var(--vla)" opacity=".85"/>
<text x="701.0" y="464" class="s">14B</text>
<text x="202" y="488" text-anchor="end" class="s">Cosmos-Predict 最大版</text>
<rect x="210" y="477" width="485.0" height="14" rx="3" fill="var(--wm)" opacity=".85"/>
<text x="701.0" y="488" class="s">14B</text>
<rect x="210" y="515" width="14" height="14" rx="3" fill="var(--vla)"/><text x="230" y="526" class="s">推論時會參與（I1–I3）</text>
<rect x="410" y="515" width="14" height="14" rx="3" fill="var(--wm)"/><text x="430" y="526" class="s">只在訓練、雲端或研究中使用</text>
</svg>
<figcaption>對數刻度。只列論文或官方頁有明寫（或可由論文數字相加）的模型；Genie 3、Veo、Tesla、Waymo、華為的世界模型參數量未公開，未列入。</figcaption>
</figure>

> ✅＝論文或官方頁明寫；🧮＝由論文數字相加；❓＝未公開

| 模型 | 類型 | 結構重點 | 參數量 | 訓練資料 | 來源 |
|---|---|---|---|---|---|
| **TD-MPC2** | 潛空間（規劃） | 編碼器＋潛動力學＋價值，MPC | 最大 **317M** ✅ | 104 個任務 | [arXiv:2310.16828](https://arxiv.org/abs/2310.16828) |
| **DreamerV3** | 潛空間（RL） | RSSM | 12M–400M（規模實驗） | 150+ 任務 | [arXiv:2301.04104](https://arxiv.org/abs/2301.04104) |
| **VLA-RFT 世界模型** | 自回歸像素 | 預訓練 tokenizer＋LLaMA 式 Transformer | **138M** ✅ | LIBERO | [arXiv:2510.00406](https://arxiv.org/abs/2510.00406) |
| **GR-2** | 自回歸影片＋動作 | 凍結 VQGAN＋GPT 式 Transformer＋cVAE 動作頭 | 預設 **230M**（可訓練 95M）✅；規模實驗 30M–719M | 3,800 萬段影片 | [arXiv:2410.06158](https://arxiv.org/abs/2410.06158) |
| **V-JEPA 2／2-AC** | JEPA | ViT 編碼器＋動作條件預測器 | 編碼器 **300M–1B**，預測器 **300M** ✅ | 100 萬小時以上影片＋62 小時 DROID | [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) |
| **DreamVLA** | VLA＋世界知識預測 | GPT-2 Medium＋DiT-B 動作頭 | 骨幹約 **345M** ✅ | CALVIN／LIBERO／真機 | [arXiv:2507.04447](https://arxiv.org/abs/2507.04447) |
| **comma.ai 世界模型** | 影片擴散 | SD VAE＋3D DiT（rectified flow）＋Plan Head | 250M／**500M（主力）**／1B ✅ | 40 萬段 1 分鐘行車影片（約 6,700 小時 🧮） | [arXiv:2504.19077](https://arxiv.org/abs/2504.19077) |
| **iVideoGPT（VLA-Reasoner 用）** | 自回歸影片 | tokenizer＋GPT | **600M** ✅ | 小量機器人資料 | [arXiv:2509.22643](https://arxiv.org/abs/2509.22643) |
| **VPP** | 影片擴散（當編碼器） | SVD U-Net＋Video Former＋擴散策略頭 | 影片模型 **1.5B** ✅ | 機器人＋網路人類操作影片 | [arXiv:2412.14803](https://arxiv.org/abs/2412.14803) |
| **Ctrl-World** | 影片擴散 | 由 SVD 初始化，多視角、動作條件 | 骨幹 **1.5B** ✅ | DROID | [arXiv:2510.10125](https://arxiv.org/abs/2510.10125) |
| **Genie Envisioner** | 影片 DiT | GE-Base（LTX-Video 2B 或 Cosmos2 2B）＋凍結 T5-XXL；GE-Act 動作解碼器 | GE-Base **2B 級** ✅，GE-Act **160M** ✅ | 約 100 萬條、2,967 小時雙臂真機 | [arXiv:2508.05635](https://arxiv.org/abs/2508.05635) |
| **Cosmos Policy** | 影片 DiT 改策略 | Cosmos-Predict2-2B；動作與價值當潛影格 | **2B** ✅ | LIBERO／RoboCasa／ALOHA | [arXiv:2601.16163](https://arxiv.org/abs/2601.16163) |
| **Dreamer 4** | 潛空間影片 | 因果 tokenizer＋shortcut-forcing 動力學 Transformer | **2B**（tokenizer 400M＋動力學 1.6B）✅ | 2,541 小時 Minecraft（其中 100 小時有動作即可） | [arXiv:2509.24527](https://arxiv.org/abs/2509.24527) |
| **UniSim** | 影片擴散 | Video U-Net，動作經 T5＋CFG 注入 | **5.6B** ✅（512 顆 TPU-v3、20 天） | 多來源混合 | [arXiv:2310.06114](https://arxiv.org/abs/2310.06114) |
| **CoT-VLA** | VLA 內含影像生成 | VILA-U 統一理解／生成模型 | **7B** ✅ | OXE 等 | [arXiv:2503.22020](https://arxiv.org/abs/2503.22020) |
| **Cosmos-Predict1** | 影片擴散／自回歸 | Cosmos tokenizer＋DiT 或 GPT | 擴散 **7B／14B**，自回歸 **4B／12B** | 2,000 萬小時 → 約 1 億段 | [arXiv:2501.03575](https://arxiv.org/abs/2501.03575) |
| **Cosmos-Predict2.5** | flow 影片 | 統一 Text／Image／Video2World | **2B／14B** ✅ | 2 億段影片 | [arXiv:2511.00062](https://arxiv.org/abs/2511.00062) |
| **GAIA-1** | 自回歸＋擴散解碼 | image tokenizer 0.3B＋世界模型 6.5B＋影片解碼器 2.6B | 約 **9.4B** 🧮 | 4,700 小時倫敦行車 | [arXiv:2309.17080](https://arxiv.org/abs/2309.17080) |
| **GAIA-2** | 潛空間 flow | tokenizer（編碼 85M、解碼 200M）＋時空分解 Transformer | 世界模型 **8.4B** ✅ | 約 2,500 萬段 2 秒影片（約 1.4 萬小時 🧮） | [arXiv:2503.20523](https://arxiv.org/abs/2503.20523) |
| **Genie（第一代）** | 自回歸 | 影片 tokenizer＋潛在動作模型＋動力學模型 | **11B** ✅ | 無標註網路影片 | [arXiv:2402.15391](https://arxiv.org/abs/2402.15391) |
| **1X World Model** | 影片擴散＋IDM | 文字條件擴散骨幹＋Depth Anything 式 IDM | 骨幹 **14B** ✅，IDM ❓ | 網路影片＋900 小時人類第一視角＋70 小時 NEO | [1X 官方](https://1x.tech/discover/world-model-self-learning) |
| **τ0-VLA 世界模型** | 影像編輯式 | 由 Step1X-Edit 初始化 | ❓（論文只給 VLM 9B、低階 2B） | 低階策略 40,115 小時 | [arXiv:2608.16885](https://arxiv.org/abs/2608.16885) |
| **WMPO** | 影片擴散 | OpenSora 骨幹＋SDXL 2D VAE | ❓ | OXE 預訓練 | [arXiv:2511.09515](https://arxiv.org/abs/2511.09515) |
| **UniPi** | 影片擴散 | Video U-Net（512 基礎通道）＋時間超解析＋IDM | ❓ | 1,400 萬影片-文字對＋Bridge | [arXiv:2302.00111](https://arxiv.org/abs/2302.00111) |
| **WorldVLA** | 自回歸統一模型 | 由 Chameleon 類模型初始化 | ❓（未核實到確切數字） | LIBERO | [arXiv:2506.21539](https://arxiv.org/abs/2506.21539) |
| **UnifoLM-WMA-0** | 影片＋動作頭 | 影片生成模型微調，程式碼大量沿用 DynamiCrafter | ❓ | Open-X | [GitHub](https://github.com/unitreerobotics/unifolm-world-model-action) |
| **Genie 3／Veo／Tesla／Waymo WM／華為 WE** | 影片生成 | — | ❓ 全部未公開 | — | 見 [08 業界產品盤點](industry.html) |

### 從表上看得出的規律

1. **要放進即時迴圈，就得小或只跑一步**：I1 用 1.5–2B 模型只跑 1 步；I3 用 138M–600M，或 2B 加多 GPU 平行。
2. **要當資料工廠或考官，就用大的**：DreamGen 用 WAN2.1、評估用 Veo、1X 用 14B，因為它們跑在雲端，不受控制頻率限制。
3. **JEPA 用很小的預測器（300M）就能做零樣本規劃**，規劃速度比生成式 Cosmos 快約 15 倍（16 秒對 4 分鐘），但仍遠不到即時。

## 五、給工程師的判斷

- **想低成本加世界模型**：先做 T1（像 FLARE 那樣加一個未來表徵對齊損失）或 T2（DreamGen 式造資料），推論成本零增加。
- **想讓推論也受益**：I1（VPP／GE-Act 式單步特徵）是目前延遲最可控的；I3（候選＋預演＋挑選）在長任務、分布外場景收益最大，但要設計「何時觸發」（像 τ0-VLA 用信心路由）。
- **I2「整個想完再做」目前只適合慢任務**：1X 自己也說 12 秒一輪不適合接觸密集的任務。
