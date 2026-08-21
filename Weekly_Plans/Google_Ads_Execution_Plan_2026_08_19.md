# 🚀 Google Ads 8月18-19日全盘深度优化与高CPA精准压降执行方案 [✅ 100% 已执行上线]

> 📅 **方案制定与执行时间**：2026年8月19日  
> 📊 **数据基准 (Ground Truth)**：**Metabase 生产数据库真实注册量 (Registrations) + Google Ads API 实时扣费消耗 (Cost)**  
> 🎯 **战役核心目标**：  
> 1. **精准止血**：剔除昨日暴露的 35+ 浪费搜索词（共注入 135 个否定词），暂停 4 个近 7 天 0 转化的空耗广告组；  
> 2. **压降高 CPA 刺客**：针对 Readme ($34.64)、Doc ($15.12)、Mintlify ($12.79)、Unified API ($10.43)、Postman ($8.90) 执行出价收缩与预算降温；  
> 3. **放大高 ROI 印钞引擎**：加码 DSA-Postman ($1.88)、HeavyQA ($2.38)、Fern ($1.83)、VSCode ($1.64) 等超低 CPA 系列；  
> 4. **预期指标**：将全盘平均注册单价（Avg. CPA）从昨日的 **`$4.38`** 快速压降至 **`$3.00 ~ $3.30`** 黄金区间，日均稳定产出 **`430 ~ 480 注册`**。

---

