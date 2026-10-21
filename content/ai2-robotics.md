# 案例：智平方 AI² Robotics

<p class="lede">把一家公司的產品線放到前面的分類地圖上逐一對照：它屬於哪個流派、跟競品差在哪裡、訓練方法公開了多少，以及「類腦」這個說法該怎麼看。整理日期 2026-10-19。</p>

!!! note "先釐清名字"
    智平方（深圳，2023 年成立，創辦人郭彥東，前小鵬、OPPO 首席科學家）**與 Allen Institute 的 Ai2 無關**（[The Robot Report](https://www.therobotreport.com/ai2-robotics-raises-series-b-funding-advance-alphabot-embodied-ai/)）。另外，[HybridVLA](https://arxiv.org/abs/2503.10631) 雖然也出自北大張尚彤團隊，但作者名單裡沒有智平方，不算它的產品。

## 重點先講

!!! key "六句話看懂智平方"
    1. **它是「VLA 公司」，不是「世界模型公司」。** 主力是自研 VLA 大腦 AlphaBrain + 輪式人形機器人 AlphaBot 2，軟硬體與場景一起做。
    2. **架構軸：主線是雙系統（快慢腦）**，和 Figure Helix、GR00T N1、π0.5 同一格；GOVLA 的慢系統會輸出語言子任務，落在「雙系統與顯式分層之間」的灰色地帶。
    3. **動作解碼軸：連續（擴散）派**，FiS-VLA 是「慢系統離散 token 訓練 + 快系統擴散出動作」的混合。
    4. **世界模型只當加值模組**：Video2Act 借用影片生成模型的特徵輔助出動作，但**論文本身不產生未來影格、也沒自稱世界模型**；「先預測後執行」是公司行銷說法。
        - **2026-10 補充**：2026-04 開源的 [AlphaBrain 框架](https://github.com/AlphaBrainGroup/AlphaBrain) 已原生整合 Cosmos Policy 權重，支援 V-JEPA 2.1、Cosmos Predict 2／2.5、Wan 2.2 世界模型骨幹切換；但這是研究平台，產品模型是否使用未公開。詳見 [世界模型代表作的實際應用](wm-in-practice.html#_5)。
    5. **NeuroVLA（2026）是分類法之外的新分支**：「大腦／小腦／脊髓」三層類腦架構，下層用神經形態晶片做 20 ms 反射。
    6. **要打折扣**：多數數字是公司或合作論文自報，比較對象多是 π0 而非 π0.5。

## 產品與模型一覽

| 代際 | 模型 | 時間 | 論文 | 一句話 |
|---|---|---|---|---|
| GOVLA 0.0 | **RoboMamba** | 2024 | [arXiv:2406.04339](https://arxiv.org/abs/2406.04339)（NeurIPS 2024） | 用 Mamba 取代 Transformer 骨幹的小型 VLA，強調推理效率 |
| GOVLA 0.5 | **FiS-VLA**（Fast-in-Slow） | 2025-06 | [arXiv:2506.01953](https://arxiv.org/abs/2506.01953)（[NeurIPS 2025](https://neurips.cc/virtual/2025/poster/119931)） | 把快系統「嵌」在慢系統 VLM 的最後幾層裡 |
| GOVLA 1.0 | **GOVLA**（產品版） | 2025 隨 AlphaBot 2 發布 | 無論文，見[官方發布頁](https://ai2robotics.com/en/%E6%99%BA%E5%B9%B3%E6%96%B9%E5%8F%91%E5%B8%83%E5%85%A8%E6%96%B0%E4%B8%80%E4%BB%A3%E6%99%BA%E8%83%BD%E6%9C%BA%E5%99%A8%E4%BA%BAalphabot-2%E5%BC%80%E5%90%AFagi%E7%BB%88%E7%AB%AF%E6%96%B0/) | 全域全身 VLA：空間互動基座 + 慢系統 + 快系統 |
| — | **Video2Act** | 2025-11 | [arXiv:2512.03044](https://arxiv.org/abs/2512.03044) | 用影片擴散模型當慢系統的特徵抽取器 |
| — | **NeuroVLA** | 2026（智源大會發表） | [arXiv:2601.14628](https://arxiv.org/abs/2601.14628) | 大腦／小腦／脊髓三層類腦 VLA，已在 AlphaBrain 平台開源 |

**GOVLA 其實是系列名**（[量子位轉載公司稿](https://www.qbitai.com/2026/02/382004.html)）：0.0 = RoboMamba，0.5 = FiS-VLA，1.0 = 目前 AlphaBot 2 上的產品版（只說「更強大」，無細節）。

**硬體 AlphaBot 2（愛寶）**：輪式雙臂人形，全身 34+ 自由度、腰腿升降、作業高度 0–240 cm、360° 感知、續航 6 小時以上，算力 NVIDIA AGX Orin 64GB（[官方發布頁](https://ai2robotics.com/en/%E6%99%BA%E5%B9%B3%E6%96%B9%E5%8F%91%E5%B8%83%E5%85%A8%E6%96%B0%E4%B8%80%E4%BB%A3%E6%99%BA%E8%83%BD%E6%9C%BA%E5%99%A8%E4%BA%BAalphabot-2%E5%BC%80%E5%90%AFagi%E7%BB%88%E7%AB%AF%E6%96%B0/)、[搜狐](https://www.sohu.com/a/1067022731_100265270)）。

## 最有辨識度的設計：快系統「嵌」在慢系統裡

<figure class="dg">
<svg viewBox="0 0 800 300" role="img" aria-label="一般雙系統與 FiS-VLA 的對比">
<text x="200" y="26" text-anchor="middle" class="h">一般雙系統（π0、GR00T、Helix）</text>
<text x="600" y="26" text-anchor="middle" class="h">FiS-VLA（智平方）</text>
<rect class="n vla" x="60" y="50" width="280" height="90" rx="12"/>
<text x="200" y="88" text-anchor="middle" class="b vla">VLM（慢系統）</text>
<text x="200" y="112" text-anchor="middle" class="s">理解畫面與指令</text>
<rect class="n mix" x="60" y="190" width="280" height="80" rx="12"/>
<text x="200" y="224" text-anchor="middle" class="b">另一個動作模型（快系統）</text>
<text x="200" y="248" text-anchor="middle" class="s">80M～1B，需要從頭學</text>
<path class="ar vla" d="M200,140 V188"/>
<text x="210" y="170" class="s">特徵</text>
<rect class="n vla" x="460" y="50" width="280" height="220" rx="12"/>
<text x="600" y="78" text-anchor="middle" class="b vla">同一個 7B VLM</text>
<rect class="n ghost" x="485" y="92" width="230" height="34" rx="6"/>
<text x="600" y="114" text-anchor="middle" class="s">前面各層：慢系統推理（低頻）</text>
<rect class="n ghost" x="485" y="134" width="230" height="34" rx="6"/>
<text x="600" y="156" text-anchor="middle" class="s">⋯</text>
<rect class="n key" x="485" y="190" width="230" height="64" rx="8"/>
<text x="600" y="216" text-anchor="middle" class="b">最後 2 層 = 快系統</text>
<text x="600" y="238" text-anchor="middle" class="s">+ 點雲、機器人狀態，擴散出動作</text>
<path class="ar" d="M600,168 V188"/>
</svg>
<figcaption>FiS-VLA 的快系統共享 VLM 自己的權重，所以直接繼承預訓練知識。慢:快 = 1:4，4090 上 action chunk = 8 時達 117.7 Hz。資料來源：<a href="https://arxiv.org/abs/2506.01953">FiS-VLA arXiv:2506.01953</a>。</figcaption>
</figure>

## 逐一對照分類法

### RoboMamba：單系統

- **架構軸**：單一系統，一個模型理解並輸出動作。
- **特色**：骨幹換成 Mamba（狀態空間模型），公司稱規模約谷歌同類模型的 1/20。屬於「效率優化」路線，不是新流派。

### GOVLA：雙系統，偏「語言子任務」灰色地帶

- **架構軸**：雙系統。慢系統負責推理與任務拆解並**輸出語言**，快系統輸出全身控制動作與底盤移動軌跡。
- **中間表徵軸**：語言子任務，和 π0.5、Gemini Robotics 1.5 一樣，介於雙系統與顯式分層之間。
- **差異化**：公司宣稱傳統 VLA 只輸出手臂動作，GOVLA 同時輸出**全身 + 移動軌跡**。這是「動作空間」的擴展，不是新派別。
- **限制**：沒有論文，解碼方式與頻率未揭露，這一格是依官方描述推論。

### FiS-VLA：雙系統 + 混合解碼（技術含量最高）

- **架構軸**：雙系統，但**直接拿 7B VLM 的最後兩層 Transformer 當快系統**（見上圖）。
- **動作解碼軸**：混合式。慢系統用離散 token 的 next-token loss 訓練，快系統用擴散生成連續動作。
- **異步雙頻**：慢:快 = 1:4，快系統額外吃 3D 點雲與機器人狀態。

| 設定 | FiS-VLA | π0 | CogACT |
|---|---|---|---|
| RLBench 10 任務成功率 | **69%** | 55% | 61% |
| AgileX 真機 | **68%** | 59% | — |
| AlphaBot 真機 | **74%** | 61% | — |
| 未見物體時成功率下降（AlphaBot） | **−19%** | −38% | — |

### Video2Act：雙系統 +「借世界模型的眼睛」

- **架構軸**：雙系統。慢系統是騰訊混元影片擴散模型（只取前 25 層當特徵抽取器），快系統是 1B 擴散 Transformer 動作專家，頻率比 1:8。
- **動作解碼軸**：擴散（DiT 去噪 action chunk，長度 64）。
- **世界模型軸**：借用的是**影片生成式世界模型**的預訓練表徵，**但不生成未來畫面、不用想像做規劃**。在分類法裡屬於「把世界模型當加值模組／感知骨幹」。公司說的「世界模型內生、先預測後執行」比論文本身說得更強，引用時要注意。
- **論文結果**：RoboTwin 1.0／2.0 平均 54.6%／54.1%；真機 6 任務 73.3%；宣稱比既有 SOTA 在模擬高 8.9%、真機高 21.7%。

### NeuroVLA：分類法之外的「類腦三層」

<figure class="dg">
<svg viewBox="0 0 800 280" role="img" aria-label="NeuroVLA 三層架構">
<rect class="n vla" x="20" y="40" width="230" height="130" rx="12"/>
<text x="135" y="72" text-anchor="middle" class="b vla">大腦皮層</text>
<text x="135" y="98" text-anchor="middle" class="s">Qwen-VL（GPU）</text>
<text x="135" y="120" text-anchor="middle" class="s">理解語言與畫面</text>
<text x="135" y="142" text-anchor="middle" class="s">產生抽象目標</text>
<rect class="n mix" x="285" y="40" width="230" height="130" rx="12"/>
<text x="400" y="72" text-anchor="middle" class="b">小腦</text>
<text x="400" y="98" text-anchor="middle" class="s">GRU + FiLM 調變</text>
<text x="400" y="120" text-anchor="middle" class="s">每秒讀感測器數百次</text>
<text x="400" y="142" text-anchor="middle" class="s">平滑、修正誤差</text>
<rect class="n key" x="550" y="40" width="230" height="130" rx="12"/>
<text x="665" y="72" text-anchor="middle" class="b">脊髓</text>
<text x="665" y="98" text-anchor="middle" class="s">LIF 脈衝神經網路</text>
<text x="665" y="120" text-anchor="middle" class="s">FPGA 神經形態處理器</text>
<text x="665" y="142" text-anchor="middle" class="s">事件驅動的反射</text>
<path class="ar" d="M250,105 H283"/>
<path class="ar" d="M515,105 H548"/>
<text x="135" y="200" text-anchor="middle" class="s">規劃</text>
<text x="400" y="200" text-anchor="middle" class="s">穩定、修正</text>
<text x="665" y="200" text-anchor="middle" class="s">反射約 20 ms、約 0.4 W</text>
<text x="400" y="250" text-anchor="middle" class="s">三層中只有脊髓層是真正的脈衝神經元 + 神經形態硬體；整套用行為克隆端到端訓練</text>
</svg>
<figcaption>資料來源：<a href="https://arxiv.org/abs/2601.14628">NeuroVLA arXiv:2601.14628</a>、<a href="https://www.sohu.com/a/1033666912_114822">搜狐四代演進整理</a>。</figcaption>
</figure>

- **怎麼歸類**：
    - 層與層之間傳的是抽象目標與控制訊號，不是人看得懂的子任務，所以**不是**綜述定義的「顯式分層」。
    - 比較像「雙系統再往下多加一層控制」，下兩層借鏡生物神經系統而非傳統控制。
    - 建議在兩軸地圖上把它標為**「三系統／類腦」新分支**，和同期的 [SaiVLA-0](https://arxiv.org/html/2603.08124)、[CereVLA](https://arxiv.org/abs/2609.27468) 歸成一類趨勢。
- **宣稱結果**：碰撞反射約 20 ms（傳統 VLA 超過 200 ms）、抖動降低 75% 以上、脊髓層功耗約 0.4 W、碰撞後任務恢復成功率 54.8%（傳統模型 0%）。

### 總表：放到分類地圖上

| 模型 | 架構軸 | 動作解碼軸 | 中間表徵軸 | 世界模型 |
|---|---|---|---|---|
| RoboMamba | 單系統 | 簡單策略頭 | 原始動作 | 無 |
| GOVLA | 雙系統（偏分層灰區） | 未公開 | 語言子任務 | 無 |
| FiS-VLA | 雙系統（快嵌於慢） | 混合（離散訓練 + 擴散輸出） | 潛向量 | 無 |
| Video2Act | 雙系統 | 擴散 | 潛向量（影片模型特徵） | 借用影片生成式表徵 |
| NeuroVLA | 三層類腦（新分支） | 未詳述 | 抽象目標 + 控制訊號 | 無 |

三條軸的定義見〈[VLA 流派怎麼分](vla-taxonomy.html)〉。

## 對照競品：大模型、小模型各多大

| 公司／模型 | 架構軸 | 大模型（慢／理解） | 小模型（快／動作） | 動作解碼 | 頻率 | 來源 |
|---|---|---|---|---|---|---|
| **智平方 FiS-VLA** | 雙系統（快系統嵌在 VLM 內） | LLaMA2 **7B**（Prismatic VLM，SigLIP + DINOv2） | 同一 LLM 的**最後 2 層**（參數量未公開） | 混合 | 慢:快 = 1:4；117.7 Hz | [arXiv:2506.01953](https://arxiv.org/abs/2506.01953) |
| **智平方 Video2Act** | 雙系統 | HunyuanVideo 前 25／60 層（全模型 **13B**，[arXiv:2412.03603](https://arxiv.org/abs/2412.03603)；截取部分未公開） | **1B** DiT | 擴散 | 慢:快 = 1:8 | [arXiv:2512.03044](https://arxiv.org/abs/2512.03044) |
| **智平方 NeuroVLA** | 三層類腦 | Qwen-VL（尺寸未公開） | 小腦 GRU；脊髓 LIF SNN 跑在 FPGA（參數量未公開） | 未詳述 | 脊髓單次推論 2.19 ms、約 0.4 W | [arXiv:2601.14628](https://arxiv.org/abs/2601.14628) |
| **智平方 RoboMamba** | 單系統 | Mamba **2.7B**（全模型約 3.2B），CLIP ViT-L | MLP 策略頭 **3.7M** | 直接回歸末端位姿 | — | [arXiv:2406.04339](https://arxiv.org/abs/2406.04339) |
| **智平方 GOVLA 1.0** | 雙系統（慢系統出語言子任務） | 未公開 | 未公開 | 未公開 | 未公開 | 官方發布頁 |
| Physical Intelligence π0 | 雙系統（同一 Transformer） | PaliGemma **3B** | 動作專家約 **300M**（共約 3.3B） | flow matching | 最高 50 Hz，chunk = 50 | [arXiv:2410.24164](https://arxiv.org/abs/2410.24164) |
| Figure Helix | 雙系統 | VLM **7B**，7–9 Hz | 視覺運動 Transformer **80M** | 連續輸出（未細說） | 200 Hz | [Figure 部落格](https://www.figure.ai/news/helix) |
| NVIDIA GR00T N1 | 雙系統 | Eagle-2 VLM **1.34B**（取第 12 層特徵） | DiT 動作頭（全模型約 **2.2B**） | flow matching | 慢 10 Hz、快 120 Hz | [arXiv:2503.14734](https://arxiv.org/abs/2503.14734) |
| 智元 AgiBot GO-1 | 分層（VLM → 潛在規劃器 → 動作專家） | InternVL2.5-**2B** | 24 層潛在規劃器 + 動作專家（未公開） | 擴散，chunk = 30 | — | [arXiv:2503.06669](https://arxiv.org/abs/2503.06669) |
| Gemini Robotics 1.5 | 雙模型，偏顯式分層 | 未公開 | 未公開 | 未公開 | — | [arXiv:2510.03342](https://arxiv.org/abs/2510.03342) |

**怎麼讀這張表**

- **同一格的對手**：智平方主線（FiS-VLA、Video2Act、GOVLA）和 π0、Helix、GR00T N1 都是雙系統。
- **差別在快系統怎麼接**：π0、GR00T、Helix 是「VLM + **另外一個**動作模型」；FiS-VLA 是「**拆 VLM 自己的最後幾層**當快系統」。
- **跟 GO-1、Gemini Robotics 的差別**：這兩家中間多了一層明確的規劃介面（潛在動作／語言子任務），更接近顯式分層。
- **NeuroVLA 沒有可比對手**：主流公司裡沒人把脈衝神經網路與神經形態晶片放進 VLA 量產路線。

## 怎麼訓練的（只寫查得到的）

### FiS-VLA（訓練細節最完整）

1. **初始化**：載入 Prismatic VLM 權重，沿用 CogACT、OpenVLA 的做法。
2. **大規模預訓練**：Open X-Embodiment、DROID、RoboMIND 等**超過 86 萬條軌跡**，5 個 epoch。這些資料沒有子任務語言標註，所以慢系統先用**離散動作 token** 監督。
3. **微調**：真機每任務 **100 條**主從遙操作示範（AgileX 與 AlphaBot 各 4 個任務），RLBench 10 任務各 100 條。慢系統額外加入人工標註的子任務規劃語言再自動擴增。模擬微調用 8 張 A800、300 epoch。
4. **損失**：快系統擴散去噪損失 + 慢系統 next-token 損失，**聯合訓練**。論文說只訓練快系統會讓慢系統的推理能力災難性遺忘；訓練時刻意讓慢系統更新得較慢，讓快系統學會用「較舊」的慢系統輸出，模擬部署時的異步。
5. **未公開**：預訓練 GPU 數與時數、哪些層被凍結。

### Video2Act

- 慢系統用現成 HunyuanVideo 抽特徵，快系統是 1B DiT，標準擴散噪聲預測損失。
- 資料：模擬每任務 100 條示範；真機 6 任務，每任務 100 條遙操作示範。
- **未公開**：影片模型是否凍結、DiT 是否另外預訓練、預訓練資料、算力與步數。

### NeuroVLA

- 從預訓練 Qwen-VL 出發，整套系統端到端用**行為克隆**訓練。
- 脈衝神經網路在 GPU 上用 **surrogate gradient** 訓練，不是從一般神經網路轉換，也不是在晶片上學習。
- 下游只用「**數百筆**」樣本微調，在 LIBERO 模擬基準評測。
- **未公開**：資料集名稱、示範數量、精確損失形式。

### RoboMamba

1. 對齊預訓練：LLaVA 558K 圖文對，只訓練投影層。
2. 指令共訓：LLaVA-1.5 655K + 約 30 萬筆 RoboVQA，訓練投影層與 Mamba。
3. 操作微調：SAPIEN 20 個任務、1 萬張圖，**只訓練 3.7M 參數的策略頭**，單張 A100 幾十分鐘。

### GOVLA 1.0 產品：只有方向性說法

- 公司稿稱冷啟動資料來自「互聯網、仿真與真機融合數據」，規模化部署後以真實作業場景資料為主，形成資料閉環（[量子位](https://www.qbitai.com/2026/02/382004.html)）。
- 公司稱為 RoboCOIN 雙臂資料集最大貢獻者（佔比超過 35%、50 多個場景），並使用千卡級算力叢集。
- **未公開**：參數量、資料總量、是否用強化學習、訓練階段。網路上沒有可靠來源，這裡不推測。

## 優勢與要打折扣的地方

| 優勢 | 說明 |
|---|---|
| **快系統設計最有辨識度** | 快系統共享 VLM 權重；AlphaBot 遇到未見物體，成功率只掉 19%，π0 掉 38% |
| **控制頻率屬第一梯隊** | 117.7 Hz 介於 GR00T N1（120 Hz）與 π0（50 Hz）之間，但 Helix 200 Hz 更高；量測硬體不同，只能粗略比 |
| **全身加移動** | GOVLA 1.0 號稱輸出全身與底盤軌跡；Gemini Robotics 2、Helix 02 也在做，算**跟上**一線而非獨家 |
| **安全反射路線獨特** | NeuroVLA 是主流公司中唯一把神經形態晶片做進 VLA 的 |
| **落地速度** | 惠科三年 1,000 台以上框架協議（約人民幣 5 億元）；部署於東風柳汽、半導體廠、無菌車間；自建產線年產能 2,000 台以上，規劃擴到 2–3 萬台（[Gasgoo](https://autonews.gasgoo.com/articles/news/ai-robotics-releases-worlds-first-brain-inspired-embodied-intelligence-system-neurovla-2066466738265505793)） |
| **資金** | 2026-02 B 輪系列超過人民幣 10 億元（百度、中車參投）；2026-06 再融約 50 億元、估值超過 200 億元（[搜狐](https://www.sohu.com/a/1067022731_100265270)） |

!!! warn "要打折扣的地方"
    - **數字多為自報**：「每台年省 45 萬元、1.5 年回本」只來自單一客戶；框架協議不等於已認列營收。
    - **比較基線偏舊**：主要對比 π0 與 CogACT，沒對比 π0.5、GR00T N1.5。
    - **預訓練規模公開得少**：π0 有 1 萬小時以上、GR00T 約 5 萬 H100 GPU 小時、GO-1 百萬條軌跡都有公開。
    - **GOVLA 沒有論文**，產品主力模型無法獨立驗證。
    - **部分中文媒體有業配色彩**（如[這篇](https://www.ithome.com/0/927/850.htm)），本整理不以其為依據。
    - **「世界模型」用語偏寬**：Video2Act 只是借用影片模型特徵，不應與 Cosmos、Genie、V-JEPA 2 並列。

## 「類腦」怎麼認定：數位果蠅 vs NeuroVLA

### 三個常被混用的詞

| 詞 | 意思 | 判斷標準 |
|---|---|---|
| **SNN（脈衝神經網路）** | 一種**神經元模型**：累積膜電位、超過閾值就放電送出離散脈衝 | 神經元是否用脈衝傳訊，例如 LIF（漏積分放電）模型 |
| **全腦仿真（brain emulation）** | 把**某個真實大腦的接線圖**照搬到電腦裡跑 | 結構是否來自真實生物的連接組（connectome） |
| **類腦啟發（brain-inspired）** | 借用大腦的**分工概念或計算方式**設計 AI | 寬鬆，只要有生物學對應就常被這樣稱呼 |

三者可以重疊，但不互相包含：SNN 不一定是全腦仿真，全腦仿真也可以不用 SNN。

### 數位果蠅算 SNN 嗎？要看是哪一隻

| 專案 | 大腦用什麼模型 | 是 SNN 嗎 |
|---|---|---|
| **Shiu 等人的果蠅全腦模型**（[Nature 2024](https://www.nature.com/articles/s41586-024-07763-9)） | 依 FlyWire 連接組建出約 **13.9 萬個 LIF 神經元**、5,000 多萬個突觸 | ✅ 是 |
| **Eon Systems 2026/03 的「數字果蠅」**（[新浪科技](https://finance.sina.com.cn/tech/roll/2026-03-09/doc-inhqksxq3976477.shtml)） | 沿用 Shiu 的 LIF 全腦模型，接上 NeuroMechFly v2 虛擬身體，在 MuJoCo 裡跑 | ✅ 大腦是 SNN 且是全腦仿真；但腦到身體的接口是人工橋接 |
| **Janelia + DeepMind flybody**（[Nature 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12310536/)） | 深度強化學習訓練的一般神經網路控制虛擬身體 | ❌ 不是，它是「數位果蠅身體」而非「大腦」 |

Eon 那隻的批評：所有神經元共用同一組參數、權重凍結不學習、「行為準確率 91%」未經同行評審。

### NeuroVLA 算「類腦」嗎？算「類腦啟發」，不算「仿腦」

**支持的理由**：脊髓層真的是 LIF 脈衝神經元，跑在 FPGA 神經形態處理器上（單次推論 2.19 ms、約 0.87 mJ），符合「類腦計算」最嚴格的技術定義；三層分工在神經科學上也有依據。

**不能說成「仿腦」的理由**：大腦層是一般 Transformer（Qwen-VL）；小腦層是 GRU，沒有模仿浦肯野細胞等真實迴路；整套靠反向傳播訓練，論文自己把線上 STDP 列為未來工作；沒有任何連接組成分。

!!! key "一句話對照"
    **數位果蠅**：結構照抄真實大腦、**不訓練**、神經元用 SNN，是「仿腦」。**NeuroVLA**：功能分工借鏡大腦、**靠資料訓練**、只有最底層用 SNN，是「類腦啟發的混合架構」。Figure Helix 02 也是三層卻沒自稱類腦；真正的技術差異在**有沒有用脈衝神經元與神經形態硬體**。
