#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载器 - 替代enhanced_config
只保留必要的配置加载功能
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class SystemConfig:
    """系统配置类"""
    
    def __init__(self, config_file: str = "enhanced_config.json"):
        self.config_file = Path(config_file)
        self._config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"⚠️ 配置文件不存在: {self.config_file}")
                return self._get_default_config()
        except Exception as e:
            print(f"⚠️ 配置文件加载失败: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "models": {
                "dashscope": {
                    "qwen-plus": {
                        "model_name": "qwen-plus",
                        "model_type": "chat",
                        "provider": "dashscope",
                        "api_key": os.environ.get("DASHSCOPE_API_KEY", ""),
                        "temperature": 0.7,
                        "timeout": 600,
                        "max_retries": 3
                    },
                    "qwen-vl-max": {
                        "model_name": "qwen-vl-max",
                        "model_type": "multimodal",
                        "provider": "dashscope",
                        "api_key": os.environ.get("DASHSCOPE_API_KEY", ""),
                        "temperature": 0.7,
                        "timeout": 60,
                        "max_retries": 3
                    },
                    "text-embedding-v4": {
                        "model_name": "text-embedding-v4",
                        "model_type": "embedding",
                        "provider": "dashscope",
                        "api_key": os.environ.get("DASHSCOPE_API_KEY", ""),
                        "timeout": 30,
                        "max_retries": 3
                    }
                }
            },
            "system": {
                "workspace_path": "./enhanced_workspace",
                "log_level": "INFO",
                "max_concurrent_tasks": 10
            }
        }
    
    @property
    def models(self) -> Dict[str, Any]:
        """获取模型配置"""
        return self._config.get("models", {})
    
    @property
    def system(self) -> Dict[str, Any]:
        """获取系统配置"""
        return self._config.get("system", {})
    
    def get_model_config(self, provider: str, model_name: str) -> Dict[str, Any]:
        """获取特定模型配置"""
        return self.models.get(provider, {}).get(model_name, {})
    
    def get_dashscope_api_key(self) -> Optional[str]:
        """获取DashScope API密钥"""
        # 优先从环境变量获取
        api_key = os.environ.get("DASHSCOPE_API_KEY")
        if api_key:
            return api_key
        
        # 从配置文件获取
        dashscope_models = self.models.get("dashscope", {})
        for model_config in dashscope_models.values():
            if isinstance(model_config, dict) and "api_key" in model_config:
                api_key = model_config["api_key"]
                if api_key:
                    return api_key
        
        return None

# 创建全局配置实例
SYSTEM_CONFIG = SystemConfig()

# 确保API密钥设置
api_key = SYSTEM_CONFIG.get_dashscope_api_key()
if api_key:
    os.environ["DASHSCOPE_API_KEY"] = api_key
