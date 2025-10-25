#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的API接口
"""

import asyncio
import aiohttp
import json

async def test_enhanced_workflow_api():
    """测试增强工作流API"""
    print("🧪 测试修复后的 /enhanced-test-workflow API")
    print("=" * 50)
    
    # 测试数据
    test_data = {
        "file_content": "# 测试需求文档\n\n这是一个测试需求文档，用于验证API接口。",
        "file_name": "test_api_fix.txt",
        "params": {
            "document_size": 100,
            "enable_streaming": True,
            "collaboration_mode": "enhanced"
        }
    }
    
    api_url = "http://localhost:8080/enhanced-test-workflow"
    
    try:
        async with aiohttp.ClientSession() as session:
            print(f"📡 发送POST请求到: {api_url}")
            print(f"📦 请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
            
            async with session.post(
                api_url,
                json=test_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                status = response.status
                print(f"\n📊 响应状态码: {status}")
                
                if status == 200:
                    result = await response.json()
                    print(f"✅ API调用成功!")
                    print(f"📋 响应数据:")
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ API调用失败!")
                    print(f"错误信息: {error_text}")
                    return False
                    
    except aiohttp.ClientConnectorError:
        print("❌ 无法连接到后端服务，请确保后端服务已启动")
        print("💡 提示: 运行 'python web_service.py' 启动后端服务")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_status_api():
    """测试状态API"""
    print("\n🧪 测试 /status API")
    print("=" * 50)
    
    api_url = "http://localhost:8080/status"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                status = response.status
                print(f"📊 响应状态码: {status}")
                
                if status == 200:
                    result = await response.json()
                    print(f"✅ 系统状态:")
                    print(f"   框架: {result.get('framework', 'N/A')}")
                    print(f"   版本: {result.get('version', 'N/A')}")
                    print(f"   系统就绪: {result.get('ready', False)}")
                    print(f"   智能体数量: {len(result.get('agents', {}))}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ API调用失败: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

async def main():
    """主函数"""
    print("🚀 开始API接口测试")
    print("=" * 60)
    
    # 测试1: 状态API
    status_ok = await test_status_api()
    
    # 测试2: 增强工作流API（如果状态正常）
    workflow_ok = False
    if status_ok:
        workflow_ok = await test_enhanced_workflow_api()
    
    # 结果总结
    print("\n" + "=" * 60)
    print("🎯 测试结果汇总")
    print("=" * 60)
    print(f"   状态API: {'✅ 通过' if status_ok else '❌ 失败'}")
    print(f"   工作流API: {'✅ 通过' if workflow_ok else '❌ 失败'}")
    
    if status_ok and workflow_ok:
        print("\n🎉 所有API测试通过！前后端可以正常通信。")
    else:
        print("\n⚠️ 部分测试失败，请检查后端服务。")

if __name__ == "__main__":
    asyncio.run(main())
