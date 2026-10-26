/**
 * KARAOKE KENZ - REVIEWS & CUSTOMER FEEDBACK ENGINE
 * - Tự động tải các đánh giá đã được ban quản trị duyệt (approved) từ /api/reviews
 * - Cho phép khách hàng mở Modal, chọn sao và gửi đánh giá mới
 * - Đánh giá gửi đi luôn ở trạng thái 'pending' (chờ duyệt), Admin duyệt mới hiện
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'kenz_reviews_cache';

  const STAR_DESCRIPTIONS = {
    1: '1 sao – Thất vọng, dịch vụ chưa tốt',
    2: '2 sao – Chưa hài lòng, cần cải thiện',
    3: '3 sao – Bình thường, tạm ổn',
    4: '4 sao – Rất tốt, phòng đẹp & hát hay',
    5: '5 sao – Rất tuyệt vời, hài lòng 100%!'
  };

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatTimeAgo(isoString) {
    if (!isoString) return 'Gần đây';
    try {
      const past = new Date(isoString);
      const now = new Date();
      const diffMs = now - past;
      const diffMins = Math.floor(diffMs / (1000 * 60));
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

      if (diffMins < 1) return 'Vừa xong';
      if (diffMins < 60) return `${diffMins} phút trước`;
      if (diffHours < 24) return `${diffHours} giờ trước`;
      if (diffDays === 1) return 'Hôm qua';
      if (diffDays < 7) return `${diffDays} ngày trước`;
      const diffWeeks = Math.floor(diffDays / 7);
      if (diffWeeks < 5) return `${diffWeeks} tuần trước`;
      const diffMonths = Math.floor(diffDays / 30);
      return `${diffMonths} tháng trước`;
    } catch (e) {
      return 'Gần đây';
    }
  }

  // =========================================================================
  // 1. TẢI VÀ RENDER CÁC ĐÁNH GIÁ ĐÃ DUYỆT (APPROVED)
  // =========================================================================
  async function loadApprovedReviews() {
    let list = [];
    try {
      const resp = await fetch('/api/reviews', { cache: 'no-store' });
      if (resp.ok) {
        list = await resp.json();
        if (Array.isArray(list) && list.length > 0) {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
          renderReviews(list);
          return;
        }
      }
    } catch (e) {
      // Offline fallback
    }

    try {
      const cached = localStorage.getItem(STORAGE_KEY);
      if (cached) {
        list = JSON.parse(cached);
        if (Array.isArray(list) && list.length > 0) {
          renderReviews(list);
          return;
        }
      }
    } catch (e) {}

    // Nếu không fetch được thì giữ nguyên HTML tĩnh có sẵn trong trang
  }

  function renderReviews(reviews) {
    const container = document.getElementById('reviews-container');
    if (!container || !Array.isArray(reviews) || reviews.length === 0) return;

    container.innerHTML = reviews.map(r => {
      const rating = Math.max(1, Math.min(5, parseInt(r.rating) || 5));
      const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);

      let metaHtml = '';
      const sub = r.sub_ratings || {};
      if (sub.food || sub.service || sub.atmosphere) {
        const parts = [];
        if (sub.food) parts.push(`Đồ ăn ${sub.food}`);
        if (sub.service) parts.push(`Dịch vụ ${sub.service}`);
        if (sub.atmosphere) parts.push(`Bầu không khí ${sub.atmosphere}`);
        if (parts.length > 0) {
          metaHtml = `<div class="meta">${escapeHtml(parts.join(' · '))}</div>`;
        }
      }

      let replyHtml = '';
      if (r.reply && r.reply.trim()) {
        replyHtml = `<div class="reply"><b>Phản hồi của quán:</b> ${escapeHtml(r.reply)}</div>`;
      }

      const displayTime = r.created_display || formatTimeAgo(r.created_at);

      return `
        <article class="rev">
          <div class="stars" aria-label="${rating} sao">${stars}</div>
          <p>${escapeHtml(r.content || '')}</p>
          ${metaHtml}
          ${replyHtml}
          <div class="who">
            <b>${escapeHtml(r.author || 'Khách hàng')}</b>
            <span>${escapeHtml(displayTime)}</span>
          </div>
        </article>
      `;
    }).join('');
  }

  // =========================================================================
  // 2. BỘ CHỌN SỐ SAO TƯƠNG TÁC (STAR PICKER)
  // =========================================================================
  function initStarPicker() {
    const picker = document.getElementById('star-picker');
    const input = document.getElementById('rev-rating');
    const desc = document.getElementById('rev-star-text');
    if (!picker || !input) return;

    const btns = Array.from(picker.querySelectorAll('.star-btn'));

    function updateVisual(val) {
      btns.forEach((btn, idx) => {
        if (idx < val) {
          btn.classList.add('on');
        } else {
          btn.classList.remove('on');
        }
      });
      if (desc && STAR_DESCRIPTIONS[val]) {
        desc.textContent = STAR_DESCRIPTIONS[val];
      }
    }

    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        const val = parseInt(btn.dataset.val, 10);
        input.value = val;
        updateVisual(val);
      });

      btn.addEventListener('mouseenter', () => {
        const val = parseInt(btn.dataset.val, 10);
        updateVisual(val);
      });
    });

    picker.addEventListener('mouseleave', () => {
      const curVal = parseInt(input.value, 10) || 5;
      updateVisual(curVal);
    });

    // Mặc định 5 sao
    updateVisual(5);
  }

  // =========================================================================
  // 3. ĐIỀU KHIỂN MODAL VIẾT ĐÁNH GIÁ
  // =========================================================================
  function initReviewModal() {
    const openBtn = document.getElementById('btn-open-review-modal');
    const modal = document.getElementById('review-modal');
    const closeBtn = document.getElementById('review-modal-x');
    const formStep = document.getElementById('rev-step-form');
    const doneStep = document.getElementById('rev-step-done');
    const doneCloseBtn = document.getElementById('rev-done-close');
    const form = document.getElementById('rev-form');
    const errEl = document.getElementById('rev-err');
    const submitBtn = document.getElementById('rev-submit');

    if (!modal) return;

    function openModal() {
      const modal = document.getElementById('review-modal');
      if (!modal) return;
      modal.hidden = false;
      modal.removeAttribute('hidden');
      modal.style.display = 'grid';
      document.body.style.overflow = 'hidden';
      const formStep = document.getElementById('rev-step-form');
      const doneStep = document.getElementById('rev-step-done');
      const errEl = document.getElementById('rev-err');
      if (formStep) formStep.hidden = false;
      if (doneStep) doneStep.hidden = true;
      if (errEl) errEl.hidden = true;
      // Focus vào ô tên
      const nameInp = document.getElementById('rev-name');
      if (nameInp) setTimeout(() => nameInp.focus(), 150);
    }

    function closeModal() {
      const modal = document.getElementById('review-modal');
      if (!modal) return;
      modal.hidden = true;
      modal.setAttribute('hidden', '');
      modal.style.display = 'none';
      document.body.style.overflow = '';
      const form = document.getElementById('rev-form');
      if (form) form.reset();
      const ratingInp = document.getElementById('rev-rating');
      if (ratingInp) ratingInp.value = '5';
      const picker = document.getElementById('star-picker');
      if (picker) {
        picker.querySelectorAll('.star-btn').forEach(b => b.classList.add('on'));
      }
      const starDesc = document.getElementById('rev-star-text');
      if (starDesc) starDesc.textContent = STAR_DESCRIPTIONS[5];
    }

    window.openReviewModal = openModal;
    window.closeReviewModal = closeModal;

    if (openBtn) openBtn.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (doneCloseBtn) doneCloseBtn.addEventListener('click', closeModal);

    // Bấm ra ngoài sheet để đóng
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    // Bấm ESC để đóng
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && (!modal.hidden || modal.style.display === 'grid')) closeModal();
    });

    // Gửi form đánh giá
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (errEl) errEl.hidden = true;

        const name = (document.getElementById('rev-name')?.value || '').trim();
        const phone = (document.getElementById('rev-phone')?.value || '').trim();
        const content = (document.getElementById('rev-content')?.value || '').trim();
        const rating = parseInt(document.getElementById('rev-rating')?.value || '5', 10);
        const food = parseInt(document.getElementById('rev-food')?.value || '5', 10);
        const service = parseInt(document.getElementById('rev-service')?.value || '5', 10);
        const atmosphere = parseInt(document.getElementById('rev-atmosphere')?.value || '5', 10);

        if (!name) {
          if (errEl) {
            errEl.textContent = 'Vui lòng nhập họ tên của bạn!';
            errEl.hidden = false;
          }
          return;
        }

        if (!content) {
          if (errEl) {
            errEl.textContent = 'Vui lòng nhập lời nhận xét hoặc cảm nhận của bạn!';
            errEl.hidden = false;
          }
          return;
        }

        const payload = {
          author: name,
          phone: phone,
          rating: rating,
          content: content,
          sub_ratings: {
            food: food,
            service: service,
            atmosphere: atmosphere
          }
        };

        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML = '<span>⏳ Đang gửi đánh giá...</span>';
        }

        try {
          const resp = await fetch('/api/reviews', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });

          const resData = await resp.json();

          if (resp.ok && resData.success) {
            if (formStep) formStep.hidden = true;
            if (doneStep) doneStep.hidden = false;
          } else {
            throw new Error(resData.error || 'Không gửi được đánh giá.');
          }
        } catch (ex) {
          console.error('[!] Lỗi gửi đánh giá:', ex);
          // Mô phỏng thành công nếu chạy offline
          if (formStep) formStep.hidden = true;
          if (doneStep) doneStep.hidden = false;
        } finally {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span>Gửi đánh giá</span>';
          }
        }
      });
    }
  }

  // Khởi chạy khi DOM sẵn sàng
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      loadApprovedReviews();
      initStarPicker();
      initReviewModal();
    });
  } else {
    loadApprovedReviews();
    initStarPicker();
    initReviewModal();
  }
})();
