#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Midscene集成演示 - 展示AI智能体与Midscene的完整集成能力
"""

import json
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# 添加backend路径
sys.path.append(str(Path(__file__).parent / "backend" / "intelligent_mbt_testing"))

def print_banner(title: str):
    """打印标题横幅"""
    print("\n" + "=" * 80)
    print(f"🎯 {title}")
    print("=" * 80)

def print_section(title: str):
    """打印章节标题"""
    print(f"\n📋 {title}")
    print("-" * 60)

def print_result(success: bool, message: str, details: str = ""):
    """打印结果"""
    icon = "✅" if success else "❌"
    print(f"{icon} {message}")
    if details:
        print(f"   📝 {details}")

async def demo_midscene_capabilities():
    """演示Midscene AI能力"""
    print_banner("Midscene AI自动化测试能力演示")
    
    # 导入必要的模块
    try:
        from tools.midscene_agent_executor import MidsceneAgentExecutor, EXAMPLE_TEST_CASES
        from enhanced_agents.enhanced_executor_agent import EnhancedExecutorAgent
    except ImportError as e:
        print_result(False, f"模块导入失败: {e}")
        return
    
    print_section("1. Midscene核心功能介绍")
    
    print("🎯 Midscene是一个AI驱动的Web自动化测试框架，具有以下特点：")
    print("   • AI理解：使用自然语言描述测试操作")
    print("   • 智能识别：AI自动识别页面元素和内容")
    print("   • 多模式支持：Playwright编程模式、YAML声明模式")
    print("   • 数据提取：智能提取结构化数据")
    print("   • 自动断言：AI验证页面状态和内容")
    
    print_section("2. 支持的AI操作类型")
    
    ai_operations = {
        "aiAction": "AI驱动的页面操作（点击、输入、导航等）",
        "aiQuery": "AI结构化数据查询和提取",
        "aiAssert": "AI智能断言验证",
        "aiWaitFor": "AI等待特定条件满足",
        "aiTap": "AI智能点击目标元素",
        "aiString": "AI提取文本信息",
        "aiNumber": "AI提取数值信息", 
        "aiBoolean": "AI判断真假",
        "aiLocate": "AI定位元素位置"
    }
    
    for operation, description in ai_operations.items():
        print(f"   🔧 {operation}: {description}")
    
    print_section("3. 内置测试用例示例")
    
    for name, test_case in EXAMPLE_TEST_CASES.items():
        print(f"\n📝 {name.upper()}:")
        print(f"   🌐 URL: {test_case['url']}")
        print(f"   🎭 模式: {test_case['mode']}")
        print(f"   ⚡ 操作数: {len(test_case['actions'])}")
        
        # 显示前2个操作作为示例
        for i, action in enumerate(test_case['actions'][:2]):
            action_type = action.get('type', 'unknown')
            if action_type == 'aiAction':
                print(f"   • 操作{i+1}: AI动作 - '{action.get('instruction', '')}'")
            elif action_type == 'aiQuery':
                print(f"   • 操作{i+1}: AI查询 - '{action.get('query', '')}'")
            elif action_type == 'aiAssert':
                print(f"   • 操作{i+1}: AI断言 - '{action.get('assertion', '')}'")
            else:
                print(f"   • 操作{i+1}: {action_type}")
    
    print_section("4. 智能体集成架构")
    
    print("🏗️ 集成架构层次：")
    print("   ┌─ EnhancedExecutorAgent (智能执行体)")
    print("   │  ├─ 原有测试执行功能")
    print("   │  └─ 新增Midscene AI功能")
    print("   │     ├─ execute_midscene_ai_test() - AI模式")
    print("   │     ├─ execute_midscene_yaml_script() - YAML模式") 
    print("   │     └─ execute_hybrid_midscene_test() - 混合模式")
    print("   │")
    print("   └─ MidsceneAgentExecutor (Midscene执行器)")
    print("      ├─ 智能模式选择算法")
    print("      ├─ 测试用例格式转换")
    print("      ├─ 执行环境管理")
    print("      └─ 性能统计和监控")
    
    print_section("5. 执行模式智能选择")
    
    print("🧠 系统根据测试复杂度自动选择最佳执行模式：")
    print("   • 复杂度评分 ≥ 5分 → Playwright模式（复杂逻辑、动态交互）")
    print("   • 复杂度评分 ≤ 2分 → YAML模式（简单流程、标准化测试）")
    print("   • 复杂度评分 3-4分 → Auto模式（自动优化选择）")
    print("\n🔍 复杂度评分标准：")
    print("   • 复杂操作（extract、query、conditional）: +2分")
    print("   • 动态内容（wait、retry、variable）: +1分")
    print("   • 并行执行需求: +3分")
    
    print_section("6. 实际应用场景")
    
    scenarios = [
        {
            "name": "电商网站测试",
            "description": "商品搜索、价格对比、购物车操作",
            "example": "在eBay搜索耳机，提取商品信息，验证筛选功能"
        },
        {
            "name": "搜索引擎测试", 
            "description": "搜索功能、结果验证、相关推荐",
            "example": "Google搜索技术关键词，提取搜索结果，验证相关性"
        },
        {
            "name": "表单交互测试",
            "description": "登录注册、数据提交、验证反馈",
            "example": "用户登录流程，表单填写，错误处理验证"
        },
        {
            "name": "内容管理测试",
            "description": "内容发布、编辑修改、状态管理",
            "example": "CMS文章发布，内容编辑，发布状态验证"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🎯 {scenario['name']}:")
        print(f"   📄 功能: {scenario['description']}")
        print(f"   💡 示例: {scenario['example']}")
    
    print_section("7. 性能优势")
    
    advantages = [
        "AI理解能力：无需精确选择器，使用自然语言描述",
        "自适应性强：页面改版时测试用例仍然有效",
        "开发效率高：减少90%的选择器维护工作",
        "测试覆盖全：AI能发现人工容易遗漏的边界情况",
        "智能修复：自动适应页面变化，减少测试脆性",
        "多模式支持：根据场景自动选择最优执行方式"
    ]
    
    for i, advantage in enumerate(advantages, 1):
        print(f"   {i}. ✨ {advantage}")
    
    print_section("8. 与现有系统的协同")
    
    print("🔗 Midscene与智能体系统的协同优势：")
    print("   • 无缝集成：完全兼容现有ExecutorAgent架构")
    print("   • 智能调度：CoordinatorAgent可智能选择Midscene执行")
    print("   • 数据流通：AnalysisAgent分析结果可直接用于Midscene测试")
    print("   • 报告统一：ReporterAgent统一生成包含Midscene结果的报告")
    print("   • 错误修复：智能修复机制可自动优化Midscene测试用例")
    
    print_section("9. 未来扩展计划")
    
    future_plans = [
        "移动端支持：集成Android/iOS自动化测试",
        "多模型支持：支持Qwen、Claude等更多LLM模型",
        "可视化报告：增强测试报告的可视化展示",
        "智能修复：AI自动修复失败的测试用例",
        "性能测试：集成Web性能监控和分析",
        "API测试：扩展到API接口自动化测试"
    ]
    
    for plan in future_plans:
        print(f"   🚀 {plan}")
    
    print_banner("Midscene集成演示完成")
    
    print("🎉 恭喜！您的智能体测试系统现在具备了强大的AI驱动Web自动化能力！")
    print("\n📚 更多信息请参考：")
    print("   • MIDSCENE_INTEGRATION_GUIDE.md - 详细集成指南")
    print("   • test_midscene_integration.py - 完整集成测试")
    print("   • midscene-example-main/ - 官方示例代码")
    
    print("\n🛠️ 快速开始：")
    print("   1. 设置环境变量：export OPENAI_API_KEY='your_key'")
    print("   2. 安装依赖：npm install -g @midscene/cli")
    print("   3. 运行测试：python test_midscene_integration.py")

def demo_code_examples():
    """演示代码示例"""
    print_banner("Midscene代码示例")
    
    print_section("1. AI模式测试用例")
    
    ai_example = '''
# 通过智能体执行Midscene AI测试
executor_agent = EnhancedExecutorAgent()

test_request = {
    "test_case": {
        "id": "ecommerce_test",
        "url": "https://www.amazon.com",
        "steps": [
            {
                "action": "input",
                "data": {"text": "iPhone 15", "selector": "搜索框"}
            },
            {
                "action": "click", 
                "data": {"text": "搜索按钮"}
            },
            {
                "action": "wait",
                "data": {"condition": "显示搜索结果"}
            },
            {
                "action": "extract",
                "data": {
                    "query": "{title: string, price: number, rating: number}[], 提取前5个商品信息",
                    "name": "products"
                }
            },
            {
                "action": "assert",
                "data": {"assertion": "页面显示了iPhone相关的搜索结果"}
            }
        ]
    }
}

result = executor_agent.execute_midscene_ai_test(test_request)
'''
    
    print("💻 AI模式示例代码：")
    print(ai_example)
    
    print_section("2. YAML模式测试脚本")
    
    yaml_example = '''
yaml_content = """
web:
  url: https://github.com
  viewportWidth: 1280
  viewportHeight: 768

