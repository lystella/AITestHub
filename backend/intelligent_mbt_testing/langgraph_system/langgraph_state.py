#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangGraph状态管理 - 兼容现有系统的所有状态
"""

from typing import TypedDict, Annotated, Dict, List, Any, Optional
from langgraph.graph.message import add_messages
from datetime import datetime

# 自定义状态更新函数，避免并发冲突
def safe_update_field(current_value: Any, new_value: Any) -> Any:
    """安全的字段更新函数，避免并发冲突"""
    if new_value is not None:
        # 对于列表类型，支持追加操作
        if isinstance(current_value, list) and isinstance(new_value, list):
            # 如果新值是空列表，直接返回新值（重置）
            if not new_value:
                return new_value
            # 否则合并列表，避免重复
            combined = current_value.copy() if current_value else []
            for item in new_value:
                if item not in combined:
                    combined.append(item)
            return combined
        # 对于字典类型，支持合并操作
        elif isinstance(current_value, dict) and isinstance(new_value, dict):
            # 如果新值是空字典，直接返回新值（重置）
            if not new_value:
                return new_value
            # 否则合并字典
            combined = current_value.copy() if current_value else {}
            combined.update(new_value)
            return combined
        # 对于数值类型，支持累加操作（如error_count）
        elif isinstance(current_value, int) and isinstance(new_value, int):
            # 如果新值为0，直接返回（重置）
            if new_value == 0:
                return new_value
            # 否则累加
            return (current_value or 0) + new_value
        # 其他类型直接替换
        else:
            return new_value
    return current_value

class TestingWorkflowState(TypedDict):
    """
    测试工作流状态 - 包含所有现有功能的状态管理
    """
    # 基础消息和会话
    messages: Annotated[list, add_messages]
    
    # 文件和输入 - 使用Annotated避免并发更新冲突
    file_content: Annotated[str, safe_update_field]
    file_name: Annotated[str, safe_update_field]
    workflow_id: Annotated[str, safe_update_field]
    
    # 协调阶段状态 - 使用Annotated避免并发更新冲突
    coordination_plan: Annotated[Dict[str, Any], safe_update_field]
    resource_allocation: Annotated[Dict[str, Any], safe_update_field]
    task_priorities: Annotated[List[Dict[str, Any]], safe_update_field]
    
    # 分析阶段状态 - 使用Annotated避免并发更新冲突
    analysis_results: Annotated[Dict[str, Any], safe_update_field]
    multimodal_analysis: Annotated[Dict[str, Any], safe_update_field]  # 新增：多模态分析结果
    requirements_analysis: Annotated[Dict[str, Any], safe_update_field]
    risk_assessment: Annotated[Dict[str, Any], safe_update_field]
    
    # 规划阶段状态 - 使用Annotated避免并发更新冲突
    test_strategy: Annotated[Dict[str, Any], safe_update_field]
    test_plan: Annotated[Dict[str, Any], safe_update_field]
    execution_plan: Annotated[Dict[str, Any], safe_update_field]
    
    # 数据处理状态 - 使用Annotated避免并发更新冲突
    processed_data: Annotated[Dict[str, Any], safe_update_field]
    embeddings: Annotated[List[float], safe_update_field]  # 新增：向量嵌入
    vector_search_results: Annotated[List[Dict[str, Any]], safe_update_field]  # 新增：语义搜索结果
    data_quality_metrics: Annotated[Dict[str, Any], safe_update_field]
    
    # 执行阶段状态 - 使用Annotated避免并发更新冲突
    test_cases: Annotated[List[Dict[str, Any]], safe_update_field]
    excel_data: Annotated[Dict[str, Any], safe_update_field]
    yaml_config: Annotated[Dict[str, Any], safe_update_field]
    execution_results: Annotated[List[Dict[str, Any]], safe_update_field]
    midscene_results: Annotated[List[Dict[str, Any]], safe_update_field]
    
    # Phase 2优化: 新增字段支持拆分后的节点
    environment_ready: Annotated[bool, safe_update_field]  # 环境准备状态
    midscene_config: Annotated[Dict[str, Any], safe_update_field]  # Midscene配置
    
    # 报告阶段状态 - 使用Annotated避免并发更新冲突
    final_report: Annotated[Dict[str, Any], safe_update_field]
    performance_metrics: Annotated[Dict[str, Any], safe_update_field]
    quality_assessment: Annotated[Dict[str, Any], safe_update_field]
    
    # 工作流控制 - 使用Annotated避免并发更新冲突
    current_step: Annotated[str, safe_update_field]
    step_history: Annotated[List[str], safe_update_field]
    error_count: Annotated[int, safe_update_field]
    retry_count: Annotated[int, safe_update_field]
    
    # 时间戳 - 使用Annotated避免并发更新冲突
    start_time: Annotated[str, safe_update_field]
    current_time: Annotated[str, safe_update_field]
    step_timestamps: Annotated[Dict[str, str], safe_update_field]
    
    # 错误处理 - 使用Annotated避免并发更新冲突
    errors: Annotated[List[Dict[str, Any]], safe_update_field]
    warnings: Annotated[List[Dict[str, Any]], safe_update_field]
    
    # WebSocket和流式输出 - 使用Annotated避免并发更新冲突
    websocket_session_id: Annotated[Optional[str], safe_update_field]
    streaming_enabled: Annotated[bool, safe_update_field]
    
    # 长期记忆和学习 - 使用Annotated避免并发更新冲突
    memory_context: Annotated[Dict[str, Any], safe_update_field]
    learning_insights: Annotated[Dict[str, Any], safe_update_field]

class WorkflowStateManager:
    """工作流状态管理器 - 兼容现有系统"""
    
    def __init__(self):
        self.state_history = []
        self.checkpoints = {}
        
    def create_initial_state(self, file_content: str, file_name: str, workflow_id: str = None) -> TestingWorkflowState:
        """创建初始状态 - 兼容现有系统的初始化"""
        if not workflow_id:
            workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        current_time = datetime.now().isoformat()
        
        return TestingWorkflowState(
            # 基础消息和会话
            messages=[],
            
            # 文件和输入
            file_content=file_content,
            file_name=file_name,
            workflow_id=workflow_id,
            
            # 协调阶段状态
            coordination_plan={},
            resource_allocation={},
            task_priorities=[],
            
            # 分析阶段状态
            analysis_results={},
            multimodal_analysis={},
            requirements_analysis={},
            risk_assessment={},
            
            # 规划阶段状态
            test_strategy={},
            test_plan={},
            execution_plan={},
            
            # 数据处理状态
            processed_data={},
            embeddings=[],
            vector_search_results=[],
            data_quality_metrics={},
            
            # 执行阶段状态
            test_cases=[],
            excel_data={},
            yaml_config={},
            execution_results=[],
            midscene_results=[],
            
            # 报告阶段状态
            final_report={},
            performance_metrics={},
            quality_assessment={},
            
            # 工作流控制
            current_step="initialization",
            step_history=["initialization"],
            error_count=0,
            retry_count=0,
            
            # 时间戳
            start_time=current_time,
            current_time=current_time,
            step_timestamps={"initialization": current_time},
            
            # 错误处理
            errors=[],
            warnings=[],
            
            # WebSocket和流式输出
            websocket_session_id=None,
            streaming_enabled=True,
            
            # 长期记忆和学习
            memory_context={},
            learning_insights={}
        )
    
    def update_step(self, state: TestingWorkflowState, step_name: str) -> TestingWorkflowState:
        """更新工作流步骤"""
        current_time = datetime.now().isoformat()
        
        state["current_step"] = step_name
        state["step_history"].append(step_name)
        state["current_time"] = current_time
        state["step_timestamps"][step_name] = current_time
        
        return state
    
    def add_error(self, state: TestingWorkflowState, error: Dict[str, Any]) -> TestingWorkflowState:
        """添加错误记录"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": state["current_step"],
            **error
        }
        state["errors"].append(error_entry)
        state["error_count"] += 1
        return state
    
    def add_warning(self, state: TestingWorkflowState, warning: Dict[str, Any]) -> TestingWorkflowState:
        """添加警告记录"""
        warning_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": state["current_step"],
            **warning
        }
        state["warnings"].append(warning_entry)
        return state
    
    def create_checkpoint(self, state: TestingWorkflowState, checkpoint_name: str = None) -> str:
        """创建状态检查点"""
        if not checkpoint_name:
            checkpoint_name = f"checkpoint_{state['current_step']}_{datetime.now().strftime('%H%M%S')}"
        
        # 深拷贝状态以避免引用问题
        import copy
        checkpoint_data = copy.deepcopy(dict(state))
        
        self.checkpoints[checkpoint_name] = {
            "timestamp": datetime.now().isoformat(),
            "step": state["current_step"],
            "state": checkpoint_data
        }
        
        print(f"📸 状态检查点已创建: {checkpoint_name}")
        return checkpoint_name
    
    def restore_checkpoint(self, checkpoint_name: str) -> Optional[TestingWorkflowState]:
        """恢复状态检查点"""
        if checkpoint_name in self.checkpoints:
            checkpoint_data = self.checkpoints[checkpoint_name]["state"]
            print(f"🔄 状态已恢复: {checkpoint_name}")
            return TestingWorkflowState(**checkpoint_data)
        else:
            print(f"❌ 检查点不存在: {checkpoint_name}")
            return None
    
    def get_workflow_summary(self, state: TestingWorkflowState) -> Dict[str, Any]:
        """获取工作流摘要"""
        return {
            "workflow_id": state["workflow_id"],
            "current_step": state["current_step"],
            "progress": len(state["step_history"]),
            "errors": state["error_count"],
            "warnings": len(state["warnings"]),
            "duration": self._calculate_duration(state),
            "status": self._get_workflow_status(state)
        }
    
    def _calculate_duration(self, state: TestingWorkflowState) -> float:
        """计算工作流持续时间"""
        try:
            start = datetime.fromisoformat(state["start_time"])
            current = datetime.fromisoformat(state["current_time"])
            return (current - start).total_seconds()
        except:
            return 0.0
    
    def _get_workflow_status(self, state: TestingWorkflowState) -> str:
        """获取工作流状态"""
        if state["error_count"] > 3:
            return "failed"
        elif state["current_step"] == "completed":
            return "completed"
        elif state["error_count"] > 0:
            return "warning"
        else:
            return "running"

# 全局状态管理器实例
_state_manager = None

def get_state_manager() -> WorkflowStateManager:
    """获取状态管理器单例"""
    global _state_manager
    if _state_manager is None:
        _state_manager = WorkflowStateManager()
    return _state_manager
