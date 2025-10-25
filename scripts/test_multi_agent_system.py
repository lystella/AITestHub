#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多Agent智能协作系统测试脚本
"""

import asyncio
import json
import requests
import websockets
from datetime import datetime
import time

class MultiAgentSystemTester:
    """多Agent系统测试器"""
    
    def __init__(self, base_url="http://localhost:8080", ws_url="ws://localhost:8080"):
        self.base_url = base_url
        self.ws_url = ws_url
        self.test_results = []
    
    def log_test(self, test_name, success, message="", details=None):
        """记录测试结果"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if details:
            print(f"   详情: {details}")
    
    def test_backend_health(self):
        """测试后端健康检查"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "后端健康检查", 
                    True, 
                    f"状态: {data.get('status')}", 
                    data
                )
                return True
            else:
                self.log_test(
                    "后端健康检查", 
                    False, 
                    f"HTTP状态码: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_test("后端健康检查", False, f"连接失败: {str(e)}")
            return False
    
    def test_system_status(self):
        """测试系统状态"""
        try:
            response = requests.get(f"{self.base_url}/status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                ready = data.get('ready', False)
                self.log_test(
                    "系统状态检查", 
                    ready, 
                    f"系统就绪: {ready}", 
                    data
                )
                return ready
            else:
                self.log_test(
                    "系统状态检查", 
                    False, 
                    f"HTTP状态码: {response.status_code}"
                )
                return False
        except Exception as e:
            self.log_test("系统状态检查", False, f"请求失败: {str(e)}")
            return False
    
    def test_stream_test_api(self):
        """测试流式测试API"""
        try:
            payload = {
                "test_type": "multi_agent_collaboration",
                "tasks": [
                    {"task": "测试需求分析"},
                    {"task": "测试用例生成"},
                    {"task": "自动化执行"}
                ],
                "params": {
                    "document_name": "test_document.txt",
                    "enable_streaming": True
                }
            }
            
            response = requests.post(
                f"{self.base_url}/stream-test", 
                json=payload, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                workflow_id = data.get('workflow_id')
                
                self.log_test(
                    "流式测试API", 
                    success, 
                    f"工作流ID: {workflow_id}", 
                    data
                )
                return workflow_id if success else None
            else:
                self.log_test(
                    "流式测试API", 
                    False, 
                    f"HTTP状态码: {response.status_code}"
                )
                return None
                
        except Exception as e:
            self.log_test("流式测试API", False, f"请求失败: {str(e)}")
            return None
    
    async def test_websocket_connection(self, workflow_id):
        """测试WebSocket连接"""
        try:
            ws_url = f"{self.ws_url}/ws/{workflow_id}"
            
            async with websockets.connect(ws_url) as websocket:
                self.log_test("WebSocket连接", True, f"连接成功: {ws_url}")
                
                # 发送心跳
                await websocket.send("ping")
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                
                if response == "pong":
                    self.log_test("WebSocket心跳", True, "心跳响应正常")
                else:
                    self.log_test("WebSocket心跳", False, f"意外响应: {response}")
                
                # 监听消息 (最多10秒)
                messages_received = 0
                start_time = time.time()
                
                while time.time() - start_time < 10:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=2)
                        data = json.loads(message)
                        messages_received += 1
                        
                        print(f"   📨 收到消息 #{messages_received}: {data.get('type', 'unknown')}")
                        
                        if data.get('type') == 'workflow_complete':
                            break
                            
                    except asyncio.TimeoutError:
                        continue
                    except json.JSONDecodeError:
                        continue
                
                self.log_test(
                    "WebSocket消息接收", 
                    messages_received > 0, 
                    f"收到 {messages_received} 条消息"
                )
                
                return messages_received > 0
                
        except Exception as e:
            self.log_test("WebSocket连接", False, f"连接失败: {str(e)}")
            return False
    
    def test_workflow_status_api(self, workflow_id):
        """测试工作流状态API"""
        try:
            response = requests.get(
                f"{self.base_url}/workflow-status/{workflow_id}", 
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "工作流状态API", 
                    True, 
                    f"状态查询成功", 
                    data
                )
                return True
            else:
                self.log_test(
                    "工作流状态API", 
                    False, 
                    f"HTTP状态码: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test("工作流状态API", False, f"请求失败: {str(e)}")
            return False
    
    def test_active_workflows_api(self):
        """测试活跃工作流API"""
        try:
            response = requests.get(f"{self.base_url}/active-workflows", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                self.log_test(
                    "活跃工作流API", 
                    True, 
                    f"活跃工作流数量: {count}", 
                    data
                )
                return True
            else:
                self.log_test(
                    "活跃工作流API", 
                    False, 
                    f"HTTP状态码: {response.status_code}"
                )
                return False
                
        except Exception as e:
            self.log_test("活跃工作流API", False, f"请求失败: {str(e)}")
            return False
    
    async def run_full_test(self):
        """运行完整测试"""
        print("🧪 开始多Agent智能协作系统测试")
        print("=" * 50)
        
        # 1. 后端健康检查
        if not self.test_backend_health():
            print("❌ 后端服务不可用，终止测试")
            return
        
        # 2. 系统状态检查
        if not self.test_system_status():
            print("⚠️ 系统未就绪，但继续测试API")
        
        # 3. 测试流式测试API
        workflow_id = self.test_stream_test_api()
        if not workflow_id:
            print("❌ 无法启动工作流，跳过WebSocket测试")
        else:
            # 4. 测试WebSocket连接
            await self.test_websocket_connection(workflow_id)
            
            # 5. 测试工作流状态API
            self.test_workflow_status_api(workflow_id)
        
        # 6. 测试活跃工作流API
        self.test_active_workflows_api()
        
        # 生成测试报告
        self.generate_test_report()
    
    def generate_test_report(self):
        """生成测试报告"""
        print("\n" + "=" * 50)
        print("📊 测试报告")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"通过率: {passed_tests/total_tests*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ 失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['message']}")
        
        print("\n📝 详细结果:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"   {status} {result['test']}")
        
        print("\n" + "=" * 50)
        
        if failed_tests == 0:
            print("🎉 所有测试通过！系统运行正常")
        else:
            print("⚠️ 部分测试失败，请检查系统配置")
        
        print("=" * 50)

async def main():
    """主函数"""
    print("🤖 多Agent智能协作系统测试工具")
    print("⏳ 正在连接系统...")
    
    tester = MultiAgentSystemTester()
    await tester.run_full_test()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试执行失败: {e}")
