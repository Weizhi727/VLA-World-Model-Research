# 三類世界模型怎麼訓練 VLA：用一個車禍畫面走一遍

<p class="lede">本站把世界模型分成 ①影片生成、②潛空間動力學、③JEPA、④3D 四類。這一頁只回答一件事（先用「行人闖紅燈」的入門版講一遍，再進入細節）：真實的 VLA（以及自駕的端到端駕駛模型）在訓練時，是怎麼用前三類世界模型的？每一類給一張流程圖、一個實際用過的例子，再拿同一個「車禍前 2 秒」的畫面逐步走一遍：指令是什麼、進哪個模組、輸出什麼、VLA 最後學到什麼。數字都回到論文或官方頁核對過，查不到的標「未寫」或「未公開」。</p>

## 入門：用「行人闖紅燈」講一遍

想讓車子學會一件事：**有人闖紅燈衝出來，車子要自動減速或閃開**。先看 VLA 本身吃什麼、吐什麼，再看三類世界模型各自怎麼幫它。

### 先看 VLA：輸入與輸出

<figure class="dg">
<svg viewBox="0 0 800 330" role="img" aria-label="駕駛 VLA 的輸入輸出，以及三類世界模型怎麼幫它">
<rect class="n key" x="10" y="20" width="200" height="110" rx="10"/>
<text x="110" y="46" text-anchor="middle" class="b">VLA 的輸入</text>
<text x="25" y="72" class="s">① 最近約 2 秒的鏡頭畫面</text>
<text x="25" y="94" class="s">② 自車狀態：車速、加速度</text>
<text x="25" y="116" class="s">③ 導航指令：「直行」</text>
<rect class="n vla" x="300" y="20" width="200" height="110" rx="10"/>
<text x="400" y="66" text-anchor="middle" class="b vla">VLA（駕駛模型）</text>
<text x="400" y="90" text-anchor="middle" class="s">車上真正在跑的只有它</text>
<rect class="n" x="590" y="20" width="200" height="110" rx="10"/>
<text x="690" y="46" text-anchor="middle" class="b">VLA 的輸出</text>
<text x="605" y="72" class="s">未來幾秒要走的軌跡</text>
<text x="605" y="94" class="s">或直接的控制量：</text>
<text x="605" y="116" class="s">方向盤、油門、煞車</text>
<path class="ar vla" d="M210,75 H298"/>
<path class="ar vla" d="M500,75 H588"/>
<rect class="n wm" x="10" y="190" width="240" height="110" rx="10"/>
<text x="130" y="220" text-anchor="middle" class="b wm">① 影片生成</text>
<text x="130" y="246" text-anchor="middle" class="s">生成「有人闖紅燈」的影片</text>
<text x="130" y="270" text-anchor="middle" class="b">給 VLA：新教材</text>
<rect class="n wm" x="280" y="190" width="240" height="110" rx="10"/>
<text x="400" y="220" text-anchor="middle" class="b wm">② 潛空間動力學</text>
<text x="400" y="246" text-anchor="middle" class="s">預測「這樣開會不會撞到」</text>
<text x="400" y="270" text-anchor="middle" class="b">給 VLA：試錯的機會</text>
<rect class="n wm" x="550" y="190" width="240" height="110" rx="10"/>
<text x="670" y="220" text-anchor="middle" class="b wm">③ JEPA</text>
<text x="670" y="246" text-anchor="middle" class="s">猜「接下來幾秒會怎樣」</text>
<text x="670" y="270" text-anchor="middle" class="b">給 VLA：好眼力</text>
<path class="ar wm dash" d="M130,190 V160 H360 V132"/>
<path class="ar wm dash" d="M400,190 V132"/>
<path class="ar wm dash" d="M670,190 V160 H440 V132"/>
<text x="400" y="322" text-anchor="middle" class="s">虛線：訓練時三類世界模型從旁幫忙；部署到車上後，世界模型都拿掉</text>
</svg>
<figcaption>VLA 的輸入輸出以真實系統為例：comma.ai 的駕駛策略看最近約 2 秒的畫面，輸出方向盤曲率與加速度（<a href="https://arxiv.org/abs/2504.19077">arXiv:2504.19077</a>）；NAVSIM 基準給的導航指令是「左轉／直行／右轉」三選一，模型輸出未來幾秒的軌跡（<a href="https://arxiv.org/abs/2406.15349">arXiv:2406.15349</a>）。</figcaption>
</figure>

| | 具體內容（闖紅燈的例子） |
|---|---|
| **VLA 輸入** | ① 最近約 2 秒的前視鏡頭畫面（例如每秒 5 張，共 10 張）：畫面裡是一個路口，右邊人行道有個行人正要踏出來，行人號誌是紅燈；② 自車狀態：時速 40 公里；③ 導航指令：「直行」 |
| **VLA 輸出** | 未來幾秒的動作：例如「從時速 40 公里減速到 0，方向盤保持不動」，或寫成接下來幾秒的一串軌跡點 |
| **要學會的事** | 輸入畫面裡**出現有人要闖紅燈的跡象**時，輸出就要變成**減速或閃避**，而不是照導航指令繼續直行 |

難處在於：真實行車資料裡，這種畫面非常少，也不可能找人真的去衝撞車子來收集資料。三類世界模型就是從不同角度補這個缺口。

### ① 影片生成：幫 VLA「拍」出新教材

| | 具體內容 |
|---|---|
| **世界模型輸入** | 一張真實的路口照片＋條件：文字「行人從右側闖紅燈走出」、行人的位置與走路方向、自車要做的動作「從時速 40 公里煞停」 |
| **世界模型輸出** | 一段幾秒的影片：行人走出來，畫面中的車子慢慢停在行人前面 |
| **交給 VLA 的東西** | 把影片切成一筆一筆的訓練資料。每一筆是：**輸入**＝影片中的某一張畫面（行人剛踏出）＋車速＋「直行」；**正確答案**＝當時應該做的動作（開始煞車）。因為煞車動作是生成時指定的，答案本來就知道 |
| **VLA 學到什麼** | 換天氣、換路口、換行人走的速度，就能生成上千筆。VLA 看多了就學會：**畫面裡有人往馬路走，就要煞車** |

