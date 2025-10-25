import React from 'react';
import { BulbOutlined, EditOutlined, DatabaseOutlined, RocketOutlined, BarChartOutlined, SafetyOutlined, SettingOutlined } from '@ant-design/icons';
import FunctionCard from './FunctionCard';

const Dashboard = () => {
  const functionCards = [
    {
      key: 'requirement',
      title: 'AI需求分析',
      description: '智能解析需求文档,生成测试要点',
      icon: <BulbOutlined />,
      status: 'ready',
      statusText: '就绪',
      iconColor: '#1890ff'
    },
    {
      title: 'AI测试设计',
      description: '自动创建测试用例,覆盖核心场景',
      icon: <EditOutlined />,
      status: 'progress',
      statusText: '进行中',
      iconColor: '#722ed1'
    },
    {
      title: 'AI数据生成',
      description: '智能生成测试数据,保障数据质量',
      icon: <DatabaseOutlined />,
      status: 'ready',
      statusText: '就绪',
      iconColor: '#52c41a'
    },
    {
      title: 'AI测试执行',
      description: '智能执行测试,实时反馈结果',
      icon: <RocketOutlined />,
      status: 'running',
      statusText: '运行中',
      iconColor: '#1890ff'
    },
    {
      title: 'AI性能测试',
      description: '模拟高并发场景,定位性能瓶颈',
      icon: <BarChartOutlined />,
      status: 'ready',
      statusText: '就绪',
      iconColor: '#fa8c16'
    },
    {
      title: 'AI安全测试',
      description: '自动扫描漏洞,保障应用安全',
      icon: <SafetyOutlined />,
      status: 'config',
      statusText: '需配置',
      iconColor: '#ff4d4f'
    },
    {
      key: 'multi-agent',
      title: '多Agent智能调度',
      description: '智能识别需求并调用多Agent进行测试执行',
      icon: <SettingOutlined />,
      status: 'ready',
      statusText: '就绪',
      iconColor: '#722ed1'
    }
  ];

  return (
    <div>
      <div className="function-cards">
        {functionCards.map((card, index) => (
          <div key={card.key || index} onClick={() => {
            if (card.key === 'requirement') {
              window.location.href = '/ai/requirement';
            } else if (card.key === 'multi-agent') {
              window.location.href = '/ai/multi-agent';
            }
          }}>
            <FunctionCard
              title={card.title}
              description={card.description}
              icon={card.icon}
              status={card.status}
              statusText={card.statusText}
              iconColor={card.iconColor}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;