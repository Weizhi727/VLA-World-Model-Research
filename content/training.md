# 訓練、資料、輸入輸出、使用與評估

<p class="lede">五個實作問題，每題都把 <span class="tag vla">VLA</span> 和 <span class="tag wm">WM</span>（世界模型）並排對照：怎麼訓練、資料怎麼建、輸入輸出是什麼、實際怎麼用、怎麼評估。</p>

!!! key "最核心的差別"
    VLA 學的是「看到這個、聽到這句話，**該做什麼動作**」（策略 π(a | o, l)）；世界模型學的是「現在是這樣、做了這個動作，**世界接下來會變怎樣**」（動態 p(o′ | o, a)）。所以 **VLA 要「好的示範」，世界模型要「多樣的後果，包含失敗」**。後面五題的差異幾乎都由此而來。

## 一張表看完

| | <span class="tag vla">VLA</span> | <span class="tag wm">World Model</span> |
|---|---|---|
| **訓練** | VLM 預訓練 → 大量機器人軌跡預訓練（常與網路資料共訓）→ 少量示範微調 →（新趨勢）RL 後訓練。本質是**模仿學習** | 自監督預測未來：像素、token、潛空間三種路線。先用海量影片學「世界怎麼動」，再用帶動作的資料學「動作造成什麼」 |
| **資料** | (影像, 語言指令, 本體狀態, 動作) 的成功示範軌跡；主要靠遙操作，輔以模擬、合成與人類影片 | 數百萬小時影片＋帶動作標籤的互動資料（遊戲、駕駛、機器人，失敗案例很有價值） |
| **輸入** | 1–3 路相機影像＋語言指令＋關節／夾爪狀態 | 過去的觀測（影格或潛狀態）＋動作（或文字、潛在動作） |
| **輸出** | 動作序列（action chunk），例如未來 50 步 × 7–14 維 | 未來的觀測（影片影格或潛在表徵），有時加上獎勵、是否結束 |
| **使用** | 部署在機器人上閉環控制；新機器人用 LoRA 微調 50–200 條示範 | 想像中訓練 RL、MPC 規劃、合成訓練資料、當模擬器評估策略、遊戲與駕駛模擬 |
| **評估** | 真機成功率（多次重複、盲測）＋模擬基準（LIBERO、SimplerEnv、CALVIN）＋泛化軸 | 畫質（FVD 等）＋物理一致性＋動作可控性＋**下游有用度** |

## Q1 怎麼訓練？

!!! key "重點"
    現代 VLA 幾乎都是「站在 VLM 肩膀上」的多階段模仿學習，關鍵技術選擇是**動作怎麼表示**（離散 token 還是連續的擴散／flow matching）。世界模型則是「預測下一刻」的自監督學習，關鍵選擇是**在哪個空間預測**（像素、離散 token 或抽象潛空間）。

### VLA 的四個階段

<figure class="dg">
<svg viewBox="0 0 800 170" role="img" aria-label="VLA 四階段訓練流程">
<rect class="n" x="10" y="20" width="175" height="110" rx="12"/>
<text x="97" y="48" text-anchor="middle" class="b vla">0 · VLM 預訓練</text>
<text x="97" y="74" text-anchor="middle" class="s">網路圖文資料</text>
<text x="97" y="94" text-anchor="middle" class="s">通常直接用現成 VLM</text>
<text x="97" y="114" text-anchor="middle" class="s">PaliGemma、Qwen-VL…</text>
<rect class="n vla" x="215" y="20" width="175" height="110" rx="12"/>
<text x="302" y="48" text-anchor="middle" class="b vla">1 · 機器人預訓練</text>
<text x="302" y="74" text-anchor="middle" class="s">數十萬到上百萬條</text>
<text x="302" y="94" text-anchor="middle" class="s">跨機器人軌跡</text>
<text x="302" y="114" text-anchor="middle" class="s">＋網路資料共訓</text>
<rect class="n" x="420" y="20" width="175" height="110" rx="12"/>
<text x="507" y="48" text-anchor="middle" class="b vla">2 · 任務微調</text>
<text x="507" y="74" text-anchor="middle" class="s">數十到數百條</text>
<text x="507" y="94" text-anchor="middle" class="s">高品質示範</text>
<text x="507" y="114" text-anchor="middle" class="s">全參數或 LoRA</text>
<rect class="n key" x="625" y="20" width="165" height="110" rx="12"/>
<text x="707" y="48" text-anchor="middle" class="b key">3 · RL 後訓練</text>
<text x="707" y="74" text-anchor="middle" class="s">2025 年起的新方向</text>
<text x="707" y="94" text-anchor="middle" class="s">真機、模擬或</text>
<text x="707" y="114" text-anchor="middle" class="s">世界模型裡試錯</text>
<path class="ar vla" d="M185,75 H213"/><path class="ar vla" d="M390,75 H418"/><path class="ar vla" d="M595,75 H623"/>
<text x="400" y="160" text-anchor="middle" class="s">co-training：預訓練時混入網路 VQA 資料，避免模型忘掉常識</text>
</svg>
</figure>

