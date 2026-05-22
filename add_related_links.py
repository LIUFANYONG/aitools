"""Add related article cross-links to all article HTML files."""
import os, re, random

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "articles")

files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html') and f != 'index.html']

# Extract metadata from all articles
all_articles = []
for fname in files:
    fpath = os.path.join(ARTICLES_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'<title>(.*?)</title>', html)
    title = m.group(1).replace(' - AI工具箱', '') if m else fname
    m2 = re.search(r'<meta name="keywords" content="([^"]*)"', html)
    cat = m2.group(1).split(',')[0] if m2 else 'AI工具'
    all_articles.append({"file": fname, "title": title, "cat": cat})

# Group by category
cat_map = {}
for a in all_articles:
    cat_map.setdefault(a["cat"], []).append(a)

print(f"Found {len(all_articles)} articles across {len(cat_map)} categories")

# Add related links to each article
for a in all_articles:
    # Find related articles (same category, exclude self)
    same_cat = [x for x in cat_map.get(a["cat"], []) if x["file"] != a["file"]]
    related = random.sample(same_cat, min(4, len(same_cat)))

    related_html = '\n<h2>相关文章</h2>\n<div class="related-box">\n'
    for r in related:
        related_html += f'  <a href="{r["file"]}" class="related-link">{r["title"]}</a>\n'
    related_html += '</div>\n'

    fpath = os.path.join(ARTICLES_DIR, a["file"])
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Only add if not already present
    if 'related-box' in html:
        continue

    # Also add CSS for related-box if not present
    if 'related-box' not in html:
        related_style = '.related-box{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:16px;margin:20px 0}.related-link{display:block;padding:8px 12px;margin:2px 0;color:#58a6ff;text-decoration:none;font-size:14px;border-radius:6px;transition:.15s}.related-link:hover{background:#1a2332;color:#fff}'
        # Insert CSS before </style>
        html = html.replace('</style>', related_style + '\n</style>', 1)

    # Insert related articles section before </article>
    html = html.replace('</article>', related_html + '</article>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

print("Done! Added related article cross-links.")
