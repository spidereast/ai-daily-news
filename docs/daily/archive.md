---
layout: page

title: 归档
description: AI Daily News 历史归档
---

# 📚 历史归档

此页面列出所有历史日报。

<script>
// 动态加载历史文件列表
async function loadArchive() {
  const container = document.getElementById('archive-list');
  if (!container) return;
  
  try {
    // 从GitHub API获取内容目录
    const response = await fetch('https://api.github.com/repos/spidereast/ai-daily-news/contents/content/daily');
    if (response.ok) {
      const data = await response.json();
      let html = '';
      
      // 按年份排序
      const years = data
        .filter(item => item.type === 'dir' && item.name.match(/^\d{4}$/))
        .sort((a, b) => b.name.localeCompare(a.name));
      
      for (const yearDir of years) {
        html += `## ${yearDir.name}年\n\n`;
        
        // 获取该年份下的月份
        const yearResponse = await fetch(yearDir.url);
        if (yearResponse.ok) {
          const yearData = await yearResponse.json();
          const months = yearData
            .filter(item => item.type === 'dir' && item.name.match(/^\d{2}$/))
            .sort((a, b) => b.name.localeCompare(a.name));
          
          for (const monthDir of months) {
            html += `### ${monthDir.name}月\n\n`;
            
            // 获取该月份下的文件
            const monthResponse = await fetch(monthDir.url);
            if (monthResponse.ok) {
              const monthData = await monthResponse.json();
              const files = monthData
                .filter(item => item.name.endsWith('.md'))
                .sort((a, b) => b.name.localeCompare(a.name));
              
              for (const file of files) {
                const date = file.name.replace('.md', '');
                html += `- [${date}](/daily/${yearDir.name}/${monthDir.name}/${file.name})\n`;
              }
              html += '\n';
            }
          }
        }
      }
      
      container.innerHTML = html;
    } else {
      container.innerHTML = '<div class="warning">无法加载归档列表，请确保仓库已正确配置。</div>';
    }
  } catch (e) {
    console.error('加载归档失败:', e);
    container.innerHTML = '<div class="warning">加载归档时出错，请稍后重试。</div>';
  }
}

// 页面加载后执行
document.addEventListener('DOMContentLoaded', loadArchive);
</script>

<div id="archive-list">
  <div style="text-align: center; padding: 40px;">
    <div class="loading">正在加载历史归档...</div>
  </div>
</div>

<style>
.warning {
  padding: 15px;
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  border-radius: 4px;
  margin: 20px 0;
}

.loading {
  padding: 20px;
  text-align: center;
  color: #666;
}
</style>

---

**注**：归档页面会自动从GitHub仓库读取`content/daily/`目录结构。如果目录为空或不存在，页面会显示警告信息。