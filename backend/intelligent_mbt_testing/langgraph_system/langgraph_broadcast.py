#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangGraph消息广播系统 - 模拟AgentScope的MsgHub功能
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Set, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

class MessageType(Enum):
    """消息类型"""
    BROADCAST = "broadcast"
    DIRECT = "direct"
    SYSTEM = "system"
    NOTIFICATION = "notification"
    COORDINATION = "coordination"

class MessagePriority(Enum):
    """消息优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4

@dataclass
class BroadcastMessage:
    """广播消息"""
    id: str
    sender: str
    recipients: List[str]
    message_type: MessageType
    priority: MessagePriority
    content: str
    metadata: Dict[str, Any]
    timestamp: str
    ttl: int = 300  # 消息生存时间(秒)
    delivered_to: Set[str] = None
    
    def __post_init__(self):
        if self.delivered_to is None:
            self.delivered_to = set()

class LangGraphMessageBroadcaster:
    """
    LangGraph消息广播器 - 模拟AgentScope MsgHub功能
    
    功能：
    - 多智能体消息广播
    - 点对点消息传递
    - 消息优先级管理
    - 消息持久化和恢复
    - 消息订阅和过滤
    """
    
    def __init__(self, websocket_manager=None):
        self.websocket_manager = websocket_manager
        
        # 消息存储
        self.message_queue: Dict[str, List[BroadcastMessage]] = {
            "coordinator": [],
            "analyzer": [],
            "planner": [],
            "data_processor": [],
            "executor": [],
            "reporter": [],
            "system": []
        }
        
        # 消息历史
        self.message_history: List[BroadcastMessage] = []
        
        # 订阅者和回调
        self.subscribers: Dict[str, Set[str]] = {}  # topic -> subscribers
        self.message_handlers: Dict[str, List[Callable]] = {}  # agent -> handlers
        
        # 统计信息
        self.stats = {
            "total_messages": 0,
            "broadcast_messages": 0,
            "direct_messages": 0,
            "failed_deliveries": 0,
            "active_subscriptions": 0
        }
        
        print("📡 LangGraph消息广播系统初始化")
        print("   🔄 支持多智能体消息广播")
        print("   📨 支持点对点消息传递")
    
    async def broadcast_to_all(self, sender: str, content: str, 
                             message_type: MessageType = MessageType.BROADCAST,
                             priority: MessagePriority = MessagePriority.NORMAL,
                             metadata: Dict[str, Any] = None,
                             exclude: List[str] = None) -> str:
        """
        广播消息给所有智能体
        
        Args:
            sender: 发送者
            content: 消息内容
            message_type: 消息类型
            priority: 优先级
            metadata: 元数据
            exclude: 排除的接收者
            
        Returns:
            消息ID
        """
        all_agents = list(self.message_queue.keys())
        if exclude:
            recipients = [agent for agent in all_agents if agent not in exclude and agent != sender]
        else:
            recipients = [agent for agent in all_agents if agent != sender]
        
        return await self.send_message(
            sender=sender,
            recipients=recipients,
            content=content,
            message_type=message_type,
            priority=priority,
            metadata=metadata
        )
    
    async def send_message(self, sender: str, recipients: List[str], content: str,
                         message_type: MessageType = MessageType.DIRECT,
                         priority: MessagePriority = MessagePriority.NORMAL,
                         metadata: Dict[str, Any] = None,
                         ttl: int = 300) -> str:
        """
        发送消息给指定接收者
        
        Args:
            sender: 发送者
            recipients: 接收者列表
            content: 消息内容
            message_type: 消息类型
            priority: 优先级
            metadata: 元数据
            ttl: 生存时间
            
        Returns:
            消息ID
        """
        try:
            # 创建消息
            message = BroadcastMessage(
                id=str(uuid.uuid4()),
                sender=sender,
                recipients=recipients,
                message_type=message_type,
                priority=priority,
                content=content,
                metadata=metadata or {},
                timestamp=datetime.now().isoformat(),
                ttl=ttl,
                delivered_to=set()
            )
            
            # 分发消息
            delivery_results = await self._deliver_message(message)
            
            # 添加到历史
            self.message_history.append(message)
            
            # 更新统计
            self.stats["total_messages"] += 1
            if message_type == MessageType.BROADCAST:
                self.stats["broadcast_messages"] += 1
            else:
                self.stats["direct_messages"] += 1
            
            # WebSocket广播
            if self.websocket_manager:
                await self._broadcast_via_websocket(message)
            
            print(f"📡 [{sender}] 发送消息: {message_type.value}")
            print(f"   📨 接收者: {recipients}")
            print(f"   📝 内容: {content[:50]}...")
            print(f"   ✅ 成功投递: {len(delivery_results['success'])}")
            if delivery_results['failed']:
                print(f"   ❌ 投递失败: {delivery_results['failed']}")
            
            return message.id
            
        except Exception as e:
            print(f"❌ 发送消息失败: {e}")
            self.stats["failed_deliveries"] += 1
            return None
    
    async def _deliver_message(self, message: BroadcastMessage) -> Dict[str, Any]:
        """投递消息"""
        success = []
        failed = []
        
        for recipient in message.recipients:
            try:
                if recipient in self.message_queue:
                    # 按优先级插入消息
                    await self._insert_by_priority(recipient, message)
                    message.delivered_to.add(recipient)
                    success.append(recipient)
                    
                    # 调用消息处理器
                    await self._call_message_handlers(recipient, message)
                else:
                    failed.append(recipient)
                    
            except Exception as e:
                print(f"⚠️ 向 {recipient} 投递消息失败: {e}")
                failed.append(recipient)
        
        return {"success": success, "failed": failed}
    
    async def _insert_by_priority(self, recipient: str, message: BroadcastMessage):
        """按优先级插入消息"""
        queue = self.message_queue[recipient]
        
        # 找到插入位置
        insert_index = len(queue)
        for i, existing_msg in enumerate(queue):
            if message.priority.value > existing_msg.priority.value:
                insert_index = i
                break
        
        queue.insert(insert_index, message)
    
    async def _call_message_handlers(self, recipient: str, message: BroadcastMessage):
        """调用消息处理器"""
        handlers = self.message_handlers.get(recipient, [])
        for handler in handlers:
            try:
                await handler(message)
            except Exception as e:
                print(f"⚠️ 消息处理器执行失败: {e}")
    
    async def get_messages(self, recipient: str, limit: int = 10, 
                         message_type: MessageType = None) -> List[BroadcastMessage]:
        """获取消息"""
        try:
            messages = self.message_queue.get(recipient, [])
            
            # 过滤消息类型
            if message_type:
                messages = [msg for msg in messages if msg.message_type == message_type]
            
            # 清理过期消息
            current_time = datetime.now().timestamp()
            valid_messages = []
            
            for msg in messages:
                msg_time = datetime.fromisoformat(msg.timestamp).timestamp()
                if current_time - msg_time < msg.ttl:
                    valid_messages.append(msg)
            
            # 更新队列
            self.message_queue[recipient] = valid_messages
            
            return valid_messages[:limit]
            
        except Exception as e:
            print(f"❌ 获取消息失败: {e}")
            return []
    
    async def subscribe_to_topic(self, agent: str, topic: str):
        """订阅主题"""
        if topic not in self.subscribers:
            self.subscribers[topic] = set()
        
        self.subscribers[topic].add(agent)
        self.stats["active_subscriptions"] += 1
        
        print(f"📌 [{agent}] 订阅主题: {topic}")
    
    async def unsubscribe_from_topic(self, agent: str, topic: str):
        """取消订阅"""
        if topic in self.subscribers and agent in self.subscribers[topic]:
            self.subscribers[topic].remove(agent)
            self.stats["active_subscriptions"] -= 1
            print(f"📌 [{agent}] 取消订阅: {topic}")
    
    async def publish_to_topic(self, sender: str, topic: str, content: str,
                             priority: MessagePriority = MessagePriority.NORMAL,
                             metadata: Dict[str, Any] = None) -> str:
        """发布消息到主题"""
        subscribers = self.subscribers.get(topic, set())
        if not subscribers:
            print(f"⚠️ 主题 '{topic}' 没有订阅者")
            return None
        
        return await self.send_message(
            sender=sender,
            recipients=list(subscribers),
            content=content,
            message_type=MessageType.NOTIFICATION,
            priority=priority,
            metadata={**(metadata or {}), "topic": topic}
        )
    
    def register_message_handler(self, agent: str, handler: Callable):
        """注册消息处理器"""
        if agent not in self.message_handlers:
            self.message_handlers[agent] = []
        
        self.message_handlers[agent].append(handler)
        print(f"🔧 [{agent}] 注册消息处理器")
    
    async def clear_messages(self, recipient: str, message_type: MessageType = None):
        """清空消息"""
        if recipient in self.message_queue:
            if message_type:
                self.message_queue[recipient] = [
                    msg for msg in self.message_queue[recipient] 
                    if msg.message_type != message_type
                ]
            else:
                self.message_queue[recipient] = []
            
            print(f"🗑️ [{recipient}] 清空消息队列")
    
    async def _broadcast_via_websocket(self, message: BroadcastMessage):
        """通过WebSocket广播"""
        if self.websocket_manager:
            try:
                # 使用WebSocketManager的broadcast_log方法
                log_message = f"[{message.sender}] {message.content}"
                await self.websocket_manager.broadcast_log(
                    workflow_id="system",
                    message=log_message,
                    level="info",
                    agent_name=message.sender
                )
                
            except Exception as e:
                print(f"⚠️ WebSocket广播失败: {e}")
    
    def get_broadcast_stats(self) -> Dict[str, Any]:
        """获取广播统计"""
        queue_sizes = {agent: len(queue) for agent, queue in self.message_queue.items()}
        
        return {
            "total_messages": self.stats["total_messages"],
            "broadcast_messages": self.stats["broadcast_messages"],
            "direct_messages": self.stats["direct_messages"],
            "failed_deliveries": self.stats["failed_deliveries"],
            "active_subscriptions": self.stats["active_subscriptions"],
            "queue_sizes": queue_sizes,
            "total_subscribers": sum(len(subs) for subs in self.subscribers.values()),
            "active_topics": len(self.subscribers),
            "message_history_size": len(self.message_history)
        }
    
    async def cleanup_expired_messages(self):
        """清理过期消息"""
        current_time = datetime.now().timestamp()
        cleaned_count = 0
        
        for agent, messages in self.message_queue.items():
            valid_messages = []
            for msg in messages:
                msg_time = datetime.fromisoformat(msg.timestamp).timestamp()
                if current_time - msg_time < msg.ttl:
                    valid_messages.append(msg)
                else:
                    cleaned_count += 1
            
            self.message_queue[agent] = valid_messages
        
        # 清理历史消息（保留最近1000条）
        if len(self.message_history) > 1000:
            self.message_history = self.message_history[-1000:]
            cleaned_count += len(self.message_history) - 1000
        
        if cleaned_count > 0:
            print(f"🧹 清理了 {cleaned_count} 条过期消息")


# 全局消息广播实例
_broadcaster_instance = None

def get_message_broadcaster(websocket_manager=None) -> LangGraphMessageBroadcaster:
    """获取消息广播器单例"""
    global _broadcaster_instance
    if _broadcaster_instance is None:
        _broadcaster_instance = LangGraphMessageBroadcaster(websocket_manager)
    return _broadcaster_instance
