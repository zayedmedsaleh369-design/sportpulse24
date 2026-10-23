import os
import feedparser
import google.generativeai as genai
import requests

# إعدادات المدونة والمعرّفات
BLOG_ID = "1096868669091416564"
RSS_URL = "https://www.kooora.com/default.aspx?r=rss" # مصدر الأخبار الرياضية

# جلب المفاتيح من بيئة العمل الآمنة في GitHub
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOGGER_ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")

# تكوين نموذج الذكاء الاصطناعي (Gemini)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def fetch_latest_news():
    """جلب أحدث خبر من ملف الـ RSS"""
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("لا توجد أخبار جديدة في الـ RSS.")
        return None, None
    latest = feed.entries[0]
    return latest.title, latest.summary

def generate_article(title, summary):
    """توليد مقال رياضي احترافي باستخدام Gemini"""
    prompt = f"""
    اكتب مقالاً رياضياً احترافياً، مشوقاً، ومنسقاً بعناية باللغة العربية بناءً على العنوان والملخص التاليين:
    العنوان: {title}
    الملخص: {summary}
    """
    response = model.generate_content(prompt)
    return response.text

def post_to_blogger(title, content):
    """نشر المقال مباشرة على Blogger عبر API"""
    api_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts"
    headers = {
        "Authorization": f"Bearer {BLOGGER_ACCESS_   
