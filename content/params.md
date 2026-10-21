# 參數量總表

<p class="lede">把這個網站、專案研究筆記與三份簡報裡出現過的 VLA 與世界模型，逐一回到論文、官方頁或官方模型卡核對參數量。<b>只寫官方明寫的數字；官方沒說的一律標「未公開」，不推測、不引用第三方估算。</b>其他每一章的最後也會自動列出「本頁提到的模型參數量」，資料都來自這張表。</p>

!!! key "重點先讀"
    1. **量產級 VLA 集中在 2B–5B**：π0 約 3.3B、GR00T N1 約 2.2B、GR00T N1.5／N1.6 3B、GR-3 約 4B、π\*0.6 是 Gemma 3 4B 加 860M 動作專家。早期的 RT-2（55B）、PaLM-E（562B）太大，跑不動即時控制。
    2. **真正在高頻迴圈裡跑的「快系統」都很小**：Helix S1 80M（200 Hz）、Figure Helix 02 的 S0 只有 10M（1 kHz）、1X Redwood 160M。大模型負責理解，小模型負責動。
    3. **世界模型從 19M 到 14B 都有**：放進推論迴圈的通常是 2B 以下（Cosmos Policy 2B、V-JEPA 2-AC 預測器 300M、VLA-RFT 138M）；當資料工廠或考官的則用大的（WAN2.1 14B、Cosmos 14B、1X 14B）。
    4. **最強的那幾個都沒公開**：Gemini Robotics、Veo、Genie 3、Sora、Tesla、理想 MindVLA、智平方 GOVLA 1.0 都查不到官方數字。
    5. **注意「總數」與「組成」**：很多論文只寫骨幹大小（例如 π0.5 只寫 VLM 2B 與動作專家 300M，沒寫總數）。表中照原文寫組成，不自己加總；少數由原文數字相加的會註明。

