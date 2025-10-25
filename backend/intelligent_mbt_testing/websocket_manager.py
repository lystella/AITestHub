# -*- coding: utf-8 -*-
"""
WebSocket管理器 - 处理实时通信
"""

import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # 活跃连接列表
        self.active_connections: List[WebSocket] = []
        # 工作流状态存储
        self.workflow_status: Dict[str, Dict] = {}
        # 连接到工作流的映射
        self.connection_workflows: Dict[WebSocket, str] = {}
    
    async def connect(self, websocket: WebSocket, workflow_id: str):
        """建立WebSocket连接"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_workflows[websocket] = workflow_id
        
        # 初始化工作流状态
        if workflow_id not in self.workflow_status:
            self.workflow_status[workflow_id] = {
                "status": "connected",
                "start_time": datetime.now().isoformat(),
                "steps": {},
                "logs": []
            }
        
        logger.info(f"WebSocket连接已建立: {workflow_id}")
        
        # 发送连接成功消息
        await self.send_to_workflow(workflow_id, {
            "type": "connection_established",
            "workflow_id": workflow_id,
            "message": "WebSocket连接已建立",
            "timestamp": datetime.now().isoformat()
        })
    
    def disconnect(self, websocket: WebSocket):
        """断开WebSocket连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            
        workflow_id = self.connection_workflows.get(websocket)
        if workflow_id:
            logger.info(f"WebSocket连接已断开: {workflow_id}")
            del self.connection_workflows[websocket]
    
    async def send_to_workflow(self, workflow_id: str, message: dict):
        """向特定工作流发送消息"""
        # 添加到工作流日志
        if workflow_id in self.workflow_status:
            self.workflow_status[workflow_id]["logs"].append({
                **message,
                "timestamp": datetime.now().isoformat()
            })
        
        # 发送给对应的连接
        disconnected = []
        for connection, conn_workflow_id in self.connection_workflows.items():
            if conn_workflow_id == workflow_id:
                try:
                    await connection.send_text(json.dumps(message, ensure_ascii=False))
                except Exception as e:
                    logger.error(f"发送消息失败: {e}")
                    disconnected.append(connection)
        
        # 清理断开的连接
        for conn in disconnected:
            self.disconnect(conn)
    
    async def broadcast_step_start(self, workflow_id: str, step_id: str, step_name: str, description: str = ""):
        """广播步骤开始"""
        message = {
            "type": "step_start",
            "workflow_id": workflow_id,
            "step_id": step_id,
            "step_name": step_name,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        # 更新工作流状态
        if workflow_id in self.workflow_status:
            self.workflow_status[workflow_id]["steps"][step_id] = {
                "status": "active",
                "start_time": datetime.now().isoformat(),
                "name": step_name,
                "description": description
            }
        
        await self.send_to_workflow(workflow_id, message)
    
    async def broadcast_step_complete(self, workflow_id: str, step_id: str, result: dict = None):
        """广播步骤完成"""
        message = {
            "type": "step_complete",
            "workflow_id": workflow_id,
            "step_id": step_id,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
        # 更新工作流状态
        if workflow_id in self.workflow_status:
            if step_id in self.workflow_status[workflow_id]["steps"]:
                self.workflow_status[workflow_id]["steps"][step_id].update({
                    "status": "completed",
                    "end_time": datetime.now().isoformat(),
                    "result": result
                })
        
        await self.send_to_workflow(workflow_id, message)
    
    async def broadcast_step_error(self, workflow_id: str, step_id: str, error: str):
        """广播步骤错误"""
        message = {
            "type": "step_error",
            "workflow_id": workflow_id,
            "step_id": step_id,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        
        # 更新工作流状态
        if workflow_id in self.workflow_status:
            if step_id in self.workflow_status[workflow_id]["steps"]:
                self.workflow_status[workflow_id]["steps"][step_id].update({
                    "status": "error",
                    "error": error,
                    "end_time": datetime.now().isoformat()
                })
        
        await self.send_to_workflow(workflow_id, message)
    
    async def broadcast_log(self, workflow_id: str, message: str, level: str = "info", agent_name: str = "System"):
        """广播日志消息"""
        log_message = {
            "type": "log",
            "workflow_id": workflow_id,
            "agent_name": agent_name,
            "message": message,
            "level": level,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.send_to_workflow(workflow_id, log_message)
    
    async def broadcast_progress(self, workflow_id: str, progress: int, total: int, description: str = ""):
        """广播进度更新"""
        message = {
            "type": "progress",
            "workflow_id": workflow_id,
            "progress": progress,
            "total": total,
            "percentage": int((progress / total) * 100) if total > 0 else 0,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.send_to_workflow(workflow_id, message)
    
    def get_workflow_status(self, workflow_id: str) -> Dict:
        """获取工作流状态"""
        return self.workflow_status.get(workflow_id, {})
    
    def get_active_workflows(self) -> List[str]:
        """获取活跃的工作流ID列表"""
        return list(set(self.connection_workflows.values()))

# 全局WebSocket管理器实例
websocket_manager = WebSocketManager()
