# EzLuyenThi — Cấu trúc DB (PostgREST), công cụ truy cập & giới hạn

**Site:** [ezluyenthi.id.vn](https://ezluyenthi.id.vn/)

Tài liệu này mô tả những gì có thể biết **hợp pháp** từ bên ngoài (anon key + OpenAPI), và những gì **chỉ chủ dự án** nắm đầy đủ (Supabase Dashboard, service role, backup).

---

## 1. Giới hạn quan trọng

| Yêu cầu | Thực tế |
|--------|---------|
| “Full data” toàn bộ production | **Không** lấy được chỉ với anon key nếu **RLS** chặn — mỗi bảng chỉ đọc được phần policy cho phép. |
| “Full DB” như file `.sql` dump | Chỉ qua **Supabase → SQL Editor / backup** (đăng nhập project). |
| ER diagram đầy đủ FK | OpenAPI PostgREST mô tả bảng & cột; quan hệ khóa ngoại nên xem **Dashboard → Database → Schema** hoặc `information_schema`. |

---

## 2. Kiến trúc đã biết

- **Frontend:** SPA, cấu hình runtime: `/config.js` → `window.__APP_CONFIG__` (Supabase URL, anon key, v.v.).
- **Dữ liệu:** Supabase **PostgREST** `{supabaseUrl}/rest/v1/{table}`.
- **Snapshot OpenAPI** (đã tạo bằng script, không chứa secret): `docs/ezluyenthi_openapi_snapshot.json` (~426 KB, có thể tái tạo bất cứ lúc nào).
- **Schema bảng/cột đọc được** (Markdown, sinh từ OpenAPI): `docs/ezluyenthi_schema_public_from_openapi.md` — chạy `python scripts/ezluyenthi_openapi_to_markdown.py` sau khi cập nhật snapshot.

---

## 3. Thống kê bảng (từ OpenAPI, tháng 3/2026)

PostgREST liệt kê **71 path** gồm bảng `public` và các **RPC**. Một số bảng tiêu biểu:

- **Thư viện / nội dung:** `library_resources`, `blog_posts`, `blog_media`, `questions`, `quiz_questions`, `exams`, `vocabulary_sets`, `words`, …
- **Người dùng / giao dịch:** `profiles`, `wallet_transactions`, `payments`, `subscriptions`, `course_purchases`, `exam_purchases`, …
- **AI / phân tích:** `ai_analysis` (trong OpenAPI); bảng `ai_usage` **không** xuất hiện trong schema cache hiện tại — có thể đổi tên hoặc chỉ dùng phía backend (`usage_tracking` là một bảng tracking khác).
- **Khác:** `battles`, `battle_queue`, `code_battle_*`, `conversations`, `messages`, `notifications`, …

**Ước lượng số dòng (anon, thử nghiệm):**

- `library_resources`: **~2831** (đọc được công khai qua crawl đã mô tả trong `EzLuyenThi-API-ThuVien.md`).
- `profiles`, `wallet_transactions`: **0** với truy vấn anon mẫu — thường là **RLS** (không cho đọc hàng loạt), không nhất thiết là bảng rỗng.

**Mối quan hệ:** Nhiều bảnh có `user_id` → `profiles` (chi tiết cột trong `definitions` của file OpenAPI). Để sơ đồ ER đầy đủ, dùng Supabase **Schema Visualizer** hoặc export DDL trong project của bạn.

---

## 4. Công cụ trong repo: `scripts/ezluyenthi_supabase_explorer.py`

Đọc OpenAPI, in danh sách path, ước lượng `count` cho vài bảng (không in full API key).

```powershell
cd scripts
pip install -r requirements-ezlibrary.txt
python ezluyenthi_supabase_explorer.py --config-url https://ezluyenthi.id.vn/config.js --tables library_resources profiles wallet_transactions
```

Hoặc chỉ dùng biến môi trường (khuyến nghị khi bạn là chủ project):

```powershell
$env:EZ_SUPABASE_URL="https://xxxx.supabase.co"
$env:EZ_SUPABASE_ANON_KEY="eyJ..."
python ezluyenthi_supabase_explorer.py
```

Kiểm tra key AI **từ env máy bạn** (không lấy từ `config.js`):

```powershell
$env:GROQ_API_KEY="..."
$env:GEMINI_API_KEY="..."
python ezluyenthi_supabase_explorer.py --test-ai-env
```

---

## 5. Bảo mật (tóm tắt kiểm tra thụ động)

Chi tiết route AI và rủi ro key client: `docs/EzLuyenThi-AI-BaoMat.md`.

**Phát hiện lặp lại:** `config.js` công khai thường chứa **Groq**, **Gemini** và **Supabase anon**. Anon là thiết kế cho client; **key AI trong JS là sai** — cần **xoay key** và chuyển gọi AI sang backend.

**PostgREST:** Nhiều bảnh xuất hiện trong OpenAPI **không** đồng nghĩa anon có quyền đọc/ghi — **RLS** quyết định từng hàng.

---

## 6. Tài liệu liên quan

- `docs/EzLuyenThi-API-ThuVien.md` — thư viện `library_resources`, crawl JSON.
- `docs/EzLuyenThi-Wallet-ThanhToan.md` — ví / thanh toán.
- `scripts/ezlibrary_crawl.py` — tải metadata thư viện (tuân ToS / bản quyền).

*Tài liệu phục vụ chủ hệ thống, tích hợp hợp pháp và hardening — không khuyến khích truy cập trái phép hoặc vượt quyền.*
