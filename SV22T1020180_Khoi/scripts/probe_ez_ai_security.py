"""Extract /api/v1 paths and AI-related strings from EzLuyenThi JS bundle."""
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(os.environ["TEMP"]) / "ez_ai_bundle.js"
s = path.read_text(encoding="utf-8", errors="ignore")

# Unique /api/v1/... (strict)
apis = sorted(set(re.findall(r'["\'](/api/v1/[a-zA-Z0-9_/-]+)', s)))
print("=== /api/v1/ (strict) ===")
for a in apis:
    print(a)
print("count:", len(apis), "\n")

# Broader template literals
broader = sorted(set(re.findall(r"/api/v1/[a-zA-Z0-9_/`$:-]+", s)))
clean = []
for b in broader:
    b = b.split("${")[0].rstrip("`")
    if b.startswith("/api/v1/") and b not in clean:
        clean.append(b)
print("=== /api/v1/ (broader, dedup) ===")
for a in sorted(set(clean)):
    print(a)
print()

# External AI provider URLs (loose)
ext = sorted(set(re.findall(
    r"https://[a-zA-Z0-9.-]+\.(?:com|io|ai|googleapis\.com)/[a-zA-Z0-9_?&=./-]*",
    s,
)))
ai_ext = [
    u for u in ext
    if any(k in u.lower() for k in (
        "openai", "groq", "googleapis", "generativelanguage", "anthropic",
        "cohere", "mistral", "api.groq",
    ))
]
print("=== External HTTPS (AI-ish, sample) ===")
for u in ai_ext[:60]:
    print(u)
print("total ai-ish urls:", len(ai_ext), "\n")

keywords = (
    "groq", "gemini", "openai", "anthropic", "claude", "ai-learning",
    "dolphin", "completion", "embedding", "chat/completions",
    "generativelanguage", "GradingService",
)
print("=== keyword hit ===")
for kw in keywords:
    print(f"  {kw}: {kw.lower() in s.lower()}")
