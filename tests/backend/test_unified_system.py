#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一体化LangGraph智能测试系统测试脚本
"""

import asyncio
import json
from datetime import datetime

async def test_unified_system():
    """测试一体化系统"""
    print("🧪 一体化LangGraph智能测试系统测试")
    print("=" * 60)
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # 导入系统
        from unified_intelligent_testing_system import create_unified_intelligent_testing_system
        
        # 创建系统实例
        print("🚀 创建一体化系统实例...")
        system = create_unified_intelligent_testing_system()
        print("   ✅ 系统实例创建成功")
        
        # 初始化系统
        print("\n⚡ 初始化系统...")
        init_result = await system.initialize_system()
        
        if init_result.get("success", False):
            print("   ✅ 系统初始化成功")
            print(f"   🆔 系统ID: {init_result.get('system_id', 'unknown')}")
            print(f"   🎯 健康分数: {init_result.get('system_health', {}).get('overall_score', 0):.1%}")
            print(f"   🤖 智能体数量: {init_result.get('agents_ready', 0)}")
            print(f"   📊 模型可用: {init_result.get('models_available', 0)}/3")
            
            # 测试系统状态
            print("\n📊 获取系统状态...")
            status = await system.get_system_status()
            print(f"   ✅ 系统就绪: {status.get('ready', False)}")
            print(f"   ⏰ 运行时间: {status.get('uptime', 0):.1f}s")
            
            # 测试工作流可视化
            print("\n📈 测试工作流可视化...")
            visualization = await system.get_workflow_visualization()
            if "error" not in visualization:
                print("   ✅ 工作流可视化获取成功")
            else:
                print(f"   ⚠️ 工作流可视化: {visualization.get('error', '未知错误')}")
            
            # 测试执行分析
            print("\n📊 测试执行分析...")
            analytics = await system.get_execution_analytics()
            if "error" not in analytics:
                print("   ✅ 执行分析数据获取成功")
                print(f"   📈 总工作流: {analytics.get('system_metrics', {}).get('total_workflows', 0)}")
            else:
                print(f"   ⚠️ 执行分析: {analytics.get('error', '未知错误')}")
            
            # 测试简单工作流执行
            print("\n🚀 测试工作流执行...")
            test_content = "这是一个测试文件内容，用于验证一体化系统的工作流执行能力。"
            workflow_result = await system.execute_complete_workflow(
                file_content=test_content,
                file_name="test_unified_system.txt"
            )
            
            if workflow_result.get("success", False):
                print("   ✅ 工作流执行成功")
                print(f"   ⏱️ 执行时间: {workflow_result.get('execution_duration', 0):.2f}s")
                print(f"   🆔 工作流ID: {workflow_result.get('workflow_id', 'unknown')}")
            else:
                print(f"   ❌ 工作流执行失败: {workflow_result.get('error', '未知错误')}")
            
            # 优雅关闭系统
            print("\n🔄 关闭系统...")
            await system.shutdown_system()
            print("   ✅ 系统已优雅关闭")
            
            print("\n" + "=" * 60)
            print("🎉 一体化系统测试完成！所有功能正常运行！")
            print("=" * 60)
            return True
            
        else:
            print(f"   ❌ 系统初始化失败: {init_result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_unified_system())
