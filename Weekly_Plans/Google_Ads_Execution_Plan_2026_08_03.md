# 🚀 下周 Google Ads 投放与横向拓量增量计划 (Week 2 Action Plan)

基于本周的数据表现，下周的整体策略重心是：**“大组剥离排重、劣质流量一刀切、发力验证成功的局部增量、横向跨产品线搭建全新矩阵”**。

---

## 🔗 全局配置：UTM 追踪后缀 (Tracking Template)
在配置所有新建 Campaign 或 Ad Group 时，**必须**在 Campaign 级或 Ad Group 级的 `URL options` (网址选项) -> `Tracking template` (追踪模板) 中配置以下后缀，缺一不可，否则无法归因有效注册：
```text
utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}
```
*(注：如果官网自建了其他特殊的 tracking 参数，请在上方的基础上直接追加)*

---

## 一、 🛑 止血与防跑偏计划 (Optimization & Scrubbing)

### 1. 针对 0 消耗的多语言 Campaign (TW & ES)
*   **激活 0 消耗国家 (TW & ES)**：将台湾和西班牙的初始 CPC 提高 20%，强行帮助它们度过冷启动期。

---

## 二、 🔥 核心优势放大计划 (Scaling the Winners)

### 1. `Postman Alternative` 核心大盘深度下钻
*   **痛点词拓量 (Phrase Match)**：`postman runner limits alternative`, `postman 100% offline`, `import postman collections locally`

---

## 三、 🌌 横向产品线增量矩阵 (Horizontal Products Expansion)

### 1. API 文档生态 (API Docs) ➡️ 【归入现有 Campaign：`Google-Sa-Swagger-Global`】
*   **Ad Group 设置**：新建 Ad Group `API-Docs-Generation`。
*   **拓充关键词**: `[redoc alternative]`, `[stoplight alternative]`, `[readme alternative]`, `swagger ui generator`, `auto generate api docs`, `create interactive api documentation`, `api documentation software`, `generate api docs from postman`, `openapi viewer`
*   **落地页**: `https://apidog.com/api-doc/`
*   **📝 RSA 响应式搜索广告创意 (15 Headlines + 4 Descriptions)**:
    *   **Headlines (标题)**:
        1. Best API Documentation Tool
        2. Beautiful API Documentation
        3. Auto-Generate API Docs
        4. Interactive API Docs
        5. Stop Syncing Docs Manually
        6. Swagger UI Alternative
        7. Better Than Redoc
        8. OpenAPI to Docs Instantly
        9. Zero Code API Documentation
        10. Share APIs with Your Team
        11. Professional API Portal
        12. Free API Documentation Tool
        13. #1 API Design Platform
        14. Seamless API Collaboration
        15. Try Apidog for Free Today
    *   **Descriptions (描述)**:
        1. Stop syncing docs manually. Generate interactive API docs instantly from OpenAPI specs.
        2. Build a beautiful, customized API developer portal in minutes. Try Apidog for free.
        3. The ultimate alternative to Swagger UI and Redoc. Auto-generate docs from your code.
        4. Enhance developer experience with beautiful, interactive, and shareable documentation.

### 2. 智能 Mock 数据 (Mocking) ➡️ 【归入现有 Campaign：现有 Mock 大组】
*   **Ad Group 设置**：既然您账户里已经有了专门针对 Mock 的 Campaign，那我们无需新建，直接在该老 Campaign 下设立全新的长尾攻坚 Ad Group `Mock-Server-Frontend` 即可。
*   **拓充关键词**: `[mockoon alternative]`, `[wiremock alternative]`, `[beeceptor alternative]`, `json server alternative`, `mock api server online`, `fake rest api generator`, `api mock server open source`, `simulate api response`, `mock api for frontend testing`
*   **落地页**: `https://apidog.com/api-mocking/`
*   **📝 RSA 响应式搜索广告创意 (15 Headlines + 4 Descriptions)**:
    *   **Headlines (标题)**:
        1. Smart API Mock Server
        2. Best Mockoon Alternative
        3. Fake REST API Generator
        4. Unblock Your Frontend Team
        5. Generate Mock Data Instantly
        6. Local API Mocking Tool
        7. Better Than JSON Server
        8. Open Source Mock Server
        9. Dynamic Mock API Data
        10. Zero-Code Mocking Engine
        11. OpenAPI to Mock Server
        12. Start Mocking APIs for Free
        13. Frontend Development Tool
        14. Simulate API Responses
        15. Try Apidog for Free Today
    *   **Descriptions (描述)**:
        1. Generate dynamic fake data instantly without writing backend code. 100% realistic.
        2. The ultimate Mockoon alternative. Unblock your frontend team and speed up development.
        3. Create a local or cloud API mock server in seconds based on your OpenAPI specifications.
        4. Stop waiting for backend APIs. Simulate advanced API responses and test UIs faster.

