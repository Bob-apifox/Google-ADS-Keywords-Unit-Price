# 🚀 Google Ads 执行方案 (2026-08-07 专属复盘与拓量)

> **基于 8 月 6 日大盘数据生成** 
> *总消耗: $1,569.31 | 总注册: 416 | 均价 CPA: $3.77*

---

## 1. 🛑 止损与惩罚计划 (Optimization & Penalization)

针对昨日 CPA 严重超标以及出现空耗的广告组，需立即进行否定词清洗和出价抑制。

*   **动作 1：削减预算与下调出价 (Budget & tCPA Reduction)**
    *   **`Google-Sa-Insomnia-Global`** (CPA 极高: $47.28)：日预算下调 **40%**，tCPA 进一步下调。
    *   **`Google-Sa-CLI-Terminal-Global`** (CPA 极高: $33.99)：日预算下调 **30%**。
    *   **`Google-Sa-Func-MultiProtocol-Global`** (CPA 极高: $29.82)：日预算下调 **30%**。
    *   **`Google-Sa-Stoplight-Global`** (CPA: $16.60)：日预算下调 **20%**。
    *   **`Google-PMax-Postman`** (CPA偏高: $6.93)：当前无 tCPA 限制导致跑偏。**建议立即设定 tCPA（约 $4.00 - $4.50）**作为紧箍咒，限制算法在低效展示版位上挥霍预算。

*   **动作 2：基于真实报表精准否词 (Data-Driven Negative Keywords)**
    *   **`Google-Sa-Insomnia-Global`**：被应用开发类流量疯狂吸血。添加否词 (Phrase/Exact)：`pwa progressive web app`, `mobile app development`, `app js`, `insomnia api`, `v0 by vercel`, `glide apps`, `pwabuilder`。
    *   **`Google-Sa-CLI-Terminal-Global`**：跑偏到 Web 端竞品搜索。添加否词 (Phrase/Exact)：`online postman`, `postman online web`, `postman web`。
    *   **`Google-Sa-Func-MultiProtocol-Global`**：宽泛匹配吃掉预算。添加否词 (Phrase/Exact)：`websocket`, `download postman`, `postman desktop`, `dio websocket`, `websocket online`。
    *   **`Google-Sa-Stoplight-Global`**：无关建站与 AI 蹭量。添加否词 (Phrase/Exact)：`groupdocs`, `relume`, `v0 dev bolt new`, `anthropic console`, `web bluetooth api`, `web design software`。
    *   **`Google-Sa-Func-CICD-Global`** (0 转化)：被宽泛词吸血。添加否词 (Exact)：`github`。

---

## 2. 📈 乘胜追击：拓量计划 (Expansion Plan)

以下核心宽泛概念词展示出了极佳的性价比，潜力巨大，可以稳步放量：

*   **🔥 拓量方向 1：竞品拦截神词 (高曝光低 CPC)**
    *   `readyapi alternative` ($0.74 CPC)
    *   `hoppscotch` ($0.56 CPC)
    *   `postman alternative` ($0.81 CPC)
    *   **策略**：由于采用自动出价 (tCPA)，放量不能通过手动改 CPC 来实现。建议：**上调对应 Campaign 日预算 15%-20%**，并**微升 tCPA 目标值（约 5-10%）**，给机器释放更大的竞价空间，以便稳健吃下这批高性价比流量。

*   **🔥 拓量方向 2：MCP (Model Context Protocol) 前沿生态**
    *   `connect API to Cursor` ($0.58 CPC，在 `Google-Sa-MCP-Infrastructure` 跑出 202 个点击)
    *   **策略**：随着 AI IDE 的火热，这是一个极其精准的新增量点。建议在 MCP 广告系列里保持较高预算，单独为 "API to Cursor/Windsurf" 相关的搜索词建立独立的广告组。

*   **🔥 拓量方向 3：性能压测与年度盘点**
    *   `performance load testing` ($0.49 CPC)
    *   `top 10 API tools` ($0.48 CPC)
    *   **策略**：年底或盘点期 `top 10 API tools` 流量极大。建议为 Jmeter 压测系列 (`Google-Sa-Jmeter-Global`) 和 趋势系列 (`Google-Sa-Annual Planning & New Trends-26`) **微升 10% 预算** 探索这批温和流量。

*   **🔥 拓量方向 4：PMax 品牌与通用拉新 (高转化低 CPA)**
    *   **`Google-PMax-CP-Global`** (CPA 极低: $2.25)
    *   **策略**：该系列目前在最大化转化策略下表现极佳。建议**继续保持不设 tCPA 的状态**，并缓慢上调其日预算（10%-15%），让算法在低价区间继续畅快吃量。

---

## 3. ⚙️ 执行与追踪规范

1.  **否定词批量添加**：优先使用脚本或 Google Ads Editor 批量无误地将上述问题搜索词打入各 Campaign 的否定词库。
2.  **预算调整规范**：高 CPA 的“四大刺客”务必在今天中午前完成预算下调操作。
3.  **零转化小语种**：对于昨日有消耗但 0 转化的 `Google-Sa-CP-ESP` 和 `Google-Sa-CP-ID`，继续观察 2 天，若仍无转化则考虑暂停测试。
4.  **新 Group 搭建规范**：凡是涉及新建广告组（如 AI 细分词组、MCP 专属组等），**必须严格按照之前搭建规则配置**：撰写高相关性的专属广告创意（Ad Copy），并绑定带完整 UTM 参数（特别是 `utm_campaign` 和 `utm_term`）的着陆页，保证后续数据追踪不掉链子。
