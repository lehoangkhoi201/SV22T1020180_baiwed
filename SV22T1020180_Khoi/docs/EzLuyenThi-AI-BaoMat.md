# EzLuyenThi — API AI & đánh giá lộ lọt bảo mật

Tài liệu dựa trên: `https://ezluyenthi.id.vn/config.js` và bundle `index-CBK9Z4Kd.js` (có thể đổi tên khi deploy). **Không** nhúng secret thật vào file này.

---

## 1. Tóm tắt bảo mật (quan trọng)

| Hạng mục | Mức độ | Ghi chú |
|----------|--------|---------|
| **`config.js` lộ `groqApiKey`** | **Rất nghiêm trọng** | Key Groq đủ để gọi API Groq từ bất kỳ máy nào, tốn quota / lạm dụng. |
| **`config.js` lộ `geminiApiKey` (Google AI)** | **Rất nghiêm trọng** | Tương tự — không được đặt trong file JS công khai. |
| **`supabaseUrl` + `supabaseKey` (anon)** | Chấp nhận được cho SPA | Quyền thật do RLS; anon không phải “master key”. |
| **Gọi Groq từ trình duyệt** | **Rất nghiêm trọng** | Trong bundle có `fetch("https://api.groq.com/openai/v1/chat/completions", …)` với header `Authorization: Bearer …` — token lấy từ runtime (cùng nguồn với key trong `config.js`). Bất kỳ ai mở DevTools đều có thể **copy key** và dùng ngoài trang. |
| **Lộ cấu trúc route `/api/v1/...`** | Trung bình | Giúp attacker lập bản đồ endpoint; vẫn cần auth cho phần nhạy cảm. |

**Kết luận:** Việc lộ **Groq + Gemini** trong `config.js` và (đối với Groq) khả năng gọi **trực tiếp từ client** là mức **bảo mật kém rõ rệt** — cần chuyển toàn bộ gọi AI sang **backend**, key chỉ trên server hoặc dùng proxy có kiểm soát.

---

## 2. Nội dung `config.js` (loại dữ liệu, không ghi secret)

Object `window.__APP_CONFIG__` thường gồm:

- `supabaseUrl`, `supabaseKey` — Supabase (anon).
- `groqApiKey` — **Groq API key** (dạng `gsk_...`).
- `geminiApiKey` — **Google Gemini / Generative Language API** (dạng `AIza...`).

→ **Không** được commit các giá trị này vào repo; chủ hệ thống nên **xoay (rotate) key** sau khi đã lộ công khai.

---

## 3. API liên quan AI — same-origin `https://ezluyenthi.id.vn`

Các path xuất hiện trong bundle (một số có `$` là tham số động):

### 3.1. Nhóm AI / học tập / chat

| Path | Gợi ý chức năng |
|------|------------------|
| `POST/GET` (tùy server) `/api/v1/groq/chat` | Chat qua backend (proxy Groq — an toàn hơn nếu key không nằm client) |
| `/api/v1/ai-learning/roadmap` | Lộ trình học AI |
| `/api/v1/ai-learning/roadmap/$` | Chi tiết / thao tác theo id |
| `/api/v1/ai-learning/roadmap/task-lesson` | Bài học theo task |
| `/api/v1/ai-learning/analyze/$` | Phân tích |
| `/api/v1/ai-learning/analysis/$` | Phân tích (biến thể) |
| `/api/v1/ai/generate-slides` | Tạo slide (AI) |
| `/api/v1/email/study-goal` | Gửi email mục tiêu học (có thể gọi AI phía server) |

### 3.2. Hạn mức / usage

| Path | Gợi ý |
|------|--------|
| `/api/v1/usage/check/$` | Kiểm tra quota |
| `/api/v1/usage/record` | Ghi nhận usage |

### 3.3. API khác xuất hiện cùng bundle (không thuần AI nhưng lộ bề mặt tấn công)

| Path |
|------|
| `/api/v1/admin/users`, `/api/v1/admin/users/$` |
| `/api/v1/admin/transactions`, `/api/v1/admin/transactions/$` |
| `/api/v1/admin/collaborators`, `.../add`, `.../remove` |
| `/api/v1/admin/course-purchases`, `/api/v1/admin/tool-purchases` |
| `/api/v1/payments/wallet/*`, `/api/v1/users/$` |

Các route admin thường yêu cầu **quyền quản trị** — không thử truy cập trái phép.

---

## 4. API bên thứ ba (AI) thấy trong bundle

| URL / pattern | Ghi chú |
|---------------|---------|
| `https://api.groq.com/openai/v1/chat/completions` | **Gọi trực tiếp từ browser** với Bearer token — trùng với rủi ro key trong `config.js`. |
| Có thể có tham chiếu tài liệu / marketing `anthropic.com` | Không nhất thiết là tích hợp API. |

Google Gemini: key có trong `config.js`; cách gọi (REST `generativelanguage` hay SDK) có thể nằm ở đoạn khác trong bundle — **vẫn là client-side nếu dùng key đó trên trình duyệt**.

---

## 5. Supabase — bảng liên quan AI (client)

Trong code có tham chiếu `pt.from("ai_usage")` (đếm usage theo ngày), cùng các bảng khác đã liệt kê ở tài liệu thư viện.

---

## 6. Khuyến nghị cho chủ hệ thống (nếu bạn vận hành EzLuyenThi)

1. **Gỡ ngay** Groq / Gemini key khỏi `config.js`; xoay key trên Groq Cloud & Google Cloud Console.
2. Chỉ gọi Groq/Gemini từ **server** (Edge Functions, API route), kèm **auth user**, rate limit, logging.
3. Kiểm tra có đoạn nào còn `fetch("https://api.groq.com/...")` từ client — **xóa** và thay bằng gọi `/api/v1/...` proxy.
4. Rà soát RLS Supabase cho bảng `ai_usage`, `profiles`, v.v.

---

## 7. Công cụ trong repo

Chạy sau khi tải bundle JS vào file (hoặc để script tự tải):

```bash
python scripts/probe_ez_ai_security.py "%TEMP%\ez_ai_bundle.js"
```

Script liệt kê path `/api/v1/...` và URL ngoài liên quan AI.

---

*Tài liệu phục vụ đánh giá kỹ thuật & hardening; không khuyến khích lạm dụng API hoặc key lộ ra ngoài.*
