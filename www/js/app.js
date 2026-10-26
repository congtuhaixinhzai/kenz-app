/**
 * =========================================================================
 * KHỞI TẠO TƯƠNG TÁC CHÍNH (MAIN APPLICATION) - KARAOKE KENZ WEB
 * =========================================================================
 * - Đồng bộ thông tin từ config.js vào toàn bộ giao diện HTML.
 * - Xử lý menu cuộn phát sáng thông minh (IntersectionObserver).
 * - Xử lý các nút liên hệ nổi FAB (Zalo, WeChat QR, Hotline) & sao chép 1 chạm.
 * - Hộp thoại xem ảnh phóng to (Lightbox).
 * =========================================================================
 */

(function () {
  const digits = (s) => (s ? String(s).replace(/\D/g, "") : "");

  // Hiển thị thông báo Toast nổi
  function showToast(msg) {
    let t = document.getElementById("toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "toast";
      t.className = "toast";
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.hidden = false;
    clearTimeout(showToast._timer);
    showToast._timer = setTimeout(() => {
      t.hidden = true;
    }, 2400);
  }
  window.toast = showToast;

  // Sao chép văn bản vào bộ nhớ đệm
  async function copyToClipboard(text, successMsg) {
    try {
      await navigator.clipboard.writeText(text.replace(/\s/g, ""));
      showToast(successMsg || `Đã sao chép: ${text}`);
    } catch (err) {
      // Fallback cho trình duyệt cũ hoặc khi chạy file:// không có Secure Context
      const input = document.createElement("input");
      input.value = text.replace(/\s/g, "");
      document.body.appendChild(input);
      input.select();
      document.execCommand("copy");
      document.body.removeChild(input);
      showToast(successMsg || `Đã sao chép: ${text}`);
    }
  }

  // Đồng bộ cấu hình từ config.js vào DOM
  function applyConfigToDOM() {
    const cfg = window.SITE_CONFIG || (typeof SITE_CONFIG !== "undefined" ? SITE_CONFIG : null);
    if (!cfg) return;

    // Cập nhật text liên hệ
    document.querySelectorAll("[data-c]").forEach((el) => {
      const key = el.dataset.c;
      if (key === "phone" && cfg.contact.hotlineDisplay) {
        el.textContent = cfg.contact.hotlineDisplay;
      } else if (key === "zalo" && cfg.contact.zalo) {
        el.textContent = cfg.contact.zalo;
      } else if (key === "wechat" && cfg.contact.wechat) {
        el.textContent = cfg.contact.wechat;
      } else if (key === "address" && cfg.brand.address) {
        el.textContent = cfg.brand.address;
      }
    });

    // Cập nhật các đường link gọi & chat
    const telNumber = digits(cfg.contact.hotline);
    const zaloNumber = digits(cfg.contact.zalo);

    const zaloLink = document.getElementById("zalo-link");
    if (zaloLink) zaloLink.href = `https://zalo.me/${zaloNumber}`;

    const telLink = document.getElementById("tel-link");
    if (telLink) telLink.href = `tel:${telNumber}`;

    const heroHotline = document.getElementById("hero-hotline");
    if (heroHotline) heroHotline.href = `tel:${telNumber}`;

    const promoCall = document.getElementById("promo-call");
    if (promoCall) promoCall.href = `tel:${telNumber}`;

    const wechatQrImg = document.getElementById("wechat-qr");
    if (wechatQrImg && cfg.contact.wechatQrImage) {
      wechatQrImg.src = cfg.contact.wechatQrImage;
    }

    const gmapsLink = document.getElementById("gmaps-link");
    if (gmapsLink && cfg.brand.googleMapsUrl) {
      gmapsLink.href = cfg.brand.googleMapsUrl;
    }
  }

  // Khởi tạo các nút liên hệ nổi FAB (WeChat, Zalo, Hotline)
  function initFloatingActions() {
    const fabButtons = document.querySelectorAll("[data-pop]");
    const popovers = document.querySelectorAll(".pop");

    fabButtons.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const targetId = btn.dataset.pop;
        const targetPop = document.getElementById(targetId);

        // Đóng các popover khác
        popovers.forEach((p) => {
          if (p.id !== targetId) p.hidden = true;
        });

        if (targetPop) {
          targetPop.hidden = !targetPop.hidden;
        }

        // Hiệu ứng nảy khi bấm
        btn.classList.remove("burst");
        void btn.offsetWidth;
        btn.classList.add("burst");

        fabButtons.forEach((b) => {
          b.classList.toggle("on", b === btn && targetPop && !targetPop.hidden);
        });
      });
    });

    // Đóng popover khi bấm nút X
    document.querySelectorAll(".pop .x").forEach((xBtn) => {
      xBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const pop = xBtn.closest(".pop");
        if (pop) pop.hidden = true;
        fabButtons.forEach((b) => b.classList.remove("on"));
      });
    });

    // Đóng popover khi bấm ra ngoài
    document.addEventListener("click", (e) => {
      if (!e.target.closest(".pop") && !e.target.closest(".fab-btn")) {
        popovers.forEach((p) => (p.hidden = true));
        fabButtons.forEach((b) => b.classList.remove("on"));
      }
    });

    // Nút sao chép số / WeChat ID
    document.querySelectorAll("[data-copy]").forEach((copyBtn) => {
      copyBtn.addEventListener("click", () => {
        const type = copyBtn.dataset.copy;
        const cfg = window.SITE_CONFIG ? window.SITE_CONFIG.contact : {};
        let val = "";
        if (type === "phone") val = cfg.hotline || "";
        else if (type === "zalo") val = cfg.zalo || "";
        else if (type === "wechat") val = cfg.wechat || "";

        if (val) {
          const msg = typeof window.T === "function" ? window.T("Đã sao chép ") + val : `Đã sao chép: ${val}`;
          copyToClipboard(val, msg);
        }
      });
    });
  }

  // Khởi tạo Menu cuộn phát sáng (Scroll Spy)
  function initScrollSpy() {
    const navLinks = Array.from(document.querySelectorAll('nav.links a[href^="#"]'));
    if (!navLinks.length) return;

    navLinks.forEach((a) => {
      a.addEventListener("click", () => {
        navLinks.forEach((x) => x.classList.toggle("on", x === a));
        a.classList.remove("flash");
        void a.offsetWidth;
        a.classList.add("flash");
      });
    });

    const targetMap = new Map();
    navLinks.forEach((a) => {
      const id = a.getAttribute("href").slice(1);
      const targetEl = document.getElementById(id);
      if (targetEl) targetMap.set(id, { link: a, element: targetEl });
    });

    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            const data = targetMap.get(entry.target.id);
            if (!data) return;
            if (entry.isIntersecting) {
              navLinks.forEach((x) => x.classList.toggle("on", x === data.link));
            } else if (data.link.classList.contains("on") && entry.boundingClientRect.top > 0) {
              data.link.classList.remove("on");
            }
          });
        },
        { rootMargin: "-35% 0px -55% 0px" }
      );

      targetMap.forEach((val) => observer.observe(val.element));
    }
  }

  // Khởi tạo lightbox xem ảnh toàn màn hình siêu nét
  function initGalleryLightbox() {
    // Hỗ trợ cả thư viện ảnh trang chủ, trang chi tiết quán và danh sách KTV
    const photoTargets = document.querySelectorAll(".gallery .photo, .ktv-gallery-item, [data-lightbox]");
    if (!photoTargets.length) return;

    let lightbox = document.getElementById("gallery-lightbox");
    if (!lightbox) {
      lightbox = document.createElement("div");
      lightbox.className = "ktv-lightbox";
      lightbox.id = "gallery-lightbox";
      lightbox.innerHTML = `
        <div class="ktv-lightbox-inner">
          <button class="ktv-lightbox-close" type="button" aria-label="Đóng">×</button>
          <img class="ktv-lightbox-img" id="lightbox-img" src="" alt="Phóng to ảnh phòng VIP">
          <div class="ktv-lightbox-caption" id="lightbox-caption"></div>
        </div>
      `;
      document.body.appendChild(lightbox);
    }

    const lbImg = document.getElementById("lightbox-img");
    const lbCap = document.getElementById("lightbox-caption");
    const lbClose = lightbox.querySelector(".ktv-lightbox-close");

    function closeLightbox() {
      lightbox.classList.remove("active");
      document.body.classList.remove("lock");
    }

    if (lbClose) lbClose.addEventListener("click", closeLightbox);
    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox || e.target.classList.contains("ktv-lightbox-inner")) {
        closeLightbox();
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && lightbox.classList.contains("active")) {
        closeLightbox();
      }
    });

    photoTargets.forEach((target) => {
      target.style.cursor = "zoom-in";
      target.addEventListener("click", () => {
        const img = target.querySelector("img");
        if (!img) return;
        lbImg.src = img.src;
        const caption = target.querySelector("figcaption");
        lbCap.textContent = caption ? caption.textContent : (img.alt || "Không gian phòng hát VIP");
        lightbox.classList.add("active");
        document.body.classList.add("lock");
      });
    });
  }

  // Khởi tạo tính năng Hỏi & Đáp Accordion tương tác
  function initFaqAccordion() {
    const faqItems = document.querySelectorAll(".ktv-faq-item");
    if (!faqItems.length) return;

    faqItems.forEach((item) => {
      const q = item.querySelector(".ktv-faq-q");
      if (!q) return;
      q.addEventListener("click", () => {
        const wasActive = item.classList.contains("active");
        // Đóng các câu hỏi khác nếu muốn chế độ đơn
        faqItems.forEach((other) => other.classList.remove("active"));
        if (!wasActive) {
          item.classList.add("active");
        }
      });
    });
  }

  // Khởi chạy toàn bộ ứng dụng
  function initApp() {
    applyConfigToDOM();
    initFloatingActions();
    initScrollSpy();
    initGalleryLightbox();
    initFaqAccordion();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initApp);
  } else {
    initApp();
  }
})();

