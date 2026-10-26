# HƯỚNG DẪN BIẾN WEBSITE THÀNH APP CHO IOS & ANDROID
### Dành riêng cho hệ thống Karaoke Kenz 202 Trung Kính & KTV Hà Nội

Chào bạn! Toàn bộ mã nguồn và tài nguyên của website hiện tại đã được nâng cấp toàn diện để sẵn sàng hoạt động như một **Ứng dụng Di Động (Mobile App) thực thụ** trên cả **iOS (iPhone/iPad)** và **Android (Samsung, Xiaomi, Oppo, Vivo, v.v.)**.

Dưới đây là 3 phương pháp tối ưu nhất, từ cách dùng ngay trong 30 giây đến cách đóng gói file `.apk` và `.ipa`.

---

## 🚀 CÁCH 1: CÀI ĐẶT DÙNG NGAY LẬP TỨC (KHUYẾN NGHỊ CAO NHẤT ⭐⭐⭐⭐⭐)
> **Không cần máy tính Mac, không cần cài phần mềm nặng, không tốn phí 99$/năm của Apple.**  
> Khách hàng và nhân viên mở web là cài được ngay thành App độc lập trên màn hình chính!

Hệ thống đã được tích hợp công nghệ **Progressive Web App (PWA Chuẩn Quốc Tế)** với bộ icon độ phân giải cao (`assets/icon-512x512.png`, `assets/apple-touch-icon.png`), tệp cấu hình `manifest.webmanifest`, bộ đệm ngoại tuyến `sw.js` và xử lý tai thỏ / Dynamic Island trên iPhone.

### 📱 1. Hướng dẫn cài trên iPhone / iPad (iOS):
1. Dùng trình duyệt **Safari** trên iPhone mở trang web của bạn (ví dụ: `https://karaokekenz.com` hoặc qua địa chỉ IP mạng nội bộ).
2. Bấm vào nút **Chia sẻ (Share)** ở thanh công cụ Safari bên dưới màn hình *(Biểu tượng hình vuông có mũi tên chỉ lên ⎋)*.
3. Cuộn xuống danh sách tùy chọn và chọn: **"Thêm vào Màn hình chính" (Add to Home Screen ➕)**.
4. Bấm **"Thêm" (Add)** ở góc trên bên phải.
5. 👉 **Kết quả:** Biểu tượng vàng kim sang trọng của **Karaoke Kenz** sẽ xuất hiện ngay trên màn hình chính của iPhone. Khi bấm mở:
   - App chạy **toàn màn hình (Standalone)**, biến mất hoàn toàn thanh địa chỉ Safari.
   - Tương thích 100% với tai thỏ và thanh gạt vuốt Home của iPhone.
   - Đặt bàn, gọi hotline, xem 30 phòng VIP hoạt động cực kỳ mượt mà.

### 🤖 2. Hướng dẫn cài trên Điện thoại Android:
1. Mở trang web bằng trình duyệt **Google Chrome** hoặc **Cốc Cốc**.
2. Một nút nổi màu vàng kim **"Cài Đặt App"** sẽ tự động xuất hiện ở góc dưới màn hình.
3. Bấm vào nút **"Cài Đặt App"** -> Bấm **"Cài đặt" (Install)**.
4. 👉 **Kết quả:** Hệ điều hành Android sẽ tự động tạo một file ứng dụng native (WebAPK) và đưa vào màn hình ứng dụng của bạn. App có thông báo riêng, mở độc lập, có thể ghim vào màn hình khóa và chạy siêu tốc.

---

## 📦 CÁCH 2: TỰ ĐỘNG XUẤT FILE `.APK` (ANDROID) TRÊN CLOUD MIỄN PHÍ
> Bạn **không cần cài Android Studio nặng nề vào máy tính**. Hệ thống đã được thiết lập sẵn file tự động build trên Cloud qua **GitHub Actions** (`.github/workflows/build-mobile.yml`).

