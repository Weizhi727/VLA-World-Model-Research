# 流派怎麼分：VLA 的三條軸、世界模型的四個流派

<p class="lede">「端到端 vs 分層」是 VLA 的一種分類沒錯，但它只是其中一條軸。一個模型通常在每條軸上各選一格。世界模型也有流派，最常見的切法是「在哪個空間預測未來」。</p>

!!! key "重點先講"
    1. **「端到端 vs 分層」只是一條軸**：看的是系統架構，以及中間有沒有人看得懂的中間產物。
    2. **VLA 至少還有另外兩條常用的軸**：**動作怎麼解碼**（離散 token 自回歸、擴散／flow matching、兩者混合），以及**中間表徵是什麼**（語言子任務、程式碼、關鍵點、軌跡、目標影像、潛在動作、原始動作、推理鏈）。
    3. **世界模型也分流派**：「輸出影片」和「潛空間」是前兩派，**第三派是 JEPA 式的非生成表徵預測（如 V-JEPA 2），第四派是 3D／4D 空間式（如 World Labs Marble、佔據柵格）**。
    4. 專案早期課件的「VLA 四大流派」把不同軸混在一起，也漏了真正的「顯式分層」派；本頁的「兩軸地圖」是建議的替代講法。

## VLA 的三條分類軸

<figure class="dg">
<svg viewBox="0 0 800 250" role="img" aria-label="VLA 的三條分類軸">
<rect class="n vla" x="10" y="20" width="250" height="210" rx="12"/>
<text x="135" y="50" text-anchor="middle" class="b vla">軸 A：系統架構</text>
<text x="135" y="72" text-anchor="middle" class="s">中間有沒有可解釋的介面</text>
<rect class="n" x="30" y="90" width="210" height="34" rx="8"/><text x="135" y="112" text-anchor="middle">單系統</text>
<rect class="n" x="30" y="132" width="210" height="34" rx="8"/><text x="135" y="154" text-anchor="middle">雙系統（快慢腦）</text>
<rect class="n" x="30" y="174" width="210" height="34" rx="8"/><text x="135" y="196" text-anchor="middle">顯式分層</text>
<rect class="n vla" x="275" y="20" width="250" height="210" rx="12"/>
<text x="400" y="50" text-anchor="middle" class="b vla">軸 B：動作怎麼解碼</text>
<text x="400" y="72" text-anchor="middle" class="s">動作是 token 還是連續值</text>
<rect class="n" x="295" y="90" width="210" height="34" rx="8"/><text x="400" y="112" text-anchor="middle">離散 token 自回歸</text>
<rect class="n" x="295" y="132" width="210" height="34" rx="8"/><text x="400" y="154" text-anchor="middle">擴散／flow matching</text>
<rect class="n" x="295" y="174" width="210" height="34" rx="8"/><text x="400" y="196" text-anchor="middle">混合式</text>
<rect class="n vla" x="540" y="20" width="250" height="210" rx="12"/>
<text x="665" y="50" text-anchor="middle" class="b vla">軸 C：中間表徵</text>
<text x="665" y="72" text-anchor="middle" class="s">模組之間傳的是什麼 token</text>
<text x="665" y="108" text-anchor="middle">語言、程式碼、affordance</text>
<text x="665" y="138" text-anchor="middle">軌跡、目標影像</text>
<text x="665" y="168" text-anchor="middle">潛在表徵、原始動作</text>
<text x="665" y="198" text-anchor="middle">推理鏈</text>
</svg>
<figcaption>三條軸分別來自三篇綜述：軸 A 依 <a href="https://arxiv.org/abs/2508.13073">arXiv:2508.13073</a>，軸 B 依 <a href="https://arxiv.org/abs/2509.19012">arXiv:2509.19012</a>，軸 C 依 <a href="https://arxiv.org/abs/2507.01925">arXiv:2507.01925</a>。</figcaption>
</figure>

### 軸 A：系統架構（「端到端 vs 分層」在這條軸）

