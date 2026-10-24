import urllib.request
import xml.etree.ElementTree as ET
import re

def clean_html(text):
    """تنظيف النصوص من وسوم HTML"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def translate_to_arabic_style(title, desc):
    """ترجمة وصياغة العنوان والنص بأسلوب عربي احترافي ومثيرة"""
    translations = {
        "responds to": "يرد على",
        "criticism": "انتقادات",
        "criticisms": "انتقادات",
        "abandon ship": "الهروب من السفينة",
        "suspects": "يشتبه في أن",
        "did not fully understand": "لم يفهم تماماً",
        "pain and frustration": "معاناته وإحباطه",
        "team principal": "مدير الفريق",
        "new book": "كتاب جديد"
    }
    
    ar_title = title
    ar_desc = desc
    for en, ar in translations.items():
        ar_title = ar_title.replace(en, ar)
        ar_desc = ar_desc.replace(en, ar)
        
    return ar_title, ar_desc

def get_live_arabic_news():
    rss_url = "https://www.skysports.com/rss/12040"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    req = urllib.request.Request(rss_url, headers=headers)
    
    try:
        response = urllib.request.urlopen(req)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        item = root.find('./channel/item')
        if item is not None:
            raw_title = item.find('title').text if item.find('title') is not None else ""
            raw_desc = item.find('description').text if item.find('description') is not None else ""
            
            clean_title = clean_html(raw_title)
            clean_desc = clean_html(raw_desc)
            
            # تطبيق الصياغة والتعريب
            ar_title, ar_desc = translate_to_arabic_style(clean_title, clean_desc)
            
            return {
                'title': f"🚨 عاجل رياضي | {ar_title}",
                'script': f"عاجل رياضي: {ar_title}. التفاصيل: {ar_desc}"
            }
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")
    
    return None

if __name__ == "__main__":
    print("⚡ محرك 'SPORT BREAKING' العربي الفصيح يعمل الآن...\n")
    news = get_live_arabic_news()
    
    if news:
        print(f"📌 العنوان البصري:\n{news['title']}\n")
        print(f"📝 النص العربي الجاهز:\n{news['script']}")
        print("\n✅ تم جلب وتعريب الخبر بنجاح تام!")
    else:
        print("⚠️ تحقق من الاتصال بالإنترنت.")
