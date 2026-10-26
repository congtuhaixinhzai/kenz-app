/**
 * =========================================================================
 * BỘ MÁY ĐẶT PHÒNG TRỰC TUYẾN (BOOKING ENGINE) - KARAOKE KENZ WEB
 * =========================================================================
 * - Kiểm tra tính hợp lệ dữ liệu (Tên, SĐT Việt Nam, Ngày, Giờ, Bẫy bot Honeypot).
 * - Tự động tạo mã đặt phòng độc nhất (VD: KZ-8291).
 * - Lưu trữ cục bộ vào LocalStorage ("karaoke_bookings") để test ngay trên Windows.
 * - Hỗ trợ gửi thông báo tức thì về Telegram Bot nếu cấu hình trong config.js.
 * =========================================================================
 */

(function () {
  const pad = (n) => String(n).padStart(2, "0");
  const ymd = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

  let lastFocus = null;

  function generateBookingCode() {
    const prefix = (window.SITE_CONFIG && window.SITE_CONFIG.booking && window.SITE_CONFIG.booking.codePrefix) || "KZ-";
    const randNum = Math.floor(1000 + Math.random() * 9000);
    return `${prefix}${randNum}`;
  }

  function parseTime(val) {
    if (!val) return null;
    const m = val.trim().match(/^(\d{1,2})(?:[:hH.](\d{1,2})?)?$/);
    if (!m) return null;
    const h = +m[1];
    const mi = +(m[2] || 0);
    if (h > 23 || mi > 59) return null;
    return `${pad(h)}:${pad(mi)}`;
  }

  // Lưu đơn vào LocalStorage
  function saveBookingLocally(booking) {
    try {
      const existing = JSON.parse(localStorage.getItem("karaoke_bookings") || "[]");
      existing.unshift(booking);
      localStorage.setItem("karaoke_bookings", JSON.stringify(existing));
      window.dispatchEvent(new CustomEvent("karaoke_new_booking", { detail: booking }));
    } catch (e) {
      console.warn("Không thể lưu đơn vào LocalStorage:", e);
    }
  }

  function escapeHtml(text) {
    if (!text) return "";
    return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Gửi thông báo đến Telegram Bot (nếu bật)
  async function notifyTelegram(booking) {
    const siteConfig = window.SITE_CONFIG || (typeof SITE_CONFIG !== "undefined" ? SITE_CONFIG : null);
    const cfg = siteConfig && siteConfig.booking && siteConfig.booking.telegram;
    if (!cfg || !cfg.enabled || !cfg.botToken || !cfg.chatId) {
      console.warn("Telegram chưa được bật hoặc thiếu cấu hình:", cfg);
      return;
    }

    const text = `🎤 <b>ĐƠN ĐẶT PHÒNG MỚI - KARAOKE KENZ</b>
━━━━━━━━━━━━━━━━━━━━
🔖 <b>Mã đặt:</b> <code>${escapeHtml(booking.code)}</code>
🏢 <b>Cơ sở:</b> ${escapeHtml(booking.venue || "Karaoke Kenz 202 Trung Kính")}
👤 <b>Khách hàng:</b> ${escapeHtml(booking.name)}
📞 <b>Số điện thoại:</b> <code>${escapeHtml(booking.phone)}</code>
📅 <b>Ngày hát:</b> ${escapeHtml(booking.date)}
⏰ <b>Giờ đến:</b> ${escapeHtml(booking.time)}
📝 <b>Ghi chú:</b> ${escapeHtml(booking.note || "Không có")}
⏱ <b>Thời gian gửi:</b> ${new Date(booking.createdAt).toLocaleString("vi-VN")}`;

    const url = `https://api.telegram.org/bot${cfg.botToken}/sendMessage`;
    const params = new URLSearchParams();
    params.append("chat_id", cfg.chatId);
    params.append("text", text);
    params.append("parse_mode", "HTML");

    console.log("Đang gửi thông báo Telegram...", cfg.chatId);

    try {
      await fetch(url, {
        method: "POST",
        mode: "no-cors",
        body: params
      });
      console.log("Đã gửi Telegram thành công!");
    } catch (err) {
      try {
        await fetch(`${url}?${params.toString()}`, { mode: "no-cors" });
      } catch (e2) {
        window._tgBeacon = new Image();
        window._tgBeacon.src = `${url}?${params.toString()}`;
      }
    }
  }

  // Gửi thông báo đến Zalo Bot (nếu bật)
  async function notifyZalo(booking) {
    const siteConfig = window.SITE_CONFIG || (typeof SITE_CONFIG !== "undefined" ? SITE_CONFIG : null);
    const cfg = siteConfig && siteConfig.booking && siteConfig.booking.zaloBot;
    if (!cfg || !cfg.enabled || !cfg.serviceUrl) return;

    try {
      await fetch(cfg.serviceUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(booking)
      });
      console.log("Đã kích hoạt gửi qua Zalo Bot service.");
    } catch (err) {
      // Bỏ qua nếu service chưa bật để không ảnh hưởng khách
    }
  }

  let currentSelectedVenue = "Karaoke Kenz Club 202 Trung Kính";

  function openBooking(venue, room) {
    if (venue && typeof venue === "string") {
      currentSelectedVenue = venue;
    } else {
      currentSelectedVenue = "Karaoke Kenz Club 202 Trung Kính";
    }

    lastFocus = document.activeElement;
    document.querySelectorAll(".pop").forEach((p) => (p.hidden = true));
    document.querySelectorAll(".fab-btn").forEach((b) => b.classList.remove("on"));

    const formStep = document.getElementById("bk-step-form");
    const doneStep = document.getElementById("bk-step-done");
    const errBox = document.getElementById("f-err");
    const modal = document.getElementById("modal");
    const dateInput = document.getElementById("f-date");
    const nameInput = document.getElementById("f-name");
    const noteInput = document.getElementById("f-note");
    const venueDisplay = document.getElementById("f-selected-venue");
    const venueInput = document.getElementById("f-venue");

    if (venueDisplay) venueDisplay.textContent = currentSelectedVenue;
    if (venueInput) venueInput.value = currentSelectedVenue;
    if (room && noteInput && (!noteInput.value || noteInput.value.startsWith("Yêu cầu: "))) {
      noteInput.value = `Yêu cầu: ${room}`;
    }

    if (formStep) formStep.hidden = false;
    if (doneStep) doneStep.hidden = true;
    if (errBox) errBox.hidden = true;

    const todayStr = ymd(new Date());
    if (dateInput) {
      dateInput.min = todayStr;
      if (!dateInput.value || dateInput.value < todayStr) {
        dateInput.value = todayStr;
      }
    }

    if (modal) {
      modal.hidden = false;
      document.body.classList.add("lock");
      if (typeof window.getCurrentLang === "function" && window.getCurrentLang() === "zh" && typeof window.setLanguage === "function") {
        window.setLanguage("zh");
      }
    }

    setTimeout(() => {
      if (nameInput) nameInput.focus();
    }, 40);
  }

  window.openBooking = openBooking;

  function closeBooking() {
    const modal = document.getElementById("modal");
    if (modal) {
      modal.hidden = true;
      document.body.classList.remove("lock");
    }
    if (lastFocus && typeof lastFocus.focus === "function") {
      lastFocus.focus();
    }
  }

  function initBooking() {
    // Nút mở modal
    document.querySelectorAll("[data-book], .btn-book-venue").forEach((b) => {
      b.addEventListener("click", () => {
        const v = b.getAttribute("data-venue") || "Karaoke Kenz Club 202 Trung Kính";
        const room = b.getAttribute("data-room");
        openBooking(v, room);
      });
    });

    // Nút đóng modal
    const closeBtn = document.getElementById("modal-x");
    const doneCloseBtn = document.getElementById("d-close");
    const modal = document.getElementById("modal");
    const againBtn = document.getElementById("d-again");
    const timeInput = document.getElementById("f-time");
    const form = document.getElementById("bk-form");

    if (closeBtn) closeBtn.addEventListener("click", closeBooking);
    if (doneCloseBtn) doneCloseBtn.addEventListener("click", closeBooking);
    if (modal) {
      modal.addEventListener("click", (e) => {
        if (e.target.id === "modal") closeBooking();
      });
    }

    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal && !modal.hidden) {
        closeBooking();
      }
    });

    if (againBtn) {
      againBtn.addEventListener("click", () => {
        const formStep = document.getElementById("bk-step-form");
        const doneStep = document.getElementById("bk-step-done");
        if (doneStep) doneStep.hidden = true;
        if (formStep) formStep.hidden = false;
        if (timeInput) timeInput.focus();
      });
    }

    // Tự động thêm dấu : khi gõ giờ (ví dụ "1930" -> "19:30")
    if (timeInput) {
      timeInput.addEventListener("input", (e) => {
        const t = e.target;
        const d = t.value.replace(/\D/g, "").slice(0, 4);
        if (/^\d{1,2}[:hH.]\d{0,2}$/.test(t.value)) return;
        t.value = d.length > 2 ? `${d.slice(0, 2)}:${d.slice(2)}` : d;
      });
    }

    // Xử lý gửi Form
    if (form) {
      form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const errBox = document.getElementById("f-err");
        const nameInput = document.getElementById("f-name");
        const phoneInput = document.getElementById("f-phone");
        const dateInput = document.getElementById("f-date");
        const noteInput = document.getElementById("f-note");
        const honeypot = document.getElementById("f-website");
        const submitBtn = document.getElementById("f-submit");

        const fail = (msg, inputEl) => {
          if (errBox) {
            errBox.textContent = typeof window.T === "function" ? window.T(msg) : msg;
            errBox.hidden = false;
          }
          if (inputEl) {
            inputEl.classList.add("bad");
            inputEl.focus();
          }
        };

        if (errBox) errBox.hidden = true;
        document.querySelectorAll(".bad").forEach((el) => el.classList.remove("bad"));

        // Chống bot spam (Honeypot)
        if (honeypot && honeypot.value.trim() !== "") {
          closeBooking();
          return;
        }

        const name = nameInput ? nameInput.value.trim() : "";
        const phone = phoneInput ? phoneInput.value.replace(/[\s.\-]/g, "") : "";
        const date = dateInput ? dateInput.value : "";
        const rawTime = timeInput ? timeInput.value : "";
        const time = parseTime(rawTime);
        const note = noteInput ? noteInput.value.trim() : "";

        // Kiểm tra hợp lệ (Validation)
        if (name.length < 2) {
          return fail("Nhập họ tên để nhân viên gọi xác nhận.", nameInput);
        }
        if (!/^(0|\+84)\d{9}$/.test(phone)) {
          return fail("Số điện thoại chưa đúng, ví dụ 0912345678.", phoneInput);
        }
        if (!date) {
          return fail("Chọn ngày đặt.", dateInput);
        }
        if (date < ymd(new Date())) {
          return fail("Ngày đặt đã qua, chọn lại ngày khác.", dateInput);
        }
        if (!time) {
          return fail("Nhập giờ đến, ví dụ 19:30.", timeInput);
        }

        const targetDateTime = new Date(`${date}T${time}`);
        if (!isNaN(targetDateTime.getTime()) && targetDateTime < new Date()) {
          return fail("Giờ này đã qua, vui lòng chọn giờ hoặc ngày khác.", timeInput);
        }

        if (timeInput) timeInput.value = time;

        // Bắt đầu quá trình tạo đơn
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = typeof window.T === "function" ? window.T("Đang gửi…") : "Đang gửi…";
        }

        const bookingCode = generateBookingCode();
        const venueVal = (document.getElementById("f-venue") ? document.getElementById("f-venue").value : currentSelectedVenue) || currentSelectedVenue;
        const bookingData = {
          id: "bk_" + Date.now(),
          code: bookingCode,
          venue: venueVal,
          name: name,
          phone: phone,
          date: date,
          time: time,
          note: note,
          status: "Mới đặt",
          createdAt: new Date().toISOString()
        };

        // Lưu đơn và thông báo song song (Telegram + Zalo Bot)
        saveBookingLocally(bookingData);
        notifyTelegram(bookingData);
        notifyZalo(bookingData);

        // Hiển thị màn hình xác nhận thành công
        const codeDisplay = document.getElementById("d-code");
        const listDisplay = document.getElementById("d-list");
        const formStep = document.getElementById("bk-step-form");
        const doneStep = document.getElementById("bk-step-done");

        if (codeDisplay) codeDisplay.textContent = bookingCode;

        if (listDisplay) {
          const dObj = new Date(`${date}T00:00`);
          const weekdayStr = typeof window.getI18nWeekday === "function" ? window.getI18nWeekday(dObj.getDay()) : "T" + (dObj.getDay() + 1);
          const lang = typeof window.getCurrentLang === "function" ? window.getCurrentLang() : "vi";
          const formattedDate = `${time}${lang === "zh" ? "，" : ", "} ${weekdayStr} ${pad(dObj.getDate())}/${pad(dObj.getMonth() + 1)}`;

          listDisplay.innerHTML = `
            <dt>${typeof window.T === "function" ? window.T("Cơ sở đặt") : "Cơ sở"}</dt>
            <dd style="color:var(--amber,#ffd166);font-weight:700">${escapeHtml(venueVal)}</dd>
            <dt>${typeof window.T === "function" ? window.T("Họ và tên") : "Họ tên"}</dt>
            <dd>${name}</dd>
            <dt>${typeof window.T === "function" ? window.T("Số điện thoại") : "Điện thoại"}</dt>
            <dd>${phone}</dd>
            <dt>${typeof window.T === "function" ? window.T("Thời gian") : "Thời gian"}</dt>
            <dd>${formattedDate}</dd>
            ${note ? `<dt>${typeof window.T === "function" ? window.T("Ghi chú") : "Ghi chú"}</dt><dd>${note}</dd>` : ""}
          `;
        }

        // Cập nhật nút nhắn Zalo trực tiếp
        const zaloBtn = document.getElementById("d-zalo-btn");
        if (zaloBtn) {
          const cfg = window.SITE_CONFIG ? window.SITE_CONFIG.contact : {};
          const zaloPhone = (cfg.zalo || "0342 092 999").replace(/\D/g, "");
          const noteText = note ? ` Ghi chú: ${note}.` : "";
          const zaloMsg = `Chào quán Karaoke Kenz, tôi vừa đặt phòng tại ${venueVal} trên web. Mã đặt: ${bookingCode}, Tên: ${name}, SĐT: ${phone}, Giờ đến: ${time} ngày ${date}.${noteText} Nhờ quán xác nhận giữ phòng giúp tôi nhé!`;
          
          zaloBtn.href = `https://zalo.me/${zaloPhone}`;
          zaloBtn.onclick = () => {
            try {
              navigator.clipboard.writeText(zaloMsg);
              if (typeof window.toast === "function") {
                window.toast("Đã sao chép nội dung đặt phòng, đang chuyển đến Zalo...");
              }
            } catch (err) {}
          };
        }

        if (formStep) formStep.hidden = true;
        if (doneStep) doneStep.hidden = false;

        if (timeInput) timeInput.value = "";
        if (noteInput) noteInput.value = "";

        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = typeof window.T === "function" ? window.T("Gửi yêu cầu đặt bàn") : "Gửi yêu cầu đặt bàn";
        }
      });
    }
  }

  // Mở ra phạm vi toàn cục
  window.openBookingModal = openBooking;
  window.closeBookingModal = closeBooking;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initBooking);
  } else {
    initBooking();
  }
})();
