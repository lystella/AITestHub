#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangGraph高级追踪系统 - 模拟AgentScope的@trace_reply功能
"""

import asyncio
import json
import time
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import functools
import inspect

class TraceLevel(Enum):
    """追踪级别"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class TraceType(Enum):
    """追踪类型"""
    FUNCTION_CALL = "function_call"
    AGENT_EXECUTION = "agent_execution"
    MODEL_CALL = "model_call"
    WORKFLOW_STEP = "workflow_step"
    SYSTEM_EVENT = "system_event"

@dataclass
class TraceSpan:
    """追踪跨度"""
    span_id: str
    parent_id: Optional[str]
    trace_id: str
    operation_name: str
    trace_type: TraceType
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    status: str = "running"  # running, success, error
    input_data: Any = None
    output_data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    tags: Dict[str, str] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.tags is None:
            self.tags = {}

class LangGraphTracer:
    """
    LangGraph追踪系统
    
    功能：
    - 函数调用追踪
    - 执行链路追踪
    - 性能分析
    - 调用关系图
    - 错误追踪
    """
    
    def __init__(self, max_spans: int = 10000):
        self.max_spans = max_spans
        
        # 追踪存储
        self.spans: Dict[str, TraceSpan] = {}
        self.traces: Dict[str, List[str]] = {}  # trace_id -> span_ids
        self.active_spans: Dict[str, str] = {}  # context -> span_id
        
        # 统计信息
        self.stats = {
            "total_spans": 0,
            "active_traces": 0,
            "completed_traces": 0,
            "error_spans": 0,
            "avg_execution_time": 0.0
        }
        
        print("📊 LangGraph高级追踪系统初始化")
        print(f"   📈 最大跨度数: {max_spans}")
        print("   🔍 支持完整执行链路追踪")
    
    def start_trace(self, operation_name: str, trace_type: TraceType = TraceType.FUNCTION_CALL,
                   parent_span_id: str = None, metadata: Dict[str, Any] = None,
                   tags: Dict[str, str] = None) -> str:
        """开始追踪"""
        # 生成ID
        span_id = str(uuid.uuid4())
        trace_id = parent_span_id and self._get_trace_id(parent_span_id) or str(uuid.uuid4())
        
        # 创建跨度
        span = TraceSpan(
            span_id=span_id,
            parent_id=parent_span_id,
            trace_id=trace_id,
            operation_name=operation_name,
            trace_type=trace_type,
            start_time=time.time(),
            metadata=metadata or {},
            tags=tags or {}
        )
        
        # 存储跨度
        self.spans[span_id] = span
        
        # 更新追踪
        if trace_id not in self.traces:
            self.traces[trace_id] = []
            self.stats["active_traces"] += 1
        
        self.traces[trace_id].append(span_id)
        self.stats["total_spans"] += 1
        
        print(f"🔍 开始追踪: {operation_name} ({trace_type.value})")
        print(f"   🆔 Span ID: {span_id[:8]}...")
        print(f"   🔗 Trace ID: {trace_id[:8]}...")
        
        return span_id
    
    def end_trace(self, span_id: str, output_data: Any = None, 
                 error: Exception = None, metadata: Dict[str, Any] = None):
        """结束追踪"""
        if span_id not in self.spans:
            print(f"⚠️ 未找到追踪跨度: {span_id}")
            return
        
        span = self.spans[span_id]
        span.end_time = time.time()
        span.duration = span.end_time - span.start_time
        
        if error:
            span.status = "error"
            span.error = str(error)
            self.stats["error_spans"] += 1
        else:
            span.status = "success"
            span.output_data = output_data
        
        if metadata:
            span.metadata.update(metadata)
        
        # 更新平均执行时间
        self._update_avg_execution_time(span.duration)
        
        print(f"✅ 追踪完成: {span.operation_name}")
        print(f"   ⏱️ 耗时: {span.duration:.3f}s")
        print(f"   📊 状态: {span.status}")
        
        # 检查追踪是否完成
        self._check_trace_completion(span.trace_id)
    
    def add_span_event(self, span_id: str, event_name: str, 
                      event_data: Any = None, timestamp: float = None):
        """添加跨度事件"""
        if span_id not in self.spans:
            return
        
        span = self.spans[span_id]
        if "events" not in span.metadata:
            span.metadata["events"] = []
        
        event = {
            "name": event_name,
            "timestamp": timestamp or time.time(),
            "data": event_data
        }
        
        span.metadata["events"].append(event)
        print(f"📝 [{span.operation_name}] 事件: {event_name}")
    
    def set_span_tag(self, span_id: str, key: str, value: str):
        """设置跨度标签"""
        if span_id in self.spans:
            self.spans[span_id].tags[key] = value
    
    def set_span_metadata(self, span_id: str, key: str, value: Any):
        """设置跨度元数据"""
        if span_id in self.spans:
            self.spans[span_id].metadata[key] = value
    
    def get_trace(self, trace_id: str) -> List[TraceSpan]:
        """获取完整追踪"""
        span_ids = self.traces.get(trace_id, [])
        return [self.spans[span_id] for span_id in span_ids if span_id in self.spans]
    
    def get_span(self, span_id: str) -> Optional[TraceSpan]:
        """获取跨度"""
        return self.spans.get(span_id)
    
    def get_call_tree(self, trace_id: str) -> Dict[str, Any]:
        """获取调用树"""
        spans = self.get_trace(trace_id)
        if not spans:
            return {}
        
        # 构建调用树
        tree = {}
        span_map = {span.span_id: span for span in spans}
        
        # 找到根节点
        root_spans = [span for span in spans if span.parent_id is None]
        
        def build_tree_node(span: TraceSpan) -> Dict[str, Any]:
            children = [
                build_tree_node(child_span)
                for child_span in spans
                if child_span.parent_id == span.span_id
            ]
            
            return {
                "span_id": span.span_id,
                "operation_name": span.operation_name,
                "trace_type": span.trace_type.value,
                "duration": span.duration,
                "status": span.status,
                "start_time": span.start_time,
                "end_time": span.end_time,
                "error": span.error,
                "children": children,
                "metadata": span.metadata,
                "tags": span.tags
            }
        
        tree["trace_id"] = trace_id
        tree["root_spans"] = [build_tree_node(span) for span in root_spans]
        tree["total_spans"] = len(spans)
        tree["total_duration"] = max(span.end_time or 0 for span in spans) - min(span.start_time for span in spans)
        
        return tree
    
    def get_performance_analysis(self, trace_id: str) -> Dict[str, Any]:
        """获取性能分析"""
        spans = self.get_trace(trace_id)
        if not spans:
            return {}
        
        # 计算统计信息
        total_duration = max(span.end_time or 0 for span in spans) - min(span.start_time for span in spans)
        avg_duration = sum(span.duration or 0 for span in spans) / len(spans)
        
        # 找出最慢的操作
        slowest_spans = sorted(spans, key=lambda x: x.duration or 0, reverse=True)[:5]
        
        # 统计操作类型
        operation_stats = {}
        for span in spans:
            op_type = span.trace_type.value
            if op_type not in operation_stats:
                operation_stats[op_type] = {"count": 0, "total_time": 0.0}
            
            operation_stats[op_type]["count"] += 1
            operation_stats[op_type]["total_time"] += span.duration or 0
        
        # 计算平均时间
        for op_type, stats in operation_stats.items():
            stats["avg_time"] = stats["total_time"] / stats["count"]
        
        return {
            "trace_id": trace_id,
            "total_duration": total_duration,
            "avg_span_duration": avg_duration,
            "total_spans": len(spans),
            "error_spans": len([span for span in spans if span.status == "error"]),
            "slowest_operations": [
                {
                    "operation": span.operation_name,
                    "duration": span.duration,
                    "type": span.trace_type.value
                }
                for span in slowest_spans
            ],
            "operation_statistics": operation_stats
        }
    
    def get_error_analysis(self, trace_id: str = None) -> Dict[str, Any]:
        """获取错误分析"""
        if trace_id:
            spans = self.get_trace(trace_id)
        else:
            spans = list(self.spans.values())
        
        error_spans = [span for span in spans if span.status == "error"]
        
        # 错误统计
        error_stats = {}
        for span in error_spans:
            error_type = type(span.error).__name__ if hasattr(span.error, '__class__') else "Unknown"
            if error_type not in error_stats:
                error_stats[error_type] = {"count": 0, "operations": []}
            
            error_stats[error_type]["count"] += 1
            error_stats[error_type]["operations"].append(span.operation_name)
        
        return {
            "total_errors": len(error_spans),
            "error_rate": len(error_spans) / max(1, len(spans)),
            "error_types": error_stats,
            "recent_errors": [
                {
                    "operation": span.operation_name,
                    "error": span.error,
                    "timestamp": span.start_time,
                    "trace_id": span.trace_id
                }
                for span in sorted(error_spans, key=lambda x: x.start_time, reverse=True)[:10]
            ]
        }
    
    def _get_trace_id(self, span_id: str) -> str:
        """获取跨度的追踪ID"""
        span = self.spans.get(span_id)
        return span.trace_id if span else ""
    
    def _check_trace_completion(self, trace_id: str):
        """检查追踪是否完成"""
        span_ids = self.traces.get(trace_id, [])
        spans = [self.spans[span_id] for span_id in span_ids if span_id in self.spans]
        
        # 检查是否所有跨度都已完成
        if all(span.status != "running" for span in spans):
            self.stats["active_traces"] -= 1
            self.stats["completed_traces"] += 1
            print(f"🏁 追踪完成: {trace_id[:8]}... ({len(spans)} 个跨度)")
    
    def _update_avg_execution_time(self, duration: float):
        """更新平均执行时间"""
        current_avg = self.stats["avg_execution_time"]
        total_spans = self.stats["total_spans"]
        
        self.stats["avg_execution_time"] = (current_avg * (total_spans - 1) + duration) / total_spans
    
    def cleanup_old_traces(self, max_age_hours: int = 24):
        """清理旧追踪"""
        current_time = time.time()
        cutoff_time = current_time - (max_age_hours * 3600)
        
        old_spans = []
        for span_id, span in self.spans.items():
            if span.start_time < cutoff_time:
                old_spans.append(span_id)
        
        # 删除旧跨度
        for span_id in old_spans:
            span = self.spans[span_id]
            del self.spans[span_id]
            
            # 从追踪中删除
            if span.trace_id in self.traces:
                self.traces[span.trace_id].remove(span_id)
                if not self.traces[span.trace_id]:
                    del self.traces[span.trace_id]
        
        print(f"🧹 清理了 {len(old_spans)} 个旧追踪跨度")
    
    def get_tracing_stats(self) -> Dict[str, Any]:
        """获取追踪统计"""
        return {
            **self.stats,
            "memory_usage": {
                "total_spans": len(self.spans),
                "active_traces": len(self.traces),
                "memory_limit": self.max_spans
            }
        }


