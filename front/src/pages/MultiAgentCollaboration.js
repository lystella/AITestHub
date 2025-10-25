import React, { useState, useEffect, useRef } from 'react';
import { 
  Upload, 
  Button, 
  Steps, 
  Card, 
  Typography, 
  message, 
  Progress, 
  Tag, 
  Divider,
  Space,
  Alert,
  Empty
} from 'antd';
import { 
  CloudUploadOutlined, 
  PlayCircleOutlined, 
  ReloadOutlined,
  CheckCircleOutlined,
  LoadingOutlined,
  FileTextOutlined,
  RobotOutlined,
  ThunderboltOutlined,
  BugOutlined,
  ClockCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Step } = Steps;
const { Dragger } = Upload;

const MultiAgentCollaboration = () => {
  // 状态管理
  const [currentStep, setCurrentStep] = useState(0);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [logs, setLogs] = useState([]);
  const [websocket, setWebsocket] = useState(null);
  const [workflowId, setWorkflowId] = useState(null);
  const [stepStatus, setStepStatus] = useState({
    coordination: 'wait',
    analysis: 'wait', 
    execution: 'wait'
  });
  const [progress, setProgress] = useState({ current: 0, total: 0, percentage: 0 });
  const [workflowComplete, setWorkflowComplete] = useState(false);
  const [stepResults, setStepResults] = useState({});

  const logContainerRef = useRef(null);

  // 读取文件内容的辅助函数
  const readFileContent = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = (e) => reject(e);
      reader.readAsText(file);
    });
  };

  // WebSocket连接管理
  useEffect(() => {
    if (workflowId && !websocket) {
      connectWebSocket();
    }
    
    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  }, [workflowId]);

  const connectWebSocket = () => {
    const wsUrl = `ws://localhost:8090/ws/${workflowId}`;
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      console.log('WebSocket连接已建立');
      setWebsocket(ws);
      
      // 发送心跳
      const heartbeat = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send('ping');
        } else {
          clearInterval(heartbeat);
        }
      }, 30000);
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      } catch (error) {
        console.error('解析WebSocket消息失败:', error);
      }
    };
    
    ws.onclose = () => {
      console.log('WebSocket连接关闭');
      setWebsocket(null);
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket错误:', error);
      message.error('WebSocket连接失败');
    };
  };

  const handleWebSocketMessage = (data) => {
    const { type, step_id, step_name, message: msg, level, agent_name, progress: progressData } = data;
    
    switch (type) {
      case 'connection_established':
        addLog('🔗 WebSocket连接已建立', 'success', 'System');
        break;
        
      case 'step_start':
        setStepStatus(prev => ({ ...prev, [step_id]: 'process' }));
        updateCurrentStep(step_id);
        addLog(`🚀 ${step_name}阶段开始`, 'info', 'System');
        break;
        
      case 'step_complete':
        setStepStatus(prev => ({ ...prev, [step_id]: 'finish' }));
        setStepResults(prev => ({ ...prev, [step_id]: data.result }));
        addLog(`✅ ${step_name}阶段完成`, 'success', 'System');
        break;
        
      case 'step_error':
        setStepStatus(prev => ({ ...prev, [step_id]: 'error' }));
        addLog(`❌ ${step_name}阶段失败: ${data.error}`, 'error', 'System');
        setIsProcessing(false);
        break;
        
      case 'log':
        addLog(msg, level || 'info', agent_name || 'System');
        break;
        
      case 'progress':
        setProgress({
          current: progressData.progress,
          total: progressData.total,
          percentage: progressData.percentage
        });
        addLog(`📊 进度更新: ${progressData.description} (${progressData.percentage}%)`, 'info', 'System');
        break;
        
      case 'workflow_complete':
        setWorkflowComplete(true);
        setIsProcessing(false);
        addLog('🎉 多Agent协作工作流执行完成！', 'success', 'System');
        message.success('工作流执行完成！');
        break;
        
      default:
        console.log('未处理的消息类型:', type, data);
    }
  };

  const updateCurrentStep = (stepId) => {
    const stepMapping = {
      'coordination': 0,
      'analysis': 1,
      'execution': 2
    };
    if (stepMapping[stepId] !== undefined) {
      setCurrentStep(stepMapping[stepId] + 1);
    }
  };

  const addLog = (message, type = 'info', agent = 'System') => {
    const newLog = {
      id: Date.now() + Math.random(),
      message,
      type,
      agent,
      timestamp: new Date().toLocaleTimeString()
    };
    
    setLogs(prev => [...prev, newLog]);
    
    // 自动滚动到底部
    setTimeout(() => {
      if (logContainerRef.current) {
        logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
      }
    }, 100);
  };

  const getLogIcon = (type) => {
    switch (type) {
      case 'success':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case 'error':
        return <ExclamationCircleOutlined style={{ color: '#ff4d4f' }} />;
      case 'warning':
        return <ExclamationCircleOutlined style={{ color: '#faad14' }} />;
      default:
        return <ClockCircleOutlined style={{ color: '#1890ff' }} />;
    }
  };

  const getAgentIcon = (agent) => {
    switch (agent) {
      case 'CoordinatorAgent':
        return <RobotOutlined style={{ color: '#722ed1' }} />;
      case 'AnalysisAgent':
        return <FileTextOutlined style={{ color: '#1890ff' }} />;
      case 'ExecutorAgent':
        return <ThunderboltOutlined style={{ color: '#52c41a' }} />;
      case 'PlannerAgent':
        return <BugOutlined style={{ color: '#faad14' }} />;
      default:
        return <RobotOutlined style={{ color: '#8c8c8c' }} />;
    }
  };

  const uploadProps = {
    name: 'file',
    multiple: false,
    showUploadList: false,
    accept: '.doc,.docx,.pdf,.txt',
    beforeUpload: (file) => {
      const isValidType = [
        'application/msword', 
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
        'application/pdf', 
        'text/plain'
      ].includes(file.type);
      
      if (!isValidType) {
        message.error('只支持 Word、PDF、TXT 格式文件！');
        return false;
      }
      
      const isLt10M = file.size / 1024 / 1024 < 10;
      if (!isLt10M) {
        message.error('文件大小不能超过 10MB！');
        return false;
      }
      
      setUploadedFile(file);
      message.success(`${file.name} 文件已选择`);
      return false; // 阻止自动上传
    }
  };

  const startAnalysis = async () => {
    if (!uploadedFile) {
      message.error('请先上传文档！');
      return;
    }

    setIsProcessing(true);
    setLogs([]);
    setCurrentStep(1);
    setWorkflowComplete(false);
    setStepResults({});
    setProgress({ current: 0, total: 0, percentage: 0 });

    try {
      // 读取文件内容
      const fileContent = await readFileContent(uploadedFile);
      
      // 启动增强测试工作流
      const response = await fetch('http://localhost:8090/enhanced-test-workflow', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_content: fileContent,
          file_name: uploadedFile.name,
          params: {
            document_size: uploadedFile.size,
            enable_streaming: true,
            collaboration_mode: 'enhanced'
          }
        })
      });

      const result = await response.json();
      
      if (result.success) {
        setWorkflowId(result.workflow_id);
        addLog('🚀 多Agent协作流程已启动...', 'success', 'System');
        addLog(`📋 工作流ID: ${result.workflow_id}`, 'info', 'System');
      } else {
        throw new Error(result.error || '启动流程失败');
      }
      
    } catch (error) {
      console.error('启动流程失败:', error);
      message.error('启动流程失败：' + error.message);
      setIsProcessing(false);
    }
  };

  const resetProcess = () => {
    // 关闭WebSocket连接
    if (websocket) {
      websocket.close();
      setWebsocket(null);
    }
    
    // 重置所有状态
    setCurrentStep(0);
    setIsProcessing(false);
    setUploadedFile(null);
    setLogs([]);
    setWorkflowId(null);
    setWorkflowComplete(false);
    setStepResults({});
    setProgress({ current: 0, total: 0, percentage: 0 });
    setStepStatus({
      coordination: 'wait',
      analysis: 'wait',
      execution: 'wait'
    });
    
    message.info('流程已重置');
  };

  const renderStepResult = (stepId) => {
    const result = stepResults[stepId];
    if (!result) return null;

    return (
      <div style={{ marginTop: '8px', padding: '8px', background: '#f6ffed', borderRadius: '4px', fontSize: '12px' }}>
        <Text type="secondary">
          {stepId === 'coordination' && `涉及智能体: ${result.agents_involved?.join(', ')}, 耗时: ${result.duration}`}
          {stepId === 'analysis' && `功能需求: ${result.functional_requirements}个, 非功能需求: ${result.non_functional_requirements}个`}
          {stepId === 'execution' && `测试用例: ${result.total_test_cases}个, 通过: ${result.passed}个, 失败: ${result.failed}个`}
        </Text>
      </div>
    );
  };

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: '32px', textAlign: 'center' }}>
        <Title level={2} style={{ marginBottom: '8px' }}>
          <RobotOutlined style={{ marginRight: '12px', color: '#722ed1' }} />
          多Agent智能协作
        </Title>
        <Paragraph type="secondary" style={{ fontSize: '16px' }}>
          基于AgentScope框架的6个专业智能体协作，实现智能化测试流程
        </Paragraph>
      </div>

      {/* 文档上传区域 */}
      {currentStep === 0 && (
        <Card 
          title={
            <Space>
              <FileTextOutlined />
              <span>文档上传</span>
            </Space>
          } 
          style={{ marginBottom: '24px' }}
        >
          <Dragger {...uploadProps} style={{ marginBottom: '24px' }}>
            <p className="ant-upload-drag-icon">
              <CloudUploadOutlined style={{ fontSize: '48px', color: '#1890ff' }} />
            </p>
            <p className="ant-upload-text" style={{ fontSize: '18px', fontWeight: 'bold' }}>
              点击或拖拽文件到此处上传
            </p>
            <p className="ant-upload-hint" style={{ fontSize: '14px' }}>
              支持 Word (.doc/.docx)、PDF (.pdf)、文本 (.txt) 格式<br/>
              文件大小不超过 10MB
            </p>
          </Dragger>
          
          {uploadedFile && (
            <Alert
              message="文件已选择"
              description={
                <Space direction="vertical" size={4}>
                  <Text strong>{uploadedFile.name}</Text>
                  <Text type="secondary">
                    大小: {(uploadedFile.size / 1024).toFixed(2)} KB | 
                    类型: {uploadedFile.type || '未知'}
                  </Text>
                </Space>
              }
              type="success"
              showIcon
              icon={<CheckCircleOutlined />}
              style={{ marginBottom: '24px' }}
            />
          )}
          
          <div style={{ textAlign: 'center' }}>
            <Button 
              type="primary" 
              size="large" 
              icon={<PlayCircleOutlined />}
              onClick={startAnalysis}
              disabled={!uploadedFile}
              style={{ height: '48px', fontSize: '16px', padding: '0 32px' }}
            >
              开始多Agent协作分析
            </Button>
          </div>
        </Card>
      )}

      {/* 流程执行区域 */}
      {currentStep > 0 && (
        <>
          {/* 执行进度 */}
          <Card 
            title={
              <Space>
                <ThunderboltOutlined />
                <span>执行进度</span>
                {isProcessing && <LoadingOutlined />}
              </Space>
            }
            style={{ marginBottom: '24px' }}
            extra={
              workflowComplete ? (
                <Tag color="success" icon={<CheckCircleOutlined />}>执行完成</Tag>
              ) : isProcessing ? (
                <Tag color="processing" icon={<LoadingOutlined />}>执行中</Tag>
              ) : (
                <Tag color="default">等待中</Tag>
              )
            }
          >
            <Steps 
              current={currentStep - 1} 
              status={isProcessing ? 'process' : workflowComplete ? 'finish' : 'wait'}
              style={{ marginBottom: '24px' }}
            >
              <Step 
                title="协调规划" 
                description="任务分解与资源调度"
                status={stepStatus.coordination}
                icon={stepStatus.coordination === 'process' ? <LoadingOutlined /> : undefined}
              />
              <Step 
                title="需求分析" 
                description="文档解析与需求提取"
                status={stepStatus.analysis}
                icon={stepStatus.analysis === 'process' ? <LoadingOutlined /> : undefined}
              />
              <Step 
                title="用例执行" 
                description="测试用例生成与执行"
                status={stepStatus.execution}
                icon={stepStatus.execution === 'process' ? <LoadingOutlined /> : undefined}
              />
            </Steps>

            {/* 显示步骤结果 */}
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px' }}>
              <div style={{ flex: 1 }}>
                <Text strong>协调规划</Text>
                {renderStepResult('coordination')}
              </div>
              <div style={{ flex: 1 }}>
                <Text strong>需求分析</Text>
                {renderStepResult('analysis')}
              </div>
              <div style={{ flex: 1 }}>
                <Text strong>用例执行</Text>
                {renderStepResult('execution')}
              </div>
            </div>

            {/* 进度条 */}
            {progress.total > 0 && (
              <div style={{ marginTop: '16px' }}>
                <Text type="secondary">执行进度:</Text>
                <Progress 
                  percent={progress.percentage} 
                  status={isProcessing ? 'active' : 'success'}
                  format={() => `${progress.current}/${progress.total}`}
                />
              </div>
            )}
          </Card>

          {/* 实时日志 */}
          <Card 
            title={
              <Space>
                <BugOutlined />
                <span>Agent执行日志</span>
                <Tag color="blue">{logs.length}</Tag>
              </Space>
            }
            style={{ marginBottom: '24px' }}
          >
            <div 
              ref={logContainerRef}
              style={{ 
                height: '400px', 
                overflowY: 'auto', 
                background: '#001529', 
                padding: '16px',
                borderRadius: '6px',
                fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace'
              }}
            >
              {logs.length === 0 ? (
                <Empty 
                  description="等待Agent开始执行..." 
                  style={{ color: '#8c8c8c' }}
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                />
              ) : (
                logs.map(log => (
                  <div 
                    key={log.id} 
                    style={{ 
                      display: 'flex',
                      alignItems: 'flex-start',
                      marginBottom: '8px',
                      fontSize: '14px',
                      lineHeight: '1.5'
                    }}
                  >
                    <span style={{ color: '#8c8c8c', minWidth: '80px', fontSize: '12px' }}>
                      [{log.timestamp}]
                    </span>
                    <span style={{ marginRight: '8px' }}>
                      {getAgentIcon(log.agent)}
                    </span>
                    <span style={{ marginRight: '8px' }}>
                      {getLogIcon(log.type)}
                    </span>
                    <span style={{ 
                      color: log.type === 'error' ? '#ff4d4f' : 
                             log.type === 'success' ? '#52c41a' : 
                             log.type === 'warning' ? '#faad14' : '#ffffff',
                      flex: 1
                    }}>
                      {log.message}
                    </span>
                  </div>
                ))
              )}
            </div>
          </Card>

          {/* 操作按钮 */}
          <div style={{ textAlign: 'center' }}>
            <Space size="large">
              <Button 
                icon={<ReloadOutlined />}
                onClick={resetProcess}
                size="large"
                disabled={isProcessing}
              >
                重置流程
              </Button>
              
              {workflowComplete && (
                <Button 
                  type="primary"
                  icon={<FileTextOutlined />}
                  size="large"
                  onClick={() => message.info('查看详细报告功能开发中...')}
                >
                  查看详细报告
                </Button>
              )}
            </Space>
          </div>

          {/* 上传文件信息 */}
          {uploadedFile && (
            <Card size="small" style={{ marginTop: '24px' }}>
              <Text type="secondary">当前处理文件: </Text>
              <Text strong>{uploadedFile.name}</Text>
              <Text type="secondary"> ({(uploadedFile.size / 1024).toFixed(2)} KB)</Text>
            </Card>
          )}
        </>
      )}
    </div>
  );
};

export default MultiAgentCollaboration;