這條軸最清楚的定義來自 [Large VLM-based VLA Models for Robotic Manipulation: A Survey（arXiv:2508.13073）](https://arxiv.org/abs/2508.13073)。它把 VLA 分成兩大類、三小類：

| 類別 | 定義（綜述原意） | 代表模型 |
|---|---|---|
| **單一系統（Monolithic／single-system）** | 一個模型吃所有模態，直接用自回歸或平行解碼輸出動作 | [RT-2](https://arxiv.org/abs/2307.15818)、[OpenVLA](https://arxiv.org/abs/2406.09246)、CogVLA |
| **雙系統（Monolithic／dual-system）** | VLM 骨幹負責理解，另接動作專家輸出動作；**兩者之間沒有人看得懂的中間產物**，仍可整體端到端訓練 | [π0](https://arxiv.org/abs/2410.24164)、[π0.5](https://arxiv.org/abs/2504.16054)、[GR00T N1](https://arxiv.org/abs/2503.14734)、CogACT、[SmolVLA](https://arxiv.org/abs/2506.01844) |
| **顯式分層（Hierarchical）** | 規劃器先輸出**可解釋的中間表徵**，再交給低階策略執行，「明確把規劃與執行解耦」 | [PaLM-E](https://arxiv.org/abs/2303.03378)、[RoboPoint](https://arxiv.org/abs/2406.10721)、[Hi Robot](https://arxiv.org/abs/2502.19417)、[HAMSTER](https://arxiv.org/abs/2502.05485) |

!!! warn "命名陷阱"
    - 業界常把 Figure Helix、GR00T N1 這種「慢想快做」叫做「分層」。但在這篇綜述的定義下，它們屬於**雙系統的端到端模型**，因為兩個系統之間傳的是潛向量或特徵，不是人看得懂的東西。
    - 所以「端到端 vs 分層」真正的分界線是：**中間有沒有可解釋、可人工介入的介面**（子任務文字、關鍵點、軌跡、程式碼）。
    - 灰色地帶：π0.5 和 [Gemini Robotics 1.5](https://arxiv.org/abs/2510.03342) 會先產生語言子任務再出動作，介於兩者之間。
    - 自駕領域的「端到端 vs 模組化」是更早的整個駕駛系統分法（感知、預測、規劃分不分開），不是 VLA 專屬。國內車廠另有「VLA 派 vs WA（World Action）派」之爭，差別在要不要經過語言層，例如華為 WEWA 明確拒絕語言層（見 [08 業界產品盤點](industry.html)）。

### 軸 B：動作怎麼解碼

[Pure Vision Language Action (VLA) Models: A Comprehensive Survey（arXiv:2509.19012）](https://arxiv.org/abs/2509.19012) 依動作生成方式分成五個範式：

1. **自回歸式**：動作離散成 token 逐一生成。代表作 RT-2、OpenVLA，以及 [FAST tokenizer](https://arxiv.org/abs/2501.09747)。
2. **擴散／flow matching 式**：從雜訊生成連續動作塊，例如 π0，以及延伸自 [Diffusion Policy](https://arxiv.org/abs/2303.04137) 的各種方法。
3. **強化學習式**：用 RL 微調或訓練 VLA。
4. **混合式**：同一模型結合自回歸與擴散，例如 [HybridVLA](https://arxiv.org/abs/2503.10631)。
5. **特化方法**：其他特定設計。

!!! note "小提醒"
    嚴格說，「RL 式」是**訓練方法**，不是架構。它和前兩派可以疊加，比較適合放在訓練章節講（見 [04 訓練、資料與評估](training.html)）。

### 軸 C：中間表徵／action token 是什麼

[A Survey on VLA Models: An Action Tokenization Perspective（arXiv:2507.01925）](https://arxiv.org/abs/2507.01925) 換了一個角度：把 VLA 看成「一串模組，每個模組輸出某種 action token」，並依 token 類型分成 8 類：**語言描述、程式碼、affordance、軌跡、目標狀態（目標影像）、潛在表徵、原始動作、推理鏈。**

這條軸可以把很多「看起來是不同流派」的東西統一起來：

- 分層 VLA＝前段輸出「語言／關鍵點／軌跡」，後段輸出「原始動作」。
- 預測式 VLA（GR-2、[CoT-VLA](https://arxiv.org/abs/2503.22020)）＝先輸出「目標狀態」。
- [LAPA](https://arxiv.org/abs/2410.11758)、智元 GO-1＝先輸出「潛在動作」。
- ECoT 等推理型 VLA＝先輸出「推理鏈」。

### 小結：一個模型在每條軸上各選一格

| 軸 | 選項 | 早期課件「四大流派」的對應 |
|---|---|---|
| A 系統架構 | 單系統／雙系統／顯式分層 | ③ 雙系統（**缺顯式分層**） |
| B 動作解碼 | 離散自回歸／擴散·flow／混合 | ① 離散、② 連續專家 |
| C 中間表徵 | 語言、關鍵點、軌跡、目標影像、潛在動作、推理… | ④ 預測式（目標影像、潛在動作） |
| （訓練） | 模仿學習／RL 微調 | 已在訓練章節 |

例如：

- **GR00T N1**＝雙系統＋flow 解碼＋潛向量介面。
- **π0.5**＝雙系統＋FAST 離散（預訓練）與 flow（動作專家）混合＋語言子任務。

## 建議的「兩軸地圖」

<figure class="dg">
<svg viewBox="0 0 800 400" role="img" aria-label="VLA 兩軸地圖：架構 × 動作解碼">
<text x="470" y="22" text-anchor="middle" class="h">軸 A：系統架構 →</text>
<text x="250" y="48" text-anchor="middle" class="b">單系統</text>
<text x="470" y="48" text-anchor="middle" class="b">雙系統（快慢腦）</text>
<text x="690" y="48" text-anchor="middle" class="b">顯式分層</text>
<text x="70" y="120" text-anchor="middle" class="b">離散 token</text>
<text x="70" y="140" text-anchor="middle" class="s">自回歸</text>
<text x="70" y="225" text-anchor="middle" class="b">連續</text>
<text x="70" y="245" text-anchor="middle" class="s">擴散／flow</text>
<text x="20" y="180" class="h" transform="rotate(-90 20 180)" text-anchor="middle">軸 B：解碼</text>
<rect class="n" x="145" y="62" width="210" height="100" rx="10"/>
<text x="250" y="102" text-anchor="middle">RT-2、OpenVLA</text>
<text x="250" y="126" text-anchor="middle">π0-FAST</text>
<rect class="n" x="365" y="62" width="210" height="100" rx="10"/>
<text x="470" y="98" text-anchor="middle" class="s">（少見純離散；常見混合）</text>
<text x="470" y="124" text-anchor="middle">π0.5、FiS-VLA</text>
<text x="470" y="144" text-anchor="middle" class="s">離散訓練＋連續輸出</text>
<rect class="n" x="585" y="62" width="210" height="100" rx="10"/>
<text x="690" y="102" text-anchor="middle">PaLM-E、RoboPoint</text>
<text x="690" y="126" text-anchor="middle" class="s">規劃器以 token 輸出</text>
<rect class="n" x="145" y="172" width="210" height="100" rx="10"/>
<text x="250" y="212" text-anchor="middle">OpenVLA-OFT</text>
<text x="250" y="236" text-anchor="middle">RoboMamba</text>
<rect class="n vla" x="365" y="172" width="210" height="100" rx="10"/>
<text x="470" y="204" text-anchor="middle" class="b">π0、SmolVLA、CogACT</text>
<text x="470" y="228" text-anchor="middle" class="b">GR00T N1、Helix</text>
<text x="470" y="252" text-anchor="middle" class="s">目前主流</text>
<rect class="n" x="585" y="172" width="210" height="100" rx="10"/>
<text x="690" y="212" text-anchor="middle">Hi Robot、HAMSTER</text>
<text x="690" y="236" text-anchor="middle" class="s">低階多為連續策略</text>
<rect class="n mix" x="145" y="292" width="650" height="90" rx="10"/>
<text x="470" y="318" text-anchor="middle" class="b mix">跨格的加值模組（軸 C）</text>
<text x="470" y="344" text-anchor="middle">世界模型預測：GR-2、CoT-VLA、DreamVLA、VPP</text>
<text x="470" y="366" text-anchor="middle">推理鏈：ECoT、Gemini Robotics 1.5　｜　潛在動作：LAPA、GO-1</text>
</svg>
<figcaption>建議的分類講法：橫軸是架構，縱軸是動作解碼，把「融合世界模型」與「推理鏈」改成跨格的加值模組。格子位置依綜述定義與各論文描述推論；混合式模型（π0.5、FiS-VLA）放在雙系統欄的上格。</figcaption>
</figure>

**為什麼這樣畫比「四大流派」好**

- **舊講法的問題 1：混用不同的軸。** ① 離散 token 和 ② 連續動作專家屬於「動作解碼」軸；③ 雙系統屬於「架構」軸；④ 預測式屬於「中間表徵」軸。聽眾容易誤以為這是同一層級的四選一。
- **舊講法的問題 2：漏了真正的「顯式分層」派。** 依 [arXiv:2508.13073](https://arxiv.org/abs/2508.13073) 的定義，Helix／GR00T N1 是端到端的雙系統；真正的分層派（規劃器輸出子任務、關鍵點、軌跡或程式碼，再交給低階策略）需要自己的代表作，例如 Hi Robot、RoboPoint、HAMSTER。
- **新分支**：智平方的 NeuroVLA（大腦／小腦／脊髓三層類腦）不屬於上面任何一格，可以標成「三系統／類腦」新分支，見 [09 案例：智平方](ai2-robotics.html)。

## 世界模型的流派

### 主切法：在哪個空間預測未來

| 流派 | 預測什麼 | 代表作 | 長處／代價 |
|---|---|---|---|
| **① 影片／像素生成式** | 未來的影格。通常在影片 tokenizer 的 latent 裡生成，最後解碼成像素 | [Cosmos](https://arxiv.org/abs/2501.03575)、[Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)、[GAIA-2](https://arxiv.org/abs/2503.20523)、[UniSim](https://arxiv.org/abs/2310.06114) | 人看得懂、能當模擬器或造合成資料；但貴、慢，物理不一定對 |
| **② 潛空間動力學** | 低維潛狀態的下一步，通常仍保留重建像素的解碼器幫助學習 | [DreamerV3](https://arxiv.org/abs/2301.04104)、[Dreamer 4](https://arxiv.org/abs/2509.24527)、[TD-MPC2](https://arxiv.org/abs/2310.16828) | 快，適合在想像中做 RL 或規劃；但畫面細節少 |
| **③ JEPA 式表徵預測** | 在自監督表徵空間預測，**完全不生成、也不重建像素** | [V-JEPA 2／2-AC](https://arxiv.org/abs/2506.09985) | 不浪費算力在畫面細節，可零樣本規劃；但無法產出可看的影片，難直接檢查 |
| **④ 3D／4D 空間式** | 顯式 3D 場景（高斯潑濺、NeRF、佔據柵格、BEV） | [World Labs Marble](https://www.worldlabs.ai/blog/marble-world-model)、[OccWorld](https://arxiv.org/abs/2311.16038) | 幾何一致、可自由視角；但動態與拓撲變化難處理 |

!!! key "最常被混淆的一點"
    **② 和 ③ 都在潛空間，差別只在「要不要重建畫面」。** Dreamer 系列會訓練解碼器去重建畫面，JEPA 刻意不重建，這正是 LeCun「生成式 vs 非生成式」的核心。若只分兩派，常見說法是「生成式（①②④）vs 非生成式（③）」；若分三派，就是「影片、潛空間、JEPA」。

### 其他切法（綜述用的軸）

- **用途軸**：[A Comprehensive Survey on World Models for Embodied AI（arXiv:2510.16732）](https://arxiv.org/abs/2510.16732) 分成 **Decision-coupled**（為特定控制任務而學，如 Dreamer）與 **General-purpose**（通用模擬器，如 Cosmos、Genie）。
- **時間軸**：同一篇綜述再分成**逐步自回歸模擬**（適合閉環控制，但誤差會累積）與**一次平行預測整段未來**（延遲低，但互動性差）。
- **空間表徵軸**：同一篇綜述分成全域潛向量、token 特徵序列、空間潛柵格（BEV／voxel）、可渲染表徵（3DGS／NeRF），大致對應上表的 ②、①、④。
- **功能軸**：[Understanding World or Predicting Future?（arXiv:2411.14499）](https://arxiv.org/abs/2411.14499) 分成「理解世界」（建立內部表徵，如 LLM 內隱的世界知識）與「預測未來」（模擬未來以輔助決策）。

## 來源

- VLA 架構分類：[arXiv:2508.13073](https://arxiv.org/abs/2508.13073)
- VLA 動作解碼分類：[arXiv:2509.19012](https://arxiv.org/abs/2509.19012)
- VLA action token 分類：[arXiv:2507.01925](https://arxiv.org/abs/2507.01925)
- 世界模型具身綜述：[arXiv:2510.16732](https://arxiv.org/abs/2510.16732)
- 世界模型理解 vs 預測綜述：[arXiv:2411.14499](https://arxiv.org/abs/2411.14499)