**動作怎麼變成可訓練的目標（最關鍵的設計）**

| 方法 | 做法 | 損失函數 | 代表 |
|---|---|---|---|
| 均勻分箱 token | 每個動作維度切成 256 個區間，對應到詞表裡的 token，像生成文字一樣逐一輸出 | 交叉熵（next-token） | [RT-2](https://arxiv.org/abs/2307.15818)、[OpenVLA](https://arxiv.org/abs/2406.09246) |
| 壓縮 token | 對動作序列做 DCT 頻域轉換再 BPE 壓縮，token 數少很多，高頻動作也學得好 | 交叉熵 | [FAST（π0-FAST）](https://arxiv.org/abs/2501.09747) |
| Flow matching／擴散動作專家 | VLM 產生特徵，另一個小網路從噪聲逐步去噪出整段連續動作 | 速度場回歸／去噪 MSE | [π0](https://arxiv.org/abs/2410.24164)、[GR00T N1](https://arxiv.org/abs/2503.14734)、[Diffusion Policy](https://arxiv.org/abs/2303.04137) |
| 連續回歸＋平行解碼 | 一次輸出整段動作，用 L1 損失直接回歸，推論快很多 | L1 | [OpenVLA-OFT](https://arxiv.org/abs/2502.19645) |
| 混合（知識隔離） | VLM 用 FAST token 訓練，動作專家用 flow matching，並阻斷動作專家的梯度回流到 VLM | 交叉熵＋flow matching | [π0.5＋KI](https://arxiv.org/abs/2505.23705) |

另一個幾乎所有模型都用的技巧是 **action chunking**：一次預測未來 H 步（例如 50 步，約 1 秒）而不是一步，減少誤差累積、讓動作更平滑。這來自 [ACT／ALOHA](https://arxiv.org/abs/2304.13705)。

**規模參考**

- **OpenVLA（7B）**：Open X-Embodiment 中約 97 萬條軌跡，64 張 A100 訓練約 14 天。
- **π0（3.3B）**：約 1 萬小時、7 種機器人、68 個任務的自有資料＋OXE 開源資料。
- **π0.5**：加入多環境家庭資料、網路資料、「子任務文字標註」的高層預測，讓模型能在沒見過的家裡做清潔（[論文](https://arxiv.org/abs/2504.16054)）。
- **RL 後訓練**：Physical Intelligence 的 [π*0.6（Recap）](https://www.pi.website/blog/pistar06) 結合示範、人類介入修正與自主經驗，以學到的價值函數做優勢加權訓練。

### 世界模型的三條訓練路線

- **A. 潛空間動態模型（為 RL 而生）**：編碼器把觀測壓成潛狀態 z，遞迴網路（RSSM）學 z<sub>t</sub>, a<sub>t</sub> → z<sub>t+1</sub>，同時預測獎勵與是否結束。損失＝重建＋KL＋獎勵預測。策略**完全在想像的軌跡裡**訓練。代表：[World Models](https://arxiv.org/abs/1803.10122)、[DreamerV3](https://arxiv.org/abs/2301.04104)、[TD-MPC2](https://arxiv.org/abs/2310.16828)（不重建畫面）。
- **B. JEPA：在表徵空間預測**：不生成像素，遮住影片的一部分，讓模型預測被遮部分的**表徵**。代表：[V-JEPA 2](https://arxiv.org/abs/2506.09985)：先在超過 100 萬小時網路影片上自監督預訓練，再只用約 62 小時 DROID 機器人資料訓練動作條件的 V-JEPA 2-AC。
- **C. 影片生成式**：把世界模型當「可被動作控制的影片生成器」。**擴散／flow**（在連續潛空間去噪）或**自回歸**（VQ tokenizer 把影格變成離散 token，再 next-token 預測）。代表：[Cosmos](https://arxiv.org/abs/2501.03575)、[GAIA-1](https://arxiv.org/abs/2309.17080)、[UniSim](https://arxiv.org/abs/2310.06114)、[DIAMOND](https://arxiv.org/abs/2405.12399)、[GameNGen](https://arxiv.org/abs/2408.14837)。
- **沒有動作標籤怎麼辦？潛在動作**：網路影片沒有記錄「按了哪個鍵」。[Genie](https://arxiv.org/abs/2402.15391) 用潛在動作模型（LAM）從前後兩幀**自己推斷**出 8 種離散動作，從約 3 萬小時遊戲影片無監督學出可操控的世界。[LAPA](https://arxiv.org/abs/2410.11758) 把同樣想法用在 VLA 預訓練上。

**典型的影片世界模型訓練流程**

1. **Tokenizer 訓練**：先訓練影片編碼器（連續 VAE 或離散 VQ），把影片壓縮 8–16 倍以上，讓後續模型算得動。
2. **大規模預訓練**：在數百萬小時、無動作標籤的影片上，學「給定過去影格（和文字），預測未來影格」，學到物理常識和物體運動。
3. **動作條件後訓練**：在帶動作的資料（機器人、駕駛、遊戲）上微調，把動作注入模型（加到時間步 embedding 或 cross-attention），學「動作 → 後果」。
4. **（選用）蒸餾加速**：把多步去噪蒸餾成少步才能即時互動，例如 [Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/) 可 720p、24 fps 即時生成。

## Q2 資料集怎麼構建？

!!! key "重點"
    機器人資料是整個領域最大的瓶頸，因為不像文字和圖片可以從網路爬。業界的解法是一座「**資料金字塔**」。世界模型的資料工程重點則在**海量影片的清洗與標註**，以及**保留失敗案例**。

<figure class="dg">
<svg viewBox="0 0 800 300" role="img" aria-label="VLA 資料金字塔">
<path d="M400,20 L470,95 L330,95 Z" class="n vla"/>
<path d="M330,100 L470,100 L545,180 L255,180 Z" class="n wm"/>
<path d="M250,185 L550,185 L640,280 L160,280 Z" class="n"/>
<text x="400" y="80" text-anchor="middle" class="b">真機遙操作</text>
<text x="400" y="138" text-anchor="middle" class="b">手持採集器・模擬・</text>
<text x="400" y="160" text-anchor="middle" class="b">世界模型合成</text>
<text x="400" y="225" text-anchor="middle" class="b">人類第一人稱影片</text>
<text x="400" y="250" text-anchor="middle" class="b">網路圖文與影片</text>
<text x="490" y="50" class="s">ALOHA、DROID：品質最高、最貴</text>
<text x="560" y="135" class="s">UMI、MimicGen、RoboCasa、DreamGen</text>
<text x="560" y="155" class="s">量大、有標註，但有 sim2real 差距</text>
<text x="650" y="235" class="s">Ego4D、VQA</text>
<text x="650" y="255" class="s">量最大，沒有機器人動作</text>
<path class="ar" d="M120,280 V30"/>
<text x="110" y="40" text-anchor="end" class="s">精準</text>
<text x="110" y="58" text-anchor="end" class="s">成本高</text>
<text x="110" y="268" text-anchor="end" class="s">量大</text>
</svg>
<figcaption>VLA 的資料金字塔：頂層貴但精確，底層量大但沒有動作標籤。GR00T N1 的訓練配方就是這座金字塔的典型例子。</figcaption>
</figure>

### VLA 資料從哪裡來

| 來源 | 怎麼收 | 優缺點 | 例子 |
|---|---|---|---|
| **真機遙操作** | 人用主從手臂、VR 頭顯、SpaceMouse 遠端操控機器人，同步記錄相機、關節與指令 | 品質最高、動作空間精確；但貴、慢 | [ALOHA](https://arxiv.org/abs/2304.13705)、[DROID](https://arxiv.org/abs/2403.12945) |
| **手持採集器** | 人拿著裝了相機的夾爪在真實環境操作，不需要機器人在場 | 便宜、可大量部署；需處理與機器人的形態差 | [UMI](https://arxiv.org/abs/2402.10329) |
| **模擬／程序生成** | 在 Isaac、MuJoCo 等模擬器中用腳本或少量示範自動擴增 | 近乎無限、自帶標註；有 sim-to-real 差距 | [MimicGen](https://arxiv.org/abs/2310.17596)、[RoboCasa](https://arxiv.org/abs/2406.02523) |
| **世界模型合成** | 用影片世界模型生成新場景的軌跡，再用逆動力學模型補上動作標籤 | 能擴展到新動詞與新環境；物理正確性待驗證 | [DreamGen](https://arxiv.org/abs/2505.12705) |
| **人類影片** | 第一人稱影片（頭戴相機），提供「人怎麼操作物體」的先驗 | 量大且多樣；沒有機器人動作標籤 | [Ego4D](https://arxiv.org/abs/2110.07058) |
| **網路圖文** | VQA、圖片描述、物體定位資料，與機器人資料共訓 | 保住語言與常識能力；不直接教動作 | RT-2、π0.5 的共訓配方 |

### 一條軌跡長什麼樣（RLDS／LeRobot 格式）

```python
episode = {
  "language_instruction": "把紅色杯子放進水槽",
  "steps": [                                   # 以 5–50 Hz 記錄，每條數十到數百步
    {
      "observation": {
        "image_primary": uint8[224, 224, 3],   # 第三人稱相機
        "image_wrist":   uint8[224, 224, 3],   # 腕部相機
        "state":         float32[8],           # 關節角度或末端位姿＋夾爪開合
      },
      "action":  float32[7],                   # Δx, Δy, Δz, Δroll, Δpitch, Δyaw, gripper
      "is_terminal": False,
    },
    ...
  ],
  "success": True                              # 有些資料集會標註成功／失敗
}
```

格式標準：[RLDS](https://arxiv.org/abs/2111.02767)（Google，OXE 使用）、[LeRobot Dataset](https://github.com/huggingface/lerobot)（Hugging Face，以 Parquet＋MP4 存放）。

### 從原始錄影到可訓練資料

1. **對齊時間**：多路相機與關節訊號時間戳同步，統一重採樣頻率。
2. **清理**：刪掉機器人靜止不動的片段、失敗或操作者失誤的軌跡（若是純模仿學習）。
3. **統一動作空間**：跨機器人時通常轉成末端執行器的相對位移，或保留各自關節空間但補零到固定維度。
4. **正規化**：按每個資料集的 1%–99% 分位數把動作縮放到 [-1, 1]，避免離群值主導。
5. **語言標註**：補寫或改寫任務指令；π0.5 等模型還會標註細粒度子任務（「拿起海綿」「擦桌面」），可以用 VLM 自動重新標註。
6. **配比**：決定各資料集的採樣權重。OpenVLA、Octo 都花了大量功夫調配 OXE 子集比例。

### 主要公開資料集

| 資料集 | 規模 | 特點 |
|---|---|---|
| [Open X-Embodiment](https://arxiv.org/abs/2310.08864) | 100 萬條以上軌跡 | 21 個機構、22 種機器人、60 個資料集匯整；VLA 預訓練的標準起點 |
| [DROID](https://arxiv.org/abs/2403.12945) | 7.6 萬條／350 小時 | 同一型號 Franka，564 個場景，場景多樣性高 |
| [BridgeData V2](https://arxiv.org/abs/2308.12952) | 6 萬條 | 低成本 WidowX 手臂，24 種環境；學術界最常用的評估平台之一 |
| [RT-1 資料](https://arxiv.org/abs/2212.06817) | 13 萬條 | Google 移動操作機器人，700+ 指令，17 個月採集 |
| [LeRobot Hub](https://github.com/huggingface/lerobot) | 持續增加 | 社群上傳的低成本機器人（SO-100 等）資料，格式統一 |

### 世界模型的資料怎麼建

**無動作的海量影片（學物理常識）**，以 [Cosmos](https://arxiv.org/abs/2501.03575) 的管線為例：收集約 2,000 萬小時原始影片 → 鏡頭切分 → 過濾低畫質、靜止、字幕過多、純動畫 → 用嵌入向量去重 → 用 VLM 為每段寫文字描述 → 按類別平衡配比，最終約上億個片段。

**帶動作的互動資料（學因果）**

- **遊戲**：讓 RL 智能體玩遊戲同時記錄動作與畫面（[GameNGen](https://arxiv.org/abs/2408.14837) 用這種方式蒐集 DOOM 資料）。
- **駕駛**：車隊日誌包含方向盤、油門、速度與多相機影像（[GAIA-1](https://arxiv.org/abs/2309.17080) 用了約 4,700 小時倫敦駕駛資料）。
- **機器人**：沿用 VLA 的軌跡資料，但**要特別保留失敗與隨機探索**，否則世界模型只會預測成功，拿來評估策略時會過度樂觀。
- **無標註影片**：用潛在動作模型或逆動力學模型自動補動作。

## Q3 輸入輸出是什麼？

!!! key "重點"
    VLA 的輸出是**直接給馬達的控制訊號**；世界模型的輸出是**對未來的預測**，本身不會讓機器人動起來，需要搭配策略或規劃器。

### <span class="tag vla">VLA</span> π(a<sub>t:t+H</sub> | o<sub>t</sub>, l)

- **輸入**
    - **影像**：1–3 路 RGB，常見是 1 個第三人稱＋1–2 個腕部相機，縮放到 224×224 左右。
    - **語言指令**：「把襪子摺好放進抽屜」。
    - **本體感知（proprioception）**：關節角度、末端位姿、夾爪開合度。
    - （部分模型）歷史幾幀影像、深度圖、觸覺。
- **輸出**
    - **動作 chunk**：形狀 [H, D]，例如 π0 是 50 步 × 最多 18 維。
    - D 依機器人而定：單臂常用 7 維（6 自由度位移＋夾爪），雙臂 14 維，人形可達 30 維以上。
    - 控制頻率：RT-2／OpenVLA 約 3–6 Hz，π0／GR00T 可達 50 Hz 以上。
    - （分層或雙系統模型）π0.5 會先輸出子任務文字，再輸出低層動作。

```text
輸入：
  images = [cam_high, cam_left_wrist, cam_right_wrist]   # 各 224×224×3
  prompt = "fold the towel"
  state  = float32[14]        # 雙臂關節角
輸出：
  actions = float32[50, 14]   # 未來 50 步的關節目標（50 Hz 下 ≈ 1 秒）
```

### <span class="tag wm">WM</span> p(o<sub>t+1:t+k</sub> | o<sub>≤t</sub>, a<sub>t:t+k</sub>)

- **輸入**：過去觀測（前幾幀影像，或已編碼的潛狀態）＋條件訊號（機器人動作向量、駕駛操控、遊戲按鍵、文字描述、相機軌跡或潛在動作代碼）。
- **輸出**：

| 模型 | 輸出 |
|---|---|
| DreamerV3 | 下一個潛狀態＋獎勵＋是否結束 |
| V-JEPA 2-AC | 未來影格的表徵向量（非像素） |
| Cosmos、UniSim | 未來數秒的影片影格 |
| Genie 3 | 可即時互動的 720p 畫面串流 |

更完整的「四類世界模型輸入輸出對照」見 [05 世界模型四類與五種角色](world-model-roles.html)。

## Q4 使用方法是什麼？

!!! key "重點"
    VLA 的標準用法是「**下載開源預訓練權重 → 在自己的機器人上收少量示範 → 微調 → 閉環部署**」。世界模型很少單獨使用，它是**其他系統的工具**：訓練場、規劃器、資料工廠或評估器。

### VLA：微調與閉環部署

1. **微調到自己的機器人**：收集 50–200 條目標任務的遙操作示範，轉成 LeRobot 或 RLDS 格式；定義新機器人的動作維度與正規化統計值；用 LoRA 或全參數微調。開源工具：[openpi](https://github.com/Physical-Intelligence/openpi)（π0／π0.5）、[OpenVLA](https://github.com/openvla/openvla)、[LeRobot](https://github.com/huggingface/lerobot)（含 SmolVLA、ACT、Diffusion Policy）、[Isaac GR00T](https://github.com/NVIDIA/Isaac-GR00T)。
2. **閉環部署**：

```python
while not done:
    obs = robot.get_observation()            # 讀相機與關節
    chunk = policy.infer(obs, instruction)   # 輸出 [H, D] 動作
    for a in chunk[:k]:                      # 只執行前 k 步（receding horizon）
        robot.apply(a)
        sleep(1 / control_hz)
```

- **執行策略**：每次只執行 chunk 的前一部分再重新推論；或用 temporal ensembling 把重疊的 chunk 加權平均；或用 real-time chunking 在執行當下非同步推論下一段，避免動作卡頓。
- **推論架構**：大模型通常跑在旁邊的 GPU 伺服器，機器人透過網路收動作（openpi 就是 client-server 架構）；邊緣部署則需量化與蒸餾。
- **安全**：關節限位、速度上限、人類隨時可按急停。

### 世界模型的五種用法

| 用法 | 怎麼做 | 例子 |
|---|---|---|
| **想像中訓練** | 策略在世界模型產生的虛擬軌跡中做 RL，不必碰真實環境 | [DreamerV3](https://arxiv.org/abs/2301.04104) |
| **模型預測控制（MPC）** | 取樣多組候選動作，在世界模型中各自推演，挑最接近目標的一組執行，每步重新規劃 | [V-JEPA 2-AC](https://arxiv.org/abs/2506.09985)、[TD-MPC2](https://arxiv.org/abs/2310.16828) |
| **合成訓練資料** | 生成新場景、新物體、新動作的影片，補上動作標籤後拿去訓練 VLA | [DreamGen](https://arxiv.org/abs/2505.12705) |
| **策略評估** | 把 VLA 接到世界模型裡閉環執行，用生成結果判斷成敗，取代昂貴的真機測試 | [Veo 評測（arXiv:2512.10675）](https://arxiv.org/abs/2512.10675)、1X |
| **互動模擬與內容** | 遊戲引擎、自駕罕見情境生成、智能體訓練場 | [GameNGen](https://arxiv.org/abs/2408.14837)、[GAIA-1](https://arxiv.org/abs/2309.17080)、[Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/) |

MPC 規劃的核心迴圈（以 V-JEPA 2-AC 的 CEM 為例）：

```python
for step in range(T):
    z = encoder(obs); z_goal = encoder(goal_image)
    candidates = sample_actions(N=300, horizon=H)
    for _ in range(iters):                        # CEM 迭代
        costs = [dist(world_model.rollout(z, a), z_goal) for a in candidates]
        candidates = refit_gaussian(top_k(candidates, costs))
    robot.apply(best(candidates)[0])              # 只執行第一步
    obs = robot.get_observation()
```

## Q5 怎麼評估效能？

!!! key "重點"
    VLA 的黃金標準永遠是**真機成功率**，但它昂貴、難重現、樣本少，因此出現模擬基準與分散式評估。世界模型有一個常見陷阱：**畫面好看 ≠ 物理正確 ≠ 對決策有用**，必須多層評估，最後一定要看下游任務。

### VLA 評估

**真機評估怎麼做才可信**

- **成功率**：每個任務重複 10–20 次以上，固定初始擺放的分布；常加上**部分得分**（抓到了但沒放好得 0.5 分）。
- **A/B 盲測**：同一組初始條件下輪流測試不同模型，評分者不知道是哪個模型。
- **泛化軸**：分別量測在新背景／光照、新物體、新位置、新指令說法、新機器人下的成功率下降多少。
- **其他指標**：完成時間、推論延遲與控制頻率、人類介入次數、長時任務平均完成子任務數。
- **統計提醒**：20 次試驗、成功率 50% 時，95% 信賴區間約 ±22%。兩個模型差 10% 往往不具統計意義。

**模擬基準**

| 基準 | 內容 | 指標 | 備註 |
|---|---|---|---|
| [LIBERO](https://arxiv.org/abs/2306.03310) | 4 個套件（空間、物體、目標、長時），各 10 個任務 | 平均成功率 | 最常被引用；頂尖模型已超過 95%，接近飽和 |
| [SimplerEnv](https://arxiv.org/abs/2405.05941) | 在模擬中重現 Google Robot 與 WidowX 的真實場景 | 成功率＋與真機的相關性 | 目的是讓模擬分數能預測真機排名 |
| [CALVIN](https://arxiv.org/abs/2112.03227) | 連續完成 5 個語言指定的子任務 | 平均連續完成長度（0–5） | 測長時與指令跟隨 |
| [RoboCasa](https://arxiv.org/abs/2406.02523) | 大規模廚房場景與日常任務 | 成功率 | 場景多樣性高 |
| [RoboArena](https://robo-arena.github.io/) | 多個機構在各自的 DROID 機器人上做成對盲測 | 類 Elo 排名 | 用分散式真機評估解決重現性 |

### 世界模型的四層評估

<figure class="dg">
<svg viewBox="0 0 800 120" role="img" aria-label="世界模型四層評估">
<rect class="n" x="10" y="20" width="180" height="80" rx="10"/>
<text x="100" y="52" text-anchor="middle" class="b">1 視覺品質</text>
<text x="100" y="76" text-anchor="middle" class="s">FVD、VBench</text>
<rect class="n" x="210" y="20" width="180" height="80" rx="10"/>
<text x="300" y="52" text-anchor="middle" class="b">2 物理一致性</text>
<text x="300" y="76" text-anchor="middle" class="s">Physics-IQ、物體恆存</text>
<rect class="n" x="410" y="20" width="180" height="80" rx="10"/>
<text x="500" y="52" text-anchor="middle" class="b">3 動作可控性</text>
<text x="500" y="76" text-anchor="middle" class="s">換動作，結果跟著變嗎</text>
<rect class="n wm" x="610" y="20" width="180" height="80" rx="10"/>
<text x="700" y="52" text-anchor="middle" class="b wm">4 下游有用度</text>
<text x="700" y="76" text-anchor="middle" class="s">規劃、RL、評估排序</text>
<path class="ar" d="M190,60 H208"/><path class="ar" d="M390,60 H408"/><path class="ar wm" d="M590,60 H608"/>
</svg>
<figcaption>越往右越重要、也越難量。第 4 層才是最終答案。</figcaption>
</figure>

| 層次 | 問的問題 | 常用指標或方法 |
|---|---|---|
| **1 視覺品質** | 生成的畫面像不像真的？ | [FVD](https://arxiv.org/abs/1812.01717)、FID、PSNR／SSIM／LPIPS、[VBench](https://arxiv.org/abs/2311.17982) |
| **2 物理與一致性** | 物體會不會憑空消失？碰撞、重力對不對？轉回頭場景還在不在？ | [Physics-IQ](https://arxiv.org/abs/2501.09038) 等物理基準、3D 幾何一致性、物體恆存測試、長時漂移 |
| **3 動作可控性** | 給不同動作，結果真的跟著變嗎？ | 同一起點餵入不同動作比較差異（Genie 用 ΔPSNR）、與真實動作後果的軌跡誤差 |
| **4 下游有用度** | 拿它做決策有沒有幫助？ | 用它規劃的真機成功率、用它訓練的 RL 分數（Atari 100k、DMC）、用它評估策略時與真機排名的相關係數 |

第 4 層最重要也最難。一個 FVD 很低的模型可能因為「太樂觀」而讓每個策略看起來都會成功，拿來評估就失去鑑別力，這就是世界模型資料要包含失敗案例的原因。

## 延伸閱讀（建議順序）

- <span class="tag vla">VLA</span> [RT-2](https://arxiv.org/abs/2307.15818) → [OpenVLA](https://arxiv.org/abs/2406.09246) → [π0](https://arxiv.org/abs/2410.24164) → [π0.5](https://arxiv.org/abs/2504.16054) → [Open X-Embodiment](https://arxiv.org/abs/2310.08864) → [OpenVLA-OFT](https://arxiv.org/abs/2502.19645) → [SimplerEnv](https://arxiv.org/abs/2405.05941)
- <span class="tag wm">WM</span> [World Models](https://arxiv.org/abs/1803.10122) → [DreamerV3](https://arxiv.org/abs/2301.04104) → [Genie](https://arxiv.org/abs/2402.15391) → [Cosmos](https://arxiv.org/abs/2501.03575) → [V-JEPA 2](https://arxiv.org/abs/2506.09985) → [DreamGen](https://arxiv.org/abs/2505.12705) → [Physics-IQ](https://arxiv.org/abs/2501.09038)

本頁數字（資料量、算力、控制頻率）取自各論文發表時的版本，後續版本可能有更新。
