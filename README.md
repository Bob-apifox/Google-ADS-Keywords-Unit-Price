# 📊 Google Ads & Metabase 注册单价分析工作流

本项目旨在自动化整合 Google Ads 的消耗数据（USD）与 Metabase 的用户注册数据，并按照注册单价（CPA）生成每日排名报告。

## 📂 项目结构 (按属性分类)

```text
google-ads-keywords-unit-price/
├── common/                  # 共享文件
│   └── config/              # 配置文件 (google-ads.yaml)
├── keyword_unit_price/      # 综合分析中心 (核心逻辑)
│   ├── scripts/             # generate_unit_price_report.py (集成脚本)
│   ├── reports/             # 最新综合报告 (final_registration_report.md)
│   └── archive/             # 历史报告存档 (按日期命名)
├── README.md                # 项目说明文档
└── run_report.bat           # Windows 一键执行入口 (双击运行)
```

## 📍 核心组件
1.  **`common/config/google-ads.yaml`**: Google Ads API 配置文件。
2.  **`keyword_unit_price/scripts/generate_unit_price_report.py`**: **集成执行脚本**。顺序执行：注册单价分析 -> Top 20 关键词抓取 -> Postman 竞品词分析。
3.  **`keyword_unit_price/reports/final_registration_report.md`**: 自动生成的最新一份**综合分析报表**。
4.  **`keyword_unit_price/archive/`**: 自动保存的每日历史报告存档。

## 🚀 运行流程
只需执行以下命令，脚本会自动处理所有逻辑：
- **方式 A (推荐)**: 直接双击根目录下的 `run_report.bat`。
- **方式 B (命令行)**: 在根目录下执行 `py keyword_unit_price/scripts/generate_unit_price_report.py`。

## 🛠️ 技术细节
-   **数据源**: 
    -   Google Ads API: 拉取昨日 (Yesterday) 各广告系列的 `metrics.cost_micros`。
    -   Metabase API: 从 `Apidog RDS` 库执行 SQL，获取 `utm_campaign` 对应的注册数。
-   **匹配维度**: 
    -   优先通过 **Campaign ID** 进行关联。
    -   若 ID 不匹配，则尝试通过 **Campaign Name** 进行兼容性关联。
-   **评估预警**:
    -   ✅ **表现优异**: 单价 < 平均价的 50%。
    -   ⚠️ **成本偏高**: 单价 > 平均价的 150%。
    -   🔴 **无转化**: 有消耗但注册数为 0。

## 🧹 环境要求
-   Python 3.10+
-   安装依赖: `pip install requests google-ads`
-   需开启本地代理 (默认 `127.0.0.1:7890`)。

---
*文档更新于: 2026-03-13*
