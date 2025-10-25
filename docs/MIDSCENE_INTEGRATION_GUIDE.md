# 🎯 Midscene智能体集成指南

## 📋 概述

本指南详细介绍了如何将Midscene.js AI自动化测试框架集成到我们的多智能体测试系统中。

## 🚀 Midscene简介

Midscene是一个基于AI的Web自动化测试框架，具有以下特点：

- **AI驱动**: 使用自然语言描述测试操作
- **多模式支持**: Playwright、Puppeteer、YAML脚本
- **智能理解**: AI理解页面内容和用户意图
- **灵活配置**: 支持多种LLM模型（GPT-4、Qwen等）

## 🔧 集成架构

```
智能体系统
├── EnhancedExecutorAgent (执行智能体)
│   ├── 原有执行功能
│   └── 新增Midscene集成
│       ├── execute_midscene_ai_test()      # AI模式执行
│       ├── execute_midscene_yaml_script()  # YAML模式执行
│       └── execute_hybrid_midscene_test()  # 混合模式执行
│
├── MidsceneAgentExecutor (Midscene执行器)
│   ├── Playwright模式 - 编程式AI控制
│   ├── YAML Scripts模式 - 声明式配置
│   └── 智能模式选择 - 自动选择最佳方式
│
└── 测试用例格式转换
    ├── 通用格式 → Midscene格式
    ├── YAML配置 → Midscene格式
    └── 智能复杂度分析
```

## 📦 安装依赖

### 1. Node.js依赖

```bash
# 全局安装Midscene CLI
npm install -g @midscene/cli

# 项目依赖（如需要）
npm install @midscene/web playwright
```

### 2. Python依赖

```bash
# 已集成到现有系统中，无需额外安装
```

### 3. 环境配置

创建`.env`文件：

```bash
# OpenAI API Key（用于Midscene AI功能）
OPENAI_API_KEY="your_openai_api_key_here"

# 或使用其他模型（参考Midscene文档）
# QWEN_API_KEY="your_qwen_api_key_here"
```

## 🎯 使用方式

### 1. AI模式执行

```python
# 通过智能体执行Midscene AI测试
executor_agent = EnhancedExecutorAgent()

test_request = {
    "test_case": {
        "id": "ai_web_test",
        "url": "https://example.com",
        "steps": [
            {
                "action": "click",
                "data": {"text": "登录按钮"}
            },
            {
                "action": "input", 
                "data": {"text": "用户名", "selector": "用户名输入框"}
            },
            {
                "action": "assert",
                "data": {"assertion": "页面显示欢迎信息"}
            },
            {
                "action": "extract",
                "data": {
                    "query": "{title: string, price: number}[], 找到商品列表",
                    "name": "products"
                }
            }
        ]
    }
}

result = executor_agent.execute_midscene_ai_test(test_request)
```

### 2. YAML模式执行

```python
yaml_content = """
web:
  url: https://www.ebay.com
  viewportWidth: 1280
  viewportHeight: 768

tasks:
  - name: search_products
    flow:
      - aiAction: type 'Headphones' in search box, hit Enter
      - sleep: 3000
      - aiWaitFor: there is at least one product item on page
      - aiQuery: "{name: string, price: number}[], find products and prices"
        name: products
      - aiAssert: There are search results on the page
"""

yaml_request = {
    "yaml_content": yaml_content,
    "yaml_config": {"case_id": "ebay_search"}
}

result = executor_agent.execute_midscene_yaml_script(yaml_request)
```

### 3. 混合智能模式

```python
# 系统自动选择最佳执行模式（Playwright/YAML/Auto）
hybrid_request = {
    "test_case": {
        "id": "smart_test",
        "url": "https://www.google.com",
        "steps": [
            {"action": "input", "data": {"text": "AI测试", "selector": "搜索框"}},
            {"action": "click", "data": {"text": "搜索按钮"}},
            {"action": "extract", "data": {"query": "搜索结果列表", "name": "results"}}
        ]
    },
    "options": {"intelligent_mode": True}
}

result = executor_agent.execute_hybrid_midscene_test(hybrid_request)
```

## 🎭 执行模式对比

| 模式 | 适用场景 | 优势 | 劣势 |
|------|----------|------|------|
| **Playwright模式** | 复杂逻辑、动态交互 | 功能强大、灵活性高 | 需要编程知识 |
| **YAML模式** | 标准化测试流程 | 简单易用、声明式 | 灵活性有限 |
| **智能混合模式** | 自动优化选择 | 最佳性能、智能决策 | 依赖AI分析 |

## 🔍 AI能力

Midscene提供多种AI操作：

### 基础操作
- `aiAction`: AI驱动的页面操作（点击、输入等）
- `aiTap`: AI智能点击目标元素
- `aiWaitFor`: AI等待特定条件满足

### 数据提取
- `aiQuery`: AI结构化数据查询
- `aiString`: AI提取文本信息
- `aiNumber`: AI提取数值信息
- `aiBoolean`: AI判断真假
- `aiLocate`: AI定位元素位置

