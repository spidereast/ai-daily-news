#!/bin/bash
# 完整部署脚本 - 从零开始部署到GitHub Pages

set -e

echo "🚀 AI Daily News 完整部署"
echo "============================"

# 检查Git
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装"
    exit 1
fi

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo "❌ 不在Git仓库中，请先创建仓库"
    echo "   1. 在GitHub创建仓库: spidereast/ai-daily-news"
    echo "   2. git clone https://github.com/spidereast/ai-daily-news.git"
    echo "   3. 复制所有文件到仓库目录"
    exit 1
fi

# 检查API密钥
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  未设置OPENROUTER_API_KEY"
    read -p "请输入OpenRouter API密钥: " api_key
    export OPENROUTER_API_KEY="$api_key"
fi

# 1. 安装依赖
echo "📦 安装依赖..."
pip3 install -r requirements.txt --user
npm install

# 2. 生成内容
echo "🔄 生成日报..."
python3 src/main.py --date "$(date +%Y-%m-%d)"

# 3. 构建VitePress
echo "🏗️  构建VitePress..."
npm run docs:build

# 4. 提交并推送
echo "📤 提交到GitHub..."
git add content/ docs/
git commit -m "🤖 Update $(date '+%Y-%m-%d')"
git push origin main

echo ""
echo "✅ 部署完成！"
echo "🌐 网站地址: https://spidereast.github.io/ai-daily-news/"
echo "⏰ 下次自动更新: 明天 8:00"