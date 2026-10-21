# 起源與歷史：為什麼會有 VLA 與世界模型

<p class="lede">兩個名詞各自從不同的瓶頸長出來：VLA 要解決「機器人學不會泛化」，世界模型要解決「在真實世界試錯太貴、太慢」。2023 年後，大模型與影片生成讓它們匯流。</p>

!!! key "一句話"
    **VLA** 借用網路規模的圖文知識，彌補機器人資料的匱乏；**世界模型**讓智能體先在「腦中」模擬後果再行動。VLA 缺的是物理常識與可擴展的資料，世界模型正好能提供想像中的練習場與合成資料，所以 2025 年後的系統（NVIDIA Cosmos＋GR00T、π0.5、Gemini Robotics、V-JEPA 2）大多同時涉及兩者。

## 兩條路線的時間軸

<figure class="dg">
<svg viewBox="0 0 800 330" role="img" aria-label="VLA 與世界模型兩條路線的時間軸">
<text x="70" y="24" text-anchor="middle" class="h">1943–1991</text>
<text x="190" y="24" text-anchor="middle" class="h">2015–2018</text>
<text x="310" y="24" text-anchor="middle" class="h">2019–2022</text>
<text x="430" y="24" text-anchor="middle" class="h">2023</text>
<text x="550" y="24" text-anchor="middle" class="h">2024</text>
<text x="700" y="24" text-anchor="middle" class="h">2025–</text>
<text x="10" y="62" class="b vla">VLA 路線</text>
<path d="M30,100 H620" stroke="var(--vla)" stroke-width="2"/>
<circle cx="190" cy="100" r="6" fill="var(--vla)"/><circle cx="310" cy="100" r="6" fill="var(--vla)"/>
<circle cx="430" cy="100" r="8" fill="var(--vla)"/><circle cx="550" cy="100" r="6" fill="var(--vla)"/>
<text x="70" y="106" text-anchor="middle" class="s">手工模組化管線</text>
<text x="190" y="88" text-anchor="middle" class="b">端到端視動</text>
<text x="190" y="124" text-anchor="middle" class="s">Levine 2015</text>
<text x="310" y="88" text-anchor="middle" class="b">SayCan・RT-1</text>
<text x="310" y="124" text-anchor="middle" class="s">LLM 接上機器人</text>
<text x="430" y="86" text-anchor="middle" class="b vla">RT-2</text>
<text x="430" y="124" text-anchor="middle" class="s">「VLA」誕生</text>
<text x="550" y="88" text-anchor="middle" class="b">OpenVLA・π0</text>
<text x="550" y="124" text-anchor="middle" class="s">開源、連續動作</text>
<text x="10" y="196" class="b wm">世界模型路線</text>
<path d="M30,240 H620" stroke="var(--wm)" stroke-width="2"/>
<circle cx="70" cy="240" r="6" fill="var(--wm)"/><circle cx="190" cy="240" r="8" fill="var(--wm)"/>
<circle cx="310" cy="240" r="6" fill="var(--wm)"/><circle cx="430" cy="240" r="6" fill="var(--wm)"/><circle cx="550" cy="240" r="8" fill="var(--wm)"/>
<text x="70" y="228" text-anchor="middle" class="b">Craik・Dyna</text>
<text x="70" y="264" text-anchor="middle" class="s">心智模型、想像經驗</text>
<text x="190" y="226" text-anchor="middle" class="b wm">World Models</text>
<text x="190" y="264" text-anchor="middle" class="s">Ha &amp; Schmidhuber 2018</text>
<text x="310" y="228" text-anchor="middle" class="b">MuZero・Dreamer</text>
<text x="310" y="264" text-anchor="middle" class="s">潛空間想像</text>
<text x="430" y="228" text-anchor="middle" class="b">UniPi・UniSim</text>
<text x="430" y="264" text-anchor="middle" class="s">影片生成用於決策</text>
<text x="550" y="226" text-anchor="middle" class="b wm">Sora・Genie</text>
<text x="550" y="264" text-anchor="middle" class="s">世界模擬器成熱詞</text>
<path class="ar vla" d="M620,100 C650,100 650,150 638,150"/>
<path class="ar wm" d="M620,240 C650,240 650,190 638,190"/>
<rect class="n mix" x="640" y="120" width="150" height="100" rx="12"/>
<text x="715" y="152" text-anchor="middle" class="b mix">兩者匯流</text>
<text x="715" y="176" text-anchor="middle" class="s">Cosmos＋GR00T</text>
<text x="715" y="196" text-anchor="middle" class="s">π0.5・V-JEPA 2</text>
<text x="715" y="212" text-anchor="middle" class="s">Genie 3</text>
<text x="400" y="310" text-anchor="middle" class="s">上排：機器人學走向「借用大模型」；下排：強化學習走向「學一個可想像的世界」</text>
</svg>
<figcaption>兩條路線各自從不同的瓶頸出發，到 2025 年前後在同一批系統中匯流。</figcaption>
</figure>

