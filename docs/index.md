---
layout: home

hero:
  name: AI Daily News
  text: 智能资讯 每日更新
  tagline: AI/编程/科技/创业/经济/数码/新能源汽车/数码影像
  actions:
    - theme: brand
      text: 查看今日内容
      link: /daily/current
    - theme: alt
      text: 手动采集
      link: /manual

features:
  - title: ⏰ 自动更新
    details: 每天北京时间8点自动运行，无需人工干预
  - title: 🖱️ 手动触发
    details: 随时点击按钮立即采集最新资讯
  - title: 🤖 AI摘要
    details: 使用Step 3.5 Flash生成智能摘要
  - title: 📊 多领域覆盖
    details: 涵盖9大领域，30+专业新闻源
  - title: 🎨 现代化界面
    details: VitePress构建，快速、美观
  - title: 🆓 完全免费
    details: GitHub Pages托管，无服务器成本
---

## 🚀 快速开始

### 自动运行
系统会每天北京时间8点自动运行，生成最新日报。

### 手动采集
如果希望立即获取最新资讯：

1. 点击上方的"手动采集"按钮
2. 在GitHub Actions页面点击"Run workflow"
3. 返回此页面查看进度
4. 3-5分钟后网站自动更新

## 📊 采集状态

<script>
// 简单的状态检查
async function checkStatus() {
  try {
    const response = await fetch('https://api.github.com/repos/spidereast/ai-daily-news/actions/runs?per_page=1');
    if (response.ok) {
      const data = await response.json();
      if (data.workflow_runs && data.workflow_runs.length > 0) {
        const run = data.workflow_runs[0];
        const status = run.status;
        const conclusion = run.conclusion;
        
        document.getElementById('status').innerHTML = `
          <div style="padding: 10px; background: #e3f2fd; border-radius: 4px; margin: 20px 0;">
            <strong>最新运行状态：</strong> ${status === 'completed' ? (conclusion === 'success' ? '✅ 成功' : '❌ 失败') : '⏳ 运行中'}
            <br>
            <small>更新时间：${new Date(run.updated_at).toLocaleString('zh-CN')}</small>
          </div>
        `;
      }
    }
  } catch (e) {
    console.log('状态检查失败', e);
  }
}

// 页面加载后检查状态
document.addEventListener('DOMContentLoaded', () => {
  checkStatus();
  // 每30秒检查一次
  setInterval(checkStatus, 30000);
});
</script>

<div id="status">
  <div style="padding: 10px; background: #fff3cd; border-radius: 4px; margin: 20px 0;">
    <strong>状态检查中...</strong>
  </div>
</div>

## 📝 使用说明

### 配置要求

1. **OpenRouter API密钥**（用于AI摘要）
   - 在GitHub仓库Settings → Secrets中设置 `OPENROUTER_API_KEY`
   - 获取地址：https://openrouter.ai/keys

2. **GitHub Actions权限**
   - 确保仓库已启用GitHub Actions
   - 工作流会自动提交更改并部署

### 自定义新闻源

编辑 `src/config/sources.yaml` 文件，可以：
- 添加/删除RSS源
- 调整每个源的最大文章数
- 修改领域分类
- 配置关键词过滤

### 问题反馈

如遇到问题，请提交Issue：https://github.com/spidereast/ai-daily-news/issues

---

<center>
<small>Made with ❤️ | Powered by Step AI & VitePress</small>
</center>