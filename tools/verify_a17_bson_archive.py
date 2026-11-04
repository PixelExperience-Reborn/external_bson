#!/usr/bin/env python3
"""Host-only inventory of old BSON PE modules; not an Android17 compatibility test."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
top = (root / "Android.bp").read_text(encoding="utf-8")
bp = (root / "src/Android.bp").read_text(encoding="utf-8")
readme = (root / "README").read_text(encoding="utf-8")
checks = {
    "legacy root Soong subdirs": 'subdirs = [' in top and '"*"' in top,
    "shared module libbson": 'cc_library_shared {' in bp and 'name: "libbson"' in bp,
    "historically vendor_available": "vendor_available: true" in bp,
    "C99 compatibility macro": '"-DMONGO_HAVE_STDINT"' in bp,
    "core BSON source": '"bson.c"' in bp,
    "numeric BSON helper source": '"numbers.c"' in bp,
    "network driver excluded from Android module": '"mongo.c"' not in bp,
    "historic alpha MongoDB description": "alpha release" in readme,
    "Apache license present": (root / "APACHE-2.0.txt").is_file(),
}
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
if not all(checks.values()):
    raise SystemExit("BSON archival module assumptions have changed: manual audit required")
print("PASS: archive source inventory only; no Android17 module or product test")
