import json
from datetime import datetime

with open('ktv_venues_full.json', 'r', encoding='utf-8') as f:
    venues = json.load(f)

today_str = datetime.now().strftime("%Y-%m-%d")

urls = [
    {
        "loc": "https://karaokekenz.com/",
        "priority": "1.0",
        "changefreq": "daily"
    },
    {
        "loc": "https://karaokekenz.com/karaoke-kenz-club-202-trung-knh.html",
        "priority": "0.98",
        "changefreq": "daily"
    },
    {
        "loc": "https://karaokekenz.com/karaoke-kenz-club-202-trung-kinh.html",
        "priority": "0.95",
        "changefreq": "daily"
    },
    {
        "loc": "https://karaokekenz.com/ktv-hanoi.html",
        "priority": "0.95",
        "changefreq": "daily"
    },
    {
        "loc": "https://karaokekenz.com/karaoke-ktv-ha-noi.html",
        "priority": "0.90",
        "changefreq": "daily"
    },
    {
        "loc": "https://karaokekenz.com/tin-tuc/tintuc.html",
        "priority": "0.75",
        "changefreq": "weekly"
    },
    {
        "loc": "https://karaokekenz.com/tin-tuc/karaoke-cho-khach-trung-quoc-ha-noi.html",
        "priority": "0.70",
        "changefreq": "monthly"
    }
]

PRIORITY_IDS = [26, 27, 12, 29, 24]

for v in venues:
    if v['id'] == 11:
        continue # Already added as top priority
    is_prio = v['id'] in PRIORITY_IDS
    urls.append({
        "loc": f"https://karaokekenz.com/{v['slug']}.html",
        "priority": "0.90" if is_prio else "0.80",
        "changefreq": "weekly"
    })

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]

for u in urls:
    xml_lines.append(f"""  <url>
    <loc>{u['loc']}</loc>
    <lastmod>{today_str}</lastmod>
    <changefreq>{u['changefreq']}</changefreq>
    <priority>{u['priority']}</priority>
  </url>""")

xml_lines.append('</urlset>')

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write("\n".join(xml_lines))
print(f"Generated sitemap.xml with {len(urls)} URLs!")

robots_txt = """User-agent: *
Allow: /
Disallow: /admin.html
Disallow: /api/

Sitemap: https://karaokekenz.com/sitemap.xml
"""

with open('robots.txt', 'w', encoding='utf-8') as f:
    f.write(robots_txt)
print("Generated robots.txt successfully!")
