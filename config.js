/**
 * =========================================================================
 * FILE CẤU HÌNH TRUNG TÂM (CENTRAL CONFIGURATION) - KARAOKE WEB
 * =========================================================================
 * Bạn chỉ cần sửa thông tin tại file này, toàn bộ website sẽ tự động cập nhật:
 * - Tên quán, chi nhánh, địa chỉ, số hotline, Zalo, WeChat
 * - Danh sách tiện ích, ưu đãi, bảng giá & hình ảnh
 * - Cấu hình nhận thông báo đặt phòng (Lưu trên máy / Telegram Bot)
 * =========================================================================
 */

const SITE_CONFIG = {
  // 1. THÔNG TIN THƯƠNG HIỆU & ĐỊA ĐIỂM
  brand: {
    name: "KARAOKE KENZ",
    branch: "202 TRUNG KÍNH",
    fullName: "Karaoke Kenz Club - 202 Trung Kính",
    tagline: "Hát hết mình, quẩy nhiệt tình",
    description: "30 phòng hát Siêu VIP, âm thanh cực chất, nội thất sang trọng và hiện đại.",
    address: "202 Trung Kính, phường Yên Hoà, Cầu Giấy, Hà Nội",
    areaServed: "Cầu Giấy, Hà Nội",
    openHours: "24/24h",
    googleMapsUrl: "https://www.google.com/maps/search/?api=1&query=Karaoke+Kenz+Club+202+Trung+K%C3%ADnh%2C+Y%C3%AAn+Ho%C3%A0%2C+C%E1%BA%A7u+Gi%E1%BA%A5y%2C+H%C3%A0+N%E1%BB%99i"
  },

  // 2. THÔNG TIN LIÊN HỆ & MẠNG XÃ HỘI
  contact: {
    hotline: "0342 092 999",
    hotlineDisplay: "0342 092 999",
    zalo: "0342 092 999",
    wechat: "wxid_0oxdncgq75g312",
    wechatQrImage: "assets/images/wechat-qr.png",
    email: "contact@karaokekenz.com"
  },

  // 3. CẤU HÌNH ĐẶT PHÒNG (BOOKING ENGINE)
  booking: {
    codePrefix: "KZ-",             // Tiền tố mã đặt phòng: KZ-6839
    requireConfirm: true,          // Hiển thị thông báo nhân viên sẽ gọi xác nhận
    
    // Chế độ lưu trữ: 
    // - "local": Lưu trên trình duyệt máy bạn (xem qua trang admin.html) -> Hoàn hảo cho Win Test
    // - "telegram": Vừa lưu máy vừa bắn thông báo trực tiếp về Telegram cá nhân
    storageMode: "local",

    // Cấu hình Telegram Bot (Nếu bạn muốn nhận thông báo tức thì trên điện thoại):
    // 1. Tạo bot qua @BotFather lấy Token
    // 2. Chat với @userinfobot để lấy Chat ID
    telegram: {
      enabled: true,               // ĐÃ KÍCH HOẠT THÀNH CÔNG!
      botToken: "8100028873:AAHaCHDY3ufKX7hB1h4Enm65faIexNczM7o",
      chatId: "-5167215010"       // Chat ID Nhóm Telegram của quán
    },

    // Cấu hình Zalo Bot tự động kết nối qua máy chủ cổng 80
    zaloBot: {
      enabled: true,               // Bật thông báo qua Zalo song song với Telegram
      serviceUrl: (typeof window !== "undefined" && window.location.port === "8123") 
        ? "http://192.168.1.245:80/send-zalo" 
        : "/send-zalo"             // Chạy cùng cổng 80 với web, chuyển tiếp đến Zalo Bot (3000)
    }
  },

  // 4. TIỆN ÍCH MIỄN PHÍ CỦA QUÁN
  amenities: [
    "Wi-Fi miễn phí",
    "Chỗ đỗ ô tô & xe máy rộng rãi",
    "Trang trí sinh nhật theo yêu cầu",
    "Nhân viên biết tiếng Trung (中文)",
    "Xuất hoá đơn VAT",
    "Hệ thống phòng cách âm 100%"
  ],

  // 5. CÁC ĐẶC QUYỀN & ƯU ĐÃI NỔI BẬT
  perks: [
    {
      icon: "🍉",
      title: "Tặng hoa quả",
      desc: "Đĩa trái cây tươi đầy đặn cho phòng của bạn."
    },
    {
      icon: "🎂",
      title: "Tặng bánh sinh nhật",
      desc: "Ghi chú khi đặt phòng trước để quán chuẩn bị trang trí chu đáo."
    },
    {
      icon: "🎁",
      title: "Và nhiều ưu đãi hấp dẫn khác",
      desc: "Gọi hotline để được tư vấn gói phòng và ưu đãi theo đoàn."
    }
  ],

  // 6. DANH SÁCH ĐÁNH GIÁ 5 SAO (GOOGLE MAPS REVIEWS)
  reviews: [
    {
      name: "Lê",
      time: "2 tuần trước",
      stars: 5,
      content: "Sinh Nhật hát ở đây rất oki giá hợp lý nv chu đáo không thái độ làm việc chuyên nghiệp",
      meta: "Đồ ăn 5 · Dịch vụ 5 · Bầu không khí 5"
    },
    {
      name: "MinhQuân Nguyễn",
      time: "1 tuần trước",
      stars: 5,
      content: "quán sạch sẽ nv phục vụ tốt chuyên nghiệp",
      reply: "Cảm ơn quý khách đã đánh giá 5 sao kenz Club"
    },
    {
      name: "Lan Lê",
      time: "3 tuần trước",
      stars: 5,
      content: "Trải nghiệm rất tốt giá hợp lý",
      meta: "Đồ ăn 5 · Dịch vụ 5 · Bầu không khí 5"
    },
    {
      name: "Tuấn linh Lê",
      time: "2 tuần trước",
      stars: 5,
      content: "Nhân viên xinh, phục vụ nhiệt tình",
      meta: "Đồ ăn 5 · Dịch vụ 5 · Bầu không khí 5"
    }
  ],

  // 7. CÂU HỎI THƯỜNG GẶP (FAQ)
  faq: [
    {
      q: "Đặt phòng có mất phí không?",
      a: "Không. Bạn chỉ cần để lại họ tên, số điện thoại và giờ muốn hát. Quán sẽ gọi hoặc nhắn Zalo để xác nhận và giữ phòng."
    },
    {
      q: "Huỷ hoặc đổi giờ thế nào?",
      a: "Nhắn Zalo hoặc gọi hotline trước giờ hẹn ít nhất 1 tiếng, kèm mã đặt phòng để nhân viên hỗ trợ đổi giờ hoặc bảo lưu."
    },
    {
      q: "Quán có phòng cho nhóm đông không?",
      a: "Có. Quán có hệ thống 30 phòng: phòng gia đình cho nhóm nhỏ, phòng Party và phòng Siêu VIP cho tiệc đông 20-50 người. Hãy báo số lượng khách khi đặt để quán xếp phòng phù hợp nhất."
    },
    {
      q: "Có mang bánh kem sinh nhật vào được không?",
      a: "Được. Bạn có thể tự mang bánh kem hoặc báo trước khi đặt phòng để quán tặng bánh và hỗ trợ trang trí tiệc."
    }
  ]
};

// Gắn chắc chắn vào window object để toàn bộ script khác đều truy cập được
if (typeof window !== "undefined") {
  window.SITE_CONFIG = SITE_CONFIG;
}

// Đóng băng object để tránh vô tình bị ghi đè runtime
if (typeof Object.freeze === "function") {
  Object.freeze(SITE_CONFIG);
}
