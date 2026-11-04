#!/usr/bin/env python3
r"""Citation guard — validates that all \citep{} in the paper have matching .bib entries.

CI gate: fails if a citation is missing from references.bib.
"""
import re, sys
from pathlib import Path

PAPER_DIR = Path("paper")
BIB = PAPER_DIR / "references.bib"

if not PAPER_DIR.exists():
    print("No paper found — skipping citation guard.")
    sys.exit(0)

bib = BIB.read_text() if BIB.exists() else ""

cites = set()
for tex_file in sorted(PAPER_DIR.glob("*.tex")):
    text = tex_file.read_text()
    for match in re.findall(r'\\cite[pt]?\{([^}]+)\}', text):
        for key in match.split(","):
            key = key.strip()
            if key:
                cites.add(key)

missing = sorted(c for c in cites if c not in bib)

if missing:
    print(f"❌ {len(missing)} missing citations: {missing}")
    sys.exit(1)
else:
    print(f"✅ All {len(cites)} citations found in references.bib")
