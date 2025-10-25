#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纯LangGraph智能测试系统启动脚本
"""

import os
import asyncio
from datetime import datetime

async def main():
    """启动纯LangGraph系统"""
    print("🚀 启动纯LangGraph智能测试系统")
    print("=" * 60)
    print(f"⏰ 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 设置API密钥
    os.environ["DASHSCOPE_API_KEY"] = "sk-343983e4232340128017e03e90f79070"
    
    try:
        # 创建系统
        from unified_intelligent_testing_system import create_unified_intelligent_testing_system
        system = create_unified_intelligent_testing_system()
        
        print("🔧 正在初始化系统...")
        
        # 初始化系统
        init_result = await system.initialize_system()
        
        if init_result.get("success", False):
            print("\n🎉 LangGraph系统启动成功!")
            print("=" * 60)
            print("📊 系统信息:")
            print(f"   🤖 智能体数量: {init_result.get('agents_count', 6)}")
            print(f"   📊 模型数量: {init_result.get('models_count', 3)}")
            print(f"   🎯 健康分数: {init_result.get('health_score', 1.0) * 100:.1f}%")
            print(f"   🧠 记忆条数: {init_result.get('memory_count', 0)}")
            print(f"   📡 通信订阅: {init_result.get('subscriptions_count', 12)}")
            
            print("\n🎯 系统特性:")
            print("   ✅ 多智能体协作")
            print("   ✅ 多模态分析 (qwen-vl-max)")
            print("   ✅ 向量搜索 (text-embedding-v4)")
            print("   ✅ 长期记忆学习")
            print("   ✅ 实时消息广播")
            print("   ✅ Hook精准检查")
            print("   ✅ 完整追踪监控")
            
            print("\n💡 使用方式:")
            print("   1. Web服务: python web_service.py")
            print("   2. 直接测试: 调用 system.execute_complete_workflow()")
            
            # 简单测试
            print("\n🧪 执行简单测试...")
            test_result = await system.execute_complete_workflow(
                file_content="这是一个简单的测试文件内容，用于验证系统功能。",
                file_name="startup_test.txt"
            )
            
            if test_result.get("success", False):
                print("✅ 测试执行成功!")
                print(f"   📄 工作流ID: {test_result.get('workflow_id')}")
                print(f"   ⏱️ 执行时间: {test_result.get('execution_time', 0):.2f}s")
            else:
                print(f"⚠️ 测试执行失败: {test_result.get('error')}")
            
            print("\n" + "=" * 60)
            print("🎯 系统运行中... 按 Ctrl+C 退出")
            
            # 保持运行
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🔄 正在关闭系统...")
                await system.shutdown_system()
                print("✅ 系统已优雅关闭")
                
        else:
            print(f"❌ 系统启动失败: {init_result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 启动过程异常: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("🎉 程序正常退出")
    else:
        print("❌ 程序异常退出")
        exit(1)