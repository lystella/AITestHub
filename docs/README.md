# 🚀 增强型智能测试系统

基于**AgentScope框架**的企业级智能测试平台，6个智能体协作完成复杂测试任务。

## 🎯 核心特性

- **🧠 6个智能体协作**: 协调、分析、规划、数据、执行、报告
- **📊 完整的AgentScope集成**: 精确协作、状态管理、错误恢复
- **⚡ 多种运行模式**: 命令行、守护进程、Web服务
- **📈 企业级可靠性**: 检查点机制、自动恢复、完整日志

## 🚀 快速开始

### 命令行模式 (推荐)
```bash
# 查看系统状态
python command_runner.py status

# 执行测试
python command_runner.py test ui
python command_runner.py test api

# 查看帮助
python command_runner.py help
```

### 守护进程模式
```bash
# 长期运行，自动执行测试
python simple_daemon.py
```

### Web服务模式
```bash
# 安装依赖
pip install -r requirements_service.txt

# 启动Web服务
python start_service.py --mode web --port 8080

# 访问 http://127.0.0.1:8080
```

## 🤖 智能体团队

1. **CoordinatorAgent** - 协调专家：资源管理和任务调度
2. **AnalysisAgent** - 分析专家：需求分析和策略制定  
3. **PlannerAgent** - 规划专家：测试计划生成和优化
4. **DataAgent** - 数据专家：测试数据管理和生成
5. **ExecutorAgent** - 执行专家：自动化测试执行
6. **ReporterAgent** - 报告专家：测试报告生成和分析

## 📁 核心文件

- `command_runner.py` - 命令行工具 ⭐ 推荐使用
- `simple_daemon.py` - 守护进程 ⭐ 长期运行
- `enhanced_intelligent_testing_system.py` - 主系统文件
- `enhanced_config.py` - 系统配置
- `web_service.py` - Web服务接口

## 📊 监控和日志

- **日志**: `enhanced_workspace/logs/`
- **检查点**: `enhanced_workspace/checkpoints/`
- **恢复数据**: `recovery/`

## 🔧 配置

API密钥已预配置。如需修改，编辑 `enhanced_config.py` 文件。

## 📖 详细文档

- `USAGE.md` - 详细使用指南
- `SERVICE_USAGE.md` - Web服务说明

---

**版本**: 1.0.0 | **框架**: AgentScope | **更新**: 2025-09-19