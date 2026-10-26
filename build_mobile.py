import os
import shutil
import glob
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def build_mobile_dist():
    dist_dir = 'www'
    print(f"[*] Bắt đầu đóng gói thư mục mobile app: '{dist_dir}'...")

    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir, exist_ok=True)

    # 1. Copy thư mục static
    dirs_to_copy = ['css', 'js', 'assets', 'tin-tuc']
    for d in dirs_to_copy:
        if os.path.exists(d):
            dest = os.path.join(dist_dir, d)
            shutil.copytree(d, dest)
            print(f" -> Đã sao chép thư mục: {d}/")

    # 2. Copy toàn bộ file HTML
    html_files = glob.glob("*.html")
    for f in html_files:
        shutil.copy2(f, os.path.join(dist_dir, f))
    print(f" -> Đã sao chép {len(html_files)} file HTML")

    # 3. Copy các file config & PWA
    single_files = [
        'config.js',
        'manifest.webmanifest',
        'manifest.json',
        'sw.js',
        'favicon.ico',
        'reviews.json',
        'promotions.json',
        'venue_visibility.json'
    ]
    for f in single_files:
        if os.path.exists(f):
            shutil.copy2(f, os.path.join(dist_dir, f))
            print(f" -> Đã sao chép: {f}")

    # Đếm tổng dung lượng www
    total_size = 0
    file_count = 0
    for root, _, files in os.walk(dist_dir):
        for f in files:
            fp = os.path.join(root, f)
            total_size += os.path.getsize(fp)
            file_count += 1

    size_mb = total_size / (1024 * 1024)
    print(f"\n[OK] Đóng gói thành công '{dist_dir}' cho Mobile App!")
    print(f" -> Tổng số file: {file_count}")
    print(f" -> Dung lượng ứng dụng: {size_mb:.2f} MB")
    print(f" -> Sẵn sàng nạp vào Capacitor (Android/iOS) hoặc chạy Offline!")

if __name__ == '__main__':
    build_mobile_dist()
