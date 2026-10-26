import os
import base64
from PIL import Image

src_path = 'assets/kenz-logo.png'
img = Image.open(src_path)

# Ensure RGBA
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# 1. Generate favicon.ico at root and in assets
# Multi-size ico: 16, 32, 48, 64
img.save('favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
img.save('assets/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("Created favicon.ico & assets/favicon.ico")

# 2. Generate PNG favicons
sizes = {
    'assets/favicon-16x16.png': (16, 16),
    'assets/favicon-32x32.png': (32, 32),
    'assets/favicon-48x48.png': (48, 48),  # Multiple of 48 for Google
    'assets/favicon-96x96.png': (96, 96),  # Multiple of 48 for Google
    'assets/favicon-144x144.png': (144, 144),  # Multiple of 48 for Google
    'assets/favicon-192x192.png': (192, 192),  # Multiple of 48 for Google
    'assets/apple-touch-icon.png': (180, 180),
    'assets/favicon.png': (192, 192),
    'assets/logo.png': (320, 320),
}

for path, size in sizes.items():
    resized = img.resize(size, Image.Resampling.LANCZOS)
    resized.save(path, format='PNG', optimize=True)
    print(f"Created {path} ({size[0]}x{size[1]})")

# 3. Create SVG that embeds the 192x192 PNG as base64 so assets/favicon.svg displays the new logo
with open('assets/favicon-192x192.png', 'rb') as f:
    b64_png = base64.b64encode(f.read()).decode('utf-8')

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 192 192" width="192" height="192">
  <image width="192" height="192" href="data:image/png;base64,{b64_png}" />
</svg>
'''

with open('assets/favicon.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)
print("Updated assets/favicon.svg with embedded base64 of new logo!")

print("All icons successfully generated!")
