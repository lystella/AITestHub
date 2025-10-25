#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的LangGraph系统
"""

import asyncio
import os
from datetime import datetime

# 设置API密钥
os.environ["DASHSCOPE_API_KEY"] = "sk-343983e4232340128017e03e90f79070"

async def test_system_initialization():
    """测试系统初始化"""
    print("🧪 测试1: 系统初始化")
    print("=" * 50)
    
    try:
        from unified_intelligent_testing_system import create_unified_intelligent_testing_system
        
        # 创建系统
        system = create_unified_intelligent_testing_system()
        print("✅ 系统创建成功")
        
        # 初始化系统
        init_result = await system.initialize_system()
        print(f"✅ 系统初始化: {init_result.get('success', False)}")
        
        # 检查系统状态
        status = await system.get_system_status()
        print(f"✅ 系统状态: {status}")
        
        return system
        
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        return None

async def test_memory_system(system):
    """测试记忆系统"""
    print("\n🧪 测试2: 记忆系统")
    print("=" * 50)
    
    try:
        # 测试存储经验
        memory_id = await system.long_term_memory.store_experience(
            agent_type="system",
            experience_type="test",
            content="这是一个测试经验",
            metadata={"test": True},
            success_score=0.8
        )
        print(f"✅ 经验存储成功: {memory_id}")
        
        # 测试检索经验
        memories = await system.long_term_memory.retrieve_similar_experiences(
            agent_type="system",
            query="测试经验",
            top_k=3
        )
        print(f"✅ 经验检索成功: {len(memories)} 条")
        
        # 获取记忆统计
        stats = system.long_term_memory.get_memory_stats()
        print(f"✅ 记忆统计: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ 记忆系统测试失败: {e}")
        return False

async def test_broadcast_system(system):
    """测试广播系统"""
    print("\n🧪 测试3: 广播系统")
    print("=" * 50)
    
    try:
        # 测试广播消息
        from langgraph_system.langgraph_broadcast import MessagePriority
        await system.message_broadcaster.broadcast_to_all(
            sender="test_system",
            content="测试广播消息",
            priority=MessagePriority.HIGH
        )
        print("✅ 广播消息发送成功")
        
        # 测试点对点消息
        await system.message_broadcaster.send_message(
            sender="test_system",
            recipients=["coordinator"],
            content="测试点对点消息",
            priority=MessagePriority.NORMAL
        )
        print("✅ 点对点消息发送成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 广播系统测试失败: {e}")
        return False

async def test_hook_system(system):
    """测试Hook系统"""
    print("\n🧪 测试4: Hook系统")
    print("=" * 50)
    
    try:
        # 测试Hook执行
        test_data = {"test": "data"}
        
        # 执行前置Hook
        pre_result = await system.hook_manager.execute_pre_hooks(
            agent_type="test_agent",
            input_data=test_data
        )
        print(f"✅ 前置Hook执行: {pre_result}")
        
        # 执行后置Hook
        post_result = await system.hook_manager.execute_post_hooks(
            agent_type="test_agent",
            output_data=test_data
        )
        print(f"✅ 后置Hook执行: {post_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Hook系统测试失败: {e}")
        return False

async def test_simple_workflow(system):
    """测试简单工作流"""
    print("\n🧪 测试5: 简单工作流")
    print("=" * 50)
    
    try:
        # 创建测试文件内容
        test_content = """
        # 测试文件
        这是一个简单的测试文件，用于验证LangGraph工作流。
        
        ## 测试内容
        - 功能测试
        - 性能测试
        - 集成测试
        """
        
        # 执行工作流（简化版本，不执行完整流程）
        print("🚀 开始执行简化工作流...")
        
        # 只测试状态管理
        from langgraph_system.langgraph_state import get_state_manager
        state_manager = get_state_manager()
        
        initial_state = state_manager.create_initial_state(
            file_content=test_content,
            file_name="test_file.txt",
            workflow_id="test_workflow_001"
        )
        
        print(f"✅ 初始状态创建成功: {initial_state['workflow_id']}")
        
        # 测试状态更新
        updated_state = state_manager.update_step(initial_state, "testing")
        print(f"✅ 状态更新成功: {updated_state['current_step']}")
        
        # 获取工作流摘要
        summary = state_manager.get_workflow_summary(updated_state)
        print(f"✅ 工作流摘要: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ 简单工作流测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🚀 开始测试修复后的LangGraph系统")
    print("=" * 60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 测试结果
    results = {}
    
    # 测试1: 系统初始化
    system = await test_system_initialization()
    results["initialization"] = system is not None
    
    if system:
        # 测试2: 记忆系统
        results["memory"] = await test_memory_system(system)
        
        # 测试3: 广播系统
        results["broadcast"] = await test_broadcast_system(system)
        
        # 测试4: Hook系统
        results["hooks"] = await test_hook_system(system)
        
        # 测试5: 简单工作流
        results["workflow"] = await test_simple_workflow(system)
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("🎯 测试结果汇总")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name:15} : {status}")
    
    print(f"\n📊 总体结果: {passed_tests}/{total_tests} 测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！LangGraph系统运行正常！")
    else:
        print("⚠️ 部分测试失败，需要进一步调试。")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    asyncio.run(main())
