# 業界產品盤點

<p class="lede">只看已落地或接近量產的產品與商用平台（截至 2026-10），純學術模型只在對照時出現。每一家都標出「有沒有 VLA、有沒有世界模型、開不開源、有什麼文件可讀」。</p>

**標記說明**：🟢 開源權重或程式碼｜📄 有論文或技術報告｜🎤 只有部落格、發表會或演講｜🔒 閉源

!!! warn "時效提醒"
    2026 年的項目（Gemini Robotics 2、π0.7、Helix 02、Waymo World Model、1X World Model 等）是依官方部落格與新聞查核，細節以原始公告為準。只有演講或發表會的資訊，都**沒有可重現的訓練細節**。

## 重點摘要

!!! key "四件事先記住"
    1. **「VLA + 世界模型」並用已是主流，但分工很固定**：VLA 是機器人或車上的「大腦」（策略），世界模型放在雲端當「模擬器、資料工廠、考官」。真正把世界模型放進即時控制迴圈的（1X、V-JEPA 2-AC、Unitree WMA）還在早期。
    2. **最透明、能直接上手的三家**：Physical Intelligence（π0／π0.5／openpi）、NVIDIA（GR00T + Cosmos + Alpamayo）、comma.ai openpilot。
    3. **最強但最封閉**：Tesla、Waymo、Figure、華為、理想、小鵬，只有演講、部落格或發表會。
    4. **自駕分成兩派**：VLA 派（含語言推理：理想、小鵬、Waymo EMMA、Alpamayo、Wayve LINGO）與 WA 派（World Action，不走語言：華為 WEWA、蔚來 NWM、Tesla FSD）。

## 典型分工：車端／機器人端 vs 雲端

<figure class="dg">
<svg viewBox="0 0 800 325" role="img" aria-label="VLA 在端側，世界模型在雲端的分工">
<rect class="n band" x="10" y="10" width="370" height="280" rx="14"/>
<text x="195" y="38" text-anchor="middle" class="h">機器人／車端（即時）</text>
<rect class="n band" x="420" y="10" width="370" height="280" rx="14"/>
<text x="605" y="38" text-anchor="middle" class="h">雲端（離線、大算力）</text>
<rect class="n vla" x="60" y="70" width="270" height="80" rx="12"/>
<text x="195" y="104" text-anchor="middle" class="b vla">VLA／端到端策略</text>
<text x="195" y="128" text-anchor="middle" class="s">看畫面、聽指令、輸出動作</text>
<rect class="n" x="60" y="200" width="270" height="60" rx="10"/>
<text x="195" y="226" text-anchor="middle" class="b">真實世界</text>
<text x="195" y="246" text-anchor="middle" class="s">車隊、機器人收回的資料</text>
<rect class="n wm" x="460" y="60" width="290" height="50" rx="10"/>
<text x="605" y="90" text-anchor="middle" class="b wm">① 資料工廠：生成新情境</text>
<rect class="n wm" x="460" y="122" width="290" height="50" rx="10"/>
<text x="605" y="152" text-anchor="middle" class="b wm">② 考官：閉環評估</text>
<rect class="n wm" x="460" y="184" width="290" height="50" rx="10"/>
<text x="605" y="214" text-anchor="middle" class="b wm">③ 訓練場：想像中 RL</text>
<text x="605" y="268" text-anchor="middle" class="s">④ 預訓練、⑤ 直接當策略：見下表</text>
<path class="ar vla" d="M195,150 V198"/>
<path class="ar" d="M330,230 H395 V85 H458"/>
<path class="ar wm" d="M458,152 H350 V110 H332"/>
<text x="400" y="318" text-anchor="middle" class="s">真實資料上雲，訓好的策略（常經蒸餾）下發到端側</text>
</svg>
<figcaption>大多數產品的世界模型不在即時控制迴圈裡。小鵬（72B 雲端基座 → 車端小模型）與 NVIDIA Alpamayo（雲端教師 → DRIVE Thor）都明講用蒸餾把雲端能力搬到端側。</figcaption>
</figure>

