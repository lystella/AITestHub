#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试真实实现 - 验证所有Mock修复
"""

import asyncio
import sys
from datetime import datetime
from unified_intelligent_testing_system import UnifiedIntelligentTestingSystem

async def test_real_implementation():
    """测试真实实现的所有功能"""
    
    print("=" * 80)
    print("🧪 真实实现测试 - v3.0 Phase 2")
    print("=" * 80)
    print()
    
    # 初始化系统
    print("📦 正在初始化系统...")
    system = UnifiedIntelligentTestingSystem()
    await system.initialize_system()
    print("✅ 系统初始化完成\n")
    
    # 测试数据
    test_content = """
# 电商网站购物流程测试

## 测试目标
测试用户在电商网站的完整购物流程

## 测试场景
1. 用户登录
2. 浏览商品列表
3. 查看商品详情
4. 添加商品到购物车
5. 修改商品数量
6. 进行结算

## 质量要求
- 页面加载时间 < 2秒
- 购物车更新实时
- 数据准确无误
"""
    
    print("🔄 开始执行完整工作流...")
    print(f"   测试文件: shopping_flow_test.md")
    print(f"   开始时间: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    try:
        result = await system.execute_complete_workflow(
            file_content=test_content,
            file_name="shopping_flow_test.md"
        )
        
        print()
        print("=" * 80)
        print("✅ 工作流执行完成！")
        print("=" * 80)
        print()
        
        # 基本信息
        print("📊 基本信息:")
        print(f"   - 工作流ID: {result.get('workflow_id', 'N/A')}")
        print(f"   - 执行状态: {'✅ 成功' if result.get('success') else '❌ 失败'}")
        print()
        
        # 真实实现验证
        print("🔍 真实实现验证:")
        print()
        
        # 1. 向量搜索验证
        vector_results = result.get('state', {}).get('vector_search_results', [])
        if vector_results:
            print("✅ 1. 向量搜索 - 真实实现")
            print(f"   找到 {len(vector_results)} 个相关历史经验")
            for i, vr in enumerate(vector_results[:3], 1):
                similarity = vr.get('similarity', 0)
                content = str(vr.get('content', ''))[:30]
                print(f"   {i}. 相似度 {similarity:.2f}: {content}...")
        else:
            print("ℹ️  1. 向量搜索 - 未找到历史经验（首次运行）")
        print()
        
        # 2. 文件生成验证
        excel_data = result.get('state', {}).get('excel_data', {})
        yaml_config = result.get('state', {}).get('yaml_config', {})
        
        if excel_data.get('file_exists'):
            print("✅ 2. Excel文件生成 - 真实实现")
            print(f"   文件路径: {excel_data.get('filename')}")
            print(f"   文件大小: {excel_data.get('file_size', 0)} bytes")
            print(f"   工作表: {', '.join(excel_data.get('sheets', []))}")
        else:
            print("⚠️  2. Excel文件生成 - 降级到数据结构")
            if excel_data.get('error'):
                print(f"   原因: {excel_data.get('error')}")
        print()
        
        if yaml_config.get('_file_exists'):
            print("✅ 3. YAML文件生成 - 真实实现")
            print(f"   文件路径: {yaml_config.get('_filename')}")
            print(f"   文件大小: {yaml_config.get('_file_size', 0)} bytes")
        else:
            print("⚠️  3. YAML文件生成 - 降级到数据结构")
            if yaml_config.get('_error'):
                print(f"   原因: {yaml_config.get('_error')}")
        print()
        
        # 3. Midscene执行验证
        midscene_results = result.get('midscene_results', [])
        if midscene_results:
            print("✅ 4. Midscene测试执行 - 真实实现")
            print(f"   执行用例数: {len(midscene_results)}")
            
            real_execution = 0
            mock_execution = 0
            
            for mr in midscene_results:
                exec_mode = mr.get('execution_mode', 'unknown')
                if exec_mode == 'mock':
                    mock_execution += 1
                elif exec_mode in ['playwright', 'yaml', 'websocket']:
                    real_execution += 1
            
            if real_execution > 0:
                print(f"   ✅ 真实执行: {real_execution} 个")
            if mock_execution > 0:
                print(f"   ⚠️  模拟执行: {mock_execution} 个（Midscene不可用时降级）")
            
            print()
            print("   测试用例详情:")
            for i, mr in enumerate(midscene_results[:5], 1):
                status_icon = "✅" if mr.get('status') == 'passed' else "❌" if mr.get('status') == 'failed' else "⚠️"
                case_name = mr.get('case_name', 'N/A')
                exec_time = mr.get('execution_time', 'N/A')
                exec_mode = mr.get('execution_mode', 'unknown')
                print(f"   {i}. {status_icon} {case_name}")
                print(f"      - 执行模式: {exec_mode}")
                print(f"      - 执行时间: {exec_time}")
                if mr.get('screenshot'):
                    print(f"      - 截图: {mr.get('screenshot')}")
            
            if len(midscene_results) > 5:
                print(f"   ... 还有{len(midscene_results)-5}个测试用例")
        else:
            print("⚠️  4. Midscene测试执行 - 无执行结果")
        print()
        
        # 统计信息
        print("📈 执行统计:")
        test_cases = result.get('test_cases', [])
        execution_results = result.get('execution_results', [])
        
        print(f"   - 生成测试用例: {len(test_cases)} 个")
        print(f"   - 执行结果记录: {len(execution_results)} 条")
        
        if midscene_results:
            passed = len([r for r in midscene_results if r.get('status') == 'passed'])
            failed = len([r for r in midscene_results if r.get('status') == 'failed'])
            error = len([r for r in midscene_results if r.get('status') == 'error'])
            total = len(midscene_results)
            success_rate = (passed / total * 100) if total > 0 else 0
            
            print(f"   - 通过: {passed} 个 ✅")
            print(f"   - 失败: {failed} 个 ❌")
            if error > 0:
                print(f"   - 错误: {error} 个 ⚠️")
            print(f"   - 成功率: {success_rate:.1f}%")
        print()
        
        # 性能信息
        state = result.get('state', {})
        step_history = state.get('step_history', [])
        
        if step_history:
            print("⏱️  执行阶段:")
            for step in step_history:
                print(f"   ✓ {step}")
        print()
        
        # 最终报告
        final_report = result.get('final_report', {})
        if final_report:
            print("📄 最终报告:")
            print(f"   - 报告ID: {final_report.get('report_id', 'N/A')}")
            print(f"   - 生成时间: {final_report.get('generation_time', 'N/A')[:19]}")
            print(f"   - 质量得分: {final_report.get('quality_score', 0):.2f}")
        print()
        
        # 总结
        print("=" * 80)
        print("🎯 测试总结")
        print("=" * 80)
        
        has_real_vector = len(vector_results) > 0
        has_real_excel = excel_data.get('file_exists', False)
        has_real_yaml = yaml_config.get('_file_exists', False)
        has_real_midscene = any(mr.get('execution_mode') != 'mock' for mr in midscene_results)
        
        real_count = sum([has_real_vector, has_real_excel, has_real_yaml, has_real_midscene])
        total_count = 4
        
        print(f"✅ 真实实现: {real_count}/{total_count} 项")
        print()
        
        if has_real_vector:
            print("   ✅ 向量搜索: 真实实现")
        else:
            print("   ℹ️  向量搜索: 无历史数据")
        
        if has_real_excel:
            print("   ✅ Excel生成: 真实文件")
        else:
            print("   ⚠️  Excel生成: 降级模式")
        
        if has_real_yaml:
            print("   ✅ YAML生成: 真实文件")
        else:
            print("   ⚠️  YAML生成: 降级模式")
        
        if has_real_midscene:
            print("   ✅ Midscene执行: 真实浏览器测试")
        else:
            print("   ⚠️  Midscene执行: 降级模式（Midscene不可用）")
        
        print()
        
        if real_count >= 3:
            print("🎉 核心功能已使用真实实现！")
        elif real_count >= 2:
            print("✅ 部分功能使用真实实现，系统正常运行")
        else:
            print("⚠️  大部分功能使用降级模式，请检查环境配置")
        
        print()
        print("💡 提示:")
        print("   - 如果Midscene执行使用降级模式，请确保Playwright已安装")
        print("   - 如果文件生成使用降级模式，请检查文件系统权限")
        print("   - 首次运行时向量搜索可能无历史数据")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ 测试失败")
        print("=" * 80)
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    success = await test_real_implementation()
    
    print()
    print("=" * 80)
    if success:
        print("✅ 真实实现测试完成！")
    else:
        print("❌ 真实实现测试失败")
    print("=" * 80)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

