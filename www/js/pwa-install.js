/**
 * =========================================================================
 * PWA INSTALL & SERVICE WORKER MANAGER - KARAOKE KENZ
 * =========================================================================
 * - Đăng ký Service Worker
 * - Hỗ trợ Cài đặt App 1-Chạm trên Android (WebAPK)
 * - Hướng dẫn Cài đặt Màn hình chính trên iOS (iPhone/iPad Standalone)
 * =========================================================================
 */

(function () {
  'use strict';

  // 1. Đăng ký Service Worker nếu trình duyệt hỗ trợ và đang chạy http/https
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.protocol === 'http:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1')) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('./sw.js')
        .then((reg) => {
          console.log('[PWA] Service Worker đăng ký thành công với scope:', reg.scope);
        })
        .catch((err) => {
          console.warn('[PWA] Lỗi đăng ký Service Worker:', err);
        });
    });
  }

  // 2. Kiểm tra xem app đã được mở ở chế độ App (Standalone) hay chưa
  const isStandalone = () => {
    return window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone === true ||
      document.referrer.includes('android-app://');
  };

  // 3. Nhận diện thiết bị iOS
  const isIOS = () => {
    return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  };

  let deferredPrompt = null;

  // 4. Lắng nghe sự kiện cài đặt trên Android / Chrome
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    showInstallTrigger(true);
  });

  window.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    hideInstallTrigger();
    if (window.toast) {
      window.toast('Đã cài đặt App Karaoke Kenz thành công!');
    }
  });

  // 5. Khởi tạo giao diện nút Cài App
  function initInstallUI() {
    if (isStandalone()) {
      console.log('[PWA] Ứng dụng đang chạy ở chế độ Standalone App.');
      return;
    }

    // Tạo nút Cài đặt App nổi (Floating Pill hoặc gắn vào header)
    const btn = document.createElement('button');
    btn.id = 'pwa-install-btn';
    btn.className = 'pwa-install-btn';
    btn.setAttribute('aria-label', 'Cài đặt ứng dụng Karaoke Kenz');
    btn.innerHTML = `
      <svg class="pwa-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="7 10 12 15 17 10"></polyline>
        <line x1="12" y1="15" x2="12" y2="3"></line>
      </svg>
      <span class="pwa-label">Cài Đặt App</span>
    `;

    btn.addEventListener('click', onInstallClick);
    document.body.appendChild(btn);

    // Luôn hiển thị nút trên iOS nếu chưa cài
    if (isIOS()) {
      showInstallTrigger(false);
    }
  }

  function showInstallTrigger(isAndroidReady) {
    const btn = document.getElementById('pwa-install-btn');
    if (btn) {
      btn.classList.add('visible');
    }
  }

  function hideInstallTrigger() {
    const btn = document.getElementById('pwa-install-btn');
    if (btn) {
      btn.classList.remove('visible');
    }
  }

  // 6. Xử lý khi bấm nút Cài Đặt
  async function onInstallClick() {
    if (deferredPrompt) {
      // Android / Chrome: Gọi prompt native
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      if (outcome === 'accepted') {
        deferredPrompt = null;
        hideInstallTrigger();
      }
    } else if (isIOS()) {
      // iOS Safari: Mở modal hướng dẫn chi tiết
      showIOSInstallModal();
    } else {
      // Trình duyệt khác (Firefox, Edge desktop, hoặc đã chặn prompt)
      showGenericInstallModal();
    }
  }

  // 7. Modal hướng dẫn cho iOS (iPhone / iPad)
  function showIOSInstallModal() {
    let modal = document.getElementById('pwa-ios-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'pwa-ios-modal';
      modal.className = 'pwa-modal-backdrop';
      modal.innerHTML = `
        <div class="pwa-modal-box">
          <button class="pwa-modal-close" aria-label="Đóng">&times;</button>
          <div class="pwa-modal-header">
            <img src="assets/apple-touch-icon.png" alt="Karaoke Kenz App Icon" class="pwa-modal-app-icon">
            <div>
              <h3 class="pwa-modal-title">Cài App Cho iPhone / iPad</h3>
              <p class="pwa-modal-sub">Trải nghiệm toàn màn hình như ứng dụng App Store</p>
            </div>
          </div>
          <div class="pwa-ios-steps">
            <div class="pwa-step">
              <span class="pwa-step-num">1</span>
              <div class="pwa-step-text">
                Bấm vào nút <strong>Chia sẻ</strong> 
                <span class="pwa-ios-share-icon" title="Nút Share">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path>
                    <polyline points="16 6 12 2 8 6"></polyline>
                    <line x1="12" y1="2" x2="12" y2="15"></line>
                  </svg>
                </span>
                ở thanh công cụ Safari bên dưới màn hình.
              </div>
            </div>
            <div class="pwa-step">
              <span class="pwa-step-num">2</span>
              <div class="pwa-step-text">
                Cuộn xuống và chọn <strong>"Thêm vào Màn hình chính"</strong> (Add to Home Screen ➕).
              </div>
            </div>
            <div class="pwa-step">
              <span class="pwa-step-num">3</span>
              <div class="pwa-step-text">
                Bấm <strong>"Thêm"</strong> ở góc trên bên phải để hoàn tất. Icon App sẽ có ngay trên màn hình iPhone của bạn!
              </div>
            </div>
          </div>
          <button class="pwa-modal-btn-ok">Đã Hiểu</button>
        </div>
      `;

      modal.querySelector('.pwa-modal-close').onclick = () => modal.classList.remove('active');
      modal.querySelector('.pwa-modal-btn-ok').onclick = () => modal.classList.remove('active');
      modal.onclick = (e) => {
        if (e.target === modal) modal.classList.remove('active');
      };
      document.body.appendChild(modal);
    }

    modal.classList.add('active');
  }

  // 8. Modal hướng dẫn chung cho trình duyệt máy tính / khác
  function showGenericInstallModal() {
    let modal = document.getElementById('pwa-generic-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'pwa-generic-modal';
      modal.className = 'pwa-modal-backdrop';
      modal.innerHTML = `
        <div class="pwa-modal-box">
          <button class="pwa-modal-close" aria-label="Đóng">&times;</button>
          <div class="pwa-modal-header">
            <img src="assets/icon-192x192.png" alt="Karaoke Kenz App Icon" class="pwa-modal-app-icon">
            <div>
              <h3 class="pwa-modal-title">Cài Đặt App Karaoke Kenz</h3>
              <p class="pwa-modal-sub">Dùng trên điện thoại Android, iPhone hoặc máy tính</p>
            </div>
          </div>
          <div class="pwa-ios-steps">
            <div class="pwa-step">
              <span class="pwa-step-num">📱</span>
              <div class="pwa-step-text">
                <strong>Trên Android:</strong> Mở trang web trên Google Chrome, bấm menu 3 chấm (⋮) ở góc trên -> Chọn <strong>"Cài đặt ứng dụng"</strong> hoặc <strong>"Thêm vào màn hình chính"</strong>.
              </div>
            </div>
            <div class="pwa-step">
              <span class="pwa-step-num">🍎</span>
              <div class="pwa-step-text">
                <strong>Trên iPhone (iOS):</strong> Mở trang web bằng <strong>Safari</strong> -> Bấm nút Chia sẻ (hình vuông mũi tên lên) -> Chọn <strong>"Thêm vào MH chính"</strong>.
              </div>
            </div>
            <div class="pwa-step">
              <span class="pwa-step-num">💻</span>
              <div class="pwa-step-text">
                <strong>Trên Máy tính:</strong> Bấm vào biểu tượng cài đặt (mũi tên tải xuống) nằm ở bên phải thanh gõ địa chỉ trình duyệt.
              </div>
            </div>
          </div>
          <button class="pwa-modal-btn-ok">Đã Hiểu</button>
        </div>
      `;

      modal.querySelector('.pwa-modal-close').onclick = () => modal.classList.remove('active');
      modal.querySelector('.pwa-modal-btn-ok').onclick = () => modal.classList.remove('active');
      modal.onclick = (e) => {
        if (e.target === modal) modal.classList.remove('active');
      };
      document.body.appendChild(modal);
    }

    modal.classList.add('active');
  }

  // Khởi chạy khi DOM sẵn sàng
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initInstallUI);
  } else {
    initInstallUI();
  }
})();
