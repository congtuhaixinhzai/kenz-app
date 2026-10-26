import os
import json
import re
import sys
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

with open('ktv_venues_full.json', 'r', encoding='utf-8') as f:
    raw_venues = json.load(f)

# =============================================================================
# THỨ TỰ ƯU TIÊN ĐẶC BIỆT THEO YÊU CẦU:
# 1. ID 11: Karaoke Kenz Club 202 Trung Kính (👑 QUÁN CHÍNH CHỦ - LUÔN LUÔN TOP 1)
# 2. ID 26: Karaoke Royal Club 97 Cầu Giấy (⭐ TOP ƯU TIÊN 2)
# 3. ID 27: Karaoke Thượng Hải KTV 229 Tây Sơn (⭐ TOP ƯU TIÊN 3)
# 4. ID 12: Karaoke Tip Top 85G Nguyễn Khang (⭐ TOP ƯU TIÊN 4)
# 5. ID 29: Karaoke LONDON 28 Thành Thái (⭐ TOP ƯU TIÊN 5)
# 6. ID 24: Karaoke S 69 Trần Thái Tông (⭐ TOP ƯU TIÊN 6)
# =============================================================================
PRIORITY_ORDER = [11, 26, 27, 12, 29, 24]
venue_map = {v['id']: v for v in raw_venues}
venues = [venue_map[vid] for vid in PRIORITY_ORDER if vid in venue_map] + [v for v in raw_venues if v['id'] not in PRIORITY_ORDER]

# Cập nhật vĩnh viễn file ktv_venues_full.json theo đúng thứ tự ưu tiên
with open('ktv_venues_full.json', 'w', encoding='utf-8') as f:
    json.dump(venues, f, ensure_ascii=False, indent=2)
print("0. Permanently updated ktv_venues_full.json with prioritized order!")

# =============================================================================
# CẤU HÌNH CÁC QUẬN ĐANG HOẠT ĐỘNG (ACTIVE DISTRICTS)
# Tạm thời ẩn Hà Đông, Hai Bà Trưng, HCM, Nam Từ Liêm, Tây Hồ... CHỈ ĐỂ CẦU GIẤY VS ĐỐNG ĐA
# =============================================================================
ACTIVE_DISTRICTS = ['Cầu Giấy', 'Đống Đa']
active_venues = [v for v in venues if v.get('district') in ACTIVE_DISTRICTS]
print(f"-> Active venues in Cầu Giấy & Đống Đa: {len(active_venues)} quán (Đã tạm ẩn các quận khác)")

# 1. GENERATE js/ktv-data.js
js_content = """// =============================================================================
// DỮ LIỆU HỆ THỐNG QUÁN KARAOKE KTV ĐANG HOẠT ĐỘNG (CẦU GIẤY & ĐỐNG ĐA)
// =============================================================================
var KTV_VENUES = """ + json.dumps(active_venues, ensure_ascii=False, indent=2) + """;
var KTV_ALL_VENUES = """ + json.dumps(venues, ensure_ascii=False, indent=2) + """;
if (typeof window !== 'undefined') {
  window.KTV_VENUES = KTV_VENUES;
  window.KTV_ALL_VENUES = KTV_ALL_VENUES;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { KTV_VENUES, KTV_ALL_VENUES };
}
"""

with open('js/ktv-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("1. Updated js/ktv-data.js successfully!")

# Build Mega Dropdown HTML (Chỉ hiển thị Cầu Giấy & Đống Đa)
mega_dropdown_html = """
        <div class="nav-item-dropdown">
          <a href="ktv-hanoi.html" class="nav-ktv-highlight on" aria-current="page">
            <span class="badge-hot">HOT</span>
            <span>KTV HÀ NỘI</span>
            <svg class="dropdown-arrow" width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>
          </a>
          <div class="ktv-dropdown-menu">
            <div class="ktv-dropdown-head">
              <span class="title">👑 HỆ THỐNG QUÁN KARAOKE KTV VIP (CẦU GIẤY &amp; ĐỐNG ĐA)</span>
              <a href="ktv-hanoi.html" class="view-all">Xem tất cả 21 cơ sở →</a>
            </div>
            <div class="ktv-dropdown-grid">
              <div class="ktv-dropdown-col">
                <div class="col-title">📍 Cầu Giấy (Ưu tiên hàng đầu)</div>
                <a href="karaoke-kenz-club-202-trung-knh.html" class="dropdown-link highlight" style="color:#ffd166;font-weight:800">👑 Kenz Club 202 Trung Kính (Chính Chủ)</a>
                <a href="karaoke-royal-club-97-cu-giy.html" class="dropdown-link highlight" style="color:#ff758c;font-weight:700">⭐ Royal Club 97 Cầu Giấy</a>
                <a href="karaoke-tip-top-85g-nguyn-khang.html" class="dropdown-link highlight" style="color:#ff758c;font-weight:700">⭐ Tip Top 85G Nguyễn Khang</a>
                <a href="karaoke-london-28-thanh-thai.html" class="dropdown-link highlight" style="color:#ff758c;font-weight:700">⭐ LONDON 28 Thành Thái</a>
                <a href="karaoke-s-69-trn-thi-tng.html" class="dropdown-link highlight" style="color:#ff758c;font-weight:700">⭐ Karaoke S 69 Trần Thái</a>
                <a href="karaoke-paris-club-69-tran-thai-tong.html" class="dropdown-link">Paris Club 69 Trần Thái Tông</a>
                <a href="karaoke-summit-64-tran-thai-tong.html" class="dropdown-link">Summit 64 Trần Thái Tông</a>
              </div>
              <div class="ktv-dropdown-col">
                <div class="col-title">📍 Cầu Giấy (Cơ sở mở rộng)</div>
                <a href="karaoke-zozo-12-tran-kim-xuyen.html" class="dropdown-link">Zozo 12 Trần Kim Xuyến</a>
                <a href="karaoke-flamenco-ktv-16-18-vu-pham-ham.html" class="dropdown-link">Flamenco 16-18 Vũ Phạm Hàm</a>
                <a href="karaoke-royal-31-33-nguyen-khang.html" class="dropdown-link">Royal 31-33 Nguyễn Khang</a>
                <a href="karaoke-85-hong-gia-cu-giy.html" class="dropdown-link">85 Hoàng Gia Cầu Giấy</a>
                <a href="karaoke-the-voice-quan-hoa.html" class="dropdown-link">The Voice Quan Hoa</a>
                <a href="karaoke-f5-plus-5-trn-duy-hng.html" class="dropdown-link">F5 Plus 5 Trần Duy Hưng</a>
                <a href="karaoke-v-pop-50-trung-ha.html" class="dropdown-link">V-POP 50 Trung Hòa</a>
              </div>
              <div class="ktv-dropdown-col">
                <div class="col-title">📍 Đống Đa (Trung tâm giải trí)</div>
                <a href="karaoke-thuong-hai-ktv-229-tay-son.html" class="dropdown-link highlight" style="color:#ff758c;font-weight:700">⭐ Thượng Hải KTV 229 Tây Sơn</a>
                <a href="karaoke-x-men-club-402-la-thnh.html" class="dropdown-link">X-MEN Club 402 Đê La Thành</a>
                <a href="karaoke-grand-300-x-n.html" class="dropdown-link">GRAND 300 Xã Đàn</a>
                <a href="karaoke-v-party-5-h-c-di.html" class="dropdown-link">V-Party 5 Hồ Đắc Di</a>
                <a href="karaoke-sing-ktv-65-thai-thinh.html" class="dropdown-link">Sing KTV 65 Thái Thịnh</a>
                <a href="karaoke-mc-qeen-29-la-thanh.html" class="dropdown-link">MC QEEN 29 La Thành</a>
                <a href="karaoke-v-max-402-de-la-thanh.html" class="dropdown-link">V-MAX 402 Đê La Thành</a>
              </div>
            </div>
            <div class="ktv-dropdown-foot">
              <span>📞 Hotline điều phối 24/7: <b>0342 092 999</b></span>
              <a href="ktv-hanoi.html" style="color:#ffd166;font-weight:700;text-decoration:none">Xem toàn bộ 21 quán Cầu Giấy &amp; Đống Đa →</a>
            </div>
          </div>
        </div>
"""

# Helper to render venue cards for ktv-hanoi.html
def render_static_card(v, is_active=True):
    is_main = v['id'] == 11 or v.get('is_main')
    is_priority = v['id'] in [26, 27, 12, 29, 24] or v.get('is_priority')
    slug_url = f"{v['slug']}.html"

    card_classes = ["ktv-card"]
    if is_main:
        card_classes.append("main-venue")
    elif is_priority:
        card_classes.append("priority-venue")

    star_badge = "⭐ 5.0 VIP"
    if is_main:
        star_badge = "👑 CHÍNH CHỦ"
    elif is_priority:
        star_badge = "🔥 TOP VIP"

    special_pill = ""
    if is_main:
        special_pill = '<span class="ktv-feat-pill" style="color:#ffd166;border-color:#ffd166;font-weight:700">👑 TRỤ SỞ CHÍNH CHỦ KENZ CLUB</span>'
    elif is_priority:
        special_pill = '<span class="ktv-feat-pill" style="color:#ff758c;border-color:rgba(255,117,140,0.6);font-weight:700">🔥 TOP QUÁN VIP ƯU TIÊN</span>'

    display_style = '' if is_active else ' style="display:none"'

    return f"""
      <article class="{' '.join(card_classes)}" data-id="{v['id']}" data-district="{v['district']}"{display_style}>
        <a href="{slug_url}" class="ktv-img-wrap" title="Xem chi tiết {v['name']}">
          <img src="{v['local_image']}" alt="{v['name']} – Phòng Hát Karaoke KTV VIP" loading="lazy" decoding="async" width="400" height="250" onerror="this.onerror=null; this.src='{v['image']}'">
          <span class="ktv-card-badge">📍 {v['district']}</span>
          <span class="ktv-card-stars">{star_badge}</span>
        </a>
        <div class="ktv-body">
          <h3 class="ktv-title"><a href="{slug_url}" style="color:inherit;text-decoration:none">{v['name']}</a></h3>
          <p class="ktv-addr">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
            <span>{v['address'] or v['name']}</span>
          </p>
          <div class="ktv-features">
            <span class="ktv-feat-pill">🔊 Âm thanh cực đã</span>
            <span class="ktv-feat-pill">💡 Phòng VIP LED</span>
            <span class="ktv-feat-pill">⚡ Phục vụ 24/7</span>
            {special_pill}
          </div>
          <div class="ktv-card-footer">
            <a href="{slug_url}" class="btn-detail-venue" title="Xem chi tiết {v['name']}">
              <span>Xem chi tiết</span>
            </a>
            <button class="btn-book-venue" type="button" data-book data-venue="{v['name']}">
              <span>Đặt phòng ngay</span>
            </button>
            <a class="btn-call-venue" href="tel:0342092999" title="Gọi hotline 0342 092 999">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>
            </a>
          </div>
        </div>
      </article>
    """

all_cards_html = "\n".join([render_static_card(v, v in active_venues) for v in venues])

# Generate JSON-LD ItemList for ktv-hanoi.html (Chỉ index các quán đang hoạt động)
item_list_elements = []
for idx, v in enumerate(active_venues, 1):
    item_list_elements.append({
        "@type": "ListItem",
        "position": idx,
        "name": v['name'],
        "url": f"https://karaokekenz.com/{v['slug']}.html",
        "image": f"https://karaokekenz.com/{v['local_image']}"
    })

schema_ktv_hanoi = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "CollectionPage",
            "@id": "https://karaokekenz.com/ktv-hanoi.html#webpage",
            "url": "https://karaokekenz.com/ktv-hanoi.html",
            "name": "Hệ Thống Karaoke KTV Hà Nội – Danh Sách 21+ Quán Hát VIP Cầu Giấy & Đống Đa",
            "description": "Danh sách 21+ Quán Karaoke KTV VIP hàng đầu Hà Nội tại 2 quận trung tâm: Cầu Giấy và Đống Đa. Phòng hát cực đẹp, âm thanh đỉnh cao, giữ phòng 24/7.",
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Trang chủ",
                        "item": "https://karaokekenz.com/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Hệ Thống KTV Hà Nội",
                        "item": "https://karaokekenz.com/ktv-hanoi.html"
                    }
                ]
            }
        },
        {
            "@type": "ItemList",
            "name": "Danh Sách 21+ Quán Karaoke KTV VIP Cầu Giấy & Đống Đa",
            "numberOfItems": len(active_venues),
            "itemListElement": item_list_elements
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Hệ thống Karaoke KTV Hà Nội có những quán nào nổi bật và ưu tiên hàng đầu?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Hệ thống tập trung 21+ cơ sở KTV VIP đẳng cấp nhất tại 2 quận trung tâm Cầu Giấy & Đống Đa, đặc biệt ưu tiên các cơ sở đỉnh cao: 👑 Karaoke Kenz Club 202 Trung Kính (Cơ sở chính chủ độc quyền Cầu Giấy), ⭐ Karaoke Royal Club 97 Cầu Giấy, ⭐ Karaoke Thượng Hải KTV 229 Tây Sơn (Đống Đa), ⭐ Karaoke Tip Top 85G Nguyễn Khang, ⭐ Karaoke LONDON 28 Thành Thái, ⭐ Karaoke S 69 Trần Thái Tông, cùng chuỗi các quán Paris Club, Summit 64 Trần Thái Tông, Zozo 12 Trần Kim Xuyến, Flamenco 16-18 Vũ Phạm Hàm, Royal 31-33, X-MEN Club 402 Đê La Thành, GRAND 300 Xã Đàn, Sing KTV 65 Thái Thịnh..."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Đặt phòng qua hệ thống KTV Hà Nội có mất phí đặt cọc không?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Hoàn toàn MIỄN PHÍ. Quý khách chỉ cần để lại số điện thoại và giờ đến trên website, quản lý sẽ liên hệ xác nhận và giữ phòng VIP đẹp nhất cho quý khách."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Giá phòng hát Karaoke KTV tại Hà Nội khoảng bao nhiêu một giờ?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Giá phòng hát cao cấp tại hệ thống dao động từ 500.000đ – 540.000đ/giờ đối với phòng Deluxe (5–10 khách); từ 620.000đ – 760.000đ/giờ đối với phòng VIP Luxury (10–20 khách); và 850.000đ/giờ đối với phòng Super VIP Party (20–40 khách)."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Quán có hỗ trợ trang trí tiệc sinh nhật hoặc liên hoan công ty không?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Có. Khi đặt phòng trước, quán tặng gói trang trí tiệc sinh nhật (bóng bay, bảng tên), đĩa hoa quả tươi và bánh kem sinh nhật theo yêu cầu."
                    }
                }
            ]
        }
    ]
}

