"""Generate tag aggregation pages from index.html tool data."""
import os, re, urllib.parse
from collections import Counter

TAGS_DIR = os.path.join(os.path.dirname(__file__), "tags")
os.makedirs(TAGS_DIR, exist_ok=True)
BASE = "https://aitools-khaki.vercel.app"

# --- Extract tools from index.html ---
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
pat = re.compile(r'\{name:"([^"]+)",desc:"([^"]+)",url:"([^"]+)",icon:"([^"]+)",cat:"([^"]+)",tags:\[([^\]]+)\]\}')
tools = []
for m in pat.findall(html):
    tools.append({
        "name": m[0], "desc": m[1], "url": m[2], "icon": m[3], "cat": m[4],
        "tags": [t.strip().strip('"') for t in m[5].split(",") if t.strip()]
    })

# --- Count tags and filter (>= 3 tools) ---
tag_counter = Counter()
for t in tools:
    for tag in t["tags"]:
        tag_counter[tag] += 1

valid_tags = {tag: count for tag, count in tag_counter.items() if count >= 3}
print(f"Tags with 3+ tools: {len(valid_tags)}")
for tag, count in sorted(valid_tags.items(), key=lambda x: -x[1]):
    print(f"  {tag}: {count} tools")

# --- Category name map ---
cat_names = {
    "chat":"对话聊天","image":"图像创作","video":"视频生成","code":"编程开发",
    "office":"办公效率","audio":"音频音乐","agent":"AI Agent",
    "search":"AI搜索","design":"AI设计","marketing":"AI营销","edu":"AI教育","data":"AI数据",
}

# --- Generate each tag page ---
tag_pages = []
for tag, count in sorted(valid_tags.items()):
    tag_slug = tag
    tag_tools = [t for t in tools if tag in t["tags"]]

    # Build tool cards
    cards_html = ""
    for t in tag_tools:
        cname = cat_names.get(t["cat"], t["cat"])
        slug = t["name"].lower().replace(" ","-").replace(".","").replace("·","").replace("(","").replace(")","")
        tag_labels = "".join(f'<span class="t-tag">{tg}</span>' for tg in t["tags"])
        cards_html += f"""<a href="/tools/{slug}.html" class="tag-tool-card">
  <span class="t-icon">{t['icon']}</span>
  <div class="t-info">
    <div class="t-name">{t['name']}</div>
    <div class="t-desc">{t['desc']}</div>
    <div class="t-tags">{tag_labels}<span class="t-cat">{cname}</span></div>
  </div>
</a>"""

    page_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{tag}类AI工具合集：收录{count}款{tag}AI工具，涵盖{', '.join(set(cat_names.get(t['cat'],t['cat']) for t in tag_tools))}">
