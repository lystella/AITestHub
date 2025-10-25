#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Midscene智能体执行器 - 基于midscene-example的完整实现
集成Playwright + YAML Scripts + AI能力
"""

import os
import json
import yaml
import asyncio
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

# 导入系统配置
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config_loader import SYSTEM_CONFIG

class MidsceneAgentExecutor:
    """
    Midscene智能体执行器
    
    基于midscene-example实现，支持：
    1. Playwright模式 - 编程式AI控制
    2. YAML Scripts模式 - 声明式配置
    3. 混合模式 - 智能选择最佳方式
    """
    
    def __init__(
        self,
        headless: bool = True,
        viewport_width: int = 1280,
        viewport_height: int = 768,
        api_key: Optional[str] = None,
        temp_dir: Optional[str] = None,
        model_name: str = "qwen-plus"
    ):
        self.headless = headless
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.model_name = model_name
        
        # 从系统配置获取API密钥和模型配置
        self.model_config = self._get_model_config(model_name)
        self.api_key = api_key or self.model_config.get("api_key") or os.getenv("OPENAI_API_KEY")
        
        self.temp_dir = Path(temp_dir or tempfile.gettempdir()) / "midscene_agent"
        
        # 执行统计
        self.execution_stats = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "playwright_executions": 0,
            "yaml_executions": 0,
            "average_execution_time": 0
        }
        
        # 创建临时目录
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🎯 Midscene智能体执行器初始化完成")
        print(f"   🖥️ 视窗: {viewport_width}x{viewport_height}")
        print(f"   👁️ 无头模式: {headless}")
        print(f"   🤖 使用模型: {model_name}")
        print(f"   🔑 API密钥: {'已配置' if self.api_key else '未配置'}")
        
        if not self.api_key:
            print("   ⚠️ 警告: 未配置API密钥，Midscene功能可能无法正常工作")
            print("   💡 请检查enhanced_config.json中的模型配置")
    
    def _get_model_config(self, model_name: str) -> Dict[str, Any]:
        """从系统配置获取模型配置"""
        try:
            # 查找DashScope模型配置
            models_config = getattr(SYSTEM_CONFIG, 'models', {})
            dashscope_models = models_config.get("dashscope", {})
            if model_name in dashscope_models:
                return dashscope_models[model_name]
            
            # 如果没找到，返回默认的qwen-plus配置
            return dashscope_models.get("qwen-plus", {})
            
        except Exception as e:
            print(f"⚠️ 获取模型配置失败: {e}")
            return {}
    
    def _get_api_env_vars(self) -> Dict[str, str]:
        """获取API环境变量"""
        env_vars = {}
        
        if self.api_key:
            # 根据模型类型设置不同的环境变量
            if "qwen" in self.model_name.lower():
                # 通义千问模型使用DashScope API
                env_vars["DASHSCOPE_API_KEY"] = self.api_key
                # 同时设置OPENAI_API_KEY以兼容Midscene
                env_vars["OPENAI_API_KEY"] = self.api_key
            else:
                # 其他模型使用OpenAI API
                env_vars["OPENAI_API_KEY"] = self.api_key
        
        return env_vars
    
    async def execute_ai_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行AI测试用例
        
        Args:
            test_case: 测试用例配置
                {
                    "url": "https://example.com",
                    "actions": [
                        {"type": "aiAction", "instruction": "click login button"},
                        {"type": "aiQuery", "query": "{title: string, price: number}[]"},
                        {"type": "aiAssert", "assertion": "there is a search box"}
                    ],
                    "mode": "playwright|yaml|auto",
                    "options": {...}
                }
        """
        start_time = datetime.now()
        case_id = test_case.get("id", f"case_{int(start_time.timestamp())}")
        mode = test_case.get("mode", "auto")
        
        try:
            print(f"🚀 执行AI测试用例: {case_id}")
            print(f"   🌐 URL: {test_case.get('url', 'N/A')}")
            print(f"   🎭 模式: {mode}")
            
            # 智能选择执行模式
            if mode == "auto":
                mode = self._determine_execution_mode(test_case)
            
            # 根据模式执行
            if mode == "playwright":
                result = await self._execute_playwright_mode(test_case)
            elif mode == "yaml":
                result = await self._execute_yaml_mode(test_case)
            else:
                raise ValueError(f"不支持的执行模式: {mode}")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # 更新统计
            self._update_stats(mode, True, execution_time)
            
            print(f"✅ 测试用例执行成功 (耗时: {execution_time:.2f}s)")
            
            return {
                "success": True,
                "case_id": case_id,
                "execution_mode": mode,
                "execution_time": execution_time,
                "result": result,
                "timestamp": start_time.isoformat()
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_stats(mode, False, execution_time)
            
            print(f"❌ 测试用例执行失败: {e}")
            
            return {
                "success": False,
                "case_id": case_id,
                "execution_mode": mode,
                "execution_time": execution_time,
                "error": str(e),
                "timestamp": start_time.isoformat()
            }
    
    def _determine_execution_mode(self, test_case: Dict[str, Any]) -> str:
        """智能确定执行模式"""
        actions = test_case.get("actions", [])
        
        # 复杂逻辑判断
        complex_actions = ["aiQuery", "aiNumber", "aiBoolean", "aiString", "aiLocate"]
        has_complex_actions = any(
            action.get("type") in complex_actions for action in actions
        )
        
        # 条件判断逻辑
        has_conditionals = any(
            "if" in action or "condition" in action for action in actions
        )
        
        # 动态数据处理
        has_dynamic_data = any(
            "extract" in str(action) or "variable" in action for action in actions
        )
        
        if has_complex_actions or has_conditionals or has_dynamic_data:
            return "playwright"
        else:
            return "yaml"
    
    async def _execute_playwright_mode(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Playwright模式执行"""
        # 创建Playwright执行脚本
        script_content = self._generate_playwright_script(test_case)
        script_file = self.temp_dir / f"playwright_script_{int(datetime.now().timestamp())}.js"
        
        # 写入脚本文件
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        try:
            # 执行脚本
            result = await self._execute_nodejs_script(script_file)
            return result
        finally:
            # 清理临时文件
            if script_file.exists():
                script_file.unlink()
    
    def _generate_playwright_script(self, test_case: Dict[str, Any]) -> str:
        """生成Playwright执行脚本"""
        url = test_case.get("url", "about:blank")
        actions = test_case.get("actions", [])
        options = test_case.get("options", {})
        
        script_lines = [
            "import { chromium } from 'playwright';",
            "import { PlaywrightAgent } from '@midscene/web/playwright';",
            "",
            "const sleep = (ms) => new Promise(r => setTimeout(r, ms));",
            "",
            "Promise.resolve((async () => {",
            "  const browser = await chromium.launch({",
            f"    headless: {str(self.headless).lower()},",
            "    args: ['--no-sandbox', '--disable-setuid-sandbox']",
            "  });",
            "",
            "  const page = await browser.newPage();",
            "  await page.setViewportSize({",
            f"    width: {self.viewport_width},",
            f"    height: {self.viewport_height}",
            "  });",
            "",
            f"  await page.goto('{url}');",
            "  await sleep(3000);",
            "",
            "  const agent = new PlaywrightAgent(page);",
            "  const results = {};",
            ""
        ]
        
        # 生成动作代码
        for i, action in enumerate(actions):
            action_type = action.get("type", "")
            action_code = self._generate_action_code(action, i)
            script_lines.extend(action_code)
            script_lines.append("")
        
        # 输出结果和关闭浏览器
        script_lines.extend([
            "  console.log(JSON.stringify(results, null, 2));",
            "  await browser.close();",
            "})().catch(console.error));"
        ])
        
        return "\n".join(script_lines)
    
    def _generate_action_code(self, action: Dict[str, Any], index: int) -> List[str]:
        """生成单个动作的代码"""
        action_type = action.get("type", "")
        
        if action_type == "aiAction":
            instruction = action.get("instruction", "")
            return [
                f"  // Action {index + 1}: AI操作",
                f"  await agent.aiAction('{instruction}');"
            ]
        
        elif action_type == "aiQuery":
            query = action.get("query", "")
            name = action.get("name", f"query_result_{index}")
            return [
                f"  // Action {index + 1}: AI查询",
                f"  const {name} = await agent.aiQuery('{query}');",
                f"  results.{name} = {name};"
            ]
        
        elif action_type == "aiAssert":
            assertion = action.get("assertion", "")
            return [
                f"  // Action {index + 1}: AI断言",
                f"  await agent.aiAssert('{assertion}');"
            ]
        
        elif action_type == "aiWaitFor":
            condition = action.get("condition", "")
            return [
                f"  // Action {index + 1}: AI等待",
                f"  await agent.aiWaitFor('{condition}');"
            ]
        
        elif action_type == "aiNumber":
            question = action.get("question", "")
            name = action.get("name", f"number_result_{index}")
            return [
                f"  // Action {index + 1}: AI数字查询",
                f"  const {name} = await agent.aiNumber('{question}');",
                f"  results.{name} = {name};"
            ]
        
        elif action_type == "aiBoolean":
            question = action.get("question", "")
            name = action.get("name", f"boolean_result_{index}")
            return [
                f"  // Action {index + 1}: AI布尔查询",
                f"  const {name} = await agent.aiBoolean('{question}');",
                f"  results.{name} = {name};"
            ]
        
        elif action_type == "aiString":
            question = action.get("question", "")
            name = action.get("name", f"string_result_{index}")
            return [
                f"  // Action {index + 1}: AI字符串查询",
                f"  const {name} = await agent.aiString('{question}');",
                f"  results.{name} = {name};"
            ]
        
        elif action_type == "aiLocate":
            target = action.get("target", "")
            name = action.get("name", f"location_result_{index}")
            return [
                f"  // Action {index + 1}: AI定位",
                f"  const {name} = await agent.aiLocate('{target}');",
                f"  results.{name} = {name};"
            ]
        
        elif action_type == "aiTap":
            target = action.get("target", "")
            return [
                f"  // Action {index + 1}: AI点击",
                f"  await agent.aiTap('{target}');"
            ]
        
        elif action_type == "sleep":
            duration = action.get("duration", 1000)
            return [
                f"  // Action {index + 1}: 等待",
                f"  await sleep({duration});"
            ]
        
        else:
            return [
                f"  // Action {index + 1}: 未知操作类型 {action_type}",
                f"  console.warn('未支持的操作类型: {action_type}');"
            ]
    
    async def _execute_yaml_mode(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """YAML模式执行"""
        # 生成YAML配置
        yaml_content = self._generate_yaml_config(test_case)
        yaml_file = self.temp_dir / f"yaml_script_{int(datetime.now().timestamp())}.yaml"
        
        # 写入YAML文件
        with open(yaml_file, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        try:
            # 使用midscene CLI执行
            result = await self._execute_midscene_cli(yaml_file)
            return result
        finally:
            # 清理临时文件
            if yaml_file.exists():
                yaml_file.unlink()
    
    def _generate_yaml_config(self, test_case: Dict[str, Any]) -> str:
        """生成YAML配置"""
        url = test_case.get("url", "about:blank")
        actions = test_case.get("actions", [])
        options = test_case.get("options", {})
        
        yaml_config = {
            "web": {
                "url": url,
                "viewportWidth": self.viewport_width,
                "viewportHeight": self.viewport_height,
                "output": str(self.temp_dir / "output.json")
            },
            "tasks": []
        }
        
        # 按类型分组动作
        current_task = {
            "name": "ai_test_execution",
            "flow": []
        }
        
        for action in actions:
            action_type = action.get("type", "")
            
            if action_type == "aiAction":
                current_task["flow"].append({
                    "aiAction": action.get("instruction", "")
                })
            
            elif action_type == "aiQuery":
                flow_item = {
                    "aiQuery": action.get("query", "")
                }
                if action.get("name"):
                    flow_item["name"] = action["name"]
                current_task["flow"].append(flow_item)
            
            elif action_type == "aiAssert":
                current_task["flow"].append({
                    "aiAssert": action.get("assertion", "")
                })
            
            elif action_type == "aiWaitFor":
                current_task["flow"].append({
                    "aiWaitFor": action.get("condition", "")
                })
            
            elif action_type == "aiNumber":
                current_task["flow"].append({
                    "aiNumber": action.get("question", "")
                })
            
            elif action_type == "aiBoolean":
                current_task["flow"].append({
                    "aiBoolean": action.get("question", "")
                })
            
            elif action_type == "aiString":
                current_task["flow"].append({
                    "aiString": action.get("question", "")
                })
            
            elif action_type == "aiLocate":
                current_task["flow"].append({
                    "aiLocate": action.get("target", "")
                })
            
            elif action_type == "aiTap":
                current_task["flow"].append({
                    "aiAction": f"click {action.get('target', '')}"
                })
            
            elif action_type == "sleep":
                current_task["flow"].append({
                    "sleep": action.get("duration", 1000)
                })
        
        yaml_config["tasks"].append(current_task)
        
        return yaml.dump(yaml_config, default_flow_style=False, allow_unicode=True)
    
    async def _execute_nodejs_script(self, script_file: Path) -> Dict[str, Any]:
        """执行Node.js脚本"""
        try:
            # 设置环境变量
            env = os.environ.copy()
            env_vars = self._get_api_env_vars()
            env.update(env_vars)
            
            # 执行脚本
            process = await asyncio.create_subprocess_exec(
                "npx", "tsx", str(script_file),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
                cwd=str(script_file.parent)
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
                    "error": stderr.decode() or "脚本执行失败",
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"脚本执行异常: {e}"
            }
    
    async def _execute_midscene_cli(self, yaml_file: Path) -> Dict[str, Any]:
        """执行Midscene CLI"""
        try:
            # 设置环境变量
            env = os.environ.copy()
            env_vars = self._get_api_env_vars()
            env.update(env_vars)
            
            # 构建命令
            cmd = ["midscene", str(yaml_file)]
            if self.headless:
                cmd.append("--headless")
            
            # 执行命令
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                # 尝试读取输出文件
                output_file = self.temp_dir / "output.json"
                output_data = {}
                
                if output_file.exists():
                    try:
                        with open(output_file, 'r', encoding='utf-8') as f:
                            output_data = json.load(f)
                        output_file.unlink()  # 清理输出文件
                    except:
                        pass
                
                return {
                    "success": True,
                    "data": output_data,
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode()
                }
            else:
                return {
                    "success": False,
                    "error": stderr.decode() or "YAML执行失败",
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode()
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"CLI执行异常: {e}"
            }
    
    def _update_stats(self, mode: str, success: bool, execution_time: float):
        """更新执行统计"""
        self.execution_stats["total_executions"] += 1
        
        if success:
            self.execution_stats["successful_executions"] += 1
        else:
            self.execution_stats["failed_executions"] += 1
        
        if mode == "playwright":
            self.execution_stats["playwright_executions"] += 1
        elif mode == "yaml":
            self.execution_stats["yaml_executions"] += 1
        
        # 更新平均执行时间
        total = self.execution_stats["total_executions"]
        current_avg = self.execution_stats["average_execution_time"]
        self.execution_stats["average_execution_time"] = (
            (current_avg * (total - 1) + execution_time) / total
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """获取执行统计"""
        return self.execution_stats.copy()
    
    async def cleanup(self):
        """清理资源"""
        try:
            # 清理临时目录
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            print("🧹 Midscene执行器资源清理完成")
        except Exception as e:
            print(f"⚠️ 清理过程中出现异常: {e}")

# 便捷函数
async def execute_midscene_test_case(
    test_case: Dict[str, Any],
    headless: bool = True,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """执行Midscene测试用例的便捷函数"""
    executor = MidsceneAgentExecutor(
        headless=headless,
        api_key=api_key
    )
    
    try:
        return await executor.execute_ai_test_case(test_case)
    finally:
        await executor.cleanup()

# 示例测试用例
EXAMPLE_TEST_CASES = {
    "ebay_search": {
        "id": "ebay_headphone_search",
        "url": "https://www.ebay.com",
        "mode": "auto",
        "actions": [
            {
                "type": "aiAction",
                "instruction": "type 'Headphones' in search box, hit Enter"
            },
            {
                "type": "aiWaitFor",
                "condition": "there is at least one headphone item on page"
            },
            {
                "type": "aiQuery",
                "query": "{itemTitle: string, price: number}[], find item in list and corresponding price",
                "name": "headphones"
            },
            {
                "type": "aiNumber",
                "question": "What is the price of the first headphone?",
                "name": "first_price"
            },
            {
                "type": "aiBoolean",
                "question": "Is the price of the headphones more than 1000?",
                "name": "is_expensive"
            },
            {
                "type": "aiAssert",
                "assertion": "There is a category filter on the left"
            }
        ]
    },
    
    "simple_navigation": {
        "id": "simple_page_test",
        "url": "https://example.com",
        "mode": "yaml",
        "actions": [
            {
                "type": "aiAssert",
                "assertion": "There is a heading on the page"
            },
            {
                "type": "aiString",
                "question": "What is the main heading text?",
                "name": "heading_text"
            }
        ]
    }
}
