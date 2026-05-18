import os
import json
from groq import Groq
from typing import List, Dict

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def summarize_news(news_list: List[Dict]) -> List[Dict]:
    if not news_list:
        return []
    
    news_text = "\n".join([f"- {n['title']}" for n in news_list[:10]])
    
    prompt = f"""Summarize each news in ONE short sentence in Arabic.
Format: [{{"title_ar": "...", "summary": "...", "link": "..."}}]

News:
{news_text}"""
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
        )
        
        content = response.choices[0].message.content
        # تنظيف النص
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        result = json.loads(content)
        if isinstance(result, dict):
            result = [result]
        return result[:10]
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return [{
            "title_ar": news['title'][:80],
            "summary": "ملخص غير متوفر حالياً",
            "link": news['link']
        } for news in news_list[:10]]