### 3. 多协议支持 (Multi-Protocol) ➡️ 【归入现有 Campaign：`Google-Sa-Testing-Global`】
*   **Ad Group 设置**：新建 Ad Group `Testing-Multi-Protocol`。
*   **拓充关键词**: `test websocket api online`, `websocket client tool`, `grpc client online`, `test graphql api local`, `[altair graphql client alternative]`, `[bloomrpc alternative]`, `grpc gui client`, `test graphql mutations`
*   **落地页**: `https://apidog.com/blog/websocket-testing-tools/` (或协议主页)
*   **📝 RSA 响应式搜索广告创意 (15 Headlines + 4 Descriptions)**:
    *   **Headlines (标题)**:
        1. Test WebSocket APIs Easily
        2. Best GraphQL Client Tool
        3. Advanced gRPC API Testing
        4. Beyond REST APIs
        5. Multi-Protocol API Client
        6. Test WebSockets Online
        7. Best gRPC GUI Client
        8. Visual GraphQL API Tester
        9. Debug APIs Flawlessly
        10. Support WebSockets & gRPC
        11. All-in-One API Tool
        12. Test Any API Protocol
        13. Powerful API Debugger
        14. Seamless API Testing
        15. Try Apidog for Free Today
    *   **Descriptions (描述)**:
        1. The ultimate API client for all protocols. Debug WebSocket, GraphQL, and gRPC endpoints.
        2. Stop using different tools for different APIs. Test REST, SOAP, and gRPC in one workspace.
        3. A powerful visual client for WebSocket and GraphQL testing. Elevate your workflow today.
        4. Easily connect, test, and debug multi-protocol APIs with an intuitive GUI. Start for free.

---

## 四、 🚀 Performance Max (PMax) 双轨试水与风控计划

基于您账户中已有的暂停状态的 PMax Campaign，下周我们将直接唤醒并改造它们。PMax 的核心是 **“素材资源组 (Asset Group)”** 和 **“受众信号 (Audience Signals)”**。
**⚠️ 核心风险提示**：PMax 极度容易跑偏并带入低质量流量（如 AI 词、移动端游戏内广告），且竞品投放极易触发违规。请**务必**在开启前完成以下三道防线配置：

### 防线 1：账户级否定词与版位排除 (杜绝垃圾/AI流量)
在开启 PMax 前，进入 Google Ads 后台的 **Account Settings (账户设置)**：
1.  **Account-level Negative Keywords (账户级否定关键字)**：把 `ai`, `generator`, `chatgpt`, `bot`, `free api` 全部加进去！这是唯一能让 PMax 不乱跑 AI 词的方法。
2.  **Placement Exclusions (展示位置排除)**：把所有 **App Categories (应用类别，共140多个)** 全部打勾排除！绝对不允许我们的 PMax 广告展示在移动端游戏里浪费钱。

### 防线 2：唤醒 `Google-PMax-Postman` (竞品精准抢夺轨)
*   **🌍 地域风控 (极度重要)**：**必须排除美国 (US)**，甚至建议排除英国 (UK)！Postman 在北美对商标 (Trademark) 保护极严，PMax 会自动拼接文案并在全网乱投，极易导致 Google 判定违规甚至封号。
*   **🔗 落地页与扩展设置 (极其关键)**：
    *   **Final URL (最终到达网址)**：设定为专门的对比页 `https://apidog.com/compare/apidog-vs-postman/?utm_source=google_PMax`。
    *   **Final URL Expansion (网址扩展)**：**必须关闭 (Turn Off)**！绝不能让 Google 自作主张把搜竞品的人导流去毫无关联的博客或帮助文档中心。
