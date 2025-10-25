# -*- coding: utf-8 -*-
"""简化版通义千问 AgentScope 使用示例 - 只使用3个核心模型"""

import sys
import asyncio
import os
from pathlib import Path

# 添加AgentScope到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import agentscope
from agentscope.config import ConfigManager, create_model
from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit
from agentscope.message import Msg


def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查DashScope API密钥
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 请设置 DASHSCOPE_API_KEY 环境变量")
        print("   获取地址：https://dashscope.console.aliyun.com/")
        return False
    
    print("✅ DashScope API密钥已配置")
    return True


class SimpleQwenAgent(ReActAgent):
    """简化的通义千问智能体"""
    
    def __init__(self, name: str = "QwenAgent", agent_type: str = "text"):
        """
        创建简化的通义千问智能体
        
        Args:
            name: 智能体名称
            agent_type: 智能体类型 ("text" | "vision" | "embedding")
        """
        # 根据类型选择模型
        model_map = {
            "text": "qwen-plus",          # 主要LLM模型
            "vision": "qwen-vl-max",     # 视觉模型
            "embedding": "text-embedding-v4"  # 嵌入模型
        }
        
        model_name = model_map.get(agent_type, "qwen-plus")
        
        # 创建模型
        model = create_model("dashscope", model_name)
        
        # 根据类型设置提示词
        prompts = {
            "text": "你是通义千问AI助手，能够帮助用户解决各种文本相关的问题。",
            "vision": "你是通义千问视觉助手，能够分析和理解图像内容，提供准确的视觉描述。",
            "embedding": "你是通义千问嵌入助手，专门负责文本向量化和语义相似度计算。"
        }
        
        sys_prompt = prompts.get(agent_type, prompts["text"])
        
        super().__init__(
            name=name,
            sys_prompt=sys_prompt,
            model=model,
            formatter=OpenAIChatFormatter(),
            toolkit=Toolkit(),
            memory=InMemoryMemory(),
        )
        
        self.agent_type = agent_type
        print(f"✅ 创建 {agent_type} 类型智能体: {name} (模型: {model_name})")


