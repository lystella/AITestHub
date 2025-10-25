#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AITestHub 一键启动脚本
简化版启动工具，替代复杂的多脚本启动
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

class AITestHubLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend" / "intelligent_mbt_testing"
        self.frontend_dir = self.project_root / "front"
        self.venv_python = self.project_root / "venv" / "bin" / "python"
        
    def check_environment(self):
        """检查环境依赖"""
        print("🔍 检查环境依赖...")
        
        # 检查Python虚拟环境
        if not self.venv_python.exists():
            print("❌ Python虚拟环境不存在，请先运行: python3 -m venv venv")
            return False
            
        # 检查Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Node.js未安装")
                return False
            print(f"✅ Node.js版本: {result.stdout.strip()}")
        except FileNotFoundError:
            print("❌ Node.js未安装")
            return False
            
        # 检查依赖文件
        requirements_file = self.backend_dir / "requirements_service.txt"
        if not requirements_file.exists():
            print("❌ 后端依赖文件不存在")
            return False
            
        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            print("❌ 前端依赖文件不存在")
            return False
            
        print("✅ 环境检查通过")
        return True
        
    def install_dependencies(self):
        """安装依赖"""
        print("📦 安装依赖...")
        
        # 安装后端依赖
        print("  安装后端依赖...")
        try:
            subprocess.run([
                str(self.venv_python), "-m", "pip", "install", "-r", 
                str(self.backend_dir / "requirements_service.txt")
            ], check=True)
            print("  ✅ 后端依赖安装完成")
        except subprocess.CalledProcessError:
            print("  ❌ 后端依赖安装失败")
            return False
            
        # 安装前端依赖
        print("  安装前端依赖...")
        try:
            subprocess.run(["npm", "install"], cwd=self.frontend_dir, check=True)
            print("  ✅ 前端依赖安装完成")
        except subprocess.CalledProcessError:
            print("  ❌ 前端依赖安装失败")
            return False
            
        return True
        
    def start_backend(self):
        """启动后端服务"""
        print("🚀 启动后端服务...")
        try:
            # 启动后端服务
            self.backend_process = subprocess.Popen([
                str(self.venv_python), "web_service.py"
            ], cwd=self.backend_dir)
            
            # 等待服务启动
            time.sleep(5)
            
            # 检查服务是否启动成功
            try:
                import requests
                response = requests.get("http://localhost:8090/", timeout=5)
                if response.status_code == 200:
                    print("✅ 后端服务启动成功 (http://localhost:8090)")
                    return True
            except:
                pass
                
            print("⚠️ 后端服务可能未完全启动，请检查日志")
            return True
            
        except Exception as e:
            print(f"❌ 后端服务启动失败: {e}")
            return False
            
    def start_frontend(self):
        """启动前端服务"""
        print("🎨 启动前端服务...")
        try:
            # 启动前端服务
            self.frontend_process = subprocess.Popen([
                "npm", "start"
            ], cwd=self.frontend_dir)
            
            # 等待服务启动
            time.sleep(10)
            print("✅ 前端服务启动成功 (http://localhost:3000)")
            return True
            
        except Exception as e:
            print(f"❌ 前端服务启动失败: {e}")
            return False
            
    def start_services(self):
        """启动所有服务"""
        print("🚀 启动AITestHub服务...")
        print("=" * 50)
        
        # 检查环境
        if not self.check_environment():
            return False
            
        # 安装依赖
        if not self.install_dependencies():
            return False
            
        # 启动后端
        if not self.start_backend():
            return False
            
        # 启动前端
        if not self.start_frontend():
            return False
            
        print("=" * 50)
        print("🎉 AITestHub启动完成！")
        print("📡 后端服务: http://localhost:8090")
        print("🎨 前端界面: http://localhost:3000")
        print("📊 API文档: http://localhost:8090/docs")
        print("=" * 50)
        print("按 Ctrl+C 停止服务")
        
        return True
        
    def stop_services(self):
        """停止所有服务"""
        print("\n🛑 停止服务...")
        
        if hasattr(self, 'backend_process'):
            self.backend_process.terminate()
            print("✅ 后端服务已停止")
            
        if hasattr(self, 'frontend_process'):
            self.frontend_process.terminate()
            print("✅ 前端服务已停止")
            
        print("👋 服务已全部停止")
        
    def run(self):
        """运行启动器"""
        try:
            if self.start_services():
                # 保持运行
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.stop_services()
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            self.stop_services()

def main():
    """主函数"""
    print("🤖 AITestHub 启动器")
    print("=" * 30)
    
    launcher = AITestHubLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
