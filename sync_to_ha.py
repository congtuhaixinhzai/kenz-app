import os
import shutil
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r"c:\Users\Home_Family\Desktop\WEB"
addon_dest = r"\\192.168.1.245\addons\kenz_web_80"
www_dest = r"\\192.168.1.245\config\www\kenz"

files_to_copy = [
    "index.html",
    "ktv-hanoi.html",
    "karaoke-ktv-ha-noi.html",
    "admin.html",
    "config.js",
    "server.py",
    "reviews.json",
    "ktv_venues_full.json"
]

dirs_to_copy = [
    ("css", "css"),
    ("js", "js"),
    ("assets", "assets"),
    ("tin-tuc", "tin-tuc"),
    ("zalo_bot", "zalo_bot")
]

def sync_to(target_name, dest_root):
    print(f"\n--- SYNCING TO {target_name}: {dest_root} ---")
    if not os.path.exists(dest_root):
        print(f"[!] Target path does not exist: {dest_root}")
        return False
        
    # Copy all .html, .js, .json, .py files from root
    for item in os.listdir(src_dir):
        s_item = os.path.join(src_dir, item)
        if os.path.isfile(s_item):
            ext = os.path.splitext(item)[1].lower()
            if ext in ['.html', '.js', '.json', '.py', '.xml', '.txt', '.ico', '.png'] or item in ['config.yaml', 'Dockerfile']:
                d_file = os.path.join(dest_root, item)
                shutil.copy2(s_item, d_file)
                # print(f"  [+] Copied file: {item}")
    print(f"  [+] Copied all HTML, SEO, XML & config files to {target_name}!")
            
    for s_sub, d_sub in dirs_to_copy:
        s_folder = os.path.join(src_dir, s_sub)
        d_folder = os.path.join(dest_root, d_sub)
        if os.path.exists(s_folder):
            shutil.copytree(s_folder, d_folder, dirs_exist_ok=True)
            print(f"  [+] Copied dir: {s_sub}/ -> {d_sub}/")
            
    return True

# 1. Sync to Addon
sync_to("ADD-ON (kenz_web_80)", addon_dest)

# 2. Update config.yaml in addon to 2.0.0
config_yaml_path = os.path.join(addon_dest, "config.yaml")
if os.path.exists(config_yaml_path):
    with open(config_yaml_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'version:\s*"[^"]+"', 'version: "2.0.0"', content)
    with open(config_yaml_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  [+] Bumped add-on version to 2.0.0 in config.yaml")

# 3. Sync to www/kenz
sync_to("WWW (/local/kenz/)", www_dest)

print("\nAll files and assets synced successfully to Home Assistant!")
