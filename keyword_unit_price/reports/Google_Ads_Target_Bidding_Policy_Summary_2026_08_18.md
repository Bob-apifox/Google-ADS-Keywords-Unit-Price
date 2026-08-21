# 📘 Google Ads Target-based Bidding Update 机制升级解读与归档报告

> **文档来源**: `Google Ads Target-based Bidding Update Client Guide.pdf`  
> **文档链接**: https://drive.weixin.qq.com/s?k=AOYARgdSAGAGIPtrjZ  
> **归档日期**: 2026-08-18  
> **整理人**: Apidog 增长黑客与数据分析团队  

---

## 一、 核心升级背景与机制变更 (Executive Summary)

Google Ads 官方针对以目标为导向的智能出价策略（**Target CPA** 与 **Target ROAS**）进行了底层竞价算法重大升级：

### 1. 从“死板单次限制”转向“周期全局收益最大化”
* **旧版算法痛点**：算法逐次严格限制每一次竞价出价。一旦某次竞价可能突破设定的 Target CPA 门槛，算法会直接收缩出价甚至放弃竞拍，导致高意向、高商业价值的用户流失，系列易触发 `Limited by bid strategy` 或流量断崖下滑。
* **升级后新机制**：算法改在 **7 - 14 天的滚动周期窗口**内做全局动态优化。针对**超高转化概率（High Conversion Probability）的优质开发者**，算法被赋予更高的弹性——**允许单次出价突破 tCPA 门槛**去抢占高价值转化，只要整个周期的平均 CPA 保持在设定目标以内。

---

## 二、 官方给广告主的核心指导原则 (Best Practices)

### 1. 避免频密改动（遵守 5-7 天冷凝期）
* 智能出价算法升级后依赖完整的模型学习。**切忌因为 1-2 天的单价短期波动频繁修改 Target CPA**。
* 频繁改动会导致算法不断重置学习期（Learning Phase），打断全局动态寻优逻辑。

### 2. 预算与 tCPA 保持充沛比例 (Budget-to-tCPA Ratio)
* 为保证新算法拥有足够的弹性竞价空间，官方建议**日预算（Daily Budget）保持为 Target CPA 的 10 - 15 倍以上**。
* 预算过窄（如日预算仅为 tCPA 的 2-3 倍）会导致算法束手脚，失去高价抢优质流量的能力。

### 3. 考虑转化归因延迟 (Conversion Lag)
* 开发者工具类产品用户从点击广告到完成注册/激活存在 1-3 天的时滞（Conversion Lag）。评估智能出价效果应看 **7 天或 14 天的滚动均值**，忽略最近 2-3 天未完全归因的即时数据。

---

## 三、 对 Apidog 当前账户的实操指导与落地应用

| 广告系列类别 | Apidog 代表 Campaign | 日预算 / tCPA 设定 | 新政策适应度与实操动作 |
| :--- | :--- | :--- | :--- |
| **旗舰印钞系列** | `Google-Sa-CP-Global` | 日预算 $200.00 / 均价 $2.50 | 预算为单价 80 倍，**极完美适配新算法**！允许算法弹性高价抢占高端开发者。 |
| **放量黑马系列** | `Google-Sa-Expansion-Horizon-2026` | 日预算 $60.00 / 均价 $3.70 | 预算空间充沛（16 倍），适合放量。保持策略稳定。 |
| **展示双轨系列** | `Google-Dis-DevPlacements-Global` | 日预算 $15.00 / tCPA $3.00 | 预算为 tCPA 5 倍，给予算法低频高质出价空间。 |
| **展示再营销系列** | `Google-Dis-Remarketing-Global` | 日预算 $10.00 / tCPA $2.50 | 维持 3 天断舍离通牒，观察滚动 7 天 CPA 均值。 |

---

## 四、 结论与团队工作要求

1. **已妥善归档**：本解读已存档至 `keyword_unit_price/reports/Google_Ads_Target_Bidding_Policy_Summary_2026_08_18.md`。
2. **执行铁律**：已生效的 `CP-Global`（$200/天）、`DevPlacements`（$15/天）、`Remarketing`（$10/天）智能出价策略，**保持 5-7 天无调价观察期**，充分利用 Google 升级后的弹性算法捕获高意向流量！

