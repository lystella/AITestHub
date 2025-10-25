# 简化版通义千问配置 - 3个核心模型

## 🎯 简化说明

根据您的需求，我们已经将 AgentScope 的模型配置简化为只使用 3 个核心通义千问模型：

### 📋 核心模型配置

| 模型 | 用途 | 描述 |
|------|------|------|
| **qwen-plus** | 主要LLM模型 | 统一处理所有文本任务：对话、推理、代码生成、文档写作、任务规划 |
| **qwen-vl-max** | 视觉模型 | 专门处理图像相关任务：图像分析、视觉问答、OCR文字识别 |
| **text-embedding-v4** | 嵌入模型 | 负责文本向量化：语义搜索、相似度计算、文档检索 |

## 🗂️ 文件结构

```
examples/config/
├── qwen_simplified_config.json    # 🆕 简化版配置文件
├── qwen_simple_example.py         # 🆕 简化版使用示例
├── qwen_quick_start.py            # 🔄 更新的快速启动脚本
├── README_simplified.md           # 🆕 简化版说明文档
├── qwen_config.json               # 原完整配置（可选）
├── qwen_example.py                # 原完整示例（可选）
└── README_qwen.md                 # 原详细文档（可选）

src/agentscope/
└── config.py                     # 🔄 已简化，只支持DashScope
```

## 🚀 快速开始

### 1. 环境设置

```bash
# 安装DashScope SDK
pip install dashscope

# 设置API密钥
export DASHSCOPE_API_KEY="your_dashscope_api_key"
```

### 2. 获取API密钥

访问 [DashScope控制台](https://dashscope.console.aliyun.com/) 获取API密钥

### 3. 运行示例

```bash
cd examples/config

# 快速启动（推荐）
python qwen_quick_start.py

# 简化版演示
python qwen_simple_example.py

# 使用简化配置的流式推理
cd ../streaming_reasoning
python main.py

# 使用简化配置的MBT测试
cd ../mbt_testing_application
python main.py
```

## 💰 成本分析

| 模型 | 成本/1K tokens | 使用频率 | 主要场景 |
|------|----------------|----------|----------|
| qwen-plus | ¥0.004 | 🔥🔥🔥 高 | 90%的日常任务 |
| qwen-vl-max | ¥0.02 | 🔥 低 | 仅图像相关任务 |
| text-embedding-v4 | ¥0.0007 | 🔥 低 | 仅向量化任务 |

**💡 成本优化建议：**
- 大部分场景只使用 qwen-plus，成本可控
- 只在真正需要时才调用视觉和嵌入模型
- 统一模型减少了复杂度和管理成本

## 🔧 在代码中使用

### 简单使用

```python
from agentscope.config import create_model
import agentscope

# 初始化
agentscope.init(project="my_project")

# 创建文本模型（默认）
text_model = create_model("dashscope", "qwen-plus")

# 创建视觉模型（按需）
vision_model = create_model("dashscope", "qwen-vl-max")

# 创建嵌入模型（按需）
embedding_model = create_model("dashscope", "text-embedding-v4")
```

### 使用简化配置

```python
from agentscope.config import ConfigManager
from pathlib import Path

# 加载简化配置
config_file = Path("examples/config/qwen_simplified_config.json")
config_manager = ConfigManager(config_file)

# 获取预配置的智能体
default_agent_config = config_manager.get_agent_config("default")
vision_agent_config = config_manager.get_agent_config("vision")
```

## 📊 智能体角色分配

所有智能体现在统一使用 **qwen-plus** 作为基础模型：

| 智能体 | 模型 | 职责 |
|--------|------|------|
| DefaultAgent | qwen-plus | 通用对话和任务处理 |
| PlannerAgent | qwen-plus | 任务规划和分解 |
| ExecutorAgent | qwen-plus | 指令执行和操作 |
| ReporterAgent | qwen-plus | 报告生成和总结 |
| VisionAgent | qwen-vl-max | 图像分析和视觉理解 |
| EmbeddingAgent | text-embedding-v4 | 文本向量化 |

## 🔄 已删除的配置

为了简化配置，我们已经删除了以下内容：

### 已删除的模型提供商
- ❌ OpenAI (gpt-4, gpt-3.5-turbo, gpt-4-turbo)
- ❌ Claude (claude-3-5-sonnet, claude-3-haiku)
- ❌ Ollama (llama2, llama3, codellama)
- ❌ Azure OpenAI

### 已删除的Qwen模型
- ❌ qwen-turbo (被qwen-plus替代)
- ❌ qwen-max (成本较高，qwen-plus已足够)
- ❌ qwen2.5-72b-instruct (开源版本，不常用)
- ❌ qwq-32b-preview (深度推理，特殊场景)
- ❌ qwen-vl-plus (被qwen-vl-max替代)

### 已删除的配置类
- ❌ OpenAIConfig
- ❌ ClaudeConfig  
- ❌ OllamaConfig
- ❌ AzureOpenAIConfig

## ✅ 简化后的优势

### 🎯 降低复杂度
- 只需管理 3 个模型
- 配置文件更简洁
- 更容易理解和维护

### 💰 成本可控
- 统一使用 qwen-plus 处理大部分任务
- 按需使用视觉和嵌入模型
- 避免高成本模型的误用

### 🚀 提高效率  
- 减少模型选择的困扰
- 统一的调用方式
- 更快的开发和部署

### 🔧 易于维护
- 单一API密钥管理
- 统一的错误处理
- 简化的监控和日志

## 🛠️ 迁移指南

如果您之前使用了其他模型，迁移到简化配置：

### 从 OpenAI 迁移
```python
# 旧代码
model = create_model("openai", "gpt-4")

# 新代码
model = create_model("dashscope", "qwen-plus")
```

### 从其他 Qwen 模型迁移
```python
# 旧代码
model = create_model("dashscope", "qwen-max")
model = create_model("dashscope", "qwen-turbo")

# 新代码（统一使用）
model = create_model("dashscope", "qwen-plus")
```

### 视觉任务迁移
```python
# 旧代码
model = create_model("dashscope", "qwen-vl-plus")

# 新代码
model = create_model("dashscope", "qwen-vl-max")
```

## 📝 配置验证

使用简化配置后，系统会自动验证：

```python
from agentscope.config import get_config_manager

config_manager = get_config_manager()
issues = config_manager.validate_config()

if issues:
    print("配置问题:", issues)
else:
    print("✅ 配置验证通过")
```

## 🔍 故障排除

### 常见问题

1. **API密钥问题**
   ```bash
   export DASHSCOPE_API_KEY="your_key_here"
   ```

2. **模型不存在错误**
   - 确认只使用 3 个支持的模型
   - 检查模型名称拼写

3. **导入错误**
   - 确保安装了 `dashscope` 包
   - 检查 AgentScope 路径

### 获取帮助

- [DashScope官方文档](https://help.aliyun.com/zh/dashscope/)
- [AgentScope GitHub](https://github.com/modelscope/agentscope)

---

通过这个简化配置，您现在可以用最少的复杂度和成本，充分利用通义千问的强大能力！