*   **受众信号 (Audience Signals)**：
    *   **Custom Segments**：输入高意向竞品词 `postman alternative`, `migrate from postman`, `postman runner limits`。
    *   **URL 信号**：浏览过 `postman.com/pricing` 的人。
*   **素材组 (Asset Group) 改造策略**：
    *   **命名修改**：将现有的旧 Asset Group 重命名为 `AssetGroup-Postman-Interception` (或您习惯的规范命名)。
    *   **素材更替**：直接在原有 Asset Group 上修改。**保留**之前上传的优质图片素材（避免重新审核），**清空**其他旧的文字创意，根据数量规范填入以下全新定制素材：
        *   **Headlines (15个)**: Best Postman Alternative, Switch From Postman, No More Runner Limits, 100% Free API Tool, Import Postman in 1-Click, Postman Without Limits, Free Postman Alternative, Ditch Postman Limits, Better API Collaboration, Ultimate API Client, Design & Test APIs Faster, Seamless Postman Migration, Stop Paying for Postman, Advanced API Testing, Try Apidog for Free
        *   **Long Headlines (5个)**: The ultimate Postman alternative without any collection runner limits. | Switch to Apidog and import your Postman collections in one single click. | Stop paying for expensive API tools. Get a complete API platform for free. | Design, debug, and test APIs seamlessly in a powerful visual workspace. | Upgrade your API workflow with a faster, more collaborative Postman alternative.
        *   **Descriptions (5个)**: Tired of Postman's runner limits? Switch to Apidog for unlimited local API testing. | A complete set of tools connecting the entire API lifecycle. Start for free today. | Easily import Postman data and transition your entire team with zero downtime. | An integrated platform for API design, debugging, testing, and documentation. | Realize Design-first API development without the enterprise price tag.
        *   **Sitelinks (4个)**: Apidog Blog, Apidog Changelog, Apidog pricing, Apidog Products
    *   **红线警告**：图片里绝对不能出现 Postman 的官方 Logo。

### 防线 3：唤醒 `Google-PMax-CP-Global` (Apidog 全家桶拉新轨)
*   **🔗 落地页与扩展设置 (极其关键)**：
    *   **Final URL (最终到达网址)**：设定为 `https://apidog.com/?utm_source=google_PMax`。
    *   **Final URL Expansion (网址扩展)**：可以选择 **关闭**，或者如果您想开启让机器自动找流量，则**必须配置 URL Exclusions (排除网址)**，把 `apidog.com/help/` 和 `apidog.com/blog/` 排除掉。
*   **受众信号 (Audience Signals)**：
    *   **Custom Segments**：输入涵盖文档、Mock、自动化的横向宽泛词汇（如 `api documentation tool`, `swagger ui generator`, `fake api mock server`）。
*   **素材组 (Asset Group) 改造策略**：
    *   **命名修改**：将现有的旧 Asset Group 重命名为 `AssetGroup-Apidog-All-in-One`。
    *   **素材更替**：同样在原组修改，**保留**高质量的界面配图，**清空旧文案**，根据数量规范填入以下全新定制素材：
        *   **Headlines (15个)**: All-in-One API Workspace, Swagger UI Alternative, Auto-Generate API Docs, Smart Fake API Mocking, Better API Documentation, Free API Mock Server, Automated API Testing, Complete API Platform, Visual API Editor, Seamless API Collaboration, Design & Debug APIs, Best API Development Tool, API Design Made Easy, Try Apidog for Free, Elevate API Workflows
        *   **Long Headlines (5个)**: Apidog is your all-in-one workspace for API design, documentation, mocking, and testing. | Stop using fragmented tools. Unify your API lifecycle in one powerful platform. | Auto-generate beautiful, interactive API documentation directly from OpenAPI specs. | Instantly create dynamic fake API mock servers without writing backend code. | Experience a real Design-first API development platform tailored for modern teams.
        *   **Descriptions (5个)**: Streamline your API workflow. Design, mock, test, and document APIs in one place. | Automatically validate responses and keep your API docs synced with zero effort. | Replace Swagger, Postman, and Stoplight with a single integrated workspace. | Empower your frontend and backend teams to collaborate flawlessly on APIs. | Create local or cloud API mock servers in seconds. Start your free trial today.
        *   **Sitelinks (4个)**: Apidog Blog, Apidog Changelog, Apidog pricing, Apidog Products

