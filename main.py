import os
import requests
import feedparser
import google.generativeai as genai

# 1. إعداد المفاتيح
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOGGER_ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")
BLOG_ID = os.environ.get("BLOG_ID")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 2. مصادر الأخبار العاجلة العالمية (BBC & Sky Sports)
RSS_URLS = [
    "http://feeds.bbci.co.uk/sport/football/rss.xml",
    "https://www.skysports.com/rss/12040"
]

def get_latest_breaking_news():
    print("🔍 جاري جلب أحدث الأخبار العاجلة عالمياً...")
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        if feed.entries:
            latest = feed.entries[0]
            title = latest.title
            summary = latest.get("summary", "")
            return title, summary
    return None, None

def generate_and_post():
    news_title, news_summary = get_latest_breaking_news()
    
    if not news_title:
        print("لا توجد أخبار جديدة حالياً.")
        return

    # المطالبة المتقدمة للذكاء الاصطناعي مع تهيئة الإعلانات والوسوم
    prompt = f"""
    أنت رئيس التحرير في المنصة الرياضية العالمية 'SportPulse24'.
    اكتب مقالاً صحفياً عاجلاً ومثيراً باللغة العربية استناداً للخبر التالي:
    العنوان الأصلي: {news_title}
    التفاصيل: {news_summary}

    الشروط والمتطلبات:
    1. السطر الأول يجب أن يحتوي على العنوان فقط متضمناً كلمة [عاجل] ومحفزاً للقرّاء بدون علامات HTML.
    2. اترك سطر فارغ، ثم ابدأ جسم المقال بتنسيق HTML جذاب (استخدم <h2>, <p>, <strong>).
    3. أضف في نهاية المقال فقرة تحتوي على 5 هاشتجات عربية رياضية متوافقة مع محركات البحث وتويتر وفيسبوك.
    """

    print(f"🤖 جاري صياغة وتحليل الخبر العاجل: {news_title}")
    response = model.generate_content(prompt)
    content = response.text.strip()

    lines = content.split("\n", 1)
    title = lines[0].replace("#", "").strip()
    body = lines[1].strip() if len(lines) > 1 else content

    # 3. النشر على Blogger
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        "Authorization": f"Bearer {BLOGGER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "kind": "blogger#post",
        "title": title,
        "content": body
    }

    res = requests.post(url, headers=headers, json=payload)
    if res.status_code in [200, 201]:
        print("✅ تم نشر الخبر العاجل بنجاح على المدونة!")
    else:
        print(f"❌ خطأ أثناء النشر: {res.text}")

if __name__ == "__main__":
    generate_and_post()