## 總覽表

| 公司／產品 | 領域 | VLA | 世界模型 | 開源 | 文件 |
|---|---|---|---|---|---|
| Physical Intelligence π0／π0.5／π\*0.6／π0.7 | 通用機器人 | ✅ | — | 🟢 π0、π0.5 | 📄 |
| Google DeepMind Gemini Robotics 1.5／2 | 通用機器人 | ✅ | （Genie 3 另線） | 🔒 SDK 給試用夥伴 | 📄 1.0／1.5；2 只有安全報告 |
| NVIDIA Isaac GR00T N1 → N1.6 | 人形機器人 | ✅ | ✅ Cosmos 生成資料 | 🟢 | 📄 |
| NVIDIA Cosmos（Predict／Transfer／Reason） | 平台 | — | ✅ | 🟢 | 📄 |
| NVIDIA Alpamayo 1（R1） | 自駕 | ✅ | ✅ AlpaSim + Cosmos | 🟢 | 📄 |
| Figure Helix／Helix 02 | 人形機器人 | ✅ | — | 🔒 | 🎤 |
| 1X Redwood AI + 1X World Model（NEO） | 家用人形 | ✅ | ✅ 直接用於控制與評估 | 🔒 | 🎤 |
| 智元 AgiBot GO-1 + Genie Envisioner | 人形機器人 | ✅ | ✅ | 🟢 部分 | 📄 |
| 字節 Seed GR-2／GR-3 | 機器人 | ✅ | ✅ 影片生成預訓練 | 🔒 | 📄 |
| 宇樹 Unitree UnifoLM-WMA-0 | 機器人 | ✅ | ✅ | 🟢 | 程式碼 + 說明 |
| Hugging Face SmolVLA（LeRobot） | 低成本手臂 | ✅ | — | 🟢 | 📄 |
| Meta V-JEPA 2／V-JEPA 2-AC | 研究平台 | — | ✅ | 🟢 | 📄 |
| Tesla FSD v12+／Optimus | 自駕 + 人形 | 端到端（非語言） | ✅ 神經世界模擬器 | 🔒 | 🎤 ICCV 2025 演講 |
| Waymo EMMA + Waymo World Model | Robotaxi | ✅ EMMA（研究） | ✅ 基於 Genie 3 | 🔒 | 📄 EMMA；🎤 WM |
| Wayve LINGO-2 + GAIA-1／2 | 自駕 | ✅ | ✅ | 🔒 | 📄 |
| comma.ai openpilot | 駕駛輔助 | 端到端 | ✅ 用來訓練策略 | 🟢 | 📄 |
| 理想 MindVLA | 自駕 | ✅ | ✅ 雲端 WM 當考官 | 🔒 | 📄 DriveVLM；🎤 其餘 |
| 小鵬 VLA 2.0 + 72B 世界基座模型 | 自駕 | ✅ | ✅ | 🔒 | 🎤 CVPR 2025 WAD |
| 華為 乾崑 ADS 4 WEWA | 自駕 | ❌ 刻意不用語言 | ✅ 雲端 World Engine | 🔒 | 🎤 |
| 蔚來 NWM | 自駕 | ❌ | ✅ | 🔒 | 🎤 |

## 機器人領域

### Physical Intelligence：π0 系列 🟢📄（最推薦閱讀）

