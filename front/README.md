# AI测试平台

一个基于React和Ant Design的现代化AI测试平台首页。

## 功能特性

- 🎨 现代化的UI设计，基于Ant Design组件库
- 📱 响应式布局，适配不同屏幕尺寸
- 🚀 7个AI测试功能模块卡片展示
- 📊 实时状态显示（就绪、进行中、运行中、需配置）
- 🎯 直观的导航和操作界面

## 技术栈

- React 18
- Ant Design 5.x
- @ant-design/icons
- CSS3

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm start
```

项目将在 http://localhost:3000 启动

### 构建生产版本

```bash
npm run build
```

## 项目结构

```
src/
├── components/
│   ├── Header.js          # 顶部导航栏
│   ├── Sidebar.js         # 左侧边栏
│   ├── Dashboard.js       # 主仪表盘
│   └── FunctionCard.js    # 功能卡片组件
├── App.js                 # 主应用组件
├── index.js              # 应用入口
└── index.css             # 全局样式
```

## 功能模块

1. **AI需求分析** - 智能解析需求文档,生成测试要点
2. **AI测试设计** - 自动创建测试用例,覆盖核心场景
3. **AI数据生成** - 智能生成测试数据,保障数据质量
4. **AI测试执行** - 智能执行测试,实时反馈结果
5. **AI性能测试** - 模拟高并发场景,定位性能瓶颈
6. **AI安全测试** - 自动扫描漏洞,保障应用安全
7. **多Agent智能调度** - 智能识别需求并调用多Agent进行测试执行

## 浏览器支持

- Chrome >= 60
- Firefox >= 60
- Safari >= 12
- Edge >= 79