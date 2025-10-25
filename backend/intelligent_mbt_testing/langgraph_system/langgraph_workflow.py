#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangGraph工作流实现 - 完全兼容现有系统的协作模式
优化版本：添加Checkpoint、并行度、流式输出
"""

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing import Dict, Any
from pathlib import Path

from .langgraph_state import TestingWorkflowState, get_state_manager
from .langgraph_nodes import LangGraphNodes

class LangGraphWorkflow:
    """
    LangGraph工作流管理器
    完全复制现有AgentScope系统的协作模式：
    1. 协调规划 → 2. 分析准备 → 3. 规划设计 → 4. 数据处理 → 5. 执行测试 → 6. 报告生成
    """
    
    def __init__(self, websocket_manager=None):
        self.websocket_manager = websocket_manager
        self.state_manager = get_state_manager()
        self.nodes = LangGraphNodes(websocket_manager)
        self.workflow = None
        
        # 优化1: 添加Checkpoint支持 - 断点续传
        self.checkpointer = MemorySaver()
        
        print("🚀 LangGraph工作流系统初始化 (优化版v3.0 - Phase 2)")
        print("   📊 完全兼容现有AgentScope协作模式")
        print("   🔗 WebSocket流式输出已集成")
        print("   💾 Checkpoint机制已启用 - 支持断点续传")
        print("   ⚡ 并行优化Phase 2 - Executor节点拆分为3个")
    
    def create_workflow(self) -> StateGraph:
        """
        创建优化后的LangGraph工作流图
        优化Phase 2: 增加并行度 - 从5个并行节点扩展到7个
        将Executor拆分为3个节点以提升性能
        """
        # 创建状态图
        workflow = StateGraph(TestingWorkflowState)
        
        # 添加节点 - 优化：细粒度拆分以增加并行度
        workflow.add_node("coordinator", self.nodes.coordinator_node)
        
        # 优化：将analyzer拆分为3个并行节点
        workflow.add_node("requirement_analyzer", self.nodes.requirement_analyzer_node)
        workflow.add_node("multimodal_analyzer", self.nodes.multimodal_analyzer_node)
        workflow.add_node("risk_analyzer", self.nodes.risk_analyzer_node)
        
        # 优化：将planner拆分为2个并行节点
        workflow.add_node("test_strategy_planner", self.nodes.test_strategy_planner_node)
        workflow.add_node("execution_planner", self.nodes.execution_planner_node)
        
        # 数据处理节点
        workflow.add_node("data_processor", self.nodes.data_processor_node)
        
        # 优化Phase 2: 将executor拆分为3个节点
        workflow.add_node("test_case_generator", self.nodes.test_case_generator_node)
        workflow.add_node("environment_setup", self.nodes.environment_setup_node)
        workflow.add_node("test_case_executor", self.nodes.test_case_executor_node)
        
        # 报告节点
        workflow.add_node("reporter", self.nodes.reporter_node)
        
        # 定义边 - 优化的协作流程
        # 阶段1: 协调规划
        workflow.add_edge(START, "coordinator")
        
        # 阶段2: 并行分析和规划 (5个节点并行执行)
        workflow.add_edge("coordinator", "requirement_analyzer")
        workflow.add_edge("coordinator", "multimodal_analyzer")
        workflow.add_edge("coordinator", "risk_analyzer")
        workflow.add_edge("coordinator", "test_strategy_planner")
        workflow.add_edge("coordinator", "execution_planner")
        
        # 阶段3: 数据处理 - 等待所有5个并行节点完成
        workflow.add_edge(
            ["requirement_analyzer", "multimodal_analyzer", "risk_analyzer", 
             "test_strategy_planner", "execution_planner"],
            "data_processor"
        )
        
        # 阶段4: 测试准备 - 用例生成和环境准备并行执行 (优化Phase 2 ✨)
        workflow.add_edge("data_processor", "test_case_generator")
        workflow.add_edge("data_processor", "environment_setup")
        
        # 阶段5: 测试执行 - 等待用例生成和环境准备完成
        workflow.add_edge(
            ["test_case_generator", "environment_setup"],
            "test_case_executor"
        )
        
        # 阶段6: 报告生成
        workflow.add_edge("test_case_executor", "reporter")
        
        # 结束工作流
        workflow.add_edge("reporter", END)
        
        # 优化1: 编译时添加checkpointer
        self.workflow = workflow.compile(checkpointer=self.checkpointer)
        
        print("✅ 优化版v3.0 LangGraph工作流图创建完成")
        print("   🔄 工作流: START → 协调 → [5个并行] → 数据 → [2个并行] → 执行 → 报告 → END")
        print("   ⚡ 总节点数: 11个 (v2.0为9个)")
        print("   ⚡ 并行阶段: 2个 (分析5个 + 准备2个)")
        print("   💾 Checkpoint: 支持断点续传")
        print("   🚀 预期性能提升: 30-40秒 (Executor优化)")
        
        return self.workflow
    
    async def execute_complete_workflow(self, file_content: str, file_name: str, workflow_id: str = None) -> Dict[str, Any]:
        """
        执行完整的测试工作流
        完全兼容现有系统的execute_complete_workflow方法
        """
        if not self.workflow:
            self.create_workflow()
        
        # 创建初始状态
        initial_state = self.state_manager.create_initial_state(file_content, file_name, workflow_id)
        
        if not workflow_id:
            workflow_id = initial_state["workflow_id"]
        
        print(f"🚀 开始执行LangGraph完整测试工作流: {workflow_id}")
        
        try:
            # 广播工作流开始
            if self.websocket_manager:
                await self.websocket_manager.broadcast_log(workflow_id, "🚀 开始执行完整测试工作流", "info", "System")
            
            # 优化1: 执行工作流 - 使用checkpoint支持断点续传
            config = {
                "configurable": {
                    "thread_id": workflow_id  # 使用workflow_id作为thread_id
                }
            }
            final_state = await self.workflow.ainvoke(initial_state, config=config)
            
            # 构建返回结果 - 兼容现有API格式
            result = {
                "success": True,
                "workflow_id": workflow_id,
                "summary": self.state_manager.get_workflow_summary(final_state),
                
                # 兼容现有系统的返回格式
                "coordination_result": final_state.get("coordination_plan", {}),
                "analysis_results": final_state.get("analysis_results", {}),
                "test_plan": final_state.get("test_plan", {}),
                "execution_results": final_state.get("execution_results", []),
                "final_report": final_state.get("final_report", {}),
                
                # 新增的LangGraph功能
                "multimodal_analysis": final_state.get("multimodal_analysis", {}),
                "vector_search_results": final_state.get("vector_search_results", []),
                "embeddings_count": len(final_state.get("embeddings", [])),
                
                # 状态和性能信息
                "state": final_state,
                "performance_metrics": final_state.get("performance_metrics", {}),
                "error_count": final_state.get("error_count", 0),
                "warnings_count": len(final_state.get("warnings", [])),
                
                # 兼容字段
                "test_cases": final_state.get("test_cases", []),
                "excel_data": final_state.get("excel_data", {}),
                "yaml_config": final_state.get("yaml_config", {}),
                "midscene_results": final_state.get("midscene_results", [])
            }
            
            # 广播工作流完成
            if self.websocket_manager:
                await self.websocket_manager.broadcast_log(workflow_id, "🎉 完整测试工作流执行完成", "success", "System")
                await self.websocket_manager.broadcast_step_complete(workflow_id, "workflow_complete", "工作流完成", result["summary"])
            
            print(f"🎉 LangGraph工作流执行完成: {workflow_id}")
            print(f"   📊 测试用例: {len(result['test_cases'])}")
            print(f"   ⏱️ 执行时间: {result['performance_metrics'].get('total_duration', 0):.1f}s")
            print(f"   ✅ 成功率: {result['performance_metrics'].get('success_rate', 0):.1%}")
            
            return result
            
        except Exception as e:
            error_msg = f"工作流执行失败: {str(e)}"
            print(f"❌ {error_msg}")
            
            if self.websocket_manager:
                await self.websocket_manager.broadcast_log(workflow_id, f"❌ {error_msg}", "error", "System")
            
            return {
                "success": False,
                "workflow_id": workflow_id,
                "error": error_msg,
                "summary": {"status": "failed", "error": error_msg}
            }
    
    def get_workflow_visualization(self) -> Dict[str, Any]:
        """
        获取工作流可视化信息
        优化v3.0: 更新为拆分后的工作流结构
        """
        return {
            "nodes": [
                {"id": "coordinator", "label": "协调节点", "type": "coordinator", "stage": 1},
                {"id": "requirement_analyzer", "label": "需求分析", "type": "analyzer", "stage": 2, "parallel": True},
                {"id": "multimodal_analyzer", "label": "多模态分析", "type": "analyzer", "stage": 2, "parallel": True},
                {"id": "risk_analyzer", "label": "风险分析", "type": "analyzer", "stage": 2, "parallel": True},
                {"id": "test_strategy_planner", "label": "测试策略", "type": "planner", "stage": 2, "parallel": True},
                {"id": "execution_planner", "label": "执行计划", "type": "planner", "stage": 2, "parallel": True},
                {"id": "data_processor", "label": "数据处理", "type": "data_processor", "stage": 3},
                {"id": "test_case_generator", "label": "用例生成", "type": "executor", "stage": 4, "parallel": True},
                {"id": "environment_setup", "label": "环境准备", "type": "executor", "stage": 4, "parallel": True},
                {"id": "test_case_executor", "label": "用例执行", "type": "executor", "stage": 5},
                {"id": "reporter", "label": "报告生成", "type": "reporter", "stage": 6}
            ],
            "edges": [
                {"from": "START", "to": "coordinator"},
                # 第一并行阶段
                {"from": "coordinator", "to": "requirement_analyzer"},
                {"from": "coordinator", "to": "multimodal_analyzer"},
                {"from": "coordinator", "to": "risk_analyzer"},
                {"from": "coordinator", "to": "test_strategy_planner"},
                {"from": "coordinator", "to": "execution_planner"},
                # 汇聚到数据处理
                {"from": "requirement_analyzer", "to": "data_processor"},
                {"from": "multimodal_analyzer", "to": "data_processor"},
                {"from": "risk_analyzer", "to": "data_processor"},
                {"from": "test_strategy_planner", "to": "data_processor"},
                {"from": "execution_planner", "to": "data_processor"},
                # 第二并行阶段
                {"from": "data_processor", "to": "test_case_generator"},
                {"from": "data_processor", "to": "environment_setup"},
                # 汇聚到执行
                {"from": "test_case_generator", "to": "test_case_executor"},
                {"from": "environment_setup", "to": "test_case_executor"},
                # 报告
                {"from": "test_case_executor", "to": "reporter"},
                {"from": "reporter", "to": "END"}
            ],
            "flow_type": "multi_stage_parallel",
            "estimated_duration": "2-3分钟",
            "parallel_stages": [
                {"stage": 2, "nodes": 5, "description": "分析和规划"},
                {"stage": 4, "nodes": 2, "description": "测试准备"}
            ],
            "optimization_version": "v3.0",
            "total_nodes": 11,
            "performance_improvement": "30-40秒 (相比v2.0)"
        }
    
    async def execute_single_step(self, step_name: str, state: TestingWorkflowState) -> TestingWorkflowState:
        """
        执行单个工作流步骤
        用于调试和增量执行
        """
        if step_name == "coordinator":
            return await self.nodes.coordinator_node(state)
        elif step_name == "analyzer":
            return await self.nodes.analyzer_node(state)
        elif step_name == "planner":
            return await self.nodes.planner_node(state)
        elif step_name == "data_processor":
            return await self.nodes.data_processor_node(state)
        elif step_name == "executor":
            return await self.nodes.executor_node(state)
        elif step_name == "reporter":
            return await self.nodes.reporter_node(state)
        else:
            raise ValueError(f"未知的工作流步骤: {step_name}")

# 全局工作流实例
_workflow_instance = None

def get_langgraph_workflow(websocket_manager=None) -> LangGraphWorkflow:
    """获取LangGraph工作流单例"""
    global _workflow_instance
    if _workflow_instance is None:
        _workflow_instance = LangGraphWorkflow(websocket_manager)
    return _workflow_instance
