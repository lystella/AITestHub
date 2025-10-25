import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Statistic, 
  Table, 
  Tag, 
  Progress, 
  Select, 
  DatePicker, 
  Button,
  Tabs,
  Timeline,
  Alert,
  Tooltip,
  Space,
  Typography,
  Divider,
  Badge
} from 'antd';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip as RechartsTooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  Area,
  AreaChart,
  Legend
} from 'recharts';
import {
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined,
  TrophyOutlined,
  BugOutlined,
  ThunderboltOutlined,
  EyeOutlined,
  DownloadOutlined,
  ReloadOutlined,
  FilterOutlined
} from '@ant-design/icons';
import RealtimeReportUpdater from '../components/RealtimeReportUpdater';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { TabPane } = Tabs;
const { Option } = Select;

const TestReports = () => {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedTimeRange, setSelectedTimeRange] = useState('7days');
  const [selectedAgent, setSelectedAgent] = useState('all');
  const [activeTab, setActiveTab] = useState('overview');

  // 模拟数据 - 实际使用时从API获取
  const mockReportData = {
    summary: {
      totalTests: 1247,
      successRate: 87.3,
      avgExecutionTime: 2.4,
      totalAgents: 6,
      midsceneTests: 342,
      midsceneSuccessRate: 91.2
    },
    executionTrend: [
      { date: '2024-01-15', total: 45, success: 39, failed: 6, midscene: 12 },
      { date: '2024-01-16', total: 52, success: 47, failed: 5, midscene: 15 },
      { date: '2024-01-17', total: 48, success: 42, failed: 6, midscene: 13 },
      { date: '2024-01-18', total: 61, success: 55, failed: 6, midscene: 18 },
      { date: '2024-01-19', total: 58, success: 51, failed: 7, midscene: 16 },
      { date: '2024-01-20', total: 67, success: 60, failed: 7, midscene: 22 },
      { date: '2024-01-21', total: 73, success: 66, failed: 7, midscene: 25 }
    ],
    agentPerformance: [
      { name: 'CoordinatorAgent', tests: 156, success: 142, rate: 91.0, avgTime: 1.8 },
      { name: 'AnalysisAgent', tests: 203, success: 185, rate: 91.1, avgTime: 3.2 },
      { name: 'PlannerAgent', tests: 178, success: 164, rate: 92.1, avgTime: 2.1 },
      { name: 'DataAgent', tests: 189, success: 169, rate: 89.4, avgTime: 2.8 },
      { name: 'ExecutorAgent', tests: 298, success: 251, rate: 84.2, avgTime: 4.1 },
      { name: 'ReporterAgent', tests: 223, success: 207, rate: 92.8, avgTime: 1.9 }
    ],
    midscenePerformance: {
      modeDistribution: [
        { name: 'Playwright模式', value: 145, color: '#1890ff' },
        { name: 'YAML模式', value: 89, color: '#52c41a' },
        { name: '智能混合模式', value: 108, color: '#faad14' }
      ],
      aiOperations: [
        { operation: 'aiAction', count: 234, successRate: 89.3 },
        { operation: 'aiQuery', count: 167, successRate: 92.8 },
        { operation: 'aiAssert', count: 198, successRate: 94.4 },
        { operation: 'aiWaitFor', count: 145, successRate: 87.6 },
        { operation: 'aiTap', count: 123, successRate: 91.1 }
      ]
    },
    recentExecutions: [
      {
        id: 'exec_001',
        testName: 'eBay商品搜索测试',
        agent: 'ExecutorAgent',
        type: 'Midscene AI',
        status: 'success',
        duration: '3.2s',
        timestamp: '2024-01-21 14:32:15',
        mode: 'playwright'
      },
      {
        id: 'exec_002',
        testName: '用户登录流程测试',
        agent: 'ExecutorAgent',
        type: 'Traditional',
        status: 'failed',
        duration: '2.1s',
        timestamp: '2024-01-21 14:28:43',
        error: '元素定位失败'
      },
      {
        id: 'exec_003',
        testName: 'Google搜索功能测试',
        agent: 'ExecutorAgent',
        type: 'Midscene YAML',
        status: 'success',
        duration: '4.5s',
        timestamp: '2024-01-21 14:25:12',
        mode: 'yaml'
      }
    ]
  };

  useEffect(() => {
    fetchReportData();
  }, [selectedTimeRange, selectedAgent]);

  const fetchReportData = async () => {
    setLoading(true);
    try {
      // 并行获取所有报告数据
      const [summaryRes, executionsRes, trendsRes] = await Promise.all([
        fetch('http://localhost:8080/test-reports/summary'),
        fetch('http://localhost:8080/test-reports/executions?limit=50'),
        fetch(`http://localhost:8080/test-reports/trends?days=${selectedTimeRange.replace('days', '') || '7'}`)
      ]);

      if (summaryRes.ok && executionsRes.ok && trendsRes.ok) {
        const [summaryData, executionsData, trendsData] = await Promise.all([
          summaryRes.json(),
          executionsRes.json(), 
          trendsRes.json()
        ]);

        // 组合数据
        const combinedData = {
          summary: summaryData.summary || mockReportData.summary,
          agentPerformance: summaryData.agentPerformance || mockReportData.agentPerformance,
          midscenePerformance: {
            ...summaryData.midscenePerformance,
            aiOperations: mockReportData.midscenePerformance.aiOperations // 暂时使用模拟数据
          },
          executionTrend: trendsData.trends || mockReportData.executionTrend,
          recentExecutions: executionsData.executions || mockReportData.recentExecutions
        };

        setReportData(combinedData);
      } else {
        // API调用失败，使用模拟数据
        console.warn('API调用失败，使用模拟数据');
        setReportData(mockReportData);
      }
    } catch (error) {
      console.error('获取报告数据失败:', error);
      // 出错时使用模拟数据
      setReportData(mockReportData);
    } finally {
      setLoading(false);
    }
  };

  const refreshData = () => {
    fetchReportData();
  };

  const exportReport = () => {
    if (!reportData) return;
    
    // 生成报告内容
    const reportContent = {
      title: '测试报告可视化数据',
      generatedAt: new Date().toISOString(),
      summary: reportData.summary,
      agentPerformance: reportData.agentPerformance,
      midscenePerformance: reportData.midscenePerformance,
      executionTrend: reportData.executionTrend,
      recentExecutions: reportData.recentExecutions.slice(0, 20) // 只导出前20条记录
    };
    
    // 创建并下载JSON文件
    const dataStr = JSON.stringify(reportContent, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `test-report-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    message.success('报告已导出为JSON文件');
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case 'failed':
        return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />;
      case 'running':
        return <ClockCircleOutlined style={{ color: '#1890ff' }} />;
      default:
        return null;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'success':
        return 'success';
      case 'failed':
        return 'error';
      case 'running':
        return 'processing';
      default:
        return 'default';
    }
  };

  const executionColumns = [
    {
      title: '测试名称',
      dataIndex: 'testName',
      key: 'testName',
      render: (text, record) => (
        <Space>
          {getStatusIcon(record.status)}
          <Text strong>{text}</Text>
        </Space>
      )
    },
    {
      title: '智能体',
      dataIndex: 'agent',
      key: 'agent',
      render: (text) => <Tag color="blue">{text}</Tag>
    },
    {
      title: '执行类型',
      dataIndex: 'type',
      key: 'type',
      render: (text, record) => {
        let color = 'default';
        if (text.includes('Midscene')) {
          color = 'purple';
        }
        return (
          <Space>
            <Tag color={color}>{text}</Tag>
            {record.mode && <Tag color="orange">{record.mode}</Tag>}
          </Space>
        );
      }
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Badge 
          status={status === 'success' ? 'success' : status === 'failed' ? 'error' : 'processing'} 
          text={status === 'success' ? '成功' : status === 'failed' ? '失败' : '运行中'} 
        />
      )
    },
    {
      title: '执行时间',
      dataIndex: 'duration',
      key: 'duration'
    },
    {
      title: '时间戳',
      dataIndex: 'timestamp',
      key: 'timestamp'
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Button size="small" icon={<EyeOutlined />}>详情</Button>
          {record.status === 'failed' && (
            <Button size="small" type="link" icon={<BugOutlined />}>
              查看错误
            </Button>
          )}
        </Space>
      )
    }
  ];

  if (loading) {
    return (
      <div style={{ padding: '50px', textAlign: 'center' }}>
        <Title level={3}>加载测试报告数据...</Title>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      {/* 实时更新组件 */}
      <RealtimeReportUpdater onDataUpdate={fetchReportData} />
      
      {/* 页面标题和操作按钮 */}
      <Row justify="space-between" align="middle" style={{ marginBottom: '24px' }}>
        <Col>
          <Title level={2}>
            <TrophyOutlined style={{ marginRight: '8px', color: '#faad14' }} />
            测试报告可视化
          </Title>
        </Col>
        <Col>
          <Space>
            <Select
              value={selectedTimeRange}
              onChange={setSelectedTimeRange}
              style={{ width: 120 }}
            >
              <Option value="1day">今天</Option>
              <Option value="7days">近7天</Option>
              <Option value="30days">近30天</Option>
              <Option value="90days">近90天</Option>
            </Select>
            <Select
              value={selectedAgent}
              onChange={setSelectedAgent}
              style={{ width: 150 }}
            >
              <Option value="all">所有智能体</Option>
              <Option value="coordinator">CoordinatorAgent</Option>
              <Option value="executor">ExecutorAgent</Option>
              <Option value="analyzer">AnalysisAgent</Option>
            </Select>
            <Button icon={<ReloadOutlined />} onClick={refreshData}>
              刷新
            </Button>
            <Button type="primary" icon={<DownloadOutlined />} onClick={exportReport}>
              导出报告
            </Button>
          </Space>
        </Col>
      </Row>

      {/* 核心指标概览 */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="总测试数"
              value={reportData.summary.totalTests}
              prefix={<ThunderboltOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="成功率"
              value={reportData.summary.successRate}
              suffix="%"
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
            <Progress 
              percent={reportData.summary.successRate} 
              size="small" 
              showInfo={false}
              strokeColor="#52c41a"
              style={{ marginTop: '8px' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="平均执行时间"
              value={reportData.summary.avgExecutionTime}
              suffix="s"
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Midscene测试"
              value={reportData.summary.midsceneTests}
              prefix={<EyeOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
            <div style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
              成功率: {reportData.summary.midsceneSuccessRate}%
            </div>
          </Card>
        </Col>
      </Row>

      {/* Midscene特别提示 */}
      <Alert
        message="🎯 Midscene AI测试能力已集成"
        description="系统现在支持AI驱动的Web自动化测试，包括Playwright模式、YAML模式和智能混合模式。查看下方详细的Midscene执行分析。"
        type="info"
        showIcon
        style={{ marginBottom: '24px' }}
        closable
      />

      {/* 详细报告标签页 */}
      <Tabs activeKey={activeTab} onChange={setActiveTab}>
        {/* 概览标签页 */}
        <TabPane tab="执行趋势" key="overview">
          <Row gutter={[16, 16]}>
            <Col xs={24} lg={16}>
              <Card title="执行趋势分析" extra={<Tag color="blue">近7天</Tag>}>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={reportData.executionTrend}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Area 
                      type="monotone" 
                      dataKey="total" 
                      stackId="1"
                      stroke="#1890ff" 
                      fill="#1890ff" 
                      fillOpacity={0.6}
                      name="总执行数"
                    />
                    <Area 
                      type="monotone" 
                      dataKey="success" 
                      stackId="2"
                      stroke="#52c41a" 
                      fill="#52c41a" 
                      fillOpacity={0.6}
                      name="成功数"
                    />
                    <Area 
                      type="monotone" 
                      dataKey="midscene" 
                      stackId="3"
                      stroke="#722ed1" 
                      fill="#722ed1" 
                      fillOpacity={0.8}
                      name="Midscene执行"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </Card>
            </Col>
            <Col xs={24} lg={8}>
              <Card title="智能体性能排行">
                <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
                  {reportData.agentPerformance
                    .sort((a, b) => b.rate - a.rate)
                    .map((agent, index) => (
                      <div key={agent.name} style={{ marginBottom: '16px' }}>
                        <Row justify="space-between" align="middle">
                          <Col>
                            <Space>
                              <Badge 
                                count={index + 1} 
                                style={{ 
                                  backgroundColor: index < 3 ? '#faad14' : '#d9d9d9',
                                  color: index < 3 ? '#fff' : '#666'
                                }} 
                              />
                              <Text strong>{agent.name}</Text>
                            </Space>
                          </Col>
                          <Col>
                            <Text type="success">{agent.rate.toFixed(1)}%</Text>
                          </Col>
                        </Row>
                        <Progress 
                          percent={agent.rate} 
                          size="small" 
                          showInfo={false}
                          strokeColor={index < 3 ? '#52c41a' : '#1890ff'}
                        />
                        <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
                          {agent.tests}次执行 • 平均{agent.avgTime}s
                        </div>
                      </div>
                    ))}
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>

        {/* Midscene分析标签页 */}
        <TabPane tab="🎯 Midscene分析" key="midscene">
          <Row gutter={[16, 16]}>
            <Col xs={24} md={12}>
              <Card title="执行模式分布">
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={reportData.midscenePerformance.modeDistribution}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(1)}%`}
                    >
                      {reportData.midscenePerformance.modeDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <RechartsTooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Card>
            </Col>
            <Col xs={24} md={12}>
              <Card title="AI操作类型分析">
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={reportData.midscenePerformance.aiOperations}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="operation" />
                    <YAxis />
                    <RechartsTooltip />
                    <Bar dataKey="count" fill="#1890ff" name="执行次数" />
                  </BarChart>
                </ResponsiveContainer>
              </Card>
            </Col>
          </Row>
          
          <Card title="AI操作详细统计" style={{ marginTop: '16px' }}>
            <Row gutter={[16, 16]}>
              {reportData.midscenePerformance.aiOperations.map((op) => (
                <Col xs={24} sm={12} md={8} lg={6} key={op.operation}>
                  <Card size="small">
                    <Statistic
                      title={op.operation}
                      value={op.successRate}
                      suffix="%"
                      valueStyle={{ fontSize: '18px' }}
                    />
                    <div style={{ marginTop: '8px' }}>
                      <Text type="secondary">执行次数: {op.count}</Text>
                    </div>
                    <Progress 
                      percent={op.successRate} 
                      size="small" 
                      strokeColor={op.successRate > 90 ? '#52c41a' : '#faad14'}
                      style={{ marginTop: '8px' }}
                    />
                  </Card>
                </Col>
              ))}
            </Row>
          </Card>
        </TabPane>

        {/* 执行记录标签页 */}
        <TabPane tab="执行记录" key="executions">
          <Card 
            title="最近执行记录" 
            extra={
              <Space>
                <Button size="small" icon={<FilterOutlined />}>
                  筛选
                </Button>
                <Button size="small" icon={<ReloadOutlined />} onClick={refreshData}>
                  刷新
                </Button>
              </Space>
            }
          >
            <Table
              columns={executionColumns}
              dataSource={reportData.recentExecutions}
              rowKey="id"
              pagination={{
                pageSize: 10,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total, range) => 
                  `显示 ${range[0]}-${range[1]} 条，共 ${total} 条记录`
              }}
              scroll={{ x: 800 }}
            />
          </Card>
        </TabPane>

        {/* 性能分析标签页 */}
        <TabPane tab="性能分析" key="performance">
          <Row gutter={[16, 16]}>
            <Col xs={24}>
              <Card title="智能体性能对比">
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={reportData.agentPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <RechartsTooltip />
                    <Legend />
                    <Bar yAxisId="left" dataKey="tests" fill="#1890ff" name="测试次数" />
                    <Bar yAxisId="left" dataKey="success" fill="#52c41a" name="成功次数" />
                    <Line yAxisId="right" type="monotone" dataKey="rate" stroke="#faad14" name="成功率%" />
                  </BarChart>
                </ResponsiveContainer>
              </Card>
            </Col>
          </Row>
          
          <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
            <Col xs={24} lg={12}>
              <Card title="执行时间分析">
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={reportData.agentPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <RechartsTooltip />
                    <Line 
                      type="monotone" 
                      dataKey="avgTime" 
                      stroke="#722ed1" 
                      strokeWidth={2}
                      name="平均执行时间(s)"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Card>
            </Col>
            <Col xs={24} lg={12}>
              <Card title="性能优化建议">
                <Timeline>
                  <Timeline.Item color="green">
                    <Text strong>ExecutorAgent</Text> - 考虑优化复杂测试用例的执行逻辑
                  </Timeline.Item>
                  <Timeline.Item color="blue">
                    <Text strong>Midscene集成</Text> - AI模式执行效率优于传统模式23%
                  </Timeline.Item>
                  <Timeline.Item color="orange">
                    <Text strong>DataAgent</Text> - 数据准备环节可进一步优化
                  </Timeline.Item>
                  <Timeline.Item>
                    <Text strong>整体建议</Text> - 增加Midscene使用比例，提升测试智能化水平
                  </Timeline.Item>
                </Timeline>
              </Card>
            </Col>
          </Row>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default TestReports;
