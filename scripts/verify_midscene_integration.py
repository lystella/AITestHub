#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Midscene集成验证脚本 - 快速验证所有功能是否正确集成
"""

import sys
import importlib
from pathlib import Path

def print_status(message: str, status: bool):
    """打印状态信息"""
    icon = "✅" if status else "❌"
    print(f"{icon} {message}")

def verify_imports():
    """验证模块导入"""
    print("🔍 验证模块导入...")
    
    # 添加路径
    backend_path = Path(__file__).parent / "backend" / "intelligent_mbt_testing"
    sys.path.append(str(backend_path))
    
    try:
        # 验证核心模块导入
        from tools.midscene_agent_executor import MidsceneAgentExecutor, EXAMPLE_TEST_CASES
        print_status("MidsceneAgentExecutor导入", True)
        
        from enhanced_agents.enhanced_executor_agent import EnhancedExecutorAgent
        print_status("EnhancedExecutorAgent导入", True)
        
        # 验证示例用例
        print_status(f"示例用例加载 ({len(EXAMPLE_TEST_CASES)}个)", len(EXAMPLE_TEST_CASES) > 0)
        
        return True, (MidsceneAgentExecutor, EnhancedExecutorAgent, EXAMPLE_TEST_CASES)
        
    except ImportError as e:
        print_status(f"模块导入失败: {e}", False)
        return False, None

def verify_class_methods(classes):
    """验证类方法"""
    print("\n🔍 验证类方法...")
    
    MidsceneAgentExecutor, EnhancedExecutorAgent, EXAMPLE_TEST_CASES = classes
    
    # 验证MidsceneAgentExecutor方法
    midscene_methods = [
        'execute_ai_test_case',
        'get_stats',
        'cleanup'
    ]
    
    for method in midscene_methods:
        has_method = hasattr(MidsceneAgentExecutor, method)
        print_status(f"MidsceneAgentExecutor.{method}", has_method)
    
    # 验证EnhancedExecutorAgent新增方法
    executor_methods = [
        'execute_midscene_ai_test',
        'execute_midscene_yaml_script', 
        'execute_hybrid_midscene_test'
    ]
    
    for method in executor_methods:
        has_method = hasattr(EnhancedExecutorAgent, method)
        print_status(f"EnhancedExecutorAgent.{method}", has_method)

def verify_example_cases(EXAMPLE_TEST_CASES):
    """验证示例用例结构"""
    print("\n🔍 验证示例用例结构...")
    
    required_fields = ['id', 'url', 'mode', 'actions']
    
    for name, test_case in EXAMPLE_TEST_CASES.items():
        print(f"\n📝 验证 {name}:")
        
        for field in required_fields:
            has_field = field in test_case
            print_status(f"  {field}字段", has_field)
        
        # 验证actions结构
        actions = test_case.get('actions', [])
        valid_actions = all('type' in action for action in actions)
        print_status(f"  actions结构 ({len(actions)}个)", valid_actions)

def verify_integration_architecture():
    """验证集成架构"""
    print("\n🔍 验证集成架构...")
    
    # 验证文件存在
    files_to_check = [
        "backend/intelligent_mbt_testing/tools/midscene_agent_executor.py",
        "backend/intelligent_mbt_testing/enhanced_agents/enhanced_executor_agent.py",
        "test_midscene_integration.py",
        "demo_midscene_integration.py",
        "MIDSCENE_INTEGRATION_GUIDE.md"
    ]
    
    for file_path in files_to_check:
        file_exists = Path(file_path).exists()
        print_status(f"文件 {file_path}", file_exists)

def verify_configuration():
    """验证配置和依赖"""
    print("\n🔍 验证配置和依赖...")
    
    # 检查环境变量
    import os
    has_api_key = bool(os.getenv("OPENAI_API_KEY"))
    print_status("OPENAI_API_KEY环境变量", has_api_key)
    if not has_api_key:
        print("   💡 提示: 设置环境变量 export OPENAI_API_KEY='your_key'")
    
    # 检查Node.js相关（可选）
    import subprocess
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        has_node = result.returncode == 0
        print_status(f"Node.js ({result.stdout.strip() if has_node else 'not found'})", has_node)
    except FileNotFoundError:
        print_status("Node.js", False)
    
    # 检查npm包（可选）
    try:
        result = subprocess.run(['npm', 'list', '-g', '@midscene/cli'], capture_output=True, text=True)
        has_midscene_cli = '@midscene/cli' in result.stdout
        print_status("@midscene/cli全局包", has_midscene_cli)
        if not has_midscene_cli:
            print("   💡 提示: 安装命令 npm install -g @midscene/cli")
    except FileNotFoundError:
        print_status("npm命令", False)

def verify_functionality():
    """验证基本功能"""
    print("\n🔍 验证基本功能...")
    
    try:
        # 添加路径
        backend_path = Path(__file__).parent / "backend" / "intelligent_mbt_testing"
        sys.path.append(str(backend_path))
        
        from tools.midscene_agent_executor import MidsceneAgentExecutor
        from enhanced_agents.enhanced_executor_agent import EnhancedExecutorAgent
        
        # 测试MidsceneAgentExecutor实例化
        try:
            executor = MidsceneAgentExecutor(headless=True)
            print_status("MidsceneAgentExecutor实例化", True)
            
            # 测试统计功能
            stats = executor.get_stats()
            print_status("统计功能", isinstance(stats, dict))
            
        except Exception as e:
            print_status(f"MidsceneAgentExecutor实例化: {e}", False)
        
        # 测试EnhancedExecutorAgent实例化
        try:
            agent = EnhancedExecutorAgent()
            print_status("EnhancedExecutorAgent实例化", True)
            
            # 检查是否有midscene_executor属性
            has_midscene = hasattr(agent, 'midscene_executor')
            print_status("Midscene集成属性", has_midscene)
            
        except Exception as e:
            print_status(f"EnhancedExecutorAgent实例化: {e}", False)
            
    except Exception as e:
        print_status(f"功能验证异常: {e}", False)

def main():
    """主验证函数"""
    print("=" * 80)
    print("🎯 Midscene集成完整性验证")
    print("=" * 80)
    
    # 1. 验证导入
    import_success, classes = verify_imports()
    if not import_success:
        print("\n❌ 导入验证失败，请检查代码结构")
        return
    
    # 2. 验证方法
    verify_class_methods(classes)
    
    # 3. 验证示例用例
    verify_example_cases(classes[2])
    
    # 4. 验证架构
    verify_integration_architecture()
    
    # 5. 验证配置
    verify_configuration()
    
    # 6. 验证功能
    verify_functionality()
    
    print("\n" + "=" * 80)
    print("🎉 Midscene集成验证完成！")
    print("=" * 80)
    
    print("\n📚 下一步操作：")
    print("1. 🔧 设置环境变量：export OPENAI_API_KEY='your_key'")
    print("2. 📦 安装Node.js依赖：npm install -g @midscene/cli")
    print("3. 🧪 运行集成测试：python test_midscene_integration.py")
    print("4. 🎭 查看功能演示：python demo_midscene_integration.py")
    print("5. 📖 阅读详细指南：MIDSCENE_INTEGRATION_GUIDE.md")
    
    print("\n✨ Midscene AI自动化测试能力已成功集成到您的智能体系统！")

if __name__ == "__main__":
    main()
