# 增强型智能测试系统 - 使用指南

## 🚀 快速开始

### 1. 命令行模式 (推荐)
```bash
# 查看系统状态
python command_runner.py status

# 执行测试
python command_runner.py test ui        # UI测试
python command_runner.py test api       # API测试
python command_runner.py test performance # 性能测试

# 查看帮助
python command_runner.py help
```

### 2. 守护进程模式 (长期运行)
```bash
# 启动守护进程，自动定期执行测试
python simple_daemon.py
```

### 3. 交互式模式 (修复版)
```bash
# 方式1: 修复版交互式服务
python interactive_service.py

# 方式2: 简化菜单式交互
python test_interactive.py

# 方式3: 通过启动脚本
python start_service.py --mode interactive
```

### 4. Web服务模式
```bash
# 安装依赖
pip install -r requirements_service.txt

# 启动Web服务
python start_service.py --mode web --port 8080

# 访问 http://127.0.0.1:8080
```

## 📁 核心文件说明

### 主要文件
- `enhanced_intelligent_testing_system.py` - 主系统文件
- `enhanced_config.py` - 系统配置
- `model_config.py` - 模型配置
- `command_runner.py` - 命令行运行器 ⭐
- `simple_daemon.py` - 守护进程 ⭐

### 可选文件
- `web_service.py` - Web服务接口
- `interactive_service.py` - 交互式服务 (修复版)
- `test_interactive.py` - 简化交互式测试
- `start_service.py` - 统一启动脚本

### 目录
- `enhanced_agents/` - 6个核心智能体
- `enhanced_workspace/` - 工作空间（日志、检查点）
- `tools/` - 工具函数

## 🤖 智能体功能

1. **CoordinatorAgent** - 协调专家：资源管理和任务调度
2. **AnalysisAgent** - 分析专家：需求分析和策略制定  
3. **PlannerAgent** - 规划专家：测试计划生成和优化
4. **DataAgent** - 数据专家：测试数据管理和生成
5. **ExecutorAgent** - 执行专家：自动化测试执行
6. **ReporterAgent** - 报告专家：测试报告生成和分析

## ⚙️ 配置

API密钥已预设为：`sk-343983e4232340128017e03e90f79070`

如需修改，编辑 `enhanced_config.py` 文件。

## 📊 监控

- 日志：`enhanced_workspace/logs/`
- 检查点：`enhanced_workspace/checkpoints/`
- 恢复数据：`recovery/`

## 🆘 故障排除

1. **初始化失败**：检查网络连接和API密钥
2. **智能体无响应**：查看日志文件排查错误
3. **Web服务启动失败**：安装依赖 `pip install -r requirements_service.txt`

## 📞 支持

详细文档请参考：
- `SERVICE_USAGE.md` - Web服务详细说明
- `README.md` - 系统概述

---
**版本**: 1.0.0 | **更新**: 2025-09-19