### 验证断言
- `aiAssert`: AI智能断言验证

## 📊 性能优化

### 1. 智能模式选择

系统根据测试用例复杂度自动选择最佳执行模式：

```python
def _analyze_optimal_execution_mode(self, test_case, options):
    complexity_score = 0
    
    # 复杂操作 +2分
    complex_actions = ["extract", "query", "conditional", "loop"]
    
    # 动态内容 +1分  
    dynamic_indicators = ["wait", "retry", "variable"]
    
    # 并行需求 +3分
    if options.get("parallel_execution"):
        complexity_score += 3
    
    # 智能选择
    if complexity_score >= 5:
        return "playwright"  # 复杂逻辑
    elif complexity_score <= 2:
        return "yaml"        # 简单流程
    else:
        return "auto"        # 自动选择
```

### 2. 资源管理

- 自动清理临时文件
- 浏览器进程管理
- 内存使用优化
- 并发执行控制

## 🧪 测试示例

### eBay商品搜索测试

```python
ebay_test = {
    "id": "ebay_headphone_search",
    "url": "https://www.ebay.com",
    "mode": "auto",
    "actions": [
        {
            "type": "aiAction",
            "instruction": "type 'Headphones' in search box, hit Enter"
        },
        {
            "type": "aiWaitFor", 
            "condition": "there is at least one headphone item on page"
        },
        {
            "type": "aiQuery",
            "query": "{itemTitle: string, price: number}[], find item in list and corresponding price",
            "name": "headphones"
        },
        {
            "type": "aiAssert",
            "assertion": "There is a category filter on the left"
        }
    ]
}
```

### Google搜索测试

```python
google_test = {
    "id": "google_search_test",
    "url": "https://www.google.com", 
    "steps": [
        {"action": "input", "data": {"text": "Midscene.js", "selector": "search box"}},
        {"action": "click", "data": {"text": "search button"}},
        {"action": "wait", "data": {"condition": "search results are displayed"}},
        {"action": "extract", "data": {
            "query": "{title: string, url: string}[], find first 3 search results",
            "name": "search_results"
        }}
    ]
}
```

## 🔧 配置选项

### MidsceneAgentExecutor配置

```python
executor = MidsceneAgentExecutor(
    headless=True,              # 无头模式
    viewport_width=1280,        # 视窗宽度
    viewport_height=768,        # 视窗高度
    api_key="your_api_key",     # API密钥
    temp_dir="/tmp/midscene"    # 临时目录
)
```

### 测试用例选项

```python
test_options = {
    "execution_mode": "auto",           # 执行模式
    "parallel_execution": False,       # 并行执行
    "intelligent_mode": True,          # 智能模式
    "retry_attempts": 3,               # 重试次数
    "timeout": 30000                   # 超时时间(ms)
}
```

## 📈 监控和统计

### 执行统计

```python
stats = executor_agent.execution_stats
print(f"总执行: {stats['total_executions']}")
print(f"成功率: {stats['success_rate']:.1f}%")
print(f"平均时间: {stats['average_execution_time']:.2f}s")

# Midscene特定统计
midscene_stats = executor_agent.midscene_executor.get_stats()
print(f"Playwright执行: {midscene_stats['playwright_executions']}")
print(f"YAML执行: {midscene_stats['yaml_executions']}")
```

### 性能指标

- 执行成功率
- 平均执行时间
- 资源使用情况
- 错误类型分布
- 模式选择统计

## 🚨 故障排除

### 常见问题

1. **Node.js依赖问题**
   ```bash
   npm install -g @midscene/cli
   npm list -g @midscene/cli
   ```

2. **API密钥配置**
   ```bash
   export OPENAI_API_KEY="your_key_here"
   ```

3. **浏览器启动失败**
   ```bash
   npx playwright install chromium
   ```

4. **权限问题**
   ```bash
   chmod +x /path/to/midscene
   ```

### 调试模式

```python
# 启用详细日志
executor = MidsceneAgentExecutor(headless=False)  # 显示浏览器

# 保留临时文件用于调试
test_case["options"]["debug"] = True
```

## 🔮 未来扩展

### 计划功能

1. **移动端支持**: 集成Android自动化
2. **多模型支持**: 支持更多LLM模型
3. **可视化报告**: 增强测试报告功能
4. **智能修复**: AI自动修复测试用例
5. **性能测试**: 集成性能监控

### 集成路线图

- [x] 基础Midscene集成
- [x] 智能模式选择
- [x] 多执行模式支持
- [ ] 移动端测试集成
- [ ] 可视化测试报告
- [ ] AI智能修复功能

## 📚 参考资源

- [Midscene.js官方文档](https://midscenejs.com/)
- [Playwright文档](https://playwright.dev/)
- [AgentScope文档](https://agentscope.readthedocs.io/)
- [示例代码库](./midscene-example-main/)

## 🤝 贡献

欢迎提交Issue和Pull Request来改进Midscene集成功能！

---

🎉 **Midscene集成让我们的智能体测试系统具备了强大的AI驱动Web自动化能力！**
