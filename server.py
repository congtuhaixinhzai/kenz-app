#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
KARAOKE KENZ - WEB SERVER & ZALO BOT BRIDGE (PORT 80)
=============================================================================
- Chạy trực tiếp trên cổng 80 (truy cập thẳng http://localhost hoặc IP máy).
- Tích hợp sẵn Web Server phục vụ toàn bộ website: HTML, CSS, JS, ảnh, tin tức.
- Tích hợp cổng API /send-zalo kết nối thẳng tới Zalo Bot trên Home Assistant
  (MultiZlogin tại http://192.168.1.245:3000).
- Tự động lấy Cookie đăng nhập, tìm người nhận và bắn tin nhắn Zalo tức thì.
- Zero Dependencies: Chỉ dùng Python có sẵn, không cần cài bất kỳ thư viện nào!
=============================================================================
"""

import http.server
import socketserver
import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

# Đảm bảo in tiếng Việt và ký tự đặc biệt không bị lỗi trên Windows CMD
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PORT = 80
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZALO_SERVER_URL = "http://192.168.1.245:3000"
ZALO_ACCOUNT = "+84702002732"
# ID Nhóm Zalo mới tạo "THÔNG BÁO KENZ" - CHỈ GỬI DUY NHẤT VÀO ĐÂY
TARGET_GROUP_THREAD_ID = "6974367796269023658"

# Bộ nhớ đệm session cookie của Zalo Bot
_zalo_session_cookie = None

def get_zalo_cookie():
    """Đăng nhập vào Zalo Bot server để lấy session cookie"""
    global _zalo_session_cookie
    if _zalo_session_cookie:
        return _zalo_session_cookie

    try:
        url = f"{ZALO_SERVER_URL}/api/test-login"
        payload = json.dumps({"username": "admin", "password": "admin"}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            set_cookie = resp.headers.get("Set-Cookie")
            if set_cookie:
                _zalo_session_cookie = set_cookie.split(";")[0]
                return _zalo_session_cookie
    except Exception as e:
        print(f"[!] Chưa kết nối được Zalo Bot tại {ZALO_SERVER_URL}: {e}")
    return None

def send_raw_zalo_message(message_text, log_title="Thông báo"):
    """Hàm gửi tin nhắn Zalo an toàn chỉ vào nhóm THÔNG BÁO KENZ"""
    cookie = get_zalo_cookie()
    if not cookie:
        print(f"[!] Không có cookie kết nối Zalo Bot cho '{log_title}'. Lưu log giả lập.")
        return {"success": True, "mode": "simulation", "message": "Đã lưu log (Chờ Zalo Bot)"}

    recipients = [
        {"threadId": TARGET_GROUP_THREAD_ID, "type": 1, "name": "Nhóm THÔNG BÁO KENZ"}
    ]

    results = []
    for rec in recipients:
        if rec["threadId"] != TARGET_GROUP_THREAD_ID:
            print(f"[CHẶN AN TOÀN] Bỏ qua {rec.get('name')} vì không phải nhóm THÔNG BÁO KENZ")
            continue
        try:
            payload = json.dumps({
                "message": {
                    "msg": message_text,
                    "ttl": 0
                },
                "threadId": rec["threadId"],
                "accountSelection": ZALO_ACCOUNT,
                "type": rec["type"]
            }).encode("utf-8")

            url = f"{ZALO_SERVER_URL}/api/sendMessageByAccount"
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Cookie": cookie
                }
            )

            with urllib.request.urlopen(req, timeout=10) as resp:
                res_body = resp.read().decode("utf-8")
                print(f"[✅ ZALO THÀNH CÔNG] Đã gửi thông báo ({log_title}) tới {rec['name']}: {res_body}")
                results.append({"target": rec["name"], "status": "sent"})
        except Exception as ex:
            print(f"[⚠️ ZALO THẤT BẠI] Gửi ({log_title}) tới {rec['name']} lỗi: {ex}")
            results.append({"target": rec["name"], "status": "error", "error": str(ex)})

    return {"success": True, "results": results}

def send_zalo_notification(booking_data):
    """Gửi thông báo đơn đặt bàn qua MultiZlogin trên cổng 3000"""
    code = booking_data.get("code", "KZ-TEST")
    name = booking_data.get("name", "Khách Hàng")
    phone = booking_data.get("phone", "Chưa có")
    date = booking_data.get("date", "")
    time_str = booking_data.get("time", "")
    note = booking_data.get("note", "Không có")
    guests = booking_data.get("guests", "2-5 người")
    venue = booking_data.get("venue", "Karaoke Kenz Club 202 Trung Kính")
    now_str = datetime.now().strftime("%H:%M - %d/%m/%Y")
    phone_raw = str(phone).strip()
    phone_clean = ''.join(filter(str.isdigit, phone_raw))
    
    # Định dạng ngày DD/MM/YYYY chuẩn tiếng Việt
    date_display = date
    if "-" in str(date):
        parts = str(date).split("-")
        if len(parts) == 3 and len(parts[0]) == 4:
            date_display = f"{parts[2]}/{parts[1]}/{parts[0]}"

    call_link = f"tel:{phone_clean}" if phone_clean else "Chưa có"
    zalo_link = f"https://zalo.me/{phone_clean}" if phone_clean else ""

    message_text = (
        f"👑 [ĐƠN ĐẶT PHÒNG MỚI - KARAOKE KENZ]\n"
        f"══════════════════════════\n"
        f"🔖 Mã đặt chỗ: #{code}\n"
        f"🏢 Cơ sở / Quán: {venue}\n"
        f"👤 Khách hàng: {str(name).upper()}\n"
        f"📞 Điện thoại: {phone_raw}\n"
        f"📲 BẤM GỌI NGAY: {call_link}\n"
        + (f"💬 NHẮN ZALO KHÁCH: {zalo_link}\n" if zalo_link else "") +
        f"──────────────────────────\n"
        f"📅 Ngày hát: {date_display}\n"
        f"⏰ Giờ đến: {time_str}\n"
        f"👥 Số lượng khách: {guests}\n"
        f"📝 Ghi chú: {note}\n"
        f"⏱ Báo lúc: {now_str}\n"
        f"══════════════════════════\n"
        f"⚡ Quán bấm link gọi ngay để xác nhận & giữ phòng cho khách!"
    )

    print(f"\n[🔔 ĐƠN MỚI] Khách {name} ({phone}) đặt lúc {time_str} ngày {date}")
    return send_raw_zalo_message(message_text, f"Đơn mới #{code}")

def send_review_zalo_notification(review_data):
    """Gửi thông báo có khách vừa gửi đánh giá mới cần Admin duyệt"""
    author = review_data.get("author", "Khách Hàng")
    phone = review_data.get("phone", "Không cung cấp")
    rating = review_data.get("rating", 5)
    content = review_data.get("content", "")
    stars_str = "⭐" * int(rating)
    now_str = datetime.now().strftime("%H:%M - %d/%m/%Y")

    sub = review_data.get("sub_ratings", {})
    sub_text = ""
    if sub and any(sub.values()):
        sub_text = f"📊 Chi tiết: Đồ ăn {sub.get('food', 5)}/5 · Dịch vụ {sub.get('service', 5)}/5 · Không khí {sub.get('atmosphere', 5)}/5\n"

    phone_clean = ''.join(filter(str.isdigit, str(phone)))
    call_link = f"tel:{phone_clean}" if phone_clean else ""
    zalo_link = f"https://zalo.me/{phone_clean}" if phone_clean else ""

    message_text = (
        f"🌟 [ĐÁNH GIÁ MỚI - CHỜ DUYỆT]\n"
        f"══════════════════════════\n"
        f"👤 Khách gửi: {str(author).upper()}\n"
        f"📞 Số điện thoại: {phone}\n"
        + (f"📲 Bấm gọi: {call_link}\n" if call_link else "") +
        (f"💬 Nhắn Zalo: {zalo_link}\n" if zalo_link else "") +
        f"✨ Điểm đánh giá: {stars_str} ({rating}/5 sao)\n"
        + sub_text +
        f"💬 Cảm nhận: \"{content}\"\n"
        f"⏱ Thời gian: {now_str}\n"
        f"══════════════════════════\n"
        f"⚠️ Đánh giá này ĐANG CHỜ DUYỆT và CHƯA HIỂN THỊ trên website.\n"
        f"👉 Quản trị viên vào Bảng Điều Khiển để DUYỆT hoặc PHẢN HỒI:\n"
        f"🔗 http://localhost/admin.html"
    )

    print(f"\n[🌟 ĐÁNH GIÁ MỚI] Khách {author} gửi đánh giá {rating} sao (Chờ duyệt)")
    return send_raw_zalo_message(message_text, f"Đánh giá mới từ {author}")

class KenzServerHandler(http.server.SimpleHTTPRequestHandler):
    """Xử lý phục vụ file web tĩnh và các API đặt bàn /send-zalo"""
    extensions_map = http.server.SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map.update({
        '.webmanifest': 'application/manifest+json',
        '.json': 'application/json; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Cho phép Cross-Origin Request
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        # Bắt buộc Cloudflare & Trình duyệt luôn luôn lấy file mới nhất 2.0.0, chống cache cũ
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/status" or self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            status_data = {
                "server": "Karaoke Kenz Port 80",
                "port": PORT,
                "zaloBotUrl": ZALO_SERVER_URL,
                "zaloAccount": ZALO_ACCOUNT,
                "status": "online",
                "time": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(status_data, ensure_ascii=False).encode("utf-8"))
            return

        if self.path in ["/api/promotions", "/promotions.json"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            promo_file = os.path.join(BASE_DIR, "promotions.json")
            if os.path.exists(promo_file):
                with open(promo_file, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.wfile.write(b"[]")
            return

        if self.path in ["/api/venue-visibility", "/venue_visibility.json"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            vis_file = os.path.join(BASE_DIR, "venue_visibility.json")
            if os.path.exists(vis_file):
                with open(vis_file, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.wfile.write(b"{}")
            return
        
        if self.path in ["/api/reviews", "/reviews.json"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            rev_file = os.path.join(BASE_DIR, "reviews.json")
            if os.path.exists(rev_file):
                try:
                    with open(rev_file, "r", encoding="utf-8") as f:
                        all_revs = json.load(f)
                    # Chỉ trả về đánh giá đã được duyệt (status == 'approved') cho khách xem
                    approved = [r for r in all_revs if r.get("status") == "approved"]
                    sanitized = []
                    for r in approved:
                        item = dict(r)
                        p = str(item.get("phone", "")).strip()
                        if p:
                            item["phone"] = (p[:3] + "****" + p[-3:]) if len(p) >= 7 else "***"
                        sanitized.append(item)
                    self.wfile.write(json.dumps(sanitized, ensure_ascii=False).encode("utf-8"))
                    return
                except Exception as e:
                    print(f"[!] Lỗi đọc reviews.json: {e}")
            self.wfile.write(b"[]")
            return

        if self.path in ["/api/admin/reviews"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            rev_file = os.path.join(BASE_DIR, "reviews.json")
            if os.path.exists(rev_file):
                with open(rev_file, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.wfile.write(b"[]")
            return
        
        # Mặc định chuyển / thành /index.html và route các trang KTV
        clean_path = self.path.split("?")[0].rstrip("/")
        if clean_path == "" or clean_path == "/":
            self.path = "/index.html"
        elif clean_path in ["/ktv-hanoi", "/karaoke-ktv-ha-noi"]:
            self.path = "/ktv-hanoi.html"
        else:
            # Tự động phục vụ file .html nếu đường dẫn không có đuôi .html
            rel_file = clean_path.lstrip("/") + ".html"
            potential_file = os.path.join(BASE_DIR, rel_file)
            if os.path.isfile(potential_file):
                self.path = "/" + rel_file
            
        super().do_GET()

    def do_POST(self):
        if self.path in ["/api/promotions"]:
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "[]"
                promos = json.loads(post_data)
                promo_file = os.path.join(BASE_DIR, "promotions.json")
                with open(promo_file, "w", encoding="utf-8") as f:
                    json.dump(promos, f, ensure_ascii=False, indent=2)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "count": len(promos)}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))
            return

        if self.path in ["/api/venue-visibility"]:
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
                visibility_data = json.loads(post_data)
                vis_file = os.path.join(BASE_DIR, "venue_visibility.json")
                with open(vis_file, "w", encoding="utf-8") as f:
                    json.dump(visibility_data, f, ensure_ascii=False, indent=2)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "count": len(visibility_data)}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))
            return

        if self.path in ["/api/reviews"]:
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
                data = json.loads(post_data)
                
                author = str(data.get("author", "")).strip()[:50] or "Khách giấu tên"
                phone = str(data.get("phone", "")).strip()[:20]
                content = str(data.get("content", "")).strip()[:1000]
                try:
                    rating = int(data.get("rating", 5))
                    if rating < 1: rating = 1
                    if rating > 5: rating = 5
                except Exception:
                    rating = 5

                sub_ratings = data.get("sub_ratings", {})

                new_rev = {
                    "id": f"rev_{int(datetime.now().timestamp() * 1000)}",
                    "author": author,
                    "phone": phone,
                    "rating": rating,
                    "content": content,
                    "sub_ratings": sub_ratings,
                    "reply": "",
                    "status": "pending",  # ĐÁNH GIÁ MỚI LUÔN Ở TRẠNG THÁI CHỜ DUYỆT (PENDING)
                    "created_at": datetime.now().isoformat(),
                    "created_display": "Vừa xong"
                }

                rev_file = os.path.join(BASE_DIR, "reviews.json")
                all_revs = []
                if os.path.exists(rev_file):
                    try:
                        with open(rev_file, "r", encoding="utf-8") as f:
                            all_revs = json.load(f)
                    except Exception:
                        all_revs = []

                all_revs.insert(0, new_rev)
                with open(rev_file, "w", encoding="utf-8") as f:
                    json.dump(all_revs, f, ensure_ascii=False, indent=2)

                # Bắn thông báo Zalo vào nhóm "THÔNG BÁO KENZ" để Admin biết có đánh giá mới
                try:
                    send_review_zalo_notification(new_rev)
                except Exception as ze:
                    print(f"[!] Lỗi gửi Zalo đánh giá: {ze}")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "message": "Cảm ơn quý khách! Đánh giá đã được ghi nhận và đang chờ ban quản trị duyệt trước khi hiển thị lên website."
                }, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))
            return

        if self.path in ["/api/admin/reviews"]:
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
                body = json.loads(post_data)
                rev_file = os.path.join(BASE_DIR, "reviews.json")

                if isinstance(body, list):
                    # Admin gửi toàn bộ danh sách đã chỉnh sửa
                    with open(rev_file, "w", encoding="utf-8") as f:
                        json.dump(body, f, ensure_ascii=False, indent=2)
                elif isinstance(body, dict):
                    # Admin gửi lệnh cập nhật 1 review
                    rev_id = body.get("id")
                    action = body.get("action")
                    all_revs = []
                    if os.path.exists(rev_file):
                        with open(rev_file, "r", encoding="utf-8") as f:
                            all_revs = json.load(f)

                    if action == "delete":
                        all_revs = [r for r in all_revs if str(r.get("id")) != str(rev_id)]
                    else:
                        for r in all_revs:
                            if str(r.get("id")) == str(rev_id):
                                if action == "approve":
                                    r["status"] = "approved"
                                elif action == "reject":
                                    r["status"] = "rejected"
                                if "status" in body:
                                    r["status"] = body["status"]
                                if "reply" in body:
                                    r["reply"] = body["reply"]

                    with open(rev_file, "w", encoding="utf-8") as f:
                        json.dump(all_revs, f, ensure_ascii=False, indent=2)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))
            return

        if self.path in ["/send-zalo", "/api/booking", "/api/send-zalo"]:
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

                booking_info = {}
                try:
                    booking_info = json.loads(post_data)
                except Exception:
                    try:
                        booking_info = dict(urllib.parse.parse_qsl(post_data))
                    except Exception:
                        pass

                result = send_zalo_notification(booking_info)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                print(f"[!] Lỗi xử lý do_POST: {e}")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def main():
    print("=" * 70)
    print("   🎤 HỆ THỐNG MÁY CHỦ WEB & ZALO BOT - KARAOKE KENZ 202 TRUNG KÍNH")
    print("=" * 70)
    print(f"🚀 MÁY CHỦ ĐANG CHẠY TRÊN CỔNG: {PORT}")
    print(f"👉 Website chính:      http://localhost")
    print(f"👉 Quản trị đơn:       http://localhost/admin.html")
    print(f"👉 Chuyên mục tin tức: http://localhost/tin-tuc/tintuc.html")
    print(f"👉 Kết nối Zalo Bot:   {ZALO_SERVER_URL} (Tài khoản: {ZALO_ACCOUNT})")
    print("=" * 70)
    print("Đang lắng nghe truy cập và đơn đặt bàn... (Bấm Ctrl + C để dừng)\n")

    # Cho phép tái sử dụng port ngay khi khởi động lại
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), KenzServerHandler) as httpd:
            httpd.serve_forever()
    except PermissionError:
        print("\n[!] LỖI QUYỀN HẠN: Cổng 80 cần chạy bằng quyền Administrator.")
        print("[!] Hãy nhấp chuột phải vào file chay-server-80.bat và chọn 'Run as administrator'.")
        input("\nNhấn Enter để thoát...")
    except OSError as e:
        print(f"\n[!] LỖI KHỞI ĐỘNG CỔNG 80: {e}")
        print("[!] Có thể có chương trình khác đang dùng cổng 80.")
        input("\nNhấn Enter để thoát...")
    except KeyboardInterrupt:
        print("\n[!] Đã dừng máy chủ cổng 80.")

if __name__ == "__main__":
    main()
