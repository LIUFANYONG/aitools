"""Add UI improvements to all tool detail pages: progress bar + back-to-top button."""
import os

tools_dir = "tools"
improved = 0
skipped = 0

progress_css = """/* Progress bar */
.progress-bar{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,#58a6ff,#a371f7);z-index:9999;width:0;transition:width .1s}"""

btp_css = """/* Back to top */
.btp{position:fixed;bottom:24px;right:24px;width:40px;height:40px;border-radius:50%;background:#58a6ff;color:#fff;border:none;cursor:pointer;font-size:18px;opacity:0;transform:translateY(20px);transition:opacity .3s,transform .3s;z-index:99;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(88,166,255,0.3)}
.btp.visible{opacity:1;transform:translateY(0)}
.btp:hover{background:#79b8ff;transform:translateY(-2px)}
html{scroll-behavior:smooth}"""

btp_html_js = """<button class="btp" id="btp" onclick="window.scrollTo({top:0,behavior:'smooth'})" title="回到顶部">↑</button>
<script>
window.addEventListener('scroll',function(){document.getElementById('btp').classList.toggle('visible',window.scrollY>400)});
</script>"""

progress_html_js = """<div class="progress-bar" id="progressBar"></div>
<script>
window.addEventListener('scroll',function(){var h=document.documentElement.scrollHeight-document.documentElement.clientHeight;var p=h>0?Math.min(100,(window.scrollY/h)*100):0;document.getElementById('progressBar').style.width=p+'%'});
</script>"""

for fname in os.listdir(tools_dir):
    if not fname.endswith('.html'):
        continue
    if fname == 'index.html':
        continue

    fpath = os.path.join(tools_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'id="progressBar"' in html and 'id="btp"' in html:
        skipped += 1
        continue

    # Add CSS
    if '.progress-bar{' not in html:
        html = html.replace('</style>', f'\n{progress_css}\n</style>', 1)
    if '.btp{' not in html:
        html = html.replace('</style>', f'\n{btp_css}\n</style>', 1)

    # Add HTML + JS
    if 'id="progressBar"' not in html:
        html = html.replace('<body>', f'<body>\n{progress_html_js}', 1)
    if 'id="btp"' not in html:
        html = html.replace('</body>', f'{btp_html_js}\n</body>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    improved += 1

print(f"Tool pages improved: {improved}, skipped (already done): {skipped}")
