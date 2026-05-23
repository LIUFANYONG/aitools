"""Add AdSense ad units to all article HTML files."""
import os

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "articles")
PUB_ID = "ca-pub-9833675612669955"

ADSENSE_SCRIPT = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB_ID}" crossorigin="anonymous"></script>'

# In-article ad unit (native fluid format)
# NOTE: data-ad-slot needs to be replaced with real slot ID after AdSense approval
AD_UNIT_1 = f'''<div class="ad-unit">
<ins class="adsbygoogle"
     style="display:block;text-align:center;margin:24px 0"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="{PUB_ID}"
     data-ad-slot="5528030556"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>'''

AD_UNIT_2 = f'''<div class="ad-unit">
<ins class="adsbygoogle"
     style="display:block;text-align:center;margin:24px 0"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="{PUB_ID}"
     data-ad-slot="REPLACE-WITH-SLOT-ID-2"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>'''

AD_CSS = '.ad-unit{margin:24px 0;padding:8px 0;border-top:1px solid #30363d;border-bottom:1px solid #30363d}'

files = [f for f in os.listdir(ARTICLES_DIR) if f.endswith('.html') and f != 'index.html']
print(f"Found {len(files)} articles to add ads")

count = 0
for fname in files:
    fpath = os.path.join(ARTICLES_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if ads already added (check for the actual ad ins element)
    if 'data-ad-slot' in html:
        continue

    modified = False

    # 1. Add AdSense base script before </head> (if not present)
    if 'adsbygoogle.js' not in html:
        html = html.replace('</head>', f'  {ADSENSE_SCRIPT}\n</head>', 1)
        modified = True

    # 2. Add ad-unit CSS (if not present)
    if '.ad-unit' not in html:
        html = html.replace('</style>', f'{AD_CSS}\n</style>', 1)
        modified = True

    # 3. Add first ad unit after tool cards section, before "三、横向对比"
    if 'data-ad-slot' not in html:
        html = html.replace(
            '\n<h2>三、横向对比</h2>',
            f'\n{AD_UNIT_1}\n<h2>三、横向对比</h2>',
            1
        )
        # 4. Add second ad unit after CTA div and before "相关文章"
        html = html.replace(
            '\n<h2>相关文章</h2>',
            f'\n{AD_UNIT_2}\n<h2>相关文章</h2>',
            1
        )
        modified = True

    if modified:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1

print(f"Done! Added ads to {count} articles. Skipped {len(files) - count} (already had ads).")
print("NOTE: Replace '5528030556' and 'REPLACE-WITH-SLOT-ID-2' with real AdSense slot IDs after account approval.")
