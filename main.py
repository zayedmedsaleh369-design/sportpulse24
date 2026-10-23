import os
import json
from google import genai
from google.genai import types
import requests

# جلب المفاتيح والأسرار من إعدادات GitHub Secrets
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID") or os.environ.get("BLOG_ID")
ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN") or os.environ.get("BLOG")

def fetch_and_publish_latest_news():
    try:
        # 1. إعداد عميل الذكاء الاصطناعي والبحث اللحظي
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = """
        ابحث في الإنترنت عن أحدث وأبرز الأخبار العاجلة والسياسية والاقتصادية والرياضية والتقنية اليوم.
        اختر أهم خبر عاجل وبارز الآن، واكتب عنه مقالاً صحفياً احترافياً شاملاً لموقع (SportPulse24).
        
        الشروط:
        1. عنوان جذاب واحترافي.
        2. محتوى تفصيلي وموضوعي مصاغ بالكامل بلغة HTML (استخدم <h2>, <p>, <ul>, <li>).
        3. أضف صورة معبرة تناسب الخبر باستخدام وسم HTML (مثل: <img src="https://picsum.photos/800/400" alt="صورة الخبر" style="width:100%; border-radius:8px;">).
        
        أريد النتيجة بصيغة JSON حصرياً وبدون أي نصوص إضافية، وتحتوي على:
        - "title": عنوان المقال
        - "content": محتوى المقال كامل بلغة HTML
        - "labels": تصنيف الخبر
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}],
                response_mime_type="application/json"
            ),
        )
        
        text_response = response.text.strip()
        
        # تنظيف أي رموز ماركداون إضافية
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
            
        article = json.loads(text_response.strip())
        
        # 2. النشر التلقائي في مدونة بلوجر
        url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "title": article.get("title", "خبر عاجل"),
            "content": article.get("content", ""),
            "labels": [article.get("labels", "أخبار عامة")]
        }
        
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            print("🎉 تم نشر الخبر العاجل تلقائياً في مدونة SportPulse24 بنجاح!")
        else:
            print(f"❌ خطأ أثناء النشر عبر بلوجر: {res.text}")
            
    except Exception as e:
        print(f"⚠️ حدث خطأ مؤقت أثناء التشغيل وسيتم تجاوزه في الجولة القادمة: {str(e)}")

if __name__ == "__main__":
    print("🤖 بدأ الروبوت الصحفي العمل تلقائياً لجلب ونشر آخر الأخبار...")
    fetch_and_publish_latest_news()
