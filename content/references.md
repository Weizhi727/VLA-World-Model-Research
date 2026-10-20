# 參考資料

<p class="lede">全站引用過的論文、官方頁面與報導，依主題分組。每一條都是原始出處的超連結；各章節內文也在引用處直接附上連結。</p>

!!! note "來源可靠度"
    論文與技術報告優先；只有官方部落格、發表會或媒體報導的項目，在〈[業界產品盤點](industry.html)〉以 🎤 標記，代表沒有可重現的細節。數字（資料量、參數量）取自各論文摘要或正文，引用前建議對照原文。

## 綜述與分類依據

- [Pure Vision Language Action (VLA) Models: A Comprehensive Survey（arXiv:2509.19012）](https://arxiv.org/abs/2509.19012)
- [VLA 系統架構綜述：單系統、雙系統、分層（arXiv:2508.13073）](https://arxiv.org/abs/2508.13073)
- [A Survey on VLA Models: An Action Tokenization Perspective（arXiv:2507.01925）](https://arxiv.org/abs/2507.01925)
- [A Comprehensive Survey on World Models for Embodied AI（arXiv:2510.16732）](https://arxiv.org/abs/2510.16732)
- [Understanding World or Predicting Future?（arXiv:2411.14499）](https://arxiv.org/abs/2411.14499)

## VLA 之前：機器人學習的前史

- [End-to-End Visuomotor Policies（arXiv:1504.00702）](https://arxiv.org/abs/1504.00702)
- [Domain Randomization（arXiv:1703.06907）](https://arxiv.org/abs/1703.06907)
- [R2R 視覺語言導航（arXiv:1711.07280）](https://arxiv.org/abs/1711.07280)
- [QT-Opt（arXiv:1806.10293）](https://arxiv.org/abs/1806.10293)
- [CLIP（arXiv:2103.00020）](https://arxiv.org/abs/2103.00020)
- [CLIPort（arXiv:2109.12098）](https://arxiv.org/abs/2109.12098)
- [SayCan（arXiv:2204.01691）](https://arxiv.org/abs/2204.01691)
- [Gato（arXiv:2205.06175）](https://arxiv.org/abs/2205.06175)
- [Inner Monologue（arXiv:2207.05608）](https://arxiv.org/abs/2207.05608)
- [Code as Policies（arXiv:2209.07753）](https://arxiv.org/abs/2209.07753)
- [VIMA（arXiv:2210.03094）](https://arxiv.org/abs/2210.03094)
- [PaLM-E（arXiv:2303.03378）](https://arxiv.org/abs/2303.03378)

## VLA 主要模型

### 離散 token 與單系統

- [RT-1（arXiv:2212.06817）](https://arxiv.org/abs/2212.06817)
- [RT-2（arXiv:2307.15818）](https://arxiv.org/abs/2307.15818)
- [Octo（arXiv:2405.12213）](https://arxiv.org/abs/2405.12213)
- [OpenVLA（arXiv:2406.09246）](https://arxiv.org/abs/2406.09246)
- [OpenVLA-OFT（arXiv:2502.19645）](https://arxiv.org/abs/2502.19645)
- [FAST tokenizer／π0-FAST（arXiv:2501.09747）](https://arxiv.org/abs/2501.09747)
- [RoboMamba（arXiv:2406.04339）](https://arxiv.org/abs/2406.04339)
- [SmolVLA（arXiv:2506.01844）](https://arxiv.org/abs/2506.01844)

### 連續動作：擴散與 flow matching

- [Diffusion Policy（arXiv:2303.04137）](https://arxiv.org/abs/2303.04137)
- [ACT／ALOHA（arXiv:2304.13705）](https://arxiv.org/abs/2304.13705)
- [π0（arXiv:2410.24164）](https://arxiv.org/abs/2410.24164)
- [π0.5（arXiv:2504.16054）](https://arxiv.org/abs/2504.16054)
- [Knowledge Insulation（arXiv:2505.23705）](https://arxiv.org/abs/2505.23705)
- [RDT-1B（arXiv:2410.07864）](https://arxiv.org/abs/2410.07864)
- [CogACT（arXiv:2411.19650）](https://arxiv.org/abs/2411.19650)
- [HybridVLA（arXiv:2503.10631）](https://arxiv.org/abs/2503.10631)
- [openpi 程式碼](https://github.com/Physical-Intelligence/openpi)｜[LeRobot](https://github.com/huggingface/lerobot)

### 雙系統、分層與中間表徵

- [GR00T N1（arXiv:2503.14734）](https://arxiv.org/abs/2503.14734)｜[Isaac-GR00T GitHub](https://github.com/NVIDIA/Isaac-GR00T)
- [Figure Helix 官方部落格](https://www.figure.ai/news/helix)
- [Gemini Robotics（arXiv:2503.20020）](https://arxiv.org/abs/2503.20020)
- [Gemini Robotics 1.5（arXiv:2510.03342）](https://arxiv.org/abs/2510.03342)
- [Gemini Robotics 2 部落格](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)
- [Hi Robot（arXiv:2502.19417）](https://arxiv.org/abs/2502.19417)
- [AgiBot World／GO-1（arXiv:2503.06669）](https://arxiv.org/abs/2503.06669)
- [FiS-VLA（arXiv:2506.01953）](https://arxiv.org/abs/2506.01953)
- [Video2Act（arXiv:2512.03044）](https://arxiv.org/abs/2512.03044)
- [NeuroVLA（arXiv:2601.14628）](https://arxiv.org/abs/2601.14628)
- [SaiVLA-0（arXiv:2603.08124）](https://arxiv.org/html/2603.08124)
- [CereVLA（arXiv:2609.27468）](https://arxiv.org/abs/2609.27468)
- [HAMSTER（arXiv:2502.05485）](https://arxiv.org/abs/2502.05485)
- [RoboPoint（arXiv:2406.10721）](https://arxiv.org/abs/2406.10721)
- [LAPA（arXiv:2410.11758）](https://arxiv.org/abs/2410.11758)
- [UniVLA（arXiv:2505.06111）](https://arxiv.org/abs/2505.06111)

## 世界模型

### 經典與潛空間路線

- [World Models（arXiv:1803.10122）](https://arxiv.org/abs/1803.10122)｜[互動版](https://worldmodels.github.io/)
- [PlaNet（arXiv:1811.04551）](https://arxiv.org/abs/1811.04551)
- [SimPLe（arXiv:1903.00374）](https://arxiv.org/abs/1903.00374)
- [MuZero（arXiv:1911.08265）](https://arxiv.org/abs/1911.08265)
- [Dreamer（arXiv:1912.01603）](https://arxiv.org/abs/1912.01603)
- [DreamerV2（arXiv:2010.02193）](https://arxiv.org/abs/2010.02193)
- [DreamerV3（arXiv:2301.04104）](https://arxiv.org/abs/2301.04104)
- [Dreamer 4（arXiv:2509.24527）](https://arxiv.org/abs/2509.24527)
- [IRIS（arXiv:2209.00588）](https://arxiv.org/abs/2209.00588)
- [TD-MPC2（arXiv:2310.16828）](https://arxiv.org/abs/2310.16828)
- [DINO-WM（arXiv:2411.04983）](https://arxiv.org/abs/2411.04983)

### JEPA 表徵預測

- [V-JEPA（arXiv:2404.08471）](https://arxiv.org/abs/2404.08471)
- [V-JEPA 2／V-JEPA 2-AC（arXiv:2506.09985）](https://arxiv.org/abs/2506.09985)

### 影片生成與互動世界

- [UniSim（arXiv:2310.06114）](https://arxiv.org/abs/2310.06114)
- [Genie 1（arXiv:2402.15391）](https://arxiv.org/abs/2402.15391)
- [Genie 3 部落格](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)
- [DIAMOND（arXiv:2405.12399）](https://arxiv.org/abs/2405.12399)
- [GameNGen（arXiv:2408.14837）](https://arxiv.org/abs/2408.14837)
- [Diffusion Forcing（arXiv:2407.01392）](https://arxiv.org/abs/2407.01392)
- [Self Forcing（arXiv:2506.08009）](https://arxiv.org/abs/2506.08009)
- [NVIDIA Cosmos（arXiv:2501.03575）](https://arxiv.org/abs/2501.03575)
- [Cosmos-Transfer1（arXiv:2503.14492）](https://arxiv.org/abs/2503.14492)
- [Cosmos-Reason1（arXiv:2503.15558）](https://arxiv.org/abs/2503.15558)
- [Cosmos-Predict2.5（arXiv:2511.00062）](https://arxiv.org/abs/2511.00062)
- [HunyuanVideo（arXiv:2412.03603）](https://arxiv.org/abs/2412.03603)
- [Genie Envisioner（arXiv:2508.05635）](https://arxiv.org/abs/2508.05635)
- [Ctrl-World（arXiv:2510.10125）](https://arxiv.org/abs/2510.10125)

### 自駕與 3D／4D

- [GAIA-1（arXiv:2309.17080）](https://arxiv.org/abs/2309.17080)
- [GAIA-2（arXiv:2503.20523）](https://arxiv.org/abs/2503.20523)
- [OccWorld（arXiv:2311.16038）](https://arxiv.org/abs/2311.16038)
- [DriveVLM（arXiv:2402.12289）](https://arxiv.org/abs/2402.12289)
- [EMMA（arXiv:2410.23262）](https://arxiv.org/abs/2410.23262)
- [Alpamayo-R1（arXiv:2511.00088）](https://arxiv.org/abs/2511.00088)
- [Learning to Drive from a World Model（arXiv:2504.19077）](https://arxiv.org/abs/2504.19077)｜[openpilot](https://github.com/commaai/openpilot)

## 世界模型 × VLA 的結合

- [UniPi（arXiv:2302.00111）](https://arxiv.org/abs/2302.00111)：先生成影片再反推動作
- [GR-1（arXiv:2312.13139）](https://arxiv.org/abs/2312.13139)、[GR-2（arXiv:2410.06158）](https://arxiv.org/abs/2410.06158)、[GR-3（arXiv:2507.15493）](https://arxiv.org/abs/2507.15493)：影片預測預訓練
- [VPP（arXiv:2412.14803）](https://arxiv.org/abs/2412.14803)、[Seer（arXiv:2412.15109）](https://arxiv.org/abs/2412.15109)、[UVA（arXiv:2503.00200）](https://arxiv.org/abs/2503.00200)：預測式 VLA
- [CoT-VLA（arXiv:2503.22020）](https://arxiv.org/abs/2503.22020)、[WorldVLA（arXiv:2506.21539）](https://arxiv.org/abs/2506.21539)、[DreamVLA（arXiv:2507.04447）](https://arxiv.org/abs/2507.04447)、[FLARE（arXiv:2505.15659）](https://arxiv.org/abs/2505.15659)
- [DreamGen（arXiv:2505.12705）](https://arxiv.org/abs/2505.12705)：世界模型當資料工廠
- [WMPO（arXiv:2511.09515）](https://arxiv.org/abs/2511.09515)、[VLA-RFT（arXiv:2510.00406）](https://arxiv.org/abs/2510.00406)：想像中強化學習
- [VLA-Reasoner（arXiv:2509.22643）](https://arxiv.org/abs/2509.22643)、[FOREWARN（arXiv:2502.01828）](https://arxiv.org/abs/2502.01828)、[Cosmos Policy（arXiv:2601.16163）](https://arxiv.org/abs/2601.16163)、[τ0-VLA（arXiv:2608.16885）](https://arxiv.org/abs/2608.16885)：推論時候選搜尋
- [Veo 當策略評測模擬器（arXiv:2512.10675）](https://arxiv.org/abs/2512.10675)
- [MimicGen（arXiv:2310.17596）](https://arxiv.org/abs/2310.17596)：模擬中擴增示範

## 資料集、基準與評測

- [Open X-Embodiment／RT-X（arXiv:2310.08864）](https://arxiv.org/abs/2310.08864)
- [DROID（arXiv:2403.12945）](https://arxiv.org/abs/2403.12945)
- [BridgeData V2（arXiv:2308.12952）](https://arxiv.org/abs/2308.12952)
- [RLDS（arXiv:2111.02767）](https://arxiv.org/abs/2111.02767)
- [UMI（arXiv:2402.10329）](https://arxiv.org/abs/2402.10329)
- [Ego4D（arXiv:2110.07058）](https://arxiv.org/abs/2110.07058)
- [LIBERO（arXiv:2306.03310）](https://arxiv.org/abs/2306.03310)
- [CALVIN（arXiv:2112.03227）](https://arxiv.org/abs/2112.03227)
- [SimplerEnv（arXiv:2405.05941）](https://arxiv.org/abs/2405.05941)
- [RoboCasa（arXiv:2406.02523）](https://arxiv.org/abs/2406.02523)
- [TRI Large Behavior Models（arXiv:2507.05331）](https://arxiv.org/abs/2507.05331)
- [FVD（arXiv:1812.01717）](https://arxiv.org/abs/1812.01717)
- [VBench（arXiv:2311.17982）](https://arxiv.org/abs/2311.17982)
- [Physics-IQ（arXiv:2501.09038）](https://arxiv.org/abs/2501.09038)
- [How Far is Video Generation from World Model（arXiv:2411.02385）](https://arxiv.org/abs/2411.02385)
- [VideoPhy（arXiv:2406.03520）](https://arxiv.org/abs/2406.03520)
- [PhyGenBench（arXiv:2410.05363）](https://arxiv.org/abs/2410.05363)

## 業界官方頁面與報導

- [Physical Intelligence 研究頁](https://www.physicalintelligence.company/research)
- [NVIDIA CES 2026 物理 AI 新聞稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Releases-New-Physical-AI-Models-as-Global-Partners-Unveil-Next-Generation-Robots/default.aspx)
- [NVIDIA Alpamayo 新聞稿](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Alpamayo-Family-of-Open-Source-AI-Models-and-Tools-to-Accelerate-Safe-Reasoning-Based-Autonomous-Vehicle-Development/)
- [1X Redwood AI／World Model](https://www.1x.tech/discover/redwood-ai-world-model)
- [Unitree UnifoLM-WMA-0](https://github.com/unitreerobotics/unifolm-world-model-action)
- [Wayve LINGO-2](https://wayve.ai/thinking/lingo-2-driving-with-language/)
- [Tesla 世界模擬器演講整理](https://www.humanoidsdaily.com/feed/tesla-ai-chief-details-unified-world-simulator-for-fsd-and-optimus)
- [Waymo World Model 報導](https://the-decoder.com/waymo-taps-google-deepminds-genie-3-to-simulate-driving-scenarios-its-cars-have-never-seen/)
- [36Kr 中國車廠技術路線整理](https://www.36kr.com/p/3463098292770179)
- [智平方 AlphaBot 2／GOVLA 發布頁](https://ai2robotics.com/en/%E6%99%BA%E5%B9%B3%E6%96%B9%E5%8F%91%E5%B8%83%E5%85%A8%E6%96%B0%E4%B8%80%E4%BB%A3%E6%99%BA%E8%83%BD%E6%9C%BA%E5%99%A8%E4%BA%BAalphabot-2%E5%BC%80%E5%90%AFagi%E7%BB%88%E7%AB%AF%E6%96%B0/)
- [The Robot Report：智平方 B 輪](https://www.therobotreport.com/ai2-robotics-raises-series-b-funding-advance-alphabot-embodied-ai/)
- [果蠅全腦模型（Nature 2024）](https://www.nature.com/articles/s41586-024-07763-9)

## 本專案的原始產出 {#project-outputs}

這個網站整理自專案內先前的報告與簡報。以下連結是 claude.ai 上的私人頁面，**需要登入、且有權限的帳號才能開啟**。

| 產出 | 內容 | 對應章節 |
|---|---|---|
| [起源與歷史報告](https://claude.ai/code/artifact/5c119e30-7c97-4bec-bb9e-b7a2628d3995) | 兩條路線的瓶頸、里程碑、匯流；具身基礎模型與合成資料追問 | 01、07 |
| [主流模型架構報告](https://claude.ai/artifact/8VrHVsBejHtCYZm1aJEDsT) | VLA 四路線、世界模型四路線 | 02 |
| [訓練與評估手冊](https://claude.ai/artifact/VBZAwSnrQMFA4q5zeze5bR) | 訓練流程、資料、I/O、評估 | 04 |
| [工程師課件簡報](https://claude.ai/artifact/J5M7pfkUDBvDbspadVYUop) | 72 頁，模型架構與結果 | 02、04 |
| [非技術版簡報](https://claude.ai/artifact/FjNw2SX9ALNwFMG7hbmz1m) | 32 頁，給非工程背景讀者 | 首頁 |
| [世界模型種類簡報](https://claude.ai/artifact/XasR8g8FD5Saj3dBfrd5jk) | 四類世界模型、五種角色 | 05 |

專案共享資料夾內的調研筆記（流派分類、訓練時 vs 推論時、業界產品、智平方）分別對應第 03、06、08、09 章。
