#!/usr/bin/env python3
"""
AI摘要处理器 - 使用OpenRouter API (Step模型)
"""

import os
import openai
from typing import Dict, Any, Optional

class AISummarizer:
    """AI摘要生成器"""
    
    def __init__(self, 
                 api_key: str = None,
                 model: str = "openrouter/stepfun/step-3.5-flash",
                 prompt_template: str = None):
        """
        初始化AI摘要器
        
        Args:
            api_key: OpenRouter API密钥，默认从环境变量读取
            model: 使用的模型
            prompt_template: 自定义提示词模板
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("未设置OPENROUTER_API_KEY环境变量")
        
        self.model = model
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        # 默认提示词
        self.default_prompt = """你是一个专业的科技资讯编辑。请为以下新闻生成简明的中文摘要，突出核心信息，控制在150字以内。

标题：{title}
来源：{source}
内容：{content}

摘要："""
        
        self.prompt_template = prompt_template or self.default_prompt
    
    def summarize(self, article: Dict[str, Any]) -> str:
        """
        为文章生成摘要
        
        Args:
            article: 文章字典，包含title, content, source等字段
            
        Returns:
            生成的摘要文本
        """
        try:
            # 准备输入
            title = article.get('title', '无标题')
            content = article.get('content', article.get('summary', ''))
            source = article.get('source', '未知来源')
            
            # 截断过长的内容
            if len(content) > 2000:
                content = content[:2000] + "..."
            
            # 构建提示词
            prompt = self.prompt_template.format(
                title=title,
                content=content,
                source=source
            )
            
            # 调用API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的科技资讯编辑，擅长生成简明扼要的新闻摘要。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7,
                extra_headers={
                    "HTTP-Referer": "https://github.com/spidereast/ai-daily-news",
                    "X-Title": "AI Daily News"
                }
            )
            
            summary = response.choices[0].message.content.strip()
            
            # 清理摘要
            if summary.startswith('摘要：'):
                summary = summary[3:].strip()
            
            return summary
            
        except Exception as e:
            print(f"AI摘要生成失败: {str(e)}")
            # 降级到简单摘要
            simple = article.get('summary', '')[:150]
            return simple if simple else "暂无摘要"
    
    def batch_summarize(self, articles: List[Dict[str, Any]], max_articles: int = 20) -> List[Dict[str, Any]]:
        """
        批量生成摘要
        
        Args:
            articles: 文章列表
            max_articles: 最多处理的文章数
            
        Returns:
            添加了ai_summary字段的文章列表
        """
        processed = []
        for i, article in enumerate(articles[:max_articles]):
            print(f"  AI处理 {i+1}/{min(max_articles, len(articles))}: {article['title'][:50]}...")
            summary = self.summarize(article)
            article['ai_summary'] = summary
            processed.append(article)
        
        # 剩余文章不处理
        for article in articles[max_articles:]:
            article['ai_summary'] = article.get('summary', '')[:150]
            processed.append(article)
        
        return processed

# 便捷函数
def create_summarizer() -> Optional[AISummarizer]:
    """创建摘要器实例"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("⚠️  未设置OPENROUTER_API_KEY，跳过AI摘要")
        return None
    
    try:
        return AISummarizer(api_key=api_key)
    except Exception as e:
        print(f"❌ 创建AI摘要器失败: {e}")
        return None