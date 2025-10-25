#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangGraph Hook精准性检查系统 - 模拟AgentScope的Hook机制
"""

import asyncio
import json
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import functools

class HookType(Enum):
    """Hook类型"""
    PRE_EXECUTION = "pre_execution"
    POST_EXECUTION = "post_execution"
    VALIDATION = "validation"
    ERROR_HANDLING = "error_handling"
    PERFORMANCE = "performance"

class HookPriority(Enum):
    """Hook优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class HookResult:
    """Hook执行结果"""
    hook_name: str
    hook_type: HookType
    success: bool
    execution_time: float
    result: Any = None
    error: str = None
    metadata: Dict[str, Any] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any] = None

class LangGraphHookManager:
    """
    LangGraph Hook管理器 - 精准性检查和验证
    
    功能：
    - 前置和后置Hook
    - 输入输出验证
    - 性能监控Hook
    - 错误处理Hook
    - 自定义验证规则
    """
    
    def __init__(self):
        # Hook注册表
        self.hooks: Dict[str, Dict[HookType, List[Callable]]] = {}
        self.hook_priorities: Dict[str, Dict[HookType, Dict[str, HookPriority]]] = {}
        
        # 全局Hook
        self.global_hooks: Dict[HookType, List[Callable]] = {}
        for hook_type in HookType:
            self.global_hooks[hook_type] = []
        
        # Hook执行历史
        self.hook_history: List[HookResult] = []
        
        # 验证规则
        self.validation_rules: Dict[str, List[Callable]] = {}
        
        # 统计信息
        self.stats = {
            "total_hooks_executed": 0,
            "successful_hooks": 0,
            "failed_hooks": 0,
            "validation_failures": 0,
            "performance_violations": 0
        }
        
        print("🔧 LangGraph Hook精准性检查系统初始化")
        print("   ✅ 支持前置和后置Hook")
        print("   🔍 支持输入输出验证")
    
    def register_hook(self, agent_type: str, hook_type: HookType, 
                     hook_func: Callable, priority: HookPriority = HookPriority.NORMAL,
                     hook_name: str = None):
        """
        注册Hook
        
        Args:
            agent_type: 智能体类型
            hook_type: Hook类型
            hook_func: Hook函数
            priority: 优先级
            hook_name: Hook名称
        """
        if agent_type not in self.hooks:
            self.hooks[agent_type] = {hook_type: [] for hook_type in HookType}
            self.hook_priorities[agent_type] = {hook_type: {} for hook_type in HookType}
        
        if hook_type not in self.hooks[agent_type]:
            self.hooks[agent_type][hook_type] = []
            self.hook_priorities[agent_type][hook_type] = {}
        
        self.hooks[agent_type][hook_type].append(hook_func)
        
        name = hook_name or getattr(hook_func, '__name__', str(hook_func))
        self.hook_priorities[agent_type][hook_type][name] = priority
        
        # 按优先级排序
        self._sort_hooks_by_priority(agent_type, hook_type)
        
        print(f"🔧 [{agent_type}] 注册Hook: {hook_type.value} - {name} (优先级: {priority.value})")
    
    def register_global_hook(self, hook_type: HookType, hook_func: Callable, hook_name: str = None):
        """注册全局Hook"""
        self.global_hooks[hook_type].append(hook_func)
        name = hook_name or getattr(hook_func, '__name__', str(hook_func))
        print(f"🌍 注册全局Hook: {hook_type.value} - {name}")
    
    def register_validation_rule(self, agent_type: str, rule_func: Callable, rule_name: str = None):
        """注册验证规则"""
        if agent_type not in self.validation_rules:
            self.validation_rules[agent_type] = []
        
        self.validation_rules[agent_type].append(rule_func)
        name = rule_name or getattr(rule_func, '__name__', str(rule_func))
        print(f"📋 [{agent_type}] 注册验证规则: {name}")
    
    async def execute_pre_hooks(self, agent_type: str, input_data: Any, 
                              context: Dict[str, Any] = None) -> List[HookResult]:
        """执行前置Hook"""
        return await self._execute_hooks(agent_type, HookType.PRE_EXECUTION, 
                                       input_data, context)
    
    async def execute_post_hooks(self, agent_type: str, output_data: Any, 
                               input_data: Any = None, context: Dict[str, Any] = None) -> List[HookResult]:
        """执行后置Hook"""
        hook_context = {**(context or {}), "input_data": input_data}
        return await self._execute_hooks(agent_type, HookType.POST_EXECUTION, 
                                       output_data, hook_context)
    
    async def validate_input(self, agent_type: str, input_data: Any) -> ValidationResult:
        """验证输入数据"""
        errors = []
        warnings = []
        metadata = {}
        
        try:
            # 执行验证规则
            rules = self.validation_rules.get(agent_type, [])
            for rule in rules:
                try:
                    result = await self._call_hook_function(rule, input_data)
                    if isinstance(result, ValidationResult):
                        errors.extend(result.errors)
                        warnings.extend(result.warnings)
                        if result.metadata:
                            metadata.update(result.metadata)
                    elif isinstance(result, dict):
                        if not result.get('valid', True):
                            errors.append(result.get('error', '验证失败'))
                    elif result is False:
                        errors.append(f"验证规则 {getattr(rule, '__name__', 'unknown')} 失败")
                        
                except Exception as e:
                    errors.append(f"验证规则执行异常: {str(e)}")
            
            # 执行验证Hook
            validation_hooks = await self._execute_hooks(agent_type, HookType.VALIDATION, input_data)
            for hook_result in validation_hooks:
                if not hook_result.success:
                    errors.append(f"验证Hook失败: {hook_result.error}")
            
            is_valid = len(errors) == 0
            if not is_valid:
                self.stats["validation_failures"] += 1
            
            print(f"🔍 [{agent_type}] 输入验证: {'✅ 通过' if is_valid else '❌ 失败'}")
            if errors:
                for error in errors:
                    print(f"   ❌ {error}")
            if warnings:
                for warning in warnings:
                    print(f"   ⚠️ {warning}")
            
            return ValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                metadata=metadata
            )
            
        except Exception as e:
            print(f"❌ 输入验证异常: {e}")
            return ValidationResult(
                is_valid=False,
                errors=[f"验证过程异常: {str(e)}"],
                warnings=[]
            )
    
    async def validate_output(self, agent_type: str, output_data: Any, 
                            input_data: Any = None) -> ValidationResult:
        """验证输出数据"""
        errors = []
        warnings = []
        metadata = {}
        
        try:
            # 基础输出检查
            if output_data is None:
                errors.append("输出数据为空")
            
            # 检查输出类型和结构
            if hasattr(output_data, '__dict__'):
                # 检查必要字段
                required_fields = ['success', 'content']
                for field in required_fields:
                    if not hasattr(output_data, field) and field not in output_data:
                        warnings.append(f"缺少推荐字段: {field}")
            
            # 执行输出验证Hook
            validation_hooks = await self._execute_hooks(agent_type, HookType.VALIDATION, 
                                                       output_data, {"input_data": input_data})
            
            for hook_result in validation_hooks:
                if not hook_result.success:
                    errors.append(f"输出验证Hook失败: {hook_result.error}")
            
            is_valid = len(errors) == 0
            
            print(f"🔍 [{agent_type}] 输出验证: {'✅ 通过' if is_valid else '❌ 失败'}")
            
            return ValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                metadata=metadata
            )
            
        except Exception as e:
            print(f"❌ 输出验证异常: {e}")
            return ValidationResult(
                is_valid=False,
                errors=[f"验证过程异常: {str(e)}"],
                warnings=[]
            )
    
    async def handle_error(self, agent_type: str, error: Exception, 
                         context: Dict[str, Any] = None) -> List[HookResult]:
        """处理错误"""
        error_context = {
            **(context or {}),
            "error": error,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc()
        }
        
        return await self._execute_hooks(agent_type, HookType.ERROR_HANDLING, 
                                       error, error_context)
    
    async def monitor_performance(self, agent_type: str, execution_time: float,
                                resource_usage: Dict[str, Any] = None) -> List[HookResult]:
        """性能监控"""
        performance_data = {
            "execution_time": execution_time,
            "resource_usage": resource_usage or {},
            "timestamp": datetime.now().isoformat()
        }
        
        # 检查性能阈值
        if execution_time > 30.0:  # 30秒阈值
            self.stats["performance_violations"] += 1
            print(f"⚠️ [{agent_type}] 性能警告: 执行时间 {execution_time:.2f}s 超过阈值")
        
        return await self._execute_hooks(agent_type, HookType.PERFORMANCE, 
                                       performance_data)
    
    async def _execute_hooks(self, agent_type: str, hook_type: HookType, 
                           data: Any, context: Dict[str, Any] = None) -> List[HookResult]:
        """执行Hook"""
        results = []
        
        try:
            # 执行全局Hook
            for hook_func in self.global_hooks.get(hook_type, []):
                result = await self._execute_single_hook(
                    f"global_{hook_type.value}", hook_func, data, context
                )
                results.append(result)
            
            # 执行智能体特定Hook
            agent_hooks = self.hooks.get(agent_type, {}).get(hook_type, [])
            for hook_func in agent_hooks:
                hook_name = getattr(hook_func, '__name__', str(hook_func))
                result = await self._execute_single_hook(
                    f"{agent_type}_{hook_name}", hook_func, data, context
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"❌ Hook执行异常: {e}")
            return results
    
    async def _execute_single_hook(self, hook_name: str, hook_func: Callable, 
                                 data: Any, context: Dict[str, Any] = None) -> HookResult:
        """执行单个Hook"""
        start_time = datetime.now()
        
        try:
            result = await self._call_hook_function(hook_func, data, context)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            hook_result = HookResult(
                hook_name=hook_name,
                hook_type=HookType.PRE_EXECUTION,  # 会被调用者覆盖
                success=True,
                execution_time=execution_time,
                result=result,
                metadata=context
            )
            
            self.stats["total_hooks_executed"] += 1
            self.stats["successful_hooks"] += 1
            self.hook_history.append(hook_result)
            
            return hook_result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            hook_result = HookResult(
                hook_name=hook_name,
                hook_type=HookType.PRE_EXECUTION,
                success=False,
                execution_time=execution_time,
                error=str(e),
                metadata=context
            )
            
            self.stats["total_hooks_executed"] += 1
            self.stats["failed_hooks"] += 1
            self.hook_history.append(hook_result)
            
            print(f"❌ Hook执行失败: {hook_name} - {str(e)}")
            return hook_result
    
    async def _call_hook_function(self, hook_func: Callable, *args) -> Any:
        """调用Hook函数"""
        if asyncio.iscoroutinefunction(hook_func):
            return await hook_func(*args)
        else:
            return hook_func(*args)
    
    def _sort_hooks_by_priority(self, agent_type: str, hook_type: HookType):
        """按优先级排序Hook"""
        hooks = self.hooks[agent_type][hook_type]
        priorities = self.hook_priorities[agent_type][hook_type]
        
        def get_priority(hook_func):
            name = getattr(hook_func, '__name__', str(hook_func))
            return priorities.get(name, HookPriority.NORMAL).value
        
        hooks.sort(key=get_priority, reverse=True)
    
    def get_hook_stats(self) -> Dict[str, Any]:
        """获取Hook统计"""
        return {
            "total_hooks_executed": self.stats["total_hooks_executed"],
            "successful_hooks": self.stats["successful_hooks"],
            "failed_hooks": self.stats["failed_hooks"],
            "success_rate": self.stats["successful_hooks"] / max(1, self.stats["total_hooks_executed"]),
            "validation_failures": self.stats["validation_failures"],
            "performance_violations": self.stats["performance_violations"],
            "registered_hooks": {
                agent_type: {hook_type.value: len(hooks) for hook_type, hooks in agent_hooks.items()}
                for agent_type, agent_hooks in self.hooks.items()
            },
            "global_hooks": {hook_type.value: len(hooks) for hook_type, hooks in self.global_hooks.items()},
            "validation_rules": {agent_type: len(rules) for agent_type, rules in self.validation_rules.items()}
        }


# Hook装饰器
def with_hooks(agent_type: str, hook_manager: LangGraphHookManager = None):
    """Hook装饰器"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if hook_manager is None:
                return await func(*args, **kwargs)
            
            # 执行前置Hook
            if args:
                await hook_manager.execute_pre_hooks(agent_type, args[0])
            
            try:
                # 执行原函数
                start_time = datetime.now()
                result = await func(*args, **kwargs)
                execution_time = (datetime.now() - start_time).total_seconds()
                
                # 执行后置Hook
                await hook_manager.execute_post_hooks(agent_type, result, args[0] if args else None)
                
                # 性能监控
                await hook_manager.monitor_performance(agent_type, execution_time)
                
                return result
                
            except Exception as e:
                # 错误处理Hook
                await hook_manager.handle_error(agent_type, e)
                raise
        
        return wrapper
    return decorator


# 全局Hook管理器实例
_hook_manager_instance = None

def get_hook_manager() -> LangGraphHookManager:
    """获取Hook管理器单例"""
    global _hook_manager_instance
    if _hook_manager_instance is None:
        _hook_manager_instance = LangGraphHookManager()
    return _hook_manager_instance
