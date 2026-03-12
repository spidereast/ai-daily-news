---
layout: page

title: 今日
---

# 📰 今日AI Daily News

<script>
// 自动跳转到最新一期
async function redirectToLatest() {
  try {
    // 从GitHub API获取最新内容
    const response = await fetch('https://api.github.com/repos/spidereast/ai-daily-news/contents/content/daily?ref=main');
    if (response.ok) {
      const data = await response.json();
      
      // 查找最新年份和月份
      const years = data
        .filter(item => item.type === 'dir' && item.name.match(/^\d{4}$/))
        .sort((a, b) => b.name.localeCompare(a.name));
      
      if (years.length > 0) {
        const latestYear = years[0].name;
        const yearResponse = await fetch(years[0].url);
        if (yearResponse.ok) {
          const yearData = await yearResponse.json();
          const months = yearData
            .filter(item => item.type === 'dir' && item.name.match(/^\d{2}$/))
            .sort((a, b) => b.name.localeCompare(a.name));
          
          if (months.length > 0) {
            const latestMonth = months[0].name;
            const monthResponse = await fetch(months[0].url);
            if (monthResponse.ok) {
              const monthData = await monthResponse.json();
              const files = monthData
                .filter(item => item.name.endsWith('.md'))
                .sort((a, b) => b.name.localeCompare(a.name));
              
              if (files.length > 0) {
                const latestFile = files[0].name;
                window.location.href = `/daily/${latestYear}/${latestMonth}/${latestFile}`;
                return;
              }
            }
          }
        }
      }
    }
  } catch (e) {
    console.error('获取最新内容失败:', e);
  }
  
  // 如果失败，显示提示
  document.getElementById('content').innerHTML = `
    <div class="empty-state">
      <h2>📭 暂无内容</h2>
      <p>今日日报尚未生成，可能原因：</p>
      <ul>
        <li>系统仍在生成中（约需5-10分钟）</li>
        <li>今日是首次运行，正在初始化</li>
        <li>定时任务将在明天8点自动运行</li>
      </ul>
      <p>👉 <a href="/manual">手动采集</a> 立即获取最新资讯</p>
    </div>
  `;
}

// 页面加载后执行跳转
document.addEventListener('DOMContentLoaded', redirectToLatest);
</script>

<div id="content">
  <div style="text-align: center; padding: 40px;">
    <div class="loading">⏳ 正在加载最新内容...</div>
  </div>
</div>

<style>
.empty-state {
  padding: 40px;
  text-align: center;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 20px 0;
}

.empty-state ul {
  list-style: none;
  padding: 0;
  margin: 15px 0;
}

.empty-state li {
  padding: 5px 0;
  color: #666;
}

.loading {
  padding: 20px;
  text-align: center;
  color: #666;
}
</style>