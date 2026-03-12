# 🚀 AI Daily News - 完整部署指南

## 📋 目录

1. [前提条件](#前提条件)
2. [快速部署](#快速部署)
3. [手动配置](#手动配置)
4. [使用说明](#使用说明)
5. [故障排除](#故障排除)
6. [自定义配置](#自定义配置)

---

## 📦 前提条件

- ✅ GitHub 账号
- ✅ OpenRouter 账号（用于AI摘要）
- ✅ 本地 Git 环境（可选，用于本地开发）

---

## 🏃 快速部署（推荐）

### 步骤1： Fork 或克隆仓库

```bash
# 如果项目已公开，直接Fork
# 如果私有，克隆到本地
git clone https://github.com/spidereast/ai-daily-news.git
cd ai-daily-news
```

### 步骤2：设置 OpenRouter API 密钥

1. 访问 https://openrouter.ai/
2. 注册/登录账号
3. 进入 [API Keys](https://openrouter.ai/keys)
4. 创建新密钥
5. 在GitHub仓库中设置：
   - 进入仓库 → Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - Name: `OPENROUTER_API_KEY`
   - Value: 你的API密钥

### 步骤3：启用 GitHub Pages

1. 进入仓库 → Settings → Pages
2. **Source**: 选择 `GitHub Actions`
3. 点击 Save

### 步骤4：首次运行

**方式A：自动运行**
- 等待明天北京时间8点自动运行

**方式B：手动触发**
1. 进入仓库 → Actions
2. 选择 "AI Daily News - 自动生成"
3. 点击 "Run workflow" → "Run workflow"
4. 等待5-10分钟完成

### 步骤5：访问网站

```
https://spidereast.github.io/ai-daily-news/
```

---

## 🔧 手动配置（如需要）

### 安装本地依赖

```bash
# Python依赖
pip3 install -r requirements.txt

# Node.js依赖
npm install
```

### 配置环境变量

```bash
# 复制环境变量示例
cp .env.example .env

# 编辑.env文件，填入你的OPENROUTER_API_KEY
```

### 本地测试运行

```bash
# 测试模式（使用模拟数据）
python3 src/main.py --test

# 正式运行（需要API密钥）
OPENROUTER_API_KEY=your-key python3 src/main.py --date 2025-03-12
```

### 本地预览网站

```bash
# 安装VitePress依赖
npm install

# 启动开发服务器
npm run docs:dev

# 访问 http://localhost:5173
```

---

## 📱 使用说明

### 自动运行

- **时间**：每天北京时间8:00（UTC 0:00）
- **触发**：GitHub Actions定时任务
- **操作**：自动采集 → AI摘要 → 生成Markdown → 部署Pages

### 手动采集

1. 访问：`https://github.com/spidereast/ai-daily-news/actions/workflows/daily.yml`
2. 点击 "Run workflow"
3. 确认运行
4. 等待完成后访问网站

### 查看内容

- **首页**：`/` - 显示最新一期
- **今日**：`/daily/current` - 自动跳转到最新
- **归档**：`/daily/archive` - 历史列表

---

## ⚙️ 自定义配置

### 添加/修改新闻源

编辑 `src/config/sources.yaml`：

```yaml
rss_feeds:
  # 添加新源
  - name: "我的新闻源"
    url: "https://example.com/rss"
    type: "tech"  # 分类: ai, programming, tech, startup, economy, digital, hightech, ev, imaging
    max_items: 5  # 最多获取文章数
```

支持的分类：
- `ai` - 人工智能
- `programming` - 编程开发
- `tech` - 科技数码
- `startup` - 创业投资
- `economy` - 经济金融
- `digital` - 数码产品
- `hightech` - 高科技
- `ev` - 新能源汽车
- `imaging` - 数码影像

### 调整AI摘要

编辑 `src/ai_processor.py` 中的提示词：

```python
self.default_prompt = """你是一个专业的编辑。请为新闻生成摘要..."""
```

### 修改VitePress主题

编辑 `.vitepress/config.ts`：

```typescript
export default defineConfig({
  title: '你的站点标题',
  themeConfig: {
    nav: [ /* 自定义导航 */ ],
    sidebar: { /* 自定义侧边栏 */ }
  }
})
```

---

## 🐛 故障排除

### 常见问题

#### 1. 工作流失败：`OPENROUTER_API_KEY` 未设置

**解决**：在GitHub Secrets中正确设置密钥

#### 2. 没有文章采集到

**原因**：某些RSS源可能被墙或失效

**解决**：
- 检查网络连接
- 编辑 `sources.yaml` 注释掉有问题的源
- 只保留稳定的源（如Hacker News）

#### 3. GitHub Pages 404

**原因**：Pages未正确配置或构建失败

**解决**：
1. 检查 Settings → Pages，Source应为 `GitHub Actions`
2. 查看Actions日志，确认构建成功
3. 等待几分钟缓存刷新

#### 4. AI摘要失败

**原因**：API调用限制或错误

**解决**：
- 检查OpenRouter账户余额
- 确认API密钥有效
- 查看日志中的具体错误

#### 5. 本地运行报错：缺少依赖

**解决**：
```bash
pip3 install -r requirements.txt
```

---

## 🔍 查看日志

### GitHub Actions日志

1. 进入仓库 → Actions
2. 点击失败的运行
3. 查看各步骤日志输出

### 本地调试

```bash
# 详细日志
python3 src/main.py --date 2025-03-12 2>&1 | tee generate.log
```

---

## 📊 项目结构说明

```
ai-daily-news/
├── .github/
│   └── workflows/
│       └── daily.yml        # GitHub Actions工作流（自动+手动）
├── src/
│   ├── main.py              # 主程序
│   ├── collectors/          # 采集器（RSS等）
│   ├── ai_processor.py      # AI摘要处理
│   ├── markdown_generator.py # Markdown生成
│   ├── utils.py             # 工具函数
│   └── config/
│       └── sources.yaml     # 新闻源配置
├── .vitepress/
│   └── config.ts            # VitePress配置
├── content/
│   └── daily/               # 生成的Markdown文件
│       └── 2025/
│           └── 03-12.md
├── docs/                    # VitePress文档源
│   ├── index.md             # 首页
│   ├── manual.md            # 手动采集指引
│   └── daily/
│       ├── current.md       # 今日（跳转）
│       └── archive.md       # 归档
├── scripts/
│   ├── generate.sh          # 本地生成脚本
│   └── deploy.sh            # 完整部署脚本
├── requirements.txt         # Python依赖
├── package.json             # Node依赖
├── .env.example             # 环境变量示例
└── README.md                # 项目说明
```

---

## 🆘 需要帮助？

- 📖 [项目README](README.md)
- 🐛 [提交Issue](https://github.com/spidereast/ai-daily-news/issues)
- 💬 [讨论区](https://github.com/spidereast/ai-daily-news/discussions)

---

## ✅ 检查清单

完成部署后，确认以下项目：

- [ ] GitHub仓库已创建
- [ ] OPENROUTER_API_KEY 已设置
- [ ] GitHub Pages 启用（Source: GitHub Actions）
- [ ] Actions工作流已手动触发一次
- [ ] 网站可访问：`https://spidereast.github.io/ai-daily-news/`
- [ ] 首页显示最新内容
- [ ] 手动采集按钮可用

---

**🎉 祝你使用愉快！AI Daily News 将每天为你自动收集最新资讯。**

---

*最后更新: 2025-03-12*