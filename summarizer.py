import os
import json
import re
from groq import Groq
from typing import List, Dict

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def summarize_news(news_list: List[Dict]) -> List[Dict]:
    if not news_list:
        return []
    
    news_text = "\n".join([f"- {n['title']}" for n in news_list[:10]])
    
    prompt = f"""Summarize the following tech news in Arabic. Each news item in ONE short sentence.
Output ONLY valid JSON array format. DO NOT add any text before or after.
Example: [{{"title_ar": "عنوان الخبر", "summary": "ملخص الخبر", "link": "الرابط"}}]

News:
{news_text}

Output JSON array:"""
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.2,
        )
        
        content = response.choices[0].message.content
        print(f"[DEBUG] Raw response: {content[:200]}...")
        
        # محاولة استخراج JSON بطرق مختلفة
        # الطريقة 1: البحث عن قوسين []
        json_match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                result = json.loads(json_str)
                if isinstance(result, list) and len(result) > 0:
                    return result[:10]
            except:
                pass
        
        # الطريقة 2: البحث عن أي شيء يشبه JSON
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = "[" + json_match.group(0) + "]"
            try:
                result = json.loads(json_str)
                if isinstance(result, list):
                    return result[:10]
            except:
                pass
        
        # Fallback: إذا فشل كل شيء، أرجع الأخبار الأصلية
        print("[DEBUG] Using fallback: returning original titles")
        return [{
            "title_ar": news['title'][:100],
            "summary": "ملخص غير متوفر لهذا الخبر",
            "link": news['link']
        } for news in news_list[:10]]
        
    except Exception as e:
        print(f"[ERROR] Groq API error: {e}")
        return [{
            "title_ar": news['title'][:100],
            "summary": "تعذر التلخيص بسبب خطأ في الخدمة",
            "link": news['link']
        } for news in news_list[:10]]