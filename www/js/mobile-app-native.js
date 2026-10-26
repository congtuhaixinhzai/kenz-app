/**
 * =============================================================================
 * KARAOKE KENZ - VIP NATIVE MOBILE APP CONTROLLER (IOS & ANDROID)
 * =============================================================================
 * - Tự động thiết lập Thanh điều hướng dưới đáy (Native Tab Bar) 5 Tab chuẩn App
 * - Xử lý phím Back vật lý trên Android (Đóng Modal -> Toast thoát App)
 * - Tích hợp Haptic Feedback (rung nhẹ xúc giác khi chạm nút)
 * - Kéo vuốt để đóng Bottom Sheet chuẩn iOS (Pull-to-dismiss gesture)
 * - Tự động cuộn ô nhập liệu khi bàn phím ảo bật lên (Anti-keyboard overlap)
 * - Cảnh báo trạng thái mạng trực tiếp (Online/Offline)
 * - Đồng bộ Safe Area & 100dvh
 * =============================================================================
 */

(function () {
  'use strict';

  // 1. ĐỒNG BỘ CHIỀU CAO THẬT 100DVH & SAFE-AREA TRÊN MỌI MÀN HÌNH
  function syncViewportHeight() {
    const doc = document.documentElement;
    const vh = window.innerHeight * 0.01;
    doc.style.setProperty('--vh', `${vh}px`);
    doc.style.setProperty('--app-height', `${window.innerHeight}px`);
  }
  window.addEventListener('resize', syncViewportHeight, { passive: true });
  window.addEventListener('orientationchange', syncViewportHeight, { passive: true });
  syncViewportHeight();

  // 2. PHẢN HỒI XÚC GIÁC HAPTIC FEEDBACK KHI CHẠM
  function triggerHaptic(duration = 10) {
    if (typeof navigator !== 'undefined' && navigator.vibrate) {
      try {
        navigator.vibrate(duration);
      } catch (e) {
        // Bỏ qua nếu thiết bị không hỗ trợ
      }
    }
  }

  // 3. DANH SÁCH KIỂM TRA & ĐÓNG TẤT CẢ CÁC MODAL/SHEET ĐANG MỞ
  function getActiveModalCloser() {
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
    const revModal = document.getElementById('review-modal') || document.getElementById('rev-modal');
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

  // 4. XỬ LÝ PHÍM BACK VẬT LÝ ANDROID & CỬ CHỈ VUỐT CẠNH MÀN HÌNH
  let lastBackPressTime = 0;

  function handleBackButtonEvent() {
    const closeAction = getActiveModalCloser();
    if (closeAction) {
      closeAction();
      triggerHaptic(12);
      return true;
    }
    return false;
  }

  // A. Tích hợp Plugin Native Capacitor (dành cho file APK Android)
  if (window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.App) {
    window.Capacitor.Plugins.App.addListener('backButton', ({ canGoBack }) => {
      const closed = handleBackButtonEvent();
      if (closed) return;

      if (canGoBack) {
        window.history.back();
      } else {
        const now = Date.now();
        if (now - lastBackPressTime < 2000) {
          window.Capacitor.Plugins.App.exitApp();
        } else {
          lastBackPressTime = now;
          showNativeToast('Nhấn lần nữa để thoát ứng dụng');
        }
      }
    });
  }

  // B. Tích hợp History API cho trình duyệt di động & PWA
  window.addEventListener('popstate', () => {
    handleBackButtonEvent();
  });

  // Gắn điểm dừng ảo vào history khi mở modal đặt bàn
  const rawOpenBooking = window.openBookingModal || window.openBooking;
  if (rawOpenBooking) {
    const wrappedOpen = function (...args) {
      history.pushState({ kenzModal: 'booking' }, '');
      return rawOpenBooking.apply(this, args);
    };
    window.openBookingModal = wrappedOpen;
    window.openBooking = wrappedOpen;
  }

  // 5. HIỂN THỊ TOAST THÔNG BÁO DẠNG NATIVE
  function showNativeToast(message, duration = 2500) {
    let toast = document.getElementById('native-app-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'native-app-toast';
      toast.style.cssText = `
        position: fixed;
        bottom: calc(var(--tabbar-height, 64px) + 24px + env(safe-area-inset-bottom, 0px));
        left: 50%;
        transform: translateX(-50%) translateY(20px);
        background: rgba(20, 18, 38, 0.94);
        color: #fff;
        padding: 10px 20px;
        border-radius: 999px;
        font-size: 0.86rem;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(0,0,0,0.6);
        border: 1px solid rgba(255, 183, 3, 0.4);
        z-index: 999999;
        opacity: 0;
        pointer-events: none;
        transition: all 0.25s cubic-bezier(0.2, 0.8, 0.4, 1);
        white-space: nowrap;
        text-align: center;
      `;
      document.body.appendChild(toast);
    }

    toast.textContent = message;
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(-50%) translateY(20px)';
    }, duration);
  }

  // 6. TỰ ĐỘNG KHỞI TẠO THANH ĐIỀU HƯỚNG TAB BAR NATIVE (5 TAB CHUẨN APP)
  function setupNativeTabBar() {
    let tabbar = document.getElementById('native-app-tabbar');

    const isIndex = window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname.endsWith('/');
    const prefix = isIndex ? '' : 'index.html';

    if (!tabbar) {
      tabbar = document.createElement('nav');
      tabbar.id = 'native-app-tabbar';
      tabbar.setAttribute('aria-label', 'Điều hướng ứng dụng');
      tabbar.innerHTML = `
        <div class="native-tabbar-inner">
          <!-- 1. TRANG CHỦ -->
          <button type="button" class="tab-item active" id="tab-home" aria-label="Trang chủ">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
            <span>Trang chủ</span>
          </button>

          <!-- 2. KTV HÀ NỘI VIP (21+ QUÁN CẦU GIẤY & ĐỐNG ĐA) -->
          <button type="button" class="tab-item" id="tab-ktv" aria-label="KTV Hà Nội">
            <div style="position:relative;display:inline-flex;align-items:center;justify-content:center">
              <svg viewBox="0 0 24 24"><path d="M12 3v9.28a4.39 4.39 0 0 0-1.5-.28C8.01 12 6 14.01 6 16.5S8.01 21 10.5 21c2.31 0 4.2-1.75 4.45-4H15V6h4V3h-7z"/></svg>
              <span class="tab-hot-badge">HOT</span>
            </div>
            <span>KTV Hà Nội</span>
          </button>

          <!-- 3. ĐẶT BÀN SIÊU VIP (HERO ACTION NỔI BẬT) -->
          <button type="button" class="tab-item tab-hero" id="tab-book" aria-label="Đặt bàn giữ phòng">
            <div class="tab-hero-inner">
              <svg viewBox="0 0 24 24"><path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zM9 14H7v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2zm-8 4H7v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2z"/></svg>
            </div>
            <span class="tab-hero-label">ĐẶT PHÒNG</span>
          </button>

          <!-- 4. ƯU ĐÃI KHUYẾN MÃI -->
          <button type="button" class="tab-item" id="tab-promo" aria-label="Ưu đãi">
            <svg viewBox="0 0 24 24"><path d="M20 6h-2.18c.11-.31.18-.65.18-1 0-1.66-1.34-3-3-3-1.05 0-1.96.54-2.5 1.35l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm11 15H4v-2h16v2zm0-5H4V8h5.08L7 10.83 8.62 12 11 8.76V8h2v.76L15.38 12 17 10.83 14.92 8H20v6z"/></svg>
            <span>Ưu đãi</span>
          </button>

          <!-- 5. HOTLINE & ZALO -->
          <button type="button" class="tab-item" id="tab-contact" aria-label="Hỗ trợ Hotline">
            <svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>
            <span>Hotline</span>
          </button>
        </div>
      `;
      document.body.appendChild(tabbar);
    }

    // Gắn sự kiện điều hướng mượt mà cho từng Tab
    const tabHome = document.getElementById('tab-home');
    const tabKtv = document.getElementById('tab-ktv');
    const tabBook = document.getElementById('tab-book');
    const tabPromo = document.getElementById('tab-promo');
    const tabContact = document.getElementById('tab-contact');

    function setActiveTab(el) {
      document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
      if (el && !el.classList.contains('tab-hero')) {
        el.classList.add('active');
      }
    }

    tabHome.addEventListener('click', () => {
      triggerHaptic(12);
      setActiveTab(tabHome);
      if (isIndex) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        window.location.href = 'index.html';
      }
    });

    if (tabKtv) {
      tabKtv.addEventListener('click', () => {
        triggerHaptic(12);
        setActiveTab(tabKtv);
        const targetUrl = window.location.pathname.includes('/tin-tuc/') ? '../ktv-hanoi.html' : 'ktv-hanoi.html';
        window.location.href = targetUrl;
      });
    }

    tabBook.addEventListener('click', () => {
      triggerHaptic(18);
      // Mở modal đặt bàn ngay lập tức
      if (typeof window.openBookingModal === 'function') {
        window.openBookingModal('Karaoke Kenz Club 202 Trung Kính');
      } else if (typeof window.openBooking === 'function') {
        window.openBooking('Karaoke Kenz Club 202 Trung Kính');
      } else {
        const modal = document.getElementById('modal');
        if (modal) {
          modal.hidden = false;
          document.body.classList.add('lock');
        }
      }
    });

    tabPromo.addEventListener('click', () => {
      triggerHaptic(12);
      setActiveTab(tabPromo);
      const target = document.getElementById('uu-dai') || document.getElementById('promotions') || document.querySelector('.promo');
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        window.location.href = prefix + '#uu-dai';
      }
    });

    tabContact.addEventListener('click', () => {
      triggerHaptic(12);
      window.location.href = 'tel:0342092999';
    });

    // Đánh dấu Tab KTV active nếu đang ở trang ktv-hanoi.html
    if (window.location.pathname.includes('ktv-hanoi')) {
      setActiveTab(tabKtv);
    }

    // Theo dõi cuộn trang để tự động đổi màu tab tương ứng trên index.html
    if (isIndex && 'IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            if (entry.target.id === 'ktv-hanoi') {
              setActiveTab(tabKtv);
            } else if (entry.target.id === 'uu-dai' || entry.target.id === 'promotions') {
              setActiveTab(tabPromo);
            } else if (entry.target.id === 'hero' || window.scrollY < 300) {
              setActiveTab(tabHome);
            }
          }
        });
      }, { threshold: 0.3 });

      ['ktv-hanoi', 'uu-dai', 'hero'].forEach(id => {
        const el = document.getElementById(id);
        if (el) observer.observe(el);
      });
    }
  }

  // 7. BẢO VỆ VÙNG NHẬP LIỆU: TỰ ĐỘNG CUỘN ĐỂ KHÔNG BỊ BÀN PHÍM CHE KHUẤT
  function setupInputFocusHandling() {
    document.addEventListener('focusin', (e) => {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) {
        setTimeout(() => {
          e.target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 280);
      }
    });
  }

  // 8. CỬ CHỈ KÉO VUỐT ĐỂ ĐÓNG BOTTOM SHEET (PULL-TO-DISMISS GESTURE)
  function setupSheetSwipeGesture() {
    document.addEventListener('touchstart', (e) => {
      const sheet = e.target.closest('.sheet');
      if (!sheet) return;

      const startY = e.touches[0].clientY;
      const initialScrollTop = sheet.scrollTop;

      function onTouchMove(moveEvent) {
        const currentY = moveEvent.touches[0].clientY;
        const diff = currentY - startY;

        // Chỉ cho phép kéo đóng nếu đang ở đỉnh của sheet
        if (initialScrollTop <= 0 && diff > 0) {
          sheet.style.transform = `translateY(${diff * 0.7}px)`;
          sheet.style.transition = 'none';
        }
      }

      function onTouchEnd(endEvent) {
        const endY = endEvent.changedTouches[0].clientY;
        const diff = endY - startY;

        sheet.style.transition = 'transform 0.25s cubic-bezier(0.2, 0.8, 0.4, 1)';
        if (initialScrollTop <= 0 && diff > 90) {
          // Kéo đủ xa -> Đóng sheet
          const modal = sheet.closest('.modal');
          if (modal) {
            const closeBtn = modal.querySelector('.x') || modal.querySelector('[data-close]');
            if (closeBtn) closeBtn.click();
            else modal.hidden = true;
          }
        } else {
          sheet.style.transform = 'translateY(0)';
        }

        document.removeEventListener('touchmove', onTouchMove);
        document.removeEventListener('touchend', onTouchEnd);
      }

      document.addEventListener('touchmove', onTouchMove, { passive: true });
      document.addEventListener('touchend', onTouchEnd, { passive: true });
    }, { passive: true });
  }

  // 9. THÔNG BÁO TRẠNG THÁI MẠNG TRỰC TIẾP (ONLINE / OFFLINE)
  function setupNetworkStatusIndicator() {
    let bar = document.getElementById('native-app-offline-bar');
    if (!bar) {
      bar = document.createElement('div');
      bar.id = 'native-app-offline-bar';
      bar.innerHTML = '<span>⚠️</span> <span>Bạn đang ngoại tuyến (Dữ liệu đã sẵn sàng)</span>';
      document.body.appendChild(bar);
    }

    window.addEventListener('offline', () => {
      bar.className = 'show';
      bar.innerHTML = '<span>⚠️</span> <span>Bạn đang ngoại tuyến (Dữ liệu đã sẵn sàng)</span>';
    });

    window.addEventListener('online', () => {
      bar.className = 'show online';
      bar.innerHTML = '<span>✅</span> <span>Đã kết nối Internet thành công</span>';
      setTimeout(() => {
        bar.className = '';
      }, 3000);
    });
  }

  // 10. NGĂN CHẶN DOUBLE-TAP ZOOM GÂY VỠ GIAO DIỆN TRÊN IOS
  let lastTouchEndTime = 0;
  document.addEventListener('touchend', (e) => {
    const now = Date.now();
    if (now - lastTouchEndTime <= 300) {
      if (!e.target.closest('#lightbox')) {
        e.preventDefault();
      }
    }
    lastTouchEndTime = now;
  }, { passive: false });

  // 11. NÚT KTV HÀ NỘI TRÊN HEADER MOBILE (GIỮ NGUYÊN TRÊN ĐỈNH MÀN HÌNH)
  function setupMobileHeaderKtv() {
    const topActs = document.querySelector('header.top .top-acts');
    if (!topActs || document.getElementById('btn-header-ktv')) return;

    const ktvUrl = window.location.pathname.includes('/tin-tuc/') ? '../ktv-hanoi.html' : 'ktv-hanoi.html';
    const ktvBtn = document.createElement('a');
    ktvBtn.id = 'btn-header-ktv';
    ktvBtn.className = 'btn-top-ktv';
    ktvBtn.href = ktvUrl;
    ktvBtn.innerHTML = '🔥 <span>KTV HÀ NỘI</span>';
    
    // Đặt nút KTV trước các nút khác
    topActs.insertBefore(ktvBtn, topActs.firstChild);
  }

  // 12. THANH DANH MỤC LƯỚT NGANG CHUẨN NATIVE (CHIPS BAR DƯỚI HEADER)
  function setupMobileCategoryStrip() {
    if (document.getElementById('mobile-category-strip')) return;
    const header = document.querySelector('header.top');
    if (!header) return;

    const isIndex = window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname.endsWith('/');
    const prefix = isIndex ? '' : 'index.html';
    const ktvUrl = window.location.pathname.includes('/tin-tuc/') ? '../ktv-hanoi.html' : 'ktv-hanoi.html';
    const newsUrl = window.location.pathname.includes('/tin-tuc/') ? 'tintuc.html' : 'tin-tuc/tintuc.html';

    const strip = document.createElement('div');
    strip.id = 'mobile-category-strip';
    strip.className = 'mobile-cat-strip';
    strip.setAttribute('aria-label', 'Danh mục nhanh');
    strip.innerHTML = `
      <a href="${ktvUrl}" class="cat-pill hot">🔥 KTV HÀ NỘI (21+ Quán)</a>
      <a href="${prefix}#bang-gia" class="cat-pill">👑 Bảng Giá Phòng</a>
      <a href="${prefix}#hinh-anh" class="cat-pill">📸 Ảnh Quán</a>
      <a href="${prefix}#uu-dai" class="cat-pill">🎁 Ưu Đãi VIP</a>
      <a href="${prefix}#danh-gia" class="cat-pill">⭐ Đánh Giá</a>
      <a href="${newsUrl}" class="cat-pill">📰 Tin Tức</a>
    `;

    header.insertAdjacentElement('afterend', strip);
  }

  // 13. KHỞI TẠO TOÀN DIỆN KHI TRANG TẢI XONG
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNativeAppExperience);
  } else {
    initNativeAppExperience();
  }

  function initNativeAppExperience() {
    setupMobileHeaderKtv();
    setupMobileCategoryStrip();
    setupNativeTabBar();
    setupInputFocusHandling();
    setupSheetSwipeGesture();
    setupNetworkStatusIndicator();
    console.log('[Native App] Giao diện chuẩn iOS & Android đã kích hoạt hoàn tất!');
  }

})();
