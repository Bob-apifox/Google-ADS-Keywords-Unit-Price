# 📊 11 个多语言 Campaign 深度审计报告

根据您的要求，我已完成针对 11 个多语言 Campaign 的全面检查。以下是 5 个核心问题的数据详报：

## 1 & 2. Campaign 与 Ad Group 命名健康度检查
> [!WARNING]
> **命名错乱预警**：部分 Campaign 内部使用的是其他国家名字命名的旧组，这源于早期的复制遗留问题。

| Campaign 名称 | 预算 (每日) | 启用的旧 Postman 组名 | 定向国家/地区 (Geo Targeting) | 命名匹配状态 |
| :--- | :--- | :--- | :--- | :--- |
| `Google-Sa-CP-JP` | $20.00 | `Postman-JP` | Japan (JP) | ✅ 匹配 |
| `Google-Sa-CP-ar` | $20.00 | `Postman-AR` | Algeria (DZ), Bahrain (BH), China (CN), Palestine (PS), Iraq (IQ), Jordan (JO), Kuwait (KW), Lebanon (LB), Libya (LY), Mauritania (MR), Morocco (MA), Oman (OM), Qatar (QA), Saudi Arabia (SA), United Arab Emirates (AE), Tunisia (TN), Egypt (EG) | ⚠️ 重名风险 (阿拉伯与阿根廷同名) |
| `Google-Sa-CP-PT` | $20.00 | `Postman-PT` | Brazil (BR), Portugal (PT) | ✅ 匹配 |
| `Google-Sa-CP-KR` | $20.00 | `Postman-KR` | South Korea (KR) | ✅ 匹配 |
| `Google-Sa-CP-DE` | $20.00 | `Postman-DE` | Austria (AT), Germany (DE), Switzerland (CH) | ✅ 匹配 |
| `Google-Sa-CP-VN` | $20.00 | `Postman-VN` | Vietnam (VN) | ✅ 匹配 |
| `Google-Sa-CP-ID` | $20.00 | `Postman-ID` | Indonesia (ID) | ✅ 匹配 |
| `Google-Sa-CP-FR` | $20.00 | `Postman-FR` | Belgium (BE), Canada (CA), France (FR) | ✅ 匹配 |
| `Google-Sa-CP-ESP-2` | $20.00 | `Postman-ES` | Argentina (AR), Chile (CL), Colombia (CO), Mexico (MX), Peru (PE), Spain (ES) | ✅ 匹配 |
| `Google-Sa-CP-AR` | $20.00 | `Postman-AR` | Bahrain (BH), Belarus (BY), Palestine (PS), Iraq (IQ), Jordan (JO), Kuwait (KW), Lebanon (LB), Libya (LY), Mauritania (MR), Morocco (MA), Oman (OM), Qatar (QA), Saudi Arabia (SA), United Arab Emirates (AE), Tunisia (TN), Egypt (EG) | ✅ 匹配 |
| `Google-Sa-CP-TW` | $20.00 | `Postman-TW` | Taiwan (TW) | ✅ 匹配 |

## 3. Postman 组的 CPA 出价 (Target CPA)
| Campaign 名称 | 启用的 Postman 组 | CPA 出价 ($) |
| :--- | :--- | :--- |
| `Google-Sa-CP-JP` | `Postman-JP` | $1.50 |
| `Google-Sa-CP-ar` | `Postman-AR` | $2.38 |
| `Google-Sa-CP-PT` | `Postman-PT` | $1.50 |
| `Google-Sa-CP-KR` | `Postman-KR` | $1.50 |
| `Google-Sa-CP-DE` | `Postman-DE` | $1.50 |
| `Google-Sa-CP-VN` | `Postman-VN` | $1.50 |
| `Google-Sa-CP-ID` | `Postman-ID` | $1.50 |
| `Google-Sa-CP-FR` | `Postman-FR` | $1.50 |
| `Google-Sa-CP-ESP-2` | `Postman-ES` | $1.50 |
| `Google-Sa-CP-AR` | `Postman-AR` | $1.50 |
| `Google-Sa-CP-TW` | `Postman-TW` | $1.50 |

