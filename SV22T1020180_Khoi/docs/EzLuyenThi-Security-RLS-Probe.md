# EzLuyenThi — Kiểm tra RLS với anon key (tháng 3/2026)

**Phương pháp:** Gọi PostgREST giống client công khai (lấy `supabaseUrl` + anon key từ `config.js`). **Không** dùng service role. **Không** lưu PII vào repo.

**Script:** `scripts/probe_ez_rls_anon.py`

```bash
cd scripts
pip install requests
python probe_ez_rls_anon.py
```

Kết quả được **ghi file log** (UTF-8), mặc định: `docs/ezluyenthi_rls_probe.log`  
Đổi đường dẫn: `python probe_ez_rls_anon.py --log D:\path\to\probe.log` — chỉ in console: `--no-log-file`

---

## Kết quả tóm tắt

| Bảng / truy vấn | Kết quả với anon | Đánh giá |
|-----------------|------------------|----------|
| `profiles` (bất kỳ, kể cả `role=eq.admin`) | **0 dòng** (`Content-Range: */0`) | Người chưa đăng nhập **không** đọc được profile — **không** lộ danh sách tài khoản admin qua kênh này. |
| `user_sessions`, `payments`, `wallet_transactions` | **0 dòng** | RLS chặn đọc hàng loạt — phù hợp kỳ vọng. |
| `app_settings` | **2 dòng** — key `app_name`, `api_version`, `visibility=public` | Chỉ cấu hình hiển thị công khai; cột `value` đọc được nhưng nội dung là tên app / phiên bản API (không phải secret). **Vẫn nên** đảm bảo sau này không thêm key nhạy cảm vào bảng này với policy cho anon. |

---

## Kết luận cho chủ hệ thống

1. **Tài khoản admin:** Với **anon key**, probe **không** trả về bản ghi `profiles` nào, kể cả khi lọc `role=admin`. Điều này **ủng hộ** việc RLS đang chặn đọc user khi chưa auth (hoặc chỉ cho phép đọc chính mình sau khi đăng nhập — không kiểm tra trong probe này).
2. **Không thay thế audit đầy đủ:** Cần kiểm tra thêm với **JWT user thường** / **JWT admin** trong DevTools, và policy trên từng bảng trong Supabase.
3. **Rủi ro khác** (độc lập RLS): Key AI trong `config.js` — xem `docs/EzLuyenThi-AI-BaoMat.md`.

*Tài liệu phục vụ hardening; chạy lại script sau khi đổi policy.*