<figure class="dg">
<svg viewBox="0 0 800 300" role="img" aria-label="VLA 與世界模型參數量的對數刻度分布">
<rect class="n band" x="10" y="10" width="780" height="280" rx="14"/>
<line x1="60" y1="40" x2="60" y2="280" class="ar dash" style="marker-end:none;opacity:.35"/><text x="60" y="32" text-anchor="middle" class="s">10M</text>
<line x1="206" y1="40" x2="206" y2="280" class="ar dash" style="marker-end:none;opacity:.35"/><text x="206" y="32" text-anchor="middle" class="s">100M</text>
<line x1="352" y1="40" x2="352" y2="280" class="ar dash" style="marker-end:none;opacity:.35"/><text x="352" y="32" text-anchor="middle" class="s">1B</text>
<line x1="498" y1="40" x2="498" y2="280" class="ar dash" style="marker-end:none;opacity:.35"/><text x="498" y="32" text-anchor="middle" class="s">10B</text>
<line x1="643" y1="40" x2="643" y2="280" class="ar dash" style="marker-end:none;opacity:.35"/><text x="643" y="32" text-anchor="middle" class="s">100B</text>
<text x="20" y="80" class="h vla">VLA</text><text x="20" y="232" class="h wm">WM</text>
<line x1="40" y1="150" x2="780" y2="150" class="ar"/>
<circle cx="60" cy="143" r="5" class="n vla"/><line x1="60" y1="138" x2="60" y2="132" class="ar vla" style="marker-end:none"/><text x="60" y="128" text-anchor="middle" class="s vla">S0</text>
<circle cx="123" cy="143" r="5" class="n vla"/><line x1="123" y1="138" x2="123" y2="108" class="ar vla" style="marker-end:none"/><text x="123" y="104" text-anchor="middle" class="s vla">Octo-S</text>
<circle cx="192" cy="143" r="5" class="n vla"/><line x1="192" y1="138" x2="192" y2="84" class="ar vla" style="marker-end:none"/><text x="192" y="80" text-anchor="middle" class="s vla">Helix S1</text>
<circle cx="236" cy="143" r="5" class="n vla"/><line x1="236" y1="138" x2="236" y2="132" class="ar vla" style="marker-end:none"/><text x="236" y="128" text-anchor="middle" class="s vla">Redwood</text>
<circle cx="301" cy="143" r="5" class="n vla"/><line x1="301" y1="138" x2="301" y2="108" class="ar vla" style="marker-end:none"/><text x="301" y="104" text-anchor="middle" class="s vla">SmolVLA</text>
<circle cx="402" cy="143" r="5" class="n vla"/><line x1="402" y1="138" x2="402" y2="84" class="ar vla" style="marker-end:none"/><text x="402" y="80" text-anchor="middle" class="s vla">GR00T N1</text>
<circle cx="427" cy="143" r="5" class="n vla"/><line x1="427" y1="138" x2="427" y2="132" class="ar vla" style="marker-end:none"/><text x="427" y="128" text-anchor="middle" class="s vla">π0</text>
<circle cx="439" cy="143" r="5" class="n vla"/><line x1="439" y1="138" x2="439" y2="108" class="ar vla" style="marker-end:none"/><text x="439" y="104" text-anchor="middle" class="s vla">GR-3</text>
<circle cx="475" cy="143" r="5" class="n vla"/><line x1="475" y1="138" x2="475" y2="84" class="ar vla" style="marker-end:none"/><text x="475" y="80" text-anchor="middle" class="s vla">OpenVLA</text>
<circle cx="605" cy="143" r="5" class="n vla"/><line x1="605" y1="138" x2="605" y2="132" class="ar vla" style="marker-end:none"/><text x="605" y="128" text-anchor="middle" class="s vla">RT-2</text>
<circle cx="753" cy="143" r="5" class="n vla"/><line x1="753" y1="138" x2="753" y2="108" class="ar vla" style="marker-end:none"/><text x="753" y="104" text-anchor="middle" class="s vla">PaLM-E</text>
<circle cx="101" cy="157" r="5" class="n wm"/><line x1="101" y1="162" x2="101" y2="167" class="ar wm" style="marker-end:none"/><text x="101" y="180" text-anchor="middle" class="s wm">DINO-WM</text>
<circle cx="226" cy="157" r="5" class="n wm"/><line x1="226" y1="162" x2="226" y2="191" class="ar wm" style="marker-end:none"/><text x="226" y="204" text-anchor="middle" class="s wm">VLA-RFT</text>
<circle cx="275" cy="157" r="5" class="n wm"/><line x1="275" y1="162" x2="275" y2="215" class="ar wm" style="marker-end:none"/><text x="275" y="228" text-anchor="middle" class="s wm">V-JEPA 2-AC</text>
<circle cx="308" cy="157" r="5" class="n wm"/><line x1="308" y1="162" x2="308" y2="239" class="ar wm" style="marker-end:none"/><text x="308" y="252" text-anchor="middle" class="s wm">comma</text>
<circle cx="377" cy="157" r="5" class="n wm"/><line x1="377" y1="162" x2="377" y2="167" class="ar wm" style="marker-end:none"/><text x="373" y="180" text-anchor="end" class="s wm">SVD</text>
<circle cx="396" cy="157" r="5" class="n wm"/><line x1="396" y1="162" x2="396" y2="191" class="ar wm" style="marker-end:none"/><text x="396" y="204" text-anchor="middle" class="s wm">Dreamer 4</text>
<circle cx="486" cy="157" r="5" class="n wm"/><line x1="486" y1="162" x2="486" y2="239" class="ar wm" style="marker-end:none"/><text x="482" y="252" text-anchor="end" class="s wm">GAIA-2</text>
<circle cx="504" cy="157" r="5" class="n wm"/><line x1="504" y1="162" x2="504" y2="215" class="ar wm" style="marker-end:none"/><text x="508" y="228" text-anchor="start" class="s wm">Genie</text>
<circle cx="519" cy="157" r="5" class="n wm"/><line x1="519" y1="162" x2="519" y2="167" class="ar wm" style="marker-end:none"/><text x="523" y="180" text-anchor="start" class="s wm">Cosmos／1X</text>
</svg>
<figcaption>對數刻度：每一格差 10 倍。上排 VLA、下排世界模型，只畫官方公布數字的代表；Gemini Robotics、Veo、Genie 3、Sora、Tesla 等未公開的不在圖上。</figcaption></figure>

{{PARAMS_TABLES}}

## 怎麼核對的

- **優先順序**：論文正文或附錄 → 官方專案頁、部落格 → 官方模型卡（Hugging Face 上的官方帳號）→ 官方發布會原話的報導。
- **媒體報導只在官方完全沒寫時列出，並明寫是媒體說法**：目前只有 π0.7（[The Decoder](https://the-decoder.com/physical-intelligence-shows-robot-model-with-llm-like-generalization-flaws-included/) 報導 Gemma 3 4B + 860M，[官方頁](https://pi.website/blog/pi07)沒寫）。
- **論文前後不一致時照實寫**：π0.5 的圖寫 Gemma 2B 與 2.6B 兩種；UniVLA 的動作頭在引言寫 10.8M、正文寫 12.6M，表中取正文。
