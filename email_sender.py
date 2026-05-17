import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict

def generate_html(news_summaries: List[Dict]) -> str:
    """توليد HTML للبريد الإلكتروني"""
    html = f"""<!DOCTYPE html>
    <html dir="rtl">
    <head><meta charset="UTF-8"><title>نشرة المراقبة التقنية</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>🤖 نشرة المراقبة التقنية</h1>
        <p>{datetime.now().strftime('%Y-%m-%d')}</p>
        <ul>"""
    
    for news in news_summaries:
        html += f"""
            <li>
                <strong>{news.get('title_ar', news.get('title', 'عنوان الخبر'))}</strong><br>
                <p>{news.get('summary', 'ملخص غير متوفر')}</p>
                <a href="{news.get('link', '#')}">المصدر</a>
            </li>"""
    
    html += "</ul></body></html>"
    return html

def send_email(html_content: str, recipients_env: str):
    """
    إرسال البريد الإلكتروني بشكل منفصل إلى كل مستقبل.
    recipients_env: str - سلسلة تحتوي عناوين البريد مفصولة بفواصل.
    """
    # 1. تجهيز الإعدادات الأساسية
    email_from = os.environ["EMAIL_FROM"]
    email_password = os.environ["EMAIL_PASSWORD"]
    
    # 2. تقسيم العناوين إلى قائمة (cleaning up)
    #    نأخذ السلسلة ونقسمها على الفاصلة، ثم نزيل المسافات الزائدة
    recipients_list = [email.strip() for email in recipients_env.split(',') if email.strip()]
    
    if not recipients_list:
        print("⚠️ لم يتم العثور على عناوين بريد صالحة للإرسال.")
        return

    print(f"📧 جاري الإرسال إلى {len(recipients_list)} مستلم...")

    # 3. حلقة الإرسال: نرسل لكل عنوان بمفرده
    for index, email_to in enumerate(recipients_list):
        try:
            # إنشاء رسالة جديدة لكل مستلم
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"نشرة المراقبة التقنية - {datetime.now().strftime('%Y-%m-%d')}"
            msg["From"] = email_from
            msg["To"] = email_to  # حقل 'To' يحتوي على عنوان واحد فقط
            msg.attach(MIMEText(html_content, "html"))

            # الاتصال بالخادم وإرسال الرسالة
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(email_from, email_password)
                server.sendmail(email_from, [email_to], msg.as_string())
            
            print(f"   ✅ [{index+1}/{len(recipients_list)}] تم الإرسال إلى: {email_to}")
            
        except Exception as e:
            print(f"   ❌ فشل الإرسال إلى {email_to}: {e}")

    print("✅ انتهت عملية الإرسال.")
