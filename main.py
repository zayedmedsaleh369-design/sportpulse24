import feedparser, os, textwrap
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip

def fetch_breaking_news():
    RSS = "https://news.google.com/rss/search?q=football+breaking+when:15m&hl=en-GB&gl=GB&ceid=GB:en"
    feed = feedparser.parse(RSS)
    if not feed.entries:
        return None
    title = feed.entries[0].title.split(" - ")[0]
    return title[:80]

def is_new(title):
    if not os.path.exists("last_news.txt"):
        return True
    with open("last_news.txt","r") as f:
        return f.read() != title

def save_last(title):
    with open("last_news.txt","w") as f:
        f.write(title)

def create_image(title):
    W,H=1080,1920
    img=Image.new('RGB',(W,H),(0,0,0))
    draw=ImageDraw.Draw(img)
    draw.text((W//2,700),"BREAKING",fill=(230,0,35),anchor="mm")
    draw.rectangle([(100,850,980,860)],fill=(230,0,35))
    wrapped=textwrap.fill(title.upper(),width=22)
    draw.text((W//2,1100),wrapped,fill=(255,255,255),anchor="mm",align="center")
    img.save("breaking.png")
    return "breaking.png"

def create_video(img_path):
    clip=ImageClip(img_path).set_duration(9)
    clip=clip.resize(lambda t: 1+0.05*t)
    clip.write_videofile("final.mp4",fps=24,codec='libx264')
    return "final.mp4"

if __name__=="__main__":
    title=fetch_breaking_news()
    if title and is_new(title):
        print(f"NEW: {title}")
        img=create_image(title)
        create_video(img)
        save_last(title)
    else:
        print("No new news")
