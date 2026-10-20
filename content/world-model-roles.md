# 世界模型四類與五種角色

<p class="lede">第一部分回答「世界模型有哪幾類、各自吃什麼、吐什麼、拿來做什麼」；第二部分回答「VLA 實際上把世界模型接在哪裡」。內容整理自專案的〈世界模型種類〉簡報（連結見 <a href="references.html#project-outputs">參考資料</a>）。</p>

!!! key "一句話帶走"
    **對 VLA 來說，世界模型同時是資料來源、陪練、想像力，也是考官。** 資料引擎造資料，輔助預測教它懂動態，想像中 RL 讓它練習，先想再做給它規劃能力，評測模擬器替它把關。

## 世界模型的共同介面

**一句話定義：給定「現在」與「打算做的動作」，預測「接下來會發生什麼」。** 不同類型的差別只在「未來」用什麼形式表示：畫面、潛向量、表徵或 3D 場景。這是 Ha 與 Schmidhuber 2018 年 [World Models](https://arxiv.org/abs/1803.10122) 以來的通用說法；[NVIDIA Cosmos](https://arxiv.org/abs/2501.03575) 也用「目前狀態＋控制訊號 → 未來狀態」描述它。

<figure class="dg">
<svg viewBox="0 0 800 230" role="img" aria-label="世界模型的共同介面">
<rect class="n" x="10" y="20" width="190" height="70" rx="10"/>
<text x="105" y="50" text-anchor="middle" class="b">現在</text>
<text x="105" y="72" text-anchor="middle" class="s">畫面、潛狀態或場景</text>
<rect class="n" x="10" y="120" width="190" height="70" rx="10"/>
<text x="105" y="150" text-anchor="middle" class="b">動作／條件</text>
<text x="105" y="172" text-anchor="middle" class="s">關節、方向盤、文字、相機</text>
<rect class="n wm" x="280" y="55" width="220" height="100" rx="12"/>
<text x="390" y="98" text-anchor="middle" class="b wm">學到的動力學</text>
<text x="390" y="122" text-anchor="middle" class="s">DiT、RSSM、Transformer…</text>
<rect class="n wm" x="580" y="70" width="210" height="70" rx="10"/>
<text x="685" y="100" text-anchor="middle" class="b">預測的未來</text>
<text x="685" y="122" text-anchor="middle" class="s">下一幀、下一個潛狀態</text>
<path class="ar" d="M200,55 H240 V90 H278"/>
<path class="ar" d="M200,155 H240 V120 H278"/>
<path class="ar wm" d="M500,105 H578"/>
<path class="ar wm dash" d="M685,140 V210 H105 V92"/>
<text x="400" y="202" text-anchor="middle" class="s wm">把預測當成新的「現在」反覆滾動，就是「想像」</text>
</svg>
<figcaption>虛線表示把預測接回去當下一步輸入，連續滾動出一整段想像軌跡。Dreamer 的想像訓練、WMPO 的想像中強化學習都靠這個迴圈。</figcaption>
</figure>

## 第一部分：四種世界模型

| 類型 | 輸入 | 輸出 | 主要用途 | 代表作 |
|---|---|---|---|---|
| ① 影片生成 | 畫面＋文字＋動作／相機 | **未來影片** | 合成資料、評測、互動模擬 | Cosmos、Genie 3、Veo |
| ② 潛空間動力學 | 畫面＋動作 | **下一個潛狀態、獎勵** | 想像中強化學習、規劃 | DreamerV3／4、TD-MPC2 |
| ③ JEPA 表徵預測 | 畫面表徵＋動作 | **下一步表徵** | 零樣本規劃、表徵學習 | V-JEPA 2-AC |
| ④ 3D／4D 空間 | 多視角畫面、佔據、文字 | **3D 場景、未來佔據** | 自駕規劃、3D 模擬場景 | OccWorld、Marble |

輸入幾乎都是「觀測＋動作或條件」，**分類的依據是輸出**。

!!! key "最常被混淆的一點"
    **② 和 ③ 都在潛空間，差別只在「要不要重建畫面」。** Dreamer 會訓練解碼器把畫面畫回來；JEPA 刻意不畫，只在表徵空間比對。這正是 LeCun 主張的「生成式 vs 非生成式」。

### ① 影片生成式：看得見的未來，最適合當模擬器

- **架構**：[Cosmos](https://arxiv.org/abs/2501.03575) 有兩個家族：擴散模型在連續 latent 上去噪，自回歸模型像 GPT 一樣逐一預測離散影片 token。基礎模型吃文字或影像；要當機器人世界模型時，再用動作序列、相機姿態等做後訓練，條件以 cross-attention 注入。
- **規模**：Cosmos 從約 **2,000 萬小時**原始影片中篩出約 1 億段預訓練片段；擴散模型 7B／14B，自回歸模型 4B／12B。代價是生成慢、算力貴，物理也不一定正確。
- **用途**：
    1. **造合成訓練資料**：[DreamGen](https://arxiv.org/abs/2505.12705) 用微調後的影片模型產生新任務的機器人影片，再推回動作。
    2. **評測機器人策略**：Gemini Robotics 團隊用 Veo 改造的模擬器評測策略、做紅隊測試（[arXiv:2512.10675](https://arxiv.org/abs/2512.10675)）。
    3. **互動世界**：[Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/) 依文字生成可即時操控的世界，720p、每秒 24 幀，數分鐘內大致一致。
    4. **推理時先想再做**：[UniPi](https://arxiv.org/abs/2302.00111) 先生成「完成任務的影片」，再由逆動力學模型轉成動作。

### ② 潛空間動力學：在小小的潛狀態裡想像未來

- **架構**：Dreamer 系列的編碼器把畫面壓成潛狀態，RSSM 預測下一個潛狀態與獎勵；策略（Actor-Critic）完全在想像出來的潛空間軌跡上學。重建畫面只是學習訊號，決策時不需要解碼成畫面。
- **輸入輸出**：畫面＋動作 → 下一個潛狀態、獎勵、是否結束（以及用來訓練的重建畫面）。
- **成果**：[DreamerV3](https://arxiv.org/abs/2301.04104) 用同一組超參數在 **150+ 項任務**贏過各領域專門方法，也是第一個從零在 Minecraft 挖到鑽石的演算法。[Dreamer 4](https://arxiv.org/abs/2509.24527) 只用離線資料就挖到鑽石，且能在單一 GPU 即時執行。
- **缺點**：多半為特定任務而學；畫面細節少，人很難直接檢查它想像了什麼。

### ③ JEPA 表徵預測：不畫出未來，只預測未來的表徵

- **架構**：V-JEPA 2-AC 的編碼器凍結，預測器只學「在表徵空間裡，做了這個動作之後會變成什麼」。規劃時把目標畫面也編碼成表徵，用取樣最佳化（CEM）找出讓預測表徵最接近目標的動作序列，執行第一步後重新規劃（模型預測控制）。
- **訓練**（[V-JEPA 2](https://arxiv.org/abs/2506.09985)，官方圖見 [GitHub](https://github.com/facebookresearch/vjepa2)）：
    - **100 萬小時以上**網路影片與影像做自監督預訓練；
    - **不到 62 小時** DROID 機器人影片做動作條件後訓練；
    - **零樣本部署**：在兩個實驗室的 Franka 手臂上抓放物品，沒有在當地收資料或給獎勵。
- **取捨**：不生成像素，省下畫細節的算力；代價是無法產出可看的影片，難以直觀檢查。

### ④ 3D／4D 空間：輸出可以走進去的場景

- **自駕：[OccWorld](https://arxiv.org/abs/2311.16038)**（官方圖見 [GitHub](https://github.com/wzzheng/OccWorld)）：輸入過去的 3D 佔據（可由相機或 LiDAR 得到），輸出未來 3 秒的 3D 佔據＋自車軌跡。用場景 tokenizer 把佔據變成離散 token，再用類 GPT 的時空 Transformer 生成。在 nuScenes 上不需要物件框或地圖標註，也能給出有競爭力的規劃結果。
- **生成世界：[World Labs Marble](https://www.worldlabs.ai/blog/marble-world-model)**（2025 年 11 月正式開放）：輸入文字、圖片、短影片或粗略 3D 版面，輸出高斯潑濺、含碰撞用的三角網格，或指定相機路徑渲染的影片。官方列出的用途包括遊戲、VFX、設計與機器人模擬。優點是幾何一致、可自由換視角；缺點是動態與拓撲變化（撕開、倒水）難處理。

## 第二部分：VLA 怎麼用世界模型（五種角色）

<figure class="dg">
<svg viewBox="0 0 800 260" role="img" aria-label="VLA 生命週期五個階段中世界模型的角色">
<text x="10" y="20" class="h">VLA 生命週期</text>
<rect class="n vla" x="10" y="30" width="144" height="44" rx="8"/><text x="82" y="57" text-anchor="middle" class="b">收資料</text>
<rect class="n vla" x="170" y="30" width="144" height="44" rx="8"/><text x="242" y="57" text-anchor="middle" class="b">預訓練</text>
<rect class="n vla" x="330" y="30" width="144" height="44" rx="8"/><text x="402" y="57" text-anchor="middle" class="b">後訓練</text>
<rect class="n vla" x="490" y="30" width="144" height="44" rx="8"/><text x="562" y="57" text-anchor="middle" class="b">推理</text>
<rect class="n vla" x="650" y="30" width="140" height="44" rx="8"/><text x="720" y="57" text-anchor="middle" class="b">上線前</text>
<path class="ar vla" d="M154,52 H168"/><path class="ar vla" d="M314,52 H328"/><path class="ar vla" d="M474,52 H488"/><path class="ar vla" d="M634,52 H648"/>
<path class="ar wm" d="M82,74 V108"/><path class="ar wm" d="M242,74 V108"/><path class="ar wm" d="M402,74 V108"/><path class="ar wm" d="M562,74 V108"/><path class="ar wm" d="M720,74 V108"/>
<text x="10" y="102" class="h">世界模型的角色</text>
<rect class="n wm" x="10" y="110" width="144" height="80" rx="10"/><text x="82" y="142" text-anchor="middle" class="b">1 資料引擎</text><text x="82" y="166" text-anchor="middle" class="s">生成合成軌跡</text>
<rect class="n key" x="170" y="110" width="144" height="80" rx="10"/><text x="242" y="142" text-anchor="middle" class="b">2 輔助預測</text><text x="242" y="166" text-anchor="middle" class="s">邊預測未來邊學動作</text>
<rect class="n wm" x="330" y="110" width="144" height="80" rx="10"/><text x="402" y="142" text-anchor="middle" class="b">3 想像中 RL</text><text x="402" y="166" text-anchor="middle" class="s">在世界模型裡練習</text>
<rect class="n wm" x="490" y="110" width="144" height="80" rx="10"/><text x="562" y="142" text-anchor="middle" class="b">4 先想再做</text><text x="562" y="166" text-anchor="middle" class="s">子目標畫面、規劃</text>
<rect class="n wm" x="650" y="110" width="140" height="80" rx="10"/><text x="720" y="142" text-anchor="middle" class="b">5 評測模擬器</text><text x="720" y="166" text-anchor="middle" class="s">取代部分真機測試</text>
<text x="82" y="220" text-anchor="middle" class="s">DreamGen</text>
<text x="242" y="220" text-anchor="middle" class="s">GR-2、VPP、DreamVLA</text>
<text x="402" y="220" text-anchor="middle" class="s">WMPO、VLA-RFT</text>
<text x="562" y="220" text-anchor="middle" class="s">UniPi、CoT-VLA</text>
<text x="720" y="220" text-anchor="middle" class="s">Veo、GE-Sim</text>
</svg>
<figcaption>上排是 VLA 的生命週期，下排是世界模型在該階段的角色，最下面是代表作。橘色那格「輔助預測」是目前論文最多的一派。</figcaption>
</figure>

### 推理時預測接在哪裡：四種接法

[DreamVLA](https://arxiv.org/abs/2507.04447) 論文把「VLA 結合預測」整理成四種範式（官方比較圖見 [GitHub](https://github.com/Zhangwenyao1/DreamVLA)）：

- **(a) 純 VLA**：直接出動作。
- **(b) 先生成子目標畫面，再交給策略**：兩個模型串接，例如 UniPi。
- **(c) VLA 同時輸出子目標畫面與動作**：把世界模型併進同一個 VLA，例如 CoT-VLA。
- **(d) 只預測動態、深度、語意等精簡特徵**：只預測對動作有用的部分，避免浪費在畫面細節，例如 DreamVLA。

### 角色 1 · 資料引擎：DreamGen 用影片世界模型「做夢」造資料

<figure class="dg">
<svg viewBox="0 0 800 200" role="img" aria-label="DreamGen 四步驟">
<rect class="n" x="10" y="20" width="175" height="90" rx="10"/>
<text x="97" y="52" text-anchor="middle" class="b">1 微調影片模型</text>
<text x="97" y="76" text-anchor="middle" class="s">用目標機器人的</text><text x="97" y="94" text-anchor="middle" class="s">遙控資料</text>
<rect class="n wm" x="215" y="20" width="175" height="90" rx="10"/>
<text x="302" y="52" text-anchor="middle" class="b wm">2 生成新任務影片</text>
<text x="302" y="76" text-anchor="middle" class="s">影像＋文字提示</text><text x="302" y="94" text-anchor="middle" class="s">可換新環境</text>
<rect class="n" x="420" y="20" width="175" height="90" rx="10"/>
<text x="507" y="52" text-anchor="middle" class="b">3 推回偽動作</text>
<text x="507" y="76" text-anchor="middle" class="s">潛在動作模型或</text><text x="507" y="94" text-anchor="middle" class="s">逆動力學模型（IDM）</text>
<rect class="n vla" x="625" y="20" width="165" height="90" rx="10"/>
<text x="707" y="52" text-anchor="middle" class="b vla">4 訓練 VLA</text>
<text x="707" y="76" text-anchor="middle" class="s">真實資料</text><text x="707" y="94" text-anchor="middle" class="s">＋神經軌跡</text>
<path class="ar" d="M185,65 H213"/><path class="ar wm" d="M390,65 H418"/><path class="ar" d="M595,65 H623"/>
<text x="400" y="150" text-anchor="middle" class="s">產出的影片沒有動作標籤，所以第 3 步要把動作「猜」回來</text>
<text x="400" y="178" text-anchor="middle" class="b">成果：只用一個環境、一個抓放任務的遙控資料，人形機器人學會 22 種新行為</text>
</svg>
</figure>

NVIDIA GEAR 的 [DreamGen](https://arxiv.org/abs/2505.12705)（也就是 GR00T-Dreams）在看過與沒看過的環境都能執行新行為。團隊另提出 DreamGen Bench，其影片品質分數與下游策略成功率相關。這是資料引擎路線最有說服力的數字：真實資料極少，泛化主要來自世界模型生成的影片。

### 角色 2 · 輔助預測：邊預測未來，邊學動作

- **[GR-2](https://arxiv.org/abs/2410.06158)（ByteDance）**：先看 **3,800 萬段**網路影片學「世界怎麼變」，再用機器人軌跡同時學影片生成與動作預測，**100 多項任務平均成功率 97.7%**。對沒看過的背景、環境、物件、任務都能泛化，模型越大越好；代價是要生成影片，訓練與推理成本高。
- **[VPP](https://arxiv.org/abs/2412.14803)**（官方圖見 [GitHub](https://github.com/roboterax/video-prediction-policy)）：階段一把影片基礎模型微調在機器人與人手操作影片上；階段二取影片擴散模型的中間特徵，交給擴散策略出動作。CALVIN ABC-D 相對前一最佳 **+18.6%**，真實靈巧手任務成功率 **+31.6%**。關鍵觀察：影片擴散模型的中間特徵同時包含「現在」與「預測的未來運動」，比只看單張圖的編碼器更適合當策略表徵。
- **[Genie Envisioner](https://arxiv.org/abs/2508.05635)（智元 AgiBot）**（官方圖見 [GitHub](https://github.com/AgibotTech/Genie-Envisioner)）：「世界模型即平台」。GE-Base 是指令條件的影片擴散模型，用 AgiBot World 約 100 萬段真實操作資料訓練；GE-Act 是輕量 flow matching 解碼器，把潛在特徵轉成動作；GE-Sim 是動作條件的神經模擬器，可閉環評測 π0、OpenVLA 等策略；另附 EWMBench 評測影片世界模型。同一個 GE-Base 同時支撐角色 2 與角色 5。
- **[DreamVLA](https://arxiv.org/abs/2507.04447)**：只預測對動作有用的精簡特徵（動態區域、深度、語意），不生成整張畫面。CALVIN 平均完成長度從純 VLA 的 **3.64 升到 4.44**；真機 Franka 平均成功率 76.7%，LIBERO 四套平均 92.6%。消融顯示只加深度或只加語意不一定有幫助，需要和動態區域預測搭配。

| 模型 | 預測什麼 | 怎麼接到動作 | 代表數字 |
|---|---|---|---|
| [GR-2](https://arxiv.org/abs/2410.06158) | 未來影格 | 同一模型同時出影片與動作 | 100+ 任務平均 97.7% |
| [VPP](https://arxiv.org/abs/2412.14803) | 未來影格（取中間特徵） | 特徵交給擴散策略 | CALVIN 相對 +18.6% |
| [Genie Envisioner](https://arxiv.org/abs/2508.05635) | 多視角未來影片 | flow matching 解碼器 | 平台型，附 EWMBench |
| [DreamVLA](https://arxiv.org/abs/2507.04447) | 動態區域、深度、語意 | 擴散 Transformer 出動作 | CALVIN 3.64 → 4.44 |
| [WorldVLA](https://arxiv.org/abs/2506.21539) | 下一張影像 | 同一自回歸模型出動作 | 抓取成功率 +4% |
| [CoT-VLA](https://arxiv.org/abs/2503.22020) | 子目標影像 | 先出子目標再出動作 | 真機 +17%、模擬 +6% |

共同點是把「預測未來」當輔助任務，讓 VLA 學到動態；差別在預測的東西多完整，以及預測和動作是同一個模型還是串接。WorldVLA 另發現自回歸逐步出動作會累積誤差，用注意力遮罩遮掉先前動作來改善。

### 角色 3 · 想像中強化學習：WMPO 讓 VLA 在世界模型裡練習

<figure class="dg">
<svg viewBox="0 0 800 250" role="img" aria-label="WMPO 想像中強化學習迴圈">
<text x="440" y="22" text-anchor="middle" class="b wm">全程不碰真實環境</text>
<rect class="n vla" x="10" y="50" width="180" height="100" rx="12"/>
<text x="100" y="92" text-anchor="middle" class="b vla">VLA 策略</text>
<text x="100" y="116" text-anchor="middle" class="s">OpenVLA-OFT</text>
<rect class="n wm" x="310" y="50" width="220" height="100" rx="12"/>
<text x="420" y="92" text-anchor="middle" class="b wm">影片世界模型</text>
<text x="420" y="116" text-anchor="middle" class="s">像素空間，先對齊策略行為</text>
<rect class="n" x="620" y="50" width="170" height="100" rx="12"/>
<text x="705" y="92" text-anchor="middle" class="b">獎勵模型</text>
<text x="705" y="116" text-anchor="middle" class="s">判斷成功或失敗</text>
<rect class="n key" x="310" y="185" width="220" height="50" rx="10"/>
<text x="420" y="215" text-anchor="middle" class="b">GRPO 更新策略</text>
<path class="ar vla" d="M190,80 H308"/>
<text x="250" y="72" text-anchor="middle" class="s vla">動作片段</text>
<path class="ar wm" d="M308,125 H192"/>
<text x="250" y="142" text-anchor="middle" class="s wm">想像的下一幀</text>
<path class="ar" d="M530,100 H618"/>
<path class="ar" d="M705,150 V210 H532"/>
<path class="ar vla" d="M308,210 H100 V152"/>
</svg>
</figure>

[WMPO](https://arxiv.org/abs/2511.09515) 的迴圈：VLA 出動作片段，影片世界模型生成接下來的畫面再餵回 VLA，反覆滾動成完整的想像軌跡；獎勵模型判斷成敗，用 GRPO 更新策略。世界模型先用策略自己的軌跡微調，才能模擬它的失敗。刻意在像素空間預測，是為了讓想像畫面和 VLA 預訓練看到的影像一致。

- **成果**：Mimicgen 四項任務平均成功率：基礎策略 33.6%，直接 GRPO 37.1%，**WMPO 57.6%**（1,280 次想像試驗預算）。不需真機試錯就能從失敗中學，出現自我修正行為。WMPO 已被 ICLR 2026 接收。
- [VLA-RFT](https://arxiv.org/abs/2510.00406) 也用世界模型當模擬器，不到 400 步微調就超越監督式基線。
- **風險**：世界模型的錯誤會被策略鑽漏洞；長時間滾動會累積誤差，需要額外技巧穩定。

### 角色 4 · 先想再做：UniPi 把決策變成「生成影片」

<figure class="dg">
<svg viewBox="0 0 800 210" role="img" aria-label="UniPi 先想再做流程">
<rect class="n" x="10" y="20" width="140" height="50" rx="8"/><text x="80" y="50" text-anchor="middle" class="b">目前畫面</text>
<rect class="n" x="10" y="100" width="140" height="50" rx="8"/><text x="80" y="130" text-anchor="middle" class="b">文字目標</text>
<rect class="n wm" x="200" y="35" width="210" height="100" rx="12"/>
<text x="305" y="78" text-anchor="middle" class="b wm">文字條件影片生成</text>
<text x="305" y="102" text-anchor="middle" class="s">畫出「完成任務的樣子」</text>
<rect class="n wm" x="460" y="50" width="130" height="70" rx="10"/><text x="525" y="90" text-anchor="middle" class="b">影片計畫</text>
<rect class="n vla" x="640" y="40" width="150" height="90" rx="10"/>
<text x="715" y="78" text-anchor="middle" class="b vla">逆動力學模型</text>
<text x="715" y="102" text-anchor="middle" class="s">相鄰畫面 → 動作</text>
<path class="ar" d="M150,45 H175 V70 H198"/><path class="ar" d="M150,125 H175 V100 H198"/>
<path class="ar wm" d="M410,85 H458"/><path class="ar" d="M590,85 H638"/>
<path class="ar vla dash" d="M715,130 V185 H80 V152"/>
<text x="400" y="178" text-anchor="middle" class="s vla">執行動作、拍下新畫面，閉環重複</text>
</svg>
</figure>

[UniPi](https://arxiv.org/abs/2302.00111) 用文字條件的影片擴散模型當規劃器：輸入目前畫面與文字目標，先生成粗略的關鍵幀再補成完整影片，最後用小型逆動力學模型把相鄰畫面轉成動作。[CoT-VLA](https://arxiv.org/abs/2503.22020) 把這件事併進一個 7B 的 VLA：先預測子目標影像，再出動作；[V-JEPA 2-AC](https://arxiv.org/abs/2506.09985) 則是在表徵空間做同樣的「先想」。代價是推理延遲，見 [06 訓練時 vs 推論時](train-vs-inference.html)。

### 角色 5 · 評測模擬器：用世界模型代替真機測試

Gemini Robotics 團隊用 **Veo** 世界模擬器評測 8 個策略版本、5 項雙臂任務，再以 **1,600 多次真機評測**對照（[arXiv:2512.10675](https://arxiv.org/abs/2512.10675)）。模擬器能正確預測策略之間的**相對排名**；還能用影像編輯換物件、背景、干擾物，量測各種泛化，並做安全紅隊測試。

評測是世界模型最快落地的用途之一：不需要模擬器的物理精準，只需要排名一致。智元的 GE-Sim 也是同一路線。

## 總結：五種角色各配哪種世界模型

| 角色 | 常用類型 | 代表作 | 好處 | 風險 |
|---|---|---|---|---|
| 1 資料引擎 | ① 影片生成 | DreamGen | 少量真實資料就能泛化 | 偽動作不準 |
| 2 輔助預測 | ① 影片、精簡特徵 | GR-2、VPP、DreamVLA | 學到動態，泛化更好 | 訓練成本高 |
| 3 想像中 RL | ① 影片（像素） | WMPO、VLA-RFT | 不用真機試錯 | 策略鑽模型漏洞 |
| 4 先想再做 | ① 影片、③ JEPA | UniPi、CoT-VLA、V-JEPA 2-AC | 可解釋、可規劃 | 推理延遲 |
| 5 評測模擬器 | ① 影片 | Veo、GE-Sim | 省真機測試、可紅隊 | 只保證相對排名 |

!!! note "觀察"
    目前 VLA 端幾乎都用影片類（①）世界模型，因為它的輸出和 VLA 吃的影像是同一種東西；潛空間（②）仍以 Dreamer 式的單任務強化學習為主；JEPA（③）開始在規劃上出現；3D（④）主要在自駕與場景模擬。

## 參考資料

[Cosmos](https://arxiv.org/abs/2501.03575)、[Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)、[DreamerV3](https://arxiv.org/abs/2301.04104)、[Dreamer 4](https://arxiv.org/abs/2509.24527)、[V-JEPA 2](https://arxiv.org/abs/2506.09985)、[OccWorld](https://arxiv.org/abs/2311.16038)、[World Labs Marble](https://www.worldlabs.ai/blog/marble-world-model)、[具身世界模型綜述 arXiv:2510.16732](https://arxiv.org/abs/2510.16732)、[World Models](https://arxiv.org/abs/1803.10122)、[DreamGen](https://arxiv.org/abs/2505.12705)、[GR-2](https://arxiv.org/abs/2410.06158)、[VPP](https://arxiv.org/abs/2412.14803)、[Genie Envisioner](https://arxiv.org/abs/2508.05635)、[DreamVLA](https://arxiv.org/abs/2507.04447)、[WorldVLA](https://arxiv.org/abs/2506.21539)、[CoT-VLA](https://arxiv.org/abs/2503.22020)、[WMPO](https://arxiv.org/abs/2511.09515)、[VLA-RFT](https://arxiv.org/abs/2510.00406)、[UniPi](https://arxiv.org/abs/2302.00111)、[Veo 世界模擬器評測](https://arxiv.org/abs/2512.10675)。
