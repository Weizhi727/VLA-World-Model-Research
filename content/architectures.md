# 主流模型架構：VLA 四條路線、世界模型四條路線

<p class="lede">VLA 的路線差在「動作怎麼表示、怎麼生成」；世界模型的路線差在「在哪個空間預測未來」。兩邊的交集是「融合世界模型的預測式 VLA」，也是目前最活躍的方向。</p>

!!! key "一句話結論"
    2026 年的 VLA 已收斂到「**預訓練 VLM 骨幹＋連續動作生成頭（flow matching／擴散）＋動作分塊**」，並往**雙系統分層**與**融合世界模型**演進。世界模型分成「**潛空間動力學**（給 RL、規劃用）」與「**像素空間影片生成**（給模擬、造資料用）」兩大陣營，**JEPA** 與 **3D 空間模型**是兩條快速成長的支線。

!!! warn "閱讀提醒：這四條路線不是同一層級的四選一"
    本頁沿用專案最初整理的「四條路線」講法，方便入門。但嚴格來說，路線一、二屬於「動作解碼」軸，路線三屬於「系統架構」軸，路線四屬於「中間表徵」軸，一個模型可以同時屬於好幾條。另外，綜述定義下的「顯式分層」派（規劃器輸出可解釋的子任務或關鍵點，再交給低階策略）在這裡只以 Hi Robot 帶過。更精確的分類請看 [03 流派怎麼分](taxonomy.html)。

## VLA 四條路線一張圖

<figure class="dg">
<svg viewBox="0 0 800 400" role="img" aria-label="VLA 四條路線的資料流">
<text x="10" y="30" class="b vla">① 離散 token</text>
<rect class="n" x="140" y="10" width="120" height="36" rx="8"/><text x="200" y="33" text-anchor="middle">影像＋指令</text>
<rect class="n vla" x="290" y="10" width="140" height="36" rx="8"/><text x="360" y="33" text-anchor="middle" class="b">VLM（LLM）</text>
<rect class="n" x="460" y="10" width="160" height="36" rx="8"/><text x="540" y="33" text-anchor="middle">逐一輸出動作 token</text>
<rect class="n" x="650" y="10" width="140" height="36" rx="8"/><text x="720" y="33" text-anchor="middle">反量化成動作</text>
<path class="ar" d="M260,28 H288"/><path class="ar" d="M430,28 H458"/><path class="ar" d="M620,28 H648"/>
<text x="10" y="54" class="s">RT-2、OpenVLA、π0-FAST</text>
<text x="10" y="120" class="b vla">② 連續動作專家</text>
<rect class="n" x="140" y="100" width="120" height="36" rx="8"/><text x="200" y="123" text-anchor="middle">影像＋指令</text>
<rect class="n vla" x="290" y="100" width="140" height="36" rx="8"/><text x="360" y="123" text-anchor="middle" class="b">VLM 骨幹</text>
<rect class="n vla" x="460" y="100" width="160" height="36" rx="8"/><text x="540" y="123" text-anchor="middle" class="b">flow／擴散動作專家</text>
<rect class="n" x="650" y="100" width="140" height="36" rx="8"/><text x="720" y="123" text-anchor="middle">動作塊（16–50 步）</text>
<path class="ar" d="M260,118 H288"/><path class="ar" d="M430,118 H458"/><path class="ar" d="M620,118 H648"/>
<text x="10" y="144" class="s">π0、SmolVLA、CogACT（目前主流）</text>
<text x="10" y="210" class="b vla">③ 雙系統</text>
<rect class="n" x="140" y="190" width="120" height="36" rx="8"/><text x="200" y="213" text-anchor="middle">影像＋指令</text>
<rect class="n vla" x="290" y="176" width="140" height="64" rx="8"/><text x="360" y="202" text-anchor="middle" class="b">慢腦 VLM</text><text x="360" y="222" text-anchor="middle" class="s">約 1–10 Hz</text>
<rect class="n key" x="460" y="190" width="160" height="36" rx="8"/><text x="540" y="213" text-anchor="middle">潛向量或子任務文字</text>
<rect class="n vla" x="650" y="176" width="140" height="64" rx="8"/><text x="720" y="202" text-anchor="middle" class="b">快腦視動策略</text><text x="720" y="222" text-anchor="middle" class="s">100–200 Hz</text>
<path class="ar" d="M260,208 H288"/><path class="ar" d="M430,208 H458"/><path class="ar" d="M620,208 H648"/>
<text x="10" y="234" class="s">Helix、GR00T N1、π0.5</text>
<text x="10" y="310" class="b mix">④ 預測式</text>
<rect class="n" x="140" y="290" width="120" height="36" rx="8"/><text x="200" y="313" text-anchor="middle">影像＋指令</text>
<rect class="n mix" x="290" y="290" width="140" height="36" rx="8"/><text x="360" y="313" text-anchor="middle" class="b">預測模型</text>
<rect class="n wm" x="460" y="276" width="160" height="64" rx="8"/><text x="540" y="302" text-anchor="middle" class="b">未來畫面</text><text x="540" y="322" text-anchor="middle" class="s">或潛在動作</text>
<rect class="n" x="650" y="290" width="140" height="36" rx="8"/><text x="720" y="313" text-anchor="middle">反推動作</text>
<path class="ar" d="M260,308 H288"/><path class="ar" d="M430,308 H458"/><path class="ar wm" d="M620,308 H648"/>
<text x="10" y="334" class="s">UniPi、GR-2、LAPA、CoT-VLA</text>
<text x="400" y="385" text-anchor="middle" class="s">橘色＝路線三中間的介面；綠色＝路線四中間的「想像」</text>
</svg>
<figcaption>四條路線的資料流比較。路線二是 2025 年後前沿 VLA 的共同設計；路線三是路線二在人形機器人上的延伸；路線四是 VLA 與世界模型的交會點。</figcaption>
</figure>

