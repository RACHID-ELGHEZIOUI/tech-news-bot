import os
from dotenv import load_dotenv
from scraper import get_news
from summarizer import summarize_news
from email_sender import generate_html, send_email

load_dotenv()

def main():
    print("🚀 بدء تشغيل وكيل المراقبة...")
    
    news = get_news()
    print(f"📡 {len(news)} خبر تم جلبها")
    
    summaries = summarize_news(news)
    print(f"🤖 {len(summaries)} خبر تم تلخيصها")
    
    html = generate_html(summaries)
    send_email(html, os.environ["EMAIL_TO"])
    print("✅ تم الإرسال")

if __name__ == "__main__":
    main()