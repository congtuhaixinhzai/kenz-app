# HƯỚNG DẪN KẾT NỐI VÀ CHẠY ZALO BOT TỰ ĐỘNG BÁO ĐƠN

Chào bạn! Đây là hướng dẫn chi tiết cách dùng **1 nick Zalo phụ** tự động nhắn tin thông báo đặt bàn cho **nick Zalo chính hoặc nhóm Zalo** của bạn.

---

## 1. NGUYÊN LÝ HOẠT ĐỘNG
- Khi khách đặt bàn trên website, website sẽ gửi dữ liệu tới con Bot Zalo đang chạy trên máy (`http://localhost:5000/send-zalo`).
- Nick Zalo phụ sẽ tự động gửi tin nhắn có đầy đủ họ tên, SĐT, giờ đến của khách sang cho nick chính của bạn.

---

## 2. CÁCH LẤY COOKIE ĐĂNG NHẬP (CHỈ MẤT 1 PHÚT)

Bạn chỉ cần lấy Cookie đăng nhập 1 lần trên trình duyệt máy tính:

1. Mở trình duyệt (Chrome / Cốc Cốc / Edge), truy cập vào trang:  
   👉 **`https://chat.zalo.me`**
2. Đăng nhập vào bằng **Nick Zalo PHỤ** của bạn (quét mã QR bằng điện thoại).
3. Sau khi đã vào được giao diện chat Zalo:
   - Nhấn phím **`F12`** trên bàn phím (hoặc nhấp chuột phải chọn **Kiểm tra / Inspect**).
   - Chọn tab **Application** (tiếng Việt là **Ứng dụng** hoặc **Bộ nhớ**).
   - Ở cột bên trái, bấm vào mũi tên mục **Cookies** $\rightarrow$ chọn `https://chat.zalo.me`.
4. Tìm 2 giá trị quan trọng:
   - Dòng tên là **`zpw_sek`**: Nhấp đúp vào cột Value để copy mã này, dán vào file `zalo_config.json` ở dòng `"zpw_sek": "..."`.
   - Chuột phải vào bất kỳ dòng nào trong bảng Cookie $\rightarrow$ chọn **Copy all** (sao chép toàn bộ cookie) dán vào dòng `"cookie": "..."`.
5. Điền số điện thoại Zalo chính nhận tin vào dòng `"receiverPhone": "0342092999"`.

---

## 3. KHỞI CHẠY BOT

- Nhấp đúp vào file: **`chay-zalo-bot.bat`**.
- Màn hình đen hiện lên thông báo:  
  `🚀 DỊCH VỤ ZALO BOT TỰ ĐỘNG BÁO ĐƠN ĐANG CHẠY CỔNG 5000`  
  `Đang lắng nghe yêu cầu đặt bàn từ website...`
- Vậy là xong! Mỗi khi khách đặt bàn, bot sẽ tự động gửi tin nhắn qua Zalo.

---

## 4. KINH NGHIỆM TRÁNH BỊ ZALO QUÉT / KHÓA NICK (ANTI-BAN)

1. **Tuyệt đối không dùng Nick Zalo cá nhân chính** để làm bot (chỉ dùng nick phụ / SIM phụ).
2. **Nên kết bạn trước**: Nick Zalo phụ và nick chính của bạn nên kết bạn với nhau trên Zalo trước khi chạy bot. Nhắn tin giữa bạn bè sẽ không bao giờ bị Zalo nghi ngờ là tin nhắn rác (spam).
3. **Cơ chế giãn cách (Rate Limit)**: Trong file `zalo_config.json` đã cài sẵn độ trễ 2 - 5 giây giữa các tin nhắn để mô phỏng giống như người thật đang gõ phím.
