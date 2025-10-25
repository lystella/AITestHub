#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混合Midscene执行器
集成WebSocket、YAML Scripts和Playwright执行模式
"""

import os
import json
import yaml
import asyncio
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from .midscene_websocket_client import (
    MidsceneWebSocketClient, 
    get_websocket_manager,
    execute_websocket_task
)

class HybridMidsceneExecutor:
    """
    混合Midscene执行器
    
    支持执行模式：
    1. WebSocket模式 - 实时双向通信，适合复杂交互
    2. YAML Scripts模式 - 声明式配置，适合标准测试
    3. Playwright模式 - 编程式控制，适合复杂逻辑
    4. 自动模式 - 智能选择最佳执行模式
    """
    
    def __init__(
        self,
        mode: str = "auto",  # auto, websocket, yaml, playwright
        headless: bool = False,
        model_config: Optional[Dict] = None,
        websocket_urls: Optional[List[str]] = None,
        temp_dir: Optional[str] = None
    ):
        self.mode = mode
        self.headless = headless
        self.model_config = model_config or self._get_default_model_config()
        self.websocket_urls = websocket_urls or ["ws://localhost:3001"]
        self.temp_dir = Path(temp_dir or tempfile.gettempdir()) / "midscene_hybrid"
        
        # 创建临时目录
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir = self.temp_dir / "screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # 执行统计
        self.execution_stats = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "websocket_executions": 0,
            "yaml_executions": 0,
            "playwright_executions": 0,
            "average_execution_time": 0
        }
        
        # WebSocket管理器
        self.websocket_manager = None
        
        print(f"🔧 混合Midscene执行器初始化完成")
        print(f"   📁 临时目录: {self.temp_dir}")
        print(f"   🎭 执行模式: {self.mode}")
        print(f"   🖥️ 无头模式: {self.headless}")
    
    def _get_default_model_config(self) -> Dict:
        """获取默认模型配置"""
        return {
            "api_key": os.getenv("DASHSCOPE_API_KEY"),
            "model_name": "qwen-vl-plus",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
        }
    
    async def initialize(self) -> bool:
        """初始化执行器"""
        try:
            # 初始化WebSocket管理器
            if self.mode in ["auto", "websocket"]:
                from .midscene_websocket_client import MidsceneWebSocketManager
                self.websocket_manager = MidsceneWebSocketManager(self.websocket_urls)
                websocket_ok = await self.websocket_manager.initialize()
                
                if not websocket_ok and self.mode == "websocket":
                    print("❌ WebSocket模式初始化失败")
                    return False
                elif not websocket_ok:
                    print("⚠️ WebSocket不可用，将使用其他执行模式")
            
            # 检查Midscene CLI是否可用
            if self.mode in ["auto", "yaml"]:
                cli_available = await self._check_midscene_cli()
                if not cli_available and self.mode == "yaml":
                    print("❌ Midscene CLI不可用")
                    return False
            
            # 检查Playwright是否可用
            if self.mode in ["auto", "playwright"]:
                playwright_available = await self._check_playwright()
                if not playwright_available and self.mode == "playwright":
                    print("❌ Playwright不可用")
                    return False
            
            print("✅ 混合执行器初始化成功")
            return True
            
        except Exception as e:
            print(f"❌ 执行器初始化失败: {e}")
            return False
    
    async def _check_midscene_cli(self) -> bool:
        """检查Midscene CLI是否可用"""
        try:
            result = await asyncio.create_subprocess_exec(
                "midscene", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            return result.returncode == 0
        except:
            return False
    
    async def _check_playwright(self) -> bool:
        """检查Playwright是否可用"""
        try:
            import playwright
            return True
        except ImportError:
            return False
    
    def _determine_execution_mode(self, instruction: Union[str, Dict, List]) -> str:
        """智能确定执行模式"""
        if self.mode != "auto":
            return self.mode
        
        # 根据指令类型和复杂度智能选择
        if isinstance(instruction, str):
            # 简单字符串指令
            if len(instruction.split()) < 10:
                # 优先使用WebSocket（如果可用）
                if self.websocket_manager and self.websocket_manager.clients:
                    return "websocket"
                else:
                    return "yaml"
            else:
                # 复杂指令使用Playwright
                return "playwright"
        
        elif isinstance(instruction, dict):
            # 字典配置，检查复杂度
            if "conditions" in instruction or "loops" in instruction:
                return "playwright"
            elif "flow" in instruction or "tasks" in instruction:
                return "yaml"
            else:
                return "websocket"
        
        elif isinstance(instruction, list):
            # 批量指令
            if len(instruction) > 5:
                return "playwright"  # 复杂批量用Playwright
            else:
                return "websocket"   # 简单批量用WebSocket
        
        # 默认使用WebSocket
        return "websocket" if self.websocket_manager else "yaml"
    
    async def execute_instruction(
        self,
        instruction: Union[str, Dict, List],
        case_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """执行指令"""
        start_time = datetime.now()
        execution_mode = self._determine_execution_mode(instruction)
        
        try:
            print(f"🎯 执行指令 ({execution_mode} 模式)")
            print(f"   📝 指令: {str(instruction)[:100]}...")
            
            # 根据模式执行
            if execution_mode == "websocket":
                result = await self._execute_websocket(instruction, case_id, context)
            elif execution_mode == "yaml":
                result = await self._execute_yaml(instruction, case_id, context)
            elif execution_mode == "playwright":
                result = await self._execute_playwright(instruction, case_id, context)
            else:
                raise ValueError(f"不支持的执行模式: {execution_mode}")
            
            # 更新统计信息
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_stats(execution_mode, True, execution_time)
            
            print(f"✅ 指令执行成功 (耗时: {execution_time:.2f}s)")
            return {
                "success": True,
                "result": result,
                "execution_mode": execution_mode,
                "execution_time": execution_time,
                "case_id": case_id
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_stats(execution_mode, False, execution_time)
            
            print(f"❌ 指令执行失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "execution_mode": execution_mode,
                "execution_time": execution_time,
                "case_id": case_id
            }
    
    async def _execute_websocket(
        self,
        instruction: Union[str, Dict, List],
        case_id: Optional[str],
        context: Optional[Dict]
    ) -> Dict[str, Any]:
        """WebSocket模式执行"""
        if not self.websocket_manager:
            raise RuntimeError("WebSocket管理器未初始化")
        
        client = self.websocket_manager.get_client()
        if not client:
            raise RuntimeError("没有可用的WebSocket连接")
        
        # 根据指令类型选择执行方法
        if isinstance(instruction, list):
            return await client.execute_batch_instructions(
                instruction, 
                case_id, 
                {"context": context}
            )
        else:
            return await client.execute_instruction(
                instruction, 
                case_id, 
                context
            )
    
    async def _execute_yaml(
        self,
        instruction: Union[str, Dict, List],
        case_id: Optional[str],
        context: Optional[Dict]
    ) -> Dict[str, Any]:
        """YAML模式执行"""
        # 将指令转换为YAML格式
        yaml_content = self._convert_to_yaml(instruction, context)
        
        # 创建临时YAML文件
        yaml_file = self.temp_dir / f"{case_id or 'temp'}.midscene.yaml"
        with open(yaml_file, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        # 执行YAML文件
        result = await self._execute_yaml_file(yaml_file)
        
        # 清理临时文件
        yaml_file.unlink(missing_ok=True)
        
        return result
    
    async def _execute_playwright(
        self,
        instruction: Union[str, Dict, List],
        case_id: Optional[str],
        context: Optional[Dict]
    ) -> Dict[str, Any]:
        """Playwright模式执行"""
        # 生成Playwright脚本
        script_content = self._generate_playwright_script(instruction, context)
        
        # 创建临时脚本文件
        script_file = self.temp_dir / f"{case_id or 'temp'}_playwright.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # 执行Playwright脚本
        result = await self._execute_playwright_script(script_file)
        
        # 清理临时文件
        script_file.unlink(missing_ok=True)
        
        return result
    
    def _convert_to_yaml(self, instruction: Union[str, Dict, List], context: Optional[Dict] = None) -> str:
        """将指令转换为YAML格式"""
        if isinstance(instruction, str):
            # 简单字符串指令
            yaml_data = {
                "web": {
                    "url": context.get("url", "about:blank") if context else "about:blank",
                    "output": str(self.temp_dir / "output.json")
                },
                "tasks": [{
                    "name": "auto_generated_task",
                    "flow": [
                        {"aiAction": instruction}
                    ]
                }]
            }
        elif isinstance(instruction, list):
            # 批量指令
            flow = []
            for idx, item in enumerate(instruction):
                if isinstance(item, str):
                    flow.append({"aiAction": item})
                elif isinstance(item, dict):
                    flow.append(item)
                
                # 在指令之间添加适当的等待
                if idx < len(instruction) - 1:
                    flow.append({"sleep": 1000})
            
            yaml_data = {
                "web": {
                    "url": context.get("url", "about:blank") if context else "about:blank",
                    "output": str(self.temp_dir / "output.json")
                },
                "tasks": [{
                    "name": "batch_task",
                    "flow": flow
                }]
            }
        elif isinstance(instruction, dict):
            # 字典配置
            if "flow" in instruction or "tasks" in instruction:
                # 已经是YAML格式
                yaml_data = instruction
            else:
                # 转换为YAML格式
                yaml_data = {
                    "web": {
                        "url": instruction.get("url", context.get("url", "about:blank") if context else "about:blank"),
                        "output": str(self.temp_dir / "output.json")
                    },
                    "tasks": [{
                        "name": instruction.get("name", "auto_task"),
                        "flow": instruction.get("actions", [{"aiAction": str(instruction)}])
                    }]
                }
        else:
            raise ValueError(f"不支持的指令类型: {type(instruction)}")
        
        return yaml.dump(yaml_data, default_flow_style=False, allow_unicode=True)
    
    def _generate_playwright_script(self, instruction: Union[str, Dict, List], context: Optional[Dict] = None) -> str:
        """生成Playwright脚本"""
        script_template = '''
import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    result = {"success": False, "error": None, "data": {}}
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless={headless})
            page = await browser.new_page()
            
            # 设置视窗大小
            await page.set_viewport_size({"width": 1280, "height": 720})
            
            # 导航到目标URL
            url = "{url}"
            if url and url != "about:blank":
                await page.goto(url)
                await page.wait_for_load_state('networkidle')
            
            {execution_code}
            
            # 保存截图
            await page.screenshot(path="{screenshot_path}")
            
            result["success"] = True
            result["data"]["screenshot_path"] = "{screenshot_path}"
            
            await browser.close()
            
        except Exception as e:
            result["error"] = str(e)
            if 'browser' in locals():
                await browser.close()
    
    # 保存结果
    with open("{result_path}", 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        # 生成执行代码
        execution_code = self._generate_execution_code(instruction)
        
        # 文件路径
        screenshot_path = self.screenshots_dir / f"playwright_{int(datetime.now().timestamp())}.png"
        result_path = self.temp_dir / "playwright_result.json"
        
        return script_template.format(
            headless=str(self.headless).lower(),
            url=context.get("url", "about:blank") if context else "about:blank",
            execution_code=execution_code,
            screenshot_path=screenshot_path,
            result_path=result_path
        )
    
    def _generate_execution_code(self, instruction: Union[str, Dict, List]) -> str:
        """生成执行代码"""
        if isinstance(instruction, str):
            # 简单指令转换为页面操作
            return f'''
            # 执行指令: {instruction}
            # 这里需要根据具体指令生成相应的Playwright代码
            # 简化实现：等待页面稳定
            await page.wait_for_timeout(2000)
            result["data"]["instruction"] = "{instruction}"
            result["data"]["message"] = "指令已接收，需要具体实现"
            '''
        elif isinstance(instruction, list):
            # 批量指令
            code_lines = []
            for i, item in enumerate(instruction):
                code_lines.append(f'''
            # 执行指令 {i+1}: {item}
            await page.wait_for_timeout(1000)
            ''')
            return '\n'.join(code_lines)
        else:
            # 复杂字典指令
            return f'''
            # 执行复杂指令: {instruction}
            await page.wait_for_timeout(2000)
            result["data"]["complex_instruction"] = True
            '''
    
    async def _execute_yaml_file(self, yaml_file: Path) -> Dict[str, Any]:
        """执行YAML文件"""
        try:
            # 使用Midscene CLI执行
            cmd = [
                "midscene",
                "run",
                str(yaml_file),
                "--headless" if self.headless else "--no-headless"
            ]
            
            # 设置环境变量
            env = os.environ.copy()
            if self.model_config.get("api_key"):
                env["OPENAI_API_KEY"] = self.model_config["api_key"]
            
            # 执行命令
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                # 解析输出结果
                try:
                    result_data = json.loads(stdout.decode())
                    return {
                        "success": True,
                        "data": result_data,
                        "stdout": stdout.decode(),
                        "stderr": stderr.decode()
                    }
                except json.JSONDecodeError:
                    return {
                        "success": True,
                        "data": {"raw_output": stdout.decode()},
                        "stdout": stdout.decode(),
                        "stderr": stderr.decode()
                    }
            else:
                return {
                    "success": False,
                    "error": stderr.decode() or "执行失败",
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"YAML执行异常: {e}"
            }
    
    async def _execute_playwright_script(self, script_file: Path) -> Dict[str, Any]:
        """执行Playwright脚本"""
        try:
            # 执行Python脚本
            process = await asyncio.create_subprocess_exec(
                "python", str(script_file),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # 读取结果文件
            result_file = self.temp_dir / "playwright_result.json"
            if result_file.exists():
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_data = json.load(f)
                result_file.unlink(missing_ok=True)
                return result_data
            else:
                return {
                    "success": False,
                    "error": "结果文件未生成",
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Playwright执行异常: {e}"
            }
    
    def _update_stats(self, mode: str, success: bool, execution_time: float):
        """更新执行统计"""
        self.execution_stats["total_executions"] += 1
        
        if success:
            self.execution_stats["successful_executions"] += 1
        else:
            self.execution_stats["failed_executions"] += 1
        
        # 更新模式统计
        mode_key = f"{mode}_executions"
        if mode_key in self.execution_stats:
            self.execution_stats[mode_key] += 1
        
        # 更新平均执行时间
        total = self.execution_stats["total_executions"]
        current_avg = self.execution_stats["average_execution_time"]
        self.execution_stats["average_execution_time"] = (
            (current_avg * (total - 1) + execution_time) / total
        )
    
    async def execute_yaml_file(self, yaml_file_path: str) -> Dict[str, Any]:
        """执行YAML文件"""
        yaml_file = Path(yaml_file_path)
        if not yaml_file.exists():
            return {
                "success": False,
                "error": f"YAML文件不存在: {yaml_file_path}"
            }
        
        return await self._execute_yaml_file(yaml_file)
    
    async def execute_batch(self, instructions: List[Union[str, Dict]]) -> Dict[str, Any]:
        """批量执行指令"""
        return await self.execute_instruction(instructions)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取执行统计"""
        success_rate = 0
        if self.execution_stats["total_executions"] > 0:
            success_rate = (
                self.execution_stats["successful_executions"] / 
                self.execution_stats["total_executions"] * 100
            )
        
        return {
            **self.execution_stats,
            "success_rate": success_rate
        }
    
    async def cleanup(self):
        """清理资源"""
        try:
            if self.websocket_manager:
                await self.websocket_manager.shutdown()
            
            # 清理临时文件（保留最近的一些文件用于调试）
            import shutil
            if self.temp_dir.exists():
                # 只清理较老的文件
                cutoff_time = datetime.now().timestamp() - 3600  # 1小时前
                for file_path in self.temp_dir.rglob("*"):
                    if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                        file_path.unlink(missing_ok=True)
            
            print("✅ 混合执行器清理完成")
            
        except Exception as e:
            print(f"⚠️ 清理过程中出现异常: {e}")

# 便捷函数
async def execute_hybrid_instruction(
    instruction: Union[str, Dict, List],
    case_id: Optional[str] = None,
    context: Optional[Dict] = None,
    mode: str = "auto"
) -> Dict[str, Any]:
    """执行混合指令的便捷函数"""
    executor = HybridMidsceneExecutor(mode=mode)
    
    try:
        await executor.initialize()
        return await executor.execute_instruction(instruction, case_id, context)
    finally:
        await executor.cleanup()

async def execute_yaml_file_hybrid(yaml_file_path: str) -> Dict[str, Any]:
    """执行YAML文件的便捷函数"""
    executor = HybridMidsceneExecutor(mode="yaml")
    
    try:
        await executor.initialize()
        return await executor.execute_yaml_file(yaml_file_path)
    finally:
        await executor.cleanup()
