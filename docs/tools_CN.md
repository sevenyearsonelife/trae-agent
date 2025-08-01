# 工具

Trae Agent 为软件工程任务提供五个内置工具：

## str_replace_based_edit_tool

具有持久状态的文件和目录操作工具。

**操作：**
- `view` - 显示文件内容（带行号），或列出目录内容（最多 2 层深度）
- `create` - 创建新文件（如果文件已存在则失败）
- `str_replace` - 替换文件中的精确字符串匹配（必须唯一）
- `insert` - 在指定行号后插入文本

**关键特性：**
- 需要绝对路径（例如，`/repo/file.py`）
- 字符串替换必须精确匹配，包括空格
- 支持大文件的行范围查看

## bash

在持久会话中执行 shell 命令。

**功能：**
- 命令在维护状态的共享 bash 会话中运行
- 每个命令 120 秒超时
- 会话重启功能
- 后台进程支持

**使用说明：**
- 使用 `restart: true` 重置会话
- 避免输出过大的命令
- 长时间运行的命令应使用 `&` 进行后台执行

## sequential_thinking

用于复杂分析的结构化问题解决工具。

**能力：**
- 将问题分解为连续的思考步骤
- 修改和分支之前的思考
- 动态调整所需的思考数量
- 跟踪思考历史和替代方法
- 生成和验证解决方案假设

**参数：**
- `thought` - 当前思考步骤
- `thought_number` / `total_thoughts` - 进度跟踪
- `next_thought_needed` - 继续思考标志
- `is_revision` / `revises_thought` - 修订跟踪
- `branch_from_thought` / `branch_id` - 替代探索

## task_done

发出任务完成信号并要求验证。

**目的：**
- 将任务标记为成功完成
- 必须在适当验证后调用
- 鼓励编写测试/重现脚本

**输出：**
- 简单的"Task done."消息
- 不需要参数

## json_edit_tool

使用 JSONPath 表达式进行精确的 JSON 文件编辑。

**操作：**
- `view` - 显示整个文件或特定 JSONPath 的内容
- `set` - 更新指定路径的现有值
- `add` - 向对象添加新属性或向数组追加
- `remove` - 删除指定路径的元素

**JSONPath 示例：**
- `$.users[0].name` - 第一个用户的名称
- `$.config.database.host` - 嵌套对象属性
- `$.items[*].price` - 所有项目价格
- `$..key` - 递归搜索键

**功能：**
- 验证 JSON 语法和结构
- 通过漂亮打印选项保留格式
- 无效操作的详细错误消息