async def demo_text_model():
    """演示文本模型 - qwen-plus"""
    
    print("\n📝 演示文本模型 (qwen-plus)")
    print("-" * 40)
    
    # 创建文本智能体
    text_agent = SimpleQwenAgent("TextAgent", "text")
    
    # 测试对话
    questions = [
        "请简要介绍一下人工智能的发展历程。",
        "帮我写一段Python代码来实现快速排序算法。",
        "分析一下在线教育相比传统教育的优势和劣势。"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n🔍 问题 {i}: {question}")
        try:
            response = await text_agent(question)
            print(f"💬 回答: {response.content[:200]}...")
        except Exception as e:
            print(f"❌ 错误: {e}")


async def demo_vision_model():
    """演示视觉模型 - qwen-vl-max"""
    
    print("\n👁️ 演示视觉模型 (qwen-vl-max)")
    print("-" * 40)
    
    try:
        # 创建视觉智能体
        vision_agent = SimpleQwenAgent("VisionAgent", "vision")
        
        # 由于这是演示，我们测试文本描述能力
        vision_tasks = [
            "描述一下如何使用计算机视觉技术进行UI自动化测试。",
            "解释一下OCR技术在文档处理中的应用。",
            "分析图像识别在安防监控中的重要性。"
        ]
        
        for i, task in enumerate(vision_tasks, 1):
            print(f"\n🔍 任务 {i}: {task}")
            try:
                response = await vision_agent(task)
                print(f"👁️ 分析: {response.content[:200]}...")
            except Exception as e:
                print(f"❌ 错误: {e}")
                
        print("\n💡 注意: 在实际应用中，qwen-vl-max 可以直接处理图像输入")
        
    except Exception as e:
        print(f"❌ 视觉模型演示失败: {e}")


async def demo_embedding_model():
    """演示嵌入模型 - text-embedding-v4"""
    
    print("\n🔢 演示嵌入模型 (text-embedding-v4)")
    print("-" * 40)
    
    try:
        # 创建嵌入智能体
        embedding_agent = SimpleQwenAgent("EmbeddingAgent", "embedding")
        
        # 测试嵌入相关任务
        embedding_tasks = [
            "解释什么是文本嵌入向量，它在NLP中的作用是什么？",
            "语义相似度计算在搜索引擎中是如何应用的？",
            "向量数据库在大规模文本检索中有哪些优势？"
        ]
        
        for i, task in enumerate(embedding_tasks, 1):
            print(f"\n🔍 任务 {i}: {task}")
            try:
                response = await embedding_agent(task)
                print(f"🔢 解答: {response.content[:200]}...")
            except Exception as e:
                print(f"❌ 错误: {e}")
                
        print("\n💡 注意: text-embedding-v4 主要用于生成文本的向量表示")
        
    except Exception as e:
        print(f"❌ 嵌入模型演示失败: {e}")


async def demo_multi_agent_conversation():
    """演示多智能体协作"""
    
    print("\n🤝 演示多智能体协作")
    print("-" * 40)
    
    try:
        # 创建不同类型的智能体
        analyst = SimpleQwenAgent("分析师", "text")
        vision_expert = SimpleQwenAgent("视觉专家", "vision") 
        
        # 模拟协作场景
        print("\n📊 场景: 分析一个电商网站的用户体验")
        
        # 分析师提供分析
        analysis_request = "请分析电商网站用户体验的关键要素有哪些？"
        print(f"\n🔍 分析师任务: {analysis_request}")
        
        analysis_result = await analyst(analysis_request)
        print(f"📊 分析师回答: {analysis_result.content[:150]}...")
        
        # 视觉专家提供视觉角度的建议
        vision_request = f"基于以下分析结果，从视觉设计角度提供改进建议: {analysis_result.content[:200]}"
        print(f"\n👁️ 视觉专家任务: {vision_request[:100]}...")
        
        vision_result = await vision_expert(vision_request)
        print(f"🎨 视觉专家建议: {vision_result.content[:150]}...")
        
        print("\n✅ 多智能体协作完成")
        
    except Exception as e:
        print(f"❌ 多智能体协作演示失败: {e}")


def demo_configuration():
    """演示配置管理"""
    
    print("\n⚙️ 演示配置管理")
    print("-" * 40)
    
    # 加载简化配置
    config_file = Path(__file__).parent / "qwen_simplified_config.json"
    
    if config_file.exists():
        config_manager = ConfigManager(config_file)
        print(f"✅ 加载简化配置文件: {config_file.name}")
        
        # 显示可用模型
        models = config_manager.list_available_models()
        print(f"\n📋 可用模型: {models}")
        
        # 显示智能体配置
        print(f"\n🤖 智能体配置:")
        agent_types = ["default", "planner", "executor", "reporter", "vision", "embedding"]
        for agent_type in agent_types:
            try:
                agent_config = config_manager.get_agent_config(agent_type)
                model_name = agent_config.model_config.model_name
                print(f"  {agent_type}: {model_name}")
            except:
                print(f"  {agent_type}: 未配置")
                
        # 显示模型用途
        print(f"\n🎯 模型用途分配:")
        print(f"  📝 qwen-plus: 所有文本处理任务 (对话、分析、生成)")
        print(f"  👁️ qwen-vl-max: 视觉理解任务 (图像分析、OCR)")
        print(f"  🔢 text-embedding-v4: 文本嵌入任务 (向量化、搜索)")
        
    else:
        print(f"⚠️ 未找到配置文件: {config_file}")


async def main():
    """主函数"""
    
    print("🎯 简化版通义千问 AgentScope 演示")
    print("=" * 50)
    print("📋 使用模型:")
    print("  • qwen-plus: 主要LLM模型")
    print("  • qwen-vl-max: 视觉理解模型") 
    print("  • text-embedding-v4: 文本嵌入模型")
    print("=" * 50)
    
    # 检查环境
    if not check_environment():
        return
    
    # 初始化AgentScope
    agentscope.init(
        project="qwen_simple_demo",
        name="simplified_example",
        logging_level="INFO"
    )
    
    # 1. 配置演示
    demo_configuration()
    
    # 2. 文本模型演示
    await demo_text_model()
    
    # 3. 视觉模型演示
    await demo_vision_model()
    
    # 4. 嵌入模型演示
    await demo_embedding_model()
    
    # 5. 多智能体协作演示
    await demo_multi_agent_conversation()
    
    print("\n✨ 演示完成！")
    print("\n💡 总结:")
    print("✅ 成功整合3个核心通义千问模型")
    print("✅ 统一使用qwen-plus处理所有文本任务")
    print("✅ qwen-vl-max专门处理视觉相关任务")
    print("✅ text-embedding-v4负责文本嵌入向量化")
    print("✅ 简化配置，降低复杂度和成本")
    
    print("\n🎯 使用建议:")
    print("• 大部分场景只需要使用 qwen-plus")
    print("• 涉及图像时才使用 qwen-vl-max")
    print("• 需要语义搜索时才使用 text-embedding-v4")
    print("• 这样的配置既经济又高效")


if __name__ == "__main__":
    asyncio.run(main())
