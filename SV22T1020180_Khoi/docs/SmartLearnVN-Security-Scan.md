# smartlearnvn.site — Kiểm tra bảo mật thụ động (snapshot)

**Ngày tham chiếu:** kiểm tra tự động qua HTTP + đọc bundle Astro. **Không** thay thế pentest chuyên nghiệp.

**Trang:** [https://smartlearnvn.site/](https://smartlearnvn.site/)

---

## 1. Công nghệ phát hiện

- **Astro** (SSR/islands), React hydrate (`/_astro/*.js`).
- **API backend:** same-origin `https://smartlearnvn.site/api` (trong bundle: `baseURL` của Axios trỏ tới đây khi hostname ≠ `localhost`).
- **Auth:** JWT (hoặc token tương đương) lưu `localStorage` key `token`, gửi header `Authorization: Bearer <token>` (xem `authStore` + interceptor trong `api.*.js`).

---

## 2. Kiểm tra đường dẫn nhạy cảm (HEAD/GET)

| URL | Kết quả (thử nhanh) |
|-----|---------------------|
| `/.env` | **404** — tốt |
| `/config.js` | **404** — không giống site lộ `config.js` công khai |
| `/.git/config` | **404** — tốt |
| `/robots.txt` | **404** |

---

## 3. Lộ API key / secret trong JS tải về?

Trong các chunk đã tải (`api.*.js`, `Header.*.js`, `authStore.*.js`):

- **Không thấy** chuỗi kiểu `sk-`, `AIza`, `gsk_`, Supabase service key, hay URL gọi thẳng OpenAI/Groq từ client với Bearer cố định.
- Cấu hình API: `apiUrl` = `https://smartlearnvn.site/api` (production), `localhost:3000` khi dev — **không** nhúng secret trong snippet đã xem.

**Lưu ý:** Trang **AI Chat** (`/ai-chat`) có thể nạp thêm chunk JS; nếu cần chắc chắn 100%, cần rà toàn bộ `_astro/*.js` hoặc mở DevTools → Network khi vào đúng trang đó.

---

## 4. Vấn đề / điểm cần cải thiện

| Vấn đề | Mức | Chi tiết |
|--------|-----|----------|
| **Console.log trong bundle giao cho người dùng cuối** | Trung bình *(chỉ khi áp dụng cho production)* | Module `api.*.js` có thể chứa `console.log` request/response — **hợp lý khi dev / test API**; không có nghĩa là “thả bừa” nếu team chỉ bật lúc phát triển. Khuyến nghị: trên **bản production** thật (user tải về) nên tắt hoặc bọc `import.meta.env.DEV` / `process.env.NODE_ENV !== 'production'` để tránh lộ luồng dữ liệu cho bất kỳ ai mở DevTools. |

**Ghi chú:** Việc dùng console để test API là **thông lệ**; điểm cần nhất quán là **build triển khai cho khách** có còn log chi tiết hay không.
| **Token trong `localStorage`** | Phổ biến | Chuẩn SPA; rủi ro chính là **XSS** — cần CSP, sanitize input, dependency an toàn. |
| **`withCredentials: true`** | Cần hiểu | Dùng cookie cross-site cùng domain; đảm bảo CORS/SameSite đúng. |
| **Header không có security headers mạnh** | Tùy cấu hình nginx | Response thử chỉ thấy `Server: nginx/1.18.0` — nên bổ sung **HSTS**, **X-Frame-Options/Content-Security-Policy**, v.v. (kiểm tra đầy đủ bằng securityheaders.com hoặc tương đương). |

---

## 5. So sánh nhanh với site lộ key trong `config.js`

Site **EzLuyenThi** (trước đó): lộ Groq/Gemini trong `config.js` + gọi Groq từ browser — **mức rủi ro cao**.

**smartlearnvn.site** (trong phạm vi file đã xem): **không thấy** lộ key AI tương tự; API gom về **`/api`** same-origin — **mô hình bình thường hơn** (chi tiết AI nằm phía server nếu được triển khai đúng).

---

## 6. Khuyến nghị

1. Trên **artifact production** (file user thật tải): giảm / tắt **logging** chi tiết; giữ log đầy đủ ở **môi trường dev** khi test API là ổn.
2. Bật **CSP + HSTS** trên nginx.
3. Rà soát endpoint `/api` (auth, rate limit, upload).
4. Nếu có trang AI: xác nhận **không** có key trong bundle bằng cách build production và grep.

---

*Tài liệu nội bộ tham khảo kỹ thuật.*
