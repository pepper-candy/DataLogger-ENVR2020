#!/usr/bin/env python3
"""Strip PWA-only bits from index.html into ENVR2020_field_log.html."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text()
html = re.sub(r"\n?<!--PWA-->.*?<!--/PWA-->\n?", "\n", html, flags=re.S)
out = ROOT / "ENVR2020_field_log.html"
out.write_text(html)
print(f"wrote {out} ({out.stat().st_size} bytes)")
