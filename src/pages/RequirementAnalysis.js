import React, { useState, useRef, useEffect } from 'react';
import { Row, Col, Card, Upload, Button, Typography, Empty, Menu, message, Spin } from 'antd';
import { 
  UploadOutlined, 
  ArrowRightOutlined, 
  CheckOutlined,
  DotChartOutlined,
  MenuOutlined,
  FileTextOutlined
} from '@ant-design/icons';
import mammoth from 'mammoth';

const { Title, Text } = Typography;

// 解析文档内容并生成层级结构
const parseDocumentContent = (html) => {
  // 创建临时DOM元素来解析HTML
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  
  const structure = [];
  const contentMap = {};
  let currentSection = null;
  let currentSubsection = null;
  let sectionIndex = 0;
  let subsectionIndex = 0;
  let subsubsectionIndex = 0;
  
  // 遍历所有元素
  const elements = doc.querySelectorAll('h1, h2, h3, h4, h5, h6, p');
  
  elements.forEach((element, index) => {
    const text = element.textContent.trim();
    if (!text) return;
    
    const tagName = element.tagName.toLowerCase();
    
    if (tagName === 'h1' || tagName === 'h2') {
      // 主要章节
      sectionIndex++;
      subsectionIndex = 0;
      subsubsectionIndex = 0;
      
      const key = sectionIndex.toString();
      currentSection = {
        key,
        label: text,
        children: [],
        content: text
      };
      structure.push(currentSection);
      contentMap[key] = currentSection;
      
    } else if (tagName === 'h3' || tagName === 'h4') {
      // 子章节
      subsectionIndex++;
      subsubsectionIndex = 0;
      
      const key = `${sectionIndex}.${subsectionIndex}`;
      currentSubsection = {
        key,
        label: text,
        children: [],
        content: text
      };
      
      if (currentSection) {
        currentSection.children.push(currentSubsection);
      }
      contentMap[key] = currentSubsection;
      
    } else if (tagName === 'h5' || tagName === 'h6') {
      // 子子章节
      subsubsectionIndex++;
      
      const key = `${sectionIndex}.${subsectionIndex}.${subsubsectionIndex}`;
      const subsubsection = {
        key,
        label: text,
        content: text
      };
      
      if (currentSubsection) {
        currentSubsection.children.push(subsubsection);
      }
      contentMap[key] = subsubsection;
      
    } else if (tagName === 'p' && text.length > 10) {
      // 段落内容，添加到当前章节
      if (currentSubsection) {
        currentSubsection.content += '\n\n' + text;
      } else if (currentSection) {
        currentSection.content += '\n\n' + text;
      }
    }
  });
  
  return { structure, contentMap };
};

// 文档解析函数
const parseDocument = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = async (event) => {
      try {
        const arrayBuffer = event.target.result;
        
        // 使用mammoth解析Word文档
        const result = await mammoth.convertToHtml({ arrayBuffer });
        const html = result.value;
        
        // 解析HTML内容生成层级结构
        const { structure, contentMap } = parseDocumentContent(html);
        
        console.log('解析出的结构:', structure);
        console.log('原始HTML:', html);
        
        // 如果没有解析出结构，使用原始HTML内容
        if (structure.length === 0) {
          const fullContent = result.value
            .replace(/<[^>]*>/g, '') // 移除HTML标签
            .replace(/\s+/g, ' ') // 合并空白字符
            .trim();
          
          console.log('使用原始内容模式');
          resolve({
            structure: [],
            content: fullContent,
            fileName: file.name,
            rawHtml: html
          });
        } else {
          // 生成完整文档内容
          const fullContent = structure.map(section => {
            let content = section.label + '\n\n' + section.content;
            if (section.children) {
              section.children.forEach(subsection => {
                content += '\n\n' + subsection.label + '\n\n' + subsection.content;
                if (subsection.children) {
                  subsection.children.forEach(subsub => {
                    content += '\n\n' + subsub.label + '\n\n' + subsub.content;
                  });
                }
              });
            }
            return content;
          }).join('\n\n');
          
          console.log('使用结构化内容模式');
          resolve({
            structure,
            content: fullContent,
            fileName: file.name,
            rawHtml: html
          });
        }
      } catch (error) {
        reject(error);
      }
    };
    
    reader.onerror = () => {
      reject(new Error('文件读取失败'));
    };
    
    reader.readAsArrayBuffer(file);
  });
};

