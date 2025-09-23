import React from 'react';
import { Card, Typography, Tag } from 'antd';
import { 
  BulbOutlined, 
  EditOutlined, 
  DatabaseOutlined, 
  RocketOutlined, 
  BarChartOutlined, 
  SafetyOutlined, 
  SettingOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  PlayCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';

const { Text } = Typography;

const FunctionCard = ({ 
  title, 
  description, 
  icon, 
  status, 
  statusText, 
  iconColor 
}) => {
  const getStatusIcon = () => {
    switch (status) {
      case 'ready':
        return <CheckCircleOutlined />;
      case 'progress':
        return <ClockCircleOutlined />;
      case 'running':
        return <PlayCircleOutlined />;
      case 'config':
        return <ExclamationCircleOutlined />;
      default:
        return <CheckCircleOutlined />;
    }
  };

  const getStatusClass = () => {
    switch (status) {
      case 'ready':
        return 'status-ready';
      case 'progress':
        return 'status-progress';
      case 'running':
        return 'status-running';
      case 'config':
        return 'status-config';
      default:
        return 'status-ready';
    }
  };

  return (
    <Card 
      className="function-card"
      hoverable
      style={{ 
        borderRadius: '12px',
        border: 'none',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
      }}
    >
      <div className="card-header">
        <div 
          className="card-icon" 
          style={{ backgroundColor: iconColor }}
        >
          {icon}
        </div>
        <div>
          <h3 className="card-title">{title}</h3>
        </div>
      </div>
      
      <Text className="card-description">
        {description}
      </Text>
      
      <div>
        <Tag 
          className={`status-badge ${getStatusClass()}`}
          icon={getStatusIcon()}
        >
          {statusText}
        </Tag>
      </div>
    </Card>
  );
};

export default FunctionCard;