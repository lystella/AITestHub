#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通义千问(Qwen) AgentScope快速启动脚本"""

import os
import sys
from pathlib import Path

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    issues = []
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        issues.append("需要 Python 3.8 或更高版本")
    
    # 检查DashScope API密钥
    if not os.environ.get("DASHSCOPE_API_KEY"):
        issues.append("请设置 DASHSCOPE_API_KEY 环境变量")
    
    # 检查依赖包
    try:
        import dashscope
        print("✅ DashScope SDK 已安装")
    except ImportError:
        issues.append("请安装 DashScope SDK: pip install dashscope")
    
    # 检查AgentScope
    try:
        agentscope_path = Path(__file__).parent.parent.parent / "src"
        sys.path.insert(0, str(agentscope_path))
        import agentscope
        print("✅ AgentScope 可用")
    except ImportError:
        issues.append("AgentScope 导入失败")
    
    return issues

def print_banner():
    """打印启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🤖 通义千问 × AgentScope 集成环境 🤖                   ║
║                                                              ║
║  ✨ 专为中文场景优化的AI智能体框架                            ║
║  🔄 支持多种Qwen模型：turbo/plus/max/QwQ                     ║
║  🌐 流式推理 + 可视化界面                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_usage_guide():
    """打印使用指南"""
    usage = """
🚀 快速开始指南:

1. 📋 设置API密钥:
   export DASHSCOPE_API_KEY="your_dashscope_api_key"
   # 获取密钥: https://dashscope.console.aliyun.com/

2. 📦 安装依赖:
   pip install dashscope

3. 🎯 选择运行模式:
   a) 演示Qwen模型能力:
      python qwen_example.py

   b) 运行流式推理系统:
      cd ../streaming_reasoning
      python main.py

   c) 运行MBT测试应用:
      cd ../mbt_testing_application
      python main.py

   d) 配置管理演示:
      python config_demo.py

4. 🔧 模型选择建议:
   - qwen-turbo:  快速任务，性价比高
   - qwen-plus:   平衡性能，通用场景
   - qwen-max:    复杂推理，质量最优
   - qwq-32b:     深度思考，逻辑推理
   - qwen-vl:     视觉理解，多模态

5. 📊 监控和调优:
   - 查看日志: tail -f qwen_agentscope.log
   - 调整温度参数: 0.1(创作) ~ 0.9(分析)
   - 启用思考模式: enable_thinking=True (仅QwQ)

💡 提示:
- 中文提示词效果更佳
- 合理设置max_tokens控制成本
- 启用流式输出获得更好体验
    """
    print(usage)

def demo_qwen_models():
    """演示使用的核心Qwen模型"""
    print("\n📊 核心Qwen模型配置:")
    
    models = {
        "qwen-plus": {
            "description": "主要LLM模型，统一处理所有文本任务",
            "max_tokens": 8000,
            "cost": "¥ 0.004/1K tokens",
            "use_case": "对话、推理、代码生成、文档写作、任务规划、报告生成"
        },
        "qwen-vl-max": {
            "description": "视觉理解模型，处理图像相关任务",
            "max_tokens": 4000,
            "cost": "¥ 0.02/1K tokens",
            "use_case": "图像分析、视觉问答、OCR文字识别、场景理解"
        },
        "text-embedding-v4": {
            "description": "文本嵌入模型，向量化和语义搜索",
            "max_tokens": "N/A",
            "cost": "¥ 0.0007/1K tokens",
            "use_case": "文本嵌入、语义搜索、相似度计算、聚类分析"
        }
    }
    
    for model, info in models.items():
        print(f"\n🤖 {model}:")
        print(f"   描述: {info['description']}")
        print(f"   最大令牌: {info['max_tokens']}")
        print(f"   成本: {info['cost']}")
        print(f"   适用场景: {info['use_case']}")

def check_config_file():
    """检查配置文件是否存在"""
    config_file = Path(__file__).parent / "config.json"
    
    if config_file.exists():
        print(f"✅ 找到配置文件: {config_file}")
        return config_file
    else:
        print(f"❌ 未找到配置文件: {config_file}")
        print("请确保 config.json 文件存在于当前目录")
        return None

def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    issues = check_environment()
    
    if issues:
        print("❌ 环境检查发现问题:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print()
        
        if "DASHSCOPE_API_KEY" in str(issues):
            print("🔑 获取DashScope API密钥:")
            print("   1. 访问: https://dashscope.console.aliyun.com/")
            print("   2. 登录阿里云账号")
            print("   3. 开通DashScope服务")
            print("   4. 创建API密钥")
            print("   5. 设置环境变量: export DASHSCOPE_API_KEY='your_key'")
            print()
        
        print_usage_guide()
        return
    
    print("✅ 环境检查通过!")
    
    # 显示模型信息
    demo_qwen_models()
    
    # 检查配置文件
    config_file = check_config_file()
    if not config_file:
        return
    
    # 提供选项菜单
    print("\n🎯 请选择操作:")
    print("1. 🚀 运行简化Qwen演示 (qwen_simple_example.py)")
    print("2. 🌊 启动流式推理系统")
    print("3. 🧪 启动MBT测试应用")
    print("4. ⚙️ 配置管理演示")
    print("5. 📖 查看详细使用指南")
    print("6. 🚪 退出")
    
    while True:
        try:
            choice = input("\n请选择 (1-6): ").strip()
            
            if choice == "1":
                print("\n🚀 启动简化Qwen演示...")
                os.system(f"{sys.executable} qwen_simple_example.py")
                break
                
            elif choice == "2":
                print("\n🌊 启动流式推理系统...")
                os.chdir("../streaming_reasoning")
                os.system(f"{sys.executable} main.py")
                break
                
            elif choice == "3":
                print("\n🧪 启动MBT测试应用...")
                os.chdir("../mbt_testing_application")
                os.system(f"{sys.executable} main.py")
                break
                
            elif choice == "4":
                print("\n⚙️ 启动配置管理演示...")
                os.system(f"{sys.executable} config_demo.py")
                break
                
            elif choice == "5":
                print_usage_guide()
                continue
                
            elif choice == "6":
                print("👋 再见!")
                break
                
            else:
                print("❌ 无效选择，请输入 1-6")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序已退出")
            break
        except Exception as e:
            print(f"\n❌ 操作失败: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("请检查环境配置或查看文档获取帮助")
