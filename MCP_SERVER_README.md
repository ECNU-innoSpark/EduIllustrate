# Explanation Generation MCP Server (HTTP/SSE)

这个 MCP (Model Context Protocol) Server 通过 HTTP/SSE 方式封装了视频生成功能。

## 快速开始

### 1. 安装依赖

```bash
pip install fastmcp uvicorn
```

### 2. 启动 MCP Server

```bash
cd /inspire/hdd/project/ai4education/bishuzhen-CZXS24220022/edubench/TheoremExplainAgent
python mcp_server.py
```

默认会在 `http://0.0.0.0:8000` 启动服务器。

### 3. 自定义端口和主机

```bash
# 使用环境变量
export MCP_HOST=127.0.0.1
export MCP_PORT=8080
python mcp_server.py

# 或者在一行
MCP_HOST=127.0.0.1 MCP_PORT=3001 python mcp_server.py
```

## 配置 MCP 客户端

### Claude Desktop 配置

编辑 Claude Desktop 配置文件:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

添加以下配置:

```json
{
  "mcpServers": {
    "explanation-generation": {
      "url": "http://localhost:8000/sse",
      "transport": "sse"
    }
  }
}
```

### 其他 MCP 客户端配置

对于支持 HTTP/SSE 传输的 MCP 客户端:

```json
{
  "server_url": "http://localhost:8000/sse",
  "transport": "sse"
}
```

## API 端点

启动服务器后,可以访问:

- **SSE 端点**: `http://localhost:8000/sse` - MCP 协议的 SSE 传输
- **健康检查**: `http://localhost:8000/health` (如果 FastMCP 提供)

## 可用工具

### 1. `generate_diagram_and_text`

生成教育视频(包含图表和文本解释)。

**参数:**

```python
{
  "problem_path": str,              # 必填: 问题文件路径
  "model": str,                     # 可选: AI 模型,默认 "gemini-3-pro-preview"
  "output_dir": str,                # 可选: 输出目录,默认 "output/explanations"
  "max_retries": int,               # 可选: 最大重试次数,默认 3
  "max_scene_concurrency": int,     # 可选: 场景并发数,默认 5
  "max_topic_concurrency": int,     # 可选: 主题并发数,默认 5
  "translate_to_chinese": bool,     # 可选: 是否翻译成中文,默认 false
  "use_rag": bool,                  # 可选: 是否使用 RAG,默认 false
  "use_visual_fix_code": bool,      # 可选: 是否使用视觉调试,默认 false
  "use_langfuse": bool,             # 可选: 是否启用 Langfuse,默认 true
  "problem_index": int              # 可选: 指定问题索引
}
```

**示例:**

```json
{
  "problem_path": "data/science_problem/science-g12_samples.json",
  "model": "Kimi-K25",
  "output_dir": "output/with_img_kimi2",
  "problem_index":0,
  "translate_to_chinese": true
}
```

**返回:**

```json
{
  "success": true,
  "summary": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "status": "...",
  "results": [
    {
      "problem_index": 0,
      "success": true,
      "md_path": "output/with_img_kimi2/problem_0_physics_g12/doc/solution.md"
    }
  ]
}
```

### 2. `list_available_models`

列出所有可用的 AI 模型。

**参数:** 无

**返回:**

```json
{
  "success": true,
  "models": ["Kimi-K25", "GPT-4", "Claude-3.5", ...],
  "count": 10
}
```

### 3. `png_to_base64`

将 PNG 图片转换为 base64 编码字符串。

**参数:**

```python
{
  "image_path": str,                # 必填: PNG 图片文件路径
  "resize_width": int,              # 可选: 调整图片宽度
  "resize_height": int              # 可选: 调整图片高度
}
```

**说明:**
- 如果只指定宽度或高度,会保持图片原始宽高比
- 如果同时指定宽度和高度,会调整为指定尺寸
- 自动处理 RGBA/透明背景,转换为白色背景

**示例:**

```json
{
  "image_path": "path/to/diagram.png",
  "resize_width": 800
}
```

**返回:**

```json
{
  "success": true,
  "base64": "/9j/4AAQSkZJRg...",
  "format": "PNG",
  "original_size": [1920, 1080],
  "encoded_size": [800, 450],
  "file_size_bytes": 45678
}
```

## 使用示例

### 通过 HTTP 直接调用 (curl)

虽然 MCP 协议通常通过客户端库使用,但你也可以直接测试:

```bash
# 启动服务器
python mcp_server.py &

# 等待几秒让服务器启动
sleep 3

# 测试连接(如果有健康检查端点)
curl http://localhost:8000/health
```

