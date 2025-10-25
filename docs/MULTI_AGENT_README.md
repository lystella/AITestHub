# 🤖 多Agent智能协作系统使用指南

## 📋 系统概述

这是一个基于**AgentScope框架**的企业级多Agent智能协作测试系统，实现了6个专业智能体的协同工作，支持实时流式输出和WebSocket通信。

### 🎯 核心特性

- **🧠 6个专业智能体协作**: CoordinatorAgent、AnalysisAgent、PlannerAgent、DataAgent、ExecutorAgent、ReporterAgent
- **🔄 实时流式输出**: WebSocket实时显示Agent执行过程
- **📊 完整工作流**: 协调规划 → 需求分析 → 用例执行
- **🎨 现代化UI**: 基于React + Ant Design的响应式界面
- **⚡ 高性能架构**: FastAPI后端 + WebSocket实时通信

## 🚀 快速启动

### 方式1: 一键启动脚本 (推荐)

```bash
python start_multi_agent_system.py
```

脚本会自动：
- 检查系统要求
- 安装前后端依赖
- 启动后端服务 (端口8080)
- 启动前端服务 (端口3000)
- 打开浏览器访问系统

### 方式2: 手动启动

#### 启动后端
```bash
cd backend/intelligent_mbt_testing
pip install -r requirements_service.txt
python start_service.py --mode web --port 8080
```

#### 启动前端
```bash
cd front
npm install
npm start
```

## 📖 使用说明

### 1. 访问系统
- 打开浏览器访问: `http://localhost:3000`
- 在Dashboard中点击 **"多Agent智能调度"** 卡片

### 2. 上传文档
- 支持格式: Word (.doc/.docx)、PDF (.pdf)、文本 (.txt)
- 文件大小限制: 10MB
- 拖拽或点击上传文档

### 3. 开始协作
- 点击 **"开始多Agent协作分析"** 按钮
- 系统将启动实时工作流

### 4. 观察执行过程
- **进度条**: 显示当前执行阶段
- **实时日志**: 显示各Agent的执行过程
- **状态指示**: 每个阶段的执行状态

## 🤖 智能体工作流

### 阶段1: 协调规划 (Coordination)
- **CoordinatorAgent**: 任务分解与资源调度
- **PlannerAgent**: 制定执行计划
- **输出**: 执行策略和资源分配方案

### 阶段2: 需求分析 (Analysis)  
- **AnalysisAgent**: 文档解析与需求提取
- **DataAgent**: 测试数据准备和生成
- **输出**: 功能需求、非功能需求、测试数据

### 阶段3: 用例执行 (Execution)
- **ExecutorAgent**: 测试用例生成与执行
- **ReporterAgent**: 测试报告生成
- **输出**: 测试结果和详细报告

## 🔧 技术架构

### 后端技术栈
- **框架**: FastAPI + uvicorn
- **AI框架**: AgentScope
- **模型**: 阿里云通义千问 (qwen-plus)
- **实时通信**: WebSocket
- **数据验证**: Pydantic

### 前端技术栈
- **框架**: React 18
- **UI库**: Ant Design 5.x
- **路由**: React Router DOM 6
- **状态管理**: React Hooks
- **实时通信**: WebSocket API

### 核心组件

#### 后端核心文件
```
backend/intelligent_mbt_testing/
├── websocket_manager.py          # WebSocket连接管理
├── streaming_workflow.py         # 流式工作流管理
├── web_service.py               # Web服务和API端点
├── enhanced_intelligent_testing_system.py  # 主系统
└── enhanced_agents/             # 6个智能体实现
```

#### 前端核心文件
```
front/src/
├── pages/MultiAgentCollaboration.js  # 多Agent协作页面
├── components/Dashboard.js           # 主仪表盘
├── components/Sidebar.js            # 侧边栏导航
└── App.js                          # 路由配置
```

## 📊 API接口

### WebSocket端点
```
ws://localhost:8080/ws/{workflow_id}
```

### HTTP API端点
- `POST /stream-test` - 启动流式测试
- `GET /workflow-status/{workflow_id}` - 获取工作流状态
- `GET /active-workflows` - 获取活跃工作流
- `GET /status` - 系统状态检查
- `GET /health` - 健康检查

## 🎨 界面功能

### Dashboard功能卡片
- **AI需求分析** - 智能解析需求文档 ✅
- **AI测试设计** - 自动创建测试用例 🔄
- **AI数据生成** - 智能生成测试数据 ✅
- **AI测试执行** - 智能执行测试 🚀
- **AI性能测试** - 模拟高并发场景 ✅
- **AI安全测试** - 自动扫描漏洞 ⚠️
- **多Agent智能调度** - 多Agent协作 ✅

### 多Agent协作页面
- **文档上传区**: 拖拽上传，格式验证
- **执行进度**: 3阶段进度条，状态指示
- **实时日志**: Agent执行过程，彩色输出
- **操作控制**: 重置流程，查看报告

## 🔍 实时日志说明

### 日志类型
- **🔗 连接消息**: WebSocket连接状态
- **🚀 阶段开始**: 各阶段启动信息
- **✅ 阶段完成**: 各阶段完成信息
- **📊 进度更新**: 执行进度信息
- **🎉 工作流完成**: 整体完成信息

### Agent图标说明
- **🤖 CoordinatorAgent**: 紫色机器人图标
- **📄 AnalysisAgent**: 蓝色文档图标
- **⚡ ExecutorAgent**: 绿色闪电图标
- **🐛 PlannerAgent**: 黄色调试图标
- **🔧 System**: 灰色机器人图标

## 🚨 故障排除

### 常见问题

#### 1. 后端启动失败
```bash
# 检查Python版本 (需要3.8+)
python --version

# 安装依赖
pip install -r backend/intelligent_mbt_testing/requirements_service.txt

# 检查端口占用
netstat -an | grep 8080
```

#### 2. 前端启动失败
```bash
# 检查Node.js版本
node --version
npm --version

# 清理并重新安装
cd front
rm -rf node_modules package-lock.json
npm install
```

#### 3. WebSocket连接失败
- 确保后端服务正常运行
- 检查防火墙设置
- 确认端口8080可访问

#### 4. 文档上传失败
- 检查文件格式 (仅支持.doc/.docx/.pdf/.txt)
- 检查文件大小 (不超过10MB)
- 确认网络连接正常

### 日志查看
```bash
# 后端日志
tail -f backend/intelligent_mbt_testing/enhanced_workspace/logs/agentscope.log

# 前端日志
# 查看浏览器开发者工具Console
```

## 📞 技术支持

### 系统要求
- **Python**: 3.8+
- **Node.js**: 14+
- **内存**: 4GB+
- **磁盘**: 2GB+

### 开发环境
- **IDE**: VSCode, PyCharm
- **浏览器**: Chrome, Firefox, Safari, Edge
- **操作系统**: Windows, macOS, Linux

### 联系方式
- **技术文档**: 查看项目README
- **问题反馈**: 提交GitHub Issues
- **功能建议**: 联系开发团队

---

## 🎉 开始使用

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd AITestHub
   ```

2. **一键启动**
   ```bash
   python start_multi_agent_system.py
   ```

3. **访问系统**
   ```
   http://localhost:3000/dashboard
   ```

4. **开始协作**
   - 点击"多Agent智能调度"
   - 上传测试文档
   - 观察实时执行过程

**🚀 享受多Agent智能协作的强大能力！**
