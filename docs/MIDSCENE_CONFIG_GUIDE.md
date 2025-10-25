# 🔑 Midscene API密钥配置指南

## 📋 概述

Midscene执行器已完全集成到系统的统一配置管理中，使用`enhanced_config.json`中的模型配置，无需单独配置API密钥。

## 🎯 统一配置架构

### 1. **配置文件位置**
```
backend/intelligent_mbt_testing/enhanced_config.json
```

### 2. **Midscene使用的模型配置**

Midscene默认使用系统中的**qwen-plus**模型配置：

```json
{
  "models": {
    "dashscope": {
      "qwen-plus": {
        "model_name": "qwen-plus",
        "api_key": "sk-343983e4232340128017e03e90f79070",
        "temperature": 0.7,
        "stream": true,
        "timeout": 600,
        "max_retries": 3,
        "metadata": {
          "description": "通义千问增强版，主要LLM模型",
          "use_case": "所有文本生成和理解任务"
        }
      }
    }
  }
}
```

## 🔧 配置机制

### 1. **API密钥获取优先级**
```
1. 构造函数传入的api_key参数
2. enhanced_config.json中的模型配置
3. 环境变量OPENAI_API_KEY
```

### 2. **环境变量设置**
Midscene执行器会自动设置以下环境变量：
- `DASHSCOPE_API_KEY`: 通义千问API密钥
- `OPENAI_API_KEY`: 兼容Midscene的API密钥

### 3. **模型配置映射**
```python
# MidsceneAgentExecutor初始化
self.midscene_executor = MidsceneAgentExecutor(
    headless=True,
    model_name="qwen-plus",  # 使用系统主要LLM模型
    api_key=None  # 自动从配置获取
)
```

## 🚀 使用方式

### 1. **默认使用（推荐）**
```python
# 使用系统配置中的qwen-plus模型
executor = MidsceneAgentExecutor()
```

### 2. **指定模型**
```python
# 使用其他配置的模型
executor = MidsceneAgentExecutor(model_name="qwen-vl-max")
```

### 3. **自定义API密钥**
```python
# 覆盖配置文件中的API密钥
executor = MidsceneAgentExecutor(api_key="your_custom_key")
```

## 🎭 支持的模型

根据`enhanced_config.json`配置，支持以下模型：

| 模型名称 | 用途 | API密钥来源 |
|----------|------|-------------|
| **qwen-plus** | 主要LLM模型，Midscene默认使用 | enhanced_config.json |
| **qwen-vl-max** | 视觉理解模型 | enhanced_config.json |
| **text-embedding-v4** | 文本嵌入模型 | enhanced_config.json |

## ⚙️ 配置验证

### 1. **检查配置状态**
```python
from tools.midscene_agent_executor import MidsceneAgentExecutor

# 创建执行器并检查配置
executor = MidsceneAgentExecutor()
print(f"API密钥状态: {'已配置' if executor.api_key else '未配置'}")
print(f"使用模型: {executor.model_name}")
```

### 2. **配置诊断**
如果Midscene功能无法正常工作，请检查：

1. **enhanced_config.json文件是否存在**
2. **qwen-plus模型配置中的api_key是否有效**
3. **API密钥是否有足够的配额**

## 🔍 故障排除

### 常见问题

1. **"未配置API密钥"警告**
   - 检查`enhanced_config.json`中的`api_key`字段
   - 确保API密钥格式正确（sk-开头）

2. **Midscene执行失败**
   - 验证API密钥是否有效
   - 检查网络连接
   - 确认API配额是否充足

3. **模型不支持错误**
   - 确认使用的模型在配置文件中存在
   - 检查模型名称拼写是否正确

### 调试模式

启用详细日志输出：
```python
executor = MidsceneAgentExecutor()
# 执行器会自动打印配置状态
```

## 📊 配置示例

### 完整的enhanced_config.json配置示例：
```json
{
  "models": {
    "dashscope": {
      "qwen-plus": {
        "model_name": "qwen-plus",
        "api_key": "sk-your-dashscope-api-key-here",
        "temperature": 0.7,
        "stream": true,
        "timeout": 600,
        "max_retries": 3,
        "enable_thinking": false,
        "metadata": {
          "description": "通义千问增强版，主要LLM模型",
          "max_context_length": 128000,
          "multimodal": false,
          "cost_per_1k_tokens": 0.004,
          "use_case": "所有文本生成和理解任务，包括Midscene AI测试"
        }
      }
    }
  },
  "agents": {
    "executor": {
      "name": "ExecutorAgent",
      "model_config": {
        "model_name": "qwen-plus",
        "temperature": 0.7,
        "stream": true
      }
    }
  }
}
```

## 🎯 最佳实践

1. **使用统一配置**: 所有模型配置都在`enhanced_config.json`中管理
2. **避免硬编码**: 不要在代码中直接写入API密钥
3. **环境隔离**: 开发、测试、生产环境使用不同的配置文件
4. **定期检查**: 监控API使用量和配额状态
5. **安全存储**: 确保配置文件的访问权限安全

## 🔮 扩展支持

如需支持其他模型提供商（如OpenAI、Claude等），可以在`enhanced_config.json`中添加相应配置：

```json
{
  "models": {
    "openai": {
      "gpt-4": {
        "model_name": "gpt-4",
        "api_key": "sk-your-openai-key",
        "temperature": 0.7
      }
    },
    "anthropic": {
      "claude-3": {
        "model_name": "claude-3-sonnet-20240229",
        "api_key": "sk-ant-your-key",
        "temperature": 0.7
      }
    }
  }
}
```

---

🎉 **通过统一配置管理，Midscene执行器现在完全集成到您的系统架构中，提供一致的配置体验！**
