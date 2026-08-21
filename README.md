# 📊 Google Ads & Metabase 规范化工作区 (Standardized Workspace)

本工作区旨在自动化整合 Google Ads 的消耗数据（USD）与 Metabase 的付费归因/用户注册数据，生成高清晰度的周度与月度投放策略报告。

---

## 📁 规范化目录结构 (Workspace Architecture)

```text
d:\Apidog Work\Google ADS Keywords Unit Price\
├── 📄 README.md                                # 工作区总览与使用说明
├── 📄 run_report.bat                           # 一键分析与报告生成批处理
├── 📂 reports/                                 # 📊 正式交付报告 (Reports & Plans)
│   ├── Apidog_Landing_URL_Paid_Attribution_Report.md  # 双看板全量月度归因分析报告 (Markdown)
│   ├── Apidog_Landing_URL_Paid_Attribution_Report_v2.docx # 双看板全量月度归因分析报告 (Word 格式)
│   ├── Google_Ads_Weekly_Execution_Plan.md             # 本周 Google Ads 投放 Master 方案
│   └── dynamic_cpa_table.md                            # 动态 CPA 分析大盘
├── 📂 docs/                                    # 📖 技术指南与配置说明 (Documentation)
│   ├── METABASE_LOGIN_GUIDE.md                 # Metabase 登录与 RDS 提取指南
│   └── METABASE_MCP_README.md                  # Metabase MCP 连接与配置指南
├── 📂 scripts/                                 # 🐍 20+ 个核心 Python 脚本库 (Scripts)
│   ├── fetch_search_terms.py                   # 搜索词提取脚本
│   ├── execute_expansion_keywords.py           # 拓词执行脚本
│   ├── analyze_campaign_negatives.py           # 否定词冲突分析脚本
│   └── ...                                     # 其它计算与归因处理脚本
├── 📂 data/                                    # 📦 数据缓存与文件归档 (Data Storage)
│   ├── raw_json/                               # API 返回的原始 JSON 缓存
│   └── uploads/                                # CSV 导入包与导出文本
├── 📂 archive/                                 # 🗄️ 历史备用文本、中间 Dump 与临时脚本全量归档库
├── 📂 common/                                  # ⚙️ 配置文件库 (Google Ads YAML 等)
└── 📂 keyword_unit_price/                      # 核心业务逻辑包
```

---

## 🎯 核心报告快速通道

* 📊 **最新双看板月度归因 Word 报告**：[Apidog_Landing_URL_Paid_Attribution_Report_v2.docx](file:///d:/Apidog%20Work/Google%20ADS%20Keywords%20Unit%20Price/Apidog_Landing_URL_Paid_Attribution_Report_v2.docx)
* 📄 **最新双看板月度归因 Markdown 报告**：[Apidog_Landing_URL_Paid_Attribution_Report.md](file:///d:/Apidog%20Work/Google%20ADS%20Keywords%20Unit%20Price/reports/Apidog_Landing_URL_Paid_Attribution_Report.md)
* 🚀 **本周 Google Ads 投放 Master 方案**：[Google_Ads_Weekly_Execution_Plan.md](file:///d:/Apidog%20Work/Google%20ADS%20Keywords%20Unit%20Price/reports/Google_Ads_Weekly_Execution_Plan.md)
