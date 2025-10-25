#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Midscene WebSocket客户端
实现与Midscene服务的WebSocket通信
"""

import json
import asyncio
import websockets
import time
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from urllib.parse import urlparse

class MidsceneWebSocketClient:
    """
    Midscene WebSocket客户端
    
    支持功能：
    - 实时双向通信
    - 任务状态监控
    - 结果流式传输
    - 错误处理和重连
    """
    
    def __init__(
        self,
        server_url: str = "ws://localhost:3001",
        reconnect_attempts: int = 3,
        timeout: int = 30
    ):
        self.server_url = server_url
        self.reconnect_attempts = reconnect_attempts
        self.timeout = timeout
        self.websocket = None
        self.is_connected = False
        
        # 任务跟踪
        self.active_tasks = {}
        self.task_results = {}
        
        # 回调函数
        self.on_task_progress = None
        self.on_task_complete = None
        self.on_error = None
        
        print(f"🔌 Midscene WebSocket客户端初始化: {server_url}")
    
    async def connect(self) -> bool:
        """连接到Midscene服务器"""
        for attempt in range(self.reconnect_attempts):
            try:
                print(f"🔗 正在连接Midscene服务器... (尝试 {attempt + 1}/{self.reconnect_attempts})")
                
                self.websocket = await websockets.connect(
                    self.server_url,
                    timeout=self.timeout
                )
                
                self.is_connected = True
                print("✅ WebSocket连接成功！")
                
                # 启动消息监听
                asyncio.create_task(self._listen_for_messages())
                
                return True
                
            except Exception as e:
                print(f"❌ 连接失败 (尝试 {attempt + 1}): {e}")
                if attempt < self.reconnect_attempts - 1:
                    await asyncio.sleep(2 ** attempt)  # 指数退避
                
        return False
    
    async def disconnect(self):
        """断开连接"""
        if self.websocket and self.is_connected:
            await self.websocket.close()
            self.is_connected = False
            print("🔌 WebSocket连接已断开")
    
    async def _listen_for_messages(self):
        """监听服务器消息"""
        try:
            async for message in self.websocket:
                await self._handle_message(json.loads(message))
        except websockets.exceptions.ConnectionClosed:
            self.is_connected = False
            print("⚠️ WebSocket连接被服务器关闭")
        except Exception as e:
            print(f"❌ 消息监听错误: {e}")
            if self.on_error:
                await self.on_error(e)
    
    async def _handle_message(self, message: Dict[str, Any]):
        """处理服务器消息"""
        msg_type = message.get("type")
        task_id = message.get("task_id")
        
        if msg_type == "task_progress":
            # 任务进度更新
            progress = message.get("progress", {})
            if self.on_task_progress:
                await self.on_task_progress(task_id, progress)
            
            print(f"📈 任务 {task_id} 进度: {progress.get('percentage', 0)}%")
            
        elif msg_type == "task_complete":
            # 任务完成
            result = message.get("result", {})
            self.task_results[task_id] = result
            
            if task_id in self.active_tasks:
                self.active_tasks[task_id]["status"] = "completed"
                self.active_tasks[task_id]["result"] = result
            
            if self.on_task_complete:
                await self.on_task_complete(task_id, result)
            
            print(f"✅ 任务 {task_id} 完成")
            
        elif msg_type == "task_error":
            # 任务错误
            error = message.get("error", {})
            
            if task_id in self.active_tasks:
                self.active_tasks[task_id]["status"] = "failed"
                self.active_tasks[task_id]["error"] = error
            
            print(f"❌ 任务 {task_id} 失败: {error.get('message', '未知错误')}")
            
        elif msg_type == "server_status":
            # 服务器状态
            status = message.get("status", {})
            print(f"🖥️ 服务器状态: {status}")
    
    async def execute_yaml_task(
        self,
        yaml_content: str,
        task_id: Optional[str] = None,
        options: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """执行YAML任务"""
        if not self.is_connected:
            raise RuntimeError("WebSocket未连接")
        
        if not task_id:
            task_id = f"task_{int(time.time() * 1000)}"
        
        task_request = {
            "type": "execute_yaml",
            "task_id": task_id,
            "yaml_content": yaml_content,
            "options": options or {}
        }
        
        # 记录任务
        self.active_tasks[task_id] = {
            "status": "running",
            "start_time": time.time(),
            "type": "yaml"
        }
        
        # 发送任务请求
        await self.websocket.send(json.dumps(task_request))
        print(f"🚀 YAML任务 {task_id} 已提交")
        
        # 等待任务完成
        return await self._wait_for_task_completion(task_id)
    
    async def execute_instruction(
        self,
        instruction: Union[str, Dict],
        task_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """执行自然语言指令"""
        if not self.is_connected:
            raise RuntimeError("WebSocket未连接")
        
        if not task_id:
            task_id = f"instruction_{int(time.time() * 1000)}"
        
        task_request = {
            "type": "execute_instruction",
            "task_id": task_id,
            "instruction": instruction,
            "context": context or {}
        }
        
        # 记录任务
        self.active_tasks[task_id] = {
            "status": "running",
            "start_time": time.time(),
            "type": "instruction"
        }
        
        # 发送任务请求
        await self.websocket.send(json.dumps(task_request))
        print(f"🎯 指令任务 {task_id} 已提交")
        
        # 等待任务完成
        return await self._wait_for_task_completion(task_id)
    
    async def execute_batch_instructions(
        self,
        instructions: List[Union[str, Dict]],
        task_id: Optional[str] = None,
        options: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """批量执行指令"""
        if not self.is_connected:
            raise RuntimeError("WebSocket未连接")
        
        if not task_id:
            task_id = f"batch_{int(time.time() * 1000)}"
        
        task_request = {
            "type": "execute_batch",
            "task_id": task_id,
            "instructions": instructions,
            "options": options or {}
        }
        
        # 记录任务
        self.active_tasks[task_id] = {
            "status": "running",
            "start_time": time.time(),
            "type": "batch",
            "total_instructions": len(instructions)
        }
        
        # 发送任务请求
        await self.websocket.send(json.dumps(task_request))
        print(f"📦 批量任务 {task_id} 已提交 ({len(instructions)} 个指令)")
        
        # 等待任务完成
        return await self._wait_for_task_completion(task_id)
    
    async def _wait_for_task_completion(self, task_id: str) -> Dict[str, Any]:
        """等待任务完成"""
        start_time = time.time()
        
        while task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            
            # 检查是否超时
            if time.time() - start_time > self.timeout:
                raise TimeoutError(f"任务 {task_id} 执行超时")
            
            # 检查任务状态
            if task["status"] == "completed":
                return task.get("result", {})
            elif task["status"] == "failed":
                error = task.get("error", {})
                raise RuntimeError(f"任务失败: {error.get('message', '未知错误')}")
            
            await asyncio.sleep(0.1)  # 短暂等待
        
        # 如果任务不在活动列表中，检查结果缓存
        if task_id in self.task_results:
            return self.task_results[task_id]
        
        raise RuntimeError(f"任务 {task_id} 状态未知")
    
    async def get_server_status(self) -> Dict[str, Any]:
        """获取服务器状态"""
        if not self.is_connected:
            raise RuntimeError("WebSocket未连接")
        
        status_request = {
            "type": "get_status",
            "timestamp": time.time()
        }
        
        await self.websocket.send(json.dumps(status_request))
        
        # 简单等待状态响应（实际实现中可能需要更复杂的处理）
        await asyncio.sleep(0.5)
        
        return {"connected": True, "active_tasks": len(self.active_tasks)}
    
    async def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        if not self.is_connected:
            return False
        
        cancel_request = {
            "type": "cancel_task",
            "task_id": task_id
        }
        
        await self.websocket.send(json.dumps(cancel_request))
        
        # 从活动任务中移除
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = "cancelled"
        
        print(f"🚫 任务 {task_id} 取消请求已发送")
        return True
    
    def get_active_tasks(self) -> Dict[str, Dict]:
        """获取活动任务列表"""
        return self.active_tasks.copy()
    
    def set_callbacks(
        self,
        on_progress=None,
        on_complete=None,
        on_error=None
    ):
        """设置回调函数"""
        self.on_task_progress = on_progress
        self.on_task_complete = on_complete
        self.on_error = on_error

class MidsceneWebSocketManager:
    """
    Midscene WebSocket管理器
    管理多个连接和负载均衡
    """
    
    def __init__(self, server_urls: List[str] = None):
        self.server_urls = server_urls or ["ws://localhost:3001"]
        self.clients = []
        self.current_client_index = 0
        
    async def initialize(self) -> bool:
        """初始化所有客户端连接"""
        success_count = 0
        
        for url in self.server_urls:
            client = MidsceneWebSocketClient(url)
            if await client.connect():
                self.clients.append(client)
                success_count += 1
            else:
                print(f"⚠️ 无法连接到服务器: {url}")
        
        if success_count > 0:
            print(f"✅ 成功连接 {success_count}/{len(self.server_urls)} 个服务器")
            return True
        else:
            print("❌ 无法连接到任何Midscene服务器")
            return False
    
    def get_client(self) -> Optional[MidsceneWebSocketClient]:
        """获取可用的客户端（负载均衡）"""
        if not self.clients:
            return None
        
        # 简单轮询负载均衡
        client = self.clients[self.current_client_index]
        self.current_client_index = (self.current_client_index + 1) % len(self.clients)
        
        return client if client.is_connected else None
    
    async def execute_with_fallback(self, task_func, *args, **kwargs):
        """执行任务，支持自动故障转移"""
        for client in self.clients:
            if client.is_connected:
                try:
                    return await task_func(client, *args, **kwargs)
                except Exception as e:
                    print(f"⚠️ 客户端 {client.server_url} 执行失败: {e}")
                    continue
        
        raise RuntimeError("所有Midscene服务器都不可用")
    
    async def shutdown(self):
        """关闭所有连接"""
        for client in self.clients:
            await client.disconnect()
        self.clients.clear()
        print("🔌 所有Midscene连接已关闭")

# 全局WebSocket管理器实例
_global_manager = None

async def get_websocket_manager() -> MidsceneWebSocketManager:
    """获取全局WebSocket管理器"""
    global _global_manager
    
    if _global_manager is None:
        _global_manager = MidsceneWebSocketManager()
        await _global_manager.initialize()
    
    return _global_manager

async def execute_websocket_task(task_type: str, **kwargs) -> Dict[str, Any]:
    """执行WebSocket任务的便捷函数"""
    manager = await get_websocket_manager()
    client = manager.get_client()
    
    if not client:
        raise RuntimeError("没有可用的Midscene连接")
    
    if task_type == "yaml":
        return await client.execute_yaml_task(
            kwargs.get("yaml_content"),
            kwargs.get("task_id"),
            kwargs.get("options")
        )
    elif task_type == "instruction":
        return await client.execute_instruction(
            kwargs.get("instruction"),
            kwargs.get("task_id"),
            kwargs.get("context")
        )
    elif task_type == "batch":
        return await client.execute_batch_instructions(
            kwargs.get("instructions"),
            kwargs.get("task_id"),
            kwargs.get("options")
        )
    else:
        raise ValueError(f"不支持的任务类型: {task_type}")
