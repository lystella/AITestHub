# 增强型智能测试系统 - 长期运行服务

## 🚀 快速启动

### 方法1: 交互式服务模式 (推荐)
```bash
# 启动交互式服务
python start_service.py --mode interactive

# 或者直接运行
python service_mode.py
```

### 方法2: Web服务模式
```bash
# 安装Web服务依赖
pip install -r requirements_service.txt

# 启动Web服务
python start_service.py --mode web --host 127.0.0.1 --port 8080

# 或者直接运行
python web_service.py
```

### 方法3: 演示模式
```bash
# 运行单次演示
python start_service.py --mode demo
```

## 📋 服务功能

### 🤖 智能体协作
- **协调专家**: 全局资源协调和任务调度
- **分析专家**: 深度需求分析和测试策略制定
- **规划专家**: 智能测试计划生成和优化
- **数据专家**: 测试数据管理和生成
- **执行专家**: 自动化测试执行和监控
- **报告专家**: 智能测试报告生成和分析

### 🔧 支持的测试类型
- `ui_testing`: UI自动化测试
- `api_testing`: API接口测试
- `performance_testing`: 性能测试
- `integration_testing`: 集成测试

## ⌨️ 交互式命令

### 基础命令
- `status` - 查看服务状态和统计信息
- `test <type>` - 执行指定类型的测试
- `quit` - 优雅退出服务
- `help` - 显示帮助信息

### 测试命令示例
```bash
# UI测试
test ui_testing

# API测试
test api_testing

# 性能测试
test performance_testing

# 集成测试
test integration_testing
```

## 🌐 Web界面使用

启动Web服务后，访问以下地址：

- **测试界面**: http://127.0.0.1:8080/
- **API文档**: http://127.0.0.1:8080/docs
- **系统状态**: http://127.0.0.1:8080/status
- **健康检查**: http://127.0.0.1:8080/health

### API调用示例

#### 执行测试 (POST /test)
```json
{
  "test_type": "ui_testing",
  "tasks": [
    {"task": "分析测试需求"},
    {"task": "生成测试用例"},
    {"task": "执行自动化测试"}
  ],
  "params": {
    "timeout": 30,
    "retry": 3
  }
}
```

#### 响应示例
```json
{
  "success": true,
  "request_id": "web_1695123456",
  "result": {
    "workflow_results": {...},
    "execution_summary": {...}
  },
  "timestamp": "2025-09-19T11:30:56.789123"
}
```

## 📊 系统监控

### 服务状态指标
- 运行时间
- 处理请求总数
- 成功/失败请求数
- 智能体健康状态
- 系统性能指标

### 日志和检查点
- **日志目录**: `enhanced_workspace/logs/`
- **检查点目录**: `enhanced_workspace/checkpoints/`
- **服务统计**: `enhanced_workspace/service_stats.json`

## 🔧 配置选项

### 环境变量
```bash
# API密钥 (必需)
export DASHSCOPE_API_KEY="your-api-key"

# 可选配置
export AGENTSCOPE_LOGGING_LEVEL="INFO"
export AGENTSCOPE_WORKSPACE="enhanced_workspace"
```

### 服务配置
- **默认主机**: 127.0.0.1
- **默认端口**: 8080
- **自动保存间隔**: 300秒
- **请求超时**: 30秒

## 🛠️ 故障排除

### 常见问题

1. **系统初始化失败**
   ```bash
   # 检查API密钥
   echo $DASHSCOPE_API_KEY
   
   # 检查网络连接
   ping dashscope.aliyuncs.com
   ```

2. **Web服务启动失败**
   ```bash
   # 安装依赖
   pip install -r requirements_service.txt
   
   # 检查端口占用
   netstat -an | findstr :8080
   ```

3. **智能体响应异常**
   - 检查日志文件: `enhanced_workspace/logs/agentscope.log`
   - 查看检查点: `enhanced_workspace/checkpoints/`
   - 重启服务恢复状态

### 性能优化

1. **内存使用优化**
   - 定期清理历史记录
   - 调整检查点保存频率
   - 使用轻量级模型

2. **并发处理优化**
   - 调整智能体数量
   - 配置合适的超时时间
   - 使用负载均衡

## 📈 扩展功能

### 自定义测试类型
可以通过修改配置文件添加新的测试类型和工作流。

### 集成其他系统
支持通过API接口与CI/CD系统、测试管理平台等集成。

### 分布式部署
支持多节点部署，提高并发处理能力。

## 🔒 安全注意事项

1. **API密钥安全**
   - 不要在代码中硬编码API密钥
   - 使用环境变量或配置文件
   - 定期轮换API密钥

2. **网络安全**
   - 在生产环境中配置HTTPS
   - 使用防火墙限制访问
   - 配置适当的认证机制

## 📞 技术支持

如有问题，请检查：
1. 系统日志文件
2. 服务状态接口
3. AgentScope官方文档
4. GitHub Issues

---

**版本**: 1.0.0  
**更新时间**: 2025-09-19  
**兼容性**: AgentScope 0.0.5+
