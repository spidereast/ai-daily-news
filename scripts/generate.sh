#!/bin/bash
# 本地生成日报脚本

set -e

echo "🚀 AI Daily News 本地生成"
echo "============================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

# 进入项目目录
cd "$(dirname "$0")/.."

# 检查依赖
echo "📦 检查Python依赖..."
if ! python3 -c "import feedparser, requests, bs4, openai" 2>/dev/null; then
    echo "⚠️  依赖未安装，正在安装..."
    pip3 install -r requirements.txt --user
fi

# 设置API密钥（从环境变量或提示输入）
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  未设置OPENROUTER_API_KEY环境变量"
    read -p "请输入你的OpenRouter API密钥: " api_key
    export OPENROUTER_API_KEY="$api_key"
fi

# 运行生成
echo "🔄 开始生成..."
python3 src/main.py --date "$(date +%Y-%m-%d)"

# 检查生成结果
if [ -d "content/daily" ]; then
    echo ""
    echo "✅ 生成成功！"
    echo "📁 生成的文件："
    find content/daily -name "*.md" -type f | tail -1 | xargs ls -lh
    echo ""
    echo "🌐 本地预览："
    echo "   npm install"
    echo "   npm run docs:dev"
else
    echo "❌ 生成失败，请检查错误信息"
    exit 1
fi