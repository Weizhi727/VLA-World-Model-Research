# 世界模型代表作的實際應用

<p class="lede">回答兩個追問：影片生成、潛空間動力學、JEPA、3D／4D 四類世界模型的代表作（Cosmos、Wan、Veo、Genie、DreamerV3／Dreamer 4、V-JEPA 2、Marble 等），實際被哪些 VLA 或其他系統用過；以及智平方、Figure Helix、GR00T N1／N1.5、GR-2／GR-3 在哪個階段、怎麼用世界模型。<b>只收有論文、官方頁或技術文章明寫的案例，查不到就寫「未找到公開證據」。</b>階段代號沿用 <a href="train-vs-inference.html">訓練時 vs 推論時</a>：T1 預訓練／輔助目標、T2 資料工廠、T3 想像中 RL、T4 評估器；I0 推論不參與、I1 借一部分特徵、I2 先想再做、I3 預演挑動作。</p>

<figure class="dg">
<svg viewBox="0 0 800 330" role="img" aria-label="四類世界模型代表作與主要使用者、使用階段">
<rect class="n band" x="10" y="10" width="780" height="310" rx="14"/>
<text x="110" y="38" text-anchor="middle" class="h">世界模型代表作</text>
<text x="400" y="38" text-anchor="middle" class="h">實際使用者（有公開來源）</text>
<text x="690" y="38" text-anchor="middle" class="h">主要階段</text>
<rect class="n wm" x="25" y="55" width="170" height="56" rx="10"/><text x="110" y="80" text-anchor="middle" class="b wm">影片生成</text><text x="110" y="99" text-anchor="middle" class="s">Cosmos · Wan · Veo 等</text>
<rect class="n" x="250" y="55" width="300" height="56" rx="10"/><text x="265" y="80" class="b">GR00T、Cosmos Policy、GE、VPP</text><text x="265" y="99" class="s">Gemini 評估、Waymo、SIMA 2、AlphaBrain</text>
<rect class="n key" x="605" y="55" width="170" height="56" rx="10"/><text x="690" y="88" text-anchor="middle" class="b">T2 · T4 · I1 · I3</text>
<rect class="n wm" x="25" y="125" width="170" height="56" rx="10"/><text x="110" y="150" text-anchor="middle" class="b wm">潛空間動力學</text><text x="110" y="169" text-anchor="middle" class="s">DreamerV3 · Dreamer 4</text>
<rect class="n" x="250" y="125" width="300" height="56" rx="10"/><text x="265" y="150" class="b">FOREWARN、DayDreamer</text><text x="265" y="169" class="s">未找到大型商用 VLA 採用</text>
<rect class="n" x="605" y="125" width="170" height="56" rx="10"/><text x="690" y="158" text-anchor="middle" class="b">T3 · I3</text>
<rect class="n wm" x="25" y="195" width="170" height="56" rx="10"/><text x="110" y="220" text-anchor="middle" class="b wm">JEPA</text><text x="110" y="239" text-anchor="middle" class="s">V-JEPA 2 / 2.1</text>
<rect class="n" x="250" y="195" width="300" height="56" rx="10"/><text x="265" y="220" class="b">V-JEPA 2-AC、JEPA-VLA、AlphaBrain</text><text x="265" y="239" class="s">從規劃器變成 VLA 的視覺編碼器</text>
<rect class="n" x="605" y="195" width="170" height="56" rx="10"/><text x="690" y="228" text-anchor="middle" class="b">I3 · T1／編碼器</text>
<rect class="n wm" x="25" y="265" width="170" height="46" rx="10"/><text x="110" y="286" text-anchor="middle" class="b wm">3D／4D</text><text x="110" y="303" text-anchor="middle" class="s">Marble · TesserAct</text>
<rect class="n" x="250" y="265" width="300" height="46" rx="10"/><text x="265" y="286" class="b">Isaac Sim、BEHAVIOR-1K、Waymo LiDAR</text><text x="265" y="303" class="s">主要用來快速造模擬場景</text>
<rect class="n" x="605" y="265" width="170" height="46" rx="10"/><text x="690" y="293" text-anchor="middle" class="b">建場景 · T4</text>
<path class="ar wm" d="M195,83 H248"/><path class="ar wm" d="M195,153 H248"/><path class="ar wm" d="M195,223 H248"/><path class="ar wm" d="M195,288 H248"/>
<path class="ar" d="M550,83 H603"/><path class="ar" d="M550,153 H603"/><path class="ar" d="M550,223 H603"/><path class="ar" d="M550,288 H603"/>
</svg>
<figcaption>被 VLA 實際用得最多的是可微調的開源影片模型（Wan、Cosmos、SVD）；Veo、Genie 3 只在 Google 體系內使用。</figcaption>
</figure>

