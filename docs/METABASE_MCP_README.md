# Metabase MCP 连接与配置指南

本指南详细说明了如何通过 Model Context Protocol (MCP) 将 Metabase 连接到 Claude Desktop 或 Cursor，使 AI 助手能够直接查询和分析您的 Metabase 数据。

## 1. 概述

通过部署 Metabase MCP 服务器，您可以：
- **自然语言查询**：直接问 AI "查询昨天的注册用户数"。
- **数据可视化**：让 AI 生成图表或分析报告。
- **架构感知**：AI 能够理解 Metabase 中的表结构和字段含义。

---

## 2. 方案选择

推荐使用以下两种成熟的开源实现之一：

### 方案 A：基于 Node.js (推荐)
- **仓库**: [lobehub/mcp-server-metabase](https://github.com/lobehub/mcp-server-metabase)
- **特点**: 配置简单，支持 Docker 部署或 npx 直接运行。

### 方案 B：基于 Python
- **仓库**: [hluaguo/metabase-mcp](https://github.com/hluaguo/metabase-mcp)
- **特点**: 适合 Python 环境，与您现有的脚本语言一致。

---

## 3. 配置步骤 (以 Claude Desktop 为例)

### 第一步：获取 Metabase 信息
您需要准备以下信息（参考您现有的 `generate_unit_price_report.py`）：
- `METABASE_URL`: `https://metabase.apifox.cn/`
- `METABASE_USERNAME`: `bob@apifox.com`
- `METABASE_PASSWORD`:您的密码

### 第二步：编辑配置文件
打开 Claude Desktop 的配置文件：
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

### 第三步：添加 MCP 服务器配置

将以下内容添加到 `mcpServers` 节点中：

#### 使用 npx 运行 (Node.js 方案):
```json
{
  "mcpServers": {
    "metabase": {
      "command": "npx",
      "args": [
        "-y",
        "@lobehub/mcp-server-metabase"
      ],
      "env": {
        "METABASE_URL": "https://metabase.apifox.cn/",
        "METABASE_USERNAME": "bob@apifox.com",
        "METABASE_PASSWORD": "您的密码",
        "HTTPS_PROXY": "http://127.0.0.1:7890"  // 如果需要代理请添加
      }
    }
  }
}
```

---

## 4. 在 Cursor 中使用

1. 打开 Cursor 设置 (`Ctrl + Shift + J`)。
2. 导航到 **General** -> **Features** -> **MCP**。
3. 点击 **+ Add New MCP Server**。
4. **Name**: `Metabase`
5. **Type**: `command`
6. **Command**: 
   ```bash
   npx -y @lobehub/mcp-server-metabase
   ```
7. **Environment Variables**:
   添加 `METABASE_URL`, `METABASE_USERNAME`, `METABASE_PASSWORD` 以及 `HTTPS_PROXY` (如需)。

---

## 5. 常用 Prompt 示例

连接成功后，您可以直接在对话框输入：

- "列出 Metabase 中 `Apidog RDS` 数据库的所有表。"
- "查询过去 7 天 `user_trackings` 表中 `utm_source='google_search'` 的记录总数。"
- "帮我分析各广告系列的 CPA (Cost Per Acquisition)，数据从 Metabase 和 Google Ads 综合获取。"

---

## 6. 注意事项

1. **代理设置**：由于您的 Metabase 部署在 `apifox.cn`，如果您的网络环境需要代理（如代码中所示的 `127.0.0.1:7890`），请务必在 `env` 中配置 `HTTPS_PROXY`。
2. **权限管理**：建议在 Metabase 中为 AI 专门创建一个只读账号。
3. **安全**：请勿将包含明文密码的配置文件上传到公共仓库。

---

> [!TIP]
> 建议优先使用 `lobehub` 的版本，因为它在维护活跃度和功能完整性上表现较好。
