"""Probe Supabase RLS with anon key (public client). No PII printed — counts/status only.

Ghi log UTF-8 (mặc định): docs/ezluyenthi_rls_probe.log

  python probe_ez_rls_anon.py
  python probe_ez_rls_anon.py --log path\\khac.log
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

CONFIG = "https://ezluyenthi.id.vn/config.js"
DEFAULT_LOG = Path(__file__).resolve().parent.parent / "docs" / "ezluyenthi_rls_probe.log"


def main() -> int:
    ap = argparse.ArgumentParser(description="RLS probe EzLuyenThi (anon)")
    ap.add_argument(
        "--log",
        type=Path,
        default=DEFAULT_LOG,
        help=f"File log (mặc định: {DEFAULT_LOG})",
    )
    ap.add_argument("--no-log-file", action="store_true", help="Chỉ in ra console, không ghi file")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    lines: list[str] = []

    def out(s: str = "") -> None:
        lines.append(s)
        print(s)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out(f"# EzLuyenThi RLS probe (anon) — {ts} UTC")
    out()

    r = requests.get(CONFIG, timeout=30)
    r.raise_for_status()
    t = r.text
    u = re.search(r'supabaseUrl:\s*"([^"]+)"', t)
    k = re.search(r'supabaseKey:\s*"(eyJ[^"]+)"', t)
    if not u or not k:
        msg = "Parse config failed"
        print(msg, file=sys.stderr)
        if not args.no_log_file:
            args.log.parent.mkdir(parents=True, exist_ok=True)
            args.log.write_text(msg + "\n", encoding="utf-8")
        return 1
    base = u.group(1).rstrip("/")
    key = k.group(1)
    h = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
        "Prefer": "count=exact",
    }

    def get(path: str, params: dict) -> tuple[int, int | None, str, str]:
        resp = requests.get(f"{base}/rest/v1/{path}", headers=h, params=params, timeout=45)
        cr = resp.headers.get("Content-Range", "")
        body = resp.text[:500]
        try:
            data = resp.json()
        except Exception:
            return resp.status_code, None, cr, body
        if isinstance(data, list):
            return resp.status_code, len(data), cr, ""
        if isinstance(data, dict) and data.get("message"):
            return resp.status_code, None, cr, str(data.get("message", ""))[:200]
        return resp.status_code, None, cr, body[:200]

    cases: list[tuple[str, str, dict]] = [
        ("profiles limit 3 (id, role only)", "profiles", {"select": "id,role", "limit": "3"}),
        ("profiles role=admin", "profiles", {"select": "id,role", "role": "eq.admin", "limit": "20"}),
        ("profiles role=super_admin", "profiles", {"select": "id,role", "role": "eq.super_admin", "limit": "10"}),
        ("app_settings (key, visibility)", "app_settings", {"select": "key,visibility", "limit": "50"}),
        ("user_sessions", "user_sessions", {"select": "id", "limit": "3"}),
        ("payments", "payments", {"select": "id", "limit": "3"}),
        ("wallet_transactions", "wallet_transactions", {"select": "id", "limit": "3"}),
    ]

    out("=== EzLuyenThi RLS probe — anon key (như client công khai) ===")
    out()
    out("Host: " + base.replace("https://", "").split("/")[0])
    out()
    for label, path, params in cases:
        code, n, cr, err = get(path, params)
        out(label)
        out(f"  HTTP {code} | rows: {n} | Content-Range: {cr}")
        if err:
            out(f"  note: {err}")
        out()

    out("app_settings — tên key lộ cho anon (không in value):")
    r2 = requests.get(
        f"{base}/rest/v1/app_settings",
        headers={**h, "Prefer": "count=exact"},
        params={"select": "key,visibility", "limit": "50"},
        timeout=45,
    )
    if r2.status_code == 200 and isinstance(r2.json(), list):
        for row in r2.json():
            out(f"  - key={row.get('key')!r} | visibility={row.get('visibility')!r}")
    else:
        out(f"  (không đọc được: HTTP {r2.status_code})")

    r3 = requests.get(
        f"{base}/rest/v1/app_settings",
        headers=h,
        params={"select": "key,value", "limit": "10"},
        timeout=45,
    )
    out("app_settings — có đọc được cột `value`? (chỉ độ dài chuỗi, không in nội dung):")
    if r3.status_code == 200 and isinstance(r3.json(), list):
        for row in r3.json():
            v = row.get("value")
            ln = len(v) if isinstance(v, str) else "n/a"
            out(f"  - {row.get('key')!r}: value_len={ln}")
    else:
        out(f"  HTTP {r3.status_code}")
    out()

    if not args.no_log_file:
        args.log.parent.mkdir(parents=True, exist_ok=True)
        args.log.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Đã ghi log: {args.log.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
