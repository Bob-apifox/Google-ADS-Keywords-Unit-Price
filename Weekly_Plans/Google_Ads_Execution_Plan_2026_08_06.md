# 🚀 Google Ads 执行方案 (2026-08-06 专属复盘与拓量)

> **基于 8 月 5 日大盘数据生成** 
> *总消耗: $1,649.60 | 总注册: 437 | 均价 CPA: $3.77*

---

## 1. 🛑 止损与惩罚计划 (Optimization & Penalization)

针对昨日 CPA 飙高（>$10）的几个顽固消耗大户，我们需要继续施加系统级的惩罚与预算剥夺，将资金让给高转化组。

*   **动作 1：削减预算与下调出价 (Budget & tCPA Reduction)**
    *   **`Google-Sa-Stoplight-Global`** (CPA 极高: $33.17)：日预算下调 **30%**，tCPA 下调 **20%**。
    *   **`Google-Sa-Insomnia-Global`** (CPA 过高: $26.18)：日预算下调 **25%**，tCPA 下调 **15%**。
    *   **`Google-Sa-Solutions-API-First-Global`** (CPA: $15.29)：日预算下调 **20%**。
    *   **`Google-Sa-CLI-Terminal-Global`** (CPA: $11.59)：日预算下调 **20%**。

*   **动作 2：基于真实报表精准否词 (Data-Driven Negative Keywords)**
    *   通过最新脚本拉取出的过去 7 天高耗无转化废词，进行定点清除：
        *   **`Google-Sa-Stoplight-Global`**：大量无关 AI 工具和建站工具在蹭流量。添加否词 (Phrase/Exact)：`groupdocs`, `relume`, `v0 dev`, `bolt new`, `anthropic console`, `ollama api`, `open source`。
        *   **`Google-Sa-Insomnia-Global`**：被各种 App 开发和 PWA 工具流量疯狂吸血。添加否词 (Phrase/Exact)：`pwa progressive web app`, `mobile app development`, `openhands`, `glide apps`, `web app`。
        *   **`Google-Sa-Solutions-API-First-Global`**：屏蔽不相关的代码生成工具和竞品误导搜索。添加否词 (Exact)：`openapi generator`, `application programing`, `apifox english`。

*   **动作 3：高耗低转 Broad 词精准控制 (Match Type Restriction)**
    *   昨天跑出大量 Broad (广泛匹配) 点击但推高了所在组 CPA 的搜索词，建议收缩为 Exact (完全匹配) 进行保守投放：
        *   在 `Google-Sa-Testing-Global` 中：收紧 `[api security testing tool]` (昨日耗费 $294，占了全组绝大部分)。
        *   在 `Google-Sa-Func-MultiProtocol-Global` 中：收紧 `[test sse stream endpoint]` (昨日耗费 $214)。

---

## 2. 📈 乘胜追击：拓量计划 (Expansion Plan)

昨日部分赛道跑出了令人震惊的极低转化单价，证明了受众匹配极其精准，必须立刻追加筹码，进一步收割市场份额！

*   **🔥 黑马赛道 1：PMax 效果最大化广告 (极简暴利) ➡️ 【稳步放量】**
    *   **数据发现**：`Google-PMax-CP-Global` (CPA $1.83) 和 `Google-PMax-Postman` (CPA $1.56) 双双超神！作为黑盒模型，PMax 显然已经找到了高净值目标人群。
    *   **拓量动作**：这两个 PMax 广告系列的日预算 **上调 10%**，保持现有的出价策略不变，稳步释放流量以供观察。

*   **🔥 拓量赛道 2：DSA 竞品拦截专列 (Blog Alternatives) ➡️ 【独立建系列 + 一竞品一单组】**
    *   **数据发现**：我们拥有一批高质量的竞品拦截博客文章（如 Best Postman/Insomnia Alternative 等），这批 SEO 流量极具精准转化潜力。
    *   **拓量动作**：**新建独立的 DSA Campaign** (`Google-Sa-DSA-Alternatives-Global`)。采用**一竞品一单组**的精细化结构（共建 9 个 Ad Group）。每个 Group 绑定唯一对应的博客 URL，并针对性地撰写专属的“痛点拉踩”广告描述（例如在 Postman 组里写 "Tired of Postman pricing?"），以实现极高的广告相关性和点击率。

---

## 3. ⚙️ 执行与追踪规范

1.  **预算调整规范**：所有预算和 tCPA 下调需通过 API 脚本批量无误执行。
2.  **新组搭建规范**：新建的 VS Code 及 AI 衍生组必须完整配置 `apidog.com` 着陆页及 UTM (`utm_campaign`, `utm_term`)，以保证 Metabase 数据归因。
3.  **风险监控**：调整生效后，由于 PMax 预算猛增，需在明日此时密切关注大盘平均 CPA 是否被瞬间拉高（阈值警戒线：$4.50）。