# 2. GENERATE ktv-hanoi.html WITH PRE-RENDERED STATIC CARDS & SCHEMA
ktv_hanoi_content = f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>Hệ Thống 21+ Quán Karaoke KTV Cầu Giấy &amp; Đống Đa VIP – Đặt Phòng Nhanh 24/7</title>
  
  <meta name="description" content="Danh sách 21+ quán Karaoke KTV VIP hàng đầu Cầu Giấy &amp; Đống Đa: Kenz Club 202 Trung Kính, Royal 97, Thượng Hải, Tip Top, Summit 64, Zozo 12. Đặt phòng 24/7: 0342 092 999.">
  <meta name="keywords" content="karaoke ktv hà nội, đặt phòng karaoke hà nội, karaoke cầu giấy, karaoke đống đa, karaoke kenz trung kính, karaoke royal cầu giấy, karaoke thượng hải tây sơn, karaoke tip top, karaoke london thành thái, karaoke s trần thái tông, karaoke summit trần thái tông, karaoke zozo trần kim xuyến, karaoke flamenco vũ phạm hàm">
  <meta name="application-name" content="Karaoke KTV Hà Nội">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="theme-color" content="#100e22">

  <link rel="canonical" href="https://karaokekenz.com/ktv-hanoi.html">
  <link rel="alternate" hreflang="vi" href="https://karaokekenz.com/ktv-hanoi.html">
  <link rel="alternate" hreflang="zh" href="https://karaokekenz.com/ktv-hanoi.html">
  <link rel="alternate" hreflang="x-default" href="https://karaokekenz.com/ktv-hanoi.html">
  <link rel="dns-prefetch" href="https://zalo.me">
  <link rel="icon" type="image/png" sizes="192x192" href="assets/favicon-192x192.png">
  <link rel="icon" type="image/png" sizes="96x96" href="assets/favicon-96x96.png">
  <link rel="icon" type="image/png" sizes="48x48" href="assets/favicon-48x48.png">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="shortcut icon" href="favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Karaoke KTV Hà Nội">
  <meta property="og:url" content="https://karaokekenz.com/ktv-hanoi.html">
  <meta property="og:title" content="Hệ Thống 21+ Quán Karaoke KTV Cầu Giấy & Đống Đa VIP – Đặt Phòng Nhanh 24/7">
  <meta property="og:description" content="Khám phá và đặt phòng tại 21+ quán Karaoke KTV VIP hàng đầu Hà Nội tại Cầu Giấy & Đống Đa. Âm thanh cực đỉnh, phòng hát sang trọng, phục vụ chu đáo 24/7. Hotline: 0342 092 999.">
  <meta property="og:image" content="https://karaokekenz.com/assets/images/ktv/ktv-11.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="800">
  <meta property="og:locale" content="vi_VN">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Hệ Thống 21+ Quán Karaoke KTV Cầu Giấy & Đống Đa VIP">
  <meta name="twitter:description" content="Danh sách 21+ quán Karaoke KTV VIP Hà Nội tại Cầu Giấy & Đống Đa. Đặt phòng 24/7 Hotline: 0342 092 999.">
  <meta name="twitter:image" content="https://karaokekenz.com/assets/images/ktv/ktv-11.jpg">

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {json.dumps(schema_ktv_hanoi, ensure_ascii=False, indent=2)}
  </script>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Stylesheets -->
  <link rel="stylesheet" href="css/base.css?v=1.4.0">
  <link rel="stylesheet" href="css/animations.css?v=1.4.0">
  <link rel="stylesheet" href="css/components.css?v=1.4.0">
  <link rel="stylesheet" href="css/responsive.css?v=1.4.0">
  <link rel="stylesheet" href="css/ktv.css?v=1.4.0">
