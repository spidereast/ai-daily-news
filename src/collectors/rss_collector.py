#!/usr/bin/env python3
"""
RSS采集器 - 通用的RSS抓取模块
"""

import feedparser
import requests
from typing import List, Dict, Optional
from datetime import datetime
import time
import re
import html

class RSSCollector:
    """RSS源采集器"""
    
    def __init__(self, timeout: int = 15, max_retries: int = 2):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; AI-Daily-News/1.0; +https://github.com/spidereast/ai-daily-news)',
            'Accept': 'application/rss+xml, application/xml, text/xml; q=0.9, */*; q=0.8'
        })
    
    def fetch(self, url: str, max_items: int = 10) -> List[Dict[str, str]]:
        """从RSS源获取文章"""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                
                # 解析RSS
                feed = feedparser.parse(response.content)
                
                if feed.bozo:
                    raise Exception(f"RSS解析错误: {feed.get('bozo_exception', 'Unknown error')}")
                
                articles = []
                for entry in feed.entries[:max_items]:
                    article = self._parse_entry(entry)
                    if article:
                        articles.append(article)
                
                return articles
                
            except requests.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                    continue
                raise Exception(f"请求失败: {str(e)}")
            except Exception as e:
                raise Exception(f"采集失败: {str(e)}")
        
        return []
    
    def _parse_entry(self, entry) -> Optional[Dict[str, str]]:
        """解析RSS条目"""
        try:
            # 标题
            title = entry.get('title', '无标题').strip()
            if not title:
                return None
            
            # 链接
            link = entry.get('link', '')
            if not link and hasattr(entry, 'links') and entry.links:
                link = entry.links[0].get('href', '')
            
            # 摘要/描述
            summary = entry.get('summary', entry.get('description', ''))
            summary = self._clean_html(summary)
            
            # 内容（如果有）
            content = entry.get('content', [{}])[0].get('value', '') if hasattr(entry, 'content') else ''
            if content:
                content = self._clean_html(content)
            
            # 发布时间
            published = self._parse_date(entry)
            
            # 作者
            author = ''
            if hasattr(entry, 'author'):
                author = entry.author
            elif hasattr(entry, 'authors') and entry.authors:
                author = entry.authors[0].get('name', '')
            
            # 标签/分类
            tags = []
            if hasattr(entry, 'tags'):
                tags = [t.get('term', '') for t in entry.tags if t.get('term')]
            
            return {
                'title': title[:200],  # 限制长度
                'link': link,
                'summary': summary[:500],
                'content': content[:1000] if content else summary[:500],
                'author': author[:100],
                'published': published,
                'tags': tags,
                'collected_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"解析条目失败: {str(e)}")
            return None
    
    def _parse_date(self, entry) -> str:
        """解析日期"""
        date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']
        
        for field in date_fields:
            if hasattr(entry, field) and getattr(entry, field):
                try:
                    dt = datetime(*getattr(entry, field)[:6])
                    return dt.isoformat()
                except:
                    continue
        
        return datetime.now().isoformat()
    
    def _clean_html(self, html_text: str) -> str:
        """清理HTML标签"""
        if not html_text:
            return ''
        
        # 移除HTML标签
        clean = re.sub(r'<[^>]+>', '', html_text)
        # 解码HTML实体
        clean = html.unescape(clean)
        # 替换多个空格为单个空格
        clean = re.sub(r'\s+', ' ', clean).strip()
        
        return clean
    
    def test_feed(self, url: str) -> Dict[str, Any]:
        """测试RSS源是否可用"""
        try:
            feed = feedparser.parse(url)
            
            if feed.bozo:
                return {
                    'status': 'error',
                    'message': str(feed.bozo_exception),
                    'entries': 0
                }
            
            entries = len(feed.entries)
            sample_title = feed.entries[0].title if entries > 0 else '无文章'
            
            return {
                'status': 'success',
                'message': f'成功，发现 {entries} 篇文章',
                'entries': entries,
                'sample_title': sample_title[:100]
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'entries': 0
            }

# 简化的函数接口
def collect_rss_feed(url: str, max_items: int = 5) -> List[Dict[str, str]]:
    """快速采集函数"""
    collector = RSSCollector()
    return collector.fetch(url, max_items=max_items)