## 重點先講

1. **被 VLA 實際用得最多的是「開源影片生成模型」，不是最有名的那幾個。** WAN2.1 是 GR00T N1 與 DreamGen 造資料的主力；Stable Video Diffusion（SVD）被 VPP、Ctrl-World 拿來當骨幹；Cosmos-Predict2 被 Cosmos Policy、智元 GE、智平方 AlphaBrain 拿來當策略骨幹。**Genie 3、Veo 只有 Google 自家（Waymo、SIMA 2、Gemini Robotics）在用**，因為沒有開放權重。
2. **各類代表作的「落點」很不一樣：**
    - **影片生成類**（Cosmos、Wan、SVD、Veo、Genie 3）：多用在 **T2 造資料、T4 評估、以及 I1／I3 當策略骨幹**。
    - **潛空間動力學類**（DreamerV3、Dreamer 4）：主要用在 **RL 與「預演挑動作」（FOREWARN）**，**沒有找到被大型商用 VLA 採用的公開證據**。
    - **JEPA 類**（V-JEPA 2）：用在 **零樣本規劃（I3）**，以及 2026 年起被拿來**當 VLA 的視覺編碼器**（JEPA-VLA）。
    - **3D／4D 類**（Marble、TesserAct、Waymo World Model 的 LiDAR 輸出）：目前主要是 **建模擬場景、評估**，直接進 VLA 訓練的案例還很少。