---

## 五、 💻 新建独立战役：纯正 CLI 与终端极客流 (Standalone Campaign: CLI & Terminal)

**💡 核心架构调整**：建立唯一一个专门针对极客后端和架构师的新大组 **`Google-Sa-CLI-Terminal-Global`**。

### 1. 结构与拓词划分 (Ad Groups & Keywords)
*   **Ad Group 1**: `schedule automated api tests`, `api testing cli tools`, `command line api client`, `run postman collection in ci/cd`, `github actions api testing`, `jenkins api test pipeline`
*   **Ad Group 2**: `newman alternative`, `postman cli alternative`, `bruno cli alternative`, `inso cli alternative`, `curl alternative for api testing`, `[httpie alternative]`

### 2. 落地页与追踪
*   **🔗 首选落地页**：`https://apidog.com/apidog-cli/`
*   **📍 UTM 追踪**：(同全局要求)

### 3. 📝 RSA 极客专属广告创意 (15 Headlines + 4 Descriptions)
*   **Headlines (标题)**:
    1. The Ultimate API CLI Tool
    2. Run API Tests in CI/CD
    3. Better Than Newman CLI
    4. Best Postman CLI Alternative
    5. Terminal-Based API Testing
    6. Command Line API Client
    7. Automate Your API Tests
    8. Perfect CI/CD Integration
    9. Zero UI Required
    10. 100% Terminal Efficiency
    11. Lightweight API CLI
    12. Automate API Documentation
    13. Fast API Test Execution
    14. API Testing for DevOps
    15. Try Apidog CLI for Free
*   **Descriptions (描述)**:
    1. Zero UI required. Execute API tests, generate mocks, and deploy directly from your terminal.
    2. Seamlessly integrates with Jenkins, GitHub Actions, and GitLab. Master your CI/CD pipeline.
    3. The perfect Newman and Postman CLI alternative. Lightweight, fast, and highly customizable.
    4. Built for DevOps and backend engineers. Run complex test suites entirely in the command line.

---

## 六、 🛠️ 高级测试场景补充计划 (合入现有 Testing 大组)

**💡 核心架构调整**：直接在现有的 **`Google-Sa-Testing-Global`** 中新增 Ad Group。

### 1. 结构与拓词划分 (Ad Groups & Keywords)
*   **Ad Group 1 (业务流与数据库)**: `graphql api testing tool`, `api testing with database`, `stripe webhook testing`, `data driven api testing`, `end to end api testing`, `api testing visual flow`
*   **Ad Group 2 (鉴权)**: `test api with client certificate`, `mutual tls api testing`, `test api security online`

### 2. 落地页与追踪
*   **🔗 落地页**：强制引导至对应的具体长尾博客（如 `/blog/how-to-test-apis-that-require-client-certificates/`）。
*   **📍 UTM 追踪**：(同全局要求)

### 3. 📝 场景痛点广告创意 (15 Headlines + 4 Descriptions)
*   **Headlines (标题)**:
    1. Advanced API Testing Tool
    2. Test GraphQL & SOAP APIs
    3. API Testing With Database
    4. Test Stripe Webhooks
    5. Support mTLS API Testing
    6. Client Certificate Testing
    7. Data-Driven API Tests
    8. Visual API Flow Control
    9. End-to-End API Workflows
    10. Professional API Testing
    11. Secure API Authentication
    12. Better Than Postman
    13. Complex API Scenarios
    14. Automated API Testing
    15. Try Apidog for Free Today
*   **Descriptions (描述)**:
    1. Handle complex API scenarios with ease. Support for mTLS, visual flow control, and databases.
    2. Build data-driven tests in a visual interface. Stop writing boilerplate test scripts manually.
    3. The best tool for testing secure APIs requiring mutual TLS and client certificates.
    4. Validate Webhooks, execute direct database queries, and test advanced API logic flawlessly.

---