## 一、VLA 之前：機器人學卡在哪裡

!!! key "結論"
    機器人學長期是「一個任務一個模型」，無法像 NLP、CV 那樣靠大資料加大模型得到泛化。VLA 的本質是**借用網路規模的圖文知識，彌補機器人資料的匱乏**。

### 瓶頸 1：模組化管線太脆弱

傳統做法是「感知 → 狀態估計 → 任務規劃 → 運動規劃 → 控制」的手工管線。每一層都依賴人為設計的物體模型與規則，換一個沒見過的杯子或光線就可能失效。這就是 [Moravec 悖論](https://en.wikipedia.org/wiki/Moravec%27s_paradox)：對人類最簡單的感知與操作，對機器反而最難。

### 瓶頸 2：端到端學習有了，但泛化很差

2015 年 Levine 等人的 [End-to-End Visuomotor Policies](https://arxiv.org/abs/1504.00702) 證明可以直接從像素學到馬達指令。之後 Google 的 [QT-Opt](https://arxiv.org/abs/1806.10293) 用 7 台機械手臂收了 58 萬次抓取資料，但學到的只是「抓取」一個技能。每個新技能都要重新付出一次這種代價。

### 瓶頸 3：強化學習在真實世界太貴，模擬又有 sim2real gap

真實機器人會壞、會慢、需要人重置場景。改在模擬器訓練，又遇到物理與視覺差異；[Domain Randomization](https://arxiv.org/abs/1703.06907) 等技巧只能部分緩解。

### 瓶頸 4：機器人資料沒有「網路規模」

語言模型有整個網路可以訓練，機器人資料則分散在各實驗室、各種機型、各種格式，一個資料集常只有幾千到幾萬條軌跡。Sutton 的 [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) 指出通用方法加算力最終勝出，但機器人學缺的正是可以「堆」的資料。

### 瓶頸 5：語意理解與開放指令

「把可樂罐拿給泰勒絲」這種指令需要常識（誰是泰勒絲、哪個是可樂罐），傳統機器人只認得訓練時的類別。從 2018 年的視覺語言導航 [R2R](https://arxiv.org/abs/1711.07280) 到 2021 年的 [CLIPort](https://arxiv.org/abs/2109.12098)，研究者開始用預訓練的圖文表徵處理這個問題。

### 轉折點：大型語言模型與視覺語言模型成熟

2020 年後 GPT-3、[CLIP](https://arxiv.org/abs/2103.00020)、PaLI 等模型證明「一個大模型可以通殺很多任務」。機器人學界自然問：能不能把這些模型的世界知識直接轉成動作？這就是 VLA 的出發點。

## 二、VLA 的發展歷程

!!! key "結論"
    VLA 經歷三個階段：**「LLM 當大腦、傳統技能當小腦」（2022）→「把動作當 token、端到端訓練」（2023）→「開源化、跨機型資料、用擴散或 flow 輸出連續動作、大小腦雙系統」（2024–2025）**。

| 時間 | 里程碑 | 解決了什麼瓶頸 |
|---|---|---|
| 2022.04 | [SayCan](https://arxiv.org/abs/2204.01691)（Google） | LLM 拆解高層任務，再用「可供性」分數挑選機器人真的做得到的技能；解決開放指令理解 |
| 2022.05 | [Gato](https://arxiv.org/abs/2205.06175)（DeepMind） | 一個 Transformer 同時玩 Atari、聊天、控機械手臂，證明「動作也能序列化」 |
| 2022.07–09 | [Inner Monologue](https://arxiv.org/abs/2207.05608)、[Code as Policies](https://arxiv.org/abs/2209.07753) | LLM 用回饋或寫程式來指揮機器人，仍依賴下層手工技能 |
| 2022.10 | [VIMA](https://arxiv.org/abs/2210.03094) | 多模態提示（圖＋文）直接驅動操作策略 |
| 2022.12 | [RT-1](https://arxiv.org/abs/2212.06817)（Google） | 13 台機器人、約 13 萬條示範、700+ 種任務，證明 Transformer＋大資料在機器人上也有效 |
| 2023.03 | [PaLM-E](https://arxiv.org/abs/2303.03378) | 562B 參數的具身多模態模型，把感測器資訊注入 LLM；主要輸出仍是高層計畫 |
| 2023.03–04 | [Diffusion Policy](https://arxiv.org/abs/2303.04137)、[ACT／ALOHA](https://arxiv.org/abs/2304.13705) | 用擴散模型與 action chunking 解決「多模態動作分布」與精細操作，後來成為 VLA 動作頭的標準設計 |
| **2023.07** | **[RT-2](https://arxiv.org/abs/2307.15818)（Google DeepMind）** | **正式提出「VLA」。把動作離散化成文字 token，與網路圖文資料一起微調 VLM，讓網路知識直接轉移到動作** |
| 2023.10 | [Open X-Embodiment／RT-X](https://arxiv.org/abs/2310.08864) | 21 個機構、22 種機器人、100 萬條以上軌跡合併，直接攻擊「資料不夠大」 |
| 2024.05 | [Octo](https://arxiv.org/abs/2405.12213) | 開源通用機器人策略，可快速微調到新機型 |
| 2024.06 | [OpenVLA](https://arxiv.org/abs/2406.09246) | 7B 開源 VLA，效果超過 55B 的 RT-2-X，讓學界也能做 VLA |
| 2024.10 | [π0](https://arxiv.org/abs/2410.24164)（Physical Intelligence） | VLM 主幹＋flow matching 動作專家，輸出 50 Hz 連續動作，解決「離散 token 太粗、太慢」 |
| 2025.01 | [FAST](https://arxiv.org/abs/2501.09747) | 用 DCT 壓縮動作 token，讓自回歸 VLA 也能處理高頻精細動作 |
| 2025.02–03 | [Helix](https://www.figure.ai/news/helix)、[GR00T N1](https://arxiv.org/abs/2503.14734)、[Gemini Robotics](https://arxiv.org/abs/2503.20020) | 「系統 2 慢思考＋系統 1 快反應」雙系統，走向人形機器人與業界落地 |
| 2025.04 | [π0.5](https://arxiv.org/abs/2504.16054) | 在沒見過的真實家庭完成長時程清潔任務，重點放在開放世界泛化 |

!!! note "關鍵觀察"
    VLA 不是一個新理論，而是一個「工程假設」的勝利：只要把動作當成另一種模態，就能搭上 LLM／VLM 的規模化便車。後續大部分研究都在修補這個假設帶來的新問題：動作精度、推論速度、資料來源。

## 三、世界模型之前：智能體卡在哪裡

!!! key "結論"
    世界模型的動機一直沒變：**「先在腦中模擬世界，再行動」**，用來解決真實試錯太貴、無法規劃、不懂物理三大問題。不同年代只是「用什麼模型來模擬」不同。

### 思想源頭：認知科學與控制理論

- 1943 年心理學家 Kenneth Craik 在《The Nature of Explanation》提出「心智模型」：生物在腦中建立外界的小型模型，用來預測後果、試跑選項。
- 控制理論的「系統識別＋模型預測控制（MPC）」是同一概念的工程版本：先學動態模型，再用它規劃。

### 瓶頸 1：無模型強化學習的樣本效率太差

[DQN](https://www.nature.com/articles/nature14236) 玩一個 Atari 遊戲要大約 2 億幀，等於人類連玩數百小時。在遊戲裡可以，在真實機器人或自駕車上不行。危險的試錯（撞車、摔壞機器人）更不能在現實中做。

### 瓶頸 2：反應式策略不會「想」

只學「看到 X 就做 Y」的策略沒有規劃能力，遇到需要多步推理或訓練分布之外的情況就失效。AlphaGo 強是因為有完美的規則模型可以搜尋；真實世界沒有現成規則，所以要「學」一個出來。

### 瓶頸 3：早期模型式 RL 的「模型誤差」

1990–2010 年代的方法（如用高斯過程的 [PILCO](https://mlg.eng.cam.ac.uk/pub/pdf/DeiRas11.pdf)）在低維狀態很有效，但遇到像素這種高維輸入就學不好；模型一旦有誤差，多步展開會越滾越大（compounding error），策略還會「鑽模型漏洞」。這是模型式 RL 長期打不過無模型 RL 的主因。

### 瓶頸 4：大語言模型不懂物理世界

2022 年 Yann LeCun 在 [A Path Towards Autonomous Machine Intelligence](https://openreview.net/pdf?id=BZ5a1r-kVsf) 主張：只靠文字的自回歸 LLM 缺乏物理常識與規劃能力，學會「預測世界如何變化」的世界模型才是通往人類級智能的關鍵。這把世界模型從 RL 子領域拉高到 AGI 路線之爭。

### 瓶頸 5：自駕與機器人的長尾場景

真實資料永遠收不齊罕見危險場景，傳統模擬器（CARLA、Isaac Sim）又要大量人工建場景。「學出來的神經模擬器」可以自動生成這些場景，這是 Wayve、Tesla、NVIDIA 積極投入的原因。

## 四、世界模型的發展歷程

!!! key "結論"
    世界模型有兩條主線：**RL 路線**（在潛空間想像來訓練策略，代表 Dreamer、MuZero）與**生成路線**（用影片生成模型當世界模擬器，代表 Sora、Genie、Cosmos）。LeCun 的 **JEPA** 主張第三條：只在表徵空間預測，不生成像素。

| 時間 | 里程碑 | 意義 |
|---|---|---|
| 1943 | Craik《The Nature of Explanation》 | 提出「心智模型」，是世界模型的哲學源頭 |
| 1990 | Schmidhuber《Making the World Differentiable》 | 用 RNN 學環境模型並在其中規劃，也提出「好奇心」驅動探索 |
| 1991 | Sutton [Dyna](https://dl.acm.org/doi/10.1145/122344.122377) | 用學到的模型產生「想像經驗」訓練策略，是 Dreamer 的前身 |
| 2011 | [PILCO](https://mlg.eng.cam.ac.uk/pub/pdf/DeiRas11.pdf) | 模型式 RL 首次在真實控制任務展現驚人樣本效率 |
| **2018.03** | **[World Models](https://arxiv.org/abs/1803.10122)（Ha & Schmidhuber），[互動版](https://worldmodels.github.io/)** | **VAE（視覺）＋MDN-RNN（記憶與預測）＋小控制器；智能體在自己的「夢境」裡訓練再轉回真實環境，讓這個名詞廣為人知** |
| 2018.11 | [PlaNet](https://arxiv.org/abs/1811.04551) | 從像素學潛空間動態（RSSM）並直接在潛空間規劃 |
| 2019.03 | [SimPLe](https://arxiv.org/abs/1903.00374) | 在學到的影片預測模型裡玩 Atari，只用 10 萬步互動（Atari 100k 基準由此而來） |
| 2019.11 | [MuZero](https://arxiv.org/abs/1911.08265)（DeepMind） | 不需要遊戲規則，自己學「只為規劃而存在」的模型 |
| 2019–2023 | [Dreamer](https://arxiv.org/abs/1912.01603) → [DreamerV2](https://arxiv.org/abs/2010.02193) → [DreamerV3](https://arxiv.org/abs/2301.04104) | 在想像中學策略；V3 一組超參數通殺 150+ 任務，首次從零在 Minecraft 挖到鑽石 |
| 2022.06 | LeCun [JEPA 立場文](https://openreview.net/pdf?id=BZ5a1r-kVsf) | 把世界模型定位為自主智能的核心模組，主張在抽象表徵空間預測 |
| 2023.02 | [UniPi](https://arxiv.org/abs/2302.00111) | 「先生成影片計畫，再反推動作」，把影片生成用在決策上 |
| 2023.09 | [GAIA-1](https://arxiv.org/abs/2309.17080)（Wayve） | 自駕生成式世界模型，可用文字或動作控制生成駕駛場景 |
| 2023.10 | [UniSim](https://arxiv.org/abs/2310.06114) | 可互動的真實世界模擬器，在其中訓練的策略可零樣本轉到現實 |
| **2024.02** | **[Sora](https://openai.com/index/video-generation-models-as-world-simulators/)（OpenAI）、[Genie](https://arxiv.org/abs/2402.15391)（DeepMind）** | **Sora 主張擴展影片生成是通往物理世界模擬器的路；Genie 從無標註影片學出「潛在動作」，可互動。自此世界模型成為業界熱詞** |
| 2024.04 | [V-JEPA](https://arxiv.org/abs/2404.08471)（Meta） | 影片版 JEPA，在表徵空間預測被遮住的部分 |
| 2024.05–08 | [DIAMOND](https://arxiv.org/abs/2405.12399)、[GameNGen](https://arxiv.org/abs/2408.14837) | 用擴散模型即時模擬遊戲（GameNGen 可即時玩 DOOM） |
| 2025.01 | [NVIDIA Cosmos](https://arxiv.org/abs/2501.03575) | 「世界基礎模型平台」，專為機器人與自駕產生合成資料 |
| 2025.06 | [V-JEPA 2](https://arxiv.org/abs/2506.09985)（Meta） | 上百萬小時影片預訓練，再用少量機器人資料訓練動作條件模型，直接規劃抓放 |
| 2025.08 | [Genie 3](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)（DeepMind） | 文字生成可即時互動、維持數分鐘一致性的 3D 世界 |

## 五、兩條路線的交會

!!! key "結論"
    VLA 負責「懂指令、做動作」，世界模型負責「預測後果、提供練習場」。現在的趨勢是把兩者合進同一個具身基礎模型（詳見 〈[具身基礎模型與合成資料](synthetic-data.html)〉）。

- **世界模型 → VLA 的資料工廠**：Cosmos、Genie 類模型可以合成大量機器人影片與罕見場景，緩解 VLA「真實資料太少」。
- **世界模型 → VLA 的評測器**：在學到的模擬器中跑策略，比在真實機器人上評測便宜得多。
- **影片預測當 VLA 的預訓練目標**：如 ByteDance [GR-1](https://arxiv.org/abs/2312.13139) 先用影片預測預訓練，再微調成動作策略；UniPi、V-JEPA 2 也是「先預測世界，再推出動作」。
- **VLA → 世界模型的動作介面**：純影片生成模型不會「做事」，需要接上動作條件與策略才能閉環。

### 仍未解決的問題

1. **資料瓶頸只是緩解，沒有解決**：最大的開放機器人資料集仍遠小於網路文字與影片；遙操作收資料很貴。
2. **物理一致性**：影片生成式世界模型常「看起來對但物理錯」（物體穿透、消失），Sora 自己的技術報告也承認。
3. **生成像素 vs 預測表徵**：要不要生成像素（Sora／Genie 路線），還是只預測抽象表徵（JEPA 路線），學界仍在爭論。
4. **推論速度**：數十億參數的 VLA 要在機器人上跑到數十 Hz，是雙系統架構出現的直接原因。
5. **長時程任務與錯誤恢復**：以模仿學習為主的 VLA 失誤後很難自己修正，所以大家重新重視「用世界模型做規劃與 RL 微調」。
6. **評測標準**：真實機器人實驗難以重現，各家數字難以直接比較。

### 延伸閱讀

- [Open X-Embodiment 專案頁](https://robotics-transformer-x.github.io/)：跨機型資料的起點
- [World Models 互動論文](https://worldmodels.github.io/)：理解世界模型直覺最好的入門材料
- [Sora 技術報告](https://openai.com/index/video-generation-models-as-world-simulators/)：生成式世界模擬器的代表性主張
