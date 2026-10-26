/**
 * =========================================================================
 * LIVE SOCIAL PROOF BOOKING NOTIFICATIONS - LUXURY EDITION
 * =========================================================================
 * - Tự động bơm CSS trực tiếp (Self-contained Inline Shield) - Không phụ thuộc Cache.
 * - Khung viền kép phát sáng Neon Vàng Hổ Phách & Hồng Ruby đẳng cấp KTV VIP.
 * - Xuất hiện trên MỌI TRANG (Trang chủ, KTV Hà Nội, Trang chi tiết quán, Tin tức).
 * - Tự động nhận diện cơ sở của trang hiện tại để tạo hiệu ứng Social Proof chuẩn xác.
 * - Cứ mỗi 30 giây hiển thị 1 lần, xuất hiện lần đầu sau 2.5s khi vào trang.
 * - Hỗ trợ chuẩn SEO, Accessibility aria-live="polite", không ảnh hưởng CLS (Layout Shift).
 * =========================================================================
 */

(function () {
  'use strict';

  // Cấu hình thời gian
  var INTERVAL_SEC = 30; // Cứ mỗi 30 giây hiện 1 lần theo yêu cầu
  var SHOW_DURATION_MS = 6500; // Hiển thị trong 6.5 giây
  var INITIAL_DELAY_MS = 2500; // Xuất hiện lần đầu sau khi tải trang 2.5 giây

  // 1. TỰ ĐỘNG BƠM CSS NỘI BỘ (CHỐNG LỖI CACHE TRÌNH DUYỆT 100%)
  function injectToastStyles() {
    if (document.getElementById('lbt-toast-injected-css')) return;
    var css = [
      '#live-booking-toast.live-booking-toast {',
      '  position: fixed !important;',
      '  bottom: 26px !important;',
      '  left: 26px !important;',
      '  z-index: 999999 !important;',
      '  max-width: 410px !important;',
      '  width: calc(100vw - 52px) !important;',
      '  background: linear-gradient(135deg, rgba(28, 22, 58, 0.97) 0%, rgba(13, 10, 30, 0.98) 100%) !important;',
      '  border: 1.5px solid rgba(255, 183, 3, 0.75) !important;',
      '  border-radius: 18px !important;',
      '  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.85), 0 0 25px rgba(255, 183, 3, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;',
      '  backdrop-filter: blur(20px) !important;',
      '  -webkit-backdrop-filter: blur(20px) !important;',
      '  overflow: hidden !important;',
      '  cursor: pointer !important;',
      '  opacity: 0 !important;',
      '  transform: translateY(30px) scale(0.92) !important;',
      '  pointer-events: none !important;',
      '  transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1), transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s, box-shadow 0.3s !important;',
      '  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;',
      '  box-sizing: border-box !important;',
      '}',
      '#live-booking-toast.live-booking-toast.active {',
      '  opacity: 1 !important;',
      '  transform: translateY(0) scale(1) !important;',
      '  pointer-events: auto !important;',
      '}',
      '#live-booking-toast.live-booking-toast.hiding {',
      '  opacity: 0 !important;',
      '  transform: translateY(25px) scale(0.94) !important;',
      '  pointer-events: none !important;',
      '}',
      '#live-booking-toast.live-booking-toast:hover {',
      '  border-color: #ffd166 !important;',
      '  box-shadow: 0 22px 55px rgba(0, 0, 0, 0.9), 0 0 35px rgba(255, 183, 3, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;',
      '}',
      '.lbt-body {',
      '  position: relative !important;',
      '  display: flex !important;',
      '  align-items: flex-start !important;',
      '  gap: 14px !important;',
      '  padding: 16px 36px 16px 16px !important;',
      '  box-sizing: border-box !important;',
      '}',
      '.lbt-close {',
      '  position: absolute !important;',
      '  top: 8px !important;',
      '  right: 10px !important;',
      '  background: rgba(255, 255, 255, 0.08) !important;',
      '  border: 1px solid rgba(255, 255, 255, 0.15) !important;',
      '  color: #c5c2de !important;',
      '  font-size: 1.35rem !important;',
      '  line-height: 1 !important;',
      '  cursor: pointer !important;',
      '  width: 26px !important;',
      '  height: 26px !important;',
      '  display: grid !important;',
      '  place-items: center !important;',
      '  border-radius: 50% !important;',
      '  transition: all 0.2s ease !important;',
      '  padding: 0 !important;',
      '  outline: none !important;',
      '  box-shadow: none !important;',
      '  -webkit-appearance: none !important;',
      '  appearance: none !important;',
      '}',
      '.lbt-close:hover {',
      '  color: #fff !important;',
      '  background: rgba(255, 77, 106, 0.55) !important;',
      '  border-color: #ff4d6a !important;',
      '}',
      '.lbt-avatar {',
      '  position: relative !important;',
      '  flex: none !important;',
      '}',
      '.lbt-avatar-ring {',
      '  width: 48px !important;',
      '  height: 48px !important;',
      '  border-radius: 50% !important;',
      '  background: linear-gradient(135deg, rgba(255, 183, 3, 0.25), rgba(255, 77, 106, 0.25)) !important;',
      '  border: 1.5px solid #ffb703 !important;',
      '  display: grid !important;',
      '  place-items: center !important;',
      '  box-shadow: 0 0 14px rgba(255, 183, 3, 0.35) !important;',
      '}',
      '.lbt-avatar-icon {',
      '  font-size: 1.45rem !important;',
      '  animation: lbtBounce 2.2s infinite ease-in-out !important;',
      '}',
      '@keyframes lbtBounce {',
      '  0%, 100% { transform: translateY(0); }',
      '  50% { transform: translateY(-3px); }',
      '}',
      '.lbt-status-dot {',
      '  position: absolute !important;',
      '  bottom: 1px !important;',
      '  right: 1px !important;',
      '  width: 12px !important;',
      '  height: 12px !important;',
      '  background: #06d6a0 !important;',
      '  border: 2px solid #14102c !important;',
      '  border-radius: 50% !important;',
      '  box-shadow: 0 0 8px #06d6a0 !important;',
      '  animation: lbtPulse 1.8s infinite !important;',
      '}',
      '@keyframes lbtPulse {',
      '  0% { transform: scale(1); opacity: 1; }',
      '  50% { transform: scale(1.25); opacity: 0.8; }',
      '  100% { transform: scale(1); opacity: 1; }',
      '}',
      '.lbt-content {',
      '  flex: 1 !important;',
      '  min-width: 0 !important;',
      '}',
      '.lbt-row-head {',
      '  display: flex !important;',
      '  align-items: center !important;',
      '  justify-content: space-between !important;',
      '  gap: 8px !important;',
      '  margin-bottom: 4px !important;',
      '  flex-wrap: wrap !important;',
      '}',
      '.lbt-customer {',
      '  color: #ffd166 !important;',
      '  font-size: 0.95rem !important;',
      '  font-weight: 800 !important;',
      '  letter-spacing: -0.01em !important;',
      '}',
      '.lbt-badge-verified {',
      '  background: rgba(6, 214, 160, 0.16) !important;',
      '  border: 1px solid rgba(6, 214, 160, 0.45) !important;',
      '  color: #06d6a0 !important;',
      '  font-size: 0.72rem !important;',
      '  font-weight: 700 !important;',
      '  padding: 2px 8px !important;',
      '  border-radius: 999px !important;',
      '  white-space: nowrap !important;',
      '}',
      '.lbt-action {',
      '  font-size: 0.86rem !important;',
      '  color: #dedbf2 !important;',
      '  margin-bottom: 3px !important;',
      '  line-height: 1.4 !important;',
      '}',
      '.lbt-action b {',
      '  color: #ffffff !important;',
      '  font-weight: 700 !important;',
      '}',
      '.lbt-venue {',
      '  font-size: 0.82rem !important;',
      '  color: #dedbf2 !important;',
      '  margin-bottom: 5px !important;',
      '  white-space: nowrap !important;',
      '  overflow: hidden !important;',
      '  text-overflow: ellipsis !important;',
      '}',
      '.lbt-venue b {',
      '  color: #ff758c !important;',
      '  font-weight: 700 !important;',
      '}',
      '.lbt-meta {',
      '  display: flex !important;',
      '  align-items: center !important;',
      '  gap: 8px !important;',
      '  font-size: 0.76rem !important;',
      '  color: #aaa3c8 !important;',
      '  flex-wrap: wrap !important;',
      '}',
      '.lbt-slot {',
      '  color: #4cc9f0 !important;',
      '  font-weight: 600 !important;',
      '}',
      '.lbt-sep {',
      '  color: rgba(255, 255, 255, 0.25) !important;',
      '}',
      '.lbt-time {',
      '  color: #aaa3c8 !important;',
      '}',
      '.lbt-progress {',
      '  height: 3.5px !important;',
      '  background: rgba(255, 255, 255, 0.08) !important;',
      '  width: 100% !important;',
      '}',
      '.lbt-progress-bar {',
      '  height: 100% !important;',
      '  background: linear-gradient(90deg, #ffb703, #ff4d6a) !important;',
      '  width: 100% !important;',
      '  transform-origin: left center !important;',
      '}',
      '@keyframes lbtProgress {',
      '  from { transform: scaleX(1); }',
      '  to { transform: scaleX(0); }',
      '}',
      '@media (max-width: 600px) {',
      '  #live-booking-toast.live-booking-toast {',
      '    bottom: calc(74px + env(safe-area-inset-bottom, 14px)) !important;',
      '    left: 10px !important;',
      '    right: 10px !important;',
      '    max-width: calc(100vw - 20px) !important;',
      '    width: auto !important;',
      '    box-sizing: border-box !important;',
      '  }',
      '}'
    ].join('\n');

    var styleEl = document.createElement('style');
    styleEl.id = 'lbt-toast-injected-css';
    styleEl.textContent = css;
    document.head.appendChild(styleEl);
  }

  // =========================================================================
  // 2. KHO DỮ LIỆU ĐA DẠNG KHỔNG LỒ (HÀNG TRĂM BIẾN THỂ THỰC TẾ)
  // =========================================================================

  // Danh sách hơn 60 khách hàng Việt Nam thực tế
  var VN_CUSTOMERS = [
    { name: 'Anh Tuấn', phone: '098***3819' },
    { name: 'Chị Phương Linh', phone: '091***7724' },
    { name: 'Anh Hoàng Long', phone: '034***9912' },
    { name: 'Chị Ngọc Mai', phone: '097***5568' },
    { name: 'Anh Minh Đức', phone: '090***6341' },
    { name: 'Chị Thanh Hằng', phone: '093***8215' },
    { name: 'Anh Quốc Bảo', phone: '088***4190' },
    { name: 'Anh Hải Đăng', phone: '096***1833' },
    { name: 'Chị Thu Thảo', phone: '094***6782' },
    { name: 'Anh Việt Dũng', phone: '039***5027' },
    { name: 'Anh Quang Huy', phone: '098***6632' },
    { name: 'Chị Diệu Linh', phone: '091***4428' },
    { name: 'Anh Thành Nam', phone: '090***9183' },
    { name: 'Chị Bích Phương', phone: '097***2219' },
    { name: 'Anh Tiến Đạt', phone: '086***5581' },
    { name: 'Chị Hà My', phone: '038***7742' },
    { name: 'Anh Trung Kiên', phone: '093***1105' },
    { name: 'Chị Yến Nhi', phone: '089***8821' },
    { name: 'Anh Khánh Toàn', phone: '094***3367' },
    { name: 'Chị Mai Anh', phone: '096***8890' },
    { name: 'Anh Hữu Thắng', phone: '098***1245' },
    { name: 'Chị Thu Trang', phone: '091***9901' },
    { name: 'Anh Duy Anh', phone: '090***5532' },
    { name: 'Chị Kim Ngân', phone: '088***6678' },
    { name: 'Anh Trọng Nhân', phone: '097***4321' },
    { name: 'Chị Quỳnh Chi', phone: '035***8912' },
    { name: 'Anh Đức Thịnh', phone: '093***7743' },
    { name: 'Chị Lan Anh', phone: '086***1209' },
    { name: 'Anh Việt Hoàng', phone: '094***8823' },
    { name: 'Chị Hồng Nhung', phone: '098***9921' },
    { name: 'Anh Duy Hưng', phone: '091***3377' },
    { name: 'Chị Thảo Nguyên', phone: '090***2266' },
    { name: 'Anh Thanh Tùng', phone: '097***1155' },
    { name: 'Chị Minh Châu', phone: '088***4499' },
    { name: 'Anh Thế Anh', phone: '039***8811' },
    { name: 'Chị Thùy Dương', phone: '096***7733' },
    { name: 'Anh Văn Thành', phone: '094***5511' },
    { name: 'Chị Thùy Linh', phone: '093***6622' },
    { name: 'Anh Quốc Huy', phone: '098***4488' },
    { name: 'Chị Cẩm Tú', phone: '091***5500' },
    { name: 'Anh Mạnh Hùng', phone: '090***7799' },
    { name: 'Chị Hương Giang', phone: '097***8866' },
    { name: 'Anh Ngọc Sơn', phone: '086***9933' },
    { name: 'Chị Bảo Trâm', phone: '038***2244' },
    { name: 'Anh Đức Duy', phone: '093***4411' },
    { name: 'Chị Hải Yến', phone: '089***6655' },
    { name: 'Anh Xuân Bách', phone: '094***1122' },
    { name: 'Chị Tuyết Mai', phone: '096***3344' },
    { name: 'Anh Vũ Long', phone: '098***7711' },
    { name: 'Chị Mỹ Duyên', phone: '091***8833' },
    { name: 'Anh Đình Trọng', phone: '090***1144' },
    { name: 'Chị Khánh Linh', phone: '088***2255' },
    { name: 'Anh Tùng Dương', phone: '097***6677' },
    { name: 'Chị Phương Nga', phone: '035***4433' },
    { name: 'Anh Bảo Long', phone: '093***9988' },
    { name: 'Chị Thảo Vy', phone: '086***7766' },
    { name: 'Bác Hùng', phone: '094***2299' },
    { name: 'Đoàn anh Nam (Cty Công Nghệ)', phone: '098***5544' },
    { name: 'Đoàn anh Phong (Khối Ngân Hàng)', phone: '091***6611' },
    { name: 'Chị Hà Trang (Hội Bạn Thân)', phone: '090***8877' },
    { name: 'Anh Tuấn Anh', phone: '097***9900' },
    { name: 'Chị Ngọc Ánh', phone: '096***5522' },
    { name: 'Anh Huy Hoàng', phone: '088***3311' }
  ];

  // Danh sách hơn 25 khách hàng tiếng Trung (Doanh nhân & Khách du lịch)
  var ZH_CUSTOMERS = [
    { name: '王总', phone: '138****5218' },
    { name: '李总', phone: '139****8823' },
    { name: '张经理', phone: '137****6619' },
    { name: '陈先生', phone: '135****4472' },
    { name: '刘女士', phone: '136****9910' },
    { name: '赵总', phone: '188****3321' },
    { name: '孙总', phone: '186****7722' },
    { name: '周经理', phone: '159****4431' },
    { name: '吴总', phone: '131****8890' },
    { name: '郑先生', phone: '150****6612' },
    { name: '林总', phone: '189****3345' },
    { name: '黄女士', phone: '134****7789' },
    { name: '何总', phone: '180****5561' },
    { name: '郭先生', phone: '133****9928' },
    { name: '谢总', phone: '177****2210' },
    { name: '马经理', phone: '132****4456' },
    { name: '朱总', phone: '185****1190' },
    { name: '胡先生', phone: '158****8834' },
    { name: '高总', phone: '138****9901' },
    { name: '徐总', phone: '187****6643' },
    { name: '梁经理', phone: '139****1123' },
    { name: '宋总', phone: '186****4455' },
    { name: '唐先生', phone: '159****7788' },
    { name: '罗总', phone: '135****6699' },
    { name: '冯女士', phone: '180****2233' }
  ];

  // Các loại sự kiện đặt phòng đa dạng & màu badge tương ứng
  var EVENT_TYPES = [
    {
      badgeVn: '✓ Đã giữ chỗ thành công',
      actionVn: 'Vừa đặt: ',
      badgeZh: '✓ 已确认成功订房',
      actionZh: '已预订：',
      icon: '👑',
      badgeColor: '#06d6a0',
      badgeBorder: 'rgba(6, 214, 160, 0.45)',
      badgeBg: 'rgba(6, 214, 160, 0.16)'
    },
    {
      badgeVn: '🔥 Đã chốt cọc phòng VIP',
      actionVn: 'Vừa cọc: ',
      badgeZh: '🔥 VIP包厢定金已付',
      actionZh: '已定金：',
      icon: '🔥',
      badgeColor: '#ff758c',
      badgeBorder: 'rgba(255, 117, 140, 0.5)',
      badgeBg: 'rgba(255, 117, 140, 0.18)'
    },
    {
      badgeVn: '👑 Tiếp khách doanh nhân VIP',
      actionVn: 'Giữ phòng: ',
      badgeZh: '👑 商务高端接待包厢',
      actionZh: '已锁定：',
      icon: '👑',
      badgeColor: '#ffd166',
      badgeBorder: 'rgba(255, 209, 102, 0.5)',
      badgeBg: 'rgba(255, 209, 102, 0.18)'
    },
    {
      badgeVn: '🎉 Giữ phòng tiệc sinh nhật',
      actionVn: 'Đặt tiệc: ',
      badgeZh: '🎉 生日聚会派对包厢',
      actionZh: '已预订：',
      icon: '🎂',
      badgeColor: '#ff9ebb',
      badgeBorder: 'rgba(255, 158, 187, 0.5)',
      badgeBg: 'rgba(255, 158, 187, 0.18)'
    },
    {
      badgeVn: '⭐ Khách quen đặt trước',
      actionVn: 'Vừa giữ chỗ: ',
      badgeZh: '⭐ VIP老客户提前预留',
      actionZh: '已预留：',
      icon: '⭐',
      badgeColor: '#4cc9f0',
      badgeBorder: 'rgba(76, 201, 240, 0.5)',
      badgeBg: 'rgba(76, 201, 240, 0.18)'
    },
    {
      badgeVn: '⚡ Giữ phòng hỏa tốc',
      actionVn: 'Đặt phòng: ',
      badgeZh: '⚡ 极速订房（马上到店）',
      actionZh: '马上到：',
      icon: '⚡',
      badgeColor: '#ffd166',
      badgeBorder: 'rgba(255, 209, 102, 0.5)',
      badgeBg: 'rgba(255, 209, 102, 0.18)'
    },
    {
      badgeVn: '🥂 Tiệc liên hoan công ty',
      actionVn: 'Vừa chốt phòng: ',
      badgeZh: '🥂 公司团建聚会包厢',
      actionZh: '已锁定：',
      icon: '🥂',
      badgeColor: '#ffb703',
      badgeBorder: 'rgba(255, 183, 3, 0.5)',
      badgeBg: 'rgba(255, 183, 3, 0.18)'
    },
    {
      badgeVn: '🎁 Nhận ưu đãi giờ vàng',
      actionVn: 'Đặt phòng: ',
      badgeZh: '🎁 享黄金时段特惠礼包',
      actionZh: '已预订：',
      icon: '🎁',
      badgeColor: '#06d6a0',
      badgeBorder: 'rgba(6, 214, 160, 0.45)',
      badgeBg: 'rgba(6, 214, 160, 0.16)'
    },
    {
      badgeVn: '🎤 Dàn âm thanh Concert',
      actionVn: 'Vừa chọn: ',
      badgeZh: '🎤 演唱会顶级声学音响',
      actionZh: '已选定：',
      icon: '🎤',
      badgeColor: '#ff758c',
      badgeBorder: 'rgba(255, 117, 140, 0.5)',
      badgeBg: 'rgba(255, 117, 140, 0.18)'
    }
  ];

  // Danh sách các loại phòng phong phú
  var ROOM_TYPES_VN = [
    'Phòng Deluxe Mini (4 - 8 khách)',
    'Phòng Deluxe Tiêu Chuẩn (6 - 10 khách)',
    'Phòng Deluxe Sang Trọng (8 - 12 khách)',
    'Phòng VIP Luxury (10 - 15 khách)',
    'Phòng VIP King Hoàng Gia (12 - 18 khách)',
    'Phòng VIP Gold Hiện Đại (15 - 20 khách)',
    'Phòng Super VIP Party (20 - 30 khách)',
    'Phòng Tổng Thống KTV Luxury (25 - 35 khách)',
    'Phòng Hoàng Gia Luxury (18 - 25 khách)',
    'Phòng Đại Tiệc KTV (30 - 50 khách)',
    'Phòng Tiệc Sinh Nhật KTV (12 - 20 khách)',
    'Phòng Mini Bar Club LED (10 - 16 khách)',
    'Phòng KTV Âm Thanh Concert (15 - 25 khách)',
    'Phòng Hát Gia Đình Ấm Cúng (6 - 10 khách)',
    'Phòng VIP KTV View Đẹp (10 - 15 khách)'
  ];

  var ROOM_TYPES_ZH = [
    '豪华Deluxe小包厢（4-8人）',
    '豪华Deluxe标准包厢（6-10人）',
    '豪华Deluxe大包厢（8-12人）',
    '尊享VIP商务包厢（10-15人）',
    '皇家VIP王者包厢（12-18人）',
    '超级VIP派对大包厢（20-30人）',
    '总统商务KTV豪华包厢（25-35人）',
    '顶级皇家奢华包厢（18-25人）',
    '公司团建大型包厢（30-50人）',
    '生日聚会定制主题包厢（12-20人）',
    '演唱会级顶级音响包厢（15-25人）'
  ];

  // Danh sách toàn bộ 21 quán đang hoạt động tại Cầu Giấy & Đống Đa
  var TOP_VENUES = [
    'Karaoke Kenz Club 202 Trung Kính',
    'Karaoke Summit 64 Trần Thái Tông',
    'Karaoke Zozo 12 Trần Kim Xuyến',
    'Karaoke Flamenco KTV 16-18 Vũ Phạm Hàm',
    'Karaoke Royal Club 97 Cầu Giấy',
    'Karaoke Thượng Hải KTV 229 Tây Sơn',
    'Karaoke Tip Top 85G Nguyễn Khang',
    'Karaoke LONDON 28 Thành Thái',
    'Karaoke S 69 Trần Thái Tông',
    'Karaoke Paris Club 69 Trần Thái Tông',
    'Karaoke X-MEN Club 402 Đê La Thành',
    'Karaoke GRAND 300 Xã Đàn',
    'Karaoke Sing KTV 65 Thái Thịnh',
    'Karaoke Royal 31-33 Nguyễn Khang',
    'Karaoke The Voice Quan Hoa',
    'Karaoke Amigo 233 Lê Đức Thọ',
    'Karaoke V-Pop 50 Trung Hòa',
    'Karaoke 85 Hoàng Gia Cầu Giấy',
    'Karaoke Level 36 Vũ Trọng Khánh',
    'Karaoke Titan 244 Vũ Quỳnh',
    'Karaoke MC Queen 29 La Thành'
  ];

  var TIME_AGO_VN = [
    'Vừa xong (10 giây trước)',
    'Cách đây 1 phút',
    'Cách đây 2 phút',
    'Cách đây 3 phút',
    'Cách đây 4 phút',
    'Cách đây 5 phút',
    'Cách đây 6 phút',
    'Cách đây 8 phút',
    'Cách đây 11 phút',
    'Cách đây 14 phút'
  ];

  var TIME_AGO_ZH = [
    '刚刚（10秒前）',
    '1分钟前',
    '2分钟前',
    '3分钟前',
    '4分钟前',
    '5分钟前',
    '6分钟前',
    '8分钟前',
    '10分钟前'
  ];

  // Bộ nhớ đệm chống lặp liên tục (Anti-repeat buffer)
  var recentCustomerIdx = [];
  var recentEventIdx = [];
  var recentRoomIdx = [];
  var recentVenueIdx = [];

  function pickNonRepeating(pool, recentList, maxHistory) {
    if (recentList.length >= pool.length) {
      recentList.splice(0, Math.floor(pool.length / 2));
    }
    var available = [];
    for (var i = 0; i < pool.length; i++) {
      if (recentList.indexOf(i) === -1) {
        available.push(i);
      }
    }
    if (available.length === 0) {
      available = [Math.floor(Math.random() * pool.length)];
    }
    var chosenIdx = available[Math.floor(Math.random() * available.length)];
    recentList.push(chosenIdx);
    if (recentList.length > maxHistory) recentList.shift();
    return pool[chosenIdx];
  }

  var currentIndex = 0;
  var hideTimeout = null;
  var nextTimeout = null;
  var isHovered = false;
  var toastEl = null;

  function isChinese() {
    return document.documentElement.lang === 'zh' || 
           (typeof localStorage !== 'undefined' && localStorage.getItem('kenz_lang') === 'zh');
  }

  function getTodayString() {
    var now = new Date();
    var day = now.getDate();
    var month = now.getMonth() + 1;
    return (day < 10 ? '0' + day : day) + '/' + (month < 10 ? '0' + month : month);
  }

  // Tự động tính toán khung giờ phù hợp theo thời gian thực hiện tại
  function generateDynamicSlot(isZh) {
    var now = new Date();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var todayStr = getTodayString();
    var slots = [];

    if (hour >= 6 && hour < 14) {
      if (isZh) {
        slots = ['中午 12:30', '下午 14:00', '今晚 19:30', '今晚 20:00', '今晚 20:30', '今晚 21:00'];
      } else {
        slots = ['Trưa nay 12:30', 'Chiều nay 14:30', 'Tối nay 19:30', 'Tối nay 20:00', 'Tối nay 20:30', 'Tối nay 21:00', 'Tối nay 21:30'];
      }
    } else if (hour >= 14 && hour < 18) {
      if (isZh) {
        slots = ['下午 16:30', '今晚 19:00', '今晚 19:30', '今晚 20:00', '今晚 20:30', '今晚 21:00', '今晚 21:30', '明晚 20:00'];
      } else {
        slots = ['Chiều nay 16:30', 'Tối nay 19:00', 'Tối nay 19:30', 'Tối nay 20:00', 'Tối nay 20:30', 'Tối nay 21:00', 'Tối nay 21:30', 'Tối mai 20:00'];
      }
    } else if (hour >= 18 && hour < 23) {
      var nextMins = minute < 30 ? '30' : '00';
      var nextHour = minute < 30 ? hour : (hour + 1);
      var nextTime = (nextHour < 10 ? '0' + nextHour : nextHour) + ':' + nextMins;
      if (isZh) {
        slots = ['稍后 ' + nextTime, '15分钟后到店', '今晚 21:00', '今晚 21:30', '今晚 22:00', '今晚 22:30', '明晚 20:00'];
      } else {
        slots = ['Đến ngay ' + nextTime, 'Đến ngay trong 15 phút', 'Tối nay 20:30', 'Tối nay 21:00', 'Tối nay 21:30', 'Tối nay 22:00', 'Tối nay 22:30', 'Tối mai 20:00'];
      }
    } else {
      if (isZh) {
        slots = ['马上到店（深夜畅唱）', '凌晨 01:00', '今晚 20:00', '今晚 20:30', '今晚 21:00'];
      } else {
        slots = ['Đến ngay (Hát xuyên đêm)', 'Tiệc đêm 01:00', 'Tối nay 20:00', 'Tối nay 20:30', 'Tối nay 21:00', 'Tối nay 21:30'];
      }
    }
    var randomSlot = slots[Math.floor(Math.random() * slots.length)];
    return randomSlot + ' (' + todayStr + ')';
  }

  function getCurrentVenue() {
    // 1. Kiểm tra tiêu đề h1 trên trang hiện tại để ưu tiên quán đó
    var pageH1 = document.querySelector('h1');
    if (pageH1 && pageH1.textContent) {
      var txt = pageH1.textContent.trim();
      if (txt.indexOf('Karaoke') !== -1 || txt.indexOf('KTV') !== -1) {
        var clean = txt.split('–')[0].split('-')[0].trim();
        if (clean.length > 5 && Math.random() < 0.7) {
          return clean; // 70% ưu tiên chính quán đang xem
        }
      }
    }
    // 2. Luân phiên ngẫu nhiên thông minh không lặp
    return pickNonRepeating(TOP_VENUES, recentVenueIdx, 8);
  }

  function createToastDOM() {
    injectToastStyles();

    if (document.getElementById('live-booking-toast')) {
      return document.getElementById('live-booking-toast');
    }

    var el = document.createElement('div');
    el.id = 'live-booking-toast';
    el.className = 'live-booking-toast';
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');

    el.innerHTML = [
      '<div class="lbt-body">',
      '  <button class="lbt-close" type="button" aria-label="Đóng thông báo">&times;</button>',
      '  <div class="lbt-avatar">',
      '    <div class="lbt-avatar-ring">',
      '      <span class="lbt-avatar-icon">👑</span>',
      '    </div>',
      '    <span class="lbt-status-dot" title="Trực tuyến"></span>',
      '  </div>',
      '  <div class="lbt-content">',
      '    <div class="lbt-row-head">',
      '      <strong class="lbt-customer"></strong>',
      '      <span class="lbt-badge-verified"></span>',
      '    </div>',
      '    <div class="lbt-action"></div>',
      '    <div class="lbt-venue"></div>',
      '    <div class="lbt-meta">',
      '      <span class="lbt-slot"></span>',
      '      <span class="lbt-sep">•</span>',
      '      <span class="lbt-time"></span>',
      '    </div>',
      '  </div>',
      '</div>',
      '<div class="lbt-progress"><div class="lbt-progress-bar"></div></div>'
    ].join('');

    // Sự kiện đóng
    var closeBtn = el.querySelector('.lbt-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        hideToast();
      });
    }

    // Nhấp vào toast để mở form đặt phòng với quán tương ứng
    el.addEventListener('click', function () {
      var venueName = el.getAttribute('data-venue') || 'Karaoke Kenz Club 202 Trung Kính';
      if (typeof window.openBookingModal === 'function') {
        window.openBookingModal(venueName);
      } else if (typeof window.openBooking === 'function') {
        window.openBooking(venueName);
      } else {
        var bookBtn = document.querySelector('[data-book]');
        if (bookBtn) {
          bookBtn.click();
        } else {
          window.location.href = 'index.html#bang-gia';
        }
      }
    });

    // Tạm dừng khi rê chuột
    el.addEventListener('mouseenter', function () {
      isHovered = true;
      var pBar = el.querySelector('.lbt-progress-bar');
      if (pBar) pBar.style.animationPlayState = 'paused';
      if (hideTimeout) {
        clearTimeout(hideTimeout);
        hideTimeout = null;
      }
    });

    el.addEventListener('mouseleave', function () {
      isHovered = false;
      var pBar = el.querySelector('.lbt-progress-bar');
      if (pBar) pBar.style.animationPlayState = 'running';
      hideTimeout = setTimeout(function () {
        hideToast();
      }, 2500);
    });

    document.body.appendChild(el);
    return el;
  }

  function showToast() {
    if (!toastEl) toastEl = createToastDOM();

    var zh = isChinese();
    var customer = pickNonRepeating(zh ? ZH_CUSTOMERS : VN_CUSTOMERS, recentCustomerIdx, 18);
    var evType = pickNonRepeating(EVENT_TYPES, recentEventIdx, 6);
    var room = pickNonRepeating(zh ? ROOM_TYPES_ZH : ROOM_TYPES_VN, recentRoomIdx, 8);
    var venue = getCurrentVenue();
    var slotStr = generateDynamicSlot(zh);
    var timeAgoPool = zh ? TIME_AGO_ZH : TIME_AGO_VN;
    var timeAgo = timeAgoPool[Math.floor(Math.random() * timeAgoPool.length)];

    toastEl.setAttribute('data-venue', venue);

    // Điền dữ liệu
    var custEl = toastEl.querySelector('.lbt-customer');
    var badgeEl = toastEl.querySelector('.lbt-badge-verified');
    var actEl = toastEl.querySelector('.lbt-action');
    var venEl = toastEl.querySelector('.lbt-venue');
    var slotEl = toastEl.querySelector('.lbt-slot');
    var timeEl = toastEl.querySelector('.lbt-time');
    var iconEl = toastEl.querySelector('.lbt-avatar-icon');
    var ringEl = toastEl.querySelector('.lbt-avatar-ring');

    if (custEl) custEl.textContent = customer.name + ' (' + customer.phone + ')';
    if (iconEl) iconEl.textContent = evType.icon;
    if (ringEl) {
      ringEl.style.borderColor = evType.badgeColor;
      ringEl.style.boxShadow = '0 0 16px ' + evType.badgeBorder;
    }

    if (badgeEl) {
      badgeEl.textContent = zh ? evType.badgeZh : evType.badgeVn;
      badgeEl.style.color = evType.badgeColor;
      badgeEl.style.borderColor = evType.badgeBorder;
      badgeEl.style.backgroundColor = evType.badgeBg;
    }

    if (actEl) {
      actEl.innerHTML = (zh ? evType.actionZh : evType.actionVn) + '<b>' + room + '</b>';
    }

    if (venEl) {
      venEl.innerHTML = (zh ? '地点：' : 'Tại: ') + '<b>' + venue + '</b>';
    }

    if (slotEl) {
      slotEl.textContent = (zh ? '📅 预订时间: ' : '📅 Lịch: ') + slotStr;
    }

    if (timeEl) {
      timeEl.textContent = (zh ? '⚡ ' : '⏱️ ') + timeAgo;
    }

    // Reset thanh thời gian progress bar
    var pBar = toastEl.querySelector('.lbt-progress-bar');
    if (pBar) {
      pBar.style.animation = 'none';
      void pBar.offsetWidth; // trigger reflow
      pBar.style.animation = 'lbtProgress ' + (SHOW_DURATION_MS / 1000) + 's linear forwards';
    }

    // Hiển thị class active
    toastEl.classList.remove('hiding');
    toastEl.classList.add('active');

    // Hẹn giờ ẩn sau SHOW_DURATION_MS
    if (hideTimeout) clearTimeout(hideTimeout);
    hideTimeout = setTimeout(function () {
      if (!isHovered) {
        hideToast();
      }
    }, SHOW_DURATION_MS);

    currentIndex++;
  }

  function hideToast() {
    if (!toastEl) return;
    toastEl.classList.remove('active');
    toastEl.classList.add('hiding');

    if (hideTimeout) {
      clearTimeout(hideTimeout);
      hideTimeout = null;
    }

    // Lên lịch lần hiển thị tiếp theo sau INTERVAL_SEC (30 giây)
    if (nextTimeout) clearTimeout(nextTimeout);
    nextTimeout = setTimeout(function () {
      showToast();
    }, INTERVAL_SEC * 1000);
  }

  // Khởi động
  function init() {
    injectToastStyles();
    // Đợi DOM sẵn sàng rồi hiện toast lần đầu
    setTimeout(function () {
      showToast();
    }, INITIAL_DELAY_MS);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
