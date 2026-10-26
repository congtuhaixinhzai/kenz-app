/**
 * =========================================================================
 * SERVER CỤC BỘ SIÊU NHẸ (ZERO DEPENDENCIES) - KARAOKE KENZ WEB
 * =========================================================================
 * - Không cần cài đặt bất kỳ thư viện npm nào (dùng sẵn module http, fs, path).
 * - Tự động nhận diện mime-type cho html, css, js, jpg, png, svg.
 * - Khởi chạy cổng 3000 và tự mở trình duyệt.
 * =========================================================================
 */

const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 80;
const ROOT_DIR = __dirname;
const ZALO_URL = "http://192.168.1.245:3000";

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".webmanifest": "application/manifest+json; charset=utf-8"
};

const server = http.createServer((req, res) => {
  // Hỗ trợ CORS
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    res.writeHead(204);
    return res.end();
  }

  let reqPath = decodeURI(req.url.split("?")[0]);
  if (reqPath === "/") reqPath = "/index.html";

  // Endpoint kiểm tra trạng thái
  if (reqPath === "/status" || reqPath === "/api/status") {
    res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
    return res.end(JSON.stringify({
      server: "Karaoke Kenz Web Server",
      port: PORT,
      zaloServer: ZALO_URL,
      status: "online"
    }));
  }

  const filePath = path.join(ROOT_DIR, reqPath);

  // Chống Directory Traversal
  if (!filePath.startsWith(ROOT_DIR)) {
    res.writeHead(403);
    return res.end("403 Forbidden");
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { "Content-Type": "text/html; charset=utf-8" });
      return res.end("<h1>404 Không tìm thấy trang</h1><p><a href='/'>Quay lại trang chủ</a></p>");
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || "application/octet-stream";

    res.writeHead(200, {
      "Content-Type": contentType
    });

    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(PORT, () => {
  console.log("=======================================================");
  console.log(`🚀 KARAOKE KENZ WEB ĐANG CHẠY TRÊN CỔNG: ${PORT}`);
  console.log(`👉 Trang chủ:      http://localhost`);
  console.log(`👉 Quản trị test:  http://localhost/admin.html`);
  console.log(`👉 Chuyên mục tin: http://localhost/tin-tuc/tintuc.html`);
  console.log(`👉 Zalo Bot (3000): ${ZALO_URL}`);
  console.log("=======================================================");
  console.log("Bấm Ctrl + C trong cửa sổ này để tắt server khi xong.");
});
