# AI Daily News

自动收集AI/编程/科技/创业/经济/数码/新能源汽车/数码影像等领域的最新信息，生成每日通讯，并自动部署到GitHub Pages。

## ✨ 功能特点

- ⏰ **自动运行**：每天北京时间8点自动更新
- 🖱️ **手动触发**：点击按钮即时采集最新信息
- 📊 **多领域覆盖**：9大领域，30+新闻源
- 🤖 **AI摘要**：使用Step 3.5 Flash生成智能摘要
- 🎨 **精美展示**：VitePress构建的现代化网站
- ☁️ **免费托管**：GitHub Pages自动部署

## 🏗️ 技术架构

- **前端**：VitePress (Vue + Markdown)
- **采集**：Python 3 (feedparser, requests, beautifulsoup4)
- **AI处理**：OpenRouter API (Step 3.5 Flash)
- **自动化**：GitHub Actions
- **部署**：GitHub Pages

## 📁 项目结构

```
ai-daily-news/
├── .github/workflows/    # GitHub Actions工作流
│   ├── daily.yml        # 每天8点自动运行
│   └── manual.yml       # 手动触发
├── src/                 # Python采集和AI处理
│   ├── collectors/      # 各源采集器
│   ├── ai_processor.py  # AI摘要生成
│   ├── markdown_gen.py  # Markdown生成
│   └── config/          # 配置文件
├── .vitepress/          # VitePress配置
├── content/             # Markdown内容
│   └── daily/          # 按日期存储
├── scripts/             # 本地脚本
├── requirements.txt     # Python依赖
└── package.json         # Node依赖
```

## ⚙️ 配置

### 1. 配置新闻源

编辑 `src/config/sources.yaml`，根据需要启用/禁用各领域新闻源。

### 2. 设置OpenRouter API密钥

在GitHub仓库Settings → Secrets and variables → Actions中添加：
- `OPENROUTER_API_KEY`：你的OpenRouter API密钥

### 3. 配置VitePress

修改 `.vitepress/config.ts` 自定义网站标题、主题等。

## 🚀 部署

1. Fork或克隆此仓库
2. 启用GitHub Pages（Settings → Pages，选择GitHub Actions）
3. 推送代码会自动触发构建和部署
4. 访问：`https://<用户名>.github.io/ai-daily-news/`

## 📱 使用

### 自动运行
每天北京时间8点自动运行，生成最新日报。

### 手动采集
1. 访问GitHub仓库的Actions页面
2. 找到"Manual Collection"工作流
3. 点击"Run workflow"按钮
4. 等待3-5分钟，网站自动更新

## 📝 自定义

### 添加新闻源
在 `src/config/sources.yaml` 中添加新的RSS源：

```yaml
rss_feeds:
  - name: "新源"
    url: "https://example.com/feed"
    type: "tech"
    max_items: 5
```

### 调整AI提示词
修改 `src/ai_processor.py` 中的系统提示词。

### 更换主题
在 `.vitepress/theme/` 中自定义CSS和组件。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**Made with ❤️ by AI Daily News Team**