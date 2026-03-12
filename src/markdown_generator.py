#!/usr/bin/env python3
"""
Markdown生成器 - VitePress格式
"""

from datetime import datetime
from typing import Dict, Any, List

class MarkdownGenerator:
    """Markdown生成器"""
    
    def generate_daily(self, data: Dict[str, Any]) -> str:
        """生成日报Markdown"""
        articles = data.get('articles', [])
        formatted_date = data.get('formatted_date', datetime.now().strftime('%Y年%m月%d日'))
        weekday = data.get('weekday', '')
        total_articles = data.get('total_articles', len(articles))
        generated_at = data.get('generated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Frontmatter
        frontmatter = f"""---
title: {formatted_date} 日报
date: {data.get('date', datetime.now().strftime('%Y-%m-%d'))}
description: AI Daily News 自动生成
---
"""
        
        # 内容
        content = f"# 📰 AI Daily News - {formatted_date} {weekday}\n\n"
        
        # 统计信息
        content += f"> ✨ 共收录 {total_articles} 篇文章 | 生成时间: {generated_at}\n\n"
        
        # 按分类分组
        categories = {}
        for article in articles:
            cat = article.get('category', '其他')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(article)
        
        # 生成各分类内容
        for category, category_articles in categories.items():
            content += f"## 📂 {category}\n\n"
            
            for article in category_articles:
                content += self._format_article_markdown(article)
                content += "\n---\n\n"
        
        # 页脚
        content += "---\n\n"
        content += f"🤖 *本日报由 AI Daily News 自动生成* | "
        content += f"*下次更新: 明天 8:00 (北京时间)*"
        
        return frontmatter + content
    
    def _format_article_markdown(self, article: Dict[str, Any]) -> str:
        """格式化单篇文章为Markdown"""
        title = article.get('title', '无标题')
        link = article.get('link', '#')
        source = article.get('source', '未知')
        summary = article.get('summary', '暂无摘要')
        ai_summary = article.get('ai_summary', '')
        author = article.get('author', '')
        published = article.get('published', '')[:10] if article.get('published') else ''
        tags = article.get('tags', [])
        
        md = f"### {title}\n\n"
        md += f"**来源**: {source} | "
        if author:
            md += f"**作者**: {author} | "
        if published:
            md += f"**时间**: {published} | "
        md += "\n\n"
        
        if summary and summary != title:
            md += f"**原文摘要**: {summary}\n\n"
        
        if ai_summary:
            md += f"> **🤖 AI 摘要**：{ai_summary}\n\n"
        
        md += f"[阅读原文]({link})"
        
        if tags:
            md += "\n\n**标签**: " + ", ".join([f"`{t}`" for t in tags[:5]])
        
        return md

def main():
    """测试"""
    generator = MarkdownGenerator()
    
    sample_data = {
        'date': '2025-03-12',
        'formatted_date': '2025年03月12日',
        'weekday': '星期三',
        'total_articles': 2,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'articles': [
            {
                'title': '测试文章1',
                'link': 'https://example.com/1',
                'source': 'Test Source',
                'category': 'AI',
                'summary': '这是测试摘要1',
                'ai_summary': 'AI生成的摘要1',
                'author': 'Test Author',
                'published': '2025-03-12T10:00:00',
                'tags': ['test', 'ai']
            }
        ]
    }
    
    md = generator.generate_daily(sample_data)
    print(md)

if __name__ == "__main__":
    main()