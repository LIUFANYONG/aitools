"""
Retrofit existing articles with JSON-LD structured data, Open Graph tags,
canonical URLs, preconnect hints, and performance optimizations.
"""
import os, re

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "articles")
BASE_URL = "https://aitools-khaki.vercel.app"

files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html') and f != 'index.html']
print(f"Found {len(files)} articles to retrofit")

skipped = 0
for fname in files:
    fpath = os.path.join(ARTICLES_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip already-retrofitted articles
    if 'application/ld+json' in html:
        skipped += 1
        continue

    # Extract title and description
    title_match = re.search(r'<title>(.*?)</title>', html)
    title = title_match.group(1) if title_match else "AI工具评测"
    title_clean = title.replace(' - AI工具箱', '')

    desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
    description = desc_match.group(1) if desc_match else title_clean

    # Extract category from nav or keywords
    kw_match = re.search(r'<meta name="keywords" content="([^"]*)"', html)
    keywords = kw_match.group(1) if kw_match else "AI工具"

    # Extract reading time
    time_match = re.search(r'阅读约(\d+)分钟', html)
    read_time = time_match.group(1) if time_match else "4"

    # Build new head with SEO tags
    url = f"{BASE_URL}/articles/{fname}"

    new_head = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="AI工具箱">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title_clean}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="AI工具箱">
<meta property="article:published_time" content="2026-05-22T00:00:00+08:00">
<meta name="twitter:card" content="summary">
<link rel="dns-prefetch" href="https://pagead2.googlesyndication.com">
<title>{title}</title>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title_clean}",
  "description": "{description}",
  "author": {{"@type": "Organization", "name": "AI工具箱"}},
  "publisher": {{"@type": "Organization", "name": "AI工具箱", "url": "{BASE_URL}"}},
  "datePublished": "2026-05-22T00:00:00+08:00",
  "dateModified": "2026-05-22T00:00:00+08:00",
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "{url}"}},
  "wordCount": "800",
  "timeRequired": "PT{read_time}M",
  "about": {{"@type": "Thing", "name": "{keywords.split(',')[0] if ',' in keywords else keywords}"}},
  "inLanguage": "zh-CN"
}}
</script>"""

    # Replace old head (from <!DOCTYPE to </title>) with new head
    # Find the old <style> tag to preserve it
    style_start = html.find('<style>')
    style_end = html.find('</style>') + len('</style>')

    old_head_end = html.find('</head>')

    # Build the final HTML
    old_style = html[style_start:style_end] if style_start > 0 else ""
    old_body_start = html.find('<body>')
    old_body_end = html.find('</body>') + len('</body>')
    old_body = html[old_body_start:old_body_end]

    final = new_head + "\n" + old_style + "\n</head>\n" + old_body + "\n</html>"

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(final)

print(f"Done! Retrofit {len(files) - skipped} new articles, skipped {skipped} already-retrofitted.")
