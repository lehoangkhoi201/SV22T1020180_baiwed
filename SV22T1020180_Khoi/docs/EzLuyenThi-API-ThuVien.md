# EzLuyenThi — Tài liệu kỹ thuật API & Thư viện (`/library`)

Tài liệu này mô tả cách trang **[EzLuyenThi](https://ezluyenthi.id.vn)** tải dữ liệu và cách gọi API tương đương phía client (PostgREST / Supabase). Dùng cho mục đích tích hợp, nghiên cứu kỹ thuật hoặc debug — **tuân thủ điều khoản dịch vụ và bản quyền** tài liệu.

---

## 1. Kiến trúc tổng quan

| Thành phần | Mô tả |
|------------|--------|
| **Frontend** | SPA (Vite/React), HTML tối giản + `div#root` |
| **Entry** | `https://ezluyenthi.id.vn/library` → cùng shell với toàn site |
| **Bundle JS** | `/assets/index-*.js`, `/assets/vendor-*.js` (tên file có hash, đổi khi build) |
| **Cấu hình runtime** | `/config.js` — gán `window.__APP_CONFIG__` (Supabase URL, anon key, v.v.) |
| **Dữ liệu thư viện** | Bảng **`library_resources`** trên **Supabase** — truy cập qua **PostgREST** (`/rest/v1/...`) |
| **API nội bộ** | Một số tính năng gọi **`/api/v1/...`** trên cùng domain — thường cần **JWT đăng nhập** |

### 1.1. Script crawl có sẵn trong repo (Python + `requests`)

Trong thư mục **`scripts/`**:

| File | Vai trò |
|------|---------|
| `ezlibrary_crawl.py` | Tải `config.js` → lấy URL/key Supabase → gọi `GET .../rest/v1/library_resources` (phân trang `limit`/`offset`) → ghi JSON |
| `requirements-ezlibrary.txt` | Dependency: `requests` |

**Chạy:**

```bash
cd scripts
pip install -r requirements-ezlibrary.txt
python ezlibrary_crawl.py
```

**Kết quả** (mặc định):

- `docs/ezlibrary_crawl_output.json` — toàn bộ bản ghi metadata (tiêu đề, mô tả, `link`, …). Lần chạy thử trên máy dev: **~2831 dòng** (~1,3 MB JSON).
- `docs/ezlibrary_crawl_meta.json` — số lượng bản ghi + **probe** một `link` đầu tiên (HEAD/GET) để kiểm tra HTTP.

**Giới hạn:** API **không** trả nội dung file PDF/video trực tiếp; cột `link` trỏ tới URL ngoài (Google Sheets, link rút gọn, …). Muốn “tải file” phải xử lý từng loại link riêng (và tuân thủ ToS / bản quyền).

---

## 2. Lấy thông tin kết nối (không lưu secret vào Git)

1. Mở trình duyệt → `https://ezluyenthi.id.vn/config.js` (hoặc DevTools → Network → file `config.js`).
2. Trong object `window.__APP_CONFIG__` có:
   - **`supabaseUrl`** — ví dụ dạng `https://<project-ref>.supabase.co`
   - **`supabaseKey`** — **anon (public) key** JWT, dùng cho client

**Lưu ý bảo mật**

- Anon key của Supabase **được thiết kế để lộ trên client**, nhưng quyền thật sự do **Row Level Security (RLS)** trên Supabase quyết định.
- Nếu trong `config.js` còn các key dịch vụ AI (Groq, Gemini, …) thì đó là **lỗi cấu hình nghiêm trọng** — không nên copy vào dự án của bạn; chủ hệ thống nên **xoay key** và chuyển sang biến môi trường phía server.

---

## 3. API thư viện — Supabase PostgREST

### 3.1. URL cơ bản

```
GET {supabaseUrl}/rest/v1/library_resources
```

Thay `{supabaseUrl}` bằng giá trị từ `config.js` (không có dấu `/` thừa ở cuối).

### 3.2. Header bắt buộc

| Header | Giá trị |
|--------|---------|
| `apikey` | `supabaseKey` (anon) |
| `Authorization` | `Bearer {supabaseKey}` |
| `Accept` | `application/json` (khuyến nghị) |

Tuỳ cấu hình schema, đôi khi cần thêm:

- `Accept-Profile: public`
- `Content-Profile: public` (chủ yếu khi POST/PATCH)

### 3.3. Các cột (theo client / phản hồi mẫu)

| Cột | Gợi ý ý nghĩa |
|-----|----------------|
| `id` | UUID |
| `title` | Tiêu đề tài liệu |
| `category` | Nhóm / danh mục (ví dụ `Free 2k8`) |
| `description` | Mô tả ngắn |
| `type` | Loại (`PDF`, `Video/PDF`, …) |
| `featured` | Nổi bật (`true` / `false`) |
| `link` | URL tải/xem (thường là link trung gian) |
| `created_at`, `updated_at` | Timestamp |

Schema có thể thay đổi theo thời gian — nên thử `select=*` hoặc xem OpenAPI của Supabase (nếu được bật).

### 3.4. Tham số truy vấn PostgREST (ví dụ)

PostgREST dùng query string theo [tài liệu Supabase](https://supabase.com/docs/reference/javascript/select):

- Chỉ lấy một số cột:  
  `?select=id,title,category,link,type,featured`
- Lọc:  
  `&category=eq.Free%202k8`  
  `&featured=eq.true`
- Sắp xếp:  
  `&order=created_at.desc`
- Phân trang:  
  `&limit=20&offset=0`

Ví dụ URL đầy đủ (thay `YOUR_PROJECT` và key khi chạy):

```
GET https://YOUR_PROJECT.supabase.co/rest/v1/library_resources?select=*&order=created_at.desc&limit=50
```

---

## 4. Hướng dẫn sử dụng

### 4.1. cURL (Windows PowerShell)

```powershell
$base = "https://<PROJECT_REF>.supabase.co"
$key  = "<SUPABASE_ANON_KEY>"

$headers = @{
  "apikey"        = $key
  "Authorization" = "Bearer $key"
  "Accept"        = "application/json"
}

Invoke-RestMethod -Uri "$base/rest/v1/library_resources?select=*&limit=10" -Headers $headers -Method GET
```

### 4.2. JavaScript (fetch) — ví dụ trong Node 18+ hoặc browser

```javascript
const supabaseUrl = "https://<PROJECT_REF>.supabase.co";
const supabaseAnonKey = "<SUPABASE_ANON_KEY>";

const res = await fetch(
  `${supabaseUrl}/rest/v1/library_resources?select=*&order=created_at.desc&limit=20`,
  {
    headers: {
      apikey: supabaseAnonKey,
      Authorization: `Bearer ${supabaseAnonKey}`,
      Accept: "application/json",
    },
  }
);

if (!res.ok) {
  console.error(await res.text());
  throw new Error(`HTTP ${res.status}`);
}

const rows = await res.json();
console.table(rows);
```

### 4.3. Dùng thư viện `@supabase/supabase-js`

```javascript
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  "https://<PROJECT_REF>.supabase.co",
  "<SUPABASE_ANON_KEY>"
);

const { data, error } = await supabase
  .from("library_resources")
  .select("*")
  .order("created_at", { ascending: false })
  .limit(20);

if (error) throw error;
console.log(data);
```

---

## 5. Các bảng khác xuất hiện trong frontend (tham khảo)

Client còn tham chiếu các bảng (tên có thể dùng với `/rest/v1/<tên_bảng>` nếu RLS cho phép):

`ai_usage`, `commissions`, `contact_requests`, `exam_attempts`, `exam_purchases`, `exams`, `ielts_trials`, `learning_roadmap`, `mentor_applications`, `notifications`, `profiles`, `questions`, `quizzes`, `referrals`, `reviews`, `speaking_sessions`, `srs_cards`, `subscriptions`, `user_login_streaks`, `wallet_transactions`

**Mỗi bảng có thể bị chặn** với anon key tùy chính sách RLS — không giả định đọc được hết.

---

## 6. API same-origin `/api/v1/...`

Trong bundle có gọi kiểu:

- `POST /api/v1/ai-learning/roadmap`
- Header: `Authorization: Bearer <access_token>` — JWT session Supabase sau đăng nhập

Các route này là **backend riêng** của EzLuyenThi; không có trong repo công khai của bạn. Muốn dùng cần:

- Đăng nhập hợp lệ trên site (lấy session),
- Hoặc tài liệu chính thức từ chủ dịch vụ (nếu có).

---

## 7. Xử lý sự cố thường gặp

| Hiện tượng | Hướng xử lý |
|------------|-------------|
| **401 / JWT expired** | Key sai hoặc bảng yêu cầu user đã đăng nhập — kiểm tra RLS. |
| **200 nhưng `[]`** | RLS không cho phép đọc dòng đó với anon; hoặc filter quá chặt. |
| **404 trên `/rest/v1/...`** | Sai `supabaseUrl` hoặc sai tên bảng. |
| **CORS (chỉ browser)** | Gọi từ server-side (Node/cURL) hoặc dùng Supabase client đúng cách. |

---

## 8. Tuân thủ & trách nhiệm

- Chỉ truy cập và sử dụng dữ liệu trong phạm vi **được phép** (ToS, bản quyền, quyền riêng tư).
- Không phát tán lại toàn bộ nội dung thư viện nếu vi phạm bản quyền.
- Không hard-code **service key** (AI, service role Supabase, …) vào mã nguồn hoặc tài liệu công khai.

---

## 9. Tham chiếu nhanh

- Trang thư viện: `https://ezluyenthi.id.vn/library`
- Cấu hình runtime: `https://ezluyenthi.id.vn/config.js`
- Endpoint dữ liệu thư viện: `{supabaseUrl}/rest/v1/library_resources`
- Tài liệu PostgREST: [PostgREST API](https://postgrest.org/en/stable/references/api.html)
- Supabase REST: [Supabase — REST API](https://supabase.com/docs/guides/api)

---

*Tài liệu được soạn theo quan sát kỹ thuật tại thời điểm viết; chủ hệ thống có thể đổi URL, bảng, RLS hoặc cấu trúc bất cứ lúc nào.*
