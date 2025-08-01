# CLAUDE.md

此文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概要

**Trae Agent** 是一个基于 LLM 的智能代理，专门用于通用软件工程任务。它提供了强大的 CLI 接口，能够理解自然语言指令并使用各种工具和 LLM 提供商执行复杂的软件工程工作流。

**核心特性：**
- 🌊 **Lakeview**: 为代理步骤提供简洁的总结
- 🤖 **多 LLM 支持**: 支持 OpenAI、Anthropic、Doubao、Azure、OpenRouter、Ollama 和 Google Gemini API
- 🛠️ **丰富的工具生态**: 文件编辑、bash 执行、结构化思考等
- 🎯 **交互模式**: 迭代开发的对话界面
- 📊 **轨迹记录**: 详细记录所有代理操作，便于调试和分析
- ⚙️ **灵活配置**: 基于 JSON 的配置，支持环境变量
- 🚀 **易于安装**: 基于 pip 的简单安装

## 开发命令

### 环境设置
```bash
# 创建虚拟环境并安装依赖（推荐）
make install-dev

# 手动设置
uv venv
uv sync --all-extras
```

### 测试
```bash
# 运行所有测试（跳过外部服务测试）
make test
make uv-test

# 运行特定测试类别
uv run pytest tests/ -v --tb=short -m unit
uv run pytest tests/ -v --tb=short -m integration
```

### 代码质量
```bash
# 运行预提交钩子
make pre-commit
make uv-pre-commit

# 修复格式错误
make fix-format

# 安装预提交钩子
make pre-commit-install
```

### CLI 使用
```bash
# 显示配置状态
trae-cli show-config

# 运行任务
trae-cli run "任务描述"
trae-cli run "任务" --provider anthropic --model claude-sonnet-4-20250514

# 交互模式
trae-cli interactive
```

## 架构概览

### 核心组件

**代理架构**: 系统采用模块化代理设计，具有完整的状态管理和执行生命周期：
- `trae_agent/agent/base.py` - 抽象基类，定义代理的核心接口和执行循环
  - 管理工具注册表 (`ToolExecutor`)、轨迹记录器 (`TrajectoryRecorder`) 和 CLI 控制台
  - 实现工厂模式 `from_config()` 支持配置化初始化
  - 提供状态管理：IDLE、THINKING、CALLING_TOOL、REFLECTING、COMPLETED、ERROR
- `trae_agent/agent/trae_agent.py` - 主要的 TraeAgent 实现，专门用于软件工程任务
  - 集成所有工具：bash、文本编辑、JSON编辑、结构化思考、任务完成
  - 支持项目路径管理和补丁生成
  - 处理软件工程特有的工作流程
- `trae_agent/agent/agent_basics.py` - 核心数据结构和错误处理
  - `AgentStep`: 记录单步执行的完整状态，包括思考过程、工具调用、LLM响应
  - `AgentExecution`: 管理整个执行会话的状态和元数据
  - `AgentError`: 专门的错误类型和异常处理

**工具系统**: 可扩展的工具框架，支持并行执行和异步操作：
- `trae_agent/tools/base.py` - 抽象基类和工具执行基础设施
  - `Tool`: 抽象基类，定义工具的接口（`execute()`、`get_name()`、`get_description()`、`get_parameters()`）
  - `ToolExecutor`: 工具执行器，管理工具注册和并行执行
  - `ToolCall`/`ToolResult`: 工具调用和结果的数据结构
  - `ToolError`: 工具执行错误处理
- `trae_agent/tools/bash_tool.py` - Shell 命令执行工具
  - 安全的命令执行环境，支持超时和错误处理
  - 提供工作目录管理和输出捕获
- `trae_agent/tools/edit_tool.py` - 基于字符串替换的文件编辑工具
  - 支持精确的文本替换，避免意外的文件修改
  - 内置语法检查和回滚机制
- `trae_agent/tools/json_edit_tool.py` - JSON 文件操作工具
  - 支持复杂的 JSON 路径操作和结构修改
  - 提供格式化和验证功能
