import os
import requests
import feedparser
from google import genai

# إعداد عميل Google Gemini بالمكتبة الجديدة
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# إعداد أسرار Blogger
BLOG_ID = os.environ.get("BLOG_ID")
BLOGGER_ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")

# مصادر RSS للأخبار العاجلة
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
            title = latest.title
            summary = latest.get("summary", "")
            link = latest.get("link", "")
            return title, summary, link
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
    3. تفاصيل الخبر في فقرتين بتنسيق أنيق.
    4. خاتمة سريعة ووسوم (Hashtags) مخصصة للشبكات الاجتماعية.
    """
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt
    )
    return response.text

def post_to_blogger(title, content):
    """نشر المقال على مدونة Blogger عبر REST API"""
    url = f"https://www.googleapis.com/blogspot/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        "Authorization": f"Bearer {BLOGGER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ تم نشر الخبر بنجاح على المدونة!")
    else:
        print(f"❌ فشل النشر: {response.status_code} - {response.text}")

def main():
    print("🔄 جاري جلب أحدث الأخبار العاجلة عالمياً...")
    title, summary, link = fetch_latest_news()
    
    if not title:
        print("⚠️ لم يتم العثور على أخبار جديدة.")
        return

    print(f"📌 جاري صياغة وتحليل الخبر العاجل: {title}")
    article_text = generate_article(title, summary)
    
    # تحويل النص إلى تنسيق HTML بسيط للظهور بشكل منظم على Blogger
    formatted_content = article_text.replace("\n", "<br>")
    
    print("🚀 جاري النشر التلقائي على SportPulse24...")
    post_to_blogger(title, formatted_content)

if __name__ == "__main__":
    main()