- **定位**：通用機器人基礎模型，授權給機器人公司。版本依序為 π0（2024/10）、π0-FAST、π0.5（2025/04）、π\*0.6（2025/11，加入 RL）、π0.7（2026/04，主打組合式泛化）。
- **架構**：PaliGemma VLM（約 3B）加上 **flow matching 的 action expert**，輸出 50 步連續動作塊（action chunk），控制頻率最高 50 Hz。
- **怎麼訓練**：
    1. **預訓練**：約 1 萬小時、7 種以上機器人平台的自有資料，加上 OXE 開源資料與網路圖文資料（VQA、caption、偵測），用來保留 VLM 的語意能力。
    2. **後訓練**：少量高品質任務資料微調（例如摺衣服）。
    3. **π0.5**：加入「高階語言子任務預測」，在同一個模型內做分層推理，能在沒見過的家庭環境工作。
    4. **Knowledge Insulation**：VLM 主幹用 FAST 離散 token 訓練，action expert 用 flow matching 訓練，並**阻斷梯度回流**，避免動作訓練破壞語言知識。
    5. **π\*0.6（Recap）**：離線 RL 加 advantage conditioning，學習人類介入修正與自主失敗經驗，做咖啡、摺箱子等長任務的成功率與吞吐量明顯提升。
