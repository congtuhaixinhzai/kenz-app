import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Home_Family\.gemini\antigravity-ide\brain\9b2e1799-dcaa-4422-8086-69cf903d52c4\.system_generated\steps\397\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Navigation Menu on karaokektvhanoi.vn
print("=== NAVIGATION MENU ON ORIGINAL SITE ===")
nav_matches = re.findall(r'<li[^>]*class="[^"]*menu-item[^"]*"[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', text)
print(f"Total menu items: {len(nav_matches)}")
for u, t in nav_matches:
    print(f"  - {t.strip()} -> {u.strip()}")

# 2. Main Page Content Structure
print("\n=== PAGE CONTENT STRUCTURE ===")
# Headings
headings = re.findall(r'<(h[1-6])[^>]*>(.*?)</\1>', text, re.DOTALL)
print(f"Total headings: {len(headings)}")
for tag, h in headings:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    if clean:
        print(f"  [{tag}] {clean}")

# 3. Contact information on page
print("\n=== CONTACT INFO FOUND ===")
hotlines = re.findall(r'(?:0\d{9,10}|tel:\+?\d+)', text)
print("Hotlines:", set(hotlines))

# 4. Any buttons or interactive elements
print("\n=== BUTTONS / CALLS TO ACTION ===")
buttons = re.findall(r'<(?:a|button)[^>]*class="[^"]*(?:btn|button)[^"]*"[^>]*>(.*?)</(?:a|button)>', text, re.DOTALL)
print(f"Total buttons: {len(buttons)}")
for b in set([re.sub(r'<[^>]+>', '', b).strip() for b in buttons if b.strip()]):
    print(f"  - Button text: {b}")
