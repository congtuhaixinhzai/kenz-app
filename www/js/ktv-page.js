/**
 * =============================================================================
 * KTV HÀ NỘI - XỬ LÝ LỌC & TÌM KIẾM QUÁN KARAOKE KTV (LIVE FILTER & SEARCH)
 * Hoạt động trực tiếp trên 36 thẻ quán đã render sẵn trong HTML
 * =============================================================================
 */

(function () {
  let activeDistrict = "all";
  let searchKeyword = "";

  function getCards() {
    return document.querySelectorAll("#ktv-grid .ktv-card");
  }

  function filterVenues() {
    const cards = getCards();
    const query = searchKeyword.toLowerCase().trim();
    const totalCountEl = document.getElementById("ktv-total-count");
    const emptyEl = document.getElementById("ktv-empty-msg");
    const gridEl = document.getElementById("ktv-grid");

    let visibleCount = 0;

    cards.forEach((card) => {
      const cardDistrict = card.getAttribute("data-district") || "";
      const cardText = card.textContent.toLowerCase();

      const matchDistrict = (activeDistrict === "all") || (cardDistrict === activeDistrict);
      const matchSearch = !query || cardText.includes(query);

      if (matchDistrict && matchSearch) {
        card.style.display = "";
        visibleCount++;
      } else {
        card.style.display = "none";
      }
    });

    if (totalCountEl) {
      totalCountEl.textContent = `${visibleCount} quán`;
    }

    if (visibleCount === 0) {
      if (!emptyEl && gridEl) {
        const div = document.createElement("div");
        div.id = "ktv-empty-msg";
        div.className = "ktv-empty";
        div.style.gridColumn = "1 / -1";
        div.innerHTML = `
          <svg viewBox="0 0 24 24" fill="currentColor" width="48" height="48" style="color:#555178;margin-bottom:12px"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          <h3>Không tìm thấy quán nào phù hợp</h3>
          <p>Thử tìm với từ khóa khác (ví dụ: Cầu Giấy, Nguyễn Khang, Trần Thái Tông...) hoặc chọn mục "Tất cả".</p>
        `;
        gridEl.appendChild(div);
      } else if (emptyEl) {
        emptyEl.style.display = "";
      }
    } else if (emptyEl) {
      emptyEl.style.display = "none";
    }
  }

  function init() {
    const searchInput = document.getElementById("ktv-search");
    const filterBtns = document.querySelectorAll(".ktv-filter-btn");

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        searchKeyword = e.target.value;
        filterVenues();
      });
    }

    filterBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        filterBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        activeDistrict = btn.getAttribute("data-district") || "all";
        filterVenues();
      });
    });

    // Gắn sự kiện nút đặt phòng cho các thẻ
    document.querySelectorAll("#ktv-grid .btn-book-venue").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const venueName = btn.getAttribute("data-venue") || "";
        if (typeof window.openBooking === "function") {
          window.openBooking(venueName);
        }
      });
    });

    // Xử lý tham số URL ?id=XX hoặc ?venue=XX để cuộn và làm nổi bật quán
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const targetId = urlParams.get("id");
      if (targetId) {
        setTimeout(() => {
          const card = document.querySelector(`.ktv-card[data-id="${targetId}"]`);
          if (card) {
            card.scrollIntoView({ behavior: "smooth", block: "center" });
            card.classList.add("flash-highlight");
            setTimeout(() => card.classList.remove("flash-highlight"), 3500);
          }
        }, 300);
      }
    } catch (e) {}

    filterVenues();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
