#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多Agent智能协作系统启动脚本
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("🤖 多Agent智能协作测试系统")
    print("=" * 60)
    print("✨ 基于AgentScope框架的6个专业智能体协作")
    print("🔄 支持实时流式输出和WebSocket通信")
    print("🎯 完整的端到端测试解决方案")
    print("=" * 60)

def check_requirements():
    """检查系统要求"""
    print("🔍 检查系统要求...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    
    # 检查后端依赖
    backend_dir = Path("backend/intelligent_mbt_testing")
    if not backend_dir.exists():
        print("❌ 找不到后端目录")
        return False
    
    # 检查前端依赖
    frontend_dir = Path("front")
    if not frontend_dir.exists():
        print("❌ 找不到前端目录")
        return False
    
    print("✅ 系统要求检查通过")
    return True

def install_backend_dependencies():
    """安装后端依赖"""
    print("📦 安装后端依赖...")
    
    backend_dir = Path("backend/intelligent_mbt_testing")
    requirements_file = backend_dir / "requirements_service.txt"
    
    if requirements_file.exists():
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, cwd=backend_dir)
            print("✅ 后端依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ 后端依赖安装失败: {e}")
            return False
    else:
        print("⚠️ 未找到requirements_service.txt，跳过依赖安装")
    
    return True

def install_frontend_dependencies():
    """安装前端依赖"""
    print("📦 安装前端依赖...")
    
    frontend_dir = Path("front")
    
    try:
        # 检查npm是否可用
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        
        # 安装依赖
        subprocess.run(["npm", "install"], check=True, cwd=frontend_dir)
        print("✅ 前端依赖安装完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 前端依赖安装失败: {e}")
        return False
    except FileNotFoundError:
        print("❌ 未找到npm，请先安装Node.js")
        return False

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    
    backend_dir = Path("backend/intelligent_mbt_testing")
    
    try:
        # 启动后端服务
        backend_process = subprocess.Popen([
            sys.executable, "start_service.py", "--mode", "web", "--port", "8080"
        ], cwd=backend_dir)
        
        print("✅ 后端服务启动中... (端口: 8080)")
        return backend_process
        
    except Exception as e:
        print(f"❌ 后端服务启动失败: {e}")
        return None

def start_frontend():
    """启动前端服务"""
    print("🌐 启动前端服务...")
    
    frontend_dir = Path("front")
    
    try:
        # 启动前端服务
        frontend_process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_dir)
        
        print("✅ 前端服务启动中... (端口: 3000)")
        return frontend_process
        
    except Exception as e:
        print(f"❌ 前端服务启动失败: {e}")
        return None

def wait_for_services():
    """等待服务启动"""
    print("⏳ 等待服务启动...")
    time.sleep(10)  # 等待服务启动

def open_browser():
    """打开浏览器"""
    print("🌐 打开浏览器...")
    try:
        webbrowser.open("http://localhost:3000/dashboard")
        print("✅ 浏览器已打开")
    except Exception as e:
        print(f"⚠️ 无法自动打开浏览器: {e}")
        print("请手动访问: http://localhost:3000/dashboard")

def main():
    """主函数"""
    print_banner()
    
    # 检查系统要求
    if not check_requirements():
        sys.exit(1)
    
    # 安装依赖
    print("\n📋 安装依赖...")
    if not install_backend_dependencies():
        sys.exit(1)
    
    if not install_frontend_dependencies():
        sys.exit(1)
    
    # 启动服务
    print("\n🚀 启动服务...")
    backend_process = start_backend()
    if not backend_process:
        sys.exit(1)
    
    time.sleep(3)  # 等待后端启动
    
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        sys.exit(1)
    
    # 等待服务启动并打开浏览器
    wait_for_services()
    open_browser()
    
    print("\n" + "=" * 60)
    print("🎉 多Agent智能协作系统启动成功！")
    print("=" * 60)
    print("📱 前端地址: http://localhost:3000")
    print("🔧 后端API: http://localhost:8080")
    print("📖 API文档: http://localhost:8080/docs")
    print("=" * 60)
    print("💡 使用说明:")
    print("1. 访问 http://localhost:3000/dashboard")
    print("2. 点击 '多Agent智能调度' 卡片")
    print("3. 上传需求文档 (Word/PDF/TXT)")
    print("4. 点击 '开始多Agent协作分析'")
    print("5. 观察实时执行过程和日志输出")
    print("=" * 60)
    print("⚠️ 按 Ctrl+C 停止所有服务")
    print("=" * 60)
    
    try:
        # 等待用户中断
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🔄 正在停止服务...")
        
        # 停止服务
        if frontend_process:
            frontend_process.terminate()
        if backend_process:
            backend_process.terminate()
        
        print("✅ 所有服务已停止")

if __name__ == "__main__":
    main()
