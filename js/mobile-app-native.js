/**
 * =============================================================================
 * MOBILE APP NATIVE EXPERIENCE JS - IOS & ANDROID
 * =============================================================================
 * - Xử lý phím Back vật lý trên Android (Đóng Modal / Sheet thay vì thoát App)
 * - Triệt tiêu độ trễ 300ms khi bấm
 * - Tự động đồng bộ chiều cao thật 100dvh trên Safari và Chrome Mobile
 * =============================================================================
 */

(function () {
  'use strict';

  // 1. Tính toán chuẩn chiều cao thật 100dvh trên mọi điện thoại
  function syncAppHeight() {
    const doc = document.documentElement;
    doc.style.setProperty('--app-height', `${window.innerHeight}px`);
  }
  window.addEventListener('resize', syncAppHeight);
  window.addEventListener('orientationchange', syncAppHeight);
  syncAppHeight();

  // 2. Danh sách hàm kiểm tra và đóng các modal đang mở
  function getActiveModal() {
    // 1. Modal đặt bàn
    const bkModal = document.getElementById('modal');
    if (bkModal && !bkModal.hidden && bkModal.style.display !== 'none') {
      return () => {
        if (typeof window.closeBookingModal === 'function') {
          window.closeBookingModal();
        } else {
          bkModal.hidden = true;
          document.body.classList.remove('lock');
        }
      };
    }

    // 2. Modal đánh giá
    const revModal = document.getElementById('rev-modal');
    if (revModal && !revModal.hidden && revModal.style.display !== 'none') {
      return () => {
        revModal.hidden = true;
        document.body.classList.remove('lock');
      };
    }

    // 3. Lightbox xem ảnh
    const lb = document.getElementById('lightbox');
    if (lb && !lb.hidden && lb.style.display !== 'none') {
      return () => {
        lb.hidden = true;
        document.body.classList.remove('lock');
      };
    }

    // 4. Popover liên hệ (WeChat, Zalo, Call)
    const openPop = document.querySelector('.pop:not([hidden])');
    if (openPop) {
      return () => {
        openPop.hidden = true;
      };
    }

    // 5. Modal PWA hướng dẫn
    const pwaModal = document.querySelector('.pwa-modal-backdrop.active');
    if (pwaModal) {
      return () => {
        pwaModal.classList.remove('active');
      };
    }

    return null;
  }

  // 3. Xử lý phím Back phần cứng Android & Cử chỉ vuốt cạnh màn hình
  // Dùng History API để tạo điểm dừng ảo khi mở Modal
  let isBackHandled = false;

  const originalOpenBooking = window.openBookingModal || window.openBooking;
  if (originalOpenBooking) {
    const wrappedOpen = function (...args) {
      history.pushState({ kenzModal: 'booking' }, '');
      return originalOpenBooking.apply(this, args);
    };
    window.openBookingModal = wrappedOpen;
    window.openBooking = wrappedOpen;
  }

  window.addEventListener('popstate', (e) => {
    const closeAction = getActiveModal();
    if (closeAction) {
      closeAction();
      isBackHandled = true;
    }
  });

  // Tích hợp phím Back riêng của Capacitor (Android Native)
  if (window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.App) {
    window.Capacitor.Plugins.App.addListener('backButton', ({ canGoBack }) => {
      const closeAction = getActiveModal();
      if (closeAction) {
        closeAction();
      } else if (canGoBack) {
        window.history.back();
      } else {
        window.Capacitor.Plugins.App.exitApp();
      }
    });
  }

  // 4. Ngăn chặn Double-Tap zoom vô tình gây vỡ bố cục trên iOS Safari
  let lastTouchEnd = 0;
  document.addEventListener('touchend', (e) => {
    const now = Date.now();
    if (now - lastTouchEnd <= 300) {
      // Chỉ ngăn zoom nếu không nằm trong khu vực zoom ảnh của Lightbox
      if (!e.target.closest('#lightbox')) {
        e.preventDefault();
      }
    }
    lastTouchEnd = now;
  }, { passive: false });

  // 5. Cải thiện độ phản hồi mượt mà của thanh Bottom Bar
  document.addEventListener('DOMContentLoaded', () => {
    const quickBar = document.querySelector('.quick');
    if (quickBar) {
      // Đảm bảo nút Đặt Bàn trong thanh đáy mở form chuẩn xác
      const bookBtn = quickBar.querySelector('[data-book]');
      if (bookBtn) {
        bookBtn.addEventListener('click', () => {
          if (typeof window.openBookingModal === 'function') {
            window.openBookingModal('Karaoke Kenz Club 202 Trung Kính');
          }
        });
      }
    }
  });

  console.log('[Native App] Tối ưu trải nghiệm iOS & Android sẵn sàng!');
})();