<meta name="keywords" content="{tag},AI工具,{tag}AI工具推荐">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE}/tags/{urllib.parse.quote(tag_slug)}.html">
<meta property="og:title" content="{tag} AI工具推荐 - AI工具箱">
<meta property="og:description" content="收录{count}款{tag}AI工具，帮你找到最合适的{tag}AI工具">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/tags/{urllib.parse.quote(tag_slug)}.html">
<meta property="og:site_name" content="AI工具箱">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-50DB4RCNL3"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-50DB4RCNL3');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9833675612669955" crossorigin="anonymous"></script>
<title>{tag} AI工具推荐（{count}款） - AI工具箱</title>
<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"CollectionPage",
  "name":"{tag} AI工具推荐",
  "description":"收录{count}款{tag}AI工具",
  "url":"{BASE}/tags/{urllib.parse.quote(tag_slug)}.html",
  "mainEntity":{{
    "@type":"ItemList",
    "itemListElement":[{",".join('{{"@type":"ListItem","position":'+str(i+1)+',"name":"'+t["name"]+'"}}' for i,t in enumerate(tag_tools))}
    ]
  }}
}}
</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.6;padding:20px;max-width:900px;margin:0 auto}}
h1{{font-size:22px;color:#fff;margin:12px 0 6px}}
.subtitle{{font-size:14px;color:#8b949e;margin-bottom:24px}}
.breadcrumb{{font-size:13px;margin-bottom:16px;color:#8b949e}}
.breadcrumb a{{color:#8b949e;text-decoration:none}}
.breadcrumb a:hover{{color:#58a6ff}}
.breadcrumb .sep{{margin:0 6px}}
.tag-tool-card{{display:flex;gap:12px;align-items:flex-start;padding:14px 16px;background:#161b22;border:1px solid #30363d;border-radius:10px;text-decoration:none;transition:.15s;margin-bottom:8px}}
.tag-tool-card:hover{{border-color:#58a6ff;background:#1a2332}}
.tag-tool-card .t-icon{{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;background:#0d1117}}
.tag-tool-card .t-info{{flex:1;min-width:0}}
.tag-tool-card .t-name{{font-size:15px;font-weight:600;color:#fff;margin-bottom:2px}}
.tag-tool-card .t-desc{{font-size:13px;color:#8b949e;line-height:1.4}}
.tag-tool-card .t-tags{{display:flex;gap:4px;margin-top:6px;flex-wrap:wrap;align-items:center}}
.tag-tool-card .t-tag{{padding:1px 6px;border-radius:8px;font-size:10px;background:rgba(88,166,255,0.1);color:#58a6ff}}
.tag-tool-card .t-cat{{font-size:10px;color:#8b949e;margin-left:4px}}
.ad-unit{{margin:24px 0;padding:8px 0;border-top:1px solid #30363d;border-bottom:1px solid #30363d}}
.back{{text-align:center;margin-top:30px}}
.back a{{color:#58a6ff}}
footer{{text-align:center;padding:30px 0;margin-top:40px;border-top:1px solid #30363d;font-size:13px;color:#8b949e}}
footer a{{color:#8b949e}}
.progress-bar{{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,#58a6ff,#a371f7);z-index:9999;width:0;transition:width .1s}}
.btp{{position:fixed;bottom:24px;right:24px;width:40px;height:40px;border-radius:50%;background:#58a6ff;color:#fff;border:none;cursor:pointer;font-size:18px;opacity:0;transform:translateY(20px);transition:opacity .3s,transform .3s;z-index:99;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(88,166,255,0.3)}}
.btp.visible{{opacity:1;transform:translateY(0)}}
.btp:hover{{background:#79b8ff;transform:translateY(-2px)}}
html{{scroll-behavior:smooth}}
@media(max-width:600px){{body{{padding:12px}}}}
</style>
</head>
<body>
<div class="progress-bar" id="progressBar"></div>
<script>window.addEventListener('scroll',function(){{var h=document.documentElement.scrollHeight-document.documentElement.clientHeight;var p=h>0?Math.min(100,(window.scrollY/h)*100):0;document.getElementById('progressBar').style.width=p+'%'}});</script>

<div class="breadcrumb"><a href="/">首页</a><span class="sep">›</span><a href="/tags/">标签</a><span class="sep">›</span><span>{tag}</span></div>
<h1>{tag} AI工具推荐</h1>
<p class="subtitle">收录 {count} 款{tag}相关AI工具，涵盖{', '.join(set(cat_names.get(t['cat'],t['cat']) for t in tag_tools))}等领域</p>

<div class="ad-unit">
<ins class="adsbygoogle" style="display:block;text-align:center" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-9833675612669955" data-ad-slot="5528030556"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

{cards_html}

<div class="ad-unit">
<ins class="adsbygoogle" style="display:block;text-align:center" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-9833675612669955" data-ad-slot="5194960856"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

<div class="back"><a href="/tags/">← 查看全部标签</a> · <a href="/">← 返回AI工具箱首页</a></div>
<footer><p>AI工具箱 2026 · <a href="/">返回首页</a> · <a href="/privacy.html">隐私政策</a> · <a href="/about.html">关于</a> · <a href="/tags/">标签列表</a></p></footer>
<button class="btp" id="btp" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="回到顶部">↑</button>
<script>window.addEventListener('scroll',function(){{document.getElementById('btp').classList.toggle('visible',window.scrollY>400)}});</script>
</body>
</html>"""

    fname = tag_slug + ".html"
    with open(os.path.join(TAGS_DIR, fname), "w", encoding="utf-8") as f:
        f.write(page_html)
    tag_pages.append({"tag": tag, "count": count, "file": fname})

print(f"\nGenerated {len(tag_pages)} tag pages")

# --- Generate tags index page ---
tag_links = ""
for tp in sorted(tag_pages, key=lambda x: -x["count"]):
    tag_links += f'<a href="{tp["file"]}" class="tag-link">{tp["tag"]}<span class="count">{tp["count"]}</span></a>\n'

idx_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="AI工具箱标签列表 - 按标签浏览AI工具，包括免费、开源、国产、推荐等分类标签">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE}/tags/">
<meta property="og:title" content="AI工具标签列表 - AI工具箱">
<meta property="og:description" content="按标签浏览110+款AI工具">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/tags/">
<meta property="og:site_name" content="AI工具箱">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-50DB4RCNL3"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-50DB4RCNL3');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9833675612669955" crossorigin="anonymous"></script>
<title>AI工具标签列表 - AI工具箱</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:20px;max-width:900px;margin:0 auto}}
h1{{font-size:22px;color:#fff;margin:12px 0;text-align:center}}
.subtitle{{font-size:14px;color:#8b949e;text-align:center;margin-bottom:24px}}
.breadcrumb{{font-size:13px;margin-bottom:16px;color:#8b949e}}
.breadcrumb a{{color:#8b949e;text-decoration:none}}
.breadcrumb a:hover{{color:#58a6ff}}
.breadcrumb .sep{{margin:0 6px}}
.tag-cloud{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}}
.tag-link{{display:inline-flex;align-items:center;gap:6px;padding:10px 18px;background:#161b22;border:1px solid #30363d;border-radius:20px;color:#c9d1d9;text-decoration:none;font-size:14px;transition:.15s}}
.tag-link:hover{{border-color:#58a6ff;color:#fff;background:#1a2332}}
.tag-link .count{{background:rgba(88,166,255,0.15);color:#58a6ff;font-size:11px;padding:2px 8px;border-radius:10px;font-weight:600}}
footer{{text-align:center;padding:30px 0;margin-top:40px;border-top:1px solid #30363d;font-size:13px;color:#8b949e}}
footer a{{color:#8b949e}}
.back{{text-align:center;margin-top:30px}}
.back a{{color:#58a6ff}}
</style>
</head>
<body>
<div class="breadcrumb"><a href="/">首页</a><span class="sep">›</span><span>标签列表</span></div>
<h1>AI工具标签列表</h1>
<p class="subtitle">共 {len(tag_pages)} 个标签，点击查看相关AI工具</p>
<div class="tag-cloud">
{tag_links}
</div>
<div class="back"><a href="/">← 返回AI工具箱首页</a></div>
<footer><p>AI工具箱 2026 · <a href="/">返回首页</a> · <a href="/privacy.html">隐私政策</a> · <a href="/about.html">关于</a></p></footer>
</body>
</html>"""

with open(os.path.join(TAGS_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(idx_html)

print(f"Generated tags index page with {len(tag_pages)} tags")
