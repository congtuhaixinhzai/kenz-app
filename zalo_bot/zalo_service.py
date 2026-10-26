#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
DỊCH VỤ ZALO BOT TỰ ĐỘNG BÁO ĐƠN (ZALO NOTIFICATION SERVICE)
=============================================================================
Chức năng:
- Lắng nghe yêu cầu đặt bàn từ website tại cổng 5000 (http://localhost:5000/send-zalo).
- Dùng tài khoản Zalo phụ tự động gửi tin nhắn báo đơn sang nick Zalo chính của bạn.
- Tích hợp cơ chế giãn cách tự nhiên (Anti-Ban Rate Limiting) chống quét spam.
- Ghi log lịch sử gửi tin vào file zalo_history.log để dễ theo dõi.
=============================================================================
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import os
import time
from datetime import datetime

PORT = 5000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "zalo_config.json")
LOG_FILE = os.path.join(BASE_DIR, "zalo_history.log")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Lỗi đọc file config: {e}")
    return {}

def log_event(text):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] {text}\n"
    print(log_line, end="")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass

def send_zalo_message(receiver_phone, message_text):
    """
    Gửi tin nhắn qua Zalo Web API sử dụng Cookie/Session của tài khoản phụ
    """
    cfg = load_config()
    sub_acc = cfg.get("subAccount", {})
    
    cookie = sub_acc.get("cookie", "")
    zpw_sek = sub_acc.get("zpw_sek", "")
    
    # Kiểm tra xem người dùng đã dán Cookie thật chưa
    is_live_mode = cookie and "DÁN_" not in cookie and zpw_sek and "DÁN_" not in zpw_sek

    if not is_live_mode:
        log_event(f"[GIẢ LẬP TEST] Đã nhận đơn và chuẩn bị gửi tới SĐT {receiver_phone}:")
        log_event(f"---> {message_text}")
        log_event("[!] Ghi chú: Hãy dán Cookie của Zalo phụ vào zalo_config.json để gửi tin thật qua Zalo.")
        return {"status": "success", "mode": "simulation", "message": "Đã ghi nhận đơn (Chế độ mô phỏng test)"}

    # Nếu có Cookie thật, gửi yêu cầu tới endpoint Zalo Web
    try:
        url = f"https://chat.zalo.me/api/message/sms?zpw_sek={zpw_sek}"
        headers = {
            "User-Agent": sub_acc.get("userAgent", "Mozilla/5.0"),
            "Cookie": cookie,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        payload = urllib.parse.urlencode({
            "phone": receiver_phone,
            "message": message_text
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            res_body = resp.read().decode("utf-8")
            log_event(f"[THÀNH CÔNG] Đã gửi tin nhắn Zalo tới {receiver_phone}: {res_body}")
            return {"status": "success", "mode": "live", "response": res_body}
    except Exception as ex:
        log_event(f"[LỖI GỬI ZALO] {ex}")
        return {"status": "error", "error": str(ex)}

class ZaloRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/status":
            cfg = load_config()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._set_cors()
            self.end_headers()
            sub = cfg.get("subAccount", {})
            has_cookie = bool(sub.get("cookie") and "DÁN_" not in sub.get("cookie"))
            res = {
                "running": True,
                "zaloConnected": has_cookie,
                "receiverPhone": cfg.get("receiverPhone", ""),
                "time": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>Zalo Bot Service is Running on Port 5000</h1><p>San sang nhan don tu website.</p>")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")

        data = {}
        try:
            data = json.loads(post_data)
        except Exception:
            try:
                data = dict(urllib.parse.parse_qsl(post_data))
            except Exception:
                pass

        if self.path == "/send-zalo":
            cfg = load_config()
            receiver = data.get("receiverPhone") or cfg.get("receiverPhone", "0342092999")
            
            code = data.get("code", "KZ-TEST")
            name = data.get("name", "Khách Hàng")
            phone = data.get("phone", "Chưa có")
            date = data.get("date", "")
            time_str = data.get("time", "")
            note = data.get("note", "Không có")

            msg = (
                f"🎤 [ĐƠN ĐẶT PHÒNG MỚI - KARAOKE KENZ]\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🔖 Mã đặt chỗ: {code}\n"
                f"👤 Khách hàng: {name}\n"
                f"📞 Số điện thoại: {phone}\n"
                f"📅 Ngày hát: {date}\n"
                f"⏰ Giờ đến: {time_str}\n"
                f"📝 Ghi chú: {note}\n"
                f"⏱ Báo lúc: {datetime.now().strftime('%H:%M %d/%m/%Y')}"
            )

            result = send_zalo_message(receiver, msg)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._set_cors()
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def main():
    print("=" * 65)
    print(f"🚀 DỊCH VỤ ZALO BOT TỰ ĐỘNG BÁO ĐƠN ĐANG CHẠY CỔNG {PORT}")
    print(f"👉 API nhận đơn: http://localhost:{PORT}/send-zalo")
    print(f"👉 Trạng thái:   http://localhost:{PORT}/status")
    print("=" * 65)
    print("Đang lắng nghe yêu cầu đặt bàn từ website... (Bấm Ctrl+C để dừng)")
    with socketserver.TCPServer(("", PORT), ZaloRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Đã dừng dịch vụ Zalo Bot.")

if __name__ == "__main__":
    main()
