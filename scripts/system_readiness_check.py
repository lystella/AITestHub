#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多智能体系统可用性检查脚本
检查系统是否可以直接使用
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, List
import importlib.util

class SystemReadinessChecker:
    """系统可用性检查器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend" / "intelligent_mbt_testing"
        self.frontend_dir = self.project_root / "front"
        
        self.check_results = {
            "overall_ready": False,
            "backend_ready": False,
            "frontend_ready": False,
            "dependencies_ready": False,
            "config_ready": False,
            "issues": [],
            "recommendations": []
        }
    
    def run_full_check(self) -> Dict[str, Any]:
        """运行完整的系统检查"""
        print("🔍 开始系统可用性检查...")
        print("=" * 60)
        
        # 1. 检查项目结构
        self._check_project_structure()
        
        # 2. 检查Python依赖
        self._check_python_dependencies()
        
        # 3. 检查配置文件
        self._check_configuration()
        
        # 4. 检查后端系统
        self._check_backend_system()
        
        # 5. 检查前端系统
        self._check_frontend_system()
        
        # 6. 生成总体评估
        self._generate_overall_assessment()
        
        # 7. 显示结果
        self._display_results()
        
        return self.check_results
    
    def _check_project_structure(self):
        """检查项目结构"""
        print("📁 检查项目结构...")
        
        required_dirs = [
            "backend/intelligent_mbt_testing",
            "backend/intelligent_mbt_testing/enhanced_agents", 
            "backend/intelligent_mbt_testing/tools",
            "front/src",
            "front/src/pages",
            "front/src/components"
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                missing_dirs.append(dir_path)
        
        if missing_dirs:
            self.check_results["issues"].append(f"缺少目录: {', '.join(missing_dirs)}")
        else:
            print("   ✅ 项目结构完整")
    
    def _check_python_dependencies(self):
        """检查Python依赖"""
        print("🐍 检查Python依赖...")
        
        required_packages = [
            "fastapi",
            "uvicorn", 
            "agentscope",
            "dashscope",
            "qdrant_client",
            "pydantic",
            "asyncio",
            "pathlib"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                if package == "asyncio" or package == "pathlib":
                    # 内置模块
                    continue
                    
                __import__(package)
                print(f"   ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"   ❌ {package} - 未安装")
        
        if missing_packages:
            self.check_results["issues"].append(f"缺少Python包: {', '.join(missing_packages)}")
            self.check_results["recommendations"].append(f"安装缺少的包: pip install {' '.join(missing_packages)}")
        else:
            self.check_results["dependencies_ready"] = True
    
    def _check_configuration(self):
        """检查配置文件"""
        print("⚙️ 检查配置文件...")
        
        config_file = self.backend_dir / "enhanced_config.json"
        
        if not config_file.exists():
            self.check_results["issues"].append("配置文件不存在: enhanced_config.json")
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查关键配置
            if "models" not in config:
                self.check_results["issues"].append("配置文件缺少models配置")
                return
            
            # 检查API密钥
            dashscope_config = config.get("models", {}).get("dashscope", {})
            qwen_plus_config = dashscope_config.get("qwen-plus", {})
            
            if not qwen_plus_config.get("api_key"):
                self.check_results["issues"].append("缺少DashScope API密钥配置")
                self.check_results["recommendations"].append("在enhanced_config.json中配置有效的API密钥")
            else:
                print("   ✅ API密钥已配置")
                self.check_results["config_ready"] = True
            
        except json.JSONDecodeError:
            self.check_results["issues"].append("配置文件格式错误")
        except Exception as e:
            self.check_results["issues"].append(f"配置文件检查失败: {e}")
    
    def _check_backend_system(self):
        """检查后端系统"""
        print("🔧 检查后端系统...")
        
        # 检查关键文件
        key_files = [
            "web_service.py",
            "enhanced_intelligent_testing_system.py",
            "enhanced_agents/__init__.py",
            "enhanced_agents/enhanced_executor_agent.py",
            "enhanced_agents/enhanced_coordinator_agent.py",
            "tools/midscene_agent_executor.py"
        ]
        
        missing_files = []
        for file_path in key_files:
            full_path = self.backend_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.check_results["issues"].append(f"后端缺少文件: {', '.join(missing_files)}")
        else:
            print("   ✅ 后端核心文件完整")
            
            # 尝试导入核心模块
            try:
                sys.path.insert(0, str(self.backend_dir))
                
                # 检查核心导入
                import enhanced_intelligent_testing_system
                
                # 检查智能体导入
                enhanced_agents_dir = self.backend_dir / "enhanced_agents"
                sys.path.insert(0, str(enhanced_agents_dir))
                
                import enhanced_executor_agent
                import enhanced_coordinator_agent
                
                print("   ✅ 核心模块导入成功")
                self.check_results["backend_ready"] = True
                
            except Exception as e:
                self.check_results["issues"].append(f"后端模块导入失败: {e}")
                print(f"   ❌ 模块导入失败: {e}")
    
    def _check_frontend_system(self):
        """检查前端系统"""
        print("🌐 检查前端系统...")
        
        # 检查package.json
        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            self.check_results["issues"].append("前端package.json文件不存在")
            return
        
        # 检查关键文件
        key_files = [
            "src/App.js",
            "src/pages/MultiAgentCollaboration.js",
            "src/pages/TestReports.js",
            "src/components/Sidebar.js",
            "src/components/Dashboard.js"
        ]
        
        missing_files = []
        for file_path in key_files:
            full_path = self.frontend_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.check_results["issues"].append(f"前端缺少文件: {', '.join(missing_files)}")
        else:
            print("   ✅ 前端核心文件完整")
        
        # 检查node_modules
        node_modules = self.frontend_dir / "node_modules"
        if not node_modules.exists():
            self.check_results["issues"].append("前端依赖未安装 (node_modules不存在)")
            self.check_results["recommendations"].append("在front目录运行: npm install")
        else:
            print("   ✅ 前端依赖已安装")
            self.check_results["frontend_ready"] = True
    
    def _generate_overall_assessment(self):
        """生成总体评估"""
        ready_components = sum([
            self.check_results["backend_ready"],
            self.check_results["frontend_ready"], 
            self.check_results["dependencies_ready"],
            self.check_results["config_ready"]
        ])
        
        self.check_results["overall_ready"] = (ready_components >= 3 and len(self.check_results["issues"]) == 0)
    
    def _display_results(self):
        """显示检查结果"""
        print("\n" + "=" * 60)
        print("📊 系统可用性检查结果")
        print("=" * 60)
        
        # 组件状态
        components = [
            ("后端系统", self.check_results["backend_ready"]),
            ("前端系统", self.check_results["frontend_ready"]),
            ("Python依赖", self.check_results["dependencies_ready"]),
            ("配置文件", self.check_results["config_ready"])
        ]
        
        for name, ready in components:
            status = "✅ 就绪" if ready else "❌ 未就绪"
            print(f"{name:12} {status}")
        
        # 问题列表
        if self.check_results["issues"]:
            print(f"\n🚨 发现 {len(self.check_results['issues'])} 个问题:")
            for i, issue in enumerate(self.check_results["issues"], 1):
                print(f"   {i}. {issue}")
        
        # 建议
        if self.check_results["recommendations"]:
            print(f"\n💡 建议:")
            for i, rec in enumerate(self.check_results["recommendations"], 1):
                print(f"   {i}. {rec}")
        
        # 总体状态
        print("\n" + "=" * 60)
        if self.check_results["overall_ready"]:
            print("🎉 系统可以直接使用！")
            print("\n🚀 启动方式:")
            print("   后端: cd backend/intelligent_mbt_testing && python web_service.py")
            print("   前端: cd front && npm start")
            print("   访问: http://localhost:3000")
        else:
            print("⚠️ 系统尚未完全就绪，请解决上述问题后再使用")
        
        print("=" * 60)
    
    def generate_startup_guide(self) -> str:
        """生成启动指南"""
        guide = """
