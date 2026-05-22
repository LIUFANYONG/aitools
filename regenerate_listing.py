"""Regenerate articles listing page with SEO tags and current article list."""
import os, re, json

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "articles")
BASE_URL = "https://aitools-khaki.vercel.app"

articles = []
for fname in sorted(os.listdir(ARTICLES_DIR)):
    if not fname.endswith('.html') or fname == 'index.html':
        continue
    fpath = os.path.join(ARTICLES_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'<title>(.*?)</title>', content)
    title = m.group(1).replace(' - AI工具箱', '') if m else fname
    m2 = re.search(r'<meta name="keywords" content="([^"]*)"', content)
    cat = m2.group(1).split(',')[0] if m2 else 'AI工具'
    articles.append({"file": fname, "title": title, "cat": cat})

cats = {}
for a in articles:
    cats.setdefault(a["cat"], []).append(a)

cat_links_html = ""
for cat, arts in cats.items():
    cat_links_html += f'<div class="cat-section"><h2>{cat}</h2>\n'
    for a in arts:
        cat_links_html += f'  <a class="article-link" href="{a["file"]}"><span class="cat-badge">{cat}</span>{a["title"]}</a>\n'
    cat_links_html += '</div>\n'

# Build JSON-LD safely
ld_items = []
for a in articles[:50]:
    ld_items.append({
        "@type": "Article",
        "headline": a["title"],
        "url": f"{BASE_URL}/articles/{a['file']}"
    })

ld_json = json.dumps({
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "AI工具评测文章列表",
    "description": f"收录{len(articles)}篇AI工具深度评测文章",
    "url": f"{BASE_URL}/articles/",
    "hasPart": ld_items
}, ensure_ascii=False, indent=2)

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="AI工具评测文章列表，收录{len(articles)}篇AI工具深度评测，涵盖AI写作、AI绘画、AI编程、AI视频等多分类">
<meta name="keywords" content="AI工具评测,AI工具推荐,AI工具对比">
<meta name="author" content="AI工具箱">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE_URL}/articles/">
<meta property="og:title" content="AI工具评测文章列表 - 共{len(articles)}篇">
<meta property="og:description" content="收录{len(articles)}篇AI工具深度评测，涵盖多分类">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE_URL}/articles/">
<meta property="og:site_name" content="AI工具箱">
<meta name="twitter:card" content="summary">
<link rel="dns-prefetch" href="https://pagead2.googlesyndication.com">
<title>AI工具评测 · 共{len(articles)}篇 - AI工具箱</title>
<script type="application/ld+json">
{ld_json}
</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:20px;max-width:900px;margin:0 auto}}
h1{{font-size:22px;color:#fff;text-align:center;margin:20px 0;padding-bottom:16px;border-bottom:1px solid #30363d}}
.cat-section{{margin:30px 0}}
.cat-section h2{{font-size:18px;color:#d4a574;margin-bottom:12px}}
.article-link{{display:block;padding:10px 14px;margin:4px 0;background:#161b22;border-radius:8px;color:#c9d1d9;text-decoration:none;font-size:14px;transition:.15s;border:1px solid #30363d}}
.article-link:hover{{background:#1a2332;border-color:#58a6ff;color:#fff}}
.back{{text-align:center;margin-top:30px}}
.back a{{color:#58a6ff}}
.cat-badge{{display:inline-block;padding:2px 8px;border-radius:8px;font-size:10px;margin-right:6px;background:rgba(88,166,255,0.1);color:#58a6ff}}
</style>
</head>
<body>
<h1>AI工具评测文章 · 共{len(articles)}篇</h1>

{cat_links_html}

<div class="back"><a href="{BASE_URL}/">← 返回AI工具箱首页</a></div>
</body>
</html>
"""

with open(os.path.join(ARTICLES_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print(f"Listing page regenerated with {len(articles)} articles across {len(cats)} categories")