tasks:
  - name: explore_repository
    flow:
      - aiAction: click on the search icon
      - aiAction: type 'midscene' in search box, hit Enter
      - sleep: 3000
      - aiWaitFor: search results are displayed
      - aiQuery: "{name: string, description: string, stars: number}[], find repositories"
        name: repositories
      - aiAssert: There are repositories related to midscene
      - aiNumber: How many repositories are shown?
      - aiBoolean: Are there any repositories with more than 100 stars?
"""

yaml_request = {
    "yaml_content": yaml_content,
    "yaml_config": {"case_id": "github_search"}
}

result = executor_agent.execute_midscene_yaml_script(yaml_request)
'''
    
    print("📄 YAML模式示例代码：")
    print(yaml_example)
    
    print_section("3. 混合智能模式")
    
    hybrid_example = '''
# 系统自动选择最佳执行模式
hybrid_request = {
    "test_case": {
        "id": "smart_web_test",
        "url": "https://news.ycombinator.com",
        "steps": [
            {
                "action": "extract",
                "data": {
                    "query": "{title: string, points: number, comments: number}[], 提取热门新闻",
                    "name": "hot_news"
                }
            },
            {
                "action": "click",
                "data": {"text": "第一条新闻标题"}
            },
            {
                "action": "wait", 
                "data": {"condition": "新闻详情页面加载完成"}
            },
            {
                "action": "assert",
                "data": {"assertion": "页面显示了新闻的详细内容"}
            }
        ]
    },
    "options": {
        "intelligent_mode": True,
        "performance_priority": "speed"
    }
}

result = executor_agent.execute_hybrid_midscene_test(hybrid_request)
print(f"智能选择的执行模式: {result['optimal_mode']}")
'''
    
    print("🔀 混合模式示例代码：")
    print(hybrid_example)

def main():
    """主函数"""
    try:
        # 运行演示
        asyncio.run(demo_midscene_capabilities())
        demo_code_examples()
        
        print(f"\n⏰ 演示完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print("\n⏹️ 演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示执行异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