### 通过 MCP 客户端库

```python
import asyncio
from mcp.client.sse import sse_client
from mcp import ClientSession

async def main():
    async with sse_client("http://localhost:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 列出可用工具
            tools = await session.list_tools()
            print("Available tools:", tools)

            # 调用生成视频工具
            result = await session.call_tool(
                "generate_explanation",
                arguments={
                    "problem_path": "data/science_problem/science-g12_samples.json",
                    "model": "Kimi-K25",
                    "translate_to_chinese": True,
                    "output_dir": "output/with_img_kimi2"
                }
            )

            print(result)

asyncio.run(main())
```

### 在 Claude Desktop 中使用

配置好后,在 Claude Desktop 中可以这样使用:

```
请帮我生成视频:
- 问题文件: data/science_problem/science-g12_samples.json
- 使用 Kimi-K25 模型
- 翻译成中文
- 输出到 output/with_img_kimi2
```

Claude 会自动调用 `generate_explanation` 工具。

## 问题文件格式

```json
{
  "problems": [
    {
      "problem": "解释勾股定理",
      "solution": "勾股定理指出,在直角三角形中...",
      "image_path": "path/to/diagram.png"  // 可选
    }
  ]
}
```

## 环境变量

创建 `.env` 文件:

```bash
# MCP Server 配置
MCP_HOST=0.0.0.0
MCP_PORT=8000

# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
# ... 其他模型的 API keys
```

## 生产环境部署

### 使用 systemd (Linux)

创建 `/etc/systemd/system/mcp-explanation-generation.service`:

```ini
[Unit]
Description=Explanation Generation MCP Server
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/TheoremExplainAgent
Environment="MCP_HOST=0.0.0.0"
Environment="MCP_PORT=8000"
ExecStart=/usr/bin/python3 /path/to/TheoremExplainAgent/mcp_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mcp-explanation-generation
sudo systemctl start mcp-explanation-generation
sudo systemctl status mcp-explanation-generation
```

### 使用 Docker

创建 `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastmcp uvicorn

COPY . .

ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000

EXPOSE 8000

CMD ["python", "mcp_server.py"]
```

构建并运行:

```bash
docker build -t explanation-generation-mcp .
docker run -p 8000:8000 --env-file .env explanation-generation-mcp
```

### 使用 nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /mcp/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 故障排查

### 1. 端口已被占用

```bash
# 检查端口占用
lsof -i :8000

# 使用其他端口
MCP_PORT=8001 python mcp_server.py
```

### 2. 无法导入 fastmcp

```bash
pip install fastmcp
```

### 3. 连接超时

检查防火墙设置:

```bash
# Linux (ufw)
sudo ufw allow 8000/tcp

# Linux (firewalld)
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
```

### 4. API Key 错误

确保 `.env` 文件包含必要的 API keys,并且服务器启动时可以读取到。

## 监控和日志

### 查看服务器日志

如果使用 systemd:

```bash
sudo journalctl -u mcp-explanation-generation -f
```

如果直接运行:

```bash
python mcp_server.py 2>&1 | tee mcp_server.log
```

### 健康检查

添加简单的健康检查脚本 `health_check.sh`:

```bash
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/sse)
if [ $response -eq 200 ] || [ $response -eq 405 ]; then
    echo "Server is healthy"
    exit 0
else
    echo "Server is down"
    exit 1
fi
```

## 安全建议

1. **不要在公网暴露**: 默认绑定到 `0.0.0.0`,建议使用反向代理或 VPN
2. **添加认证**: 考虑在 nginx 层添加 HTTP Basic Auth
3. **使用 HTTPS**: 在生产环境使用 SSL/TLS
4. **限流**: 使用 nginx 或 FastMCP 中间件限制请求频率

## 原始命令对照

| 原始命令 | MCP 调用 |
|---------|---------|
| `python generate_explanation.py --problem_path data/problems.json` | `{"tool": "generate_explanation", "arguments": {"problem_path": "data/problems.json"}}` |
| `--model Kimi-K25` | `"model": "Kimi-K25"` |
| `--translate_to_chinese` | `"translate_to_chinese": true` |
| `--output_dir output/explanations` | `"output_dir": "output/explanations"` |
| `--max_scene_concurrency 5` | `"max_scene_concurrency": 5` |

## 相关链接

- [FastMCP 文档](https://github.com/jlowin/fastmcp)
- [MCP 规范](https://modelcontextprotocol.io/)
- [SSE (Server-Sent Events)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
