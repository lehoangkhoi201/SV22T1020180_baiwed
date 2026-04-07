"""
Khám phá Supabase PostgREST (chỉ đọc, dùng anon key) — EzLuyenThi hoặc project tương tự.

- Lấy OpenAPI schema (danh sách bảng/endpoint public qua anon + RLS).
- Thử đếm bản ghi (estimate) với bảng bạn chỉ định.
- KHÔNG in full API key; chỉ hiện vài ký tự cuối để nhận biết.

Cách dùng (khuyến nghị — key trong biến môi trường, không dán vào lệnh git):

  set EZ_SUPABASE_URL=https://xxxx.supabase.co
  set EZ_SUPABASE_ANON_KEY=eyJ...
  python ezluyenthi_supabase_explorer.py

Hoặc tự tải config.js (chỉ lấy supabaseUrl + supabaseKey, không lưu file):

  python ezluyenthi_supabase_explorer.py --config-url https://ezluyenthi.id.vn/config.js

Tuỳ chọn kiểm tra key AI (chỉ nếu đã set sẵn trong env — không đọc từ config.js):

  set GROQ_API_KEY=...
  set GEMINI_API_KEY=...
  python ezluyenthi_supabase_explorer.py --test-ai-env

Yêu cầu: pip install requests
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("Cần: pip install requests", file=sys.stderr)
    sys.exit(1)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _mask(s: str, show: int = 4) -> str:
    if not s:
        return "(empty)"
    if len(s) <= show:
        return "***"
    return "***" + s[-show:]


def parse_config_js(text: str) -> tuple[str | None, str | None]:
    url_m = re.search(r"supabaseUrl:\s*\"(https://[^\"]+\.supabase\.co)\"", text)
    key_m = re.search(r"supabaseKey:\s*\"(eyJ[^\"]+)\"", text)
    return (url_m.group(1) if url_m else None, key_m.group(1) if key_m else None)


def fetch_openapi(base: str, anon: str) -> dict[str, Any] | None:
    base = base.rstrip("/")
    url = f"{base}/rest/v1/"
    headers = {
        "apikey": anon,
        "Authorization": f"Bearer {anon}",
        "Accept": "application/openapi+json",
    }
    r = requests.get(url, headers=headers, timeout=60)
    if r.status_code != 200:
        print(f"OpenAPI GET {url} -> {r.status_code}", file=sys.stderr)
        try:
            print(r.text[:500], file=sys.stderr)
        except Exception:
            pass
        return None
    return r.json()


def summarize_openapi(spec: dict[str, Any]) -> None:
    paths = spec.get("paths") or {}
    print("\n=== Bảng / path PostgREST (từ OpenAPI) ===\n")
    rows: list[tuple[str, list[str]]] = []
    for path, methods in sorted(paths.items()):
        if not path.startswith("/"):
            continue
        mkeys = list((methods or {}).keys())
        rows.append((path, mkeys))
    for path, mkeys in rows:
        print(f"  {path:45}  {mkeys}")
    print(f"\nTổng path: {len(paths)}")


def count_table(base: str, anon: str, table: str, limit: int = 1) -> tuple[int | None, str | None]:
    """Trả về (count hoặc None, error)."""
    base = base.rstrip("/")
    # Prefer Prefer: count=exact
    url = f"{base}/rest/v1/{quote(table)}?select=*&limit={limit}"
    headers = {
        "apikey": anon,
        "Authorization": f"Bearer {anon}",
        "Accept": "application/json",
        "Prefer": "count=exact",
    }
    r = requests.get(url, headers=headers, timeout=60)
    err = None if r.ok else f"HTTP {r.status_code}: {r.text[:200]}"
    cnt = r.headers.get("Content-Range")
    # Content-Range: 0-0/2831
    total = None
    if cnt and "/" in cnt:
        try:
            total = int(cnt.split("/")[-1])
        except ValueError:
            pass
    return total, err


def test_groq_key() -> None:
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        print("GROQ_API_KEY: (không set — bỏ qua)")
        return
    r = requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {key}"},
        timeout=30,
    )
    print(f"Groq GET /openai/v1/models -> {r.status_code} (key {_mask(key)})")
    if r.status_code != 200:
        print(r.text[:300])


def test_gemini_key() -> None:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        print("GEMINI_API_KEY: (không set — bỏ qua)")
        return
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    r = requests.get(url, timeout=30)
    print(f"Gemini GET v1beta/models -> {r.status_code} (key {_mask(key)})")
    if r.status_code != 200:
        print(r.text[:300])


def main() -> None:
    ap = argparse.ArgumentParser(description="Supabase PostgREST explorer (anon)")
    ap.add_argument(
        "--config-url",
        help="URL file config.js (chỉ dùng supabaseUrl + supabaseKey)",
    )
    ap.add_argument(
        "--tables",
        nargs="*",
        default=["library_resources"],
        help="Các bảng cần thử đếm (mặc định: library_resources)",
    )
    ap.add_argument(
        "--test-ai-env",
        action="store_true",
        help="Kiểm tra GROQ_API_KEY / GEMINI_API_KEY trong env (không lấy từ web)",
    )
    args = ap.parse_args()

    base = os.environ.get("EZ_SUPABASE_URL", "").strip()
    anon = os.environ.get("EZ_SUPABASE_ANON_KEY", "").strip()

    if args.config_url:
        cr = requests.get(args.config_url, timeout=30)
        cr.raise_for_status()
        u, k = parse_config_js(cr.text)
        if u:
            base = u
        if k:
            anon = k
        print(f"Đã tải config.js: supabaseUrl={base}, supabaseKey={_mask(anon)}")

    if not base or not anon:
        print(
            "Thiếu EZ_SUPABASE_URL / EZ_SUPABASE_ANON_KEY hoặc --config-url không parse được.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Kết nối: {base} | anon {_mask(anon)}")

    spec = fetch_openapi(base, anon)
    if spec:
        summarize_openapi(spec)
        out_path = os.path.join(os.path.dirname(__file__), "..", "docs", "ezluyenthi_openapi_snapshot.json")
        out_path = os.path.normpath(out_path)
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(spec, f, ensure_ascii=False, indent=2)
            print(f"\nĐã ghi OpenAPI (không chứa key) tại: {out_path}")
        except OSError as e:
            print(f"(Không ghi file OpenAPI: {e})", file=sys.stderr)

    print("\n=== Ước lượng số dòng (Prefer: count=exact) ===\n")
    for t in args.tables:
        total, err = count_table(base, anon, t)
        if err:
            print(f"  {t}: lỗi — {err}")
        else:
            print(f"  {t}: ~{total} bản ghi (theo Content-Range)")

    if args.test_ai_env:
        print("\n=== Kiểm tra key AI (env) ===\n")
        test_groq_key()
        test_gemini_key()


if __name__ == "__main__":
    main()