### ② 潛空間動力學：讓 VLA 在腦中試錯

| | 具體內容 |
|---|---|
| **世界模型輸入** | 不是照片，而是**簡化過的路口狀態**（行人在哪、往哪走、多快、燈號是什麼、自車在哪、多快）＋ VLA 這一步想做的動作，例如「繼續直行」 |
| **世界模型輸出** | 下一瞬間的狀態（行人和車子各移動到哪）、這一步的**分數**、以及**有沒有撞到** |
| **交給 VLA 的東西** | 一來一往的練習：VLA 看狀態 → 選動作 → 世界模型告訴它結果與分數 → VLA 再選下一個動作……。這時 VLA 的**輸入**是世界模型給的狀態，**輸出**是一個動作（繼續、減速、煞停、往左閃） |
| **VLA 學到什麼** | 在腦中試幾萬次：「繼續直行 → 撞到 → 扣很多分」「提早減速 → 安全通過 → 加分」。VLA 從**後果**學會選煞車，不用真的撞一次人 |

### ③ JEPA：先幫 VLA 練好眼力

| | 具體內容 |
|---|---|
| **世界模型輸入** | 大量真實行車影片（不需要任何標註），把每段的**後面幾秒遮起來** |
| **世界模型輸出** | 對被遮住那幾秒的「猜測」：不是畫出畫面，而是一組代表「接下來會發生什麼」的特徵，例如「人會走到車道中間」 |
| **交給 VLA 的東西** | 練好的**看圖模組**（視覺編碼器）直接裝進 VLA 當它的眼睛。之後再用一般的示範資料訓練 VLA：**輸入**＝鏡頭畫面＋車速＋「直行」，**輸出**＝軌跡或煞車 |
| **VLA 學到什麼** | 為了猜準「接下來會怎樣」，模型必須注意「路邊那個人正往馬路走」。所以 VLA 的眼睛一開始就**對行人的動向很敏感**，只要少量示範就能學會「看到這種情況要煞車」 |

!!! key "一句話記住"
    **① 給新教材、② 給試錯機會、③ 給好眼力。** 三種都只在訓練時用；車上真正在跑的，只有吃「畫面＋車速＋導航指令」、吐「軌跡或方向盤油門煞車」的 VLA。下面的內容是同一套觀念的進階版：用真實論文的規格，把每一步拆得更細。

