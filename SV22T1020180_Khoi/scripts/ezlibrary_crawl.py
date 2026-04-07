"""
Crawl metadata thư viện EzLuyenThi qua Supabase PostgREST (bảng library_resources).

Chạy:  python ezlibrary_crawl.py
Yêu cầu: pip install -r requirements-ezlibrary.txt

Lưu ý: API chỉ trả JSON (tiêu đề, mô tả, link). File PDF/video thường nằm sau link rút gọn / trang ngoài.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import requests

CONFIG_URL = "https://ezluyenthi.id.vn/config.js"
USER_AGENT = "Mozilla/5.0 (compatible; EzLibraryCrawl/1.1; +local-script)"
TIMEOUT = 60
PAGE_SIZE = 500


def load_supabase_from_config(session: requests.Session) -> tuple[str, str]:
    r = session.get(CONFIG_URL, timeout=TIMEOUT)
    r.raise_for_status()
    text = r.text
    url_m = re.search(r'supabaseUrl:\s*"([^"]+)"', text)
    key_m = re.search(r'supabaseKey:\s*"([^"]+)"', text)
    if not url_m or not key_m:
        raise RuntimeError("Không parse được supabaseUrl / supabaseKey từ config.js")
    base = url_m.group(1).rstrip("/")
    return base, key_m.group(1)


def fetch_library_resources(session: requests.Session, base: str, key: str) -> list[dict]:
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
    }
    url = f"{base}/rest/v1/library_resources"
    all_rows: list[dict] = []
    offset = 0
    while True:
        params = {
            "select": "*",
            "order": "created_at.asc",
            "limit": str(PAGE_SIZE),
            "offset": str(offset),
        }
        resp = session.get(url, headers=headers, params=params, timeout=TIMEOUT)
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:500]}")
        batch = resp.json()
        if not isinstance(batch, list):
            raise RuntimeError(f"Response không phải list: {type(batch)}")
        if not batch:
            break
        all_rows.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
    return all_rows


def probe_first_link(session: requests.Session, rows: list[dict]) -> dict | None:
    """Thử HEAD/GET link đầu tiên để xem có phản hồi HTTP không (không đảm bảo file trực tiếp)."""
    for row in rows:
        link = (row.get("link") or "").strip()
        if not link or not link.startswith("http"):
            continue
        try:
            h = session.head(link, allow_redirects=True, timeout=30)
            return {
                "sample_link": link,
                "final_url": h.url,
                "status": h.status_code,
                "content_type": h.headers.get("Content-Type", ""),
            }
        except requests.RequestException:
            try:
                g = session.get(link, allow_redirects=True, timeout=30, stream=True)
                g.close()
                return {
                    "sample_link": link,
                    "final_url": g.url,
                    "status": g.status_code,
                    "content_type": g.headers.get("Content-Type", ""),
                }
            except requests.RequestException as e:
                return {"sample_link": link, "error": str(e)}
    return None


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    out_dir = Path(__file__).resolve().parent.parent / "docs"
    out_json = out_dir / "ezlibrary_crawl_output.json"
    out_meta = out_dir / "ezlibrary_crawl_meta.json"

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    print("Loading config.js ...")
    base, key = load_supabase_from_config(session)
    print(f"  supabaseUrl: {base}")

    print("GET /rest/v1/library_resources ...")
    rows = fetch_library_resources(session, base, key)
    print(f"  OK: {len(rows)} rows")

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Wrote: {out_json}")

    print("Probing first external link (HEAD/GET) ...")
    probe = probe_first_link(session, rows)
    meta = {
        "count": len(rows),
        "output_file": str(out_json.name),
        "link_probe": probe,
    }
    with open(out_meta, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"Wrote: {out_meta}")
    if probe:
        print(f"  probe: {json.dumps(probe, ensure_ascii=False)}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)