- **開源**：[openpi](https://github.com/Physical-Intelligence/openpi) 提供 π0、π0-FAST、π0.5 權重與 LIBERO、DROID、ALOHA 微調腳本。
- **連結**：[π0 arXiv:2410.24164](https://arxiv.org/abs/2410.24164)｜[FAST arXiv:2501.09747](https://arxiv.org/abs/2501.09747)｜[π0.5 arXiv:2504.16054](https://arxiv.org/abs/2504.16054)｜[Knowledge Insulation arXiv:2505.23705](https://arxiv.org/abs/2505.23705)｜[官方研究頁](https://www.physicalintelligence.company/research)

### Google DeepMind：Gemini Robotics 1.0 → 1.5 → 2 📄🔒

- **架構**：雙模型分工。**Gemini Robotics-ER** 是負責具身推理與規劃的 VLM，可呼叫工具、追蹤任務進度；**Gemini Robotics** 是輸出動作的 VLA。另有在機器人本機執行的 **On-Device** 版本。
- **怎麼訓練（依 1.0／1.5 報告）**：以 Gemini 為主幹，混合 ALOHA 雙臂大量遙操作資料與網路多模態資料。1.5 提出 **Motion Transfer**，讓一個模型跨 ALOHA、Franka、Apptronik Apollo 共享技能，並加入「先思考再行動」的 embodied thinking。
- **Gemini Robotics 2（2026/07/30）**：支援人形全身控制（Apptronik Apollo 2）；On-Device 2 用不到 200 筆示範、幾小時內適應新的雙臂平台。這一版**只公開安全技術報告**，沒有方法論文。
- **取得方式**：ER 版可在 Google AI Studio 使用；VLA 本體只開放給 Trusted Tester 夥伴。
- **連結**：[技術報告 arXiv:2503.20020](https://arxiv.org/abs/2503.20020)｜[1.5 報告 arXiv:2510.03342](https://arxiv.org/abs/2510.03342)｜[Gemini Robotics 2 部落格](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)｜[安全報告 PDF](https://storage.googleapis.com/deepmind-media/gemini-robotics/Gemini-Robotics-2-Safety.pdf)｜前身 [RT-2 arXiv:2307.15818](https://arxiv.org/abs/2307.15818)

### NVIDIA：GR00T（VLA）+ Cosmos（世界模型）🟢📄

**VLA 與世界模型並用的教科書案例。**

- **GR00T N1 架構**：System 2 是 Eagle VLM，System 1 是 Diffusion Transformer（flow matching）動作頭，兩者以不同頻率協同。N1.5、N1.6 改進 VLM 凍結策略與推理能力，N1.6 已整合進 LeRobot。
- **資料金字塔**：底層是網路影片與人類第一人稱影片（用 latent action 或 IDM 推回動作偽標籤）；中層是**合成資料**（Isaac Sim 模擬與 Cosmos 生成的「神經軌跡」）；頂層是真實機器人遙操作。
- **世界模型怎麼餵 VLA（DreamGen）**：用少量目標機器人資料微調 Cosmos → 輸入新指令生成執行影片 → 用 IDM 或 latent action 標成動作 → 拿去訓練 GR00T。只靠一種真實任務的資料，泛化到 **22 種新行為**。流程圖見〈[世界模型四類與五種角色](world-model-roles.html)〉。
- **Cosmos**：Predict 2.5（未來影片預測）、Transfer 2.5（模擬畫面轉真實感）、Reason 2（物理推理 VLM），全部開源，2026/01 CES 發表。
- **連結**：[GR00T N1 arXiv:2503.14734](https://arxiv.org/abs/2503.14734)｜[Isaac-GR00T GitHub](https://github.com/NVIDIA/Isaac-GR00T)｜[Cosmos arXiv:2501.03575](https://arxiv.org/abs/2501.03575)｜[DreamGen arXiv:2505.12705](https://arxiv.org/abs/2505.12705)｜[CES 2026 新聞稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Releases-New-Physical-AI-Models-as-Global-Partners-Unveil-Next-Generation-Robots/default.aspx)

### Figure AI：Helix → Helix 02 🎤🔒

- **Helix（2025/02）**：System 2 是 7B VLM，以 7–9 Hz 處理語意；System 1 是 80M 的視覺運動 Transformer，以 **200 Hz** 控制上半身 35 個自由度。約 500 小時遙操作資料，用 VLM 自動回填指令標註；兩台機器人共用同一組權重。
- **Helix 02（2026/01）**：單一網路統一行走、操作與平衡，形成三層：語言目標層、感知轉動作層、高頻平衡層（用數千小時人體動作資料訓練）。示範是長時間自主裝卸洗碗機。
- **連結**：[Helix 官方部落格](https://www.figure.ai/news/helix)｜[Helix 02 報導](https://kulturegeek.fr/news-346271/figure-ai-devoile-helix-02-ia-rapproche-robot-humanoide-lautonomie-totale)｜沒有論文。

### 1X Technologies：NEO + Redwood AI + 1X World Model 🎤🔒

**少數把世界模型直接放進控制迴圈的商用案例。**

- **產品**：NEO 家用人形機器人，售價 2 萬美元或月租 499 美元，2026 年交付。
- **1X World Model（2026/01）**：核心是影片生成模型，網路規模影片預訓練、機器人資料微調。給定指令後先「想像」未來畫面，再由**逆動力學模型（IDM）把想像轉成動作**。
- 1X 也長期把世界模型當作**策略評估器**取代實機測試，並辦過公開的 1X World Model Challenge。
- **連結**：[Redwood AI／World Model 官方頁](https://www.1x.tech/discover/redwood-ai-world-model)｜[The Robot Report 報導](https://www.therobotreport.com/1x-launches-world-model-enabling-neo-robot-to-learn-tasks-by-watching-videos/)

### 中國機器人公司

- **智元 AgiBot**：GO-1（Genie Operator-1）是 ViLLA 架構，在 VLM 與動作專家之間加入 latent action 規劃器，用 AgiBot World 百萬級真機軌跡訓練。另有 **Genie Envisioner**，以影片擴散模型為核心，可同時當策略與模擬器。[GO-1 arXiv:2503.06669](https://arxiv.org/abs/2503.06669)｜[Genie Envisioner arXiv:2508.05635](https://arxiv.org/abs/2508.05635)
- **字節 Seed GR-2／GR-3**：先用大量網路影片做「預測下一幀」的生成式預訓練（等於先學世界模型），再用機器人軌跡微調出動作；GR-3 加入 VR 收集的人類軌跡。[GR-2 arXiv:2410.06158](https://arxiv.org/abs/2410.06158)｜[GR-3 arXiv:2507.15493](https://arxiv.org/abs/2507.15493)
- **宇樹 Unitree UnifoLM-WMA-0** 🟢：world-model-action 架構，世界模型可以當模擬器，也能同時預測未來與動作。[GitHub](https://github.com/unitreerobotics/unifolm-world-model-action)
- **智平方 AI² Robotics**：VLA 公司，主線是雙系統。完整拆解見〈[案例：智平方](ai2-robotics.html)〉。

### 開源生態（入門最友善）

- **Hugging Face SmolVLA** 🟢：450M 參數，用社群在 LeRobot 上傳的 SO-100 資料訓練，消費級 GPU 就能微調。[arXiv:2506.01844](https://arxiv.org/abs/2506.01844)
- **Meta V-JEPA 2** 🟢：100 萬小時以上影片自監督預訓練，學出不生成像素的潛空間世界模型；再用 62 小時 DROID 機器人資料訓練 action-conditioned 版（V-JEPA 2-AC），以 MPC 規劃做零樣本抓放。[arXiv:2506.09985](https://arxiv.org/abs/2506.09985)
- **TRI Large Behavior Models**（與 Boston Dynamics Atlas 合作）：系統性研究多任務擴散策略的預訓練效益。[arXiv:2507.05331](https://arxiv.org/abs/2507.05331)

## 自動駕駛領域

### Tesla：FSD v12+ 與 Optimus 🎤🔒

- **策略**：單一端到端網路，輸入影片、地圖與運動學資料，直接輸出控制，不經語言，也沒有明確的感知與規劃介面。
- **世界模型用途**（ICCV 2025 Ashok Elluswamy 演講）：用車隊資料訓練「神經世界模擬器」，依策略動作生成多鏡頭影片，用來：
    1. **閉環評估**，因為開環 loss 和真實表現相關性不高；
    2. 重播歷史資料讓模型分歧，看「如果當時這樣開」會怎樣；
    3. 生成對抗性極端情境；
    4. 大規模 RL。同一個模擬器也用於 Optimus。
- [演講整理報導](https://www.humanoidsdaily.com/feed/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus)

### Waymo：EMMA + Waymo World Model 📄🎤🔒

- **EMMA**：以 Gemini 為基礎的端到端多模態駕駛模型，軌跡、偵測框、路網都表示成文字，並使用 chain-of-thought。[arXiv:2410.23262](https://arxiv.org/abs/2410.23262)
- **Waymo World Model（2026/02）**：以 DeepMind **Genie 3** 為基礎，後訓練成同時輸出**相機與 LiDAR** 的生成式模擬器。支援駕駛動作的反事實測試、場景佈局、用文字改天氣或時段，也能把行車記錄器影片轉成模擬場景，測試車隊從未遇過的情境。[報導](https://the-decoder.com/waymo-taps-google-deepminds-genie-3-to-simulate-driving-scenarios-its-cars-have-never-seen/)｜沒有論文。

### Wayve：LINGO + GAIA 📄🔒

- **LINGO-1／2**：駕駛模型加上語言解說，LINGO-2 能用語言指令影響駕駛。[LINGO-2 部落格](https://wayve.ai/thinking/lingo-2-driving-with-language/)
- **GAIA-1（9B）／GAIA-2**：生成式駕駛世界模型，可控制自車動作、他車、天氣，支援多鏡頭，用來合成訓練與驗證資料。[GAIA-1 arXiv:2309.17080](https://arxiv.org/abs/2309.17080)｜[GAIA-2 arXiv:2503.20523](https://arxiv.org/abs/2503.20523)

### NVIDIA Alpamayo 🟢📄（自駕版「VLA + WM 全開源」）

- **Alpamayo 1（R1，10B）**：帶 chain-of-causation 推理的 VLA，輸入影片，輸出軌跡與推理文字。定位為**雲端教師模型**，再蒸餾到車端（DRIVE Thor）。
- **訓練**：先用 VLM 推理標註做 SFT，再用 RL 對齊「推理與動作的一致性」，軌跡由 diffusion 解碼器輸出。
- **配套**：AlpaSim 開源閉環模擬器、1,700 小時以上 Physical AI 開放資料集、Cosmos 生成資料。
- **連結**：[Alpamayo-R1 arXiv:2511.00088](https://arxiv.org/abs/2511.00088)｜[CES 2026 新聞稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Alpamayo-Family-of-Open-Source-AI-Models-and-Tools-to-Accelerate-Safe-Reasoning-Based-Autonomous-Vehicle-Development/)

### comma.ai openpilot 🟢📄（最小成本的「WM 訓練策略」量產案例）

- 用車隊影片訓練生成式世界模型，再讓駕駛策略**在世界模型裡 on-policy 學習**，取代傳統重模擬器，成果已上線到開源 openpilot。
- [Learning to Drive from a World Model arXiv:2504.19077](https://arxiv.org/abs/2504.19077)｜[openpilot GitHub](https://github.com/commaai/openpilot)

### 中國車廠

- **理想 MindVLA**：由 [DriveVLM（arXiv:2402.12289）](https://arxiv.org/abs/2402.12289) 的快慢雙系統演進而來，2025 年起改為自研基座的 VLA。雲端自研世界模型負責重建與生成場景，當 RL 訓練場與「考官」。
- **小鵬 VLA 2.0**：雲端訓練 **72B 世界基座模型**，結合視覺理解、CoT 與動作生成，再**蒸餾**到車端小模型。CVPR 2025 WAD 演講公開了 scaling law 觀察。
- **華為 ADS 4 WEWA**：雲端 World Engine 是「AI 駕校」，生成難例並做強化學習；車端 World Action 是約 8B 參數的 MoE 端到端模型。**明確拒絕 VLA 的語言層**，理由是延遲與資訊損失。
- **蔚來 NWM**：生成式世界模型，可在車上推演多條未來路徑，2025/05 全量推送。
- 以上都來自發表會或報導，沒有可重現的論文。[36Kr 技術路線整理](https://www.36kr.com/p/3463098292770179)

!!! note "VLA 派 vs WA 派，爭的是什麼"
    VLA 派認為語言推理帶來可解釋性與長尾泛化；WA 派認為語言是多一層翻譯，增加延遲又丟資訊，不如直接學「世界 → 動作」。兩派**都把世界模型放在雲端**，差別只在車端模型要不要語言。

## 五種共通整合模式

| 模式 | 作法 | 代表 |
|---|---|---|
| ① WM 當**資料工廠** | 生成新情境影片，用 IDM 或 latent action 標上動作，再訓練 VLA | NVIDIA DreamGen + GR00T、Waymo、Wayve GAIA、華為 WE |
| ② WM 當**閉環評估器** | 策略在 WM 裡開車或操作，取代實機測試 | Tesla、1X、Waymo、理想 |
| ③ WM 當 **RL 訓練場** | 策略在 WM 內 on-policy 學習 | comma.ai、Tesla、華為、理想 |
| ④ WM **預訓練**再接動作頭 | 先學「預測未來畫面」，再微調成策略 | 字節 GR-2／3、AgiBot GE、Unitree WMA |
| ⑤ WM **即為策略** | 想像未來畫面再用 IDM 轉動作，或在潛空間做 MPC | 1X World Model、V-JEPA 2-AC |

①②③ 發生在訓練時，④ 改變模型本身，只有 ⑤ 在推論時真的用到世界模型。這個區分的細節見〈[訓練時 vs 推論時](train-vs-inference.html)〉。

## 想自己動手：建議順序

1. **讀**：π0 → π0.5 → GR00T N1 → DreamGen → comma.ai 論文，這幾篇的訓練配方寫得最完整。
2. **跑 VLA**：用 [openpi](https://github.com/Physical-Intelligence/openpi) 或 [LeRobot](https://github.com/huggingface/lerobot)（SmolVLA、GR00T N1.6）在 LIBERO 模擬環境上微調。
3. **跑世界模型**：用 Cosmos Predict 2.5 或 V-JEPA 2 做「給定動作預測未來」，再試 DreamGen 式的合成資料流程。
4. **自駕方向**：從 Alpamayo-R1 + AlpaSim 入手，是目前唯一完整開源的「推理 VLA + 閉環模擬」組合。
