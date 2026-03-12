#!/usr/bin/env python3
"""
工具函数模块
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

def deduplicate_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    文章去重
    
    去重策略：
    1. 按URL去重（如果有）
    2. 按标题哈希去重（如果URL相似或缺失）
    """
    seen_urls = set()
    seen_title_hashes = set()
    unique_articles = []
    
    for article in articles:
        url = article.get('link', '').strip()
        title = article.get('title', '').strip()
        
        # 尝试URL去重
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)
            continue
        
        # 如果URL重复或为空，使用标题哈希
        title_hash = hashlib.md5(title.encode('utf-8')).hexdigest()
        if title_hash not in seen_title_hashes:
            seen_title_hashes.add(title_hash)
            # 如果没有URL，生成一个基于标题的伪URL
            if not url:
                article['link'] = f"#article-{title_hash[:8]}"
            unique_articles.append(article)
    
    return unique_articles

def filter_by_date(articles: List[Dict[str, Any]], days: int = 2) -> List[Dict[str, Any]]:
    """
    按日期过滤文章
    
    Args:
        articles: 文章列表
        days: 只保留最近N天的文章
        
    Returns:
        过滤后的文章列表
    """
    if days <= 0:
        return articles
    
    cutoff_date = datetime.now() - timedelta(days=days)
    filtered = []
    
    for article in articles:
        try:
            pub_str = article.get('published', '')
            if not pub_str:
                # 没有日期信息的文章保留
                filtered.append(article)
                continue
            
            # 解析日期（多种格式）
            pub_date = None
            for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%a, %d %b %Y %H:%M:%S', '%Y-%m-%d']:
                try:
                    pub_date = datetime.strptime(pub_str[:19], fmt)
                    break
                except ValueError:
                    continue
            
            if pub_date and pub_date >= cutoff_date:
                filtered.append(article)
        except Exception:
            # 日期解析失败的文章保留
            filtered.append(article)
    
    return filtered

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """配置日志"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def ensure_dir(path):
    """确保目录存在"""
    from pathlib import Path
    Path(path).mkdir(parents=True, exist_ok=True)

def load_json(path: str, default: Any = None) -> Any:
    """加载JSON文件"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path: str, data: Any, indent: int = 2):
    """保存JSON文件"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

if __name__ == "__main__":
    # 测试
    print("测试工具函数...")
    
    test_articles = [
        {'title': 'A', 'link': 'http://example.com/1'},
        {'title': 'B', 'link': 'http://example.com/1'},  # 重复URL
        {'title': 'A', 'link': ''},  # 重复标题，无URL
        {'title': 'C', 'link': 'http://example.com/2'},
    ]
    
    unique = deduplicate_articles(test_articles)
    print(f"去重: {len(test_articles)} -> {len(unique)}")
    
    now = datetime.now()
    test_articles_with_dates = [
        {'title': 'Recent', 'published': now.isoformat()},
        {'title': 'Old', 'published': (now - timedelta(days=5)).isoformat()},
        {'title': 'NoDate', 'published': ''},
    ]
    
    filtered = filter_by_date(test_articles_with_dates, days=2)
    print(f"日期过滤: {len(test_articles_with_dates)} -> {len(filtered)}")