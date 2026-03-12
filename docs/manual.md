---
layout: page

title: 手动采集
description: 手动触发AI Daily News采集和生成
---

# 🖱️ 手动采集

如果你想立即获取最新资讯，而不是等到明天8点，可以手动触发采集。

## 📋 操作步骤

### 第一步：打开GitHub Actions页面

<a href="https://github.com/spidereast/ai-daily-news/actions/workflows/daily.yml" target="_blank" style="display: inline-block; padding: 12px 24px; background: #24292e; color: white; text-decoration: none; border-radius: 6px; font-weight: bold;">
  🚀 打开Actions页面
</a>

### 第二步：点击Run workflow

1. 在上方打开的GitHub Actions页面中，找到左侧的 **"AI Daily News - 自动生成"** 工作流
2. 点击 **"Run workflow"** 按钮（绿色按钮）
3. 在下拉菜单中选择 `main` 分支
4. 点击 **"Run workflow"** 确认

### 第三步：等待完成

工作流运行步骤：
1. ✅ 检出代码 (1-2分钟)
2. ✅ 安装依赖 (2-3分钟)
3. ✅ 采集新闻 (1-2分钟)
4. ✅ AI摘要处理 (2-3分钟，取决于文章数量)
5. ✅ 生成并部署 (1-2分钟)

**总耗时：约 5-10 分钟**

### 第四步：查看结果

完成后：
- 🌐 网站自动更新：https://spidereast.github.io/ai-daily-news/
- 📄 查看最新日报：点击导航栏的"今日"
- 📊 查看历史：点击"归档"

---

## 📊 实时监控

你可以在此页面查看最新运行状态：

<script>
async function checkWorkflowStatus() {
  const statusDiv = document.getElementById('workflow-status');
  if (!statusDiv) return;
  
  try {
    const response = await fetch('https://api.github.com/repos/spidereast/ai-daily-news/actions/runs?per_page=1&event=workflow_dispatch');
    if (response.ok) {
      const data = await response.json();
      if (data.workflow_runs && data.workflow_runs.length > 0) {
        const run = data.workflow_runs[0];
        const now = new Date();
        const updated = new Date(run.updated_at);
        const diffMins = Math.floor((now - updated) / 60000);
        
        let statusHtml = `
          <div style="padding: 15px; background: ${run.status === 'completed' ? (run.conclusion === 'success' ? '#d4edda' : '#f8d7da') : '#fff3cd'}; border-radius: 8px; margin: 20px 0; border-left: 4px solid ${run.status === 'completed' ? (run.conclusion === 'success' ? '#28a745' : '#dc3545') : '#ffc107'};">
            <h4 style="margin: 0 0 10px 0;">
              最新运行: ${run.status === 'completed' ? (run.conclusion === 'success' ? '✅ 成功' : '❌ 失败') : '⏳ 运行中...'}
            </h4>
            <p style="margin: 0; font-size: 0.9em; color: #666;">
              更新时间: ${updated.toLocaleString('zh-CN')} (${diffMins}分钟前)<br>
              运行ID: ${run.id}<br>
              触发者: ${run.triggering_actor?.login || '未知'}
            </p>
          </div>
        `;
        
        statusDiv.innerHTML = statusHtml;
        
        // 如果运行完成，5秒后自动刷新
        if (run.status === 'completed') {
          setTimeout(() => {
            window.location.reload();
          }, 5000);
        }
      } else {
        statusDiv.innerHTML = '<div style="padding: 10px; background: #e9ecef; border-radius: 4px; margin: 20px 0;">最近没有找到手动触发的运行记录</div>';
      }
    }
  } catch (e) {
    console.error('状态检查失败:', e);
  }
}

// 页面加载后检查，然后每15秒检查一次
document.addEventListener('DOMContentLoaded', () => {
  checkWorkflowStatus();
  setInterval(checkWorkflowStatus, 15000);
});
</script>

<div id="workflow-status">
  <div style="padding: 10px; background: #e9ecef; border-radius: 4px; margin: 20px 0;">
    <em>正在检查运行状态...</em>
  </div>
</div---

## 🔧 故障排除

### 工作流未启动
- ✅ 确保已 Fork 或克隆此仓库
- ✅ 确保GitHub Actions已启用
- ✅ 确认你点击的是"Run workflow"按钮

### 运行失败
常见原因：
1. **OpenRouter API密钥未设置**
   - 在仓库Settings → Secrets and variables → Actions中添加 `OPENROUTER_API_KEY`
   - 获取地址：https://openrouter.ai/keys
   
2. **RSS源无法访问**
   - 某些RSS源可能在特定地区不可访问
   - 编辑 `src/config/sources.yaml` 禁用有问题的源

3. **依赖安装失败**
   - 检查 `requirements.txt` 是否正确

### 查看详细日志
1. 在GitHub Actions页面点击失败的运行
2. 查看每个步骤的日志输出
3. 根据错误信息调整配置

---

## ⚙️ 配置说明

### 设置OpenRouter API密钥（必需）

AI摘要功能需要OpenRouter API密钥：

1. 访问 https://openrouter.ai/
2. 注册/登录账号
3. 进入API Keys页面
4. 创建新密钥
5. 在GitHub仓库中添加Secrets：
   - Settings → Secrets and variables → Actions → New repository secret
   - Name: `OPENROUTER_API_KEY`
   - Value: 你的API密钥

### 调整新闻源

编辑 `src/config/sources.yaml`：

```yaml
rss_feeds:
  - name: "Hacker News"
    url: "https://hnrss.org/frontpage"
    type: "tech"
    max_items: 5  # 每个源最多文章数
    # 禁用某个源：注释掉或删除
```

支持的领域：`ai`, `programming`, `tech`, `startup`, `economy`, `digital`, `hightech`, `ev`, `imaging`

### 修改AI提示词

编辑 `src/ai_processor.py` 中的 `default_prompt`：

```python
self.default_prompt = """你是一个专业的编辑。请为以下新闻生成摘要..."""
```

---

## 🆘 需要帮助？

- 📖 [项目README](/)
- 🐛 [提交Issue](https://github.com/spidereast/ai-daily-news/issues)
- 💬 [讨论区](https://github.com/spidereast/ai-daily-news/discussions)

---

<center>
<small>手动采集页面 | 点击上方按钮开始</small>
</center>