- `trae_agent/tools/sequential_thinking_tool.py` - 结构化推理工具
  - 支持分步推理和问题分解
  - 提供假设验证和决策支持
- `trae_agent/tools/task_done_tool.py` - 任务完成工具
  - 标记任务完成状态
  - 生成执行摘要和结果报告
- `trae_agent/tools/ckg_tool.py` - 代码知识图谱工具
  - 构建和维护代码库的知识图谱
  - 支持代码搜索和关系分析

**LLM 客户端层**: 多提供商支持的工厂模式，统一的接口：
- `trae_agent/utils/llm_client.py` - 主要 LLM 客户端接口
  - `LLMClient`: 统一的客户端接口，支持所有提供商
  - `LLMProvider`: 枚举定义支持的提供商（OpenAI、Anthropic、Google、Azure、OpenRouter、Ollama、Doubao）
  - 工厂模式根据提供商动态创建对应的客户端实例
  - 支持工具调用、聊天历史管理和轨迹记录
- `trae_agent/utils/models/` - 特定提供商实现
  - 每个提供商都有独立的客户端实现，继承自 `BaseLLMClient`
  - 统一的 API 设计：`chat()`、`supports_tool_calling()`、`set_chat_history()`
  - 提供商特定的参数处理和错误处理
- `trae_agent/utils/config.py` - 配置管理，支持环境变量
  - `Config`: 主配置类，管理所有提供商的配置
  - `ModelParameters`: 模型参数数据类
  - 支持配置优先级：命令行 > 配置文件 > 环境变量 > 默认值

**配置系统**: 基于 JSON 的配置，具有优先级覆盖系统：
1. 命令行参数（最高优先级）
2. 配置文件值（`trae_config.json`）
3. 环境变量
4. 默认值（最低优先级）

**Lakeview 系统**: 智能步骤总结和可视化：
- `trae_agent/utils/lake_view.py` - 步骤分析和总结引擎
  - 自动分析代理执行的每个步骤
  - 生成简洁的任务描述和详细信息
  - 支持步骤分类：WRITE_TEST、VERIFY_TEST、EXAMINE_CODE、WRITE_FIX、VERIFY_FIX、REPORT、THINK、OUTLIER
  - 提供轨迹压缩和可视化功能

### 关键模式

**工具执行**: 工具在全局注册表中注册，通过统一接口执行。每个工具实现 `execute()` 方法并返回 `ToolResult` 对象。

**代理循环**: 代理遵循思考-行动-观察模式：
1. 从 LLM 生成推理和工具调用
2. 并行执行工具
3. 观察结果并更新状态
4. 重复直到任务完成或达到步数限制

**多 LLM 支持**: 使用工厂模式创建特定提供商的客户端，同时保持一致的接口。支持 OpenAI、Anthropic、Google、Azure、OpenRouter、Ollama 和 Doubao。

**轨迹记录**: 详细记录所有代理操作、LLM 交互和工具执行，用于调试和分析。保存到 `trajectories/` 目录，带时间戳。

### 配置结构

`trae_config.json` 文件定义：
- `default_provider` - 使用的默认 LLM 提供商
- `max_steps` - 每个任务的最大执行步数
- `enable_lakeview` - 启用 Lakeview 总结功能
- `model_providers` - 每个 LLM 提供商的配置
- `lakeview_config` - Lakeview 特定设置

### 测试框架

测试按组件组织：
- `tests/agent/` - 代理行为和执行测试
- `tests/tools/` - 工具功能测试
- `tests/utils/` - 实用程序和配置测试

测试使用 pytest，标记为 `unit`、`integration` 和 `slow` 测试。默认情况下，使用环境变量跳过外部服务测试。

### 开发指南

- 使用 `uv` 进行依赖管理
- 遵循现有代码风格（100 字符行限制）
- 新代码需要类型提示
- 所有工具必须继承自 `trae_agent.tools.base.Tool`
- 配置更改应保持向后兼容性
- 为新工具和代理功能添加测试

## Git 提交规范
所有提交消息必须遵循以下格式：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```
