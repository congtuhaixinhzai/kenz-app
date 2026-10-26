import os
import re
import json
import urllib.request
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

venues_raw = [
  {"id": 1, "title": "Karaoke Paris Club 69 Trần Thái Tông", "address": "69 Trần Thái Tông, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/10/1791100689003_755368221161736619_g3193644284611577474_4f219778bf65908f23f7f1e794fb2c47.jpg"},
  {"id": 2, "title": "Karaoke Royal 31-33 Nguyễn Khang", "address": "31-33 Nguyễn Khang, Trung Hòa, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/10/1791100697730_755368221161736619_g3193644284611577474_4b8ae029f604473873426bf690e0c961.jpg"},
  {"id": 3, "title": "Karaoke Raptor - 116 Bùi Thị Xuân", "address": "116 Bùi Thị Xuân, Hai Bà Trưng, Hà Nội", "district": "Hai Bà Trưng", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/09/1788875444502_754326553818318182_g3193644284611577474_ee56184a441e88863f63c814b7e84992.jpg"},
  {"id": 4, "title": "Karaoke T KTV – Dương Nội", "address": "KĐT Dương Nội, Hà Đông, Hà Nội", "district": "Hà Đông", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/1787554198774_753738096180371661_g3193644284611577474_1d670d8a7cba8b1c4b26710b7a8fa15f.jpg"},
  {"id": 5, "title": "New The Wann Quận 1", "address": "Quận 1, TP. Hồ Chí Minh", "district": "TP.HCM", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/08/the-wann-quan-1-2.jpg"},
  {"id": 6, "title": "Karaoke London – Phú Lương", "address": "Phú Lương, Hà Đông, Hà Nội", "district": "Hà Đông", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/07/z8052727859918_f746960d750a9862529d332617f698ca.jpg"},
  {"id": 7, "title": "Karaoke Lucky – 10 Hoà Mã", "address": "10 Hoà Mã, Phạm Đình Hổ, Hai Bà Trưng, Hà Nội", "district": "Hai Bà Trưng", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/07/z8061726014900_62243d99411fa741e54911d279cf4414.jpg"},
  {"id": 8, "title": "Karaoke MC QEEN – 29 La Thành", "address": "29 La Thành, Đống Đa, Hà Nội", "district": "Đống Đa", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/07/z8061726023848_1ea2b6ca8cf3fa71f16ebccaf506fc00.jpg"},
  {"id": 9, "title": "Karaoke Titan 244 Võ Chí Công", "address": "244 Võ Chí Công, Xuân La, Tây Hồ, Hà Nội", "district": "Tây Hồ", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6694113334790_aa5986866d9cff4df80a6b7d2dbf88c8.jpg"},
  {"id": 10, "title": "Karaoke The Voice Quan Hoa", "address": "Quan Hoa, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6838579593991_c962b8813d11b2297eb0981997d98ee1.jpg"},
  {"id": 11, "title": "Karaoke Kenz Club 202 Trung Kính", "address": "202 Trung Kính, Yên Hoà, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "isMain": True, "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6838579835405_8f3d61b32d2036c0a87a6d88f6356bc0.jpg"},
  {"id": 12, "title": "Karaoke Tip Top 85G Nguyễn Khang", "address": "85G Nguyễn Khang, Yên Hòa, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6838580060383_5c4b4d6a6c22cb98d933c09f3e440fe3.jpg"},
  {"id": 13, "title": "Karaoke 85 Hoàng Gia - Cầu Giấy", "address": "85 Nguyễn Khang, Yên Hòa, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6838580303256_c2c4bfce866a2cbddb83df3e4811a43a.jpg"},
  {"id": 14, "title": "Karaoke F5 Plus - 5 Trần Duy Hưng", "address": "5 Trần Duy Hưng, Trung Hòa, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6838580605452_93d1b702ec4c979601d51c337a8bcfef.jpg"},
  {"id": 15, "title": "Karaoke V-POP 50 Trung Hòa", "address": "50 Trung Hòa, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6838581113253_fdcf52d5e77ce093153574c87cb73f9f.jpg"},
  {"id": 16, "title": "Karaoke Level 36 Vũ Trọng Khánh", "address": "36 Vũ Trọng Khánh, Mộ Lao, Hà Đông, Hà Nội", "district": "Hà Đông", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6838581394032_dbd89617ad226716a4ce3d052a0a2df3.jpg"},
  {"id": 17, "title": "Karaoke Let's Sing 89 Tân Triều", "address": "89 Tân Triều, Thanh Trì, Hà Nội", "district": "Thanh Trì", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6838581652029_ddfe9a667b9fe7b9aa1ef78f8cb47817.jpg"},
  {"id": 18, "title": "Karaoke F5 Plus - 66 Tố Hữu", "address": "66 Tố Hữu, Vạn Phúc, Hà Đông, Hà Nội", "district": "Hà Đông", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6838582035076_cebf29a6e60b138e68e427d14d23253b.jpg"},
  {"id": 19, "title": "Karaoke X-MEN Club 402 Đê La Thành", "address": "402 Đê La Thành, Ô Chợ Dừa, Đống Đa, Hà Nội", "district": "Đống Đa", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6838582770079_68d1844bdf9891823eb526a053cbf536.jpg"},
  {"id": 20, "title": "Karaoke LONDON 20 Lê Trọng Tấn", "address": "20 Lê Trọng Tấn, La Khê, Hà Đông, Hà Nội", "district": "Hà Đông", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6847658070875_ca38ce2a106e22ba8a91da93f2f8b548.jpg"},
  {"id": 21, "title": "Karaoke SING KTV 66 Tố Hữu", "address": "66 Tố Hữu, Vạn Phúc, Hà Đông, Hà Nội", "district": "Hà Đông", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z6847658375369_c5a1762cba3cefe18c1b52aa9b80613e.jpg"},
  {"id": 22, "title": "Karaoke AMIGO 233 Lê Đức Thọ", "address": "233 Lê Đức Thọ, Mỹ Đình, Nam Từ Liêm, Hà Nội", "district": "Nam Từ Liêm", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/08/z6886005407875_18bfe0d4567c2966c406ee9a4f4ef1ce.jpg"},
  {"id": 23, "title": "Karaoke GRAND 300 Xã Đàn", "address": "300 Xã Đàn, Phương Liên, Đống Đa, Hà Nội", "district": "Đống Đa", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/08/z6886012547209_6f7f457ffad113d09a01664d603a1158.jpg"},
  {"id": 24, "title": "Karaoke S 69 Trần Thái Tông", "address": "69 Trần Thái Tông, Dịch Vọng Hậu, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/08/z6895440299210_4914fb0c9ff81ffc1c1f6c44933fa1dc.jpg"},
  {"id": 25, "title": "Karaoke V-Party 5 Hồ Đắc Di", "address": "5 Hồ Đắc Di, Nam Đồng, Đống Đa, Hà Nội", "district": "Đống Đa", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/10/z7080328084246_a10d3221fa0c22629b39d1b09b0bfa51.jpg"},
  {"id": 26, "title": "Karaoke Royal Club 97 Cầu Giấy", "address": "97 Cầu Giấy, Quan Hoa, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/10/z7082887867627_0d481f34bc4ea9638c035f29c2930263.jpg"},
  {"id": 27, "title": "Karaoke Thượng Hải KTV 229 Tây Sơn", "address": "229 Tây Sơn, Ngã Tư Sở, Đống Đa, Hà Nội", "district": "Đống Đa", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2025/07/z7755036194685_3d30b6df9f99378411b023f03b57ce6d.jpg"},
  {"id": 28, "title": "Karaoke Sing KTV 65 Thái Thịnh", "address": "65 Thái Thịnh, Thịnh Quang, Đống Đa, Hà Nội", "district": "Đống Đa", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/04/2436542073243828945_1744388836.jpg"},
  {"id": 29, "title": "Karaoke LONDON 28 Thành Thái", "address": "28 Thành Thái, Dịch Vọng, Cầu Giấy, Hà Nội", "district": "Cầu Giấy", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/04/2507723079099372337_1744389025.jpg"},
  {"id": 30, "title": "Karaoke A999 - 51 Nguyễn Hoàng", "address": "51 Nguyễn Hoàng, Mỹ Đình, Nam Từ Liêm, Hà Nội", "district": "Nam Từ Liêm", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/04/z7755277198259_5b0b467fba9ad18536beea6a82746c82.jpg"},
  {"id": 31, "title": "Karaoke V-MAX - 402 Đê La Thành", "address": "402 Đê La Thành, Ô Chợ Dừa, Đống Đa, Hà Nội", "district": "Đống Đa", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/07/z8061755801887_334547923485c986925925a3df69d3e8.jpg"},
  {"id": 32, "title": "A9 Club - 37 Nguyễn Hoàng", "address": "37 Nguyễn Hoàng, Mỹ Đình, Nam Từ Liêm, Hà Nội", "district": "Nam Từ Liêm", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/05/hinh-anh-ve-empire-club.jpg"},
  {"id": 33, "title": "A PLUS CLUB 78 Yên Phụ", "address": "78 Yên Phụ, Nguyễn Trung Trực, Ba Đình, Hà Nội", "district": "Ba Đình", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/04/z7762787747072_31d8e12470fcf14a1c5d0e2343fe3041.jpg"},
  {"id": 34, "title": "VOLUME CLUB - Xuân Phương", "address": "KĐT Hateco Apollo, Xuân Phương, Nam Từ Liêm, Hà Nội", "district": "Nam Từ Liêm", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/05/500862509_604835619325997_8367907572778734006_n.jpg"},
  {"id": 35, "title": "Karaoke Matrix 124-126 Đường 9A", "address": "124-126 Đường 9A, Khu Trung Sơn, TP.HCM", "district": "TP.HCM", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/05/1-1751903211.jpg"},
  {"id": 36, "title": "Bar Empire Club Quận 1", "address": "Quận 1, TP. Hồ Chí Minh", "district": "TP.HCM", "image": "https://karaokektvhanoi.vn/wp-content/uploads/2026/05/z4666977661079_2f20e4eb1e6df95e4e756e4c27a20c3a.jpg"}
]

os.makedirs("assets/images/ktv", exist_ok=True)
downloaded = []

headers = {"User-Agent": "Mozilla/5.0"}

for v in venues_raw:
    img_url = v["image"]
    ext = os.path.splitext(img_url.split("?")[0])[1] or ".jpg"
    filename = f"ktv-{v['id']:02d}{ext}"
    local_path = os.path.join("assets", "images", "ktv", filename)
    rel_path = f"assets/images/ktv/{filename}"
    
    try:
        req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            with open(local_path, "wb") as f_out:
                f_out.write(resp.read())
        print(f"Downloaded: {v['title']} -> {rel_path}")
        v["local_image"] = rel_path
    except Exception as e:
        print(f"Failed {v['title']}: {e}")
        v["local_image"] = img_url

with open("js/ktv-data.js", "w", encoding="utf-8") as f:
    f.write("// DỮ LIỆU TOÀN BỘ 36 QUÁN KARAOKE KTV HÀ NỘI\n")
    f.write("const KTV_VENUES = " + json.dumps(venues_raw, ensure_ascii=False, indent=2) + ";\n")
    f.write("if (typeof window !== 'undefined') { window.KTV_VENUES = KTV_VENUES; }\n")

print("Created js/ktv-data.js successfully!")