!!! key "重點先講"
    1. **三類的差別在「世界模型預測什麼」**：①預測**未來的畫面**（看得到的影片）；②預測**精簡的潛狀態＋獎勵＋會不會出事**；③預測**未來的「表徵」**（一組向量，不畫出畫面）。
    2. **所以給 VLA 的東西也不同**：
        - ① 給 **新資料** 和 **練習場**：生成罕見危險場景的影片當訓練資料，或讓 VLA 在生成的世界裡自己開、自己犯錯。
        - ② 給 **想像中的試錯**：便宜、快，一張 GPU 三天就能讓策略在「腦中」撞幾萬次車、學會避開。
        - ③ 給 **更會預判的眼睛**：當預訓練或輔助損失，逼 VLA 的視覺特徵先學會「下一秒會怎樣」。
    3. **實際例子**：① [DreamGen](https://arxiv.org/abs/2505.12705) → GR00T N1／N1.5（機器人）、[comma.ai](https://arxiv.org/abs/2504.19077) → openpilot（自駕，已上線）、[GAIA-2](https://arxiv.org/abs/2503.20523) 造危險場景；② [Think2Drive](https://arxiv.org/abs/2402.16720)（CARLA，「Accident」事故車場景成功率 0.81）；③ [VLA-JEPA](https://arxiv.org/abs/2602.10098)（機器人）、[Drive-JEPA](https://arxiv.org/abs/2601.22032)（自駕，小鵬合著）。
    4. **車禍畫面的「指令」通常不是「避開車禍」**。自駕模型拿到的是導航指令，例如 [NAVSIM](https://arxiv.org/abs/2406.15349) 只給「左轉／直行／右轉」三選一；危險要靠模型自己從畫面看出來。世界模型那一側的「條件」才是重點：可以是文字（GAIA-2 的 CLIP 文字條件）、自車動作（速度、曲率、油門煞車），或乾脆不給（JEPA 自監督）。
    5. **三類幾乎都只在訓練時出現**。訓練完部署到車上或機器人上的只有 VLA／駕駛策略本身（對應 [08 訓練時 vs 推論時](train-vs-inference.html) 的 I0）。

## 一張圖：同一個車禍畫面，送進三種世界模型

<figure class="dg">
<svg viewBox="0 0 800 380" role="img" aria-label="同一個車禍畫面送進三種世界模型，各自輸出什麼、VLA 學到什麼">
<text x="285" y="16" text-anchor="middle" class="h">世界模型</text>
<text x="495" y="16" text-anchor="middle" class="h">輸出</text>
<text x="705" y="16" text-anchor="middle" class="h">VLA 從中學到</text>
<rect class="n key" x="10" y="140" width="150" height="100" rx="10"/>
<text x="85" y="172" text-anchor="middle" class="b">車禍前 2 秒</text>
<text x="85" y="194" text-anchor="middle" class="s">前視鏡頭畫面</text>
<text x="85" y="214" text-anchor="middle" class="s">＋導航指令「直行」</text>
<rect class="n wm" x="200" y="30" width="170" height="96" rx="10"/>
<text x="285" y="58" text-anchor="middle" class="b wm">① 影片生成</text>
<text x="285" y="80" text-anchor="middle" class="s">GAIA-2、comma.ai</text>
<text x="285" y="100" text-anchor="middle" class="s">＋自車動作、文字條件</text>
<rect class="n" x="410" y="30" width="170" height="96" rx="10"/>
<text x="495" y="64" text-anchor="middle" class="b">未來幾秒的影片</text>
<text x="495" y="88" text-anchor="middle" class="s">「撞上」和「及時煞停」</text>
<text x="495" y="106" text-anchor="middle" class="s">可以各生成一版</text>
<rect class="n vla" x="620" y="30" width="170" height="96" rx="10"/>
<text x="705" y="64" text-anchor="middle" class="b vla">新資料＋練習場</text>
<text x="705" y="88" text-anchor="middle" class="s">罕見危險場景該怎麼開</text>
<text x="705" y="106" text-anchor="middle" class="s">開偏了怎麼救回來</text>
<rect class="n wm" x="200" y="142" width="170" height="96" rx="10"/>
<text x="285" y="170" text-anchor="middle" class="b wm">② 潛空間動力學</text>
<text x="285" y="192" text-anchor="middle" class="s">Think2Drive（RSSM）</text>
<text x="285" y="212" text-anchor="middle" class="s">＋策略想試的動作</text>
<rect class="n" x="410" y="142" width="170" height="96" rx="10"/>
<text x="495" y="176" text-anchor="middle" class="b">下一個潛狀態</text>
<text x="495" y="200" text-anchor="middle" class="s">＋獎勵</text>
<text x="495" y="218" text-anchor="middle" class="s">＋這一步撞了沒</text>
<rect class="n vla" x="620" y="142" width="170" height="96" rx="10"/>
<text x="705" y="176" text-anchor="middle" class="b vla">想像中試錯</text>
<text x="705" y="200" text-anchor="middle" class="s">「直開會撞」→</text>
<text x="705" y="218" text-anchor="middle" class="s">提早變道或煞車</text>
<rect class="n wm" x="200" y="254" width="170" height="96" rx="10"/>
<text x="285" y="282" text-anchor="middle" class="b wm">③ JEPA</text>
<text x="285" y="304" text-anchor="middle" class="s">Drive-JEPA、VLA-JEPA</text>
<text x="285" y="324" text-anchor="middle" class="s">把未來遮住，不給動作</text>
<rect class="n" x="410" y="254" width="170" height="96" rx="10"/>
<text x="495" y="288" text-anchor="middle" class="b">未來的表徵向量</text>
<text x="495" y="312" text-anchor="middle" class="s">不畫出畫面</text>
<text x="495" y="330" text-anchor="middle" class="s">只和真實未來比對</text>
<rect class="n vla" x="620" y="254" width="170" height="96" rx="10"/>
<text x="705" y="288" text-anchor="middle" class="b vla">會預判的視覺特徵</text>
<text x="705" y="312" text-anchor="middle" class="s">前車在減速、距離在縮</text>
<text x="705" y="330" text-anchor="middle" class="s">再接規劃頭學開車</text>
<path class="ar" d="M160,190 H180 V78 H198"/>
<path class="ar" d="M160,190 H198"/>
<path class="ar" d="M160,190 H180 V302 H198"/>
<path class="ar wm" d="M370,78 H408"/>
<path class="ar wm" d="M370,190 H408"/>
<path class="ar wm" d="M370,302 H408"/>
<path class="ar vla" d="M580,78 H618"/>
<path class="ar vla" d="M580,190 H618"/>
<path class="ar vla" d="M580,302 H618"/>
<text x="400" y="372" text-anchor="middle" class="s">三條路都只在訓練時跑；部署到車上的只有右邊學好的 VLA／駕駛策略</text>
</svg>
<figcaption>左邊是同一筆輸入。①要「條件」才能生成指定的未來；②要「策略想試的動作」才能往下推演；③不需要動作，只把未來遮住讓模型猜表徵。</figcaption>
</figure>

!!! note "先對齊：車禍畫面的「指令」到底是什麼"
    - **給 VLA（駕駛模型）的指令**：導航層級的指令，不是「避開事故」。NAVSIM 把導航目標寫成三選一的 one-hot：左轉、直行、右轉（[arXiv:2406.15349](https://arxiv.org/abs/2406.15349)）；CARLA 則給要跟的路線。帶自然語言的駕駛 VLA（例如 [DriveVLM](https://arxiv.org/abs/2402.12289)、[Alpamayo-R1](https://arxiv.org/abs/2511.00088)）也是把導航意圖寫成文字，危險必須從畫面看出來。
    - **給世界模型的條件**：這才是「指定要生成什麼未來」的地方。①可以給文字（「雨天、前車急煞」）、他車的 3D 框、自車要怎麼開；②給策略想試的動作；③什麼都不給，是自監督。
    - 下面三段的車禍例子是**把論文公開的介面代入同一個場景**：輸入格式、模組、輸出規格都來自論文，「車禍前 2 秒」這個場景是我們假設的示範。

## ① 影片生成世界模型：給 VLA「新資料」和「練習場」

影片世界模型把畫面壓進 VAE／tokenizer 的潛空間，用擴散或 flow matching 生成未來幾秒，最後解碼回看得到的影片。它對 VLA 的用法有兩種：

- **資料工廠（T2）**：生成 VLA 沒見過的場景或動作的影片，補上動作標籤，當成新訓練資料。
- **練習場（T3）**：讓 VLA 在生成的世界裡自己出動作、看後果，用強化學習或 on-policy 學習更新。

### 流程圖：DreamGen 怎麼幫 GR00T N1 造資料

<figure class="dg">
<svg viewBox="0 0 800 250" role="img" aria-label="DreamGen：影片世界模型當資料工廠訓練 VLA">
<rect class="n" x="10" y="20" width="145" height="70" rx="10"/>
<text x="82" y="50" text-anchor="middle" class="b">少量真機示範</text>
<text x="82" y="72" text-anchor="middle" class="s">GR1：2,884 條抓放</text>
<rect class="n key" x="10" y="120" width="145" height="70" rx="10"/>
<text x="82" y="150" text-anchor="middle" class="b">初始畫面</text>
<text x="82" y="172" text-anchor="middle" class="s">＋新指令「Pour water」</text>
<rect class="n wm" x="190" y="20" width="150" height="170" rx="10"/>
<text x="265" y="80" text-anchor="middle" class="b wm">影片世界模型</text>
<text x="265" y="104" text-anchor="middle" class="s">WAN2.1</text>
<text x="265" y="124" text-anchor="middle" class="s">LoRA 微調（rank 4）</text>
<text x="265" y="144" text-anchor="middle" class="s">先學這台機器人</text>
<text x="265" y="162" text-anchor="middle" class="s">長什麼樣、怎麼動</text>
<rect class="n" x="375" y="120" width="120" height="70" rx="10"/>
<text x="435" y="150" text-anchor="middle" class="b">想像影片</text>
<text x="435" y="172" text-anchor="middle" class="s">沒有動作標籤</text>
<rect class="n mix" x="525" y="120" width="120" height="70" rx="10"/>
<text x="585" y="150" text-anchor="middle" class="b mix">IDM 補動作</text>
<text x="585" y="172" text-anchor="middle" class="s">兩幀 → 中間動作</text>
<rect class="n vla" x="675" y="120" width="115" height="70" rx="10"/>
<text x="732" y="150" text-anchor="middle" class="b vla">VLA 混訓</text>
<text x="732" y="172" text-anchor="middle" class="s">GR00T N1、π0</text>
<path class="ar" d="M155,55 H188"/>
<path class="ar" d="M155,155 H188"/>
<path class="ar wm" d="M340,155 H373"/>
<path class="ar" d="M495,155 H523"/>
<path class="ar vla" d="M645,155 H673"/>
<text x="400" y="222" text-anchor="middle" class="s">想像影片＋偽動作＝「神經軌跡」，和真機資料 1:1 混在一起訓練 VLA；世界模型本身不上機器人</text>
</svg>
<figcaption>依 <a href="https://arxiv.org/abs/2505.12705">DreamGen（arXiv:2505.12705）</a> 與<a href="https://research.nvidia.com/labs/gear/dreamgen">官方頁</a>的四步驟：微調影片模型 → 用初始畫面＋語言指令生成影片 → IDM 或潛在動作模型補動作 → 用神經軌跡訓練策略。「Pour water」是官方頁列出的新行為之一。</figcaption>
</figure>

**實例卡：[DreamGen](https://arxiv.org/abs/2505.12705)（NVIDIA，2025）**

| 項目 | 內容 |
|---|---|
| 世界模型 | **WAN2.1**，LoRA（rank 4）微調；論文沒寫用 1.3B 還是 14B 版 |
| 世界模型的輸入 | 一張初始畫面＋一句語言指令，例如官方頁的「Pour water」「Iron shirt」「Water flowers」「Fold Towel」 |
| 世界模型的輸出 | 機器人執行該指令的影片，**沒有動作** |
| 動作從哪來 | 逆動力學模型（IDM）：看前後兩幀，推回中間的動作 chunk；或用 LAPA 潛在動作 |
| 訓練哪些 VLA | Diffusion Policy、π0、GR00T N1；神經軌跡沒有本體感覺，訓練時狀態設 0 |
| 數據量 | GR1 人形只用 **2,884 條**抓放示範；RoboCasa 生成 **24 萬條**神經軌跡（1,500 張 L40 跑 54 小時） |
| VLA 學到什麼 | **示範裡沒有的新動作與新環境**：只用一個抓放任務的遙操作資料，人形機器人學會 **22 種新行為**；進入 GR00T N1.5 預訓練後，12 個新動詞成功率 13.1% → 38.3%（[GR00T N1.5 官方頁](https://research.nvidia.com/labs/gear/gr00t-n1_5/)） |

**實例卡：[comma.ai 世界模型](https://arxiv.org/abs/2504.19077) → openpilot（自駕，練習場用法，已上線）**

| 項目 | 內容 |
|---|---|
| 世界模型 | Stable Diffusion 的影像 VAE（8×8 壓縮、4 通道潛在）＋ **3D DiT**（250M／**500M 主力**／1B），每個時間步用 15 步 Euler 取樣 |
| 輸入 | 過去約 **2 秒**、5 Hz、128×256 的前視畫面＋自車位姿；還有「未來錨定」：給 1 秒後的目標位姿，讓預測的軌跡會往正確狀態收斂 |
| 輸出 | 下一幀（潛在）＋ Plan Head 預測的 10 秒軌跡 |
| 駕駛策略 | 只看相機；FastViT 特徵＋小型 Transformer，輸出想要的**曲率與加速度** |
| 怎麼學 | 策略在世界模型裡 **on-policy** 開車：策略出動作 → 世界模型生成下一幀 → 再出動作……；IMPALA 式平行 actor |
| 數據量 | 10 萬／20 萬／40 萬段、每段 1 分鐘的行車資料 |
| VLA 學到什麼 | **開偏了怎麼救回來**（離線模仿學不到）：MetaDrive 車道維持測試 24/24 通過，純離線訓練只有 5/24；變換車道 19/20 vs 8/20 |
| 上線情況 | 約 500 位使用者、兩個月、40,026 趟行程，世界模型版策略的啟用里程比例 52.49%，比舊方法 48.10% 高 |

### 車禍畫面走一遍（①）

假設手上有一段真實行車記錄：**雨天市區，前車突然急煞，自車來不及停而追撞**。下面用 GAIA-2 的條件介面、comma.ai 的訓練迴圈來走。

| 步驟 | 具體內容 | 根據 |
|---|---|---|
| **0. 原始輸入** | 追撞前 **2 秒**的前視畫面。comma.ai 的規格是 5 Hz、128×256，所以是 10 幀；GAIA-2 可吃最多 5 個鏡頭、448×960 | [comma.ai](https://arxiv.org/abs/2504.19077)、[GAIA-2](https://arxiv.org/abs/2503.20523) |
| **1. 指令／條件** | 給駕駛模型的指令：導航「直行」。給世界模型的條件：①文字「雨天、傍晚、市區、前車急煞」（CLIP 文字嵌入）；②前車的 3D 框（位置、方向、尺寸、類別），讓它在 1 秒內停住；③**自車動作**：速度與曲率。自車動作做兩版：**A 版**照原紀錄不煞車，**B 版**提早 0.8 秒減速 | GAIA-2 的條件包含自車速度與曲率、他車 3D 框、天氣與時段等中繼資料、CLIP 文字 |
| **2. 進哪個模組** | 影像先進 **VAE／tokenizer** 壓成潛在（GAIA-2 時間 8 倍、空間 32 倍壓縮，約 400 倍；comma.ai 用 SD VAE）→ **時空 Transformer 骨幹**（GAIA-2 8.4B、flow matching；comma.ai 500M DiT）一邊看條件一邊生成未來的潛在 → **解碼器**還原成影片 | GAIA-2、comma.ai |
| **3. 輸出** | 兩段未來數秒的影片：**A 版**看到車頭越來越近、撞上；**B 版**看到距離縮小但停住。comma.ai 的模型還會輸出一條 10 秒的軌跡 | 同上 |
| **4. 怎麼變成 VLA 的訓練訊號** | **資料工廠**：B 版影片配上已知的自車動作（減速曲線），就是一筆「看到這種畫面 → 該這樣開」的新訓練樣本，可以大量改天氣、車型、距離。**練習場**：不預先指定動作，改成讓駕駛策略自己出曲率與加速度，世界模型生成下一幀再交回策略；開壞了，下一幀就是更糟的畫面。**考官**：同一場景生成上百種變化，數策略撞了幾次 | DreamGen（資料）、comma.ai（on-policy）、GAIA-2 官方定位：用可控、可重複的合成場景補真實資料並壓力測試（[Wayve 新聞稿報導](https://www.autonomousvehicleinternational.com/news/ai-sensor-fusion/wayve-launches-gaia-2-video-generative-world-model-for-synthetic-data-generation.html)） |
| **5. VLA 學到什麼** | ①**罕見危險場景的對應**：真實資料裡追撞極少，世界模型能把一個事故片段擴寫成很多變體；②**從自己的錯誤中恢復**：on-policy 時會遇到「自己造成的」偏離狀態，學會拉回來；③**因果感**：前車煞燈亮、距離縮短 → 自己要減速 | Wayve 引用美國資料：平均約每 53.5 萬英里才一次事故，所以靠實車收集不到 |

!!! warn "影片世界模型的代價"
    生成的影片**物理不一定對**（車可能穿模、煞車距離不合理），VLA 可能學到假的規律。comma.ai 為此加了約 700 bits 的資訊瓶頸，避免策略去鑽模擬器瑕疵的漏洞；更多把關方法見 [10 具身基礎模型與合成資料](synthetic-data.html)。生成也很貴：GAIA-2 訓練用了 256 張 H100。

## ② 潛空間動力學世界模型：讓 VLA「在腦中試錯」

這一類（Dreamer、RSSM、TD-MPC2）不追求畫得像，只學一個**精簡的潛狀態**怎麼隨動作變化，外加預測**獎勵**和**這一回合是否結束**（例如撞車）。因為全在小向量上算，想像一步非常便宜，適合大量做強化學習。

### 流程圖：Think2Drive 怎麼在潛空間學開車

<figure class="dg">
<svg viewBox="0 0 800 270" role="img" aria-label="Think2Drive：在潛空間世界模型裡想像並訓練駕駛策略">
<text x="400" y="16" text-anchor="middle" class="s">部署到模擬器收更多真實互動（佔少數）</text>
<path class="ar dash" d="M722,40 V24 H82 V48"/>
<rect class="n" x="10" y="50" width="145" height="70" rx="10"/>
<text x="82" y="80" text-anchor="middle" class="b">CARLA 模擬器</text>
<text x="82" y="102" text-anchor="middle" class="s">39 種情境</text>
<rect class="n" x="10" y="170" width="145" height="70" rx="10"/>
<text x="82" y="200" text-anchor="middle" class="b">重放緩衝區</text>
<text x="82" y="222" text-anchor="middle" class="s">撞車片段優先重放</text>
<rect class="n wm" x="190" y="40" width="255" height="210" rx="10"/>
<text x="317" y="66" text-anchor="middle" class="b wm">潛空間世界模型（RSSM）</text>
<text x="205" y="94" class="s">編碼器：BEV → 潛狀態 z</text>
<text x="205" y="118" class="s">序列模型（GRU）：記憶 h</text>
<text x="205" y="142" class="s">動力學：(h, z, 動作) → 下一個 z</text>
<text x="205" y="166" class="s">獎勵頭 → r</text>
<text x="205" y="190" class="s">結束頭 → 這一步撞了沒</text>
<text x="205" y="214" class="s">解碼器：重建 BEV（只幫忙學表徵）</text>
<rect class="n key" x="480" y="40" width="140" height="210" rx="10"/>
<text x="550" y="120" text-anchor="middle" class="b key">想像 15 步</text>
<text x="550" y="146" text-anchor="middle" class="s">不碰模擬器</text>
<text x="550" y="168" text-anchor="middle" class="s">全在潛空間跑</text>
<rect class="n vla" x="655" y="40" width="135" height="210" rx="10"/>
<text x="722" y="120" text-anchor="middle" class="b vla">駕駛策略</text>
<text x="722" y="146" text-anchor="middle" class="s">actor-critic</text>
<text x="722" y="168" text-anchor="middle" class="s">30 種離散動作</text>
<text x="722" y="190" text-anchor="middle" class="s">油門／煞車／方向</text>
<path class="ar" d="M82,120 V168"/>
<path class="ar" d="M155,205 H188"/>
<path class="ar wm" d="M445,145 H478"/>
<path class="ar vla" d="M620,130 H653"/>
<path class="ar vla dash" d="M653,170 H622"/>
<text x="637" y="264" text-anchor="middle" class="s">策略出動作 ⇄ 世界模型推演</text>
</svg>
<figcaption>依 <a href="https://arxiv.org/abs/2402.16720">Think2Drive（ECCV 2024，arXiv:2402.16720）</a>：DreamerV3 式 RSSM；策略只在潛空間想像中學，想像長度 15 步，之後的回報交給 critic 估；撞車等「結束」片段優先重放；單張 A6000 約 3 天。輸入規格見<a href="https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06129-supp.pdf">補充材料</a>。</figcaption>
</figure>

**實例卡：[Think2Drive](https://arxiv.org/abs/2402.16720)（上海交大等，ECCV 2024）**

| 項目 | 內容 |
|---|---|
| 世界模型 | DreamerV3 式 **RSSM**：編碼器、GRU 序列模型、動力學預測器，加上獎勵頭、結束頭、重建解碼器；參數量論文未寫 |
| 輸入 | **不是相機畫面**，而是特權資訊畫成的鳥瞰圖：**128×128、34 通道**（道路、路線、自車、車道線、他車、行人、緊急車輛、障礙物、紅綠燈、停止標誌），取過去 4 個時間點 |
| 動作 | **30 種離散動作**，每種是油門、煞車、方向盤的一個組合 |
| 怎麼學 | 世界模型用真實互動資料學；策略（actor-critic）只在想像中學，想像 15 步；撞車等結束片段優先重放；從簡單情境逐步加難 |
| 算力 | 單張 A6000 約 **3 天** |
| VLA 學到什麼 | 39 種 CARLA v2 情境的處理方式：**Accident（多台事故車擋住部分車道，必須變換車道）成功率 0.81**、AccidentTwoWays 0.61、HardBrake（前車突然減速）1.0、HighwayCutIn 1.0；CornerCaseRepository 駕駛分數 **83.8**，無模型 RL 基線 Roach 只有 57.5 |

### 車禍畫面走一遍（②）

場景換成 CARLA 的 **Accident 情境**：前方車道上停著幾台事故車，自車必須變換車道繞過去（[Think2Drive 補充材料](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06129-supp.pdf)的定義）。

| 步驟 | 具體內容 |
|---|---|
| **0. 原始輸入** | 不是照片，而是 **128×128×34 的鳥瞰圖**：一層畫道路、一層畫要走的路線、一層畫自車、幾層畫事故車（障礙物）的位置與動態，取過去 4 個時間點 |
| **1. 指令／條件** | 沒有文字指令；「目標」由兩樣東西表達：鳥瞰圖裡的**路線層**（要往哪裡開）和**獎勵**（沿路線前進、不撞、不偏離）。世界模型的條件是**策略想試的動作**，例如「油門 0.5、方向 0」 |
| **2. 進哪個模組** | **編碼器**把鳥瞰圖壓成潛狀態 z → **GRU 序列模型**更新記憶 h → **動力學預測器**由 (h, z, 動作) 推出下一個 z → **獎勵頭**給分、**結束頭**判斷這一步會不會撞上 |
| **3. 輸出** | 每想像一步得到：下一個潛狀態、預測獎勵、預測「回合結束」的機率。連續想像 15 步，就是一條「如果我一直直開會怎樣」的推演 |
| **4. 怎麼變成 VLA 的訓練訊號** | 例如策略試「直開」：假設想像到第 8 步，結束頭說撞了，之後沒有獎勵 → 回報很低。再試「打方向變道」：15 步都沒結束、沿路線前進 → 回報高。critic 學會估每個潛狀態的價值，actor 往高回報的動作更新。**整個過程不用真的撞一次車** |
| **5. VLA 學到什麼** | 一條「看到前方有事故車 → 提早減速、確認旁邊車道 → 變道」的**決策策略**。它學的是**後果**（撞了就結束），不是模仿某個人的開法 |

!!! wm "② 在大型 VLA 上還少見，原因與現況"
    - **原因**：RSSM 這類模型要從頭在單一任務上學，吃不到網路影片的常識，也很難處理高解析度相機畫面；Think2Drive 就是靠特權鳥瞰圖繞開這個問題。
    - **大型 VLA 做「想像中 RL」時，目前多半用 ① 的影片世界模型**：[WMPO](https://arxiv.org/abs/2511.09515)（OpenSora 改的像素級影片擴散）、[VLA-RFT](https://arxiv.org/abs/2510.00406)（138M 自回歸）、[Ctrl-World](https://arxiv.org/abs/2510.10125)（SVD 初始化）。細節見 [08 訓練時 vs 推論時](train-vs-inference.html) 的 T3。
    - **潛空間 RL 正在往駕駛與 VLA 擴散**：[DreamerAD（arXiv:2603.24587）](https://arxiv.org/abs/2603.24587) 在潛空間預測下一幀、用 GRPO 做 RL，NAVSIM v2 EPDMS 87.7；[Imagine-RL（arXiv:2609.24033）](https://arxiv.org/abs/2609.24033) 凍結 π0，只在不重建像素的潛空間世界模型裡訓練一個小 actor，對 π0 平均相對提升約 60%。
    - 機器人上，Dreamer 式模型目前主要出現在 [DayDreamer](https://arxiv.org/abs/2206.14176)（真機直接學，非 VLA）和 [FOREWARN](https://arxiv.org/abs/2502.01828)（推論時預演候選動作，再由 VLM 挑）。

## ③ JEPA 世界模型：給 VLA「更會預判的眼睛」

JEPA 也預測未來，但**只在表徵空間比對**：把未來遮起來，讓模型猜「未來的表徵應該是什麼向量」，再和老師編碼器看真實未來後給出的向量比對。它不畫畫面、不需要動作標籤，所以能吃大量**沒有動作的影片**（人類影片、行車影片）。對 VLA 的用法主要是**預訓練或輔助損失（T1）**。

### 流程圖：VLA-JEPA 怎麼把 JEPA 接進 VLA 訓練

<figure class="dg">
<svg viewBox="0 0 800 280" role="img" aria-label="VLA-JEPA：用 JEPA 目標預訓練 VLA">
<text x="490" y="14" text-anchor="middle" class="s">梯度只回傳給學生（VLM＋預測器），老師凍結</text>
<path class="ar dash" d="M700,100 V22 H280 V38"/>
<rect class="n key" x="10" y="40" width="150" height="80" rx="10"/>
<text x="85" y="72" text-anchor="middle" class="b">當前畫面 t0</text>
<text x="85" y="96" text-anchor="middle" class="s">＋語言指令</text>
<rect class="n" x="10" y="170" width="150" height="80" rx="10"/>
<text x="85" y="202" text-anchor="middle" class="b">真實的未來幀</text>
<text x="85" y="226" text-anchor="middle" class="s">只給老師看</text>
<rect class="n vla" x="195" y="40" width="170" height="100" rx="10"/>
<text x="280" y="68" text-anchor="middle" class="b vla">VLM 學生</text>
<text x="280" y="90" text-anchor="middle" class="s">Qwen3-VL-2B</text>
<text x="280" y="110" text-anchor="middle" class="s">＋潛在動作 token</text>
<text x="280" y="128" text-anchor="middle" class="s">→ 另接 flow matching 動作頭</text>
<rect class="n wm" x="400" y="40" width="170" height="100" rx="10"/>
<text x="485" y="74" text-anchor="middle" class="b wm">預測器</text>
<text x="485" y="96" text-anchor="middle" class="s">自回歸 Transformer</text>
<text x="485" y="116" text-anchor="middle" class="s">→ 預測未來的表徵</text>
<rect class="n" x="195" y="170" width="170" height="80" rx="10"/>
<text x="280" y="202" text-anchor="middle" class="b">凍結的 V-JEPA 2</text>
<text x="280" y="226" text-anchor="middle" class="s">老師 → 目標表徵</text>
<rect class="n key" x="610" y="100" width="180" height="90" rx="10"/>
<text x="700" y="136" text-anchor="middle" class="b key">潛空間回歸損失</text>
<text x="700" y="160" text-anchor="middle" class="s">預測向量 vs 目標向量</text>
<path class="ar" d="M160,80 H193"/>
<path class="ar vla" d="M365,90 H398"/>
<path class="ar wm" d="M570,90 H590 V130 H608"/>
<path class="ar" d="M160,210 H193"/>
<path class="ar" d="M365,210 H590 V160 H608"/>
</svg>
<figcaption>依 <a href="https://arxiv.org/abs/2602.10098">VLA-JEPA（arXiv:2602.10098）</a>：學生只看當前畫面與指令，從不看未來；老師是凍結的 V-JEPA 2 編碼器。人類影片（沒有動作）只算這條潛空間損失；機器人資料再加上 flow matching 動作損失。整張圖不生成任何畫面。</figcaption>
</figure>

**實例卡：[VLA-JEPA](https://arxiv.org/abs/2602.10098)（中國科大等，2026-02）**

| 項目 | 內容 |
|---|---|
| VLA 骨幹 | **Qwen3-VL-2B**；動作頭是 conditional flow matching |
| 世界模型的角色 | 老師：**凍結的 V-JEPA 2 編碼器**把真實未來幀編成目標向量；學生的預測器（自回歸 Transformer）要從「當前畫面＋潛在動作 token」猜出這些向量 |
| 預訓練資料 | 人類影片 **Something-Something-v2 約 22 萬段**（沒有動作，只算世界模型損失）＋ 機器人 **DROID 約 7.6 萬條**（加算動作損失） |
| 微調資料 | LIBERO 約 2,000 條示範；SimplerEnv 用 Fractal 與 BridgeV2；真機 3 個抓放任務共 100 條示範 |
| 成果 | LIBERO 平均 **97.2%**（π0.5 96.9%、OpenVLA-OFT 97.1%）；LIBERO-Plus（加干擾的強韌性測試）**79.5%**，拿掉人類影片只剩 62.9% |
| VLA 學到什麼 | **從沒有動作的人類影片學到「世界接下來會怎樣」**，在畫面被干擾時特別有用（LIBERO-Plus 多 16.6 個百分點） |

**實例卡：[Drive-JEPA](https://arxiv.org/abs/2601.22032)（Virginia Tech、小鵬汽車等，2026-01）**

| 項目 | 內容 |
|---|---|
| 世界模型 | 從 V-JEPA 2 權重出發的 **ViT-L 編碼器（307M）**，再用 V-JEPA 目標在行車影片上繼續預訓練 |
| 預訓練資料 | 約 **208 小時**前視行車影片（CoVLA、DrivingDojo、OpenScene），每段 8 幀、2 Hz、512×256；8 張 H800 約 3 天 |
| 接上的駕駛模型 | 規劃器以編碼器特徵為基礎，產生 32 條候選軌跡並逐步修正（完整版另用 BEV 特徵）；訓練目標除了人類軌跡，還有模擬器評分後的多條「老師軌跡」 |
| 成果 | NAVSIM v1 **93.3 PDMS**、v2 **87.8 EPDMS**；只用影片特徵、不用感知模組的版本 89.0 PDMS，比先前最佳（Epona 86.1）高約 3 分 |
| VLA 學到什麼 | **從沒有標註的行車影片學到車流怎麼動**，讓後面的規劃器少靠人工標註的感知結果 |

### 車禍畫面走一遍（③）

同一段「雨天前車急煞、自車追撞」的影片，這次用 Drive-JEPA 的格式（8 幀、2 Hz，約 4 秒）。

| 步驟 | 具體內容 |
|---|---|
| **0. 原始輸入** | 8 幀前視畫面（512×256）。前 4 幀是「前車煞燈亮、距離縮短」，後 4 幀是「撞上」 |
| **1. 指令／條件** | **預訓練階段不需要任何指令或動作標籤**，這是 JEPA 能吃大量影片的原因。只有在接 VLA 做下游訓練時，才會加上導航指令「直行」（VLA-JEPA 的機器人版則是語言指令） |
| **2. 進哪個模組** | 先**遮罩**：把後 4 幀（或影片中的時空區塊）遮掉 → **學生編碼器**只看沒遮的部分 → **預測器**猜被遮部分的表徵；同時**老師編碼器**（EMA 或凍結）看完整影片，給出被遮部分的真實表徵 |
| **3. 輸出** | **不是影片**，而是一組向量：每個被遮的影像小塊一個（ViT-L 每個向量 1,024 維）。模型不需要畫出撞擊瞬間的碎玻璃，只要猜對「這一塊的語意與運動是什麼」 |
| **4. 怎麼變成 VLA 的訓練訊號** | 預測向量與老師向量的差距就是損失，梯度回傳到學生編碼器。要猜對「後 4 幀前車會停在自車正前方、距離變 0」，編碼器**被迫把前車的相對速度、煞燈、距離編進特徵裡**。預訓練完，規劃器接在這個編碼器上，用人類軌跡和模擬器評分的軌跡學開車 |
| **5. VLA 學到什麼** | 一雙**會預判的眼睛**：特徵裡已經帶有「前車在減速、快撞了」的訊號，規劃頭更容易學會提早減速。雨滴、反光這類**無法預測的細節會被自動忽略**，因為猜它們沒有好處 |

!!! warn "JEPA 的限制"
    JEPA 學到的是**特徵**，不是可以操控的模擬器：它不能幫你生成「如果我提早煞車會怎樣」的新影片，也不能當練習場讓策略試錯。要做反事實推演，得在 JEPA 表徵上再訓一個「以動作為條件」的預測器，例如 [V-JEPA 2-AC](https://arxiv.org/abs/2506.09985)（300M 預測器，只用 62 小時 DROID 機器人影片），但它目前用在推論時的規劃（I3），不是拿來訓練 VLA。

## ④ 3D／4D 世界模型（簡述）

這一類預測未來的 3D 佔據（occupancy）、點雲或高斯場景，例如 [OccWorld（arXiv:2311.16038）](https://arxiv.org/abs/2311.16038) 在 3D 佔據空間裡同時預測場景演變與自車軌跡。自駕上常見於**同時學預測與規劃**（類似 T1）；機器人上多用於造多視角一致的模擬場景。用車禍畫面來說，它輸出的不是影片，而是「下一秒哪些立體格子會被前車佔住」，VLA 從中學到的是**幾何上的碰撞風險**。

## 三類並排：同一個問題問六次

| | ① 影片生成 | ② 潛空間動力學 | ③ JEPA |
|---|---|---|---|
| 世界模型預測什麼 | 未來的畫面（像素或影片潛在，再解碼） | 精簡潛狀態＋獎勵＋會不會結束 | 未來的表徵向量，不重建畫面 |
| 車禍畫面進去後輸出 | 「撞上」與「及時煞停」兩段影片 | 每一步的潛狀態、分數、撞了沒 | 被遮住那幾秒的特徵向量 |
| 需要什麼條件 | 文字、他車框、自車動作 | 策略想試的動作 | 都不用（自監督） |
| 給 VLA 的東西 | 新資料（T2）、練習場（T3）、考官（T4） | 想像中的回報，用來做 RL（T3） | 預訓練或輔助損失的梯度（T1） |
| VLA 學到什麼 | 罕見危險場景的開法、偏離後怎麼救 | 依「後果」做決策：提早變道、煞車 | 會預判的視覺特徵 |
| 實際例子 | DreamGen → GR00T N1／N1.5；comma.ai → openpilot；GAIA-2 | Think2Drive；DreamerAD；DayDreamer | VLA-JEPA；Drive-JEPA；JEPA-VLA |
| 世界模型規模 | 大：GAIA-2 8.4B、comma.ai 500M、Wan 2.1 1.3B／14B | 小且快：DreamerV3 12M–400M、單張 GPU 3 天 | 中：V-JEPA 2 編碼器 300M–1B |
| 主要代價 | 貴、慢、物理可能錯 | 吃不到網路常識，難處理真實相機畫面 | 只給特徵，不能當模擬器 |
| 推論時在嗎 | 通常不在（I1、I2 是例外） | 不在 | 編碼器通常留下當 VLA 的眼睛；預測器拿掉 |

!!! key "怎麼選"
    - **資料不夠、危險場景收不到** → ① 當資料工廠（DreamGen、GAIA-2）。
    - **想讓策略從後果學、又不能真撞** → 高解析度相機用 ① 當練習場（comma.ai、WMPO）；有結構化輸入（鳥瞰圖、狀態）可用 ② 走快速 RL（Think2Drive）。
    - **有大量沒標註的影片，想讓 VLA 的眼睛更懂動態** → ③ 當預訓練目標（VLA-JEPA、Drive-JEPA）。
    - 三者不互斥：一個團隊可以用 ③ 預訓練編碼器、① 造資料、再用 ① 或 ② 做 RL。Tesla 的 Policy NN＋World Sim NN 閉環就是 ① 同時當考官與練習場的例子，見 [案例：Tesla](tesla.html)。

## 參考資料

- ① 影片生成：[DreamGen（arXiv:2505.12705）](https://arxiv.org/abs/2505.12705)、[DreamGen 官方頁](https://research.nvidia.com/labs/gear/dreamgen)、[GR00T N1.5 官方頁](https://research.nvidia.com/labs/gear/gr00t-n1_5/)、[comma.ai：Learning to Drive from a World Model（arXiv:2504.19077）](https://arxiv.org/abs/2504.19077)、[GAIA-2（arXiv:2503.20523）](https://arxiv.org/abs/2503.20523)、[Wayve GAIA-2 發布報導](https://www.autonomousvehicleinternational.com/news/ai-sensor-fusion/wayve-launches-gaia-2-video-generative-world-model-for-synthetic-data-generation.html)、[WMPO（arXiv:2511.09515）](https://arxiv.org/abs/2511.09515)、[VLA-RFT（arXiv:2510.00406）](https://arxiv.org/abs/2510.00406)、[Ctrl-World（arXiv:2510.10125）](https://arxiv.org/abs/2510.10125)
- ② 潛空間動力學：[Think2Drive（arXiv:2402.16720）](https://arxiv.org/abs/2402.16720)、[Think2Drive 補充材料](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06129-supp.pdf)、[DreamerV3（arXiv:2301.04104）](https://arxiv.org/abs/2301.04104)、[DreamerAD（arXiv:2603.24587）](https://arxiv.org/abs/2603.24587)、[Imagine-RL（arXiv:2609.24033）](https://arxiv.org/abs/2609.24033)、[DayDreamer（arXiv:2206.14176）](https://arxiv.org/abs/2206.14176)、[FOREWARN（arXiv:2502.01828）](https://arxiv.org/abs/2502.01828)
- ③ JEPA：[VLA-JEPA（arXiv:2602.10098）](https://arxiv.org/abs/2602.10098)、[Drive-JEPA（arXiv:2601.22032）](https://arxiv.org/abs/2601.22032)、[V-JEPA 2（arXiv:2506.09985）](https://arxiv.org/abs/2506.09985)、[JEPA-VLA（arXiv:2602.11832）](https://arxiv.org/abs/2602.11832)
- 指令格式：[NAVSIM（arXiv:2406.15349）](https://arxiv.org/abs/2406.15349)
- ④ 3D：[OccWorld（arXiv:2311.16038）](https://arxiv.org/abs/2311.16038)