## 4. 创意 (Ads) 个性化程度与违规排查
> 大部分旧组之前已经填满了旧广告，**新注入的 2026 版个性化本地语言创意** 状态显示为 `UNKNOWN`（刚提交审核）。

| Campaign / Ad Group | 启用创意数 | 广告状态审核 | 最新注入的个性化创意标题 (摘录) |
| :--- | :--- | :--- | :--- |
| `Google-Sa-CP-JP` / `Postman-JP` | 3 条 | UNKNOWN (含刚提交的新创意) | Postmanの代替ツール Apidog<br>総合API開発プラットフォーム<br>無料APIテスト＆モック |
| `Google-Sa-CP-ar` / `Postman-AR` | 3 条 | APPROVED, UNKNOWN (含刚提交的新创意) | Best Postman Alternative 2026<br>Apidog: All-in-One API Tool<br>Free API Testing & Mocking |
| `Google-Sa-CP-PT` / `Postman-PT` | 3 条 | UNKNOWN (含刚提交的新创意) | Alternativa ao Postman<br>Plataforma de API Tudo-em-Um<br>Testar API Online Grátis |
| `Google-Sa-CP-KR` / `Postman-KR` | 3 条 | UNKNOWN (含刚提交的新创意) | Postman 최고의 대체툴 Apidog<br>올인원 API 개발 플랫폼<br>무료 API 테스트 및 목서버 |
| `Google-Sa-CP-DE` / `Postman-DE` | 3 条 | UNKNOWN (含刚提交的新创意) | Postman Alternative 2026<br>All-in-One API Platform<br>Kostenloses API Testing |
| `Google-Sa-CP-VN` / `Postman-VN` | 3 条 | UNKNOWN (含刚提交的新创意) | Công Cụ Thay Thế Postman<br>Nền Tảng API Tất-Cả-Trong-<br>Kiểm Thử API Miễn Phí |
| `Google-Sa-CP-ID` / `Postman-ID` | 3 条 | UNKNOWN (含刚提交的新创意) | Alternatif Postman Terbaik<br>Platform API All-in-One<br>Pengujian API Gratis Online |
| `Google-Sa-CP-FR` / `Postman-FR` | 3 条 | UNKNOWN (含刚提交的新创意) | Alternative à Postman<br>Plateforme API All-in-One<br>Test API & Mock Gratuit |
| `Google-Sa-CP-ESP-2` / `Postman-ES` | 3 条 | UNKNOWN (含刚提交的新创意) | Alternativas a Postman<br>Apidog: Mejor Alternativa<br>Prueba API Gratis 2026 |
| `Google-Sa-CP-AR` / `Postman-AR` | 3 条 | UNKNOWN (含刚提交的新创意) | Best Postman Alternative 2026<br>Apidog: All-in-One API Tool<br>Free API Testing & Mocking |
| `Google-Sa-CP-TW` / `Postman-TW` | 3 条 | UNKNOWN (含刚提交的新创意) | Postman 最佳替代方案 Apidog<br>一站式 API 開發測試平台<br>免費 API 測試與 Mock |

## 5. 新的 Postman 关键词是否加上去了？
> [!IMPORTANT]
> **关键词尚未更新**：因为你刚才的指令是“把旧的开启 然后调整好创意就可以投放”，所以脚本**仅仅开启了旧组并注入了新广告文案**，里面的关键词**仍然是你以前留在旧组里的那些老词**（如 `postman nedir`, `بوستمان` 等）。
> 
> 如果你需要把 **2026 方案里全新拓宽的本地化买方意图关键词**（如 `alternativas a postman gratis` 等）追加合并进这些旧组，请告诉我，我立刻运行拓词脚本为你自动注入！