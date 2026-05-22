"""Generate individual tool detail pages from index.html tool data."""
import os, re, random, urllib.parse

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")
os.makedirs(TOOLS_DIR, exist_ok=True)
BASE = "https://aitools-khaki.vercel.app"

# --- Extract tools from index.html ---
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()
pat = re.compile(r'\{name:"([^"]+)",desc:"([^"]+)",url:"([^"]+)",icon:"([^"]+)",cat:"([^"]+)",tags:\[([^\]]+)\]\}')
tools = []
for m in pat.findall(html):
    tools.append({"name":m[0],"desc":m[1],"url":m[2],"icon":m[3],"cat":m[4],
                  "tags":[t.strip().strip('"') for t in m[5].split(",") if t.strip()]})

# --- Category info ---
cat_info = {
    "chat":    ("对话聊天", "聊天对话"),
    "image":   ("图像创作", "AI绘画和图片处理"),
    "video":   ("视频生成", "视频创作和编辑"),
    "code":    ("编程开发", "写代码和开发"),
    "office":  ("办公效率", "办公文档处理"),
    "audio":   ("音频音乐", "音频和音乐制作"),
    "agent":   ("AI Agent", "AI智能体和自动化"),
    "search":  ("AI搜索引擎", "AI搜索和信息检索"),
    "design":  ("AI设计工具", "UI和平面设计"),
    "marketing":("AI营销写作", "营销文案和内容"),
    "edu":     ("AI学习教育", "学习和教育培训"),
    "data":    ("AI数据分析", "数据分析和报表"),
}

# --- Content templates ---
templates = {
    "intro": [
        "{name}在{cat_name}领域备受关注——{desc}。作为一个资深AI工具用户，我对{name}进行了深度体验，下面从功能、优缺点、使用场景和定价等方面为你全面解析。",
        "最近很多人在问{name}怎么样、值不值得用。{desc}。本文根据实际使用体验，从多个维度分析{name}的真实表现。",
        "如果你正在寻找{cat_name}领域的工具，{name}一定在你的候选名单里。{desc}。这篇评测帮你判断它是否适合你。",
    ],
    "features_intro": [
        "{name}的核心竞争力在于它的功能和定位。作为{cat_name}工具，以下是它最突出的能力：",
        "用了{name}一段时间后，以下几个功能让我印象深刻：",
    ],
    "usecase": [
        "{name}最适合的场景是{cat_name}相关的日常工作。比如你需要经常处理{task}相关的内容，{name}可以大幅提升效率。对于入门用户来说，操作门槛较低，很快就能上手；对于专业用户，它提供的深度功能也足够满足日常需求。",
        "实际使用中，{name}在以下几个方面表现最亮眼：首先是日常{task}场景，效率提升明显；其次是团队协作场景，如果你需要和同事共享工作成果；最后是个人创作场景，{name}可以帮助快速产出高质量内容。",
    ],
    "verdict": [
        "总的来说，{name}是{cat_name}领域值得推荐的一款工具。它不是完美的——任何工具都有自己的短板——但在核心功能上表现扎实。如果你在{cat_name}方面的需求比较常规，{name}能很好地满足你。",
        "经过一段时间的深度使用，我认为{name}对得起它在{cat_name}领域的口碑。虽然有一些小缺点，但瑕不掩瑜。推荐给所有需要{cat_name}工具的朋友。",
        "{name}给我的整体感受是性价比不错。它可能不是{cat_name}领域最强大的，但在实际体验和稳定性上做得很平衡。对于大多数用户来说，日常使用完全够用。",
    ],
}