</head>
<body>

  <!-- ĐÈN NỀN SÂN KHẤU VŨ TRƯỜNG -->
  <div class="bar-lights" aria-hidden="true">
    <i></i><i></i><i></i><i></i>
    <b></b><b></b><b></b>
    <span class="beams"></span>
    <span class="strobe"></span>
  </div>

  <!-- HEADER THANH ĐIỀU HƯỚNG -->
  <header class="top">
    <div class="wrap">
      <a class="brand" href="index.html">
        <img class="brand-logo" src="assets/logo.png" alt="Logo Karaoke Kenz 202 Trung Kính" width="38" height="38">
        <b><i>KARAOKE </i><em>KENZ </em><u>202 TRUNG KÍNH</u></b>
      </a>
      
      <nav class="links">
        <a href="index.html#gioi-thieu">Giới thiệu</a>
        {mega_dropdown_html}
        <a href="index.html#hinh-anh">Hình ảnh</a>
        <a href="index.html#bang-gia">Bảng giá</a>
        <a href="index.html#uu-dai" style="display:none">Ưu đãi</a>
        <a href="index.html#lien-he">Liên hệ</a>
        <a href="index.html#danh-gia">Đánh giá</a>
        <a href="tin-tuc/tintuc.html">Tin tức</a>
      </nav>

      <div class="top-acts">
        <button class="btn btn-ghost btn-sm lang-btn" type="button" id="lang-btn" lang="zh" data-no-i18n aria-label="切换到中文">中文</button>
        <button class="btn btn-hot btn-sm" type="button" data-book data-venue="Karaoke Kenz Club 202 Trung Kính">Đặt phòng ngay</button>
      </div>
    </div>
  </header>

  <!-- MAIN CONTENT -->
  <main>
    <!-- HERO SECTION KTV HÀ NỘI -->
    <section class="ktv-hero">
      <div class="wrap">
        <div class="eyebrow">👑 HỆ THỐNG KARAOKE KTV VIP CẦU GIẤY &amp; ĐỐNG ĐA</div>
        <h1>Hệ Thống <em>Karaoke KTV Hà Nội</em> VIP</h1>
        <p class="sub">
          Chuỗi 21+ phòng hát Karaoke KTV sang trọng, đẳng cấp tại các quận trung tâm Cầu Giấy &amp; Đống Đa, Hà Nội.
          Dàn âm thanh công suất lớn, ánh sáng laser sân khấu hiện đại, phục vụ chu đáo 24/7.
        </p>

        <div class="ktv-stats">
          <div class="ktv-stat-item">
            <span>🏢</span>
            <div><b id="ktv-total-count">21 quán</b> KTV VIP</div>
          </div>
          <div class="ktv-stat-item">
            <span>🎤</span>
            <div><b>500+</b> Phòng hát đẳng cấp</div>
          </div>
          <div class="ktv-stat-item">
            <span>⚡</span>
            <div><b>24/24h</b> Đặt bàn giữ chỗ</div>
          </div>
          <div class="ktv-stat-item">
            <span>📞</span>
            <div>Hotline: <b style="font-size:1.05rem">0342 092 999</b></div>
          </div>
        </div>
      </div>
    </section>

    <!-- BỘ LỌC VÀ TÌM KIẾM CỐ ĐỊNH -->
    <section class="ktv-toolbar">
      <div class="wrap ktv-toolbar-wrap">
        <div class="ktv-search-box">
          <svg class="ktv-search-icon" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
          </svg>
          <input type="text" id="ktv-search" placeholder="Tìm kiếm theo tên quán hoặc tên đường (VD: Kenz Club, Royal Club, Thượng Hải, Tip Top, Thành Thái...)" autocomplete="off">
        </div>

        <div class="ktv-filters">
          <button class="ktv-filter-btn active" type="button" data-district="all">
            <span>🌟 Tất cả</span>
            <span class="count">21</span>
          </button>
          <button class="ktv-filter-btn" type="button" data-district="Cầu Giấy">
            <span>📍 Cầu Giấy</span>
            <span class="count">14</span>
          </button>
          <button class="ktv-filter-btn" type="button" data-district="Đống Đa">
            <span>📍 Đống Đa</span>
            <span class="count">7</span>
          </button>
          <button class="ktv-filter-btn" type="button" data-district="Hà Đông" style="display:none">
            <span>📍 Hà Đông</span>
            <span class="count">0</span>
          </button>
          <button class="ktv-filter-btn" type="button" data-district="Hai Bà Trưng" style="display:none">
            <span>📍 Hai Bà Trưng</span>
            <span class="count">0</span>
          </button>
          <button class="ktv-filter-btn" type="button" data-district="TP. Hồ Chí Minh" style="display:none">
            <span>📍 TP. Hồ Chí Minh</span>
            <span class="count">0</span>
          </button>
          <button class="ktv-filter-btn" type="button" data-district="Nam Từ Liêm" style="display:none">
            <span>📍 Nam Từ Liêm</span>
            <span class="count">0</span>
          </button>
          <button class="ktv-filter-btn" type="button" data-district="Tây Hồ" style="display:none">
            <span>📍 Tây Hồ</span>
            <span class="count">0</span>
          </button>
        </div>
      </div>
    </section>

    <!-- DANH SÁCH 36 QUÁN PRE-RENDER SẴN (INDEX SEO 100% CỰC NHANH) -->
    <section class="wrap">
      <div class="ktv-grid" id="ktv-grid">
        {all_cards_html}
      </div>
    </section>

    <!-- 4 CAM KẾT VÀNG KHI ĐẶT PHÒNG -->
    <section class="ktv-guarantees-section">
      <div class="wrap">
        <div style="text-align:center;max-width:700px;margin:0 auto">
          <div class="eyebrow">💎 ĐẶC QUYỀN KHÁCH HÀNG</div>
          <h2 style="font-size:clamp(1.6rem, 3.5vw, 2.2rem);font-weight:800;color:#fff;margin-top:8px">
            4 Cam Kết Vàng Khi Đặt Phòng Qua KTV Hà Nội
          </h2>
          <p class="muted">Chúng tôi liên kết chặt chẽ với ban quản lý từng cơ sở để bảo đảm trải nghiệm tốt nhất.</p>
        </div>

        <div class="ktv-guarantees-grid">
          <div class="ktv-guarantee-card">
            <span class="ktv-guarantee-icon">👑</span>
            <h3 class="ktv-guarantee-title">Giữ Đúng Phòng VIP Đẹp Nhất</h3>
            <p class="ktv-guarantee-desc">Được xếp phòng theo đúng sở thích (Phòng Party LED, Cổ Điển hoàng gia, hoặc phòng tiệc riêng tư). Không bao giờ lo hết phòng.</p>
          </div>
          <div class="ktv-guarantee-card">
            <span class="ktv-guarantee-icon">💰</span>
            <h3 class="ktv-guarantee-title">Giá Niêm Yết Minh Bạch 100%</h3>
            <p class="ktv-guarantee-desc">Bảng giá giờ hát và đồ uống công khai, không thu phụ phí bất thường. Xuất hoá đơn VAT đầy đủ cho doanh nghiệp.</p>
          </div>
          <div class="ktv-guarantee-card">
            <span class="ktv-guarantee-icon">🎁</span>
            <h3 class="ktv-guarantee-title">Tặng Tiệc Sinh Nhật &amp; Hoa Quả</h3>
            <p class="ktv-guarantee-desc">Tặng ngay đĩa hoa quả tươi đầy đặn. Nhận trang trí tiệc sinh nhật, bóng bay nghệ thuật và tặng bánh kem khi đặt trước.</p>
          </div>
          <div class="ktv-guarantee-card">
            <span class="ktv-guarantee-icon">⚡</span>
            <h3 class="ktv-guarantee-title">Xác Nhận Giữ Chỗ Trong 30s</h3>
            <p class="ktv-guarantee-desc">Hệ thống gửi đơn trực tiếp đến quản lý cơ sở. Nhân viên liên hệ xác nhận và hướng dẫn chỗ đỗ ô tô tận tình.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- HỎI ĐÁP THƯỜNG GẶP (FAQ ACCORDION CHUẨN GOOGLE) -->
    <section class="ktv-faq-section">
      <div class="wrap">
        <div style="text-align:center;max-width:700px;margin:0 auto">
          <div class="eyebrow">❓ HỎI ĐÁP DỊCH VỤ</div>
          <h2 style="font-size:clamp(1.6rem, 3.5vw, 2.2rem);font-weight:800;color:#fff;margin-top:8px">
            Câu Hỏi Thường Gặp Khi Đặt Phòng KTV
          </h2>
        </div>

        <div class="ktv-faq-list">
          <div class="ktv-faq-item active">
            <div class="ktv-faq-q">
              <span>Đặt phòng qua website có mất phí hay phải đặt cọc trước không?</span>
              <svg class="ktv-faq-arrow" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>
            </div>
            <div class="ktv-faq-a">
              Hoàn toàn <strong>KHÔNG MẤT PHÍ</strong> và <strong>KHÔNG CẦN CỌC TRƯỚC</strong> đối với các ngày trong tuần. Quý khách chỉ cần điền họ tên, số điện thoại và giờ dự kiến đến, quán sẽ chủ động giữ phòng và chuẩn bị đón tiếp chu đáo.
            </div>
          </div>

          <div class="ktv-faq-item">
            <div class="ktv-faq-q">
              <span>Giá phòng hát Karaoke KTV tại Hà Nội được tính như thế nào?</span>
              <svg class="ktv-faq-arrow" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>
            </div>
            <div class="ktv-faq-a">
              Bảng giá phòng hát cao cấp: Phòng Deluxe (5–10 khách) từ 500.000đ – 540.000đ/giờ; Phòng VIP Luxury (10–20 khách) từ 620.000đ – 760.000đ/giờ; và Phòng Super VIP Party (20–40 khách) từ 850.000đ/giờ. Menu đồ uống bia, rượu ngoại và hoa quả được niêm yết rõ ràng minh bạch tại từng phòng.
            </div>
          </div>

          <div class="ktv-faq-item">
            <div class="ktv-faq-q">
              <span>Quán có chỗ đỗ ô tô và bảo vệ trông xe không?</span>
              <svg class="ktv-faq-arrow" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>
            </div>
            <div class="ktv-faq-a">
              100% tất cả 36 cơ sở trong hệ thống đều có chỗ đỗ xe máy và bãi đỗ ô tô rộng rãi, có bảo vệ trông giữ xe an toàn 24/24h miễn phí cho khách hàng.
            </div>
          </div>

          <div class="ktv-faq-item">
            <div class="ktv-faq-q">
              <span>Nếu tôi muốn tổ chức sinh nhật hoặc liên hoan công ty thì có ưu đãi gì?</span>
              <svg class="ktv-faq-arrow" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>
            </div>
            <div class="ktv-faq-a">
              Quán tặng gói trang trí tiệc sinh nhật (bóng chữ, phông nền), tặng đĩa hoa quả tươi và bánh kem sinh nhật cho đoàn đặt trước từ 8 người. Quý khách vui lòng ghi chú "Tổ chức sinh nhật" trong phần ghi chú khi gửi đơn đặt.
            </div>
          </div>

          <div class="ktv-faq-item">
            <div class="ktv-faq-q">
              <span>Những quán Karaoke KTV VIP nào được ưu tiên lựa chọn hàng đầu tại Hà Nội?</span>
              <svg class="ktv-faq-arrow" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>
            </div>
            <div class="ktv-faq-a">
              Các cơ sở KTV đỉnh cao luôn được đông đảo khách hàng VIP ưu tiên lựa chọn bao gồm: <strong>👑 Karaoke Kenz Club 202 Trung Kính</strong> (Cơ sở chính chủ đẳng cấp hàng đầu Cầu Giấy), <strong>⭐ Karaoke Royal Club 97 Cầu Giấy</strong>, <strong>⭐ Karaoke Thượng Hải KTV 229 Tây Sơn</strong> (Đống Đa), <strong>⭐ Karaoke Tip Top 85G Nguyễn Khang</strong>, <strong>⭐ Karaoke LONDON 28 Thành Thái</strong>, và <strong>⭐ Karaoke S 69 Trần Thái Tông</strong>. Tất cả đều cam kết âm thanh cực đỉnh, phòng ốc tráng lệ và phục vụ 24/7.
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- FOOTER CHÂN TRANG -->
  <footer class="bot">
    <div class="wrap" style="text-align:center;padding:26px 20px;font-size:0.88rem;color:#9d99be;line-height:1.7">
      <p style="margin-bottom:8px">© 2026 <strong>Karaoke Kenz 202 Trung Kính</strong> &amp; <strong>Hệ Thống 36+ Quán Karaoke KTV Hà Nội</strong>. All rights reserved.</p>
      <p style="font-size:0.82rem;color:#7e7a9b">Hotline điều phối &amp; đặt phòng VIP 24/7: <b style="color:#ffd166">0342 092 999</b> · Cam kết phục vụ chu đáo, chất lượng âm thanh đỉnh cao.</p>
    </div>
  </footer>

  <!-- THANH TIỆN ÍCH MOBILE -->
  <aside class="quick" aria-label="Hỗ trợ nhanh">
    <div class="quick-main">
      <a class="fab-btn" href="tel:0342092999">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>
        <span>Gọi điện</span>
      </a>
      <a class="fab-btn" href="https://zalo.me/0342092999" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.03 2 11c0 2.87 1.5 5.41 3.84 7.03L5 22l4.28-1.43C10.15 20.83 11.05 21 12 21c5.52 0 10-4.03 10-9s-4.48-9-10-9zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>
        <span>Zalo</span>
      </a>
      <button class="fab-btn hot" type="button" data-book data-venue="Karaoke Kenz Club 202 Trung Kính">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zM9 14H7v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2zm-8 4H7v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2z"/></svg>
        <span>Đặt bàn</span>
      </button>
    </div>
  </aside>

  <!-- HỘP THOẠI ĐẶT PHÒNG TRỰC TUYẾN (BOOKING MODAL) -->
  <div class="modal" id="modal" hidden>
    <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="bk-title">
      <button class="x" type="button" id="modal-x" aria-label="Đóng">×</button>

      <!-- BƯỚC 1: FORM NHẬP THÔNG TIN -->
      <div id="bk-step-form">
        <div class="eyebrow">Hệ Thống Karaoke KTV Hà Nội</div>
        <h2 id="bk-title">Thông tin đặt chỗ</h2>
        
        <!-- HIỂN THỊ CƠ SỞ ĐƯỢC CHỌN -->
        <div style="background:rgba(255,183,3,0.12);border:1px solid rgba(255,183,3,0.3);border-radius:12px;padding:10px 14px;margin-bottom:16px;display:flex;align-items:center;gap:10px">
          <span style="font-size:1.2rem">🏢</span>
          <div>
            <div style="font-size:0.75rem;color:#ffd166;text-transform:uppercase;font-weight:700">Cơ sở / Quán đã chọn:</div>
            <div id="f-selected-venue" style="font-size:0.98rem;font-weight:700;color:#fff">Karaoke Kenz Club 202 Trung Kính</div>
          </div>
        </div>

        <form class="bk" id="bk-form" novalidate>
          <input type="hidden" id="f-venue" value="Karaoke Kenz Club 202 Trung Kính">
          
          <div class="two">
            <div class="field">
              <label for="f-name">Họ và tên <i>*</i></label>
              <input id="f-name" autocomplete="name" placeholder="Nhập tên của bạn...">
            </div>
            <div class="field">
              <label for="f-phone">Số điện thoại <i>*</i></label>
              <input id="f-phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="Nhập số điện thoại...">
            </div>
          </div>

          <div class="two">
            <div class="field">
              <label for="f-date">Ngày đặt <i>*</i></label>
              <input id="f-date" type="date">
            </div>
            <div class="field">
              <label for="f-time">Giờ đến <i>*</i></label>
              <input id="f-time" inputmode="numeric" maxlength="5" autocomplete="off" placeholder="VD: 19:30">
            </div>
          </div>

          <!-- Bẫy bot spam -->
          <div class="hp" aria-hidden="true">
            <label>Website <input id="f-website" tabindex="-1" autocomplete="off"></label>
          </div>

          <div class="field">
            <label for="f-note">Ghi chú thêm (nếu có)</label>
            <textarea id="f-note" maxlength="300" placeholder="Yêu cầu trang trí tiệc, số lượng người, phòng VIP…"></textarea>
          </div>

          <p class="err" id="f-err" hidden></p>
          <button class="btn btn-hot" type="submit" id="f-submit">Gửi yêu cầu đặt bàn</button>
        </form>
      </div>

      <!-- BƯỚC 2: MÀN HÌNH XÁC NHẬN MÃ ĐẶT PHÒNG THÀNH CÔNG -->
      <div class="done" id="bk-step-done" hidden>
        <div class="eyebrow">Đã gửi yêu cầu đặt bàn</div>
        <div class="code" id="d-code">KZ-8888</div>
        <p class="muted">Chụp lại mã này. Nhân viên sẽ liên hệ xác nhận trong ít phút.</p>
        <dl id="d-list"></dl>

        <div style="margin-top:20px">
          <a class="btn" id="d-zalo-btn" target="_blank" rel="noopener" style="background:var(--zalo);color:#fff;width:100%;padding:14px 20px;border-radius:12px;font-size:1.02rem;display:inline-flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px -6px rgba(10,104,255,0.7);text-decoration:none;transition:transform .2s">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.03 2 11c0 2.87 1.5 5.41 3.84 7.03L5 22l4.28-1.43C10.15 20.83 11.05 21 12 21c5.52 0 10-4.03 10-9s-4.48-9-10-9zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>
            <span>Nhắn Zalo xác nhận giữ phòng ngay</span>
          </a>
          <small class="muted" style="display:block;margin-top:8px;font-size:0.82rem">Bấm để tự động mở Zalo và gửi mã đặt phòng cho quản lý</small>
        </div>
        
        <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:20px">
          <button class="btn btn-ghost" type="button" id="d-again">Đặt thêm</button>
          <button class="btn btn-hot" type="button" id="d-close">Xong</button>
        </div>
      </div>
    </div>
  </div>

  <!-- TOAST -->
  <div class="toast" id="toast" hidden></div>

  <!-- SCRIPTS -->
  <script src="config.js"></script>
  <script src="js/i18n.js"></script>
  <script src="js/ktv-data.js"></script>
  <script src="js/booking.js"></script>
  <script src="js/promotions.js"></script>
  <script src="js/live-bookings.js"></script>
  <script src="js/ktv-runtime.js"></script>
  <script src="js/app.js"></script>
  <script src="js/ktv-page.js"></script>
