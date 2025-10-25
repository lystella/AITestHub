#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LangGraph模型管理器 - 支持DashScope完整模型集
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings

class LangGraphModelManager:
    """LangGraph模型管理器 - 完全兼容现有配置"""
    
    def __init__(self, config_file: str = "enhanced_config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.models = {}
        
        # 设置API密钥
        self.api_key = self._get_dashscope_api_key()
        if self.api_key:
            os.environ["DASHSCOPE_API_KEY"] = self.api_key
        
        print("🤖 LangGraph模型管理器初始化")
        print(f"   📁 配置文件: {config_file}")
        print(f"   🔑 API密钥: {'已配置' if self.api_key else '未配置'}")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ 配置文件加载失败: {e}")
            return {}
    
    def _get_dashscope_api_key(self) -> Optional[str]:
        """获取DashScope API密钥"""
        # 优先从环境变量获取
        api_key = os.environ.get("DASHSCOPE_API_KEY")
        if api_key:
            return api_key
        
        # 从配置文件获取
        dashscope_config = self.config.get("models", {}).get("dashscope", {})
        for model_config in dashscope_config.values():
            if isinstance(model_config, dict) and "api_key" in model_config:
                return model_config["api_key"]
        
        return None
    
    def get_chat_model(self, model_name: str = "qwen-plus") -> ChatTongyi:
        """获取聊天模型 - 支持qwen-plus"""
        if model_name not in self.models:
            model_config = self.config.get("models", {}).get("dashscope", {}).get(model_name, {})
            
            # 从配置获取参数
            timeout = model_config.get("timeout", 60)
            max_retries = model_config.get("max_retries", 3)
            
            self.models[model_name] = ChatTongyi(
                model_name=model_name,
                temperature=model_config.get("temperature", 0.7),
                max_tokens=model_config.get("max_tokens", 2000),
                streaming=model_config.get("stream", False),
                timeout=timeout,
                max_retries=max_retries
            )
            print(f"   ⚙️ 配置: timeout={timeout}s, retries={max_retries}")
            print(f"✅ 聊天模型创建: {model_name}")
        
        return self.models[model_name]
    
    def get_multimodal_model(self, model_name: str = "qwen-vl-max") -> ChatTongyi:
        """获取多模态模型 - 支持qwen-vl-max"""
        if f"{model_name}_multimodal" not in self.models:
            model_config = self.config.get("models", {}).get("dashscope", {}).get(model_name, {})
            
            # 从配置获取参数
            timeout = model_config.get("timeout", 60)
            max_retries = model_config.get("max_retries", 3)
            
            self.models[f"{model_name}_multimodal"] = ChatTongyi(
                model_name=model_name,
                temperature=model_config.get("temperature", 0.7),
                max_tokens=model_config.get("max_tokens", 1000),
                streaming=model_config.get("stream", False),
                timeout=timeout,
                max_retries=max_retries
            )
            print(f"   ⚙️ 配置: timeout={timeout}s, retries={max_retries}")
            print(f"✅ 多模态模型创建: {model_name}")
        
        return self.models[f"{model_name}_multimodal"]
    
    def get_embedding_model(self, model_name: str = "text-embedding-v4") -> DashScopeEmbeddings:
        """获取嵌入模型 - 支持text-embedding-v4"""
        if f"{model_name}_embedding" not in self.models:
            self.models[f"{model_name}_embedding"] = DashScopeEmbeddings(
                model=model_name
            )
            print(f"✅ 嵌入模型创建: {model_name}")
        
        return self.models[f"{model_name}_embedding"]
    
    def get_model_for_agent(self, agent_type: str) -> ChatTongyi:
        """为特定智能体类型获取合适的模型"""
        model_mapping = {
            "coordinator": "qwen-plus",
            "analyzer": "qwen-vl-max",  # 使用多模态模型进行分析
            "planner": "qwen-plus", 
            "data_agent": "qwen-plus",
            "executor": "qwen-plus",
            "reporter": "qwen-plus"
        }
        
        model_name = model_mapping.get(agent_type, "qwen-plus")
        
        if agent_type == "analyzer":
            return self.get_multimodal_model(model_name)
        else:
            return self.get_chat_model(model_name)
    
    def validate_models(self) -> Dict[str, bool]:
        """验证模型可用性"""
        print("🔍 验证LangGraph模型可用性...")
        
        results = {}
        
        try:
            chat_model = self.get_chat_model("qwen-plus")
            results["qwen-plus"] = True
            print("   ✅ qwen-plus (聊天模型) 可用")
        except Exception as e:
            results["qwen-plus"] = False
            print(f"   ❌ qwen-plus 不可用: {e}")
        
        try:
            multimodal_model = self.get_multimodal_model("qwen-vl-max")
            results["qwen-vl-max"] = True
            print("   ✅ qwen-vl-max (多模态模型) 可用")
        except Exception as e:
            results["qwen-vl-max"] = False
            print(f"   ❌ qwen-vl-max 不可用: {e}")
        
        try:
            embedding_model = self.get_embedding_model("text-embedding-v4")
            results["text-embedding-v4"] = True
            print("   ✅ text-embedding-v4 (嵌入模型) 可用")
        except Exception as e:
            results["text-embedding-v4"] = False
            print(f"   ❌ text-embedding-v4 不可用: {e}")
        
        success_count = sum(results.values())
        total_count = len(results)
        print(f"📊 模型验证结果: {success_count}/{total_count} 个模型可用")
        
        return results


# 全局模型管理器实例
_model_manager = None

def get_model_manager() -> LangGraphModelManager:
    """获取模型管理器单例"""
    global _model_manager
    if _model_manager is None:
        _model_manager = LangGraphModelManager()
    return _model_manager
