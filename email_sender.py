import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict

def generate_html(news_summaries: List[Dict]) -> str:
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
            <strong>{news['title_ar']}</strong><br>
            <p>{news['summary']}</p>
            <a href="{news['link']}">المصدر</a>
        </li>"""
    
    html += "</ul></body></html>"
    return html

def send_email(html_content: str, to_email: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"نشرة المراقبة التقنية - {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ["EMAIL_FROM"], os.environ["EMAIL_PASSWORD"])
        server.sendmail(msg["From"], [msg["To"]], msg.as_string())