# Pricing data (approximate, based on public info)
pricing_map = {
    "ChatGPT":"免费版可用 / Plus $20/月 / Pro $200/月",
    "Claude":"免费版限额 / Pro $20/月 / Team $25/人/月",
    "Gemini":"免费 / Advanced $19.99/月",
    "DeepSeek":"完全免费 / API极低价",
    "Kimi":"免费额度充足 / 部分高级功能会员",
    "通义千问":"免费 / 企业版按量计费",
    "文心一言":"免费 / 专业版会员制",
    "豆包":"完全免费",
    "Perplexity":"免费 / Pro $20/月",
    "讯飞星火":"免费 / 企业版定制",
    "360智脑":"免费",
    "百川智能":"免费 / API收费",
    "Poe":"免费 / 订阅$19.99/月",
    "Character.AI":"免费 / c.ai+ $9.99/月",
    "Midjourney":"Basic $10/月 / Standard $30/月 / Pro $60/月",
    "Stable Diffusion":"开源免费 / 云服务按量",
    "DALL·E 3":"ChatGPT Plus包含 / API按量",
    "Canva AI":"免费 / Pro $12.99/月",
    "Remove.bg":"免费(低清) / 按张或订阅(高清)",
    "Leonardo.AI":"免费额度 / 订阅从$12/月起",
    "Adobe Firefly":"免费额度 / Creative Cloud含更多",
    "通义万相":"免费",
    "文心一格":"免费额度大 / 高级功能会员",
    "美图AI":"免费 / VIP功能付费",
    "Clipdrop":"免费额度 / Pro订阅",
    "SeaArt":"免费额度 / 会员付费",
    "Upscale.media":"免费(低清) / 付费高清",
    "Sora":"ChatGPT Plus/Pro包含",
    "Runway":"免费额度 / Standard $15/月 / Pro $35/月",
    "Pika":"免费额度 / 订阅$10/月起",
    "可灵":"免费额度 / 会员付费",
    "HeyGen":"免费额度 / Creator $29/月 / Business $89/月",
    "剪映AI":"免费 / 部分高级素材付费",
    "腾讯智影":"免费额度 / 会员付费",
    "InVideo":"免费版(有水印) / Business $30/月",
    "Fliki":"免费额度 / 订阅$28/月起",
    "Descript":"免费额度 / Pro $30/月",
    "Synthesia":"Starter $29/月 / Enterprise定制",
    "GitHub Copilot":"Individual $10/月 / Business $19/月 / 学生免费",
    "Claude Code":"API付费(按token) / Claude Pro $20/月",
    "Cursor":"免费额度(2000次/月) / Pro $20/月",
    "Windsurf":"免费 / Teams $15/人/月",
    "v0.dev":"免费额度 / 订阅$20/月",
    "Replit Ghostwriter":"免费 / Hacker $25/月",
    "通义灵码":"完全免费",
    "Bolt.new":"免费额度 / Pro $20/月",
    "Lovable":"免费额度 / 订阅制",
    "Tabnine":"免费版 / Pro $12/月 / Enterprise定制",
    "Sourcegraph Cody":"免费 / Enterprise定制",
    "Cline":"免费开源 / API费用自理",
    "Notion AI":"免费版(限额) / Plus $10/月含AI",
    "Gamma":"免费 / Plus $10/月",
    "Grammarly":"免费 / Premium $12/月",
    "秘塔写作猫":"免费额度 / 会员付费",
    "ChatPDF":"免费(每日限额) / Plus $5/月",
    "Otter.ai":"免费 / Pro $16.99/月",
    "Beautiful.ai":"Pro $12/月 / Team $40/月",
    "Tome":"免费 / Pro $16/月",
    "SlidesAI":"免费 / Pro $10/月",
    "Fireflies.ai":"免费 / Pro $18/月",
    "讯飞听见":"免费额度 / 会员付费",
    "360AI办公":"免费 / 部分高级功能付费",
    "DocuAsk":"免费额度 / 订阅制",
    "Humata":"免费 / Pro $9.99/月",
    "Suno":"免费额度(每日) / Pro $10/月",
    "ElevenLabs":"免费(1万字符/月) / Starter $5/月 / Pro $22/月",
    "Udio":"免费额度 / 订阅制",
    "Murf.ai":"免费 / Pro $29/月",
    "Audiobox":"免费(研究预览版)",
    "剪映配音":"免费",
    "Soundraw":"免费额度 / Pro $19.99/月",
    "Beatoven":"免费额度 / 订阅制",
    "Adobe Podcast":"免费",
    "网易天音":"免费额度 / 会员付费",
    "AutoGPT":"开源免费 / API费用自理",
    "MetaGPT":"开源免费 / API费用自理",
    "CrewAI":"开源 / Enterprise定制",
    "Coze":"免费 / 企业版收费",
    "Dify":"开源免费 / Cloud免费额度 / Enterprise定制",
    "扣子":"免费",
    "AgentGPT":"免费额度 / 订阅制",
    "BabyAGI":"开源免费 / API费用自理",
    "文心智能体":"免费",
    "You.com":"免费 / Pro $14.99/月",
    "Phind":"免费额度 / Phind Plus订阅",
    "Microsoft Copilot":"免费 / Copilot Pro $20/月",
    "Consensus":"免费 / Premium $11.99/月",
    "Devv":"免费",
    "秘塔AI搜索":"免费",
    "Figma AI":"免费版(限功能) / Pro $12/月 / Enterprise $45/月",
    "Uizard":"免费 / Pro $12/月",
    "Galileo AI":"等待列表 / 即将公布",
    "Looka":"Basic $20一次性 / Premium $65一次性",
    "Khroma":"免费",
    "Autodraw":"免费",
    "Jasper":"Creator $49/月 / Pro $69/月",
    "Copy.ai":"免费版 / Pro $49/月",
    "Writesonic":"免费额度 / 订阅从$20/月起",
    "火山写作":"免费额度 / 会员付费",
    "易撰":"免费额度 / VIP付费",
    "爱撰写":"免费额度 / 会员付费",
    "Duolingo Max":"免费版 / Super $12.99/月 / Max $29.99/月",
    "Khanmigo":"$44/年 / 教师免费",
    "Quizlet AI":"免费 / Quizlet Plus $7.99/月",
    "作业帮":"免费 / VIP功能付费",
    "学而思AI":"免费体验 / 课程付费",
    "Julius AI":"免费额度 / 订阅从$20/月起",
    "Obviously AI":"免费试用 / 订阅从$80/月起",
    "Rows":"免费 / Pro $19/月",
    "WPS AI":"免费额度 / WPS会员含更多AI功能",
}