# 🚀 多智能体系统启动指南

## 系统检查结果
"""
        
        if self.check_results["overall_ready"]:
            guide += """
✅ **系统已就绪，可以直接使用！**

## 快速启动

### 方式1: 使用启动脚本
```bash
python start_multi_agent_system.py
```

### 方式2: 分别启动
```bash
# 启动后端 (终端1)
cd backend/intelligent_mbt_testing
python web_service.py

# 启动前端 (终端2) 
cd front
npm start
```

## 访问地址
- 前端界面: http://localhost:3000
- 后端API: http://localhost:8080
- API文档: http://localhost:8080/docs

## 主要功能
1. **多智能体协作** - 上传需求文档，AI智能体协作分析和执行
2. **测试报告可视化** - 查看详细的测试执行报告和统计
3. **Midscene AI测试** - AI驱动的Web自动化测试
4. **实时监控** - WebSocket实时显示执行进度

"""
        else:
            guide += """
❌ **系统尚未完全就绪**

## 需要解决的问题
"""
            for issue in self.check_results["issues"]:
                guide += f"- {issue}\n"
            
            guide += "\n## 解决建议\n"
            for rec in self.check_results["recommendations"]:
                guide += f"- {rec}\n"
        
        return guide

def main():
    """主函数"""
    checker = SystemReadinessChecker()
    results = checker.run_full_check()
    
    # 生成启动指南
    guide = checker.generate_startup_guide()
    
    # 保存到文件
    guide_file = Path("SYSTEM_STARTUP_GUIDE.md")
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print(f"\n📄 启动指南已保存到: {guide_file}")
    
    return results["overall_ready"]

if __name__ == "__main__":
    ready = main()
    sys.exit(0 if ready else 1)
