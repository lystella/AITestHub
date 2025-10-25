# 🏗️ 项目结构说明

## 📊 **清理后的项目结构**

```
backend/intelligent_mbt_testing/
├── 📁 enhanced_agents/              # AgentScope智能体系统（保留）
│   ├── base_enhanced_agent.py       # 基础智能体类
│   ├── collaboration_pipeline.py    # 协作管道
│   ├── enhanced_*.py                # 6个增强智能体
│   ├── enhanced_test_workflow.py    # 增强测试工作流
│   ├── long_term_memory.py          # 长期记忆
│   ├── monitoring_system.py         # 监控系统
│   ├── state_recovery_manager.py    # 状态恢复
│   └── system_initializer.py        # 系统初始化
│
├── 📁 langgraph_system/             # LangGraph智能体系统（新增）
│   ├── langgraph_integration.py     # LangGraph集成层
│   ├── langgraph_models.py          # 模型管理器
│   ├── langgraph_nodes.py           # 智能体节点
│   ├── langgraph_state.py           # 状态管理
│   └── langgraph_workflow.py        # 工作流图
│
├── 📁 tools/                        # 工具模块
│   ├── docx_parser.py               # 文档解析
│   ├── hybrid_midscene_executor.py  # 混合执行器
│   ├── midscene_agent_executor.py   # Midscene执行器
│   └── midscene_websocket_client.py # WebSocket客户端
│
├── 📁 enhanced_workspace/           # 工作空间（运行时生成）
│   ├── agent_states/                # 智能体状态
│   ├── checkpoints/                 # 检查点（已清理）
│   ├── collaboration_history/       # 协作历史
│   ├── enhanced_workflow/           # 增强工作流
│   ├── logs/                        # 日志（已清理）
│   ├── performance_data/            # 性能数据
│   ├── recovery_data/               # 恢复数据
│   └── sessions/                    # 会话数据
│
├── 📄 enhanced_config.json          # 主配置文件
├── 📄 enhanced_config.py            # 配置管理
├── 📄 enhanced_intelligent_testing_system.py  # AgentScope主系统
├── 📄 model_config.py               # 模型配置
├── 📄 streaming_workflow.py         # 流式工作流
├── 📄 web_service.py                # Web服务（支持框架切换）
├── 📄 websocket_manager.py          # WebSocket管理
├── 📄 README.md                     # 项目说明
├── 📄 USAGE.md                      # 使用说明
├── 📄 SERVICE_USAGE.md              # 服务使用说明
└── 📄 requirements_service.txt      # 依赖要求
```

## 🗑️ **已删除的文件**

### **测试和调试脚本**
- ❌ `test_*.py` - 各种临时测试脚本
- ❌ `complete_system_test.py` - 完整系统测试
- ❌ `interactive_service.py` - 交互式服务

### **修复和优化脚本**
- ❌ `fix_*.py` - 各种修复脚本
- ❌ `auto_fix_*.py` - 自动修复脚本
- ❌ `batch_fix_*.py` - 批量修复脚本

### **分析和报告文件**
- ❌ `AGENT_OPTIMIZATION_*.md` - 优化报告
- ❌ `agent_optimization_plan.py` - 优化计划

### **冗余模块**
- ❌ `dashscope_model_adapter.py` - 已集成到LangGraph
- ❌ `simple_state_manager*.py` - 简化状态管理
- ❌ `simplified_monitoring.py` - 简化监控

### **临时文件**
- ❌ `__pycache__/` - Python缓存文件
- ❌ `enhanced_workspace/checkpoints/*` - 检查点文件
- ❌ `enhanced_workspace/logs/*` - 日志文件
- ❌ `recovery/*` - 恢复文件

## 🎯 **当前系统状态**

### **双框架支持**
- ✅ **AgentScope系统**: 完整保留，功能完整
- ✅ **LangGraph系统**: 新增，支持多模态和向量搜索
- 🔄 **框架切换**: 在`web_service.py`中修改`USE_LANGGRAPH`变量

### **核心功能**
- 🤖 **6个智能体**: 协调、分析、规划、数据、执行、报告
- 🔄 **完整工作流**: 文件上传 → 测试生成 → 执行 → 报告
- 📡 **WebSocket流式**: 实时进度推送
- 🖼️ **多模态分析**: qwen-vl-max（仅LangGraph）
- 🧠 **向量搜索**: text-embedding-v4（仅LangGraph）

### **API接口**
- 🌐 **主服务**: `http://127.0.0.1:8080`
- 📊 **系统状态**: `/status`
- 🚀 **测试执行**: `/enhanced-test-workflow`
- 📈 **工作流可视化**: `/langgraph/workflow-visualization`（LangGraph）
- ℹ️ **框架信息**: `/framework-info`

## 📝 **使用建议**

### **选择框架**
- **AgentScope**: 稳定、成熟、功能完整
- **LangGraph**: 先进、多模态、向量搜索

### **切换方法**
1. 修改 `web_service.py` 中的 `USE_LANGGRAPH = True/False`
2. 重启服务: `python web_service.py`
3. 前端无需修改，自动适配

### **开发建议**
- 保持两个框架的功能同步
- 新功能优先在LangGraph中实现
- 定期清理临时文件和缓存

## 🎉 **清理成果**

- 🗑️ **删除文件**: 20+ 个冗余文件
- 📂 **清理目录**: 多个临时目录
- 💾 **节省空间**: 显著减少项目体积
- 🧹 **结构清晰**: 更清晰的项目结构
- 🚀 **性能提升**: 减少文件扫描时间
