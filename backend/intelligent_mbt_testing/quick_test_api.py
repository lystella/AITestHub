#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试修复后的API
"""

import requests
import json

def test_api():
    """测试API"""
    print("🧪 快速测试 /enhanced-test-workflow API")
    print("=" * 50)
    
    url = "http://localhost:8080/enhanced-test-workflow"
    
    # 模拟前端发送的数据
    data = {
        "file_content": "# 测试需求\n这是一个测试需求文档。",
        "file_name": "quick_test.txt",
        "params": {
            "document_size": 100,
            "enable_streaming": True,
            "collaboration_mode": "enhanced"
        }
    }
    
    try:
        print(f"📡 POST {url}")
        print(f"📦 数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(url, json=data, timeout=600)
        
        print(f"\n📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API调用成功!")
            print(f"   成功: {result.get('success')}")
            print(f"   工作流ID: {result.get('workflow_id')}")
            print(f"   时间戳: {result.get('timestamp')}")
        else:
            print(f"❌ API调用失败!")
            print(f"   错误: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务")
        print("💡 请确保后端服务正在运行: python web_service.py")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_api()
