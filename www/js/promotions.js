/**
 * KARAOKE KENZ - DYNAMIC PROMOTIONS ENGINE (QUẢN LÝ ƯU ĐÃI & TỰ ĐỘNG HẾT HẠN)
 * - Tự động ẩn hoàn toàn mục Ưu đãi khi không có chương trình nào hoạt động.
 * - Tự động ẩn ngay lập tức khi chương trình quá ngày hết hạn (Expiry Date).
 * - Tự động hiển thị và cập nhật nội dung khi Admin thêm ưu đãi mới.
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'kenz_promotions';

  function getTodayString() {
    const d = new Date();
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
  }

  function formatDisplayDate(dateStr) {
    if (!dateStr) return '';
    const parts = dateStr.split('-');
    if (parts.length === 3) {
      return `${parts[2]}/${parts[1]}/${parts[0]}`;
    }
    return dateStr;
  }

  async function loadPromotions() {
    let promos = [];
    try {
      const resp = await fetch('/api/promotions', { cache: 'no-store' });
      if (resp.ok) {
        promos = await resp.json();
        if (Array.isArray(promos)) {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(promos));
          return promos;
        }
      }
    } catch (e) {
      // Offline fallback
    }

    try {
      const cached = localStorage.getItem(STORAGE_KEY);
      if (cached) {
        promos = JSON.parse(cached);
      }
    } catch (e) {}

    return Array.isArray(promos) ? promos : [];
  }

  function getValidPromotions(promos) {
    const today = getTodayString();
    return promos.filter(p => {
      if (!p || p.active === false) return false;
      if (p.startDate && p.startDate > today) return false;
      if (p.endDate && p.endDate < today) return false; // Quá ngày hết hạn -> Tự động ẩn!
      return true;
    });
  }

  function applyPromotionsUI(validPromos) {
    const promoSection = document.getElementById('uu-dai');
    const promoNavLinks = document.querySelectorAll('a[href*="#uu-dai"]');

    if (!validPromos || validPromos.length === 0) {
      // TẮT HOÀN TOÀN MỤC ƯU ĐÃI NẾU KHÔNG CÓ HOẶC ĐÃ HẾT HẠN
      if (promoSection) {
        promoSection.style.display = 'none';
        promoSection.setAttribute('aria-hidden', 'true');
      }
      promoNavLinks.forEach(link => {
        link.style.display = 'none';
      });
      return;
    }

    // NẾU CÓ ƯU ĐÃI CÒN HẠN: HIỂN THỊ VÀ CẬP NHẬT NỘI DUNG
    if (promoSection) {
      promoSection.style.display = '';
      promoSection.removeAttribute('aria-hidden');

      const current = validPromos[0];
      const titleEl = promoSection.querySelector('h2');
      const descEl = promoSection.querySelector('.promo-text > p.muted');
      const perksUl = promoSection.querySelector('.perks');
      const imgEl = promoSection.querySelector('.promo-img img');
      const imgWrap = promoSection.querySelector('.promo-img');

      if (current.title && titleEl) {
        titleEl.textContent = current.title;
      }
      if (current.description && descEl) {
        descEl.textContent = current.description;
      }
      if (current.banner && imgEl) {
        imgEl.src = current.banner;
        if (imgWrap) imgWrap.href = current.banner;
      }

      // Render danh sách quyền lợi / perks nếu có
      if (Array.isArray(current.perks) && current.perks.length > 0 && perksUl) {
        perksUl.innerHTML = current.perks.map(p => `
          <li>
            <span class="perk-ico" aria-hidden="true">${p.icon || '🎁'}</span>
            <div>
              <b>${p.title || 'Ưu đãi đặc biệt'}</b>
              <small>${p.desc || ''}</small>
            </div>
          </li>
        `).join('');
      }

      // Hiển thị huy hiệu hạn sử dụng rõ ràng
      let expiryBadge = promoSection.querySelector('.promo-expiry-badge');
      if (!expiryBadge && current.endDate) {
        expiryBadge = document.createElement('div');
        expiryBadge.className = 'promo-expiry-badge';
        expiryBadge.style.cssText = 'display:inline-flex;align-items:center;gap:6px;background:rgba(255,209,102,0.15);border:1px solid rgba(255,209,102,0.4);color:#ffd166;padding:6px 14px;border-radius:20px;font-size:0.86rem;font-weight:700;margin-top:14px';
        const promoText = promoSection.querySelector('.promo-text');
        if (promoText) {
          promoText.insertBefore(expiryBadge, promoText.querySelector('.hotline') || null);
        }
      }
      if (expiryBadge) {
        if (current.endDate) {
          expiryBadge.innerHTML = `⏰ Áp dụng đến hết ngày: <b>${formatDisplayDate(current.endDate)}</b>`;
          expiryBadge.style.display = 'inline-flex';
        } else {
          expiryBadge.style.display = 'none';
        }
      }
    }

    promoNavLinks.forEach(link => {
      link.style.display = '';
    });
  }

  async function init() {
    // Ẩn trước ngay lập tức khi chưa có dữ liệu để tránh giật giao diện
    const promoSection = document.getElementById('uu-dai');
    if (promoSection && !localStorage.getItem(STORAGE_KEY)) {
      promoSection.style.display = 'none';
      document.querySelectorAll('a[href*="#uu-dai"]').forEach(l => l.style.display = 'none');
    }

    const promos = await loadPromotions();
    const valid = getValidPromotions(promos);
    applyPromotionsUI(valid);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Đồng bộ khi có thay đổi từ trang Admin ở tab khác
  window.addEventListener('storage', (e) => {
    if (e.key === STORAGE_KEY) {
      try {
        const updated = JSON.parse(e.newValue || '[]');
        applyPromotionsUI(getValidPromotions(updated));
      } catch (err) {}
    }
  });

  window.KenzPromotions = {
    load: loadPromotions,
    getValid: getValidPromotions,
    apply: applyPromotionsUI
  };
})();