# Generate pages
count = 0
for t in tools:
    cat = t["cat"]
    cname = cat_info.get(cat, (cat, cat))[0]
    task = cat_info.get(cat, (cat, ""))[1]
    pricing = pricing_map.get(t["name"], "详见官网")

    slug = t["name"].lower().replace(" ","-").replace(".","").replace("·","").replace("(","").replace(")","")
    fname = slug + ".html"

    intro = random.choice(templates["intro"]).format(name=t["name"], cat_name=cname, desc=t["desc"])
    features_intro = random.choice(templates["features_intro"]).format(name=t["name"], cat_name=cname)
    usecase = random.choice(templates["usecase"]).format(name=t["name"], cat_name=cname, task=task)
    verdict = random.choice(templates["verdict"]).format(name=t["name"], cat_name=cname)

    # Similar tools (same category, max 4)
    same_cat = [x for x in tools if x["cat"]==cat and x["name"]!=t["name"]]
    similar = random.sample(same_cat, min(4, len(same_cat)))
    sim_html = ""
    for s in similar:
        sslug = s["name"].lower().replace(" ","-").replace(".","").replace("·","").replace("(","").replace(")","")
        sim_html += f'<a href="{sslug}.html" class="similar-link">{s["icon"]} {s["name"]}</a>\n'

    # Features from tags and category
    tag_features = [f"{cname}核心能力", f"智能{t['tags'][0] if t['tags'] else cname}功能"] if t["tags"] else []
    gen_features = [f"简洁直观的操作界面", f"持续更新的AI模型", f"多平台支持"]
    feat_list = tag_features + gen_features

    feat_html = ""
    for feat in feat_list:
        feat_html += f"<li>{feat}</li>\n"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{t['name']}深度评测：{t['desc']} | 功能介绍、优缺点、价格、使用场景全解析">
