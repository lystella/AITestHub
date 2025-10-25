#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的记忆存储功能
"""

import asyncio
import os

# 设置API密钥
os.environ["DASHSCOPE_API_KEY"] = "sk-343983e4232340128017e03e90f79070"

async def test_memory_storage():
    """测试记忆存储功能"""
    print("🧪 测试修复后的记忆存储功能")
    print("=" * 50)
    
    try:
        from unified_intelligent_testing_system import create_unified_intelligent_testing_system
        
        # 创建系统
        system = create_unified_intelligent_testing_system()
        
        # 初始化系统
        init_result = await system.initialize_system()
        
        if init_result.get('success', False):
            print("✅ 系统初始化成功，没有存储经验失败的错误！")
            
            # 测试手动存储经验
            memory_id = await system.long_term_memory.store_experience(
                agent_type="test",
                experience_type="success",
                content="测试记忆存储修复",
                metadata={"test": True},
                success_score=0.8
            )
            
            if memory_id:
                print(f"✅ 手动存储经验成功: {memory_id}")
            else:
                print("❌ 手动存储经验失败")
                
            return True
        else:
            print("❌ 系统初始化失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_memory_storage())
