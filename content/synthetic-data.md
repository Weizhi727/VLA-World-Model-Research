# 具身基礎模型與合成資料

<p class="lede">回答兩個追問：「具身基礎模型」到底指什麼、VLA 和世界模型怎麼「融合」；以及用世界模型生成的影片去訓練 VLA 之前，要怎麼確認它符合物理。內容整理自專案的〈起源與歷史〉報告第六、七節（連結見 <a href="references.html#project-outputs">參考資料</a>）。</p>

!!! key "一句話帶走"
    **具身基礎模型 = 同時會「理解、行動、預測後果」的通用預訓練模型。** 目前主流仍是把世界模型當資料工廠，但**生成影片無法保證物理正確**，所以要多層把關，最後以真機成功率驗收。合成資料是補充，不是取代。

## 「具身基礎模型」是什麼

這是對一個趨勢的總稱，不是某個特定模型。業界也叫 **Robot Foundation Model**；NVIDIA 把世界模型那一半叫 **World Foundation Model**。

它指的是：用**網路圖文 + 大量影片 + 機器人資料**預訓練一個通用模型，同時具備三種能力，再微調到不同機器人與任務。概念上就是「機器人版的 GPT」。

<figure class="dg">
<svg viewBox="0 0 800 260" role="img" aria-label="具身基礎模型的三種能力">
<rect class="n" x="20" y="20" width="230" height="90" rx="12"/>
<text x="135" y="55" text-anchor="middle" class="b">理解（VLM）</text>
<text x="135" y="80" text-anchor="middle" class="s">大腦的語言與理解</text>
<rect class="n vla" x="285" y="20" width="230" height="90" rx="12"/>
<text x="400" y="55" text-anchor="middle" class="b vla">行動（VLA 動作專家）</text>
<text x="400" y="80" text-anchor="middle" class="s">小腦的運動控制</text>
<rect class="n wm" x="550" y="20" width="230" height="90" rx="12"/>
<text x="665" y="55" text-anchor="middle" class="b wm">預測後果（世界模型）</text>
<text x="665" y="80" text-anchor="middle" class="s">在腦中預演</text>
<rect class="n key" x="160" y="170" width="480" height="70" rx="12"/>
<text x="400" y="200" text-anchor="middle" class="b">共用同一份預訓練知識</text>
<text x="400" y="222" text-anchor="middle" class="s">網路圖文 + 大量影片 + 機器人資料</text>
<path class="ar" d="M135,110 V140 H330 V168"/>
<path class="ar vla" d="M400,110 V168"/>
<path class="ar wm" d="M665,110 V140 H470 V168"/>
</svg>
<figcaption>過去這三件事是三個研究社群各做各的，現在大家希望它們共用同一份預訓練知識。目前還沒有系統真正把三者統一並同時達到各自的最好水準。</figcaption>
</figure>

## 「融合」的三種做法：由淺到深

