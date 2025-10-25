#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangGraph高级特性测试脚本 - 全面测试新增功能
"""

import asyncio
import json
import time
from datetime import datetime

# 测试长期记忆系统
async def test_long_term_memory():
    """测试长期记忆系统"""
    print("\n🧠 测试长期记忆系统")
    print("=" * 50)
    
    try:
        from langgraph_system.langgraph_memory import get_long_term_memory
        
        memory = get_long_term_memory()
        
        # 测试存储经验
        print("📝 测试经验存储...")
        memory_id1 = await memory.store_experience(
            agent_type="coordinator",
            experience_type="success",
            content="成功协调了复杂的多智能体任务，通过合理分工提高了效率",
            success_score=0.9
        )
        
        memory_id2 = await memory.store_experience(
            agent_type="executor",
            experience_type="failure", 
            content="执行Midscene测试时遇到超时问题，需要优化等待策略",
            success_score=0.3
        )
        
        print(f"   ✅ 存储了2条经验记录")
        
        # 测试检索相似经验
        print("🔍 测试经验检索...")
        similar_experiences = await memory.retrieve_similar_experiences(
            agent_type="coordinator",
            query="如何协调多个智能体完成复杂任务",
            top_k=3
        )
        
        print(f"   ✅ 检索到 {len(similar_experiences)} 条相似经验")
        
        # 测试成功模式
        print("📈 测试成功模式获取...")
        success_patterns = await memory.get_success_patterns("coordinator")
        print(f"   ✅ 找到 {len(success_patterns)} 个成功模式")
        
        # 测试学习反馈
        print("📚 测试反馈学习...")
        await memory.learn_from_feedback(memory_id1, 0.95, "用户反馈非常好")
        print("   ✅ 反馈学习完成")
        
        # 获取统计信息
        stats = memory.get_memory_stats()
        print("📊 记忆系统统计:")
        print(f"   📝 总记忆数: {stats['total_memories']}")
        print(f"   🎯 检索成功率: {stats['retrieval_success_rate']:.2%}")
        
        return True
        
    except Exception as e:
        print(f"❌ 长期记忆测试失败: {e}")
        return False

async def test_message_broadcast():
    """测试消息广播系统"""
    print("\n📡 测试消息广播系统")
    print("=" * 50)
    
    try:
        from langgraph_system.langgraph_broadcast import get_message_broadcaster, MessageType, MessagePriority
        
        broadcaster = get_message_broadcaster()
        
        # 测试广播消息
        print("📢 测试全体广播...")
        msg_id1 = await broadcaster.broadcast_to_all(
            sender="coordinator",
            content="开始执行新的测试任务，请各智能体准备",
            message_type=MessageType.BROADCAST,
            priority=MessagePriority.HIGH
        )
        print(f"   ✅ 广播消息ID: {msg_id1}")
        
        # 测试点对点消息
        print("📨 测试点对点消息...")
        msg_id2 = await broadcaster.send_message(
            sender="planner",
            recipients=["executor", "data_processor"],
            content="请准备执行计划中的步骤3和步骤4",
            message_type=MessageType.DIRECT,
            priority=MessagePriority.NORMAL
        )
        print(f"   ✅ 点对点消息ID: {msg_id2}")
        
        # 测试主题订阅
        print("📌 测试主题订阅...")
        await broadcaster.subscribe_to_topic("reporter", "test_results")
        await broadcaster.subscribe_to_topic("coordinator", "test_results")
        
        # 发布主题消息
        msg_id3 = await broadcaster.publish_to_topic(
            sender="executor",
            topic="test_results",
            content="测试执行完成，生成了详细报告",
            priority=MessagePriority.HIGH
        )
        print(f"   ✅ 主题消息ID: {msg_id3}")
        
        # 获取消息
        print("📬 测试消息获取...")
        messages = await broadcaster.get_messages("coordinator", limit=5)
        print(f"   ✅ 获取到 {len(messages)} 条消息")
        
        # 获取统计信息
        stats = broadcaster.get_broadcast_stats()
        print("📊 广播系统统计:")
        print(f"   📨 总消息数: {stats['total_messages']}")
        print(f"   📢 广播消息: {stats['broadcast_messages']}")
        print(f"   📩 直接消息: {stats['direct_messages']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 消息广播测试失败: {e}")
        return False

async def test_hook_manager():
    """测试Hook管理器"""
    print("\n🔧 测试Hook管理器")
    print("=" * 50)
    
    try:
        from langgraph_system.langgraph_hooks import get_hook_manager, HookType, HookPriority, ValidationResult
        
        hook_manager = get_hook_manager()
        
        # 注册测试Hook
        print("🔧 注册测试Hook...")
        
        async def pre_execution_hook(data):
            print(f"   🔄 前置Hook执行: 数据长度 {len(str(data))}")
            return {"status": "pre_hook_success"}
        
        async def validation_hook(data):
            if not data or len(str(data)) < 5:
                return ValidationResult(False, ["数据太短"], ["建议增加更多内容"])
            return ValidationResult(True, [], [])
        
        hook_manager.register_hook("test_agent", HookType.PRE_EXECUTION, pre_execution_hook, HookPriority.HIGH)
        hook_manager.register_hook("test_agent", HookType.VALIDATION, validation_hook, HookPriority.NORMAL)
        
        # 测试前置Hook
        print("🚀 测试前置Hook执行...")
        pre_results = await hook_manager.execute_pre_hooks("test_agent", "测试数据输入")
        print(f"   ✅ 前置Hook执行结果: {len(pre_results)} 个Hook")
        
        # 测试输入验证
        print("🔍 测试输入验证...")
        validation_result = await hook_manager.validate_input("test_agent", "这是一个测试输入数据")
        print(f"   ✅ 验证结果: {'通过' if validation_result.is_valid else '失败'}")
        
        # 测试输出验证
        print("✅ 测试输出验证...")
        output_validation = await hook_manager.validate_output("test_agent", {"success": True, "content": "测试输出"})
        print(f"   ✅ 输出验证: {'通过' if output_validation.is_valid else '失败'}")
        
        # 测试性能监控
        print("📊 测试性能监控...")
        perf_results = await hook_manager.monitor_performance("test_agent", 2.5, {"memory": "100MB"})
        print(f"   ✅ 性能监控结果: {len(perf_results)} 个Hook")
        
        # 获取统计信息
        stats = hook_manager.get_hook_stats()
        print("📊 Hook系统统计:")
        print(f"   🔧 总Hook执行: {stats['total_hooks_executed']}")
        print(f"   ✅ 成功率: {stats['success_rate']:.2%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Hook管理器测试失败: {e}")
        return False

async def test_tracer():
    """测试追踪系统"""
    print("\n📊 测试追踪系统")
    print("=" * 50)
    
    try:
        from langgraph_system.langgraph_tracing import get_tracer, TraceType
        
        tracer = get_tracer()
        
        # 测试基本追踪
        print("🔍 测试基本追踪...")
        span_id1 = tracer.start_trace("test_workflow", TraceType.WORKFLOW_STEP)
        
        # 模拟一些工作
        await asyncio.sleep(0.1)
        tracer.add_span_event(span_id1, "processing_data", {"items": 100})
        
        # 嵌套追踪
        span_id2 = tracer.start_trace("sub_task", TraceType.FUNCTION_CALL, parent_span_id=span_id1)
        await asyncio.sleep(0.05)
        tracer.end_trace(span_id2, {"result": "success"})
        
        tracer.end_trace(span_id1, {"final_result": "completed"})
        
        print(f"   ✅ 创建了追踪跨度: {span_id1[:8]}...")
        
        # 测试调用树
        print("🌳 测试调用树...")
        trace_id = tracer.spans[span_id1].trace_id
        call_tree = tracer.get_call_tree(trace_id)
        print(f"   ✅ 调用树包含 {call_tree['total_spans']} 个跨度")
        
        # 测试性能分析
        print("📈 测试性能分析...")
        perf_analysis = tracer.get_performance_analysis(trace_id)
        print(f"   ✅ 总耗时: {perf_analysis['total_duration']:.3f}s")
        print(f"   📊 平均跨度耗时: {perf_analysis['avg_span_duration']:.3f}s")
        
        # 获取统计信息
        stats = tracer.get_tracing_stats()
        print("📊 追踪系统统计:")
        print(f"   📈 总跨度数: {stats['total_spans']}")
        print(f"   🔄 活跃追踪: {stats['active_traces']}")
        print(f"   ✅ 完成追踪: {stats['completed_traces']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 追踪系统测试失败: {e}")
        return False

async def test_integration():
    """测试系统集成"""
    print("\n🔗 测试系统集成")
    print("=" * 50)
    
    try:
        from langgraph_system.langgraph_integration import create_langgraph_system
        
        # 创建系统实例
        print("🚀 创建LangGraph系统...")
        system = create_langgraph_system()
        
        # 初始化系统
        print("⚡ 初始化系统...")
        init_result = await system.initialize_system()
        
        if init_result["success"]:
            print("   ✅ 系统初始化成功")
            print(f"   🤖 智能体数量: {init_result['agents_ready']}")
            print(f"   📊 模型可用: {init_result['models_available']}")
            
            # 测试高级特性状态
            print("🔍 检查高级特性状态...")
            advanced_status = system.get_advanced_features_status()
            
            for feature, status in advanced_status.items():
                enabled = "✅ 启用" if status["enabled"] else "❌ 未启用"
                print(f"   {feature}: {enabled}")
            
            # 测试经验存储
            print("📝 测试经验存储...")
            exp_id = await system.store_agent_experience(
                "coordinator", "success", "系统集成测试成功完成", 0.95
            )
            if exp_id:
                print(f"   ✅ 存储经验ID: {exp_id[:8]}...")
            
            # 测试消息广播
            print("📡 测试消息广播...")
            msg_id = await system.broadcast_message(
                "system", "集成测试正在进行中", ["coordinator", "executor"]
            )
            if msg_id:
                print(f"   ✅ 广播消息ID: {msg_id[:8]}...")
            
            return True
        else:
            print(f"   ❌ 系统初始化失败: {init_result.get('error', '未知错误')}")
            return False
        
    except Exception as e:
        print(f"❌ 系统集成测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🧪 LangGraph高级特性全面测试")
    print("=" * 60)
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    test_results = {}
    
    # 执行各项测试
    test_results["long_term_memory"] = await test_long_term_memory()
    test_results["message_broadcast"] = await test_message_broadcast()
    test_results["hook_manager"] = await test_hook_manager()
    test_results["tracer"] = await test_tracer()
    test_results["integration"] = await test_integration()
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("🏆 测试结果汇总")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"🎯 总体结果: {passed}/{total} 项测试通过 ({passed/total:.1%})")
    
    if passed == total:
        print("🎉 所有高级特性测试通过！LangGraph系统功能完整！")
    else:
        print("⚠️ 部分测试失败，请检查相关功能")
    
    print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