# 追踪装饰器
def trace_execution(operation_name: str = None, trace_type: TraceType = TraceType.FUNCTION_CALL,
                   tracer: LangGraphTracer = None):
    """追踪执行装饰器"""
    def decorator(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            if tracer is None:
                return await func(*args, **kwargs)
            
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            span_id = tracer.start_trace(op_name, trace_type)
            
            try:
                # 记录输入
                tracer.set_span_metadata(span_id, "input_args", str(args)[:200])
                tracer.set_span_metadata(span_id, "input_kwargs", str(kwargs)[:200])
                
                result = await func(*args, **kwargs)
                
                # 记录输出
                tracer.set_span_metadata(span_id, "output", str(result)[:200])
                tracer.end_trace(span_id, result)
                
                return result
                
            except Exception as e:
                tracer.end_trace(span_id, error=e)
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            if tracer is None:
                return func(*args, **kwargs)
            
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            span_id = tracer.start_trace(op_name, trace_type)
            
            try:
                tracer.set_span_metadata(span_id, "input_args", str(args)[:200])
                tracer.set_span_metadata(span_id, "input_kwargs", str(kwargs)[:200])
                
                result = func(*args, **kwargs)
                
                tracer.set_span_metadata(span_id, "output", str(result)[:200])
                tracer.end_trace(span_id, result)
                
                return result
                
            except Exception as e:
                tracer.end_trace(span_id, error=e)
                raise
        
        # 根据函数类型返回对应的包装器
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# 全局追踪器实例
_tracer_instance = None

def get_tracer() -> LangGraphTracer:
    """获取追踪器单例"""
    global _tracer_instance
    if _tracer_instance is None:
        _tracer_instance = LangGraphTracer()
    return _tracer_instance