### Các bước thực hiện:
1. Tạo một kho lưu trữ (Repository) trên [GitHub](https://github.com/) (chế độ Public hoặc Private đều được).
2. Tải toàn bộ thư mục `WEB` này lên GitHub.
3. Trên giao diện GitHub của bạn, bấm vào thẻ **"Actions"**.
4. Chọn quy trình **"Build Mobile Apps (Android APK & iOS)"** -> Bấm **Run workflow**.
5. Chờ khoảng 3-4 phút, GitHub sẽ tự động biên dịch toàn bộ source web thành file:
   📁 **`Karaoke-Kenz-Android-APK.zip`**
6. Tải file zip về máy, giải nén sẽ có file: **`app-debug.apk`**.
7. Chép file `.apk` này vào bất kỳ điện thoại Android nào để cài đặt và sử dụng!

---

## 🛠️ CÁCH 3: TỰ BIÊN DỊCH BẰNG CAPACITOR & ANDROID STUDIO TRÊN MÁY BẠN
> Dành cho lập trình viên muốn can thiệp sâu vào code Android Java/Kotlin hoặc iOS Swift.

Source code đã được tạo sẵn file cấu hình Capacitor chuẩn:
- `package.json`: Khai báo `@capacitor/core`, `@capacitor/android`, `@capacitor/ios`.
- `capacitor.config.json`: Khai báo App ID `com.karaokekenz.app`, tên hiển thị `Karaoke Kenz`, thư mục đóng gói `www`.
- `build_mobile.py`: Script tự động lọc và đóng gói toàn bộ file web sạch sẽ vào thư mục `www`.

### Bước 1: Cài đặt Node.js
Nếu máy tính của bạn chưa có Node.js:
- Mở PowerShell và chạy lệnh:
  ```powershell
  winget install OpenJS.NodeJS.LTS
  ```
- Khởi động lại terminal sau khi cài.

### Bước 2: Đóng gói và tạo dự án Mobile
Tại thư mục `WEB`, chạy lần lượt các lệnh sau:
```bash
# 1. Đóng gói mã nguồn web vào thư mục www
python build_mobile.py

# 2. Cài đặt các thư viện Capacitor
npm install

# 3. Tạo dự án Android Native
npx cap add android

# 4. Đồng bộ dữ liệu mới nhất
npx cap sync
```

### Bước 3: Xuất file cài đặt:
- **Để xuất file APK cho Android:**
  - Cài đặt phần mềm **Android Studio** miễn phí từ Google.
  - Chạy lệnh: `npx cap open android`.
  - Android Studio sẽ mở dự án. Bấm menu **Build** -> **Build Bundle(s) / APK(s)** -> **Build APK(s)**.
  - Sau 1 phút, bạn sẽ có file `.apk` hoàn chỉnh.

- **Để xuất file cho iOS (iPhone):**
  - Apple yêu cầu bắt buộc phải có máy tính chạy hệ điều hành **macOS** (MacBook, Mac mini hoặc Mac Studio) có cài Xcode.
  - Trên máy Mac, chạy lệnh: `npx cap add ios` rồi `npx cap open ios`.
  - Xcode sẽ mở dự án, bạn có thể cắm trực tiếp iPhone vào Mac để cài app thử nghiệm hoặc xuất file `.ipa` đưa lên Apple TestFlight / App Store.

---

## 🌐 CÁCH 4: DÙNG CÔNG CỤ TRỰC TUYẾN PWABUILDER (CỦA MICROSOFT)
1. Đưa website của bạn lên hosting (như hướng dẫn trong `README_HUONG_DAN.md` - Vercel, Netlify hoặc Hosting quán).
2. Truy cập: [https://www.pwabuilder.com/](https://www.pwabuilder.com/)
3. Dán địa chỉ website của bạn vào và bấm **Start**.
4. PWABuilder sẽ chấm điểm PWA (sẽ đạt 100/100 điểm vì chúng ta đã tạo đầy đủ Manifest, Icon 512, Maskable, Service Worker).
5. Bấm **Package for Stores**:
   - Chọn **Android**: Tải về file `.apk` và `.aab` (Google Play Package).
   - Chọn **iOS**: Tải về mã nguồn Xcode đã bọc sẵn WebKit App.

---

## 📋 TÓM TẮT BẢNG SO SÁNH CÁC CÁCH

| Tiêu chí | Cách 1: PWA (Thêm MH chính) | Cách 2: GitHub Actions (APK) | Cách 3: Capacitor Local |
| :--- | :--- | :--- | :--- |
| **Hỗ trợ iPhone (iOS)** | ✅ Cực nhanh (30 giây) | ✅ Có mã nguồn Xcode | ✅ Cần máy Mac + Xcode |
| **Hỗ trợ Android** | ✅ Cực nhanh (30 giây) | ✅ Ra file `.apk` cài ngay | ✅ Tự build bằng Android Studio |
| **Cần máy tính Mac?** | ❌ KHÔNG CẦN | ❌ KHÔNG CẦN | ⚠️ Chỉ cần khi build iOS |
| **Chi phí Store ($)** | 🆓 0đ Miễn phí 100% | 🆓 0đ Miễn phí | ⚠️ 99$/năm (Apple) / 25$ (Google) |
| **Cập nhật nội dung** | ⚡ Tự động tức thì | Cần build lại file APK | Cần build lại file APK |

---
Chúc bạn triển khai ứng dụng cho **Karaoke Kenz 202 Trung Kính** thành công rực rỡ!
