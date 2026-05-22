"""Add previous/next article navigation to all article pages."""
import os, re
from collections import defaultdict

articles_dir = "articles"
improved = 0
skipped = 0

pn_css = """.prev-next{display:flex;justify-content:space-between;gap:12px;margin:20px 0;flex-wrap:wrap}
.pn-link{flex:1;min-width:140px;padding:12px 16px;background:#161b22;border:1px solid #30363d;border-radius:8px;color:#c9d1d9;text-decoration:none;font-size:14px;transition:.15s;display:flex;align-items:center;gap:6px}
.pn-link:hover{border-color:#58a6ff;color:#fff}
.pn-link.prev{justify-content:flex-start}
.pn-link.next{justify-content:flex-end;text-align:right}
.pn-link .arrow{color:#58a6ff;font-size:16px}
.pn-link .label{font-size:11px;color:#8b949e;display:block}
"""

# ── Step 1: Index all articles by category ──
cats = defaultdict(list)
titles = {}  # filename -> title

for fname in os.listdir(articles_dir):
    if not fname.endswith('.html') or fname == 'index.html':
        continue
    fpath = os.path.join(articles_dir, fname)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    # Extract category from meta keywords
    m = re.search(r'<meta name="keywords" content="([^"]+)"', html)
    cat = m.group(1).split(',')[0].strip() if m else '其他'

    # Extract title from h1
    tm = re.search(r'<h1[^>]*>(.*?)</h1>', html)
    title = tm.group(1) if tm else fname

    cats[cat].append(fname)
    titles[fname] = title

# Sort articles within each category by filename (consistent ordering)
for cat in cats:
    cats[cat].sort()

print(f"Indexed {sum(len(v) for v in cats.values())} articles across {len(cats)} categories")

# ── Step 2: Add prev/next to each article ──
for cat, files in cats.items():
    for i, fname in enumerate(files):
        fpath = os.path.join(articles_dir, fname)
        with open(fpath, encoding='utf-8') as f:
            html = f.read()

        if 'class="prev-next"' in html:
            skipped += 1
            continue

        prev_file = files[i-1] if i > 0 else None
        next_file = files[i+1] if i < len(files) - 1 else None

        # Build prev/next HTML
        pn_html = '<nav class="prev-next">\n'
        if prev_file:
            pn_html += f'  <a href="{prev_file}" class="pn-link prev"><span class="arrow">←</span> <span><span class="label">上一篇</span>{titles[prev_file]}</span></a>\n'
        else:
            pn_html += '  <span></span>\n'
        if next_file:
            pn_html += f'  <a href="{next_file}" class="pn-link next"><span><span class="label">下一篇</span>{titles[next_file]}</span> <span class="arrow">→</span></a>\n'
        else:
            pn_html += '  <span></span>\n'
        pn_html += '</nav>'

        # Add CSS
        if '.prev-next{' not in html:
            html = html.replace('</style>', f'\n{pn_css}\n</style>', 1)

        # Insert prev/next before </article>
        if 'class="prev-next"' not in html:
            html = html.replace('</article>', f'{pn_html}\n</article>', 1)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        improved += 1

print(f"Improved: {improved}, Skipped (already done): {skipped}")