3. **智平方：主力產品 VLA 沒有公開使用世界模型，但它的開源平台有。** 2026-04 發布的開源框架 **AlphaBrain** 原生整合 **NVIDIA Cosmos Policy 權重**，並支援 **Cosmos 2／2.5、Wan 2.2、V-JEPA 2.1** 三類世界模型骨幹一鍵切換（[GitHub README](https://github.com/AlphaBrainGroup/AlphaBrain)）。這是**研究平台**；GOVLA／AlphaBrain 產品模型本身是否用到，**未找到公開證據**。Video2Act 只借影片擴散模型（HunyuanVideo）的特徵，不生成未來畫面。
4. **大廠產品的用法：**

| 產品 | 有沒有用世界模型 | 用在哪個階段 | 怎麼用 |
|---|---|---|---|
| **Figure Helix / Helix 02** | **未找到公開證據** | — | 官方頁只提遙操作資料、VLM 自動標註、物理模擬做 RL；沒提世界模型 |
| **GR00T N1** | ✅ | T2 造資料 | 用 **WAN2.1-I2V-14B** 從 88 小時真機資料生成 **827 小時**「神經軌跡」，再用潛在動作與 IDM 補標籤 |
| **GR00T N1.5** | ✅ | T1 輔助目標 + T2 造資料 | **FLARE** 未來表徵對齊損失；**DreamGen** 合成資料進預訓練 |
| **GR-2** | ✅ | T1 預訓練 | 3,800 萬段影片做「預測下一幀」生成式預訓練，再微調出動作 |
| **GR-3** | ❌（論文未使用） | — | 改成 VLM（Qwen2.5-VL-3B）+ 動作 DiT，搭配視覺語言資料與 VR 人類軌跡共訓 |

---

## 一、影片生成類

### 1. NVIDIA Cosmos（Predict / Transfer / Tokenizer）

| 誰用 | 怎麼用 | 階段 | 來源 |
|---|---|---|---|
| **Cosmos Policy**（NVIDIA） | 把 Cosmos-Predict2-2B 直接微調成策略：動作、未來狀態、價值都當「潛空間影格」生成，再用 Best-of-N 規劃 | I3 | [arXiv:2601.16163](https://arxiv.org/abs/2601.16163) |
| **智元 Genie Envisioner（GE-Base）** | 影片骨幹可選 LTX-Video 2B 或 **Cosmos2 2B** | T1 / I1 | [arXiv:2508.05635](https://arxiv.org/abs/2508.05635) |
| **DreamGen**（NVIDIA） | 比較了 WAN2.1、Hunyuan、CogVideoX、**Cosmos** 當資料工廠 | T2 | [arXiv:2505.12705](https://arxiv.org/abs/2505.12705) |
| **智平方 AlphaBrain** | 原生載入 Cosmos Policy 權重；Cosmos Predict 2 / 2.5（約 2.1B）可當世界模型骨幹 | 研究平台 | [GitHub](https://github.com/AlphaBrainGroup/AlphaBrain) |
| **1X** | World Model Challenge 的資料集用 **Cosmos Tokenizer** 壓縮 | 資料／競賽 | [NVIDIA 新聞稿 2025-01-07](https://www.globenewswire.com/news-release/2025/01/07/3005070/0/en/index.html) |
| **Agility Robotics** | CTO 表示用 Cosmos「生成與擴增擬真場景」，減少真實資料採集 | T2 | 同上 |
| **小鵬（人形機器人）、Hillbot、Skild AI** | 新聞稿只說「用 Cosmos 加速機器人開發」，**未說明細節** | 不明 | 同上 |
| **Waabi、Foretellix、Uber（自駕）** | 資料整理、生成測試情境與訓練資料 | T2 / T4 | 同上 |
| **Wayve** | 評估用 Cosmos 搜尋邊角案例 | T4 | 同上 |

> 注意：新聞稿也列了 Figure、Fourier、Galbot、Neura 等為早期採用者，但**沒寫用途**。不能據此說 Helix 用了 Cosmos。

### 2. 阿里 Wan（WAN2.1 / 2.2）

| 誰用 | 怎麼用 | 階段 | 來源 |
|---|---|---|---|
| **GR00T N1** | LoRA 微調 **WAN2.1-I2V-14B**，88 小時遙操作 → 生成 827 小時影片（約 10 倍，花約 10.5 萬 L40 GPU 小時）；與真實軌跡 1:1 共訓，RoboCasa +4.2%～+8.8%、真機平均 +5.8% | T2 | [arXiv:2503.14734](https://arxiv.org/abs/2503.14734) |
| **DreamGen → GR00T N1.5** | 主力影片模型是 WAN2.1；生成的神經軌跡進入 N1.5 預訓練，12 個新動詞成功率 13.1% → 38.3% | T2 | [arXiv:2505.12705](https://arxiv.org/abs/2505.12705)、[GR00T N1.5 官方頁](https://research.nvidia.com/labs/gear/gr00t-n1_5/) |
| **智平方 AlphaBrain** | Wan 2.2（約 5B）可當世界模型骨幹 | 研究平台 | [GitHub](https://github.com/AlphaBrainGroup/AlphaBrain) |

### 3. Stable Video Diffusion（SVD）、HunyuanVideo、OpenSora 等開源影片模型

| 骨幹 | 誰用 | 怎麼用 | 階段 | 來源 |
|---|---|---|---|---|
| SVD 1.5B | **VPP** | 只跑一次前向取 U-Net 特徵給擴散策略 | I1 | [arXiv:2412.14803](https://arxiv.org/abs/2412.14803) |
| SVD 1.5B | **Ctrl-World** | 動作條件多視角模擬器，評估並後訓練 π0 系列（38.7% → 83.4%） | T3 / T4 | [arXiv:2510.10125](https://arxiv.org/abs/2510.10125) |
| HunyuanVideo（13B 全模型，取前段層） | **智平方 Video2Act** | 借影片擴散模型的中間特徵給慢系統，不生成未來畫面 | I1 | [arXiv:2512.03044](https://arxiv.org/abs/2512.03044) |
| OpenSora | **WMPO** | 在像素級影片世界模型裡對 OpenVLA-OFT 做 GRPO | T3 | [arXiv:2511.09515](https://arxiv.org/abs/2511.09515) |
| Step1X-Edit | **智元 τ0-VLA** | 預測子任務完成畫面，在 VLA 沒把握時做 beam search | I3 | [arXiv:2608.16885](https://arxiv.org/abs/2608.16885) |

### 4. Google Veo

| 誰用 | 怎麼用 | 階段 | 來源 |
|---|---|---|---|
| **Gemini Robotics 團隊** | 以 Veo 為基礎做策略評估：一般表現、分佈外泛化、安全紅隊；用 8 個 Gemini Robotics 檢查點、1,600 次以上真機評估驗證排名一致 | T4 | [arXiv:2512.10675](https://arxiv.org/abs/2512.10675) |

**沒找到** Veo 被用來生成 VLA 訓練資料或放進推論迴圈的公開資料。

### 5. Genie 系列（Genie 1 / Genie 3）

| 誰用 | 用了什麼 | 怎麼用 | 階段 | 來源 |
|---|---|---|---|---|
| **Waymo World Model**（2026-02） | Genie 3 | 後訓練成同時輸出**相機 + LiDAR** 的駕駛模擬器；可用駕駛動作、場景佈局、文字控制；生成龍捲風、動物上路等罕見情境做安全評估 | T4（官方未說用來訓練 Driver） | [Waymo 官方部落格](https://waymo.com/blog/2026/02/the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation) |
| **SIMA 2**（DeepMind 通用遊戲代理人） | Genie 3 | 在 Genie 3 生成的擬真世界裡導航，並在其中**自我改進** | T3 / T4 | [arXiv:2512.04797](https://arxiv.org/abs/2512.04797) |
| **LAPA**（ICLR 2025） | Genie 1 的**潛在動作模型**想法 | 從沒有動作標籤的影片學離散潛動作，預訓練 VLA；真機平均 50.1%，高於 OpenVLA 的 43.9% | T1 | [arXiv:2410.11758](https://arxiv.org/abs/2410.11758) |
| **GR00T N1** | 同一條潛在動作路線（VQ-VAE，當成「LAPA 機體」） | 替人類影片與神經軌跡補上潛在動作標籤 | T1 / T2 | [arXiv:2503.14734](https://arxiv.org/abs/2503.14734) |

> Genie 1 本身沒有被當模擬器用在 VLA 上；它對 VLA 的影響是「**潛在動作**」這個概念。

---

## 二、潛空間動力學類

### 1. DreamerV3

| 誰用 | 怎麼用 | 階段 | 來源 |
|---|---|---|---|
| **FOREWARN**（CMU） | DreamerV3 式潛空間模型預測 100 個候選動作的 64 步後果，再由 Llama-3.2-11B-Vision 讀潛向量挑一個；比基礎模仿策略好 30% 以上 | I3 | [arXiv:2502.01828](https://arxiv.org/abs/2502.01828) |
| **DayDreamer**（UC Berkeley） | 用 Dreamer 演算法直接在真機上學：四足機器人約 1 小時學會走路、機械手臂學抓放 | T3（線上） | [arXiv:2206.14176](https://arxiv.org/abs/2206.14176) |
| 原論文 | 150+ 任務、Minecraft 從零挖鑽石 | 研究 | [arXiv:2301.04104](https://arxiv.org/abs/2301.04104) |

### 2. Dreamer 4

- 2B 潛空間模型，只用離線資料在 Minecraft 想像中訓練就挖到鑽石（[arXiv:2509.24527](https://arxiv.org/abs/2509.24527)）。
- **未找到**被 VLA 或機器人產品採用的公開證據。

### 3. 其他潛空間模型的 VLA 用法（參考）

- **TD-MPC2**（最大 317M）：潛空間 MPC，單一代理人 80 個任務（[arXiv:2310.16828](https://arxiv.org/abs/2310.16828)）。
- **VLA-Reasoner**：600M iVideoGPT 式模型 + MCTS 幫 OpenVLA／π0-FAST 挑動作（[arXiv:2509.22643](https://arxiv.org/abs/2509.22643)）。

**一句話**：潛空間動力學是「RL 和規劃」的工具，學界常用來幫 VLA 做預演，但**沒有大型商用 VLA 公開說自己用 Dreamer**。

---

## 三、JEPA 類（V-JEPA 2）

| 誰用 | 怎麼用 | 階段 | 來源 |
|---|---|---|---|
| **V-JEPA 2-AC**（Meta） | 300M 動作條件預測器 + CEM 規劃，零樣本抓放 65–80% | I3 | [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) |
| **JEPA-VLA**（2026-02） | 把 V-JEPA 2 的預測式影片嵌入**加進現有 VLA 當視覺表徵**；在 LIBERO、LIBERO-plus、RoboTwin2.0、真機都有提升（摘要未給數字） | T1 / 推論時當編碼器 | [arXiv:2602.11832](https://arxiv.org/abs/2602.11832) |
| **VLA-JEPA**（2026-02） | 借 JEPA **訓練目標**：學生只看當前畫面，預測未來畫面的潛表徵；兩階段（JEPA 預訓練 → 微調動作頭） | T1 | [arXiv:2602.10098](https://arxiv.org/abs/2602.10098) |
| **智平方 AlphaBrain** | V-JEPA 2.1（約 1.8B）可當世界模型骨幹 | 研究平台 | [GitHub](https://github.com/AlphaBrainGroup/AlphaBrain) |

**趨勢**：V-JEPA 2 正在從「規劃器」變成「**VLA 的視覺編碼器**」。理由是它的表徵捨棄了不可預測的雜訊，保留了跟任務有關的時間動態。

---

## 四、3D／4D 類

| 誰用 | 用了什麼 | 怎麼用 | 階段 | 來源 |
|---|---|---|---|---|
| **NVIDIA Isaac Sim 教學**（2025-12） | World Labs **Marble** | 文字或圖片 → 3D 高斯點雲（視覺）+ 碰撞網格（物理）→ 匯入 Isaac Sim 讓機器人跑 | 建模擬場景（T4 / 為 RL 準備環境） | [NVIDIA 技術部落格](https://developer.nvidia.com/blog/simulate-robotic-environments-faster-with-nvidia-isaac-sim-and-world-labs-marble) |
| **BEHAVIOR-1K、RoboSuite 研究者**（2025-11） | Marble | 生成住家、倉庫場景，在 Isaac Sim、MuJoCo 跑 ANYmal、Spot、UR10、Franka；官方稱場景整理時間降 90% 以上 | 建模擬場景 | [World Labs 案例](https://www.worldlabs.ai/case-studies/1-robotics) |
| **TesserAct**（2025） | 自家 4D 世界模型 | 微調影片模型同時預測 RGB、深度、法向量，重建 4D 場景，再學逆動力學模型出動作 | 研究（I2 類） | [arXiv:2504.20995](https://arxiv.org/abs/2504.20995) |
| **Waymo World Model** | Genie 3 後訓練 | 輸出**可互動的 4D LiDAR 點雲**，把 2D 影片知識轉成 3D 感測器輸出 | T4 | [Waymo 官方部落格](https://waymo.com/blog/2026/02/the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation) |

**一句話**：3D／4D 世界模型現在主要是「**快速造模擬場景**」，再交給傳統物理模擬器去跑機器人；直接拿來訓練 VLA 的公開案例還很少。

---

## 五、智平方到底有沒有用世界模型？

### 結論

| 層面 | 有沒有用 | 證據 |
|---|---|---|
| **產品 VLA（GOVLA／AlphaBrain 大腦）** | **未找到公開證據** | 產品架構描述是「全域全身 VLA」；[虎嗅 2026 報導](https://www.huxiu.com/article/4873816.html)只提到業界在討論「VLA → 世界模型」範式切換，智平方的回應是持續升級 VLA |
| **Video2Act 論文** | **借用一部分** | 用 HunyuanVideo 的前段層特徵輔助慢系統；**不生成未來畫面、不做想像規劃**（[arXiv:2512.03044](https://arxiv.org/abs/2512.03044)）。屬於 I1 類「借眼睛」 |
| **NeuroVLA** | 否 | 類腦三層架構 + SNN，與世界模型無關（[arXiv:2601.14628](https://arxiv.org/abs/2601.14628)） |
| **AlphaBrain 開源平台**（2026-04-22 發布） | **有，而且四種骨幹** | 原生整合 **Cosmos Policy 原始權重**；V-JEPA 2.1（~1.8B）、Cosmos Predict 2.5（~2.1B）、Cosmos Predict 2（~2.1B）、Wan 2.2（~5B）一鍵切換，共用動作解碼器（[GitHub README](https://github.com/AlphaBrainGroup/AlphaBrain)、[京報網報導](https://news.bjd.com.cn/2026/04/22/11704136.shtml)、[中關村在線](https://news.zol.com.cn/1184/11840628.html)） |

### 怎麼解讀

- AlphaBrain 平台把世界模型當「**可插拔的策略骨幹**」：同一個任務可以換不同世界模型比較，用法和 Cosmos Policy 一樣（I3 類：世界模型直接當策略，並可預演）。報導原話是讓機器人「在行動前預演多種可能路徑，選擇最優解」。
- 但這是**開源研究框架**（README 寫明主要 fork 自 starVLA），**不等於**他們的量產機器人在用。目前沒有看到智平方發表「自研世界模型」的論文或產品。
- 所以更新後的定位：**智平方是 VLA 公司，已經在開源平台上把第三方世界模型（Cosmos、Wan、V-JEPA）整合進來；自家產品是否使用未公開。**

---

## 六、大廠 VLA 產品：在什麼階段、怎麼用世界模型

### Figure Helix（2025-02）與 Helix 02（2026-01）

- **Helix**：S2 是 7B VLM（7–9 Hz），S1 是 80M Transformer（200 Hz）；約 500 小時遙操作資料，用 VLM 自動回填指令標註；S1 的視覺骨幹「完全在模擬中預訓練」（[官方頁](https://www.figure.ai/news/helix)）。
- **Helix 02**：加入 S0（10M 參數、1 kHz 全身控制器），在 20 萬個以上平行模擬環境中做 sim-to-real RL，並用 1,000 小時以上人體動作資料（[官方頁](https://www.figure.ai/news/helix-02)）。
- **結論**：兩篇官方頁都**沒有提到世界模型或影片預測**。他們用的是傳統物理模擬器，不是學出來的世界模型。

### NVIDIA GR00T N1（2025-03）

- **T2 資料工廠**：WAN2.1-I2V-14B 生成 827 小時「神經影片」，進入預訓練資料（[arXiv:2503.14734](https://arxiv.org/abs/2503.14734)）。
- **T1 潛在動作**：用 VQ-VAE 從連續影格抽潛在動作，給人類影片和神經軌跡當監督訊號（Genie／LAPA 路線）。
- **推論時**：只跑 VLA（I0）。

### NVIDIA GR00T N1.5（2025-06）

- **T1 輔助目標**：**FLARE** 在動作 DiT 中加入未來 token，對齊未來觀測的嵌入，不生成畫面（[arXiv:2505.15659](https://arxiv.org/abs/2505.15659)）。
- **T2 資料工廠**：**DreamGen** 神經軌跡進預訓練，12 個新動詞成功率 13.1% → 38.3%（[官方頁](https://research.nvidia.com/labs/gear/gr00t-n1_5/)）。
- **推論時**：只跑 VLA（I0）。

### 字節 GR-2（2024-10）與 GR-3（2025-07）

- **GR-2**：**T1 生成式預訓練**。3,800 萬段網路影片（500 億 token）學「預測未來畫面」，再用機器人軌跡同時微調影片生成與動作（[arXiv:2410.06158](https://arxiv.org/abs/2410.06158)）。這是「世界模型直接當 VLA 預訓練」的代表。
- **GR-3**：**拿掉了**影片預測。改用 Qwen2.5-VL-3B + 動作 DiT（約 4B），靠視覺語言資料和 VR 人類軌跡共訓（[arXiv:2507.15493](https://arxiv.org/abs/2507.15493)）。論文只在相關研究提到 GR-2 的未來預測路線。

### 對照：其他公開用法

| 產品 | 階段 | 怎麼用 | 來源 |
|---|---|---|---|
| Gemini Robotics | T4 | Veo 當策略評估器 | [arXiv:2512.10675](https://arxiv.org/abs/2512.10675) |
| 1X NEO | I2 + T4 | 14B 影片模型想像 → IDM 出動作；也當評估器 | [1X 官方](https://1x.tech/discover/world-model-self-learning) |
| 智元 GE / τ0-VLA | T1 / I1 / T4 / I3 | GE-Base 預訓練、GE-Act 單步特徵、GE-Sim 評估、τ0 預演挑動作 | [arXiv:2508.05635](https://arxiv.org/abs/2508.05635)、[arXiv:2608.16885](https://arxiv.org/abs/2608.16885) |
| π0 / π0.5 | — | 公開論文沒有使用世界模型 | [π0.5 arXiv:2504.16054](https://arxiv.org/abs/2504.16054) |

---

## 七、總覽：四類代表作 × 用途

| 類別 | 代表作 | 誰在用 | 主要階段 |
|---|---|---|---|
| 影片生成 | Cosmos | Cosmos Policy、GE、AlphaBrain、Agility、自駕公司 | T2、T4、I3 |
| 影片生成 | Wan | **GR00T N1／N1.5（DreamGen）**、AlphaBrain | T2 |
| 影片生成 | SVD | VPP、Ctrl-World | I1、T3、T4 |
| 影片生成 | Veo | Gemini Robotics 評估 | T4 |
| 影片生成 | Genie 3 | Waymo、SIMA 2 | T4、T3 |
| 影片生成 | Genie 1 | 潛在動作概念 → LAPA、GR00T N1 | T1 |
| 潛空間 | DreamerV3 | FOREWARN、DayDreamer | I3、T3 |
| 潛空間 | Dreamer 4 | 未找到外部採用 | — |
| JEPA | V-JEPA 2 | V-JEPA 2-AC、JEPA-VLA、AlphaBrain | I3、T1／編碼器 |
| 3D／4D | Marble | Isaac Sim、BEHAVIOR-1K、RoboSuite 研究者 | 建模擬場景 |
| 3D／4D | TesserAct | 研究 | I2 類 |

**判斷**：

1. 想**造資料**：選開源、可微調的影片模型（Wan、Cosmos），這是 GR00T 的實際做法。
2. 想讓**推論**受益：Cosmos Policy（I3）和 VPP／Video2Act（I1）是最成熟的開源路線；V-JEPA 2 當編碼器是 2026 年的新方向。
3. 想**評估**：Veo、Genie 3 效果最好，但只有 Google 體系能用；外部團隊用 Ctrl-World、Cosmos 替代。
