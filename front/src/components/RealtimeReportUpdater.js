import React, { useEffect, useRef } from 'react';
import { message } from 'antd';

const RealtimeReportUpdater = ({ onDataUpdate, refreshInterval = 30000 }) => {
  const intervalRef = useRef(null);
  const websocketRef = useRef(null);

  useEffect(() => {
    // 设置定时刷新
    intervalRef.current = setInterval(() => {
      if (onDataUpdate) {
        onDataUpdate();
      }
    }, refreshInterval);

    // 尝试建立WebSocket连接获取实时更新
    try {
      const ws = new WebSocket('ws://localhost:8080/ws/reports');
      
      ws.onopen = () => {
        console.log('报告实时更新WebSocket连接已建立');
        websocketRef.current = ws;
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'report_update') {
            console.log('收到报告更新通知');
            if (onDataUpdate) {
              onDataUpdate();
            }
          }
        } catch (error) {
          console.warn('解析WebSocket消息失败:', error);
        }
      };

      ws.onclose = () => {
        console.log('报告实时更新WebSocket连接关闭');
        websocketRef.current = null;
      };

      ws.onerror = (error) => {
        console.warn('WebSocket连接错误:', error);
      };

    } catch (error) {
      console.warn('无法建立WebSocket连接，将使用定时刷新:', error);
    }

    return () => {
      // 清理定时器
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      
      // 关闭WebSocket连接
      if (websocketRef.current) {
        websocketRef.current.close();
      }
    };
  }, [onDataUpdate, refreshInterval]);

  return null; // 这是一个无UI组件
};

export default RealtimeReportUpdater;
