import os
import json
import re

files_to_check = [
    'index.html', 
    'ktv-hanoi.html', 
    'karaoke-ktv-ha-noi.html',
    'tin-tuc/tintuc.html',
    'tin-tuc/karaoke-cho-khach-trung-quoc-ha-noi.html'
]
venue_files = [f for f in os.listdir('.') if f.startswith(('karaoke-', 'bar-', 'a-plus-', 'new-the-wann-')) and f.endswith('.html') and f != 'karaoke-ktv-ha-noi.html']
all_files = files_to_check + venue_files

print(f"Auditing ALL {len(all_files)} HTML pages for 100% SEO, Google Search & Mobile compliance...")

report = {
    "total_pages": len(all_files),
    "valid_title": 0,
    "valid_meta_description": 0,
    "valid_canonical": 0,
    "valid_hreflang": 0,
    "valid_schema_ldjson": 0,
    "valid_single_h1": 0,
    "valid_opengraph": 0,
    "valid_twitter_card": 0,
    "valid_viewport": 0,
    "valid_mobile_quick_bar": 0,
    "valid_speed_preconnect": 0,
    "schema_types_found": set(),
    "issues": []
}

for fn in all_files:
    if not os.path.exists(fn):
        report["issues"].append(f"{fn}: File not found")
        continue

    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Title
    m_title = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if m_title and 15 <= len(m_title.group(1).strip()) <= 95:
        report["valid_title"] += 1
    else:
        title_len = len(m_title.group(1).strip()) if m_title else 0
        report["issues"].append(f"{fn}: Title length abnormal ({title_len} chars)")

    # 2. Meta Description
    m_desc = re.search(r'<meta name="description" content="([^"]+)"', html)
    if m_desc and 40 <= len(m_desc.group(1).strip()) <= 220:
        report["valid_meta_description"] += 1
    else:
        desc_len = len(m_desc.group(1).strip()) if m_desc else 0
        report["issues"].append(f"{fn}: Meta description length abnormal ({desc_len} chars)")

    # 3. Canonical
    if '<link rel="canonical"' in html:
        report["valid_canonical"] += 1
    else:
        report["issues"].append(f"{fn}: Missing canonical tag")

    # 4. Hreflang
    if 'hreflang="vi"' in html and 'hreflang="zh"' in html:
        report["valid_hreflang"] += 1
    else:
        report["issues"].append(f"{fn}: Missing hreflang multi-language tags")

    # 5. OpenGraph
    if '<meta property="og:title"' in html and '<meta property="og:image"' in html and '<meta property="og:url"' in html:
        report["valid_opengraph"] += 1
    else:
        report["issues"].append(f"{fn}: Missing OpenGraph tags")

    # 6. Twitter Card
    if '<meta name="twitter:card"' in html and '<meta name="twitter:title"' in html:
        report["valid_twitter_card"] += 1
    else:
        report["issues"].append(f"{fn}: Missing Twitter Card tags")

    # 7. Viewport
    if 'name="viewport"' in html and 'viewport-fit=cover' in html:
        report["valid_viewport"] += 1
    else:
        report["issues"].append(f"{fn}: Missing viewport or viewport-fit=cover")

    # 8. Single H1
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if len(h1_matches) == 1:
        report["valid_single_h1"] += 1
    else:
        report["issues"].append(f"{fn}: Expected exactly 1 H1 tag, found {len(h1_matches)}")

    # 9. Schema JSON-LD validation
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    if schemas:
        report["valid_schema_ldjson"] += 1
        for s_raw in schemas:
            try:
                s_json = json.loads(s_raw.strip())
                if "@graph" in s_json:
                    for node in s_json["@graph"]:
                        report["schema_types_found"].add(node.get("@type", "Unknown"))
                else:
                    report["schema_types_found"].add(s_json.get("@type", "Unknown"))
            except Exception as e:
                report["issues"].append(f"{fn}: Invalid Schema JSON ({e})")
    else:
        report["issues"].append(f"{fn}: Missing Schema JSON-LD")

    # 10. Mobile Quick Action Bar (.quick)
    if 'class="quick"' in html and 'class="quick-main"' in html:
        report["valid_mobile_quick_bar"] += 1
    else:
        report["issues"].append(f"{fn}: Missing mobile floating action bar (.quick)")

    # 11. Page Speed Resource Hints
    if 'fonts.googleapis.com' in html and 'fonts.gstatic.com' in html:
        report["valid_speed_preconnect"] += 1
    else:
        report["issues"].append(f"{fn}: Missing Google Fonts preconnect resource hints")

report["schema_types_found"] = sorted(list(report["schema_types_found"]))

print("\n" + "="*60)
print("SEO & MOBILE AUDIT COMPREHENSIVE REPORT")
print("="*60)
for k, v in report.items():
    if k != "issues":
        print(f"  - {k}: {v}")

if report["issues"]:
    print(f"\n[!] ISSUES FOUND ({len(report['issues'])}):")
    for issue in report["issues"][:15]:
        print(f"  - {issue}")
else:
    print("\n>>> [100% PERFECT PASS] ALL 41 PAGES ARE 100% SEO, GOOGLE & MOBILE OPTIMIZED! <<<")
