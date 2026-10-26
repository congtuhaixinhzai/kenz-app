# HƯỚNG DẪN SỬ DỤNG VÀ TÙY CHỈNH SOURCE CODE WEB KARAOKE

Chào bạn! Bộ mã nguồn website Karaoke này được thiết kế dựa trên phong cách cao cấp của **Karaoke Kenz 202 Trung Kính** với cấu trúc **Clean Code, Module Hóa và Tối Ưu Tối Đa Cho Windows Test**.

---

## 1. CÁCH CHẠY THỬ NGHIỆM TRÊN WINDOWS (WIN TEST)

Bạn có thể chạy thử theo bất kỳ cách nào sau đây:

### 👉 Cách 1: Nhanh nhất (Không cần cài phần mềm gì cả)
- Nhấp đúp chuột (Double-click) trực tiếp vào file **`index.html`**.
- Trang web sẽ mở ngay lập tức trên trình duyệt mặc định của bạn (Chrome, Cốc Cốc, Edge). Toàn bộ hiệu ứng ánh sáng vũ trường, chuyển ngữ Việt - Trung và form đặt bàn hoạt động trơn tru 100%.

### 👉 Cách 2: Chạy Server Cục Bộ (Khuyến khích)
- Nhấp đúp chuột vào file **`start-test.bat`**.
- File sẽ tự động kiểm tra xem máy bạn có cài sẵn `Node.js` hoặc `Python` hay không để mở cổng `http://localhost:3000`. Nếu không có, file sẽ tự động mở trang web giúp bạn.

---

## 2. KIỂM TRA ĐƠN ĐẶT BÀN CỦA KHÁCH

Khi bạn hoặc khách bấm **Đặt phòng ngay** trên web:
1. Hệ thống sẽ tự động tạo một **Mã đặt phòng** (ví dụ: `KZ-7821`) kèm thông tin tóm tắt để khách chụp màn hình gửi Zalo/gọi hotline.
2. Dữ liệu đơn sẽ được lưu trữ an toàn trong máy tính của bạn.
3. Để xem danh sách toàn bộ khách đã đặt phòng khi chạy test:
   - Truy cập trang: **`admin.html`** (hoặc link *Quản trị test* ở góc dưới cùng chân trang web).
   - Tại đây bạn có thể: Xem họ tên, SĐT, ngày giờ đến, ghi chú, đổi trạng thái sang "Đã xác nhận", xuất ra file Excel (CSV) hoặc xóa đơn test.

---

## 3. CÁCH SỬA THÔNG TIN QUÁN (CONFIG-FIRST)

Bạn **KHÔNG CẦN** mò vào các file HTML phức tạp. Tất cả thông tin chỉ nằm trong file:
📁 **`config.js`**

| Thông tin muốn sửa | Dòng trong `config.js` | Hướng dẫn |
| :--- | :--- | :--- |
| **Tên quán & Chi nhánh** | `brand.name`, `brand.branch` | Điền tên quán của bạn |
| **Hotline gọi điện** | `contact.hotline` | Điền số điện thoại quán |
| **Số Zalo** | `contact.zalo` | Điền số Zalo để khách bấm chat |
| **WeChat ID** | `contact.wechat` | Điền WeChat ID để khách quốc tế kết bạn |
| **Địa chỉ quán** | `brand.address` | Điền địa chỉ quán |
| **Link Google Maps** | `brand.googleMapsUrl` | Dán link chia sẻ vị trí Google Maps của quán |
| **Danh sách ưu đãi** | `perks` | Thêm bớt các gói quà tặng (hoa quả, bánh sinh nhật...) |
| **Câu hỏi thường gặp** | `faq` | Thêm/sửa câu hỏi và câu trả lời |

---

## 4. CÁCH THAY ẢNH CỦA QUÁN BẠN

Toàn bộ ảnh được đặt trong thư mục: `assets/images/`
Bạn chỉ cần lấy ảnh chụp thực tế quán của bạn và đổi tên trùng với các file sau:

- `hero-facade.jpg`: Ảnh chụp mặt tiền quán (ảnh lớn ở đầu trang).
- `room-vip-sofa.jpg`: Ảnh phòng VIP sofa da.
- `room-led-party.jpg`: Ảnh phòng dài màn hình LED tiệc sôi động.
- `room-banquet.jpg`: Ảnh phòng bàn tiệc sinh nhật.
- `room-red-luxury.jpg`: Ảnh phòng phong cách tông đỏ quý phái.
- `fruit-plate.jpg`: Ảnh đĩa hoa quả / đồ uống.
- `promo-banner.jpg`: Ảnh poster chương trình khuyến mại của quán.
- `wechat-qr.png`: Ảnh chụp mã QR WeChat của quán bạn.

---

## 5. TÙY CHỌN: NHẬN THÔNG BÁO VỀ TELEGRAM ĐIỆN THOẠI

Nếu bạn muốn khi khách bấm đặt phòng trên web, **điện thoại của bạn ting ting báo tin nhắn ngay lập tức**:
1. Mở ứng dụng Telegram, tìm bot `@BotFather` để tạo 1 bot miễn phí và lấy mã **Bot Token**.
2. Tìm bot `@userinfobot` để lấy **Chat ID** của bạn.
3. Mở file `config.js`, tìm mục `telegram` và điền:
```javascript
telegram: {
  enabled: true,
  botToken: "MÃ_TOKEN_CỦA_BẠN",
  chatId: "CHAT_ID_CỦA_BẠN"
}
```
Xong! Từ nay mỗi khi có khách đặt bàn, thông tin sẽ gửi thẳng về tin nhắn Telegram của bạn!

---

## 6. HƯỚNG DẪN ĐƯA LÊN MẠNG (UP WEB THẬT)

Website được xây dựng theo chuẩn Web tĩnh (Static Web), nghĩa là:
- **Không cần cài đặt Database MySQL phức tạp**.
- **Tốc độ tải trang siêu nhanh (gần như 0 giây)**.
- Bạn có thể upload toàn bộ các file trong thư mục này lên bất kỳ hosting nào:
  - **cPanel / DirectAdmin / Hostinger**: Upload tất cả file vào thư mục `public_html`.
  - **Vercel / Netlify / Cloudflare Pages / GitHub Pages**: Kéo thả thư mục vào là có ngay website miễn phí hoạt động 24/7 với chứng chỉ bảo mật SSL (https) miễn phí.

---

## 7. CÀI ĐẶT THÀNH APP DI ĐỘNG CHO IPHONE (IOS) VÀ ANDROID

Toàn bộ hệ thống đã được tích hợp chuẩn **PWA & Capacitor** để cài đặt trực tiếp thành ứng dụng di động:
- **Trên iPhone (iOS)**: Mở Safari -> Bấm nút Chia sẻ (hình vuông mũi tên lên) -> Chọn **"Thêm vào Màn hình chính"**. App sẽ xuất hiện độc lập, mở toàn màn hình như tải từ App Store.
- **Trên Android**: Bấm nút **"Cài Đặt App"** nổi màu vàng kim để cài WebAPK vào máy.
- **Xuất file APK / IPA**: Đã có sẵn cấu hình Capacitor, script `build_mobile.py` và workflow GitHub Actions.

👉 **Xem hướng dẫn chi tiết từng bước tại:** [`HUONG_DAN_CAI_APP_IOS_ANDROID.md`](file:///c:/Users/Home_Family/Desktop/WEB/HUONG_DAN_CAI_APP_IOS_ANDROID.md)

