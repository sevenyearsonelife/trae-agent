# Trae Agent 的 SWE-bench 评估

本文档解释如何使用 [SWE-bench](https://www.swebench.com/) 评估 [Trae Agent](https://github.com/bytedance/trae-agent)，SWE-bench 是一个用于评估语言模型和代理在软件工程任务上表现的基准测试。

## 概述

SWE-bench 是一个在真实软件工程任务上评估语言模型的基准测试。它包含来自流行 Python 仓库的 GitHub 问题，这些问题已被人类开发者解决。该基准测试评估代理是否能生成正确的补丁来修复问题。

评估过程包括：
1. **设置**：使用 Docker 容器准备评估环境
2. **执行**：在 SWE-bench 实例上运行 Trae Agent 以生成补丁
3. **评估**：使用 SWE-bench 工具测试生成的补丁与真实情况

## 先决条件

在运行评估之前，请确保您具备：

- **Docker**：容器化评估环境所需
- **Python 3.12+**：用于运行评估脚本
- **Git**：用于克隆仓库
- **足够的磁盘空间**：Docker 镜像每个实例可能需要几 GB
- **API 密钥**：Trae Agent 的 OpenAI/Anthropic API 密钥

## 设置说明

确保安装评估的额外依赖项并在 `evaluation` 目录中运行脚本。

```bash
uv sync --extra evaluation
cd evaluation
```

### 1. 克隆和设置 SWE-bench 工具

`swebench_setup.sh` 脚本自动设置 SWE-bench 工具：

```bash
chmod +x swebench_setup.sh
./swebench_setup.sh
```

此脚本：
- 克隆 SWE-bench 仓库
- 检出特定提交以确保可重现性（这是编写本文档时的最新提交哈希）
- 创建 Python 虚拟环境
- 安装 SWE-bench 工具

### 2. 配置 Trae Agent

确保您的 `trae_config.json` 文件已正确配置有效的 API 密钥：

```json
{
  "default_provider": "anthropic",
  "max_steps": 200,
  "model_providers": {
    "anthropic": {
      "api_key": "your_anthropic_api_key",
      "model": "claude-sonnet-4-20250514",
      "max_tokens": 4096,
      "temperature": 0.5
    }
  }
}
```

### 3. 可选：Docker 环境配置

如果需要自定义环境变量，请创建 `docker_env_config.json` 文件：

```json
{
  "preparation_env": {
    "HTTP_PROXY": "http://proxy.example.com:8080",
    "HTTPS_PROXY": "https://proxy.example.com:8080"
  },
  "experiment_env": {
    "CUSTOM_VAR": "value"
  }
}
```

## 使用方法

评估脚本 `swebench.py` 提供几种操作模式：

### 基本使用

```bash
# 在 SWE-bench_Verified 的所有实例上运行评估
python swebench.py --dataset SWE-bench_Verified --working-dir ./trae-workspace

# 在特定实例上运行评估
python swebench.py --instance_ids django__django-12345 scikit-learn__scikit-learn-67890

# 使用自定义配置运行
python swebench.py --config-file custom_config.json --run-id experiment-1
```

### 可用数据集

- **SWE-bench_Verified**：500 个已验证实例（推荐用于初始评估）
- **SWE-bench_Lite**：300 个实例（较小子集）
- **SWE-bench**：2,294 个实例（完整数据集）

### 评估模式

脚本支持三种模式：

1. **`expr`**（仅表达）：生成补丁而不进行评估
2. **`eval`**（仅评估）：评估现有补丁
3. **`e2e`**（端到端）：生成和评估补丁（默认）

```bash
# 仅生成补丁
python swebench.py --mode expr --dataset SWE-bench_Verified

# 仅评估现有补丁
python swebench.py --mode eval --swebench-harness-path ./SWE-bench

# 端到端评估（默认）
python swebench.py --mode e2e --swebench-harness-path ./SWE-bench
```

### 完整命令参考

```bash
python swebench.py \
  --dataset SWE-bench_Verified \
  --config-file ../trae_config_local.json \
  --swebench-harness-path ./SWE-bench \
  --docker-env-config docker_env_config.json \
  --mode e2e
```

**参数：**
- `--dataset`：要使用的 SWE-bench 数据集
- `--config-file`：Trae Agent 配置文件
- `--swebench-harness-path`：SWE-bench 工具路径（评估需要）
- `--docker-env-config`：Docker 环境配置文件
- `--mode`：评估模式（`e2e`、`expr`、`eval`）

## 工作原理

### 1. 镜像准备

脚本首先检查所需的 Docker 镜像：
- 每个 SWE-bench 实例都有特定的 Docker 镜像
- 如果本地不存在，镜像会自动拉取
- 使用基础 Ubuntu 镜像准备 Trae Agent

### 2. Trae Agent 准备

脚本在 Docker 容器中构建 Trae Agent：
- 创建工件（`trae-agent.tar`、`uv.tar`、`uv_shared.tar`）
- 这些工件在所有实例之间重用以提高效率

### 3. 实例执行

对于每个实例：
1. **容器设置**：准备带有实例环境的 Docker 容器
2. **问题描述**：将 GitHub 问题描述写入文件
3. **Trae Agent 执行**：运行 Trae Agent 生成补丁
4. **补丁收集**：保存生成的补丁以供评估

### 4. 评估

使用 SWE-bench 工具：
1. **补丁收集**：将所有生成的补丁收集到 `predictions.json`
2. **测试执行**：在 Docker 容器中针对测试套件运行补丁
3. **结果生成**：生成带有通过/失败状态的评估结果

## 理解结果

### 输出文件

评估在工作目录中创建几个文件：

```
trae-workspace/
├── predictions.json              # 用于评估的生成补丁
├── trae-agent.{run-id}.json     # 最终评估结果
├── {instance_id}/
│   ├── problem_statement.txt    # GitHub 问题描述
│   ├── {instance_id}.patch      # 生成的补丁
│   └── {instance_id}.json       # 轨迹文件
├── trae-agent.tar           # Trae Agent 构建工件
├── uv.tar                   # UV 二进制文件
└── uv_shared.tar            # UV 共享文件
```