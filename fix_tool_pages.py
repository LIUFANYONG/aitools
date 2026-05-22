"""Quick fix: replace broken JSON-LD block in generate_tool_pages.py"""
with open('generate_tool_pages.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add ld_json variable before the idx_html f-string
old_start = 'idx_html = f"""<!DOCTYPE html>'
ld_pre = '''ld_json = """{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "AI工具详情列表",
  "description": "收录110款AI工具详细信息",
  "url": "https://aitools-khaki.vercel.app/tools/"
}"
'''

content = content.replace(old_start, ld_pre + '\n' + old_start)

# Replace broken JSON-LD script block with variable reference
old_ld = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "AI工具详情列表",
  "description": "收录110款AI工具详细信息",
  "url": "https://aitools-khaki.vercel.app/tools/"
}
</script>'''

new_ld = '<script type="application/ld+json">\n{ld_json}\n</script>'

if old_ld in content:
    content = content.replace(old_ld, new_ld)
    print("Replaced JSON-LD block")
else:
    print("Old JSON-LD block not found - checking content...")
    if '收录110' in content:
        print("Found '收录110' in content")
    # Try to find the block
    idx = content.find('<script type="application/ld+json">')
    if idx >= 0:
        print(f"Found script tag at {idx}")
        print(repr(content[idx:idx+300]))

with open('generate_tool_pages.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
