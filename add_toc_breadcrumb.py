"""Add TOC + breadcrumb navigation to all article pages."""
import os, re

articles_dir = "articles"
improved = 0
skipped = 0

toc_css = """.toc{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:16px 20px;margin:20px 0}
.toc summary{font-size:15px;font-weight:600;color:#fff;cursor:pointer;list-style:none;display:flex;align-items:center;gap:6px}
.toc summary::-webkit-details-marker{display:none}
.toc summary::before{content:'📑';font-size:14px}
.toc ol{list-style:none;padding:0;margin:12px 0 0;counter-reset:toc}
.toc ol li{counter-increment:toc;margin:6px 0;font-size:14px}
.toc ol li a{color:#8b949e;text-decoration:none;transition:color .15s}
.toc ol li a:hover{color:#58a6ff}
.toc ol li a::before{content:counters(toc,'.')'. ';color:#d4a574;font-weight:600}
h2[id]{scroll-margin-top:20px}
"""

breadcrumb_css = """.breadcrumb{font-size:13px;margin-bottom:10px;color:#8b949e}
.breadcrumb a{color:#8b949e;text-decoration:none}
.breadcrumb a:hover{color:#58a6ff}
.breadcrumb .sep{margin:0 6px}"""

def make_breadcrumb_ld(title):
    return f"""<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"BreadcrumbList",
  "itemListElement":[
    {{"@type":"ListItem","position":1,"name":"AI工具箱","item":"https://aitools-khaki.vercel.app/"}},
    {{"@type":"ListItem","position":2,"name":"评测文章","item":"https://aitools-khaki.vercel.app/articles/"}},
    {{"@type":"ListItem","position":3,"name":"{title}"}}
  ]
}}
</script>"""

for fname in os.listdir(articles_dir):
    if not fname.endswith('.html') or fname == 'index.html':
        continue

    fpath = os.path.join(articles_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'BreadcrumbList' in html and 'class="toc"' in html and 'scroll-margin-top' in html:
        skipped += 1
        continue

    # ── 1. Add CSS ──
    if '.toc{' not in html:
        html = html.replace('</style>', f'\n{toc_css}\n</style>', 1)
    elif 'scroll-margin-top' not in html:
        html = html.replace('</style>', '\nh2[id]{scroll-margin-top:20px}\n</style>', 1)

    if '.breadcrumb{' not in html:
        html = html.replace('</style>', f'\n{breadcrumb_css}\n</style>', 1)

    # ── 2. Extract page title ──
    title_match = re.search(r'<h1>(.*?)</h1>', html)
    page_title = title_match.group(1) if title_match else "文章"

    # ── 3. Parse h2 headings, add IDs, build TOC ──
    h2_pattern = re.compile(r'<h2>(.*?)</h2>')
    h2s = h2_pattern.findall(html)

    toc_items = []
    for i, h2_text in enumerate(h2s):
        if h2_text in ('相关文章',):
            continue
        anchor = f"section-{i+1}"
        old_h2 = f'<h2>{h2_text}</h2>'
        new_h2 = f'<h2 id="{anchor}">{h2_text}</h2>'
        if old_h2 in html and f'id="{anchor}"' not in html:
            html = html.replace(old_h2, new_h2, 1)
        toc_items.append((anchor, h2_text))

    # Build TOC HTML and insert after article header
    if toc_items and 'class="toc"' not in html:
        toc_html = '<details class="toc" open>\n<summary>目录</summary>\n<ol>\n'
        for anchor, text in toc_items:
            toc_html += f'<li><a href="#{anchor}">{text}</a></li>\n'
        toc_html += '</ol>\n</details>\n'

        header_end = html.find('分钟</div>')
        if header_end > 0:
            insert_pos = html.find('\n', header_end) + 1
            html = html[:insert_pos] + '\n' + toc_html + html[insert_pos:]

    # ── 4. Breadcrumb ──
    if 'BreadcrumbList' not in html:
        breadcrumb_html = f'<div class="breadcrumb"><a href="/">首页</a><span class="sep">›</span><a href="/articles/">评测文章</a><span class="sep">›</span><span>{page_title}</span></div>'
        if '<div class="nav">' in html:
            html = re.sub(r'<div class="nav">.*?</div>', breadcrumb_html, html, count=1, flags=re.DOTALL)
        html = html.replace('</head>', f'\n{make_breadcrumb_ld(page_title)}\n</head>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    improved += 1

print(f"Articles improved: {improved}, skipped (already complete): {skipped}")