// 扁平化文档数据以便查找内容
const flattenDocumentData = (data) => {
  let flatData = {};
  data.forEach(item => {
    flatData[item.key] = item;
    if (item.children) {
      Object.assign(flatData, flattenDocumentData(item.children));
    }
  });
  return flatData;
};

const RequirementAnalysis = () => {
  const [documentStructure, setDocumentStructure] = useState([]);
  const [fullDocumentContent, setFullDocumentContent] = useState('');
  const [selectedKey, setSelectedKey] = useState('');
  const [openKeys, setOpenKeys] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState('');
  const rightContentRef = useRef(null);

  const uploadProps = {
    name: 'file',
    multiple: false,
    showUploadList: false,
    accept: '.doc,.docx',
    beforeUpload: (file) => {
      const isDoc = file.type === 'application/msword' || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
      if (!isDoc) {
        message.error('只能上传 .doc 或 .docx 格式的文件!');
        return false;
      }
      const isLt10M = file.size / 1024 / 1024 < 10;
      if (!isLt10M) {
        message.error('文件大小不能超过 10MB!');
        return false;
      }
      return true;
    },
    customRequest: async ({ file, onSuccess, onError }) => {
      try {
        setUploading(true);
        setFileName(file.name);
        
        // 解析文档
        const result = await parseDocument(file);
        
        setDocumentStructure(result.structure);
        setFullDocumentContent(result.content);
        setSelectedKey('');
        // 默认展开所有一级、二级key
        const defaultOpens = [];
        result.structure.forEach(sec => {
          defaultOpens.push(sec.key);
          (sec.children || []).forEach(sub => defaultOpens.push(sub.key));
        });
        setOpenKeys(defaultOpens);
        
        if (result.structure.length > 0) {
          message.success(`文档上传并解析成功! 共解析出 ${result.structure.length} 个主要章节`);
        } else {
          message.success('文档上传成功! 已提取文档内容');
        }
        
        onSuccess(result);
      } catch (error) {
        console.error('文档解析错误:', error);
        message.error('文档解析失败: ' + error.message);
        onError(error);
      } finally {
        setUploading(false);
      }
    },
  };

  const renderMenuItems = (items) => {
    return items.map(item => {
      if (item.children) {
        return (
          <Menu.SubMenu key={item.key} title={item.label}>
            {renderMenuItems(item.children)}
          </Menu.SubMenu>
        );
      }
      return <Menu.Item key={item.key}>{item.label}</Menu.Item>;
    });
  };

  // 移除不再使用的变量
  // const flatDocumentMap = flattenDocumentData(documentStructure);
  // const currentContent = flatDocumentMap[selectedKey]?.content || '';
  // const currentTitle = flatDocumentMap[selectedKey]?.label || '';

  return (
    <div>
      <Title level={3} style={{ marginBottom: 24 }}>AI需求分析</Title>

      <Row gutter={24}>
        <Col xs={24} md={10}>
          <Card title={<span><MenuOutlined style={{ color: '#1890ff', marginRight: 8 }} />文档层级</span>}>
            {/* 上传区域 */}
            <div style={{
              border: '1px dashed #d9d9d9',
              borderRadius: 8,
              height: 100,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexDirection: 'column',
              gap: 16,
              marginBottom: 16,
              backgroundColor: '#fafafa'
            }}>
              <Upload {...uploadProps}>
                <Button icon={<UploadOutlined />} type="primary" loading={uploading}>
                  {uploading ? '解析中...' : '上传文档'}
                </Button>
              </Upload>
              <Text type="secondary">支持 .doc/.docx 格式</Text>
              {fileName && (
                <Text type="success" style={{ fontSize: '12px' }}>
                  已上传: {fileName}
                </Text>
              )}
            </div>
            {/* 文档层级菜单 */}
            {documentStructure.length > 0 ? (
              <Menu
                mode="inline"
                selectedKeys={[selectedKey]}
                openKeys={openKeys}
                onSelect={({ key }) => {
                  setSelectedKey(key);
                  // 平滑滚动到右侧对应锚点
                  const el = document.getElementById(`section-${key}`);
                  if (el) {
                    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                  }
                }}
                onOpenChange={(keys) => setOpenKeys(keys)}
                style={{ borderRight: 0 }}
              >
                {renderMenuItems(documentStructure)}
              </Menu>
            ) : (
              <Empty 
                description="请先上传文档"
                image={Empty.PRESENTED_IMAGE_SIMPLE}
              />
            )}
          </Card>
        </Col>

        <Col xs={24} md={14}>
          <Card
            title={<span><DotChartOutlined style={{ color: '#1890ff', marginRight: 8 }} />文档内容预览</span>}
            extra={<Button type="primary" icon={<CheckOutlined />}>保存</Button>}
          >
            {uploading ? (
              <div style={{ textAlign: 'center', padding: '40px 0' }}>
                <Spin size="large" />
                <div style={{ marginTop: 16 }}>
                  <Text>正在解析文档，请稍候...</Text>
                </div>
              </div>
            ) : documentStructure.length > 0 ? (
              <div ref={rightContentRef} style={{ maxHeight: 520, overflowY: 'auto', paddingRight: 8 }}>
                {documentStructure.map(section => (
                  <div key={section.key} id={`section-${section.key}`} style={{ marginBottom: 24 }}>
                    <Title level={4} style={{ marginTop: 0 }}>{section.label}</Title>
                    <Text style={{ whiteSpace: 'pre-wrap' }}>{section.content}</Text>
                    {(section.children || []).map(sub => (
                      <div key={sub.key} id={`section-${sub.key}`} style={{ marginTop: 16, paddingLeft: 8 }}>
                        <Title level={5} style={{ marginBottom: 8 }}>{sub.label}</Title>
                        <Text style={{ whiteSpace: 'pre-wrap' }}>{sub.content}</Text>
                        {(sub.children || []).map(subsub => (
                          <div key={subsub.key} id={`section-${subsub.key}`} style={{ marginTop: 12, paddingLeft: 8 }}>
                            <Text strong>{subsub.label}</Text>
                            <div style={{ whiteSpace: 'pre-wrap' }}>{subsub.content}</div>
                          </div>
                        ))}
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            ) : fullDocumentContent ? (
              <div>
                <Title level={4}>完整文档内容</Title>
                <div style={{ 
                  maxHeight: '500px', 
                  overflowY: 'auto', 
                  padding: '16px', 
                  background: '#fafafa', 
                  borderRadius: '6px',
                  border: '1px solid #d9d9d9'
                }}>
                  <pre style={{ 
                    whiteSpace: 'pre-wrap', 
                    fontFamily: 'inherit',
                    margin: 0,
                    fontSize: '14px',
                    lineHeight: '1.6'
                  }}>{fullDocumentContent}</pre>
                </div>
              </div>
            ) : (
              <Empty
                image={Empty.PRESENTED_IMAGE_SIMPLE}
                description="请先上传文档或选择左侧层级进行预览"
              />
            )}
          </Card>
        </Col>
      </Row>

      <div style={{
        marginTop: 24,
        padding: '16px 24px',
        background: '#fff',
        borderRadius: 8,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <Text strong>下一步：开启智能测试设计</Text>
        <Button type="primary" icon={<ArrowRightOutlined />}>前往测试设计</Button>
      </div>
    </div>
  );
};

export default RequirementAnalysis;
