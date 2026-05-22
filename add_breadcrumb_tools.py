"""Add breadcrumb navigation to all tool detail pages."""
import os, re

tools_dir = "tools"
improved = 0

breadcrumb_css = """.breadcrumb{font-size:13px;margin-bottom:10px;color:#8b949e}
.breadcrumb a{color:#8b949e;text-decoration:none}
.breadcrumb a:hover{color:#58a6ff}
.breadcrumb .sep{margin:0 6px}"""

def make_breadcrumb_ld(title, url_slug):
    return f"""<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"BreadcrumbList",
  "itemListElement":[
    {{"@type":"ListItem","position":1,"name":"AI工具箱","item":"https://aitools-khaki.vercel.app/"}},
    {{"@type":"ListItem","position":2,"name":"工具详情","item":"https://aitools-khaki.vercel.app/tools/"}},
    {{"@type":"ListItem","position":3,"name":"{title}"}}
  ]
}}
</script>"""

for fname in os.listdir(tools_dir):
    if not fname.endswith('.html') or fname == 'index.html':
        continue

    fpath = os.path.join(tools_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'BreadcrumbList' in html:
        continue

    # Add CSS
    if '.breadcrumb{' not in html:
        html = html.replace('</style>', f'\n{breadcrumb_css}\n</style>', 1)

    # Extract title
    title_match = re.search(r'<h1>(.*?)</h1>', html)
    page_title = title_match.group(1) if title_match else "工具"

    # Replace nav with breadcrumb
    breadcrumb_html = f'<div class="breadcrumb"><a href="/">首页</a><span class="sep">›</span><a href="/tools/">工具详情</a><span class="sep">›</span><span>{page_title}</span></div>'
    if '<div class="nav">' in html:
        html = re.sub(r'<div class="nav">.*?</div>', breadcrumb_html, html, count=1, flags=re.DOTALL)

    # Add JSON-LD
    html = html.replace('</head>', f'\n{make_breadcrumb_ld(page_title, fname)}\n</head>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    improved += 1

print(f"Tool pages improved: {improved}")
