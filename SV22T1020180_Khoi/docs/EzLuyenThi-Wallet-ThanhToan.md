# EzLuyenThi — Trang ví / nạp tiền (`/wallet`) & API liên quan

Phân tích tĩnh từ bundle JS (`/assets/index-*.js`) và `config.js` tại thời điểm soạn. **Không** thay thế tài liệu API chính thức từ chủ dịch vụ.

**URL ví dụ:** [https://ezluyenthi.id.vn/wallet?amount=59000](https://ezluyenthi.id.vn/wallet?amount=59000) — tham số `amount` có thể chỉ dùng **prefill giao diện**; số tiền thật cần được **xác thực phía server** khi tạo giao dịch.

---

## 1. Luồng dữ liệu tổng quan

| Thành phần | Vai trò |
|------------|---------|
| **SPA** | Trang `/wallet` render trong React; cùng `config.js` + Supabase client |
| **API same-origin** | Base **`/api/v1`** — một số route thanh toán (cần token) |
| **Supabase** | Bảng `profiles` (cột `wallet_balance`), `wallet_transactions`, `subscriptions`; Realtime để cập nhật số dư |
| **Bên thứ ba hiển thị QR** | **Sepay** — URL ảnh VietQR (`qr.sepay.vn`) với tham số ngân hàng / STK / nội dung |
| **Giao diện** | Copy chữ có nhắc **VNPay / Momo / Ngân hàng**, **VietQR** |

---

## 2. API backend (same-origin) — `https://ezluyenthi.id.vn`

Trong bundle có class gọi API với base **`/api/v1`** và token lấy từ **`localStorage.getItem("auth_token")`** (không phải anon Supabase cho các route này).

Các path **xuất hiện trong client** (thanh toán / ví):

| Method (ước lượng) | Path | Ghi chú |
|--------------------|------|---------|
| — | `/api/v1/payments/wallet/create-deposit` | Tạo / chuẩn bị giao dịch nạp |
| — | `/api/v1/payments/wallet/checkout` | Checkout ví |
| — | `/api/v1/payments/check-referral-code` | Kiểm tra mã giới thiệu |

**Lưu ý:** Chi tiết body (JSON), method GET/POST và mã lỗi phải xem trong **Network** khi đăng nhập thật hoặc tài liệu server. Gọi thử không có JWT thường trả **401**.

Các route khác trong cùng base (không thuần ví): ví dụ `/api/v1/ai-learning/roadmap`, `/api/v1/groq/chat`, `/api/v1/email/study-goal`.

---

## 3. Supabase (client)

- **`profiles`**: đọc `wallet_balance`; subscribe Realtime kênh kiểu `payment-balance-<userId>` / `upgrade-balance-<userId>` để nhận cập nhật sau nạp.
- **`wallet_transactions`**, **`subscriptions`**: dùng trong app (lịch sử / gói).

Anon key trong `config.js` chỉ có quyền theo **RLS** — không đồng nghĩa bypass được nạp tiền nếu server và RLS cấu hình đúng.

---

## 4. Sepay / VietQR (phía client)

Chuỗi tạo ảnh QR (rút gọn ý nghĩa):

```text
https://qr.sepay.vn/img?bank=<mã NH>&acc=<số TK>&amount=0&des=<nội dung CK>&template=compact
```

- `amount=0` trong snippet có thể là placeholder; nội dung chuyển khoản (`des`) thường chứa mã để **đối soát** với giao dịch trên server.
- Đây là dịch vụ **hiển thị QR** của bên thứ ba ([Sepay](https://sepay.vn)), không phải “API nạp tiền” trực tiếp của EzLuyenThi.

---

## 5. Đánh giá bảo mật (ngắn gọn)

| Vấn đề | Mức độ | Gợi ý (nếu bạn là chủ hệ thống) |
|--------|--------|----------------------------------|
| **`config.js` lộ Groq / Gemini API key** | Rất nghiêm trọng | Gỡ khỏi client; chỉ dùng env server; xoay key |
| **Supabase anon key công khai** | Bình thường cho SPA | RLS + không lưu bí mật trong DB readable by anon |
| **Token trong `localStorage`** | Phổ biến SPA | Chống XSS; HTTPS; không nhét secret nhạy cảm vào JWT payload client |
| **Thanh toán** | Phụ thuộc backend | Phải xác minh số tiền, chữ ký webhook (VNPay/Momo/…), idempotency — **không** tin hoàn toàn `amount` trên URL |
| **Bundle lộ đường dẫn API** | Bình thường | Bảo vệ bằng auth + rate limit + kiểm tra server |

**Kết luận:** Việc **lộ key AI trong `config.js`** là dấu hiệu bảo mật **kém ở khâu triển khai**, không nhất thiết do riêng trang ví. Luồng nạp tiền đúng vẫn phải dựa vào **API backend + cổng thanh toán + webhook** — phần đó không thể kết luận chỉ bằng đọc JS.

---

## 6. Cách tự kiểm tra trên trình duyệt

1. Đăng nhập → mở `/wallet?amount=59000`.
2. **F12 → Network**: lọc `Fetch/XHR`, thử nạp (hoặc bước tạo giao dịch).
3. Xem request tới `/api/v1/payments/...` (header `Authorization`, body).
4. Tab **Application → Local Storage**: key `auth_token` (hoặc tên tương đương).

---

## 7. Công cụ phân tích bundle trong repo

Script (chạy sau khi tải `index-*.js` vào file local):

- `scripts/probe_ez_wallet_bundle.py` — liệt kê path `/api/v1/...`, từ khóa thanh toán, snippet Sepay.

*Tài liệu mang tính kỹ thuật; tuân thủ ToS và pháp luật khi kiểm thử.*
