# 案例：Tesla

<p class="lede">回答四個問題：Tesla 在哪個產品用了什麼模型？參數量多大？資料有多少、從哪裡來？VLA（策略）和世界模型是融合成一個、分開、還是別的接法？<b>只寫 Tesla 官方（財報、演講、官方活動頁、高層 X 貼文）或可靠媒體明寫的內容；查不到就寫「未公開」。</b>Tesla 沒有發表過 FSD 或 Optimus 的論文，所以技術細節幾乎都來自演講。整理日期 2026-10-22。</p>

## 重點先講

!!! key "六句話看懂 Tesla"
    1. **兩個產品、一套方法**：FSD（車）和 Optimus（人形機器人）都用「像素直接到動作」的端到端大模型，Tesla 在 CVPR 2026 直接說「我們不是在造一個駕駛產品，而是在為所有機器人構建一個統一的基礎模型」（[OFweek 演講整理](https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html)）。
    2. **策略與世界模型是「分開的兩個網路，接成閉環」**：Policy NN 負責開車／做事；World Sim NN 吃「目前狀態 + 動作」吐出下一刻的多鏡頭影片，再餵回 Policy。兩者用同一份車隊資料訓練，但**車上只跑策略，世界模型留在雲端**（[ICCV 2025 報導](https://www.humanoidsdaily.com/news/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus)、[CVPR 2026 整理](https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html)）。
    3. **世界模型的用途是「評估 + 強化學習 + 造對抗情境」**，對應本站的 [T4 評估器](train-vs-inference.html#t4) 與 [T3 想像中 RL](train-vs-inference.html#t3)；推論時屬於 [I0 不參與](train-vs-inference.html#i0)。
    4. **參數量官方從未給絕對數字**：只有 Musk 的相對說法，「新 FSD 模型約 10 倍參數」（2025-08）與「V15 會是大模型」（2026-04）。媒體寫的「約 10 億／100 億」不是官方數字。Optimus 與世界模擬器的參數量都未公開。
    5. **資料靠車隊**：約 130 萬輛具監督式 FSD 能力的車、FSD 累計里程接近 120 億英里（2026 Q2）。Optimus 則從遙操作與動作捕捉，改成**員工戴 5 鏡頭頭盔與背包錄製第一人稱影片**。
    6. **它算不算 VLA？** FSD 輸入有導航與指令、輸出 2 個動作 token，語言只當旁路的「解釋」輸出，比較接近本站說的 WA（World Action）派；Optimus 能用自然語言（語音／文字）叫出技能，按定義就是 VLA。

## 一張圖看懂：Tesla 的整體架構

<figure class="dg">
<svg viewBox="0 0 800 420" role="img" aria-label="Tesla 的資料、策略網路與世界模擬器閉環">
<text x="110" y="26" text-anchor="middle" class="h">資料從哪來</text>
<text x="400" y="26" text-anchor="middle" class="h">雲端訓練（Cortex 叢集）</text>
<text x="690" y="26" text-anchor="middle" class="h">部署（AI4 晶片）</text>
<rect class="n" x="15" y="50" width="190" height="96" rx="12"/>
<text x="110" y="78" text-anchor="middle" class="b">車隊</text>
<text x="110" y="100" text-anchor="middle" class="s">約 130 萬輛車</text>
<text x="110" y="118" text-anchor="middle" class="s">累計近 120 億英里</text>
<text x="110" y="136" text-anchor="middle" class="s">觸發器撈長尾片段</text>
<rect class="n" x="15" y="170" width="190" height="96" rx="12"/>
<text x="110" y="198" text-anchor="middle" class="b">Optimus 資料</text>
<text x="110" y="220" text-anchor="middle" class="s">5 鏡頭頭盔＋背包錄影</text>
<text x="110" y="238" text-anchor="middle" class="s">（早期：遙操作、動捕）</text>
<text x="110" y="256" text-anchor="middle" class="s">Optimus Academy</text>
<rect class="n vla" x="280" y="50" width="240" height="96" rx="12"/>
<text x="400" y="80" text-anchor="middle" class="b vla">Policy NN（策略）</text>
<text x="400" y="104" text-anchor="middle" class="s">影片＋導航＋運動學＋音訊</text>
<text x="400" y="124" text-anchor="middle" class="s">→ 動作（車：轉向、加速度）</text>
<rect class="n wm" x="280" y="230" width="240" height="96" rx="12"/>
<text x="400" y="260" text-anchor="middle" class="b wm">World Sim NN（世界模擬器）</text>
<text x="400" y="284" text-anchor="middle" class="s">目前狀態＋動作</text>
<text x="400" y="304" text-anchor="middle" class="s">→ 下一刻多鏡頭影片、運動學</text>
<path class="ar vla" d="M360,146 V228"/>
<text x="352" y="192" text-anchor="end" class="s vla">動作</text>
<path class="ar wm" d="M440,228 V148"/>
<text x="448" y="192" class="s wm">下一刻狀態</text>
<path class="ar" d="M205,98 H278"/>
<path class="ar" d="M205,218 C240,218 240,110 278,110"/>
<path class="ar dash" d="M205,120 C245,120 245,270 278,270"/>
<text x="110" y="296" text-anchor="middle" class="s">虛線：同一份資料</text>
<text x="110" y="314" text-anchor="middle" class="s">也拿來訓練世界模擬器</text>
<rect class="n key" x="280" y="350" width="240" height="56" rx="10"/>
<text x="400" y="374" text-anchor="middle" class="b">閉環用途</text>
<text x="400" y="394" text-anchor="middle" class="s">評估・回歸測試・對抗情境・RL</text>
<path class="ar" d="M400,326 V348"/>
<rect class="n vla" x="590" y="50" width="195" height="70" rx="12"/>
<text x="688" y="80" text-anchor="middle" class="b">FSD／Robotaxi</text>
<text x="688" y="102" text-anchor="middle" class="s">只跑策略，36 Hz</text>
<rect class="n vla" x="590" y="140" width="195" height="70" rx="12"/>
<text x="688" y="170" text-anchor="middle" class="b">Optimus</text>
<text x="688" y="192" text-anchor="middle" class="s">同一套方法，同一顆 AI4</text>
<path class="ar vla" d="M520,85 H588"/>
<path class="ar vla" d="M520,120 C555,120 555,175 588,175"/>
<rect class="n ghost" x="590" y="250" width="195" height="76" rx="12"/>
<text x="688" y="280" text-anchor="middle" class="b">世界模擬器不上車</text>
<text x="688" y="302" text-anchor="middle" class="s">推論時 = I0</text>
</svg>
<figcaption>策略和世界模擬器是兩個網路，在雲端接成閉環；車和機器人上只部署策略。資料來源：ICCV 2025 演講（<a href="https://x.com/aelluswamy/status/1981644831790379245">Ashok Elluswamy X 貼文</a>、<a href="https://www.humanoidsdaily.com/news/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus">Humanoids Daily</a>）、CVPR 2026 演講（<a href="https://www.youtube.com/watch?v=2V0ddkF1Svo">錄影</a>、<a href="https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html">OFweek 整理</a>）、<a href="https://www.aol.com/tesla-shifted-optimus-training-strategy-092502010.html">Business Insider</a>、<a href="https://notateslaapp.com/news/4481/summary-of-teslas-2026-q2-earnings-call-cybercab-fsd-ai4-and-more">2026 Q2 財報會議整理</a>。</figcaption>
</figure>

## 一、哪個產品用了什麼？

| 產品 | 用的模型 | 屬於哪一類 | 世界模型的角色 | 來源 |
|---|---|---|---|---|
| **FSD (Supervised) v12 起** | 單一端到端網路，取代 v11 的 30 萬行以上 C++ 規則 | 端到端策略（像素 → 控制） | 雲端評估、RL（車上不跑） | [v12 直播報導](https://evannex.com/blogs/news/tesla-ceo-elon-musk-test-drives-fsd-v12-in-livestream) |
| **FSD v13** | 同一路線，資料量增加 4.2 倍、輸入影片解析度更高、控制延遲減半 | 同上 | 同上 | [2024 Q4 財報](https://www.sec.gov/Archives/edgar/data/1318605/000162828025002993/exhibit991.htm) |
| **FSD v14**（2025-10 起） | 把 Robotaxi 用的大部分模型帶到一般車主；v14.3 加入「推理」、MLIR 重寫的編譯器與 runtime | 同上，多了語言推理旁路 | 同上 | [2025 Q3 財報](https://www.sec.gov/Archives/edgar/data/1318605/000162828025045861/exhibit991.htm)、[v14.3 報導](https://www.notateslaapp.com/news/3925/tesla-releases-fsd-143-fleet-learning-20-faster-reactions-and-more) |
| **FSD v14 Lite** | 把 AI4 上的駕駛行為蒸餾到 HW3（AI3）的算力限制內 | 蒸餾版策略 | — | [2026 Q2 財報會議整理](https://notateslaapp.com/news/4481/summary-of-teslas-2026-q2-earnings-call-cybercab-fsd-ai4-and-more) |
| **Robotaxi**（奧斯汀等） | Ashok 稱已在跑 **FSD V15** | 同上 | 同上 | [2026 Q2 財報會議整理](https://notateslaapp.com/news/4481/summary-of-teslas-2026-q2-earnings-call-cybercab-fsd-ai4-and-more) |
| **Optimus** | 「機器人上的單一神經網路（多工）」，技能用自然語言（語音／文字）呼叫 | **VLA**（視覺＋語言 → 動作） | 用同一套世界模擬器生成工廠、室內的動作條件影片 | [Milan Kovac X 貼文](https://x.com/_milankovac_/status/1925047791954612605)、[Not a Tesla App](https://www.notateslaapp.com/news/2761/teslas-optimus-is-now-learning-by-watching-first-person-today-third-person-tomorrow-video)、[Humanoids Daily](https://www.humanoidsdaily.com/news/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus) |
| **World Sim NN** | 神經網路影片生成引擎，可同時生成 8 路鏡頭畫面、接近即時 | **影片生成類世界模型**（見 [世界模型路線與流派](wm-architectures.html)） | 主角 | [NextBigFuture](https://www.nextbigfuture.com/2025/10/tesla-vp-ashok-describes-technology-of-fsd.html)、[華爾街見聞](https://wallstreetcn.com/articles/3757967) |

**「Drive in Video Generation」**：CVPR 2026 的 Tesla 攤位讓參觀者在 AI 生成的世界裡「開車」，也就是讓人親手操作 World Sim NN（[Tesla 官方活動頁](https://www.tesla.com/event/tesla-x-cvpr-2026)）。

## 二、策略網路：20 億個 token 進、2 個 token 出

<figure class="dg">
<svg viewBox="0 0 800 360" role="img" aria-label="FSD 策略網路的輸入、輸出與旁路輸出">
<text x="120" y="26" text-anchor="middle" class="h">輸入（約 20 億 token）</text>
<text x="400" y="26" text-anchor="middle" class="h">端到端大模型</text>
<text x="680" y="26" text-anchor="middle" class="h">輸出</text>
<rect class="n" x="15" y="45" width="210" height="64" rx="10"/>
<text x="120" y="72" text-anchor="middle" class="b">多鏡頭影片</text>
<text x="120" y="93" text-anchor="middle" class="s">7 路 × 36 FPS × 5 MP × 30 秒</text>
<rect class="n" x="15" y="121" width="210" height="44" rx="10"/>
<text x="120" y="148" text-anchor="middle" class="b">導航地圖與指令</text>
<rect class="n" x="15" y="177" width="210" height="44" rx="10"/>
<text x="120" y="204" text-anchor="middle" class="b">運動學 100 Hz</text>
<rect class="n" x="15" y="233" width="210" height="44" rx="10"/>
<text x="120" y="260" text-anchor="middle" class="b">音訊 48 kHz</text>
<path class="ar" d="M225,77 H298"/><path class="ar" d="M225,143 H298"/><path class="ar" d="M225,199 H298"/><path class="ar" d="M225,255 H298"/>
<rect class="n vla" x="300" y="45" width="200" height="232" rx="14"/>
<text x="400" y="140" text-anchor="middle" class="b vla">Policy NN</text>
<text x="400" y="164" text-anchor="middle" class="s">以 36 Hz 執行</text>
<text x="400" y="184" text-anchor="middle" class="s">參數量：未公開</text>
<rect class="n key" x="575" y="45" width="210" height="80" rx="12"/>
<text x="680" y="76" text-anchor="middle" class="b">2 個動作 token</text>
<text x="680" y="100" text-anchor="middle" class="s">轉向、加速度 → 控制車輛</text>
<path class="ar vla" d="M500,85 H573"/>
<rect class="n ghost" x="575" y="150" width="210" height="190" rx="12"/>
<text x="680" y="176" text-anchor="middle" class="b">旁路輸出（不控制車）</text>
<text x="680" y="200" text-anchor="middle" class="s">3D 佔據與流</text>
<text x="680" y="220" text-anchor="middle" class="s">車、行人等物體</text>
<text x="680" y="240" text-anchor="middle" class="s">車道、號誌、限速</text>
<text x="680" y="260" text-anchor="middle" class="s">生成式 3D 高斯</text>
<text x="680" y="280" text-anchor="middle" class="s">自然語言決策理由</text>
<text x="680" y="310" text-anchor="middle" class="s">用途：除錯、安全檢查</text>
<path class="ar dash" d="M500,220 H573"/>
</svg>
<figcaption>20 億 token 是 Tesla 投影片的估算：7 × 36 × 500 萬像素 × 30 秒，以 5×5 像素為一塊。旁路輸出可以「被提示」才產生，用來解釋與除錯，不直接開車。資料來源：<a href="https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html">CVPR 2026 演講整理</a>、<a href="https://www.nextbigfuture.com/2025/10/tesla-vp-ashok-describes-technology-of-fsd.html">ICCV 2025 演講整理</a>。</figcaption>
</figure>

- **為什麼這樣設計**：Ashok 在 2023 年的 v12 直播中說，v11 有 30 萬行以上 C++，v12 幾乎全部拿掉，「沒有一行程式碼寫著這裡有圓環」（[v12 直播報導](https://evannex.com/blogs/news/tesla-ceo-elon-musk-test-drives-fsd-v12-in-livestream)）。
- **語言在哪裡**：ICCV 2025 演講提到工程師可以用自然語言問模型「為什麼這樣決定」；CVPR 2026 展示了施工改道的思維鏈推理範例；v14.3 發布說明寫了「reasoning」並計畫擴到所有駕駛行為（[NextBigFuture](https://www.nextbigfuture.com/2025/10/tesla-vp-ashok-describes-technology-of-fsd.html)、[OFweek](https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html)、[v14.3 報導](https://www.notateslaapp.com/news/3925/tesla-releases-fsd-143-fleet-learning-20-faster-reactions-and-more)）。**語言推理是否進入控制迴路、用多少延遲：未公開。**
- **旁路輸出是不是訓練目標**：Tesla 只說模型「可以被提示輸出」這些東西；它們是否同時當輔助 loss 使用，未公開。

## 三、世界模型：World Sim NN

<figure class="dg">
<svg viewBox="0 0 800 250" role="img" aria-label="World Sim NN 的閉環與四種用途">
<rect class="n vla" x="40" y="40" width="200" height="80" rx="12"/>
<text x="140" y="74" text-anchor="middle" class="b vla">Policy NN</text>
<text x="140" y="98" text-anchor="middle" class="s">待評估的新版策略</text>
<rect class="n wm" x="40" y="150" width="200" height="80" rx="12"/>
<text x="140" y="184" text-anchor="middle" class="b wm">World Sim NN</text>
<text x="140" y="208" text-anchor="middle" class="s">狀態 t ＋ 動作 → 狀態 t+1</text>
<path class="ar vla" d="M100,120 V148"/><path class="ar wm" d="M180,148 V122"/>
<text x="92" y="139" text-anchor="end" class="s">動作</text>
<text x="188" y="139" class="s">8 路影片</text>
<path class="ar" d="M240,135 H318"/>
<rect class="n key" x="320" y="20" width="215" height="96" rx="10"/>
<text x="428" y="46" text-anchor="middle" class="b">① 閉環評估</text>
<text x="428" y="68" text-anchor="middle" class="s">開環 loss 和實車表現</text>
<text x="428" y="86" text-anchor="middle" class="s">相關性不高</text>
<rect class="n key" x="560" y="20" width="215" height="96" rx="10"/>
<text x="668" y="46" text-anchor="middle" class="b">② 重播歷史問題</text>
<text x="668" y="68" text-anchor="middle" class="s">從真實紀錄「分岔」，</text>
<text x="668" y="86" text-anchor="middle" class="s">驗證新版有沒有修好</text>
<rect class="n key" x="320" y="134" width="215" height="96" rx="10"/>
<text x="428" y="160" text-anchor="middle" class="b">③ 注入對抗情境</text>
<text x="428" y="182" text-anchor="middle" class="s">行人衝出、車輛切入</text>
<text x="428" y="200" text-anchor="middle" class="s">等長尾案例</text>
<rect class="n key" x="560" y="134" width="215" height="96" rx="10"/>
<text x="668" y="160" text-anchor="middle" class="b">④ 大規模 RL</text>
<text x="668" y="182" text-anchor="middle" class="s">目標「超越人類」；</text>
<text x="668" y="200" text-anchor="middle" class="s">細節未公開</text>
</svg>
<figcaption>資料來源：ICCV 2025 演講（<a href="https://www.humanoidsdaily.com/news/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus">Humanoids Daily</a>、<a href="https://www.nextbigfuture.com/2025/10/tesla-vp-ashok-describes-technology-of-fsd.html">NextBigFuture</a>）、CVPR 2026 演講（<a href="https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html">OFweek</a>）。</figcaption>
</figure>

| 項目 | 公開資訊 | 來源 |
|---|---|---|
| 輸入 → 輸出 | 目前狀態 + 策略動作 → 下一刻狀態：鏡頭畫面、導航、運動學、音訊 | [OFweek](https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html) |
| 鏡頭與長度 | 同時生成 8 路鏡頭；媒體報導可一次生成長達 6 分鐘的影片 | [NextBigFuture](https://www.nextbigfuture.com/2025/10/tesla-vp-ashok-describes-technology-of-fsd.html)、[華爾街見聞](https://wallstreetcn.com/articles/3757967) |
| 速度 | 「接近即時」、壓縮算力後可即時執行；精確延遲未公開 | 同上 |
| 訓練資料 | 與策略同一份車隊資料；用「便宜易得的狀態-動作資料」，不需要人工精細標註 | [Humanoids Daily](https://www.humanoidsdaily.com/news/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus)、[Medium 整理](https://medium.com/@byaman019/a-peek-into-teslas-autonomous-future-core-tech-revealed-by-vp-ashok-elluswamy-at-iccv-2025-906df7ae95de) |
| Optimus 版本 | 生成 Optimus 在工廠走路、轉彎的畫面，同時 4 路機器人視角；動作條件影片生成用於導航 | [Humanoids Daily](https://www.humanoidsdaily.com/news/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus)、[NextBigFuture](https://www.nextbigfuture.com/2025/10/tesla-vp-ashok-describes-technology-of-fsd.html) |
| 獎勵怎麼算 | 演講提到生成式世界模擬器裡的獎勵與懲罰，細節未公開 | [Matroid 演講大綱](https://podwise.ai/episodes/7101406) |
| 參數量、架構 | **未公開**（沒說是擴散還是自迴歸） | — |

!!! warning "「一天學 500 年駕駛經驗」怎麼看"
    中文媒體報導 Tesla 稱 AI「一天之內能學習相當於人類 500 年的駕駛經驗」（[華爾街見聞](https://wallstreetcn.com/articles/3757967)），但該報導沒有附演講原文，也沒說是指車隊資料量還是模擬器吞吐量。本站把它當媒體轉述，不當正式數據。

## 四、參數量

| 模型 | 官方說法 | 媒體說法（非官方） | 來源 |
|---|---|---|---|
| FSD v12／v13 | 未公開 | — | — |
| FSD v14 | 未公開絕對數字；Musk 2025-08：「正在訓練約 **10 倍參數**的新 FSD 模型，並大幅改善影片壓縮 loss」 | — | [Musk 貼文報導](https://www.notateslaapp.com/news/2999/tesla-fsds-10x-parameter-update-many-new-features-release-in-september) |
| FSD v14.3 | Musk 2026-04：「小模型進步太快，大模型還沒追上」 | 約 10 億參數的「小模型」 | [Musk X 貼文](https://x.com/elonmusk/status/2042082006314709086)、[Not a Tesla App](https://www.notateslaapp.com/news/3933/elon-musk-fsd-10x-parameter-upgrade-now-coming-with-v15) |
| FSD V15 | Musk：「V15 會是大模型」 | 約 100 億參數（「10 倍」大模型） | 同上 |
| Optimus 策略 | 未公開 | — | — |
| World Sim NN | 未公開 | — | — |

**注意**：有部落格寫「上兆參數」，那是作者估計，不採用。v14 的「10 倍」與 v15 的「大模型」可能指同一個模型（原本預計 2025 年推出，後來延到 V15），Musk 沒有說明兩者關係。

## 五、資料：有多少、從哪裡來

### 車（FSD）

| 指標 | 數字 | 時間 | 來源 |
|---|---|---|---|
| FSD 累計里程 | 超過 30 億英里 | 2025-01 | [2024 Q4 財報](https://www.sec.gov/Archives/edgar/data/1318605/000162828025002993/exhibit991.htm) |
| FSD 累計里程 | 超過 108 億英里（其中城市道路約 40.7 億） | 2026-06（CVPR 投影片） | [OFweek](https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html) |
| FSD 累計里程 | 接近 120 億英里；歐洲超過 5,000 萬公里 | 2026-07（Q2 財報會議） | [Not a Tesla App](https://notateslaapp.com/news/4481/summary-of-teslas-2026-q2-earnings-call-cybercab-fsd-ai4-and-more) |
| 具監督式 FSD 能力的車 | 約 130 萬輛 | 2026-06 | [OFweek](https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html) |
| v13 訓練資料 | 比前一版多 4.2 倍（絕對量未公開） | 2025-01 | [2024 Q4 財報](https://www.sec.gov/Archives/edgar/data/1318605/000162828025002993/exhibit991.htm) |
| 訓練資料總量（小時、片段數） | **未公開** | — | — |

- **怎麼撈**：車上有「觸發器」，只把罕見片段（複雜路口、不尋常的用路人）傳回來，不是全部上傳（[NextBigFuture](https://www.nextbigfuture.com/2025/10/tesla-vp-ashok-describes-technology-of-fsd.html)）；v14.3 說明也提到用車隊收集「少見事件」與「困難的 RL 範例」（[v14.3 報導](https://www.notateslaapp.com/news/3925/tesla-releases-fsd-143-fleet-learning-20-faster-reactions-and-more)）。
- **官方自稱**：「世界上最大的具身 AI 資料集」（[Tesla CVPR 2026 活動頁](https://www.tesla.com/event/tesla-x-cvpr-2026)）。
- **公開影片**：Musk 說進中國市場的版本用了網路上公開的亞洲街道影片訓練（[Business Insider](https://www.aol.com/tesla-shifted-optimus-training-strategy-092502010.html)）。

### 機器人（Optimus）

| 時期 | 怎麼收資料 | 來源 |
|---|---|---|
| 2024 | 「資料收集員」穿動作捕捉衣、戴 VR 頭盔做遙操作 | [Business Insider](https://www.aol.com/tesla-shifted-optimus-training-strategy-092502010.html) |
| 2025-05 | 公布從**第一人稱人類影片**學會吸塵、煮菜、倒垃圾；下一步要學第三人稱網路影片並轉成第一人稱視角 | [Not a Tesla App](https://www.notateslaapp.com/news/2761/teslas-optimus-is-now-learning-by-watching-first-person-today-third-person-tomorrow-video) |
| 2025-06 起 | 改以影片為主：員工戴 **5 個自製鏡頭的頭盔與背包**錄自己做事（撿東西、摺 T 恤），以便更快擴大資料量 | [Business Insider](https://www.aol.com/tesla-shifted-optimus-training-strategy-092502010.html) |
| 2026 | Fremont 生產的 Optimus V3 早期機台進「Optimus Academy」收集訓練資料 | [2026 Q2 財報會議整理](https://notateslaapp.com/news/4481/summary-of-teslas-2026-q2-earnings-call-cybercab-fsd-ai4-and-more) |
| — | 資料總量（小時數、示範數） | **未公開** |

Musk 在 2025-01 財報會議說，Optimus 的訓練需求「最終可能至少是車的 10 倍」（[Business Insider](https://www.aol.com/tesla-shifted-optimus-training-strategy-092502010.html)）。

## 六、算力：Dojo 停了，改用 Cortex（NVIDIA GPU）

| 時間 | 事件 | 來源 |
|---|---|---|
| 2024 Q4 | Cortex 完工：德州超級工廠約 5 萬張 H100，「幫助實現 FSD v13」；2024 年訓練算力增加 400% 以上 | [2024 Q4 財報](https://www.sec.gov/Archives/edgar/data/1318605/000162828025002993/exhibit991.htm) |
| 2025 Q2 | 加 1.6 萬張 H200，Cortex 達 6.7 萬 H100 等效 | [TechCrunch](https://techcrunch.com/2025/09/02/tesla-dojo-the-rise-and-fall-of-elon-musks-ai-supercomputer/) |
| 2025-08 | **Dojo 專案關閉、團隊解散**；Musk 稱它是「演化上的死胡同」 | [TechCrunch](https://techcrunch.com/2025/08/11/elon-musk-confirms-shutdown-of-tesla-dojo-an-evolutionary-dead-end) |
| 2025 Q3 | Cortex 達 **8.1 萬 H100 等效** | [2025 Q3 財報](https://www.sec.gov/Archives/edgar/data/1318605/000162828025045861/exhibit991.htm) |
| 2026 Q2 | Cortex 1 約 90 MW、新的 Cortex 2 約 115 MW，同時訓練車隊與 Optimus | [2026 Q2 財報會議整理](https://notateslaapp.com/news/4481/summary-of-teslas-2026-q2-earnings-call-cybercab-fsd-ai4-and-more) |
| 推論端 | **AI4** 同時用在 FSD 與 Optimus，兩台電腦互相校驗；AI5「希望明年量產」；AI6 由 Samsung 代工（165 億美元合約） | [OFweek](https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html)、[2026 Q2 財報會議整理](https://notateslaapp.com/news/4481/summary-of-teslas-2026-q2-earnings-call-cybercab-fsd-ai4-and-more)、[TechCrunch](https://techcrunch.com/2025/09/02/tesla-dojo-the-rise-and-fall-of-elon-musks-ai-supercomputer/) |

## 七、融合還是分開？放進本站的分類

!!! key "答案：分開訓練的兩個網路，用閉環接起來；部署時只有策略"
    - **不是融合**：Tesla 沒有讓策略「先想像未來畫面再出動作」（那是 [I2](train-vs-inference.html#i2)，例如 1X），也沒有用世界模型在車上預演挑動作（[I3](train-vs-inference.html#i3-vla)）。
    - **也不是完全無關**：兩者吃同一份車隊資料，World Sim NN 的唯一任務就是當 Policy NN 的「考場與練習場」。
    - **最接近**：本站 [T4 評估器](train-vs-inference.html#t4) + [T3 想像中 RL](train-vs-inference.html#t3) + 用世界模型「造」長尾情境（與 [T2 資料工廠](train-vs-inference.html#t2) 相近，但 Tesla 只說用在測試與 RL，沒說把生成影片當模仿學習資料）。

| 本站代號 | Tesla 有沒有 | 根據 |
|---|---|---|
| T1 預訓練／輔助目標 | 未公開（旁路輸出存在，但沒說是不是訓練目標） | [NextBigFuture](https://www.nextbigfuture.com/2025/10/tesla-vp-ashok-describes-technology-of-fsd.html) |
| T2 資料工廠 | 部分：生成對抗與長尾情境 | [NextBigFuture](https://www.nextbigfuture.com/2025/10/tesla-vp-ashok-describes-technology-of-fsd.html) |
| T3 想像中 RL | ✅ 明說「大規模 RL」 | [Humanoids Daily](https://www.humanoidsdaily.com/news/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus) |
| T4 評估器 | ✅ 主要用途，CVPR 2026 稱評估是「最難的一題」 | [OFweek](https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html) |
| I0 推論不參與 | ✅ 車上只跑 Policy NN | 同上 |

**跟其他公司比**：Waymo 也把世界模型（基於 Genie 3）當模擬器，Gemini Robotics 用 Veo 當評估器，路線最接近 Tesla；字節 GR-2、智元 GE 則把世界模型直接當 VLA 的預訓練骨幹，Tesla 沒有公開這樣做。詳見 [世界模型代表作的實際應用](wm-in-practice.html) 與 [業界產品盤點](industry.html)。

## 八、還不知道的事

- FSD、Optimus、World Sim NN 的**參數量、層數、架構**（Transformer？擴散？）都未公開。
- 訓練資料**總時數、片段數**、資料配比未公開。
- RL 的**獎勵設計與演算法**未公開。
- Optimus 和 FSD 是「同一個模型、不同頭」還是「同一架構、各自訓練」：Tesla 只說「同一套方法、同一套世界模擬器、同一顆晶片」，沒有更細的說明。

## 主要來源

- 演講：[ICCV 2025 Ashok Elluswamy（X 貼文）](https://x.com/aelluswamy/status/1981644831790379245)、[CVPR 2026 WAD 議程](https://cvpr2026.wad.vision/)、[CVPR 2026 錄影](https://www.youtube.com/watch?v=2V0ddkF1Svo)、[Tesla × CVPR 2026 官方活動頁](https://www.tesla.com/event/tesla-x-cvpr-2026)
- 財報：[2024 Q4 更新](https://www.sec.gov/Archives/edgar/data/1318605/000162828025002993/exhibit991.htm)、[2025 Q3 更新](https://www.sec.gov/Archives/edgar/data/1318605/000162828025045861/exhibit991.htm)、[2026 Q2 財報會議整理](https://notateslaapp.com/news/4481/summary-of-teslas-2026-q2-earnings-call-cybercab-fsd-ai4-and-more)
- 演講整理與報導：[Humanoids Daily](https://www.humanoidsdaily.com/news/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus)、[NextBigFuture](https://www.nextbigfuture.com/2025/10/tesla-vp-ashok-describes-technology-of-fsd.html)、[OFweek（CVPR 2026 全文詳解）](https://www.ofweek.com/auto/2026-06/ART-70109-8110-30689565.html)、[Business Insider（Optimus 訓練改變）](https://www.aol.com/tesla-shifted-optimus-training-strategy-092502010.html)、[TechCrunch（Dojo）](https://techcrunch.com/2025/09/02/tesla-dojo-the-rise-and-fall-of-elon-musks-ai-supercomputer/)
