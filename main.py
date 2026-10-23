import os
import requests
import google.generativeai as genai

# 1. إعداد مفاتيح الوصول والبيئة
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOGGER_ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")
BLOG_ID = os.environ.get("BLOG_ID")  # يمكنك وضع ID مدونتك هنا أو وضعه كمفتاح في Secrets

# 2. تهيئة نموذج Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 3. صياغة وإنشاء المقال الرياضي
prompt = """
أنت محرر رياضي محترف لموقع 'SportPulse24'.
قم بكتابة مقال إخباري رياضي حصري ومثير باللغة العربية حول أحدث التطورات في كرة القدم العالمية.
المقال يجب أن يحتوي على:
- عنوان جذاب ومحفز للقرّاء.
- مقدمة مشوقة.
- تفاصيل الخبر بأسلوب صحفي ممتع.
- خاتمة قصيرة.

اجعل المخرجات بتنسيق HTML جاهز للنشر (استخدم الأوسمة <h2>, <p>, <strong>).
ضع العنوان في السطر الأول تماماً بدون أي علامات HTML، ثم اترك سطر فارغ وابدأ بدنه بتنسيق HTML.
"""

def generate_and_post():
    print("جاري إنشاء المقال باستخدام Gemini AI...")
    response = model.generate_content(prompt)
    content = response.text.strip()
    
    # فصل العنوان عن نص المقال
    lines = content.split("\n", 1)
    title = lines[0].replace("#", "").strip()
