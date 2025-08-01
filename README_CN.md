# Trae Agent

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Alpha](https://img.shields.io/badge/Status-Alpha-red)
[![Pre-commit](https://github.com/bytedance/trae-agent/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/bytedance/trae-agent/actions/workflows/pre-commit.yml)
[![Unit Tests](https://github.com/bytedance/trae-agent/actions/workflows/unit-test.yml/badge.svg)](https://github.com/bytedance/trae-agent/actions/workflows/unit-test.yml)
[![Discord](https://img.shields.io/discord/1320998163615846420?label=Join%20Discord&color=7289DA)](https://discord.gg/VwaQ4ZBHvC)

**Trae Agent** 是一个基于大语言模型的通用软件工程任务智能代理。它提供强大的命令行界面，可以理解自然语言指令，并使用各种工具和 LLM 提供商执行复杂的软件工程工作流。

**项目状态：** 项目仍在积极开发中。如果您愿意帮助我们改进 Trae Agent，请参考 [docs/roadmap_CN.md](docs/roadmap_CN.md) 和 [CONTRIBUTING](CONTRIBUTING.md)。

**与其他 CLI 代理的区别：** Trae Agent 提供透明、模块化的架构，研究人员和开发人员可以轻松修改、扩展和分析，使其成为 **研究 AI 代理架构、进行消融研究和开发新型代理能力** 的理想平台。这种 **_研究友好型设计_** 使学术和开源社区能够为基础代理框架做出贡献并在此基础上构建，促进快速发展的 AI 代理领域的创新。

## ✨ 特性

- 🌊 **Lakeview**：为代理步骤提供简明扼要的总结
- 🤖 **多 LLM 支持**：支持 OpenAI、Anthropic、豆包、Azure、OpenRouter、Ollama 和 Google Gemini API
- 🛠️ **丰富的工具生态系统**：文件编辑、bash 执行、顺序思维等
- 🎯 **交互模式**：用于迭代开发的对话界面
- 📊 **轨迹记录**：详细记录所有代理操作以便调试和分析
- ⚙️ **灵活配置**：基于 JSON 的配置，支持环境变量
- 🚀 **易于安装**：简单的基于 pip 的安装

## 🚀 快速开始

### 安装

我们强烈建议使用 [uv](https://docs.astral.sh/uv/) 来设置项目。

```bash
git clone https://github.com/bytedance/trae-agent.git
cd trae-agent
uv venv
uv sync --all-extras
```

或者使用 make。

```bash
make uv-venv
make uv-sync
```

### 设置 API 密钥

我们建议使用配置文件来配置 Trae Agent。

**配置设置：**

1. **复制示例配置文件：**

   ```bash
   cp trae_config.json.example trae_config.json
   ```

2. **编辑 `trae_config.json` 并将占位符值替换为您的实际凭据：**
   - 将 `"your_openai_api_key"` 替换为您的实际 OpenAI API 密钥
   - 将 `"your_anthropic_api_key"` 替换为您的实际 Anthropic API 密钥
   - 将 `"your_google_api_key"` 替换为您的实际 Google API 密钥
   - 将 `"your_azure_base_url"` 替换为您的实际 Azure 基础 URL
   - 根据需要替换其他占位符 URL 和 API 密钥

**注意：** `trae_config.json` 文件被 git 忽略，以防止意外提交您的 API 密钥。

您还可以将 API 密钥设置为环境变量：

```bash
# 对于 OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# 对于 Anthropic
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# 对于豆包（也适用于其他 OpenAI 兼容的模型提供商）
export DOUBAO_API_KEY="your-doubao-api-key"
export DOUBAO_BASE_URL="your-model-provider-base-url"

# 对于 OpenRouter
export OPENROUTER_API_KEY="your-openrouter-api-key"

# 对于 Google Gemini
export GOOGLE_API_KEY="your-google-api-key"

# 可选：对于 OpenRouter 排名
export OPENROUTER_SITE_URL="https://your-site.com"
export OPENROUTER_SITE_NAME="Your App Name"

# 可选：如果您想使用特定的 openai 兼容 api 提供商，您可以在此处设置基础 url
export OPENAI_BASE_URL="your-openai-compatible-api-base-url"
```

虽然您可以使用 `api_key` 参数直接传递 API 密钥，但我们建议使用 [python-dotenv](https://pypi.org/project/python-dotenv/) 将 `MODEL_API_KEY="My API Key"` 添加到您的 `.env` 文件中。这种方法有助于防止您的 API 密钥在源代码控制中暴露。

### 基本用法

```bash
# 运行简单任务
trae-cli run "创建一个 hello world Python 脚本"

# 使用豆包运行
trae-cli run "创建一个 hello world Python 脚本" --provider doubao --model doubao-seed-1.6

# 使用 Google Gemini 运行
trae-cli run "创建一个 hello world Python 脚本" --provider google --model gemini-2.5-flash
```

## 📖 使用方法

### 命令行界面

主要入口点是 `trae` 命令，包含几个子命令：

#### `trae run` - 执行任务

```bash
# 基本任务执行
trae-cli run "创建一个计算斐波那契数的 Python 脚本"

# 使用特定的提供商和模型
trae-cli run "修复 main.py 中的错误" --provider anthropic --model claude-sonnet-4-20250514

# 使用 OpenRouter 和任何支持的模型
trae-cli run "优化此代码" --provider openrouter --model "openai/gpt-4o"
trae-cli run "添加文档" --provider openrouter --model "anthropic/claude-3-5-sonnet"

# 使用 Google Gemini
trae-cli run "实现数据解析函数" --provider google --model gemini-2.5-pro

# 使用自定义工作目录
trae-cli run "为 utils 模块添加单元测试" --working-dir /path/to/project

# 保存轨迹用于调试
trae-cli run "重构数据库模块" --trajectory-file debug_session.json

# 强制生成补丁
trae-cli run "更新 API 端点" --must-patch
```

#### `trae interactive` - 交互模式

```bash
# 启动交互会话
trae-cli interactive

# 使用自定义配置
trae-cli interactive --provider openai --model gpt-4o --max-steps 30
```

在交互模式中，您可以：

- 输入任何任务描述来执行它
- 使用 `status` 查看代理信息
- 使用 `help` 获取可用命令
- 使用 `clear` 清除屏幕
- 使用 `exit` 或 `quit` 结束会话

#### `trae show-config` - 配置状态

```bash
trae-cli show-config

# 使用自定义配置文件
trae-cli show-config --config-file my_config.json
```

### 配置

Trae Agent 使用 JSON 配置文件进行设置。请参考根目录中的 `trae_config.json` 文件了解详细的配置结构。

**警告：**
对于豆包用户，请使用以下 base_url。

```
base_url=https://ark.cn-beijing.volces.com/api/v3/
```

**配置优先级：**

1. 命令行参数（最高）
2. 配置文件值
3. 环境变量
4. 默认值（最低）

```bash
# 通过 OpenRouter 使用 GPT-4
trae-cli run "编写 Python 脚本" --provider openrouter --model "openai/gpt-4o"

# 通过 OpenRouter 使用 Claude
trae-cli run "审查此代码" --provider openrouter --model "anthropic/claude-3-5-sonnet"

# 通过 OpenRouter 使用 Gemini
trae-cli run "生成文档" --provider openrouter --model "google/gemini-pro"

# 直接使用 Gemini
trae-cli run "分析此数据集" --provider google --model gemini-2.5-flash

# 通过 Ollama 使用 Qwen
trae-cli run "注释此代码" --provider ollama --model "qwen3"
```

**热门 OpenRouter 模型：**

- `openai/gpt-4o` - 最新的 GPT-4 模型
- `anthropic/claude-3-5-sonnet` - 编码任务表现出色
- `google/gemini-pro` - 强大的推理能力
- `meta-llama/llama-3.1-405b` - 开源替代方案
- `openai/gpt-4o-mini` - 快速且经济高效

### 环境变量

- `OPENAI_API_KEY` - OpenAI API 密钥
- `ANTHROPIC_API_KEY` - Anthropic API 密钥
- `GOOGLE_API_KEY` - Google Gemini API 密钥
- `OPENROUTER_API_KEY` - OpenRouter API 密钥
- `OPENROUTER_SITE_URL` - （可选）您的网站 URL 用于 OpenRouter 排名
- `OPENROUTER_SITE_NAME` - （可选）您的网站名称用于 OpenRouter 排名

## 🛠️ 可用工具

Trae Agent 为文件编辑、bash 执行、结构化思维、任务完成和 JSON 操作提供了全面的工具包，新工具正在积极开发中，现有工具也在不断完善。

有关所有可用工具及其功能的详细信息，请参阅 [docs/tools_CN.md](docs/tools_CN.md)。

## 📊 轨迹记录

Trae Agent 自动记录详细的执行轨迹以便调试和分析：

```bash
# 自动生成的轨迹文件
trae-cli run "调试认证模块"
# 保存到：trajectories/trajectory_20250612_220546.json

# 自定义轨迹文件
trae-cli run "优化数据库查询" --trajectory-file optimization_debug.json
```

轨迹文件包含：

- **LLM 交互**：所有消息、响应和工具调用
- **代理步骤**：状态转换和决策点
- **工具使用**：调用了哪些工具及其结果
- **元数据**：时间戳、令牌使用和执行指标

更多详情，请参阅 [docs/TRAJECTORY_RECORDING_CN.md](docs/TRAJECTORY_RECORDING_CN.md)。

## 🤝 贡献

详细的贡献指南，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

1. Fork 仓库
2. 设置开发安装：

   ```bash
   make install-dev
   ```

3. 创建功能分支 (`git checkout -b feature/amazing-feature`)
4. 进行更改
5. 为新功能添加测试
6. 预提交检查

   ```bash
    make pre-commit
    或：
    make uv-pre-commit
   ```

    如果出现格式错误，请尝试：

   ```
    make fix-format
   ```

7. 提交更改 (`git commit -m 'Add amazing feature'`)
8. 推送到分支 (`git push origin feature/amazing-feature`)
9. 打开 Pull Request

### 开发指南

- 遵循 PEP 8 风格指南
- 为新功能添加测试
- 根据需要更新文档
- 在适当的地方使用类型提示
- 提交前确保所有测试通过

## 📋 要求

- Python 3.12+
- 所选提供商的 API 密钥：
  - OpenAI API 密钥（用于 OpenAI 模型）
  - Anthropic API 密钥（用于 Anthropic 模型）
  - OpenRouter API 密钥（用于 OpenRouter 模型）
  - Google API 密钥（用于 Google Gemini 模型）

## 🔧 故障排除

### 常见问题

**导入错误：**

```bash
# 尝试设置 PYTHONPATH
PYTHONPATH=. trae-cli run "your task"
```

**API 密钥问题：**

```bash
# 验证您的 API 密钥已设置
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
echo $GOOGLE_API_KEY
echo $OPENROUTER_API_KEY

# 检查配置
trae-cli show-config
```

**权限错误：**

```bash
# 确保文件操作具有适当权限
chmod +x /path/to/your/project
```

**命令未找到错误：**

```bash
# 您可以尝试
uv run trae-cli `xxxxx`
```

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🙏 致谢

我们感谢 Anthropic 构建 [anthropic-quickstart](https://github.com/anthropics/anthropic-quickstarts) 项目，该项目的工具生态系统为我们提供了宝贵的参考。