/**
 * KARAOKE KENZ - DYNAMIC VENUE VISIBILITY RUNTIME (ẨN/HIỆN QUÁN KTV THEO ADMIN)
 * - Tự động ẩn/hiện các quán KTV trên Lưới thẻ và Menu Dropdown theo cấu hình Admin.
 * - Tự động cập nhật bộ đếm số lượng quán KTV đang hoạt động theo thời gian thực.
 * - Hỗ trợ cả API Server máy chủ và LocalStorage cho chế độ ngoại tuyến.
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'kenz_venue_visibility';

  async function loadVisibility() {
    let vis = null;
    try {
      const resp = await fetch('/api/venue-visibility', { cache: 'no-store' });
      if (resp.ok) {
        vis = await resp.json();
        if (vis && typeof vis === 'object') {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(vis));
          return vis;
        }
      }
    } catch (e) {}

    try {
      const cached = localStorage.getItem(STORAGE_KEY);
      if (cached) {
        vis = JSON.parse(cached);
      }
    } catch (e) {}

    // Giá trị mặc định nếu chưa có cấu hình: chỉ bật Cầu Giấy & Đống Đa
    if (!vis && window.KTV_ALL_VENUES && Array.isArray(window.KTV_ALL_VENUES)) {
      vis = {};
      const activeDistricts = ['Cầu Giấy', 'Đống Đa'];
      window.KTV_ALL_VENUES.forEach(v => {
        vis[String(v.id)] = activeDistricts.includes(v.district);
      });
      localStorage.setItem(STORAGE_KEY, JSON.stringify(vis));
    }

    return vis || {};
  }

  function applyVenueVisibility(vis) {
    if (!vis || typeof vis !== 'object') return;

    // 1. Cập nhật thẻ quán trên trang danh mục & trang chủ
    const cards = document.querySelectorAll('.ktv-card[data-id]');
    let visibleCount = 0;
    const districtCounts = {};

    cards.forEach(card => {
      const id = card.getAttribute('data-id');
      const district = card.getAttribute('data-district') || '';
      const isVisible = vis[id] !== false; // Mặc định true nếu chưa có cấu hình

      if (isVisible) {
        card.style.display = '';
        visibleCount++;
        districtCounts[district] = (districtCounts[district] || 0) + 1;
      } else {
        card.style.display = 'none';
      }
    });

    // 2. Cập nhật các liên kết trong Mega Dropdown Menu
    const dropdownLinks = document.querySelectorAll('.ktv-dropdown-menu a[href*="karaoke-"]');
    if (dropdownLinks.length > 0 && window.KTV_ALL_VENUES) {
      const slugToIdMap = {};
      window.KTV_ALL_VENUES.forEach(v => {
        slugToIdMap[v.slug] = String(v.id);
      });

      dropdownLinks.forEach(link => {
        const href = link.getAttribute('href') || '';
        const slug = href.replace('.html', '').replace(/^\/+/, '');
        const vid = slugToIdMap[slug];
        if (vid) {
          const isVisible = vis[vid] !== false;
          link.style.display = isVisible ? '' : 'none';
        }
      });
    }

    // 3. Cập nhật số liệu hiển thị (Stats & Pill Counts)
    const totalCountEl = document.getElementById('ktv-total-count');
    if (totalCountEl && visibleCount > 0) {
      totalCountEl.textContent = `${visibleCount} quán`;
    }

    // Cập nhật bộ lọc Pills trên trang ktv-hanoi.html
    const allPillCount = document.querySelector('.ktv-filter-btn[data-district="all"] .count');
    if (allPillCount && visibleCount > 0) {
      allPillCount.textContent = visibleCount;
    }

    document.querySelectorAll('.ktv-filter-btn[data-district]').forEach(btn => {
      const dist = btn.getAttribute('data-district');
      if (dist && dist !== 'all') {
        const countSpan = btn.querySelector('.count');
        const c = districtCounts[dist] || 0;
        if (countSpan) {
          countSpan.textContent = c;
        }
        // Nếu quận này không có quán nào đang bật -> ẩn nút lọc quận đó
        if (c === 0) {
          btn.style.display = 'none';
        } else {
          btn.style.display = '';
        }
      }
    });
  }

  async function init() {
    const vis = await loadVisibility();
    applyVenueVisibility(vis);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Lắng nghe cập nhật khi Admin bật/tắt quán ở tab khác
  window.addEventListener('storage', (e) => {
    if (e.key === STORAGE_KEY) {
      try {
        const updated = JSON.parse(e.newValue || '{}');
        applyVenueVisibility(updated);
      } catch (err) {}
    }
  });

  window.KenzVenueRuntime = {
    load: loadVisibility,
    apply: applyVenueVisibility
  };
})();
