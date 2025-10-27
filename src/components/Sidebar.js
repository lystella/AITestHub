import React, { useMemo } from 'react';
import { Layout, Menu } from 'antd';
import { 
  DashboardOutlined, 
  FileTextOutlined, 
  EditOutlined, 
  SettingOutlined, 
  PlayCircleOutlined, 
  ThunderboltOutlined, 
  SafetyOutlined 
} from '@ant-design/icons';
import { useLocation, useNavigate } from 'react-router-dom';

const { Sider } = Layout;

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const selectedKey = useMemo(() => {
    if (location.pathname.startsWith('/ai/requirement')) return 'requirement-analysis';
    if (location.pathname.startsWith('/dashboard')) return 'dashboard';
    return 'dashboard';
  }, [location.pathname]);

  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: '测试仪表盘',
      onClick: () => navigate('/dashboard')
    },
    {
      type: 'divider',
    },
    {
      key: 'ai-functions',
      label: 'AI测试功能',
      type: 'group',
      children: [
        {
          key: 'requirement-analysis',
          icon: <FileTextOutlined />,
          label: 'AI需求分析',
          onClick: () => navigate('/ai/requirement')
        },
        {
          key: 'test-design',
          icon: <EditOutlined />,
          label: 'AI测试设计',
        },
        {
          key: 'data-generation',
          icon: <SettingOutlined />,
          label: 'AI数据生成',
        },
        {
          key: 'test-execution',
          icon: <PlayCircleOutlined />,
          label: 'AI测试执行',
        },
        {
          key: 'performance-test',
          icon: <ThunderboltOutlined />,
          label: 'AI性能测试',
        },
        {
          key: 'security-test',
          icon: <SafetyOutlined />,
          label: 'AI安全测试',
        },
      ],
    },
  ];

  return (
    <Sider 
      width={240} 
      style={{ 
        background: '#fff',
        boxShadow: '2px 0 8px rgba(0, 0, 0, 0.1)'
      }}
    >
      <div style={{ padding: '24px 0' }}>
        <Menu
          mode="inline"
          selectedKeys={[selectedKey]}
          style={{ 
            border: 'none',
            background: 'transparent'
          }}
          items={menuItems}
        />
      </div>
    </Sider>
  );
};

export default Sidebar;