## VLA 路線一：離散動作 token 自回歸

**核心想法：把動作當成另一種語言。** 將每個關節或末端位姿的連續值切成 256 個區間（bin），每個區間對應詞表中的一個 token，VLM 以「預測下一個 token」的方式輸出動作。好處是完全沿用 LLM 的訓練與推論管線，網路規模的視覺語言知識能直接遷移。

**典型資料流**：影像 → 視覺編碼器（SigLIP／DINOv2）→ 投影層 → LLM（與語言指令一起）→ 逐一輸出 7 個動作 token（xyz、旋轉、夾爪）→ 反量化成連續動作。

- [RT-2](https://arxiv.org/abs/2307.15818)（Google DeepMind, 2023）：PaLI-X／PaLM-E 骨幹，首次證明「網路資料＋機器人資料」共訓可帶來語意泛化。
- [OpenVLA](https://arxiv.org/abs/2406.09246)（Stanford 等, 2024）：7B，Llama 2＋DINOv2 與 SigLIP 雙視覺編碼器，在 Open X-Embodiment 約 97 萬條軌跡上訓練，是開源 VLA 的基準線。
- [FAST tokenizer／π0-FAST](https://arxiv.org/abs/2501.09747)（Physical Intelligence, 2025）：先對動作序列做 DCT（離散餘弦轉換）再用 BPE 壓縮，一段高頻動作只需少量 token，解決逐維分箱在高頻控制下 token 爆量的問題。
- [OpenVLA-OFT](https://arxiv.org/abs/2502.19645)（2025）：改用平行解碼＋動作分塊＋連續 L1 迴歸，推論速度提升約 25 到 50 倍，說明這條路線正往「非逐 token」修正。

**優點**：架構最簡單、可直接用 LLM 生態（量化、KV cache、RLHF）。**弱點**：**逐 token 解碼慢**（OpenVLA 原版約 5 Hz），**離散化損失精度**，難以表達多峰動作分布，所以靈巧、高頻任務多半轉向路線二。

## VLA 路線二：VLM 骨幹＋連續動作專家（目前主流）

**核心想法：VLM 負責「看懂與想」，另一個小網路負責「生成連續動作」。** 動作頭通常用 **flow matching** 或**擴散模型**，一次輸出一整塊未來動作（**action chunk**，常見 16 到 50 步），以少數去噪步得到平滑、多峰的動作分布。

**關鍵細節**

- **動作專家怎麼讀 VLM**：π0 類做法是動作專家與 VLM **共用同一個 Transformer 的注意力**（類 MoE 的兩組權重），動作 token 可以注意到所有影像與語言 token；CogACT／GR00T 類則**只拿 VLM 的輸出特徵做 cross-attention 條件**。
- **flow matching vs 擴散**：flow matching 學的是從噪聲到動作的**直線速度場，約 10 步積分即可**，延遲比 DDPM 低很多，因此成為首選。
- **知識絕緣（knowledge insulation）**：隨機初始化的動作頭回傳的梯度會破壞 VLM 原本的知識。[π0.5＋KI](https://arxiv.org/abs/2505.23705) 的解法是讓 VLM 用 FAST 離散 token 訓練、動作專家用 flow matching 訓練，並阻斷動作專家對 VLM 的梯度，兼得訓練快與推論快。

**代表模型**

- [π0](https://arxiv.org/abs/2410.24164)（Physical Intelligence, 2024）：PaliGemma 3B＋約 3 億參數的動作專家，flow matching 輸出 50 步動作塊，可達 50 Hz，展示摺衣服、收桌子等長程靈巧任務。[openpi 開源](https://github.com/Physical-Intelligence/openpi)。
- [SmolVLA](https://arxiv.org/abs/2506.01844)（Hugging Face, 2025）：約 4.5 億參數，用 SmolVLM2 的前半層＋flow matching 動作專家，支援非同步推論，消費級 GPU 可跑，是 LeRobot 生態的入門首選。
- [CogACT](https://arxiv.org/abs/2411.19650)（微軟等, 2024）：VLM 輸出一個「認知 token」，再條件化一個擴散 Transformer 動作模組。
- [RDT-1B](https://arxiv.org/abs/2410.07864)（清華, 2024）：純擴散 Transformer 的雙臂基礎模型，用「統一動作空間」容納不同機器人的自由度。
- [Octo](https://arxiv.org/abs/2405.12213)（2024）與 [Diffusion Policy](https://arxiv.org/abs/2303.04137)（2023）是前身：還沒有大型 VLM，但已確立「擴散頭＋動作分塊」的有效性。

**為何成為主流**：連續動作精度高、能表達多峰分布、動作塊讓控制頻率與 VLM 推論頻率解耦。代價是訓練更複雜，而且要處理知識絕緣問題。

## VLA 路線三：雙系統（慢腦＋快腦）

**核心想法：借用康納曼的 System 2（慢思考）與 System 1（快反應）。** 大型 VLM 以低頻（約 1 到 10 Hz）做場景理解、任務拆解、產生潛在指令；小型視動策略以高頻（100 到 200 Hz）輸出關節指令。兩個系統**非同步運行**，特別適合**全身人形機器人**。

中間的介面有兩種：**潛在向量介面**（S2 輸出嵌入向量給 S1，可端到端微分）與**語言介面**（高層輸出「拿起海綿」這類子任務文字，低層 VLA 執行，可解釋、可插入人類糾正）。

- [Helix](https://www.figure.ai/news/helix)（Figure AI, 2025）：S2 為 7B VLM，約 7 到 9 Hz；S1 為約 8,000 萬參數的視動 Transformer，200 Hz 控制人形上半身 35 個自由度，兩者以潛在向量連接。
- [GR00T N1](https://arxiv.org/abs/2503.14734)（NVIDIA, 2025）：S2 為 Eagle-2 VLM，S1 為 flow matching 的 DiT 動作模組；訓練資料金字塔結合真實遙控、模擬與人類影片。[Isaac-GR00T 開源](https://github.com/NVIDIA/Isaac-GR00T)。
- [Gemini Robotics](https://arxiv.org/abs/2503.20020)（Google DeepMind, 2025）：雲端 Gemini 骨幹＋本地動作解碼器；另有 Gemini Robotics-ER 專司具身推理。[Gemini Robotics 1.5](https://arxiv.org/abs/2510.03342) 加入「行動前先思考」與跨機體動作遷移。
- [π0.5](https://arxiv.org/abs/2504.16054)（Physical Intelligence, 2025）：同一個模型先用文字預測高層子任務，再用動作專家輸出低層動作，搭配網路、多機體與語意標註的異質共訓，能在沒見過的家中清理。
- [Hi Robot](https://arxiv.org/abs/2502.19417)（2025）：高層 VLM 處理開放式指令與即時口頭糾正，輸出語言指令給低層 π0。這是「顯式分層」派的代表。

**取捨**：潛在介面反應最快、整體可端到端調整；語言介面最易除錯與人機協作，但子任務粒度要設計。

!!! note "命名陷阱"
    業界常把 Helix、GR00T N1 這種「慢想快做」叫做「分層」。但在 [arXiv:2508.13073](https://arxiv.org/abs/2508.13073) 綜述的定義下，它們屬於**雙系統的端到端模型**，因為兩個系統之間傳的是潛向量，不是人看得懂的東西。詳見 [03 流派怎麼分](taxonomy.html)。

## VLA 路線四：融合世界模型的預測式 VLA

**核心想法：先想像「世界接下來會變成什麼」，再決定動作。** 好處是可以用大量**沒有動作標註的人類影片**預訓練，緩解機器人資料稀缺。依「預測什麼」分三類：

1. **預測未來影像，再反推動作（逆動力學）**
    - [UniPi](https://arxiv.org/abs/2302.00111)（2023）：文字條件影片生成模型當規劃器，再用逆動力學模型從相鄰幀解出動作。
    - [GR-1](https://arxiv.org/abs/2312.13139)／[GR-2](https://arxiv.org/abs/2410.06158)（ByteDance）：GPT 式 Transformer 同時預測未來影像與動作，GR-2 先在約 3,800 萬段網路影片上預訓練。
    - [Seer](https://arxiv.org/abs/2412.15109)（2024）與 [VPP](https://arxiv.org/abs/2412.14803)（2024）：前者端到端「預測式逆動力學」，後者直接拿影片擴散模型的中間特徵當策略表徵。
    - [CoT-VLA](https://arxiv.org/abs/2503.22020)（2025）：「視覺思維鏈」，先生成子目標影像，再輸出到達該狀態的動作序列。
2. **學「潛在動作」，從無標註影片預訓練**
    - [LAPA](https://arxiv.org/abs/2410.11758)（2024）：用 VQ-VAE 從前後幀差異學出離散潛在動作，先訓練 VLA 預測潛在動作，再用少量真實資料對應到關節動作。想法源自 Genie 的潛在動作模型。
    - [UniVLA](https://arxiv.org/abs/2505.06111)（2025）：在 DINOv2 特徵空間學「任務中心」的潛在動作，濾掉與任務無關的相機晃動。
3. **影像與動作在同一個模型中聯合生成**
    - [WorldVLA](https://arxiv.org/abs/2506.21539)（2025）：自回歸模型同時學「世界模型」（給動作預測影像）與「動作模型」（給影像預測動作），兩者互相提升。
    - [UVA](https://arxiv.org/abs/2503.00200)（2025）：影片與動作共用潛在表示、各自擴散解碼，推論時可跳過影片解碼以提速。
    - [Genie Envisioner](https://arxiv.org/abs/2508.05635)（AgiBot, 2025）：以影片擴散為核心，把策略學習、模擬評估統一在同一個世界模型平台。

**取捨**：預測像素昂貴、會拖慢控制迴圈，所以越來越多工作**只在訓練時預測未來（當輔助目標），推論時只用其表徵**。細節見 [06 訓練時 vs 推論時](train-vs-inference.html)。

## VLA 代表模型比較

依發表時間新到舊排列。

!!! warn "數字可信度"
    這張表來自專案早期的架構整理，當時部分控制頻率是近似值，未逐篇開原文核對（尤其 Gemini Robotics 的頻率）。π0、GR00T N1、Helix、RoboMamba 等的參數量後來在 [09 案例：智平方](ai2-robotics.html) 的競品表中已回到論文核對過，以那張表為準。

| 模型 | 路線 | VLM 骨幹 | 動作表示／生成 | 控制頻率 | 開源 |
|---|---|---|---|---|---|
| [Gemini Robotics 1.5](https://arxiv.org/abs/2510.03342) | 三 | Gemini | 動作解碼器＋先思考再行動 | 未公開 | 否 |
| [SmolVLA](https://arxiv.org/abs/2506.01844) | 二 | SmolVLM2（全模型約 4.5 億） | flow matching 動作塊 | 非同步推論 | 是 |
| [π0.5](https://arxiv.org/abs/2504.16054) | 三 | PaliGemma | 文字子任務＋flow matching | 約 50 Hz | 是（openpi） |
| [GR00T N1](https://arxiv.org/abs/2503.14734) | 三 | Eagle-2 | DiT flow matching | 約 120 Hz | 是 |
| [Gemini Robotics](https://arxiv.org/abs/2503.20020) | 三 | Gemini 2.0 | 雲端骨幹＋本地解碼 | 約 50 Hz（未核對） | 否 |
| [Helix](https://www.figure.ai/news/helix) | 三 | 7B VLM | 潛在向量 → 80M 視動策略 | 200 Hz | 否 |
| [OpenVLA-OFT](https://arxiv.org/abs/2502.19645) | 一→二 | Llama 2 7B | 平行解碼＋連續迴歸 | 約原版 25 倍 | 是 |
| [π0-FAST](https://arxiv.org/abs/2501.09747) | 一 | PaliGemma | DCT＋BPE 離散 token | 自回歸 | 是 |
| [π0](https://arxiv.org/abs/2410.24164) | 二 | PaliGemma 3B | 300M 動作專家，flow matching | 約 50 Hz | 是 |
| [GR-2](https://arxiv.org/abs/2410.06158) | 四 | 自研 GPT 式 | 影片預測＋動作 | 未公開 | 否 |
| [OpenVLA](https://arxiv.org/abs/2406.09246) | 一 | Llama 2 7B | 256-bin 離散 token | 約 5 Hz | 是 |
| [RT-2](https://arxiv.org/abs/2307.15818) | 一 | PaLI-X／PaLM-E | 256-bin 離散 token | 約 1 到 5 Hz | 否 |

## 世界模型四條路線一張圖

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
<text x="405" y="40" class="b">一、潛在動力學：任務專用潛狀態＋獎勵</text>
<text x="405" y="62" class="s">DreamerV3／4、TD-MPC2 → RL 想像訓練、MPC 規劃</text>
<rect class="n wm" x="390" y="95" width="400" height="60" rx="10"/>
<text x="405" y="120" class="b">二、JEPA：自監督表徵，不重建像素</text>
<text x="405" y="142" class="s">V-JEPA 2、DINO-WM → 零樣本目標條件規劃</text>
<rect class="n wm" x="390" y="175" width="400" height="60" rx="10"/>
<text x="405" y="200" class="b">三、影片生成：像素／影片潛空間</text>
<text x="405" y="222" class="s">Genie 3、Cosmos、GAIA-2 → 互動環境、合成資料、評估</text>
<rect class="n wm" x="390" y="255" width="400" height="60" rx="10"/>
<text x="405" y="280" class="b">四、3D 空間：顯式 3D 場景或佔據柵格</text>
<text x="405" y="302" class="s">Marble、OccWorld → 場景模擬、數位孿生、自駕</text>
<text x="20" y="300" class="s">要「做決策」選一、二；</text>
<text x="20" y="318" class="s">要「造世界、造資料」選三、四</text>
</svg>
<figcaption>差別在「把未來預測成什麼」。一和二都在潛空間，差在要不要重建畫面；三輸出人看得懂的影片；四輸出可走進去的 3D 場景。</figcaption>
</figure>

## 世界模型路線一：潛在動力學模型（給 RL 與規劃用）

**核心想法：把觀測壓成精簡的潛在狀態 z，學 p(z<sub>t+1</sub> | z<sub>t</sub>, a<sub>t</sub>) 與獎勵，然後在「想像」中訓練策略或做規劃。** 預測的是任務相關的抽象狀態，不是好看的畫面，所以便宜，可以一次展開上千條軌跡。

三個組件：**編碼器**（觀測 → z）、**動力學模型**（z, a → 下一個 z）、**預測頭**（獎勵、終止、價值）。差異在是否重建像素，以及用策略還是線上規劃決策。

- [DreamerV3](https://arxiv.org/abs/2301.04104)（2023，2025 年登上 Nature）：RSSM（確定性 GRU 狀態＋離散隨機潛在）加像素重建，在想像軌跡中訓練 actor-critic；一組超參數打通 150 多個任務，首次不靠人類資料在 Minecraft 挖到鑽石。
- [Dreamer 4](https://arxiv.org/abs/2509.24527)（2025）：改用可擴展的 Transformer 影片世界模型與 shortcut forcing 目標，可即時推論；只用離線資料在世界模型內訓練策略就能在 Minecraft 取得鑽石，是路線一與路線三的匯流。
- [TD-MPC2](https://arxiv.org/abs/2310.16828)（2023）：不重建像素的「隱式」世界模型，以潛在一致性＋獎勵＋價值損失訓練，用 MPPI 在潛空間做模型預測控制；單一 3.17 億參數模型涵蓋 80 個連續控制任務。
- 離散 token 變體：[IRIS](https://arxiv.org/abs/2209.00588)（VQ-VAE＋GPT）與 [DIAMOND](https://arxiv.org/abs/2405.12399)（擴散世界模型，證明視覺細節對 RL 很重要）。

**適合**：樣本效率導向的 RL、低維控制、線上規劃。**限制**：多半單一環境訓練，較少從網路規模資料取得常識。

## 世界模型路線二：JEPA 表徵預測

**核心想法：只在抽象表徵空間預測未來，不生成像素。** 這是 Yann LeCun 主張的路線：像素充滿不可預測的細節（樹葉、光影），生成它們浪費算力；在表徵空間預測可以自動丟掉雜訊。與路線一的差別是：編碼器用自監督在大量影片上預訓練，而不是為單一任務訓練。

**訓練方式**：遮蔽影片的一部分時空區塊，讓預測器從可見部分的表徵去預測被遮部分的表徵；目標編碼器以 EMA 更新，防止表徵崩塌。

- [V-JEPA 2](https://arxiv.org/abs/2506.09985)（Meta, 2025）：兩階段。第一階段用超過 100 萬小時網路影片預訓練約 10 億參數的 ViT 編碼器；第二階段凍結編碼器，用不到 62 小時的 DROID 機器人資料訓練動作條件預測器（V-JEPA 2-AC）。部署時給一張目標影像，用 CEM 在表徵空間搜尋動作，實現零樣本抓放。
- [DINO-WM](https://arxiv.org/abs/2411.04983)（2024）：直接用凍結的 DINOv2 patch 特徵當狀態，在其上訓練 ViT 動力學預測器，不需獎勵即可在測試時做目標條件規劃。

**適合**：想便宜地做「想像式」規劃、不需要輸出畫面的機器人。**限制**：無法直接視覺化結果來除錯，長程規劃仍仰賴外部搜尋，統一的評測標準也還不成熟。

## 世界模型路線三：影片生成式世界模型

**核心想法：世界模型＝可以接受動作輸入的影片生成器。** 給過去幀與動作（鍵盤、方向盤、關節指令或文字），生成未來幀。這是目前規模最大、最受關注的路線，主要用於遊戲與互動環境、自駕與機器人的合成資料、策略評估。

**典型架構**：影片 tokenizer（連續 VAE 或離散 VQ）先把影片壓成時空潛在 → 主幹為 DiT（擴散）或自回歸 Transformer → 動作以 adaLN、cross-attention 或拼接 token 的方式條件化。要即時互動就必須逐幀自回歸，所以 [Diffusion Forcing](https://arxiv.org/abs/2407.01392) 與 [Self Forcing](https://arxiv.org/abs/2506.08009) 這類「每幀不同噪聲等級」的訓練技巧成為關鍵，用來抑制長序列誤差累積。

- **Genie 系列（Google DeepMind）**：[Genie 1](https://arxiv.org/abs/2402.15391)（2024）由影片 tokenizer、潛在動作模型、自回歸動力學模型三部分組成，從無標註的遊戲影片學出 8 種離散潛在動作；[Genie 2](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/)（2024）改用潛在擴散＋自回歸生成 3D 環境；[Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)（2025）以 720p、24 fps 即時生成，可維持數分鐘一致性，並支援文字「世界事件」。
- [NVIDIA Cosmos](https://arxiv.org/abs/2501.03575)（2025）：「物理 AI 的世界基礎模型平台」，提供擴散與自回歸兩種世界模型、開源 tokenizer，後續拆成 Predict、Transfer、Reason 三個系列，權重開放。
- [GAIA-2](https://arxiv.org/abs/2503.20523)（Wayve, 2025）：自駕專用、潛在擴散、多相機一致，可用自車動作、他車位置、天氣、地區等條件控制生成，用來合成罕見危險場景。
- [UniSim](https://arxiv.org/abs/2310.06114)（2023）與 [1X World Model](https://www.1x.tech/discover/1x-world-model)：用動作條件影片模型模擬機器人互動，用來評估策略或在模擬中訓練。
- [Sora](https://openai.com/index/video-generation-models-as-world-simulators/)（OpenAI, 2024）：時空 patch＋DiT 的代表，提出「影片生成模型即世界模擬器」，但本身不接受動作輸入，嚴格說不是可控世界模型。

**限制**：物理正確性不保證（物體穿透、憑空消失），長時間一致性與推論成本仍是主要瓶頸。

## 世界模型路線四：3D／空間世界模型

**核心想法：輸出的不是一串 2D 影片幀，而是具有明確 3D 結構、可持久存在的場景。** 影片模型「轉個身回來場景就變了」的問題，在顯式 3D 表示（高斯潑濺、網格、點雲）中自然消失，生成的場景還能匯入物理引擎。

- [World Labs Marble](https://www.worldlabs.ai/blog/marble-world-model)（2025）：李飛飛團隊提出「空間智能」，從文字、圖片或影片生成可編輯、可匯出為高斯潑濺或網格的 3D 世界。
- 影片模型＋3D 記憶的混合：生成影片時維護一個 3D 場景快取或幾何條件，提升回訪一致性，是 2025 後互動世界模型常見的強化方式。
- 自駕領域的**佔據柵格（occupancy）世界模型**，如 [OccWorld](https://arxiv.org/abs/2311.16038)：在鳥瞰 3D 佔據空間預測未來，而非在相機影像空間。

**適合**：需要幾何一致的模擬、數位孿生、把生成場景送進 Isaac Sim 等物理模擬器訓練機器人。**限制**：多數仍是靜態場景，物體動態與互動仍要靠外部物理引擎。

## 世界模型四大路線比較

| 路線 | 在哪個空間預測 | 接受動作輸入 | 主要用途 | 代表 | 最大弱點 |
|---|---|---|---|---|---|
| 一、潛在動力學 | 任務專用潛在狀態 | 是（低維動作） | RL 想像訓練、MPC 規劃 | DreamerV3／4、TD-MPC2 | 難從網路資料取得常識 |
| 二、JEPA 表徵預測 | 自監督表徵空間 | 是（少量機器人資料後訓） | 零樣本目標條件規劃 | V-JEPA 2、DINO-WM | 無法視覺化、長程規劃昂貴 |
| 三、影片生成 | 像素／影片潛在 | 是（鍵盤、方向盤、文字、關節） | 互動環境、合成資料、策略評估 | Genie 3、Cosmos、GAIA-2 | 物理不可靠、算力昂貴 |
| 四、3D 空間 | 顯式 3D 場景 | 部分（多為相機移動） | 模擬場景、數位孿生 | Marble、OccWorld | 動態與互動不足 |

## 趨勢與選型建議

**五個正在發生的收斂**

1. **動作頭收斂到 flow matching＋動作分塊。** 離散 token 退居為「訓練時的輔助目標」（如 FAST＋知識絕緣）。
2. **分層是人形機器人的預設。** 慢 VLM 加快視動策略，差別只在中間是潛向量還是語言。
3. **「先思考再行動」進入 VLA。** Gemini Robotics 1.5、CoT-VLA 把推理鏈（文字或影像）放在動作之前。
4. **VLA 與世界模型正在合併。** 世界模型同時扮演預訓練目標、資料引擎、評估與 RL 環境三個角色。
5. **從模仿學習走向 RL 微調。** 以預訓練 VLA 為起點，用真實或世界模型中的經驗做強化學習，如 Physical Intelligence 的 [π*0.6／Recap](https://www.pi.website/blog/pistar06)。

**如果要動手實驗**

- 入門、單張 GPU：[SmolVLA](https://huggingface.co/lerobot/smolvla_base)＋[LeRobot](https://github.com/huggingface/lerobot)。
- 最強開源基準線：[openpi](https://github.com/Physical-Intelligence/openpi)（π0／π0.5）。
- 人形或全身控制：[Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)。
- 研究世界模型規劃：[V-JEPA 2](https://github.com/facebookresearch/vjepa2) 或 [TD-MPC2](https://github.com/nicklashansen/tdmpc2)。
- 生成合成資料：[Cosmos](https://github.com/nvidia-cosmos)。
