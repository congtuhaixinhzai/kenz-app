import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

html_files = []
for root, dirs, files in os.walk('.'):
    # skip node_modules or .git if any
    if '.git' in root or '.gemini' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.normpath(os.path.join(root, f)))

print(f"Total HTML files found: {len(html_files)}")

missing_i18n = []
missing_btn = []
has_i18n_count = 0
has_btn_count = 0

for hf in sorted(html_files):
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_i18n = 'i18n.js' in content
    has_btn = ('id="lang-btn"' in content) or ("id='lang-btn'" in content)

    if has_i18n:
        has_i18n_count += 1
    else:
        missing_i18n.append(hf)
        
    if has_btn:
        has_btn_count += 1
    else:
        missing_btn.append(hf)

print(f"Pages with i18n.js: {has_i18n_count} / {len(html_files)}")
print(f"Pages with lang-btn: {has_btn_count} / {len(html_files)}")

if missing_i18n:
    print("MISSING i18n.js:")
    for m in missing_i18n:
        print("  -", m)

if missing_btn:
    print("MISSING lang-btn:")
    for m in missing_btn:
        print("  -", m)
