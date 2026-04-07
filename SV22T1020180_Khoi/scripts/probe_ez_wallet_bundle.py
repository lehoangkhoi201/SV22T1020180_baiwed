import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\PC\AppData\Local\Temp\ez_wallet_bundle.js"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    s = f.read()

# /api/v1/...
apis = sorted(set(re.findall(r'["\'](/api/v1/[a-zA-Z0-9_/-]+)', s)))
print("=== /api/v1/ paths (sample) ===")
for x in apis[:100]:
    print(x)
print(f"... total unique: {len(apis)}")

# Broader: any /api/v1/... in quotes (includes backtick)
apis2 = sorted(set(re.findall(r"/api/v1/[a-zA-Z0-9_/`{}$:-]+", s)))
apis2 = [a.split("${")[0].rstrip("/") for a in apis2]
apis2 = sorted(set(apis2))
print("\n=== /api/v1/ (broader, unique prefixes) ===")
for x in apis2[:80]:
    if "wallet" in x or "payment" in x or "subscription" in x or "deposit" in x or "momo" in x or "vnpay" in x or "sepay" in x:
        print(x)

# Other URLs
for pattern, label in [
    (r"https://[a-zA-Z0-9.-]+\.(?:com|vn|io|co)/[a-zA-Z0-9_?&=./-]+", "https URLs"),
]:
    hits = set(re.findall(pattern, s))
    pay = [h for h in hits if any(k in h.lower() for k in ("pay", "momo", "vnpay", "stripe", "sepay", "vietqr", "zalopay", "bank"))]
    if pay:
        print(f"\n=== {label} (payment-ish) ===")
        for h in sorted(pay)[:40]:
            print(h)

keywords = [
    "wallet_transactions",
    "createCheckout",
    "payment",
    "PayOS",
    "Momo",
    "VNPAY",
    "sepay",
    "vietqr",
    "deposit",
    "topUp",
]
print("\n=== keyword presence ===")
for k in keywords:
    print(k, ":", k in s or k.lower() in s.lower())

# Snippets: sepay, momo, wallet API-ish strings (short unique substrings)
print("\n=== unique string samples (quoted paths/urls) ===")
for needle in [
    "sepay",
    "momo",
    "vnpay",
    "wallet",
    "/api/",
    "vietqr",
    "qr.sepay",
]:
    idx = s.lower().find(needle.lower())
    if idx != -1:
        lo = max(0, idx - 80)
        hi = min(len(s), idx + 200)
        snippet = s[lo:hi].replace("\n", " ")
        try:
            print(f"\n--- around {needle!r} ---\n{snippet}")
        except UnicodeEncodeError:
            print(f"\n--- around {needle!r} ---\n{snippet.encode('ascii', 'backslashreplace').decode()}")

# Supabase: .from("wallet
print("\n=== supabase .from( wallet / subscription ===")
for m in re.finditer(r'\.from\("([^"]+)"\)', s):
    t = m.group(1)
    if any(x in t for x in ("wallet", "subscription", "payment", "order", "deposit")):
        print(t)
