import os
import requests
import feedparser
import google.generativeai as genai

# 1. إعداد مفتاح Google Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# استخدام النموذج المتوافق لتجنب أخطاء 404
model = genai.GenerativeModel('gemini-1.5-pro')

# 2. إعداد أسرار Blogger
BLOG_ID = os.environ.get("BLOG_ID")
BLOGGER_ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")

# 3. مصادر RSS للأخبار العاجلة
RSS_FEEDS = [
    "http://feeds.bbci.co.uk/sport/rss.xml",
    "https://www.skysports.com/rss/12040"
]

def fetch_latest_news():
    """جلب أحدث خبر رياضي من الخلاصات"""
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            latest = feed.entries[0]
            return latest.title, latest.summary, latest.link
    return None, None, None

def generate_article(title, summary):
    """صياغة مقال صحفي احترافي بالذكاء الاصطناعي"""
    prompt = f"""
    بصفتك صحفياً رياضياً محترفاً في موقع SportPulse24، قم بصياغة مقال إخباري جذاب باللغة العربية بناءً على الخبر التالي:
    العنوان الأصلي: {title}
    الملخص الأصلي: {summary}

    المطلوب:
    1. عنوان عاجل ومحفز للضغط (Clickable & Engaging).
    2. مقدمة مشوقة.
    3
