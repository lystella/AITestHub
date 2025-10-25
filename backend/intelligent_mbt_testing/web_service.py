# -*- coding: utf-8 -*-
"""
LangGraph智能测试系统 - Web服务接口
纯LangGraph实现，移除了所有AgentScope相关代码
"""

import os
import asyncio
import json
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel

# 设置API密钥
os.environ["DASHSCOPE_API_KEY"] = "sk-343983e4232340128017e03e90f79070"

from unified_intelligent_testing_system import create_unified_intelligent_testing_system
from websocket_manager import websocket_manager

# 请求模型
class TestRequest(BaseModel):
    test_type: str = "ui_testing"
    tasks: list = []
    params: dict = {}

class EnhancedWorkflowRequest(BaseModel):
    file_content: str
    file_name: str = "test_file.txt"
    params: dict = {}

class TestResponse(BaseModel):
    success: bool
    request_id: str
    result: dict
    timestamp: str

# 创建FastAPI应用
app = FastAPI(
    title="LangGraph智能测试系统 API",
    description="基于LangGraph的下一代多智能体测试系统",
    version="2.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
testing_system = None
system_ready = False

@app.on_event("startup")
async def startup_event():
    """启动时初始化LangGraph系统"""
    global testing_system, system_ready
    
    print("🚀 初始化一体化LangGraph智能测试系统...")
    testing_system = create_unified_intelligent_testing_system()
    testing_system.set_websocket_manager(websocket_manager)
    
    try:
        init_result = await testing_system.initialize_system()
        if init_result.get("success", False):
            system_ready = True
            print("✅ 一体化LangGraph测试系统初始化成功！")
            print("🎯 系统特性:")
            print("   🤖 6个专业智能体完整协作")
            print("   🖼️ 原生多模态分析 (qwen-vl-max)")
            print("   🧠 强大向量搜索 (text-embedding-v4)")
            print("   💾 长期记忆与经验学习")
            print("   📡 实时消息广播机制")
            print("   🔧 Hook精准性检查")
            print("   📊 完整追踪与监控")
        else:
            print(f"❌ 测试系统初始化失败: {init_result.get('error', '未知错误')}")
    except Exception as e:
        print(f"❌ 测试系统启动异常: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """关闭时清理资源"""
    global testing_system
    if testing_system:
        try:
            await testing_system.shutdown_system()
            print("✅ LangGraph系统已优雅关闭")
        except Exception as e:
            print(f"⚠️ 系统关闭时出现异常: {e}")

# WebSocket连接管理
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket连接端点"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 处理WebSocket消息
            await websocket_manager.broadcast_log(f"收到消息: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

@app.get("/")
async def root():
    """根路径 - 系统信息"""
    return {
        "system": "LangGraph智能测试系统",
        "version": "2.0.0",
        "status": "运行中" if system_ready else "初始化中",
        "framework": "LangGraph",
        "features": {
            "multimodal_support": True,
            "vector_search": True,
            "workflow_visualization": True,
            "advanced_state_management": True,
            "long_term_memory": True,
            "message_broadcasting": True,
            "hook_checks": True,
            "advanced_tracing": True
        }
    }

@app.get("/status")
async def get_status():
    """获取系统状态"""
    if not system_ready or not testing_system:
        return {
            "status": "initializing",
            "message": "系统正在初始化中..."
        }
    
    try:
        system_status = await testing_system.get_system_status()
        return {
            "status": "ready",
            "framework": "LangGraph",
            "system_info": system_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"获取状态失败: {str(e)}"
        }

@app.get("/test-reports/summary")
async def get_test_reports_summary():
    """获取测试报告摘要"""
    if not system_ready or not testing_system:
        raise HTTPException(status_code=503, detail="系统未就绪")
    
    try:
        summary = await testing_system.get_test_reports_summary()
        return {
            "success": True,
            "data": summary,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取报告摘要失败: {str(e)}")

@app.get("/test-reports/executions")
async def get_test_executions():
    """获取测试执行历史"""
    if not system_ready or not testing_system:
        raise HTTPException(status_code=503, detail="系统未就绪")
    
    try:
        executions = await testing_system.get_test_executions()
        return {
            "success": True,
            "data": executions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取执行历史失败: {str(e)}")

@app.post("/enhanced-test-workflow")
async def execute_enhanced_test_workflow(request: EnhancedWorkflowRequest):
    """执行增强测试工作流"""
    if not system_ready or not testing_system:
        raise HTTPException(status_code=503, detail="系统未就绪")
    
    try:
        # 执行工作流（注意：execute_complete_workflow只接受file_content和file_name参数）
        # params中的其他参数（如document_size, enable_streaming等）被忽略
        workflow_result = await testing_system.execute_complete_workflow(
            file_content=request.file_content,
            file_name=request.file_name
        )
        
        return {
            "success": workflow_result.get("success", False),
            "workflow_id": workflow_result.get("workflow_id"),
            "result": workflow_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        import traceback
        error_detail = f"工作流执行失败: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ API错误详情:\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"工作流执行失败: {str(e)}")

@app.get("/langgraph/workflow-visualization")
async def get_workflow_visualization():
    """获取LangGraph工作流可视化"""
    if not system_ready or not testing_system:
        raise HTTPException(status_code=503, detail="系统未就绪")
    
    try:
        visualization = await testing_system.get_workflow_visualization()
        return {
            "success": True,
            "data": visualization,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工作流可视化失败: {str(e)}")

@app.get("/execution-analytics")
async def get_execution_analytics():
    """获取执行分析"""
    if not system_ready or not testing_system:
        raise HTTPException(status_code=503, detail="系统未就绪")
    
    try:
        analytics = await testing_system.get_execution_analytics()
        return {
            "success": True,
            "data": analytics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取执行分析失败: {str(e)}")

@app.get("/system-status-detailed")
async def get_system_status_detailed():
    """获取详细系统状态"""
    if not system_ready or not testing_system:
        raise HTTPException(status_code=503, detail="系统未就绪")
    
    try:
        detailed_status = await testing_system.get_system_status_detailed()
        return {
            "success": True,
            "data": detailed_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取详细状态失败: {str(e)}")

@app.get("/framework-info")
async def get_framework_info():
    """获取框架信息"""
    return {
        "framework": "LangGraph",
        "version": "2.0.0",
        "description": "基于LangGraph的下一代多智能体测试系统",
        "features": {
            "multimodal_support": True,
            "vector_search": True,
            "workflow_visualization": True,
            "advanced_state_management": True,
            "long_term_memory": True,
            "message_broadcasting": True,
            "hook_checks": True,
            "advanced_tracing": True
        },
        "agents": [
            "CoordinatorAgent - 协调智能体",
            "AnalysisAgent - 分析智能体", 
            "PlannerAgent - 规划智能体",
            "DataProcessorAgent - 数据处理智能体",
            "ExecutorAgent - 执行智能体",
            "ReporterAgent - 报告智能体"
        ],
        "models": {
            "chat": "qwen-plus",
            "multimodal": "qwen-vl-max", 
            "embedding": "text-embedding-v4"
        }
    }

if __name__ == "__main__":
    print("🚀 启动LangGraph智能测试系统Web服务")
    print("=" * 60)
    print("📡 服务地址: http://localhost:8090")
    print("📊 API文档: http://localhost:8090/docs")
    print("🔗 WebSocket: ws://localhost:8090/ws")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8090,
        reload=False,
        access_log=True
    )
