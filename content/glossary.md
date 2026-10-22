# 名詞速查

<p class="lede">全站出現過的術語，一行說清楚是什麼，並指回詳細解說的章節。按主題分組，同組內大致依「先懂這個才懂下一個」排序。</p>

## 基本概念

| 名詞 | 一句話解釋 | 詳見 |
|---|---|---|
| **VLA**（Vision-Language-Action） | 看畫面、聽語言指令、直接輸出機器人動作的模型；2023 年 [RT-2](https://arxiv.org/abs/2307.15818) 正式提出這個詞 | [01](origins.html)、[02](vla-architectures.html) |
| **VLM**（Vision-Language Model） | 看圖讀文字、輸出文字的模型，是多數 VLA 的主幹 | [02](vla-architectures.html) |
| **世界模型**（World Model） | 給定「現在」與「動作」，預測「接下來會發生什麼」的模型 | [05](world-model-roles.html) |
| **具身基礎模型** | 同時具備理解、行動、預測後果三種能力的通用預訓練模型，業界也叫 Robot Foundation Model | [07](synthetic-data.html) |
| **World Foundation Model** | NVIDIA 對大型通用世界模型的稱呼，例如 Cosmos | [07](synthetic-data.html) |
| **策略**（Policy） | 從觀測到動作的映射；VLA 就是一種策略 | [04](training.html) |
| **具身智能**（Embodied AI） | 有身體、能在物理世界感知與行動的 AI | [01](origins.html) |

## VLA 架構

| 名詞 | 一句話解釋 | 詳見 |
|---|---|---|
| **單系統** | 一個模型同時理解與輸出動作，例如 RT-2、OpenVLA | [03](vla-taxonomy.html) |
| **雙系統**（快慢腦） | 慢系統（大 VLM，低頻）理解與推理，快系統（小模型，高頻）出動作，例如 GR00T N1、Helix | [03](vla-taxonomy.html) |
| **顯式分層** | 上層輸出人看得懂的中間計畫（子任務、關鍵點、軌跡），下層照著執行 | [03](vla-taxonomy.html) |
| **動作專家**（Action Expert） | 接在 VLM 後面、專門輸出連續動作的子網路，例如 π0 的 300M 模組 | [02](vla-architectures.html) |
| **Action Chunk** | 一次輸出未來多步動作（例如 50 步），降低推論頻率需求、讓動作更平滑 | [04](training.html) |
| **動作離散化／動作 token** | 把連續動作切成格子變成 token，讓語言模型像出字一樣出動作 | [02](vla-architectures.html) |
| **FAST** | 用 DCT 壓縮動作序列再 token 化，讓自迴歸 VLA 也能做高頻精細動作（[arXiv:2501.09747](https://arxiv.org/abs/2501.09747)） | [02](vla-architectures.html) |
| **Diffusion Policy** | 用擴散模型從雜訊逐步去噪生成動作，能表達多模態動作分布 | [02](vla-architectures.html) |
| **Flow Matching** | 學一個把雜訊「流」到資料的向量場，比擴散步數少，π0、GR00T 用它出動作 | [02](vla-architectures.html) |
| **Knowledge Insulation** | 阻斷動作損失的梯度回流 VLM 主幹，避免動作訓練破壞語言知識 | [08](industry.html) |
| **Latent Action** | 從無標註影片學出的抽象「動作」表示，可用來給網路影片補動作標籤 | [04](training.html) |
| **IDM**（逆動力學模型） | 看前後兩幀，推回中間做了什麼動作；合成資料流程的關鍵 | [05](world-model-roles.html) |
| **Embodied CoT** | 出動作前先輸出推理文字、子任務或視覺預測，例如 CoT-VLA | [06](train-vs-inference.html) |
| **情境內模仿學習**（In-Context Imitation Learning, ICIL） | 把幾條示範放進模型輸入當提示，模型不更新權重就照著做新任務，例如 ICRT、Instant Policy、RICL | [05](in-context-imitation.html) |

## 世界模型

| 名詞 | 一句話解釋 | 詳見 |
|---|---|---|
| **影片生成式** | 輸出未來畫面，例如 Cosmos、Genie 3；最適合當模擬器與資料工廠 | [05](world-model-roles.html) |
| **潛空間動力學** | 在壓縮的潛狀態裡預測下一步，例如 Dreamer、TD-MPC2；適合想像中 RL | [05](world-model-roles.html) |
| **RSSM** | Dreamer 系列的循環狀態空間模型，同時有確定與隨機的潛狀態 | [02](wm-architectures.html) |
| **JEPA** | LeCun 提出的聯合嵌入預測架構，只在表徵空間預測，不生成像素 | [05](world-model-roles.html) |
| **3D／4D 世界模型** | 預測 3D 場景或未來佔據（occupancy），例如 OccWorld | [05](world-model-roles.html) |
| **Action-conditioned** | 預測未來時把「要做的動作」當條件輸入，才能拿來規劃或評估 | [05](world-model-roles.html) |
| **想像中訓練**（Learning in Imagination） | 策略在世界模型產生的軌跡裡練習，不碰真實環境 | [05](world-model-roles.html) |
| **MPC**（模型預測控制） | 用模型模擬多個候選動作序列，挑最好的執行第一步，再重新規劃 | [04](training.html) |
| **CEM**（交叉熵法） | MPC 常用的取樣最佳化：反覆取樣、留下最好的一批、更新分布 | [04](training.html) |
| **Compounding Error** | 模型多步展開時誤差越滾越大 | [01](origins.html) |
| **Model Exploitation** | 策略學會鑽世界模型的錯誤拿高分，在真實世界卻失敗 | [07](synthetic-data.html) |

## 訓練與資料

| 名詞 | 一句話解釋 | 詳見 |
|---|---|---|
| **模仿學習／行為克隆**（IL／BC） | 拿人類示範當標準答案，學「看到這個就做那個」 | [04](training.html) |
| **遙操作**（Teleoperation） | 人用搖桿、VR 或主從手臂操控機器人收示範資料 | [04](training.html) |
| **資料金字塔** | 底層網路影片、中層模擬與合成、頂層真機資料的混合配方 | [04](training.html) |
| **跨機型**（Cross-embodiment） | 用多種不同機器人的資料訓練同一個模型 | [04](training.html) |
| **Sim2Real Gap** | 模擬器與真實世界的物理、視覺差異 | [07](synthetic-data.html) |
| **Domain Randomization** | 在模擬中隨機改顏色、光線、物理參數，讓策略對差異更穩健 | [01](origins.html) |
| **後訓練**（Post-training） | 預訓練之後用少量高品質資料或 RL 微調到特定任務 | [04](training.html) |
| **離線 RL** | 只用已收集的資料做強化學習，不在線上試錯；π\*0.6 Recap 用它 | [08](industry.html) |
| **蒸餾**（Distillation） | 用大模型（教師）的輸出訓練小模型（學生），把雲端能力搬到端側 | [08](industry.html) |

## 評測

| 名詞 | 一句話解釋 | 詳見 |
|---|---|---|
| **開環評估** | 拿資料集算預測誤差，不讓模型真的行動；和真實表現相關性常常不高 | [04](training.html) |
| **閉環評估** | 讓策略真的在模擬器、世界模型或真機上執行，看最後成不成功 | [04](training.html) |
| **LIBERO／CALVIN／SimplerEnv** | 常用的機器人操作模擬基準 | [04](training.html) |
| **FVD** | 衡量生成影片與真實影片分布差距的指標，越低越好 | [04](training.html) |
| **Physics-IQ** | 測影片模型物理理解的基準，發現逼真度與物理正確幾乎無關 | [07](synthetic-data.html) |

## 本站自訂的分類代號

| 代號 | 意思 | 詳見 |
|---|---|---|
| **T1–T4** | 世界模型在**訓練時**的四種用法：預訓練／輔助、資料工廠、想像中 RL、評估器 | [06](train-vs-inference.html) |
| **I0–I3** | 世界模型在**推論時**的四個等級：不用、部分一步特徵、先想再做、候選搜尋 | [06](train-vs-inference.html) |
| **五種角色** | 資料引擎、輔助預測、想像中 RL、先想再做、評測模擬器 | [05](world-model-roles.html) |
| **五種整合模式** | 資料工廠、閉環評估器、RL 訓練場、預訓練再接動作頭、WM 即為策略 | [08](industry.html) |
