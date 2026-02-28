#!/bin/bash

echo "🚀 礼纪APP启动脚本"
echo "===================="

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未安装Node.js"
    echo "请先安装Node.js: https://nodejs.org"
    exit 1
fi

echo "✅ Node.js已安装"

# 进入项目目录
cd "$(dirname "$0")"

# 安装依赖（如果未安装）
if [ ! -d "backend/node_modules" ]; then
    echo "📦 正在安装依赖..."
    cd backend
    npm install
    cd ..
fi

# 初始化数据库（如果不存在）
if [ ! -f "database/liji.db" ]; then
    echo "🗄️ 正在初始化数据库..."
    cd database
    node init.js
    cd ..
fi

# 创建上传目录
if [ ! -d "uploads" ]; then
    mkdir uploads
fi

echo "🌐 启动服务器..."
echo ""
echo "应用将在以下地址运行："
echo "  - 本地: http://localhost:3000"
echo "  - 网络: http://$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | head -n 1):3000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

cd backend
npm start