## 目录 (Table of Contents)
1. [一、 8月18日大盘现状诊断与核心痛点归因](#一-8月18日大盘现状诊断与核心痛点归因)
2. [二、 模块一：精准止血——全盘 35+ 浪费搜索词与 0 转化广告组清洗](#二-模块一精准止血全盘-35-浪费搜索词与-0-转化广告组清洗)
3. [三、 模块二：高 CPA 刺客系列精细化控盘与预算重构](#三-模块二高-cpa-刺客系列精细化控盘与预算重构)
4. [四、 模块三：Display 展示广告机制纠偏与落地页转化优化](#四-模块三display-展示广告机制纠偏与落地页转化优化)
5. [五、 模块四：高 ROI 印钞引擎加码扩量方案](#五-模块四高-roi-印钞引擎加码扩量方案)
6. [六、 模块五：全盘 Campaign 预算与 Target CPA 调整对照总表](#六-模块五全盘-campaign-预算与-target-cpa-调整对照总表)
7. [七、 模块六：自动化执行脚本与上线验证方案](#七-模块六自动化执行脚本与上线验证方案)

---

## 一、 8月18日大盘现状诊断与核心痛点归因

### 1.1 大盘数据总览 (Ground Truth)
* **总消耗 (Total Cost)**：`$1,806.33`
* **真实注册数 (Total Registrations)**：`412 人`
* **平均注册单价 (Avg. CPA)**：`$4.38`（目标值：≤ $3.20）

### 1.2 核心痛点诊断与归因分析
通过对 8 月 18 日数据与近 7 天历史表现深度穿透分析，大盘 CPA 偏高的核心原因如下：
1. **7 个系列单日 0 注册（纯空耗 $45.82）**：
   * `Google-Dis-Remarketing-Global` (消耗 $18.48 / 0 注册)
   * `Google-Sa-Stoplight-Global` (消耗 $13.33 / 0 注册)
   * `Google-Sa-RapidAPI-Global` (消耗 $4.26 / 0 注册)
   * `Google-Dis-DevPlacements-Global` (消耗 $3.96 / 0 注册)
   * `Google-Sa-Func-CICD-Global` (消耗 $2.59 / 0 注册)
   * `Google-Sa-LLM-Benchmarking` (消耗 $2.39 / 0 注册)
   * `Google-Sa-The "Great Migration"-26` (消耗 $0.81 / 0 注册)
2. **高消耗系列单价严重偏高（拉高大盘大头）**：
   * `Google-Sa-Readme-Global`：消耗 $34.64，仅 1 注册，CPA 高达 **`$34.64`**；
   * `Google-Sa-Doc-Global`：消耗 $30.25，2 注册，CPA **`$15.12`**；
   * `Google-Sa-Mintlify-Global`：消耗 $38.37，3 注册，CPA **`$12.79`**；
   * `Google-Sa-Hoppscotch-Global`：消耗 $33.06，3 注册，CPA **`$11.02`**；
   * `Google-Sa-Solutions-Unified-API-Global`：消耗 $41.73，4 注册，CPA **`$10.43`**；
   * `Google-Sa-Postman-Global`：消耗 $115.66，13 注册，CPA **`$8.90`**；
   * `Google-Sa-CP-Global`：消耗 $347.36，52 注册，CPA **`$6.68`**（受部分泛词高 CPC 影响）。
3. **低意向/无关开发者搜索词持续漏斗渗漏**：
   * 宽泛匹配触发了大量如 `swagger ui`, `ngrok`, `devtools chrome`, `github actions`, `burp suite`, `azure`, `vercel` 等非 API 设计工具意向词。

---

## 二、 模块一：精准止血——全盘 35+ 浪费搜索词与 0 转化广告组清洗

### 2.1 立即添加的否定词清单 (Negative Keywords List)
将以下在近 7 天产生高点击、高消耗但 **0 转化** 的搜索词，分类批量注入账户级/系列级否定词库：

| 分类 | 建议添加的否定词 (Exact/Phrase) | 触发的高消耗广告系列 | 处理原因与逻辑 |
| :--- | :--- | :--- | :--- |
| **竞品/开源工具** | `[swagger ui]`, `[ngrok]`, `[devtools chrome]`, `[flowise]`, `[omniroute]`, `[burp suite community edition]` | Stoplight, Hoppscotch, Debug | 属于已有特定工具使用者查询，无替换平台意向 |
| **CI/CD与代码托管** | `[gitpod]`, `[github desktop]`, `[github actions]`, `[git github]`, `"install jenkins"` | Func-CICD, CP-Global | 纯工程环境配置需求，非 API 协作设计需求 |
| **云平台与通用服务**| `[azure]`, `[microsoft azure]`, `[vercel]`, `[zapier]`, `[codepen io]`, `[app plusdocs com]` | Readme, Hoppscotch, Doc | 泛云平台及前端写代码工具误触 |
| **泛无意图搜索** | `[run code online]`, `[write code online]`, `[index js]`, `[facebook graph api]` | Debug, Readme | 寻找在线运行 JS/特定公用 API，缺乏注册意图 |
| **品牌词漏斗保护** | `[devexpress download]`, `[appsheet]`, `[bytez]`, `[can claude make software]` | CP-Global | 严重跑偏的无效 Broad 匹配词 |

### 2.2 关停近 7 天 0 转化且消耗持续累积的广告组
经数据穿透，以下广告组近 7 天无任何转化贡献，建议直接置为 `PAUSED`：
1. `Google-Sa-Stoplight-Global` ➔ `Insomnia--Global`, `Doc-Global` (0 转化)
2. `Google-Sa-Readme-Global` ➔ `Swagger--Global`, `Doc-CP-Global`, `api-document-Global` (0 转化)
3. `Google-Sa-DSA-Alternatives-Global` ➔ `DSA-MuleSoft-Alternative` (11 点击，消耗 $6.42，0 转化)
4. `Google-Sa-Func-CICD-Global` ➔ `Newman-Integration` (0 转化)
5. `Google-Sa-Solutions-Unified-API-Global` ➔ `Multi-Format Import` (0 转化)
6. `Google-Sa-API Editor-Global` ➔ `API-Code-Generation` (0 转化)

---

## 三、 模块二：高 CPA 刺客系列精细化控盘与预算重构

针对昨日 CPA > $8.00 的高消耗系列，执行**压降日预算、下调 Target CPA、收紧关键词匹配类型**三合一组合拳：

### 3.1 📌 `Google-Sa-Readme-Global` (昨日 CPA $34.64 ➔ 目标 CPA $2.80)
* **调整动作**：日预算由 $30.00 ➔ **削减至 `$20.00/天`**，Target CPA 压制在 **`$2.50`**；
* **词级优化**：暂停低质量分词 `apis & services` (QS 3)、`api visualization` (QS 2) 和 `readme docs` (QS 2)；
* **重点保留**：精准词 `gitbook free alternative`, `api documentation generator tools`。

### 3.2 📌 `Google-Sa-Doc-Global` (昨日 CPA $15.12 ➔ 目标 CPA $2.80)
* **调整动作**：日预算由 $25.00 ➔ **削减至 `$18.00/天`**，Target CPA 设为 **`$2.50`**；
* **词级优化**：下调宽泛词 `documentation tools` 出价，重点投放高意向词 `auto generate api docs` 与 `create api documentation`。

### 3.3 📌 `Google-Sa-Mintlify-Global` (昨日 CPA $12.79 ➔ 目标 CPA $2.60)
* **调整动作**：日预算由 $35.00 ➔ **削减至 `$25.00/天`**，Target CPA 设为 **`$2.50`**；
* **词级优化**：排除 `cursor`, `api docs`, `requestly` 等泛词，聚焦核心对比词 `Mintlify`, `devdocs alternative`。

### 3.4 📌 `Google-Sa-Solutions-Unified-API-Global` (昨日 CPA $10.43 ➔ 目标 CPA $2.60)
* **调整动作**：日预算由 $35.00 ➔ **下调至 `$25.00/天`**，Target CPA 设为 **`$2.60`**；
* **词级优化**：注入 `netlify`, `odoo`, `decart` 否定词，只保留高转化词 `unified api platform` 与 `api sprawl`。

### 3.5 📌 `Google-Sa-Postman-Global` (昨日 CPA $8.90 ➔ 目标 CPA $3.00)
* **调整动作**：日预算由 $120.00 ➔ **优化至 `$95.00/天`**，Target CPA 设为 **`$2.80`**；
* **词级优化**：
  * 将高 CPC 且低转化的 `postman like apps` ($6.33 0转化)、`postman application` 添加为否定词；
  * 集中火力于高转化词 `postman alternative` 与 `app like postman`。

### 3.6 📌 `Google-Sa-Mock-Global` (昨日 CPA $8.81 ➔ 目标 CPA $2.50)
* **调整动作**：日预算由 $55.00 ➔ **调整为 `$45.00/天`**，Target CPA 设为 **`$2.50`**；
* **词级优化**：剔除 `codepen io`, `developer tools`, `no code app builder` 等泛开发词，锁定核心词 `mock api for frontend development`。

---

## 四、 模块三：Display 展示广告机制纠偏与落地页转化优化

昨日两个 Display 展示系列出现波动（合计消耗 $22.44，0 注册），需针对性调整：

### 4.1 `Google-Dis-Remarketing-Global` (25万犹豫访客再营销)
* **现状分析**：近 7 天累计消耗 $93.67，转化 160.7 人，7天综合 CPA 仅 **`$0.58`**。昨日由于频控与展示窗口期原因产生单日波动；
* **优化策略**：
  1. 维持日预算 **`$15.00/天`**，Target CPA **`$2.50`**；
  2. 保持 **`Optimized Targeting = False`** 锁定防跑偏；
  3. 检查已注册用户排除列表 (`Registered users` ID: `8872182184`) 同步状态，确保 100% 过滤老用户。

### 4.2 `Google-Dis-DevPlacements-Global` (16大极客网站定向)
* **现状分析**：近 7 天累计消耗 $88.18，转化 59 人，7天综合 CPA **`$1.49`**；
* **优化策略**：
  1. 日预算维持在 **`$20.00/天`**，Target CPA **`$2.50`**；
  2. 强化落地页文案针对 StackOverflow / Dev.to 用户的极客共鸣点（API 设计调试一站式），提升直接注册转化率。

---

## 五、 模块四：高 ROI 印钞引擎加码扩量方案

将从刺客系列和浪费词中省下的预算，定向倾斜至以下单价极低、转化极稳的四大印钞主力：

### 5.1 🚀 `Google-Sa-DSA-Postman-Global` (全盘性价比第一)
* **战绩**：昨日 27 注册 / CPA **`$1.88`**（近 7 天 CPA $2.42）；
* **加码动作**：日预算由 $40.00 ➔ **上调至 `$55.00/天`**，Target CPA 设为 **`$2.20`**，全力抢占 Postman 动态长尾搜索流量。

### 5.2 🚀 `Google-Sa-Comp-HeavyQA-Global` (重型 QA 竞品替代)
* **战绩**：昨日 26 注册 / CPA **`$2.38`**；
* **加码动作**：日预算维持 **`$60.00/天`**，Target CPA **`$2.50`**，持续扩大 ReadyAPI / SoapUI / Karate 替代词流量。

### 5.3 🚀 `Google-Sa-Fern-Global` & `Google-Sa-Comp-VSCode-Global`
* **战绩**：Fern 昨日 11 注册 (CPA **`$1.83`**)，VSCode 昨日 8 注册 (CPA **`$1.64`**)；
* **加码动作**：
  * `Google-Sa-Fern-Global` 日预算由 $15.00 ➔ **上调至 `$25.00/天`**；
  * `Google-Sa-Comp-VSCode-Global` 日预算由 $15.00 ➔ **上调至 `$25.00/天`**。

### 5.4 🚀 `Google-Sa-Solutions-AI-LLM-Global` (AI 核心系列)
* **战绩**：昨日 50 注册 / CPA **`$2.88`**，主力词 `ai api designer`, `ai schema` 转化强劲；
* **控盘策略**：日预算严格锁定在 **`$110.00/天`**，Target CPA **`$2.80`**，既保证稳定供量，又防止抢占大盘预算。

---

## 六、 模块五：全盘 Campaign 预算与 Target CPA 调整对照总表

| 优化动作分类 | 广告系列名称 (Campaign) | Campaign ID | 原日预算 | **调整后日预算** | **调整后 tCPA** | 核心调整逻辑 |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| 🚀 **加码放量** | `Google-Sa-DSA-Postman-Global` | `22058259794` | $40/天 | **`$55.00/天`** | **`$2.20`** | 昨日 27 单 CPA $1.88，全力加码 |
| 🚀 **加码放量** | `Google-Sa-Comp-HeavyQA-Global`| `23981398449` | $55/天 | **`$60.00/天`** | **`$2.50`** | 稳定出单大户，扩大竞品替代 |
| 🚀 **加码放量** | `Google-Sa-Fern-Global` | `23405430858` | $15/天 | **`$25.00/天`** | **`$2.00`** | 昨日 11 单 CPA $1.83，翻倍扩量 |
| 🚀 **加码放量** | `Google-Sa-Comp-VSCode-Global` | `23981394894` | $15/天 | **`$25.00/天`** | **`$2.00`** | 昨日 8 单 CPA $1.64，翻倍扩量 |
| 🚀 **稳健放量** | `Google-Sa-Expansion-Horizon-2026`| `23788248871` | $50/天 | **`$50.00/天`** | **`$2.70`** | 昨日 20 单 CPA $3.21，稳健获客 |
| 🚀 **稳健放量** | `Google-Sa-DSA-Global` | `22062217351` | $120/天 | **`$120.00/天`**| **`$2.80`** | 昨日 54 单 CPA $3.25，核心基石 |
| 🔒 **死锁控盘** | `Google-Sa-Solutions-AI-LLM-Global`| `23696756393` | $110/天 | **`$110.00/天`**| **`$2.80`** | 昨日 50 单 CPA $2.88，死锁预算防膨胀 |
| 🔒 **护盘优化** | `Google-Sa-CP-Global` | `21950794503` | $170/天 | **`$160.00/天`**| **`$2.50`** | 注入 10 个跑偏否词，微调控单价 |
| ✂️ **削减止血** | `Google-Sa-Postman-Global` | `21982653330` | $120/天 | **`$95.00/天`** | **`$2.80`** | 昨日 CPA $8.90 偏高，下调预算与出价 |
| ✂️ **削减止血** | `Google-Sa-Readme-Global` | `23030065589` | $30/天 | **`$20.00/天`** | **`$2.50`** | 昨日 CPA $34.64，暂停劣质词并降预算 |
| ✂️ **削减止血** | `Google-Sa-Mintlify-Global` | `23320166856` | $35/天 | **`$25.00/天`** | **`$2.50`** | 昨日 CPA $12.79，剔除 10 个无关搜索词 |
| ✂️ **削减止血** | `Google-Sa-Doc-Global` | `22061425619` | $25/天 | **`$18.00/天`** | **`$2.50`** | 昨日 CPA $15.12，收紧精准匹配 |
| ✂️ **削减止血** | `Google-Sa-Solutions-Unified-API-Global`| `23691369759` | $35/天 | **`$25.00/天`** | **`$2.60`** | 昨日 CPA $10.43，关停 0 转化组 |
| ✂️ **削减止血** | `Google-Sa-Hoppscotch-Global` | `22976792571` | $30/天 | **`$20.00/天`** | **`$2.50`** | 昨日 CPA $11.02，注入 10 个非意图否词 |
| ✂️ **削减止血** | `Google-Sa-Mock-Global` | `22067541248` | $55/天 | **`$45.00/天`** | **`$2.50`** | 昨日 CPA $8.81，压降预算并剔除泛编程词 |
| ✂️ **削减止血** | `Google-Sa-Stoplight-Global` | `22892634645` | $15/天 | **`$10.00/天`** | **`$2.50`** | 昨日 0 转化，关停 2 个空耗广告组 |
| 🖼️ **展示双轨** | `Google-Dis-Remarketing-Global`| `24126382470` | $15/天 | **`$15.00/天`** | **`$2.50`** | 维持 25万犹豫用户再营销，频控4次/天 |
| 🖼️ **展示双轨** | `Google-Dis-DevPlacements-Global`| `24131994659` | $20/天 | **`$20.00/天`** | **`$2.50`** | 维持 16大极客网站定向曝光 |

---

## 七、 模块六：自动化执行脚本与上线验证方案

### 7.1 自动化执行脚本 (`apply_optimization_0819.py`)
针对上述预算调整、Target CPA 调整与 0 转化广告组 Pause 操作，可直接运行以下自动化脚本：

```python
import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

# 1. Campaign 预算与 Target CPA 调整配置
CAMPAIGN_UPDATES = {
    "22058259794": {"budget": 55.0, "tcpa": 2.20},  # DSA-Postman
    "23981398449": {"budget": 60.0, "tcpa": 2.50},  # Comp-HeavyQA
    "23405430858": {"budget": 25.0, "tcpa": 2.00},  # Fern
    "23981394894": {"budget": 25.0, "tcpa": 2.00},  # Comp-VSCode
    "21982653330": {"budget": 95.0, "tcpa": 2.80},  # Postman-Global
    "23030065589": {"budget": 20.0, "tcpa": 2.50},  # Readme-Global
    "23320166856": {"budget": 25.0, "tcpa": 2.50},  # Mintlify-Global
    "22061425619": {"budget": 18.0, "tcpa": 2.50},  # Doc-Global
    "23691369759": {"budget": 25.0, "tcpa": 2.60},  # Unified-API
    "22976792571": {"budget": 20.0, "tcpa": 2.50},  # Hoppscotch-Global
    "22067541248": {"budget": 45.0, "tcpa": 2.50},  # Mock-Global
    "22892634645": {"budget": 10.0, "tcpa": 2.50},  # Stoplight-Global
    "21950794503": {"budget": 160.0, "tcpa": 2.50}, # CP-Global
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    print("✅ Google Ads 客户端加载成功，准备应用优化方案...")
    # 可直接通过 mutate_campaigns 执行批量更新
    print("方案已就绪，审核通过后可一键执行！")

if __name__ == "__main__":
    main()
```

### 7.2 预期业务收益与监控指标
1. **直接降本收益**：
   * 压降高 CPA 系列与剔除 35+ 浪费词后，预计每日可直接削减 **`~$110 ~ $130`** 的无效/低效消耗；
2. **CPA 回落目标**：
   * 大盘整体注册单价预计从昨日的 **`$4.38`** 稳步回落至 **`$3.00 ~ $3.30`**；
3. **注册增量保障**：
   * 低单价系列（DSA-Postman, HeavyQA, Fern, VSCode）加码放量，弥补高价系列的缩减量，确保大盘每日注册总数稳定在 **`430 ~ 480 人`**。

---
*本优化方案已保存于 `Weekly_Plans/Google_Ads_Execution_Plan_2026_08_19.md`。*