## 七、 🛡️ 8月3日实时数据驱动：精准否词与强势拓量计划 (Daily Optimization)

*(基于 `run_report.bat` 的真实数据反馈)*

### 1. 🚨 精准排雷：基于 8月3日 真实消耗的否词库 (Negative Keywords)
**注意**：这份否词库与之前完全不同，它不是凭空预测的，而是**直接从过去 7 天跑废了真实美金的废词词表里提取的**。请将这些只花钱不注册的词作为 **Campaign 级别**的否定词，具体下发挂载策略如下：

*   **类别 1：非 API 开发圈的大模型/自动化工具 & 纯写代码小白词 (白白浪费钱)**
    *   **👉 适用否定 Campaign**：`Google-Sa-DSA-Global` (极易跑偏)、`Google-Sa-Testing-Global` (泛流量大)、`Google-PMax-CP-Global`
    *   **否词清单**：
        *   `openhands`, `aider`, `v0 by vercel`, `bolt new`, `openmanus`, `openrouter` (大模型工具)
        *   `n8n`, `n8n community edition`, `n8n cloud`, `dify`, `langgraph studio` (自动化工作流)
        *   `qwen 3.6 coder`, `бесплатный api ключ deepseek` (寻找免费大模型 Key 的羊毛党)
        *   `pwa builder`, `appmachine`, `andromo`, `create an app`, `mobile app development`
        *   `https jsbin com`, `run code online`, `codepad`, `pycharm community`, `flask api`, `main py`

*   **类别 2：零转化竞品白嫖词**
    *   **👉 适用否定 Campaign**：`Google-PMax-Postman` (PMax竞品轨)、`Google-Sa-DSA-Global`
    *   **否词清单**：
        *   `postman download`, `postman online without login`, `postman web app`, `thunder client free`, `insomnia api testing download`

### 2. 📈 乘胜追击：基于真实高转化词的拓量计划 (Expansion Plan)
刚才的报告里藏着几个**转化成本极低、注册量极大**的黑马，我们必须马上围绕它们进行专项拓量：

*   **🔥 黑马赛道 1：AI 编程与前端代码调试 (拆分拓量) ➡️ 【极速拓量】**
    *   **数据发现**：在早前的测试中，`ai coding` (57个注册), `dart devtools` (44个注册), `chrome debugger` (20个注册) 的 CPA 全部低于 $1，简直是暴利赛道！
    *   **拓量动作**：根据词性拆分到不同的 Campaign 建新组：
        1.  **AI Coding 衍生组 ➡️ 【放入专门的 AI Campaign：`Google-Sa-Solutions-AI-LLM-Global`】**：新建 Ad Group 专门承接纯 AI 关键词：`ai coding assistant`, `ai code generator for api`, `cursor ai alternative`。
        2.  **DevTools 衍生组 ➡️ 【留在原 `Debug-Global`】**：`react devtools alternative`, `network tab debugger`, `debug api payload`。
        3.  **前端语言衍生组 ➡️ 【留在原 `Debug-Global`】**：`flutter api debugging`, `dart api client`。
*   **🌍 黑马赛道 2：阿拉伯市场的极低成本 (CP-AR) ➡️ 【加码预算】**
    *   **数据发现**：中东区 `Google-Sa-CP-AR` 带来了惊人的 **122 个注册**，CPA 只有可怜的 **$1.15**。
    *   **拓量动作**：在维持现有 Postman 词的基础上，拓充阿拉伯语本土长尾词：`بديل postman` (Postman alternative), `اختبار واجهة برمجة التطبيقات` (API testing)。
*   **🚀 黑马赛道 3：细分轻量化竞品 (Bruno & Scalar) ➡️ 【乘胜追击】**
    *   **数据发现**：`scalar api` (33个注册，CPA $1.75) 和 `bruno api` (25个注册，CPA $2.60) 表现极其稳健。
    *   **拓量动作**：在这两个 Campaign 下增加高意向转移词：`migrate from bruno to apidog`, `scalar api alternative`, `open source api client comparison`。

*(注：坚决执行您之前的决策，不对 `api testing` 等跑量泛词做“一刀切”的精确匹配收缩，让大词继续保持火力探测。)*
