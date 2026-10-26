import glob
import re

# 1. Update server.py end_headers with anti-cache headers
with open('server.py', 'r', encoding='utf-8') as f:
    srv = f.read()

old_end = '''    def end_headers(self):
        # Cho phép Cross-Origin Request
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()'''

new_end = '''    def end_headers(self):
        # Cho phép Cross-Origin Request
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        # Bắt buộc Cloudflare & Trình duyệt luôn luôn lấy file mới nhất 2.0.0, chống cache cũ
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()'''

if old_end in srv:
    srv = srv.replace(old_end, new_end)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(srv)
    print('[+] Updated server.py anti-cache headers')
else:
    print('[?] old_end not exact match in server.py')

# 2. Update all HTML files: bump all ?v=... to ?v=2.0.0
html_files = glob.glob('*.html') + glob.glob('tin-tuc/*.html')
count = 0
for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace existing ?v=... on css and js
    new_content = re.sub(r'(\.css|\.js)\?v=[^\'\" >]+', r'\1?v=2.0.0', content)
    # Also add ?v=2.0.0 to any css/js links that don't have version
    new_content = re.sub(r'href="((?:css/|\.\./css/)[^"]+\.css)(?!\?v=)"', r'href="\1?v=2.0.0"', new_content)
    new_content = re.sub(r'src="((?:js/|\.\./js/)[^"]+\.js)(?!\?v=)"', r'src="\1?v=2.0.0"', new_content)
    
    if new_content != content:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f'[+] Bumped asset versions to ?v=2.0.0 in {count} HTML files')