</body>
</html>
"""

with open('ktv-hanoi.html', 'w', encoding='utf-8') as f:
    f.write(ktv_hanoi_content)

# Distinct self-referential canonical & hreflang for karaoke-ktv-ha-noi.html
karaoke_ktv_ha_noi_content = ktv_hanoi_content.replace(
    'https://karaokekenz.com/ktv-hanoi.html',
    'https://karaokekenz.com/karaoke-ktv-ha-noi.html'
)
with open('karaoke-ktv-ha-noi.html', 'w', encoding='utf-8') as f:
    f.write(karaoke_ktv_ha_noi_content)
print("2. Generated ktv-hanoi.html & karaoke-ktv-ha-noi.html with SEO & Static Cards!")

def render_venue_map_section(v):
    if v['id'] == 11:
        # KARAOKE KENZ 202 TRUNG KÍNH (CHÍNH CHỦ - TỌA ĐỘ CHÍNH XÁC + STREET VIEW + CỐC CỐC MAP)
        return """
    <!-- VỊ TRÍ & BẢN ĐỒ CHỈ ĐƯỜNG CHI TIẾT -->
    <section class="location-section" style="margin-top:40px;padding-top:30px;border-top:1px solid rgba(255,255,255,0.08)">
      <div style="margin-bottom:20px">
        <div class="eyebrow">📍 VỊ TRÍ &amp; BẢN ĐỒ CHỈ ĐƯỜNG</div>
        <h3 style="font-size:1.45rem;color:#fff;margin-top:6px">Vị Trí &amp; Đường Đi Đến Karaoke Kenz 202 Trung Kính</h3>
        <p class="muted" style="font-size:0.9rem">Mặt đường lớn 202 Trung Kính, Yên Hoà, Cầu Giấy. Bãi đỗ xe ô tô &amp; xe máy rộng rãi, bảo vệ trông coi 24/7 an toàn.</p>
      </div>

      <div class="map-container-grid">
        <div class="map-frame-card">
          <div class="map-card-header">
            <div class="map-card-badge">
              <span class="live-pulse"></span>
              <b>ĐỊNH VỊ CHÍNH XÁC CỬA QUÁN</b>
            </div>
            <span class="coord-badge">21°01'16.9"N 105°47'28.9"E</span>
          </div>
          <div class="map-iframe-wrap">
            <iframe 
              src="https://maps.google.com/maps?q=21.0213604,105.7913589&amp;hl=vi&amp;z=18&amp;output=embed" 
              title="Bản đồ vị trí Karaoke Kenz 202 Trung Kính"
              width="100%" 
              height="100%" 
              style="border:0;" 
              allowfullscreen="" 
              loading="lazy" 
              referrerpolicy="no-referrer-when-downgrade">
            </iframe>
          </div>
        </div>

        <div class="map-info-card">
          <div class="streetview-card">
            <a href="https://www.google.com/maps/@21.0213046,105.7913309,3a,75y,65.68h,107.97t/data=!3m6!1e1!3m4!1sPBcPpnkgdiG6eOuYkfIInQ!2e0!7i16384!8i8192" target="_blank" rel="noopener" class="streetview-img-wrap" title="Bấm xem toàn cảnh 360 độ cửa quán thực tế trên Google Maps">
              <img src="assets/images/cua-quan-kenz-202-trung-kinh.jpg" alt="Mặt tiền thực tế Karaoke Kenz Club 202 Trung Kính lung linh về đêm" loading="lazy" width="960" height="1280">
              <span class="streetview-overlay-badge">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-9l6 4.5-6 4.5z"/></svg>
                <span>Toàn Cảnh Cửa Quán Thực Tế (360°)</span>
              </span>
            </a>
            <small class="streetview-caption">📸 Mặt tiền thực tế sang trọng Karaoke Kenz Club 202 Trung Kính về đêm (Biển LED vàng sang trọng, sảnh đón tiếp sáng rực rỡ, lối vào ô tô thuận tiện)</small>
          </div>

          <div class="location-details">
            <div class="loc-item">
              <span class="loc-icon">🏢</span>
              <div>
                <strong>Địa chỉ đón khách:</strong>
                <p>202 Trung Kính, Phường Yên Hoà, Quận Cầu Giấy, Hà Nội</p>
              </div>
            </div>
            <div class="loc-item">
              <span class="loc-icon">🚗</span>
              <div>
                <strong>Bãi đỗ xe máy &amp; Ô tô:</strong>
                <p>Bãi đỗ xe máy rộng rãi trong nhà, điểm đỗ xe ô tô thoải mái trước cửa, có nhân viên bảo vệ đón tiếp và trông xe miễn phí 24/7.</p>
              </div>
            </div>
            <div class="loc-item">
              <span class="loc-icon">📞</span>
              <div>
                <strong>Hotline hỗ trợ dẫn đường:</strong>
                <p><a href="tel:0342092999" class="loc-phone">0342 092 999</a> <em>(Hỗ trợ 24/24h)</em></p>
              </div>
            </div>
          </div>

          <div class="nav-action-buttons">
            <a href="https://www.google.com/maps/dir/?api=1&amp;destination=21.0213604,105.7913589" target="_blank" rel="noopener" class="btn-nav btn-google-nav">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
              <span>Chỉ Đường Google Maps</span>
            </a>
            <a href="https://map.coccoc.com/map/3766693562931497?route_end_poi_id=3766693562931497&amp;route_vehicle=MOTORCYCLE&amp;zoom=18" target="_blank" rel="noopener" class="btn-nav btn-coccoc-nav">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>
              <span>Chỉ Đường Cốc Cốc Map</span>
            </a>
          </div>
        </div>
      </div>
    </section>
        """
    else:
        # CÁC QUÁN KTV KHÁC TRONG HỆ THỐNG
        search_query = urllib.parse.quote(f"{v['name']} {v['address']}")
        return f"""
    <!-- VỊ TRÍ & BẢN ĐỒ CHỈ ĐƯỜNG -->
    <section class="location-section" style="margin-top:40px;padding-top:30px;border-top:1px solid rgba(255,255,255,0.08)">
      <div style="margin-bottom:20px">
        <div class="eyebrow">📍 VỊ TRÍ &amp; BẢN ĐỒ CHỈ ĐƯỜNG</div>
        <h3 style="font-size:1.45rem;color:#fff;margin-top:6px">Vị Trí &amp; Đường Đi Đến {v['name']}</h3>
        <p class="muted" style="font-size:0.9rem">Toạ lạc tại {v['address']}, Quận {v['district']}, Hà Nội. Có chỗ đỗ xe thuận tiện, phục vụ 24/7.</p>
      </div>

      <div class="map-container-grid">
        <div class="map-frame-card">
          <div class="map-card-header">
            <div class="map-card-badge">
              <span class="live-pulse"></span>
              <b>BẢN ĐỒ VỊ TRÍ CƠ SỞ</b>
            </div>
            <span class="coord-badge">📍 {v['district']}</span>
          </div>
          <div class="map-iframe-wrap">
            <iframe 
              src="https://maps.google.com/maps?q={search_query}&amp;hl=vi&amp;z=16&amp;output=embed" 
              title="Bản đồ vị trí {v['name']}"
              width="100%" 
              height="100%" 
              style="border:0;" 
              allowfullscreen="" 
              loading="lazy" 
              referrerpolicy="no-referrer-when-downgrade">
            </iframe>
          </div>
        </div>

        <div class="map-info-card">
          <div class="location-details">
            <div class="loc-item">
              <span class="loc-icon">🏢</span>
              <div>
                <strong>Địa chỉ đón khách:</strong>
                <p>{v['address']}, Quận {v['district']}, Hà Nội</p>
              </div>
            </div>
            <div class="loc-item">
              <span class="loc-icon">🚗</span>
              <div>
                <strong>Bãi đỗ xe:</strong>
                <p>Có bãi đỗ xe máy và ô tô, có bảo vệ hỗ trợ hướng dẫn đỗ xe miễn phí cho khách hát.</p>
              </div>
            </div>
            <div class="loc-item">
              <span class="loc-icon">📞</span>
              <div>
                <strong>Hotline giữ phòng &amp; dẫn đường:</strong>
                <p><a href="tel:0342092999" class="loc-phone">0342 092 999</a> <em>(Hỗ trợ 24/24h)</em></p>
              </div>
            </div>
          </div>

          <div class="nav-action-buttons">
            <a href="https://www.google.com/maps/dir/?api=1&amp;destination={search_query}" target="_blank" rel="noopener" class="btn-nav btn-google-nav" style="grid-column:1 / -1">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
              <span>Chỉ Đường Bằng Google Maps Đến Quán</span>
            </a>
          </div>
        </div>
      </div>
    </section>
        """

# 3. GENERATE DEDICATED DETAIL TEMPLATE FUNCTION
def generate_detail_page(v):
    is_main = v['id'] == 11 or v.get('is_main')
    slug_url = f"{v['slug']}.html"
    page_url = f"https://karaokekenz.com/{slug_url}"
    img_url = f"https://karaokekenz.com/{v['local_image']}"

    # Build gallery
    gallery_html = ""
    for g_img in v.get('gallery', []):
        gallery_html += f"""
          <div class="ktv-gallery-item" data-lightbox>
            <img src="{g_img}" alt="{v['name']} – Phòng Hát Karaoke VIP Đẹp" loading="lazy" decoding="async" width="400" height="270" onerror="this.onerror=null; this.src='{v['local_image']}';">
          </div>
        """
    if not gallery_html:
        gallery_html = f"""
          <div class="ktv-gallery-item" data-lightbox><img src="{v['local_image']}" alt="{v['name']} phòng VIP" loading="lazy" decoding="async" width="400" height="270"></div>
          <div class="ktv-gallery-item" data-lightbox><img src="assets/images/room-vip-sofa.jpg" alt="{v['name']} phòng sofa da hoàng gia" loading="lazy" decoding="async" width="400" height="270"></div>
          <div class="ktv-gallery-item" data-lightbox><img src="assets/images/room-led-party.jpg" alt="{v['name']} phòng LED party vũ trường" loading="lazy" decoding="async" width="400" height="270"></div>
        """

    # Other venues in same district (Chỉ gợi ý các quán đang hoạt động)
    other_venues = [o for o in active_venues if o['id'] != v['id'] and o['district'] == v['district']][:3]
    if len(other_venues) < 3:
        other_venues = [o for o in active_venues if o['id'] != v['id']][:3]
        
    other_html = ""
    for o in other_venues:
        other_html += f"""
          <div class="ktv-card" style="margin-bottom:0">
            <a href="{o['slug']}.html" class="ktv-img-wrap" title="{o['name']}">
              <img src="{o['local_image']}" alt="{o['name']}" loading="lazy" decoding="async" width="300" height="190" onerror="this.onerror=null; this.src='{o['image']}';">
              <span class="ktv-card-badge">📍 {o['district']}</span>
            </a>
            <div class="ktv-body">
              <h4 class="ktv-title"><a href="{o['slug']}.html" style="color:inherit;text-decoration:none">{o['name']}</a></h4>
              <p class="ktv-addr" style="font-size:0.84rem">{o['address']}</p>
              <div class="ktv-card-footer">
                <a href="{o['slug']}.html" class="btn-detail-venue" style="flex:1">Xem chi tiết</a>
                <button class="btn-book-venue" type="button" data-book data-venue="{o['name']}">Đặt phòng</button>
              </div>
            </div>
          </div>
        """

    # Schema.org JSON-LD for Venue
    schema_venue = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "EntertainmentBusiness",
                "@id": f"{page_url}#venue",
                "name": v['name'],
                "description": v['description'][:250],
                "url": page_url,
                "image": [img_url],
                "telephone": "+84342092999",
                "priceRange": "$$$",
                "currenciesAccepted": "VND",
                "paymentAccepted": "Tiền mặt, Chuyển khoản ngân hàng, Thẻ tín dụng, QR Pay",
                "servesCuisine": "Karaoke, Đồ uống, Hoa quả tươi, Rượu ngoại",
                "contactPoint": {
                    "@type": "ContactPoint",
                    "telephone": "+84342092999",
                    "contactType": "customer service",
                    "availableLanguage": ["Vietnamese", "Chinese"]
                },
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": v['address'],
                    "addressLocality": v['district'],
                    "addressRegion": "Hà Nội",
                    "addressCountry": "VN"
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": 21.0285,
                    "longitude": 105.8542
                },
                "openingHoursSpecification": {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    "opens": "00:00",
                    "closes": "23:59"
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "5.0",
                    "reviewCount": "128",
                    "bestRating": "5",
                    "worstRating": "1"
                }
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Trang chủ",
                        "item": "https://karaokekenz.com/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Hệ thống KTV Hà Nội",
                        "item": "https://karaokekenz.com/ktv-hanoi.html"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": v['district'],
                        "item": "https://karaokekenz.com/ktv-hanoi.html"
                    },
                    {
                        "@type": "ListItem",
                        "position": 4,
                        "name": v['name'],
                        "item": page_url
                    }
                ]
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"Giá phòng hát tại {v['name']} là bao nhiêu?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Tại {v['name']}, phòng Deluxe (5–10 khách) giá từ {v['price_standard']}; phòng VIP Luxury (10–20 khách) từ {v['price_vip']}; và phòng Super VIP Party (20–40 khách) là {v['price_super_vip']}."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"{v['name']} có địa chỉ chính xác ở đâu và có chỗ đỗ ô tô không?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"{v['name']} toạ lạc tại {v['address']}. Quán có bãi đỗ xe máy và ô tô rộng rãi, có bảo vệ trông coi 24/7 hoàn toàn miễn phí."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"Cách đặt phòng trước tại {v['name']} nhanh nhất?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Quý khách bấm nút 'Đặt phòng ngay tại cơ sở này' trên website hoặc gọi trực tiếp Hotline 0342 092 999 để được giữ phòng VIP đẹp nhất trong 30 giây."
                        }
                    }
                ]
            }
        ]
    }

    return f"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{v['name']} – Bảng Giá, Hình Ảnh &amp; Đặt Phòng VIP Hà Nội</title>
  
  <meta name="description" content="{v['name']} tại {v['address']}. Phòng VIP sang trọng, âm thanh JBL đỉnh cao, hệ thống LED vũ trường hiện đại. Đặt phòng giữ chỗ 24/7 Hotline: 0342 092 999.">
  <meta name="keywords" content="{v['name']}, karaoke {v['district']}, đặt phòng karaoke {v['district']}, bảng giá {v['name']}, karaoke vip hà nội">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#100e22">

  <link rel="canonical" href="{page_url}">
  <link rel="alternate" hreflang="vi" href="{page_url}">
  <link rel="alternate" hreflang="zh" href="{page_url}">
  <link rel="alternate" hreflang="x-default" href="{page_url}">
  <link rel="dns-prefetch" href="https://zalo.me">
  <link rel="icon" type="image/png" sizes="192x192" href="assets/favicon-192x192.png">
  <link rel="icon" type="image/png" sizes="96x96" href="assets/favicon-96x96.png">
  <link rel="icon" type="image/png" sizes="48x48" href="assets/favicon-48x48.png">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="shortcut icon" href="favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Karaoke KTV Hà Nội">
  <meta property="og:url" content="{page_url}">
  <meta property="og:title" content="{v['name']} – Bảng Giá, Hình Ảnh &amp; Đặt Phòng VIP">
  <meta property="og:description" content="{v['name']} tại {v['address']}. Phòng VIP âm thanh cực đỉnh, ánh sáng hiện đại. Hotline đặt phòng: 0342 092 999.">
  <meta property="og:image" content="{img_url}">
  <meta property="og:locale" content="vi_VN">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{v['name']} – Đặt Phòng VIP Hà Nội">
  <meta name="twitter:description" content="{v['name']} tại {v['address']}. Đặt phòng 24/7: 0342 092 999.">
  <meta name="twitter:image" content="{img_url}">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {json.dumps(schema_venue, ensure_ascii=False, indent=2)}
  </script>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Stylesheets -->
  <link rel="stylesheet" href="css/base.css?v=1.4.0">
  <link rel="stylesheet" href="css/animations.css?v=1.4.0">
  <link rel="stylesheet" href="css/components.css?v=1.4.0">
  <link rel="stylesheet" href="css/responsive.css?v=1.4.0">
  <link rel="stylesheet" href="css/ktv.css?v=1.4.0">
</head>
<body>

  <!-- ĐÈN NỀN SÂN KHẤU VŨ TRƯỜNG -->
  <div class="bar-lights" aria-hidden="true">
    <i></i><i></i><i></i><i></i>
    <b></b><b></b><b></b>
    <span class="beams"></span>
    <span class="strobe"></span>
  </div>

  <!-- HEADER THANH ĐIỀU HƯỚNG -->
  <header class="top">
    <div class="wrap">
      <a class="brand" href="index.html">
        <img class="brand-logo" src="assets/logo.png" alt="Logo Karaoke Kenz 202 Trung Kính" width="38" height="38">
        <b><i>KARAOKE </i><em>KENZ </em><u>202 TRUNG KÍNH</u></b>
      </a>
      
      <nav class="links">
        <a href="index.html#gioi-thieu">Giới thiệu</a>
        {mega_dropdown_html}
        <a href="index.html#hinh-anh">Hình ảnh</a>
        <a href="index.html#bang-gia">Bảng giá</a>
        <a href="index.html#uu-dai" style="display:none">Ưu đãi</a>
        <a href="index.html#lien-he">Liên hệ</a>
        <a href="tin-tuc/tintuc.html">Tin tức</a>
      </nav>

      <div class="top-acts">
        <button class="btn btn-ghost btn-sm lang-btn" type="button" id="lang-btn" lang="zh" data-no-i18n aria-label="切换到中文">中文</button>
        <button class="btn btn-hot btn-sm" type="button" data-book data-venue="{v['name']}">Đặt phòng ngay</button>
      </div>
    </div>
  </header>

  <!-- MAIN CONTENT -->
  <main class="wrap" style="padding-top: 30px; padding-bottom: 60px;">
    <!-- BREADCRUMB -->
    <nav class="crumbs" style="margin-bottom: 20px;" aria-label="Breadcrumb">
      <ol style="display:flex;gap:8px;list-style:none;padding:0;margin:0;font-size:0.88rem;color:#9d99be;flex-wrap:wrap">
        <li><a href="index.html" style="color:#c5c2de">Trang chủ</a></li>
        <li>/</li>
        <li><a href="ktv-hanoi.html" style="color:#c5c2de">Hệ thống KTV Hà Nội</a></li>
        <li>/</li>
        <li><a href="ktv-hanoi.html" style="color:#ffd166">{v['district']}</a></li>
        <li>/</li>
        <li style="color:#fff;font-weight:600">{v['name']}</li>
      </ol>
    </nav>

    <!-- VENUE HEADER BANNER -->
    <section class="venue-detail-hero" style="background:rgba(22,19,44,0.85);border:1px solid rgba(255,183,3,0.3);border-radius:24px;padding:30px;margin-bottom:30px;box-shadow:0 15px 40px rgba(0,0,0,0.5)">
      <div class="venue-detail-hero-grid">
        <!-- Main Image with Lightbox Zoom -->
        <div style="border-radius:18px;overflow:hidden;aspect-ratio:16/11;background:#15122b;box-shadow:0 10px 25px rgba(0,0,0,0.5);cursor:zoom-in" data-lightbox>
          <img src="{v['local_image']}" alt="{v['name']} – Phòng Hát Karaoke VIP Đẹp" fetchpriority="high" decoding="async" width="600" height="412" style="width:100%;height:100%;object-fit:cover;transition:transform 0.4s" onerror="this.onerror=null; this.src='{v['image']}';">
        </div>

        <!-- Info & Actions -->
        <div>
          <div style="display:flex;gap:10px;align-items:center;margin-bottom:12px;flex-wrap:wrap">
            <span style="background:rgba(255,183,3,0.2);border:1px solid rgba(255,183,3,0.5);color:#ffd166;padding:4px 12px;border-radius:20px;font-size:0.82rem;font-weight:700">📍 QUẬN {v['district'].upper()}</span>
            <span style="background:rgba(255,42,109,0.2);border:1px solid rgba(255,42,109,0.5);color:#ff758c;padding:4px 12px;border-radius:20px;font-size:0.82rem;font-weight:700">⭐ 5.0 VIP</span>
            <span class="pulse-badge"><span class="pulse-dot"></span> ĐANG MỞ CỬA 24/24H</span>
          </div>

          <h1 style="font-size:clamp(1.6rem, 3.5vw, 2.3rem);font-weight:800;color:#fff;margin-bottom:14px;line-height:1.25">
            {v['name']}
          </h1>

          <p style="display:flex;align-items:flex-start;gap:8px;color:#c5c2de;font-size:1rem;margin-bottom:18px;line-height:1.5">
            <svg style="color:#ff5e36;flex-shrink:0;margin-top:3px" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
            <span><strong>Địa chỉ:</strong> {v['address']}</span>
          </p>

          <!-- Highlights stats -->
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(110px, 1fr));gap:10px;margin-bottom:22px">
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:10px;border-radius:12px;text-align:center">
              <div style="font-size:0.78rem;color:#9d99be">Quy mô</div>
              <div style="font-size:1.15rem;font-weight:800;color:#ffd166">{v['rooms_count']}+ Phòng</div>
            </div>
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:10px;border-radius:12px;text-align:center">
              <div style="font-size:0.78rem;color:#9d99be">Nhân viên</div>
              <div style="font-size:1.15rem;font-weight:800;color:#ff758c">{v['staff_count']}+ Phục vụ</div>
            </div>
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:10px;border-radius:12px;text-align:center">
              <div style="font-size:0.78rem;color:#9d99be">Bài hát</div>
              <div style="font-size:1.15rem;font-weight:800;color:#4cc9f0">{v['songs_count']}</div>
            </div>
          </div>

          <!-- CTAs -->
          <div style="display:flex;gap:12px;flex-wrap:wrap">
            <button class="btn btn-hot" type="button" data-book data-venue="{v['name']}" style="padding:14px 28px;font-size:1.02rem;flex:1;min-width:200px">
              🎤 Đặt phòng ngay tại cơ sở này
            </button>
            <a class="btn btn-ghost" href="tel:0342092999" style="padding:14px 22px;font-size:1rem;display:inline-flex;align-items:center;gap:8px">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>
              <span>Gọi: 0342 092 999</span>
            </a>
            <a class="btn btn-ghost" href="https://zalo.me/0342092999" target="_blank" rel="noopener" style="padding:14px 20px;font-size:1rem">
              💬 Nhắn Zalo
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- CONTENT BODY: GIỚI THIỆU & BẢNG GIÁ & HÌNH ẢNH -->
    <div class="venue-content-grid">
      <div>
        <!-- GIỚI THIỆU CHI TIẾT -->
        <section style="background:rgba(22,19,44,0.7);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:28px;margin-bottom:30px">
          <h2 style="font-size:1.45rem;color:#ffd166;margin-bottom:14px;display:flex;align-items:center;gap:10px">
            <span>✨</span> Giới thiệu về {v['name']}
          </h2>
          <p style="font-size:1.02rem;line-height:1.8;color:#dedbf2;margin-bottom:20px;white-space:pre-line">
            {v['description']}
          </p>

          <!-- TIỆN ÍCH NỔI BẬT -->
          <h3 style="font-size:1.2rem;color:#fff;margin-bottom:14px">Đặc quyền nổi bật tại {v['name']}</h3>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));gap:14px">
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:14px;border-radius:12px">
              <div style="color:#ffd166;font-weight:700;margin-bottom:4px">🔊 Dàn Loa JBL / BMB Cực Khủng</div>
              <div style="font-size:0.86rem;color:#9d99be">Công suất lớn, bass chắc nịch, micro cao cấp chống hú rè tuyệt đối.</div>
            </div>
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:14px;border-radius:12px">
              <div style="color:#ff758c;font-weight:700;margin-bottom:4px">💡 Ánh Sáng Laser 3D Vũ Trường</div>
              <div style="font-size:0.86rem;color:#9d99be">Màn LED cảm ứng theo giai điệu nhạc cực bắt mắt và hiện đại.</div>
            </div>
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:14px;border-radius:12px">
              <div style="color:#4cc9f0;font-weight:700;margin-bottom:4px">🛡️ Cách Âm Chuẩn Tiêu Chuẩn 100%</div>
              <div style="font-size:0.86rem;color:#9d99be">Tường cách âm chuyên dụng, đảm bảo không gian riêng tư trọn vẹn.</div>
            </div>
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:14px;border-radius:12px">
              <div style="color:#06d6a0;font-weight:700;margin-bottom:4px">🍹 Menu Rượu Ngoại &amp; Tiệc Chu Đáo</div>
              <div style="font-size:0.86rem;color:#9d99be">Hoa quả tươi, đồ ăn nóng sốt và các loại đồ uống hảo hạng phục vụ tận nơi.</div>
            </div>
          </div>
        </section>

        <!-- HÌNH ẢNH PHÒNG HÁT THỰC TẾ -->
        <section style="background:rgba(22,19,44,0.7);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:28px;margin-bottom:30px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px">
            <h2 style="font-size:1.45rem;color:#ffd166;margin:0;display:flex;align-items:center;gap:10px">
              <span>📸</span> Không gian phòng hát thực tế
            </h2>
            <small style="color:#9d99be">(Bấm vào ảnh để phóng to toàn màn hình)</small>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));gap:16px">
            {gallery_html}
          </div>
        </section>

        <!-- HỎI ĐÁP VỀ CƠ SỞ -->
        <section style="background:rgba(22,19,44,0.7);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:28px">
          <h2 style="font-size:1.45rem;color:#ffd166;margin-bottom:18px;display:flex;align-items:center;gap:10px">
            <span>❓</span> Những câu hỏi thường gặp về {v['name']}
          </h2>
          <div class="ktv-faq-list" style="margin-top:0">
            <div class="ktv-faq-item active">
              <div class="ktv-faq-q">
                <span>Cơ sở {v['name']} có hỗ trợ đoàn đông người và tổ chức tiệc không?</span>
                <svg class="ktv-faq-arrow" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>
              </div>
              <div class="ktv-faq-a">
                Có. Quán có hệ thống phòng tiệc lớn sức chứa từ 20 đến 45 khách, nhận set up tiệc sinh nhật, liên hoan công ty trọn gói với loa kéo bổ trợ, ánh sáng sân khấu và màn chiếu theo yêu cầu.
              </div>
            </div>

            <div class="ktv-faq-item">
              <div class="ktv-faq-q">
                <span>Chỗ đỗ ô tô tại {v['name']} như thế nào?</span>
                <svg class="ktv-faq-arrow" viewBox="0 0 24 24" fill="currentColor"><path d="M7 10l5 5 5-5z"/></svg>
              </div>
              <div class="ktv-faq-a">
                Quán có khu vực đỗ xe máy và bãi đậu ô tô thuận tiện, có nhân viên bảo vệ điều phối và trông coi xe miễn phí suốt thời gian quý khách sử dụng dịch vụ.
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- SIDEBAR: BẢNG GIÁ & FORM ĐẶT PHÒNG NHANH -->
      <div>
        <div class="sticky-sidebar-book">
          <!-- 👑 BẢNG GIÁ PHÒNG KARAOKE CAO CẤP -->
          <div class="pricing-card-luxury" style="background:linear-gradient(135deg,rgba(26,20,54,0.92),rgba(15,12,35,0.95));border:1px solid rgba(255,183,3,0.4);border-radius:20px;padding:24px;margin-bottom:24px;box-shadow:0 12px 30px rgba(0,0,0,0.5),0 0 20px rgba(255,183,3,0.1)">
            <div style="margin-bottom:16px;border-bottom:1px solid rgba(255,183,3,0.25);padding-bottom:12px">
              <h3 style="font-size:1.25rem;color:#ffd166;margin:0 0 4px;display:flex;align-items:center;gap:8px">
                <span>👑</span> BẢNG GIÁ PHÒNG CAO CẤP
              </h3>
              <p style="font-size:0.82rem;color:#c5c2de;margin:0">✨ Không gian sang trọng – Dịch vụ đẳng cấp – Trải nghiệm thượng lưu</p>
            </div>

            <div style="display:flex;flex-direction:column;gap:14px;font-size:0.92rem">
              <!-- PHÒNG DELUXE -->
              <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:12px 14px">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;flex-wrap:wrap;gap:4px">
                  <span style="color:#fff;font-weight:700">💎 PHÒNG DELUXE (5–10 khách)</span>
                  <strong style="color:#ffd166;font-size:1rem">{v['price_standard']}</strong>
                </div>
                <small style="color:#9d99be;font-size:0.8rem;line-height:1.4;display:block">Không gian riêng tư, hiện đại, phù hợp cho những buổi gặp gỡ và giải trí cùng bạn bè, gia đình.</small>
              </div>

              <!-- PHÒNG VIP LUXURY -->
              <div style="background:linear-gradient(135deg,rgba(255,183,3,0.08),rgba(255,77,106,0.08));border:1px solid rgba(255,183,3,0.35);border-radius:12px;padding:12px 14px">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;flex-wrap:wrap;gap:4px">
                  <span style="color:#ffd166;font-weight:800">👑 PHÒNG VIP LUXURY (10–20 khách)</span>
                  <strong style="color:#ffb703;font-size:1.02rem">{v['price_vip']}</strong>
                </div>
                <small style="color:#dedbf2;font-size:0.8rem;line-height:1.4;display:block">Không gian rộng rãi, sang trọng, mang đến trải nghiệm giải trí đẳng cấp cho những cuộc vui đáng nhớ.</small>
              </div>

              <!-- PHÒNG SUPER VIP PARTY -->
              <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:12px 14px">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;flex-wrap:wrap;gap:4px">
                  <span style="color:#fff;font-weight:700">🔥 PHÒNG SUPER VIP PARTY (20–40 khách)</span>
                  <strong style="color:#ff758c;font-size:1rem">{v['price_super_vip']}</strong>
                </div>
                <small style="color:#9d99be;font-size:0.8rem;line-height:1.4;display:block">Không gian tiệc tùng hoành tráng, lựa chọn lý tưởng cho sinh nhật, liên hoan và các sự kiện đặc biệt.</small>
              </div>
            </div>

            <div style="margin-top:14px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.08);font-size:0.8rem;color:#c5c2de;line-height:1.5">
              <div style="color:#ffd166;font-weight:700;margin-bottom:3px">🎁 ĐẶT PHÒNG SỚM – ƯU TIÊN PHÒNG ĐẸP</div>
              <div style="color:#9d99be;font-size:0.78rem">📌 Giá tham khảo có thể thay đổi theo khung giờ, cuối tuần và dịp lễ.</div>
              <div style="color:#06d6a0;font-weight:700;margin-top:4px">📞 Hotline hỗ trợ &amp; giữ chỗ: 0342 092 999</div>
            </div>
          </div>

          <!-- FORM ĐẶT BÀN NHANH TRỰC TIẾP TRÊN TRANG -->
          <div style="background:linear-gradient(135deg,rgba(255,77,106,0.12),rgba(255,183,3,0.12));border:1px solid rgba(255,183,3,0.4);border-radius:20px;padding:24px;box-shadow:0 10px 30px rgba(0,0,0,0.4)">
            <h3 style="font-size:1.25rem;color:#fff;margin-bottom:6px">⚡ Đặt phòng nhanh 24/7</h3>
            <p style="font-size:0.86rem;color:#c5c2de;margin-bottom:16px">Giữ chỗ miễn phí 100%, nhân viên gọi xác nhận trong 3 phút.</p>
            
            <button class="btn btn-hot" type="button" data-book data-venue="{v['name']}" style="width:100%;padding:14px;font-size:1.02rem;box-shadow:0 6px 20px rgba(255,77,106,0.4)">
              🎤 Đặt phòng tại {v['name']}
            </button>

            <div style="margin-top:16px;text-align:center">
              <span style="color:#9d99be;font-size:0.84rem">Hoặc gọi hotline trực tiếp:</span><br>
              <a href="tel:0342092999" style="color:#ffd166;font-size:1.25rem;font-weight:800;text-decoration:none">0342 092 999</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    {render_venue_map_section(v)}

    <!-- CÁC CƠ SỞ KTV LIÊN QUAN -->
    <section style="margin-top:40px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px">
        <h3 style="font-size:1.35rem;color:#fff">Các quán Karaoke KTV khác tại {v['district']}</h3>
        <a href="ktv-hanoi.html" style="color:#ffd166;font-size:0.9rem;text-decoration:none;font-weight:700">Xem tất cả 21 quán →</a>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:20px">
        {other_html}
      </div>
    </section>
  </main>

  <!-- FOOTER -->
  <footer class="bot">
    <div class="wrap" style="text-align:center;padding:26px 20px;font-size:0.88rem;color:#9d99be;line-height:1.7">
      <p style="margin-bottom:8px">© 2026 <strong>Karaoke Kenz 202 Trung Kính</strong> &amp; <strong>Hệ Thống 21+ Quán Karaoke KTV Hà Nội</strong>. All rights reserved.</p>
      <p style="font-size:0.82rem;color:#7e7a9b">Hotline đặt phòng VIP 24/7: <b style="color:#ffd166">0342 092 999</b> · Cam kết dịch vụ phòng hát chất lượng cao.</p>
    </div>
  </footer>

  <!-- THANH TIỆN ÍCH MOBILE -->
  <aside class="quick" aria-label="Hỗ trợ nhanh">
    <div class="quick-main">
      <a class="fab-btn" href="tel:0342092999">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>
        <span>Gọi điện</span>
      </a>
      <a class="fab-btn" href="https://zalo.me/0342092999" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.03 2 11c0 2.87 1.5 5.41 3.84 7.03L5 22l4.28-1.43C10.15 20.83 11.05 21 12 21c5.52 0 10-4.03 10-9s-4.48-9-10-9zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>
        <span>Zalo</span>
      </a>
      <button class="fab-btn hot" type="button" data-book data-venue="{v['name']}">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zM9 14H7v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2zm-8 4H7v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2z"/></svg>
        <span>Đặt bàn</span>
      </button>
    </div>
  </aside>

  <!-- HỘP THOẠI ĐẶT PHÒNG TRỰC TUYẾN (BOOKING MODAL) -->
  <div class="modal" id="modal" hidden>
    <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="bk-title">
      <button class="x" type="button" id="modal-x" aria-label="Đóng">×</button>

      <!-- BƯỚC 1: FORM NHẬP THÔNG TIN -->
      <div id="bk-step-form">
        <div class="eyebrow">Hệ Thống Karaoke KTV Hà Nội</div>
        <h2 id="bk-title">Thông tin đặt chỗ</h2>
        
        <!-- HIỂN THỊ CƠ SỞ ĐƯỢC CHỌN -->
        <div style="background:rgba(255,183,3,0.12);border:1px solid rgba(255,183,3,0.3);border-radius:12px;padding:10px 14px;margin-bottom:16px;display:flex;align-items:center;gap:10px">
          <span style="font-size:1.2rem">🏢</span>
          <div>
            <div style="font-size:0.75rem;color:#ffd166;text-transform:uppercase;font-weight:700">Cơ sở / Quán đã chọn:</div>
            <div id="f-selected-venue" style="font-size:0.98rem;font-weight:700;color:#fff">{v['name']}</div>
          </div>
        </div>

        <form class="bk" id="bk-form" novalidate>
          <input type="hidden" id="f-venue" value="{v['name']}">
          
          <div class="two">
            <div class="field">
              <label for="f-name">Họ và tên <i>*</i></label>
              <input id="f-name" autocomplete="name" placeholder="Nhập tên của bạn...">
            </div>
            <div class="field">
              <label for="f-phone">Số điện thoại <i>*</i></label>
              <input id="f-phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="Nhập số điện thoại...">
            </div>
          </div>

          <div class="two">
            <div class="field">
              <label for="f-date">Ngày đặt <i>*</i></label>
              <input id="f-date" type="date">
            </div>
            <div class="field">
              <label for="f-time">Giờ đến <i>*</i></label>
              <input id="f-time" inputmode="numeric" maxlength="5" autocomplete="off" placeholder="VD: 19:30">
            </div>
          </div>

          <!-- Bẫy bot spam -->
          <div class="hp" aria-hidden="true">
            <label>Website <input id="f-website" tabindex="-1" autocomplete="off"></label>
          </div>

          <div class="field">
            <label for="f-note">Ghi chú thêm (nếu có)</label>
            <textarea id="f-note" maxlength="300" placeholder="Yêu cầu trang trí tiệc, số lượng người, phòng VIP…"></textarea>
          </div>

          <p class="err" id="f-err" hidden></p>
          <button class="btn btn-hot" type="submit" id="f-submit">Gửi yêu cầu đặt bàn</button>
        </form>
      </div>

      <!-- BƯỚC 2: MÀN HÌNH XÁC NHẬN MÃ ĐẶT PHÒNG THÀNH CÔNG -->
      <div class="done" id="bk-step-done" hidden>
        <div class="eyebrow">Đã gửi yêu cầu đặt bàn</div>
        <div class="code" id="d-code">KZ-8888</div>
        <p class="muted">Chụp lại mã này. Nhân viên sẽ liên hệ xác nhận trong ít phút.</p>
        <dl id="d-list"></dl>

        <div style="margin-top:20px">
          <a class="btn" id="d-zalo-btn" target="_blank" rel="noopener" style="background:var(--zalo);color:#fff;width:100%;padding:14px 20px;border-radius:12px;font-size:1.02rem;display:inline-flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 8px 24px -6px rgba(10,104,255,0.7);text-decoration:none;transition:transform .2s">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.03 2 11c0 2.87 1.5 5.41 3.84 7.03L5 22l4.28-1.43C10.15 20.83 11.05 21 12 21c5.52 0 10-4.03 10-9s-4.48-9-10-9zm1 14h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>
            <span>Nhắn Zalo xác nhận giữ phòng ngay</span>
          </a>
          <small class="muted" style="display:block;margin-top:8px;font-size:0.82rem">Bấm để tự động mở Zalo và gửi mã đặt phòng cho quản lý</small>
        </div>
        
        <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:20px">
          <button class="btn btn-ghost" type="button" id="d-again">Đặt thêm</button>
          <button class="btn btn-hot" type="button" id="d-close">Xong</button>
        </div>
      </div>
    </div>
  </div>

  <!-- TOAST -->
  <div class="toast" id="toast" hidden></div>

  <!-- SCRIPTS -->
  <script src="config.js"></script>
  <script src="js/i18n.js"></script>
  <script src="js/ktv-data.js"></script>
  <script src="js/booking.js"></script>
  <script src="js/promotions.js"></script>
  <script src="js/live-bookings.js"></script>
  <script src="js/ktv-runtime.js"></script>
  <script src="js/app.js"></script>
</body>
</html>
"""

# Generate static HTML detail page for EVERY single venue!
for v in venues:
    slug_filename = f"{v['slug']}.html"
    content = generate_detail_page(v)
    with open(slug_filename, 'w', encoding='utf-8') as f:
        f.write(content)
print(f"3. Generated {len(venues)} venue detail HTML files with Schema & Lightbox!")

# Also generate ktv-detail.html as dynamic template
with open('ktv-detail.html', 'w', encoding='utf-8') as f:
    f.write(generate_detail_page(venues[0]))
print("4. Generated ktv-detail.html!")

# Also generate alias karaoke-kenz-club-202-trung-kinh.html so both URL spellings work seamlessly!
with open('karaoke-kenz-club-202-trung-kinh.html', 'w', encoding='utf-8') as f:
    f.write(generate_detail_page(venues[0]))
print("5. Generated alias karaoke-kenz-club-202-trung-kinh.html!")