<meta name="keywords" content="{t['name']},{cname},AI工具,{t['name']}评测">
<meta name="author" content="AI工具箱">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE}/tools/{urllib.parse.quote(fname)}">
<meta property="og:title" content="{t['name']} - {cname}工具评测 | AI工具箱">
<meta property="og:description" content="{t['name']}深度评测：{t['desc']}">
<meta property="og:type" content="article">
<meta property="og:url" content="{BASE}/tools/{urllib.parse.quote(fname)}">
<meta property="og:site_name" content="AI工具箱">
<meta name="twitter:card" content="summary">
<meta name="google-adsense-account" content="ca-pub-9833675612669955">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9833675612669955" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-REPLACE-WITH-ID"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-REPLACE-WITH-ID');</script>
<title>{t['name']} - {cname}工具评测 | AI工具箱</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.6;padding:20px;max-width:800px;margin:0 auto}}
h1{{font-size:22px;color:#fff;margin-bottom:8px}}
h2{{font-size:18px;color:#d4a574;margin:30px 0 16px;border-left:3px solid #d4a574;padding-left:12px}}
h3{{font-size:16px;margin-bottom:6px}}
p{{margin-bottom:14px;color:#8b949e;font-size:15px}}
li{{color:#8b949e;font-size:14px;margin-bottom:6px;margin-left:20px}}
a{{color:#58a6ff;text-decoration:none}}
.nav{{margin-bottom:20px;font-size:13px}}
.nav a{{color:#8b949e}}
.header{{text-align:center;padding:20px 0;border-bottom:1px solid #30363d;margin-bottom:30px}}
.header .icon{{font-size:60px;display:block;margin-bottom:12px}}
.header .cat-tag{{display:inline-block;padding:2px 10px;border-radius:12px;font-size:11px;background:rgba(88,166,255,0.1);color:#58a6ff;margin-top:8px}}
.info-card{{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px;margin:20px 0;display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.info-card .label{{font-size:12px;color:#8b949e}}
.info-card .value{{font-size:14px;color:#fff}}
.btn-visit{{display:block;width:fit-content;margin:12px auto;padding:12px 32px;border-radius:24px;background:linear-gradient(135deg,#d4a574,#e6b980);color:#000;text-decoration:none;font-weight:700;font-size:15px;text-align:center;transition:.2s}}
.btn-visit:hover{{opacity:0.9}}
.ad-unit{{margin:24px 0;padding:8px 0;border-top:1px solid #30363d;border-bottom:1px solid #30363d}}
.similar-box{{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:16px;margin:20px 0}}
.similar-link{{display:inline-block;padding:6px 14px;margin:4px;border-radius:20px;background:#1a2332;color:#58a6ff;text-decoration:none;font-size:13px;transition:.15s;border:1px solid #30363d}}
.similar-link:hover{{border-color:#58a6ff;color:#fff}}
footer{{text-align:center;padding:30px 0;margin-top:40px;border-top:1px solid #30363d;font-size:13px;color:#8b949e}}
footer a{{color:#8b949e}}
@media(max-width:600px){{body{{padding:12px}}h1{{font-size:18px}}.info-card{{grid-template-columns:1fr}}}}
.progress-bar{{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,#58a6ff,#a371f7);z-index:9999;width:0;transition:width .1s}}
.btp{{position:fixed;bottom:24px;right:24px;width:40px;height:40px;border-radius:50%;background:#58a6ff;color:#fff;border:none;cursor:pointer;font-size:18px;opacity:0;transform:translateY(20px);transition:opacity .3s,transform .3s;z-index:99;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(88,166,255,0.3)}}
.btp.visible{{opacity:1;transform:translateY(0)}}
.btp:hover{{background:#79b8ff;transform:translateY(-2px)}}
html{{scroll-behavior:smooth}}
</style>
</head>
<body>
<div class="progress-bar" id="progressBar"></div>
<script>window.addEventListener('scroll',function(){{var h=document.documentElement.scrollHeight-document.documentElement.clientHeight;var p=h>0?Math.min(100,(window.scrollY/h)*100):0;document.getElementById('progressBar').style.width=p+'%'}});</script>
<div class="nav"><a href="/">AI工具箱首页</a> · <a href="/articles/">评测文章</a> · <a href="/tools/">工具详情</a></div>
<article>
<div class="header">
  <span class="icon">{t['icon']}</span>
  <h1>{t['name']}</h1>
  <p>{t['desc']}</p>
  <span class="cat-tag">{cname}</span>
</div>

<h2>工具简介</h2>
<p>{intro}</p>

<div class="info-card">
  <div><div class="label">产品类型</div><div class="value">{cname}</div></div>
  <div><div class="label">参考价格</div><div class="value">{pricing}</div></div>
  <div><div class="label">官方网站</div><div class="value"><a href="{t['url']}" target="_blank" rel="noopener nofollow">{t['url'][:40]}...</a></div></div>
  <div><div class="label">标签</div><div class="value">{', '.join(t['tags'][:4]) if t['tags'] else cname}</div></div>
</div>

<a href="{t['url']}" class="btn-visit" target="_blank" rel="noopener nofollow">访问官网</a>

<h2>核心功能</h2>
<p>{features_intro}</p>
<ul>
{feat_html}
</ul>

<h2>实际使用场景</h2>
<p>{usecase}</p>

<div class="ad-unit">
<ins class="adsbygoogle" style="display:block;text-align:center;margin:24px 0" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-9833675612669955" data-ad-slot="REPLACE-WITH-SLOT-ID-1"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

<h2>综合评价</h2>
<p>{verdict}</p>
<p>如果你对{cname}领域有持续需求，{t['name']}会是一个不错的选择。建议先了解免费版或试用额度，确认符合自己的使用习惯后再做决定。</p>

<div class="ad-unit">
<ins class="adsbygoogle" style="display:block;text-align:center;margin:24px 0" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-9833675612669955" data-ad-slot="REPLACE-WITH-SLOT-ID-2"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

<h2>同类工具推荐</h2>
<div class="similar-box">
{sim_html}
</div>
</article>
<footer>
  <p>AI工具箱 2026 · <a href="/">返回首页</a> · <a href="/privacy.html">隐私政策</a> · <a href="/about.html">关于</a> · <a href="/articles/">文章列表</a></p>
</footer>
<button class="btp" id="btp" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="回到顶部">↑</button>
<script>window.addEventListener('scroll',function(){{document.getElementById('btp').classList.toggle('visible',window.scrollY>400)}});</script>
</body>
</html>"""

    with open(os.path.join(TOOLS_DIR, fname), "w", encoding="utf-8") as f:
        f.write(html)
    count += 1

# Generate tools index
cat_links = ""
for cat_key in cat_info:
    cn = cat_info[cat_key][0]
    cat_tools = [t for t in tools if t["cat"] == cat_key]
    cat_links += f'<div class="cat-section"><h2>{cn} ({len(cat_tools)}款)</h2>\n'
    for t in cat_tools:
        slug = t["name"].lower().replace(" ","-").replace(".","").replace("·","").replace("(","").replace(")","")
        cat_links += f'  <a class="tool-link" href="{slug}.html">{t["icon"]} {t["name"]}</a>\n'
    cat_links += '</div>\n'

idx_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="AI工具箱 - {len(tools)}款AI工具详细评测，涵盖{len(cat_info)}个分类">
<meta name="keywords" content="AI工具评测,AI工具详情">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE}/tools/">
<meta property="og:title" content="AI工具详情 · {len(tools)}款工具评测 | AI工具箱">
<meta property="og:description" content="收录{len(tools)}款AI工具的详细介绍，涵盖{len(cat_info)}个分类">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/tools/">
<meta property="og:site_name" content="AI工具箱">
<title>AI工具详情 · 共{len(tools)}款 - AI工具箱</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:20px;max-width:900px;margin:0 auto}}
h1{{font-size:22px;color:#fff;text-align:center;margin:20px 0;padding-bottom:16px;border-bottom:1px solid #30363d}}
.cat-section{{margin:30px 0}}
.cat-section h2{{font-size:18px;color:#d4a574;margin-bottom:12px}}
.tool-link{{display:inline-block;padding:8px 14px;margin:3px;background:#161b22;border-radius:20px;color:#c9d1d9;text-decoration:none;font-size:13px;transition:.15s;border:1px solid #30363d}}
.tool-link:hover{{background:#1a2332;border-color:#58a6ff;color:#fff}}
.back{{text-align:center;margin-top:30px}}
.back a{{color:#58a6ff}}
footer{{text-align:center;padding:30px 0;margin-top:40px;border-top:1px solid #30363d;font-size:13px;color:#8b949e}}
footer a{{color:#8b949e}}
.progress-bar{{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,#58a6ff,#a371f7);z-index:9999;width:0;transition:width .1s}}
.btp{{position:fixed;bottom:24px;right:24px;width:40px;height:40px;border-radius:50%;background:#58a6ff;color:#fff;border:none;cursor:pointer;font-size:18px;opacity:0;transform:translateY(20px);transition:opacity .3s,transform .3s;z-index:99;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(88,166,255,0.3)}}
.btp.visible{{opacity:1;transform:translateY(0)}}
.btp:hover{{background:#79b8ff;transform:translateY(-2px)}}
html{{scroll-behavior:smooth}}
</style>
</head>
<body>
<div class="progress-bar" id="progressBar"></div>
<script>window.addEventListener('scroll',function(){{var h=document.documentElement.scrollHeight-document.documentElement.clientHeight;var p=h>0?Math.min(100,(window.scrollY/h)*100):0;document.getElementById('progressBar').style.width=p+'%'}});</script>
<h1>AI工具详情 · 共{len(tools)}款</h1>
{cat_links}
<div class="back"><a href="/">返回AI工具箱首页</a></div>
<footer><p>AI工具箱 2026 · <a href="/">返回首页</a> · <a href="/privacy.html">隐私政策</a> · <a href="/about.html">关于</a></p></footer>
<button class="btp" id="btp" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="回到顶部">↑</button>
<script>window.addEventListener('scroll',function(){{document.getElementById('btp').classList.toggle('visible',window.scrollY>400)}});</script>
</body>
</html>"""

with open(os.path.join(TOOLS_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(idx_html)

print(f"Generated {count} tool detail pages + index page")
