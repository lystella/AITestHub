# 🤖 AITestHub - 多Agent智能测试平台

> 基于LangGraph和AgentScope的企业级多智能体协作测试系统

## 🎯 项目简介

AITestHub是一个先进的多Agent智能测试平台，集成了6个专业智能体的协作能力，实现从需求分析到测试执行的完整智能化流程。

### ✨ 核心特性

- 🤖 **6个专业智能体**: CoordinatorAgent、AnalysisAgent、PlannerAgent、DataAgent、ExecutorAgent、ReporterAgent
- 🖼️ **多模态分析**: 支持图像、文档、文本等多种输入格式
- 🧠 **智能向量搜索**: 基于text-embedding-v4的强大搜索能力
- 📡 **实时协作**: WebSocket实时显示智能体协作过程
- 💾 **长期记忆**: 支持经验学习和历史记录
- 🔧 **工作流可视化**: 完整的LangGraph工作流展示

## 🏗️ 项目结构

```
AITestHub/
├── 📁 backend/                 # 后端服务
│   ├── 📁 config/              # 配置文件
│   └── 📁 intelligent_mbt_testing/  # 核心测试系统
│       ├── 📁 langgraph_system/     # LangGraph模块
│       ├── 📁 tools/               # 工具函数
│       ├── 📁 enhanced_workspace/    # 工作空间数据
│       ├── web_service.py          # Web服务入口
│       └── unified_intelligent_testing_system.py  # 核心系统
├── 📁 front/                   # 前端界面
│   ├── 📁 src/                 # React源码
│   │   ├── 📁 components/      # 组件
│   │   └── 📁 pages/           # 页面
│   └── package.json            # 前端依赖
├── 📁 docs/                    # 项目文档
├── 📁 tests/                   # 测试文件
├── 📁 scripts/                 # 启动脚本
├── 📁 examples/                # 示例代码
└── 📁 venv/                    # Python虚拟环境
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- 阿里云通义千问API密钥

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/lystella/AITestHub.git
cd AITestHub
```

2. **安装后端依赖**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r backend/intelligent_mbt_testing/requirements_service.txt
```

3. **安装前端依赖**
```bash
cd front
npm install
```

4. **配置API密钥**
```bash
# 在 backend/intelligent_mbt_testing/web_service.py 中设置
os.environ["DASHSCOPE_API_KEY"] = "your-api-key"
```

### 启动服务

1. **启动后端服务**
```bash
cd backend/intelligent_mbt_testing
python web_service.py
# 服务地址: http://localhost:8090
```

2. **启动前端服务**
```bash
cd front
npm start
# 访问地址: http://localhost:3000
```

## 🎮 使用指南

### 基本使用流程

1. **访问系统**: 打开 http://localhost:3000
2. **选择功能**: 点击"多Agent智能调度"卡片
3. **上传文档**: 支持Word、PDF、TXT格式
4. **开始分析**: 点击"开始多Agent协作分析"
5. **查看结果**: 实时观察6个智能体的协作过程

### API接口

- **系统状态**: `GET /status`
- **启动工作流**: `POST /enhanced-test-workflow`
- **WebSocket**: `ws://localhost:8090/ws/{workflow_id}`
- **API文档**: `http://localhost:8090/docs`

## 🔧 技术架构

### 后端技术栈
- **框架**: FastAPI + LangGraph + AgentScope
- **AI模型**: 阿里云通义千问 (qwen-plus, qwen-vl-max, text-embedding-v4)
- **实时通信**: WebSocket
- **数据存储**: JSON文件 + 向量数据库

### 前端技术栈
- **框架**: React 18 + Ant Design 5.x
- **路由**: React Router DOM 6
- **实时通信**: WebSocket API
- **构建工具**: Create React App + CRACO

## 📊 智能体说明

| 智能体 | 职责 | 功能描述 |
|--------|------|----------|
| **CoordinatorAgent** | 协调专家 | 任务分解、资源调度、流程控制 |
| **AnalysisAgent** | 分析专家 | 多模态需求分析、文档解析 |
| **PlannerAgent** | 规划专家 | 测试策略制定、用例设计 |
| **DataProcessorAgent** | 数据专家 | 向量搜索、数据处理、知识管理 |
| **ExecutorAgent** | 执行专家 | MidScene自动化测试执行 |
| **ReporterAgent** | 报告专家 | 结果汇总、报告生成、可视化 |

## 🛠️ 开发指南

### 添加新智能体

1. 在 `langgraph_system/langgraph_nodes.py` 中定义节点
2. 在 `langgraph_system/langgraph_workflow.py` 中注册工作流
3. 更新 `unified_intelligent_testing_system.py` 中的智能体列表

### 自定义工具

1. 在 `tools/` 目录下创建新工具
2. 实现工具接口
3. 在智能体中注册使用

## 📝 更新日志

### v2.0.0 (当前版本)
- ✅ 完整的LangGraph工作流系统
- ✅ 6个专业智能体协作
- ✅ 多模态分析支持
- ✅ 实时WebSocket通信
- ✅ 长期记忆系统
- ✅ 工作流可视化

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 创建 Pull Request

## 📄 许可证

MIT License

## 🆘 支持与反馈

- **问题反馈**: 请创建 Issue
- **功能建议**: 欢迎提交 Feature Request
- **技术交流**: 欢迎参与讨论

---

**🎉 感谢使用AITestHub！让我们一起构建更智能的测试未来！**
