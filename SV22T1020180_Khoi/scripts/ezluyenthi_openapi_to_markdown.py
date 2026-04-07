"""
Đọc OpenAPI PostgREST (Swagger 2.0) và xuất markdown: bảng, cột, kiểu, PK/FK (theo mô tả PostgREST).

Nguồn mặc định: docs/ezluyenthi_openapi_snapshot.json
Tạo lại snapshot: python ezluyenthi_supabase_explorer.py --config-url https://ezluyenthi.id.vn/config.js

Chạy:
  python ezluyenthi_openapi_to_markdown.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SPEC = ROOT / "docs" / "ezluyenthi_openapi_snapshot.json"
OUT_MD = ROOT / "docs" / "ezluyenthi_schema_public_from_openapi.md"


def _fk_from_desc(desc: str | None) -> str | None:
    if not desc:
        return None
    m = re.search(r"Foreign Key to `([^`]+)`", desc)
    if m:
        return m.group(1)
    m2 = re.search(r"<fk table='([^']+)' column='([^']+)'", desc)
    if m2:
        return f"{m2.group(1)}.{m2.group(2)}"
    return None


def _is_pk(desc: str | None) -> bool:
    return bool(desc and "<pk/>" in desc)


def main() -> int:
    spec_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SPEC
    if not spec_path.is_file():
        print(f"Không thấy file: {spec_path}", file=sys.stderr)
        return 1

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    defs = spec.get("definitions") or {}
    title = (spec.get("info") or {}).get("title", "")

    lines: list[str] = [
        "# EzLuyenThi — Schema `public` (từ PostgREST OpenAPI)",
        "",
        f"Nguồn: `{spec_path.name}` — `{title}`.",
        "",
        "Đây là **cấu trúc bảng/cột** mà PostgREST công khai qua **anon key** (giống client).",
        "**Không** gồm: policy RLS, trigger, view không expose, index, quyền chi tiết — xem thêm trong Supabase SQL Editor nếu cần.",
        "",
        "---",
        "",
    ]

    for name in sorted(defs.keys()):
        obj = defs[name]
        if not isinstance(obj, dict) or obj.get("type") != "object":
            continue
        props = obj.get("properties") or {}
        required = set(obj.get("required") or [])
        lines.append(f"## `{name}`")
        lines.append("")
        if not props:
            lines.append("*(không có properties)*")
            lines.append("")
            continue
        lines.append("| Cột | Kiểu (JSON Schema) | Bắt buộc | Ghi chú |")
        lines.append("|-----|-------------------|----------|--------|")
        for col in sorted(props.keys()):
            p = props[col] or {}
            fmt = p.get("format") or ""
            typ = p.get("type") or ""
            desc = p.get("description") or ""
            if typ and fmt:
                combo = f"`{typ}` / `{fmt}`"
            elif fmt:
                combo = f"`{fmt}`"
            elif typ:
                combo = f"`{typ}`"
            else:
                combo = "`—`"
            req = "có" if col in required else ""
            notes: list[str] = []
            if _is_pk(desc):
                notes.append("PK")
            fk = _fk_from_desc(desc)
            if fk:
                notes.append(f"FK → `{fk}`")
            if p.get("default") is not None:
                notes.append(f"default: `{p.get('default')}`")
            note_s = "; ".join(notes) if notes else ""
            lines.append(f"| `{col}` | {combo} | {req} | {note_s} |")
        lines.append("")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MD} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