| 融合方式 | 怎麼運作 | 代表例子 |
|---|---|---|
| **① 世界模型當「資料工廠」**（兩個模型分開） | 世界模型生成機器人影片 → 用逆動力學模型（IDM）標出動作 → 當 VLA 的訓練資料 | [Cosmos](https://arxiv.org/abs/2501.03575) + [GR00T N1](https://arxiv.org/abs/2503.14734)；[DreamGen](https://arxiv.org/abs/2505.12705) |
| **② 影片預測當「預訓練目標」**（同一個網路） | 先學「下一幀長怎樣」，再學輸出動作；懂世界怎麼變，動作就更容易學 | [GR-1](https://arxiv.org/abs/2312.13139)、[GR-2](https://arxiv.org/abs/2410.06158)；[UniPi](https://arxiv.org/abs/2302.00111) |
| **③ 世界模型當「想像力／評估器」**（在決策迴圈中） | 行動前先模擬幾個候選動作的後果，挑最好的執行；或在模型中評測策略，省下真機測試 | [V-JEPA 2-AC](https://arxiv.org/abs/2506.09985) 用 MPC 規劃抓放；[UniSim](https://arxiv.org/abs/2310.06114) |

**主流仍是 ①**：分開訓練、用資料串接。②、③ 的更多例子與推論代價見〈[訓練時 vs 推論時](train-vs-inference.html)〉。

## 生成影片符合物理嗎？目前無法保證

!!! warn "研究結論：看起來真 ≠ 物理對"
    業界的實際做法是「**多層把關 + 只用在它擅長的地方 + 最終以真機成功率為準**」。

### 學界的診斷

- **[Physics-IQ](https://arxiv.org/abs/2501.09038)**（Google DeepMind，2025）：測 Sora、Runway、Pika、Lumiere 等模型預測流體、力學、光學等真實實驗的結果，發現**視覺逼真度與物理理解幾乎無關**，物理理解普遍很差。
- **[How Far is Video Generation from World Model](https://arxiv.org/abs/2411.02385)**（ByteDance，2024）：在可控 2D 物理場景中訓練，模型在訓練分布內表現好，分布外就失效；它更像「找最像的訓練案例來模仿」，而不是學到物理定律。
- **[VideoPhy](https://arxiv.org/abs/2406.03520)、[PhyGenBench](https://arxiv.org/abs/2410.05363)**：專門評測物理常識的基準，結論類似，加大模型只能部分改善。
- **策略會鑽漏洞**：早在 2018 年 [World Models](https://arxiv.org/abs/1803.10122) 就發現，策略會利用世界模型的錯誤「在夢境中作弊」，模型錯得越多，被利用得越嚴重。

## 業界的四層把關

<figure class="dg">
<svg viewBox="0 0 800 250" role="img" aria-label="合成資料的四層把關流程">
<rect class="n" x="10" y="40" width="175" height="150" rx="12"/>
<text x="97" y="70" text-anchor="middle" class="b">1 生成前</text>
<text x="97" y="96" text-anchor="middle" class="s">用真實資料</text>
<text x="97" y="116" text-anchor="middle" class="s">「拴住」模型</text>
<text x="97" y="150" text-anchor="middle" class="s wm">DreamGen</text>
<rect class="n key" x="210" y="40" width="175" height="150" rx="12"/>
<text x="297" y="70" text-anchor="middle" class="b">2 生成時</text>
<text x="297" y="96" text-anchor="middle" class="s">物理交給模擬器</text>
<text x="297" y="116" text-anchor="middle" class="s">生成只負責外觀</text>
<text x="297" y="150" text-anchor="middle" class="s wm">Cosmos-Transfer1</text>
<text x="297" y="172" text-anchor="middle" class="s">最可靠</text>
<rect class="n" x="410" y="40" width="175" height="150" rx="12"/>
<text x="497" y="70" text-anchor="middle" class="b">3 生成後</text>
<text x="497" y="96" text-anchor="middle" class="s">VLM 裁判、動作可行性</text>
<text x="497" y="116" text-anchor="middle" class="s">幾何與時間一致性</text>
<text x="497" y="150" text-anchor="middle" class="s wm">Cosmos-Reason1</text>
<rect class="n vla" x="610" y="40" width="180" height="150" rx="12"/>
<text x="700" y="70" text-anchor="middle" class="b vla">4 最終驗收</text>
<text x="700" y="96" text-anchor="middle" class="s">加 vs 不加合成資料</text>
<text x="700" y="116" text-anchor="middle" class="s">比較真機成功率</text>
<text x="700" y="150" text-anchor="middle" class="s vla">金標準</text>
<path class="ar" d="M185,115 H208"/>
<path class="ar" d="M385,115 H408"/>
<path class="ar" d="M585,115 H608"/>
<path class="ar dash" d="M700,190 V225 H97 V192"/>
<text x="400" y="242" text-anchor="middle" class="s">真機沒有變好，就回頭調整混合比例或生成條件</text>
</svg>
<figcaption>四層各擋一種錯：生成前擋「憑空亂生」，生成時擋「物理錯」，生成後擋「沒完成指令、物體穿透或消失」，驗收擋「看起來沒問題但其實沒幫助」。</figcaption>
</figure>

### 1 生成前：用真實資料「拴住」模型

先用目標機器人的真實資料微調影片模型，生成時以**真實的第一幀和指令**為條件，而不是從空白生成。[DreamGen](https://arxiv.org/abs/2505.12705)（NVIDIA，CoRL 2025）就是這個流程。

### 2 生成時：讓物理引擎負責物理（目前最可靠）

在 Isaac Sim 等模擬器中跑出物理正確的軌跡，再以深度、分割、邊緣圖為條件，讓生成模型「重新上色」成各種光線、材質、場景。代表是 [Cosmos-Transfer1](https://arxiv.org/abs/2503.14492)。**物理由方程式保證，生成模型只用來縮小 sim2real 的視覺差距。**

### 3 生成後：自動過濾

- **VLM 當裁判**：用專門訓練物理常識推理的模型（如 [Cosmos-Reason1](https://arxiv.org/abs/2503.15558)）或一般 VLM，判斷影片是否完成指令、有沒有物體穿透或消失。DreamGen 也用 VLM 過濾不合格影片。
- **動作可行性檢查**：IDM 從影片推出關節動作後，檢查是否超出關節角度與速度限制；進一步把動作放回模擬器或真機重播，看能否重現影片內容。
- **幾何與時間一致性**：用追蹤、深度估計檢查物體大小、形狀、數量是否前後一致（物體恆存）。

### 4 最終驗收：下游任務才是金標準

做對照實驗：**加入合成資料 vs. 不加**，在真實機器人上比較成功率，並調整真實與合成資料的混合比例。就算有些影片物理不完美，只要真機成功率上升，就表示它有用。

## 實務原則：哪裡適合用合成資料

| 適合用生成影片補充 | 仍需真實資料或物理模擬 |
|---|---|
| **視覺多樣性**：新場景、光線、背景、物體外觀 | **接觸密集、需要精確力**：插入、擰緊、軟物處理 |
| **語意泛化**：新指令、新動詞、新物體類別 | **高速動態**：拋接、平衡 |
| **高層任務順序**與長時程計畫 | **力觸覺**等影片看不到的訊號 |

!!! key "一句話總結"
    把生成式世界模型當成**視覺與語意的放大器**，物理交給模擬器與真實資料把關，再用真機成功率驗收，是目前最穩健的路線。世界模型評測的完整四層指標見〈[訓練、資料與評估](training.html)〉。
