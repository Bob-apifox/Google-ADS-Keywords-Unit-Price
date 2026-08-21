new_sec_2_1 = """### 2.1 7大暴利王牌系列预算加码与出价释放执行表 (量身定制，拒绝一刀切)

过去 7 天累计为公司带来 **1,018 个超低成本转化（均价仅 $1.40 ~ $1.79）** 的 7 大功臣系列，本周执行 **全面加码上调预算与量身定制 Target CPA 释放**：

| 广告系列名称 (Campaign) | Campaign ID | 7天转化量 | 7天真实 CPA | 线上当前预算 ➔ 建议新预算 | 线上当前 tCPA ➔ **建议新 tCPA** | 核心增量拓词与调整逻辑 |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`Google-Sa-Jmeter-Global`** | `23120363895` | **395.6 个** | **$1.40** | $71.50 ➔ **$95.00/天** 🚀 | $0.84 ➔ **`$1.50`** (释放) | **#1 印钞机！** 放开 $0.84 严苛限制，允许以 $1.50 吸收海量负载测试流量 |
| **`Google-Sa-Readme-Global`** | `23030065589` | **216.7 个** | **$1.79** | $57.60 ➔ **$75.00/天** 🚀 | $1.80 ➔ **`$1.80`** (维持) | **#2 印钞机！** 当前 $1.80 tCPA 运行极佳，纯加大预算至 $75 放大规模 |
| **`Google-Sa-Hoppscotch-Global`** | `22976792571` | **124.0 个** | **$1.60** | $69.00 ➔ **$45.00/天** 🚀 | $0.88 ➔ **`$1.60`** (释放) | **超高 ROI！** 解开 $0.88 严重限流瓶颈，让其吃满 $45 预算，出单翻倍 |
| **`Google-Sa-Fern-Global`** | `23405430858` | **80.5 个** | **$1.74** | $19.50 ➔ **$48.00/天** 🚀 | $0.84 ➔ **`$1.80`** (释放) | 匹配 $1.74 真实转化水平，预算加至 $48 扩大现代 API 团队获客 |
| **`Google-Sa-API Editor-Global`** | `23376992548` | **96.4 个** | **$1.54** | $21.60 ➔ **$32.00/天** 🚀 | $1.80 ➔ **`$1.80`** (维持) | 维持 $1.80 良好出价，日预算提升至 $32 放大出单 |
| **`Google-Sa-Func-MultiProtocol`**| `23981407167` | **65.5 个** | **$1.28** | $21.00 ➔ **$30.00/天** 🚀 | $2.00 ➔ **`$1.80`** (优化) | **全账户最低 CPA ($1.28)！** 成立 SSE 专属组，抢占 45% 高有效率实时协议红利 |
| **`Google-Sa-Bruno-Global`** | `23347684482` | **35.5 个** | **$1.62** | $7.50 ➔ **$15.00/天** 🚀 | $2.00 ➔ **`$2.00`** (维持) | 维持 $2.00 出价，日预算翻倍至 $15 抢占离线市场 |
| **`Google-Sa-Comp-HeavyQA-Global`**| `23981398449`| **273.0 个** | **$1.09** | $34.50 ➔ **$45.00/天** 🚀 | $2.00 ➔ **`$1.60`** (优化) | **ReadyAPI 表现超神 ($1.09)**，预算加至 $45 扩大收割 |
| **合计 / 加权表现** | - | **1,291 个** | **$1.42** | **$302.20 ➔ $385.00/天** | **均价 $1.65** | **预期每周多产出 300~450 个超高性价比优质转化！** |"""

import re

for filepath in [
    r"d:\Apidog Work\Google ADS Keywords Unit Price\Weekly_Plans\Google_Ads_Execution_Plan_2026_08_11.md",
    r"d:\Apidog Work\Google ADS Keywords Unit Price\reports\Google_Ads_Weekly_Execution_Plan_2026_08_11.md"
]:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Replace section 2.1
    pattern = r"### 2\.1 7大暴利王牌系列.*?---\n\n### 2\.2"
    replacement = new_sec_2_1 + "\n\n---\n\n### 2.2"
    new_text, count = re.subn(pattern, replacement, text, flags=re.DOTALL)
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"SUCCESS: updated {filepath}")
    else:
        print(f"ERROR: could not match section 2.1 in {filepath}")
