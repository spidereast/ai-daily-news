#!/usr/bin/env python3
"""
AI Daily News - 主程序
负责采集、AI处理、生成HTML站点
"""

import os
import sys
import json
import yaml
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# 项目根目录
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入自定义模块
try:
    from src.collectors.rss_collector import RSSCollector
    from src.ai_processor import AISummarizer
    from src.markdown_generator import MarkdownGenerator
    from src.utils import deduplicate_articles, filter_by_date, setup_logging
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  部分模块不可用: {e}")
    MODULES_AVAILABLE = False

class AIDailyNews:
    """AI Daily News 主类"""
    
    def __init__(self, config_path: str = None):
        self.project_root = project_root
        self.config = self.load_config(config_path)
        self.logger = setup_logging() if MODULES_AVAILABLE else None
        
    def load_config(self, config_path: str = None) -> Dict[str, Any]:
        """加载配置"""
        if config_path is None:
            config_path = self.project_root / "src" / "config" / "sources.yaml"
        else:
            config_path = Path(config_path)
            
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(f"✅ 加载配置: {config_path}")
            return config
        else:
            print(f"⚠️  配置文件不存在: {config_path}")
            return {"rss_feeds": [], "preferences": {}}
    
    def collect_articles(self, date_str: str = None) -> List[Dict[str, Any]]:
        """采集所有文章"""
        print("=" * 50)
        print("🚀 开始采集新闻")
        print("=" * 50)
        
        all_articles = []
        feeds = self.config.get('rss_feeds', [])
        preferences = self.config.get('preferences', {})
        max_items = preferences.get('max_total_items', 50)
        
        if MODULES_AVAILABLE:
            collector = RSSCollector(timeout=preferences.get('timeout_seconds', 15))
            
            for feed in feeds:
                try:
                    max_items_per_feed = feed.get('max_items', 5)
                    articles = collector.fetch(
                        feed['url'],
                        max_items=max_items_per_feed
                    )
                    
                    # 添加元数据
                    for article in articles:
                        article['source'] = feed['name']
                        article['type'] = feed.get('type', 'general')
                        article['category'] = self._get_category_name(feed.get('type', 'general'))
                    
                    all_articles.extend(articles)
                    print(f"  ✓ {feed['name']}: {len(articles)} 篇")
                    
                except Exception as e:
                    print(f"  ✗ {feed['name']}: 错误 - {str(e)}")
                    continue
        else:
            print("⚠️  使用模拟数据（模块不可用）")
            all_articles = self._generate_dummy_articles()
        
        # 去重
        if preferences.get('deduplicate', True):
            original_count = len(all_articles)
            all_articles = deduplicate_articles(all_articles)
            print(f"  🔄 去重: {original_count} → {len(all_articles)}")
        
        # 过滤日期
        if preferences.get('date_range_days'):
            all_articles = filter_by_date(all_articles, preferences['date_range_days'])
            print(f"  📅 日期过滤后: {len(all_articles)} 篇")
        
        # 限制总数
        if len(all_articles) > max_items:
            all_articles = all_articles[:max_items]
            print(f"  📊 限制总数: 最多 {max_items} 篇")
        
        print(f"\n✅ 采集完成: 共 {len(all_articles)} 篇文章")
        return all_articles
    
    def _get_category_name(self, type_code: str) -> str:
        """获取分类名称"""
        categories = self.config.get('categories', {})
        return categories.get(type_code, type_code)
    
    def _generate_dummy_articles(self) -> List[Dict[str, Any]]:
        """生成模拟文章（用于测试）"""
        now = datetime.now()
        return [
            {
                'title': 'AI Daily News 测试文章',
                'link': 'https://github.com/spidereast/ai-daily-news',
                'summary': '这是测试文章，实际部署后将显示真实采集的新闻内容。',
                'content': '这是测试文章内容。',
                'author': 'AI Daily News',
                'published': now.isoformat(),
                'source': '测试源',
                'type': 'test',
                'category': '测试'
            }
        ]
    
    def ai_process(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """AI处理（生成摘要）"""
        print("\n" + "=" * 50)
        print("🤖 AI处理 - 生成摘要")
        print("=" * 50)
        
        ai_config = self.config.get('preferences', {}).get('ai_summary', {})
        
        if not ai_config.get('enabled', False):
            print("⚠️  AI摘要未启用")
            for article in articles:
                article['ai_summary'] = article.get('summary', '')[:150]
            return articles
        
        # 检查API密钥
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            print("⚠️  未设置OPENROUTER_API_KEY，使用简单摘要")
            for article in articles:
                article['ai_summary'] = article.get('summary', '')[:150]
            return articles
        
        if MODULES_AVAILABLE:
            max_articles = ai_config.get('max_articles', 20)
            summarizer = AISummarizer(
                api_key=api_key,
                model=ai_config.get('model', 'openrouter/stepfun/step-3.5-flash'),
                prompt=ai_config.get('prompt', '')
            )
            
            processed = []
            for i, article in enumerate(articles[:max_articles]):
                try:
                    print(f"  处理 {i+1}/{min(max_articles, len(articles))}: {article['title'][:40]}...")
                    summary = summarizer.summarize(article)
                    article['ai_summary'] = summary
                    processed.append(article)
                except Exception as e:
                    print(f"    ✗ 失败: {str(e)}")
                    article['ai_summary'] = article.get('summary', '')[:150]
                    processed.append(article)
            
            # 剩余文章使用简单摘要
            for article in articles[max_articles:]:
                article['ai_summary'] = article.get('summary', '')[:150]
                processed.append(article)
            
            print(f"✅ AI摘要完成")
            return processed
        else:
            print("⚠️  AI模块不可用，使用简单摘要")
            for article in articles:
                article['ai_summary'] = article.get('summary', '')[:150]
            return articles
    
    def generate_site(self, articles: List[Dict[str, Any]], date_str: str) -> str:
        """生成网站"""
        print("\n" + "=" * 50)
        print("🎨 生成网站")
        print("=" * 50)
        
        # 准备数据
        now = datetime.now()
        formatted_date = now.strftime('%Y年%m月%d日')
        weekday = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][now.weekday()]
        
        site_data = {
            'date': date_str,
            'formatted_date': formatted_date,
            'weekday': weekday,
            'articles': articles,
            'generated_at': now.strftime('%Y-%m-%d %H:%M:%S'),
            'total_articles': len(articles)
        }
        
        # 生成Markdown (VitePress格式)
        if MODULES_AVAILABLE:
            try:
                generator = MarkdownGenerator()
                markdown_content = generator.generate_daily(site_data)
            except Exception as e:
                print(f"⚠️  MarkdownGenerator失败: {e}, 使用内置生成器")
                markdown_content = self._generate_vitepress_markdown(site_data)
        else:
            markdown_content = self._generate_vitepress_markdown(site_data)
        
        # 写入Markdown文件
        output_dir = self.project_root / "content" / "daily" / now.strftime('%Y')
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{date_str}.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Markdown生成: {output_path}")
        
        # 更新首页内容
        self._update_index_page(date_str, formatted_date, weekday)
        
        return str(output_path)
    
    def _generate_vitepress_markdown(self, data: Dict[str, Any]) -> str:
        """生成VitePress兼容的Markdown"""
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
    
    def _update_index_page(self, date_str: str, formatted_date: str, weekday: str):
        """更新首页，添加最新文章链接"""
        try:
            index_md = self.project_root / "docs" / "index.md"
            if index_md.exists():
                content = index_md.read_text(encoding='utf-8')
                # 在<!-- Latest Daily -->注释后插入新链接
                new_entry = f"- [{formatted_date} {weekday}](/daily/{datetime.now().year}/{date_str}.md) <!-- Latest Daily -->\n"
                if '<!-- Latest Daily -->' in content:
                    # 替换占位符
                    updated = content.replace('<!-- Latest Daily -->', new_entry)
                else:
                    # 添加到features列表后面
                    updated = content.replace('## 📊 采集状态', f"{new_entry}\n## 📊 采集状态")
                
                index_md.write_text(updated, encoding='utf-8')
                print(f"✅ 更新首页: {index_md}")
        except Exception as e:
            print(f"⚠️  更新首页失败: {e}")
    
    def run(self, date_str: str = None):
        """运行完整流程"""
        print("🤖 AI Daily News 开始运行")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 1. 采集
            articles = self.collect_articles(date_str)
            
            if not articles:
                print("⚠️  没有采集到文章，使用模拟数据")
                articles = self._generate_dummy_articles()
            
            # 2. AI处理
            articles = self.ai_process(articles)
            
            # 3. 生成网站
            output_path = self.generate_site(articles, date_str or datetime.now().strftime('%Y-%m-%d'))
            
            print("\n" + "=" * 50)
            print("🎉 全部完成！")
            print(f"📁 输出: {output_path}")
            print(f"📊 文章数: {len(articles)}")
            print("=" * 50)
            
            return 0
            
        except Exception as e:
            print(f"\n❌ 运行失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return 1

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='AI Daily News Generator')
    parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)，默认为今天')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--test', action='store_true', help='测试模式（使用模拟数据）')
    
    args = parser.parse_args()
    
    # 设置日期
    date_str = args.date or datetime.now().strftime('%Y-%m-%d')
    
    # 创建运行器
    app = AIDailyNews(config_path=args.config)
    
    # 测试模式
    if args.test:
        print("🧪 测试模式")
        articles = app._generate_dummy_articles()
        app.generate_site(articles, date_str)
        return 0
    
    # 正常运行
    return app.run(date_str)

if __name__ == "__main__":
    sys.exit(main())