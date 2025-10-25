#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Midscene集成测试 - 验证AI智能体与Midscene的完整集成
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# 添加backend路径
sys.path.append(str(Path(__file__).parent / "backend" / "intelligent_mbt_testing"))

from enhanced_agents.enhanced_executor_agent import EnhancedExecutorAgent
from tools.midscene_agent_executor import MidsceneAgentExecutor, EXAMPLE_TEST_CASES

async def test_midscene_integration():
    """测试Midscene完整集成"""
    print("=" * 60)
    print("🎯 Midscene智能体集成测试")
    print("=" * 60)
    
    # 1. 测试独立Midscene执行器
    print("\n🔧 1. 测试独立Midscene执行器")
    print("-" * 40)
    
    midscene_executor = MidsceneAgentExecutor(
        headless=True,
        api_key=os.getenv("OPENAI_API_KEY", "test_key")
    )
    
    try:
        # 测试eBay搜索示例
        ebay_test_case = EXAMPLE_TEST_CASES["ebay_search"]
        print(f"📝 执行测试用例: {ebay_test_case['id']}")
        
        result = await midscene_executor.execute_ai_test_case(ebay_test_case)
        print(f"✅ 执行结果: {'成功' if result.get('success') else '失败'}")
        print(f"📊 执行时间: {result.get('execution_time', 0):.2f}s")
        print(f"🎭 执行模式: {result.get('execution_mode', 'unknown')}")
        
    except Exception as e:
        print(f"❌ 独立执行器测试失败: {e}")
    finally:
        await midscene_executor.cleanup()
    
    # 2. 测试智能体集成Midscene
    print("\n🤖 2. 测试智能体集成Midscene")
    print("-" * 40)
    
    executor_agent = EnhancedExecutorAgent(
        openai_api_key=os.getenv("OPENAI_API_KEY", "test_key")
    )
    
    try:
        # 测试Midscene AI执行
        print("🎯 测试Midscene AI执行...")
        
        ai_test_request = {
            "test_case": {
                "id": "intelligent_web_test",
                "url": "https://example.com",
                "steps": [
                    {
                        "action": "assert",
                        "data": {"assertion": "There is a heading on the page"}
                    },
                    {
                        "action": "extract",
                        "data": {
                            "query": "string, what is the main heading text?",
                            "name": "main_heading"
                        }
                    }
                ]
            },
            "options": {
                "execution_mode": "midscene_ai"
            }
        }
        
        ai_result_json = executor_agent.execute_midscene_ai_test(ai_test_request)
        ai_result = json.loads(ai_result_json)
        print(f"✅ AI执行结果: {'成功' if ai_result.get('success') else '失败'}")
        
        # 测试YAML脚本执行
        print("\n📄 测试YAML脚本执行...")
        
        yaml_content = """
web:
  url: https://example.com
  viewportWidth: 1280
  viewportHeight: 768

tasks:
  - name: simple_test
    flow:
      - aiAssert: There is content on the page
      - aiString: What is the main heading?
"""
        
        yaml_test_request = {
            "yaml_content": yaml_content,
            "yaml_config": {
                "case_id": "yaml_simple_test"
            }
        }
        
        yaml_result_json = executor_agent.execute_midscene_yaml_script(yaml_test_request)
        yaml_result = json.loads(yaml_result_json)
        print(f"✅ YAML执行结果: {'成功' if yaml_result.get('success') else '失败'}")
        
        # 测试混合模式执行
        print("\n🔀 测试混合模式执行...")
        
        hybrid_test_request = {
            "test_case": {
                "id": "hybrid_intelligence_test",
                "url": "https://www.google.com",
                "steps": [
                    {
                        "action": "input",
                        "data": {
                            "text": "Midscene.js",
                            "selector": "search box"
                        }
                    },
                    {
                        "action": "click",
                        "data": {"text": "search button"}
                    },
                    {
                        "action": "wait",
                        "data": {"condition": "search results are displayed"}
                    },
                    {
                        "action": "extract",
                        "data": {
                            "query": "{title: string, url: string}[], find first 3 search results",
                            "name": "search_results"
                        }
                    }
                ]
            },
            "options": {
                "intelligent_mode": True
            }
        }
        
        hybrid_result_json = executor_agent.execute_hybrid_midscene_test(hybrid_test_request)
        hybrid_result = json.loads(hybrid_result_json)
        print(f"✅ 混合执行结果: {'成功' if hybrid_result.get('success') else '失败'}")
        print(f"🎯 选择模式: {hybrid_result.get('optimal_mode', 'unknown')}")
        
        # 清理资源
        await executor_agent.cleanup_midscene_resources()
        
    except Exception as e:
        print(f"❌ 智能体集成测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. 性能和统计分析
    print("\n📊 3. 执行统计分析")
    print("-" * 40)
    
    try:
        stats = executor_agent.execution_stats
        print(f"总执行次数: {stats['total_executions']}")
        print(f"成功次数: {stats['successful_executions']}")
        print(f"失败次数: {stats['failed_executions']}")
        print(f"成功率: {stats.get('success_rate', 0):.1f}%")
        print(f"平均执行时间: {stats.get('average_execution_time', 0):.2f}s")
        
        # 获取Midscene执行器统计
        if hasattr(executor_agent, 'midscene_executor'):
            midscene_stats = executor_agent.midscene_executor.get_stats()
            print(f"\nMidscene执行统计:")
            print(f"- Playwright执行: {midscene_stats.get('playwright_executions', 0)}次")
            print(f"- YAML执行: {midscene_stats.get('yaml_executions', 0)}次")
            print(f"- 平均执行时间: {midscene_stats.get('average_execution_time', 0):.2f}s")
    
    except Exception as e:
        print(f"⚠️ 统计分析异常: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Midscene集成测试完成!")
    print("=" * 60)

def test_midscene_examples():
    """测试Midscene示例用例"""
    print("\n📋 Midscene示例用例展示:")
    print("-" * 40)
    
    for name, test_case in EXAMPLE_TEST_CASES.items():
        print(f"\n📝 {name}:")
        print(f"   ID: {test_case['id']}")
        print(f"   URL: {test_case['url']}")
        print(f"   模式: {test_case['mode']}")
        print(f"   操作数量: {len(test_case['actions'])}")
        
        # 显示前3个操作
        for i, action in enumerate(test_case['actions'][:3]):
            action_type = action.get('type', 'unknown')
            if action_type == 'aiAction':
                print(f"   - 操作{i+1}: AI动作 - {action.get('instruction', '')}")
            elif action_type == 'aiQuery':
                print(f"   - 操作{i+1}: AI查询 - {action.get('query', '')}")
            elif action_type == 'aiAssert':
                print(f"   - 操作{i+1}: AI断言 - {action.get('assertion', '')}")
            else:
                print(f"   - 操作{i+1}: {action_type}")
        
        if len(test_case['actions']) > 3:
            print(f"   ... 还有{len(test_case['actions']) - 3}个操作")

def main():
    """主函数"""
    print("🚀 启动Midscene智能体集成测试")
    
    # 检查环境
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ 警告: 未设置OPENAI_API_KEY环境变量，使用模拟模式")
    
    # 显示示例用例
    test_midscene_examples()
    
    # 运行集成测试
    try:
        asyncio.run(test_midscene_integration())
    except KeyboardInterrupt:
        print("\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试执行异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
