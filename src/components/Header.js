import React from 'react';
import { Layout, Typography, Space, Button, Dropdown } from 'antd';
import { BellOutlined, UserOutlined, DownOutlined } from '@ant-design/icons';

const { Header: AntHeader } = Layout;
const { Text } = Typography;

const Header = () => {
  const projectMenuItems = [
    {
      key: '1',
      label: 'AI测试项目',
    },
    {
      key: '2',
      label: '金融服务系统',
    },
    {
      key: '3',
      label: '电商平台测试',
    },
  ];

  return (
    <AntHeader style={{ 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'space-between',
      padding: '0 24px',
      background: '#fff',
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
    }}>

      {/* 中间标题 */}
      <div style={{ flex: 1, textAlign: 'center' }}>
        <Text style={{ fontSize: '20px', fontWeight: '600', color: '#262626' }}>
          AI测试平台
        </Text>
      </div>

      {/* 右侧导航和操作 */}
      <div className="header-actions">
        <Space size="large">
          <a href="#" className="nav-link">测试仪表盘</a>
          <a href="#" className="nav-link">帮助支持</a>
          
          <Button 
            type="text" 
            icon={<BellOutlined />} 
            size="large"
            style={{ color: '#8c8c8c' }}
          />
          
          <Button 
            type="text" 
            icon={<UserOutlined />} 
            size="large"
            style={{ color: '#8c8c8c' }}
          />
        </Space>
      </div>
    </AntHeader>
  );
};

export default Header;