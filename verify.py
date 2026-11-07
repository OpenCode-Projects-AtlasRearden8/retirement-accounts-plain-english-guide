#!/usr/bin/env python3
"""Verify the guide: rebuild the site, then check structure and every
internal link/anchor. Exits non-zero on any problem.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
EXPECTED_SLUGS = [
    "index",
    "401k-basics",
    "employer-match-and-vesting",
    "roth-vs-traditional",
    "iras",
    "rollovers",
    "target-date-funds",
    "first-steps",
    "glossary",
    "worksheet",
]
REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "build.py",
    "verify.py",
    "site/template.html",
    "site/style.css",
    "site/index.html",
]


def run_build() -> bool:
    result = subprocess.run([sys.executable, "build.py"], cwd=ROOT, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return result.returncode == 0


def anchor_ids(html_text: str) -> set[str]:
    return set(re.findall(r'id="([^"]+)"', html_text)) | set(re.findall(r'name="([^"]+)"', html_text))


def check() -> list[str]:
    problems: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            problems.append(f"missing required file: {rel}")

    for slug in EXPECTED_SLUGS:
        if not (SITE / f"{slug}.html").exists():
            problems.append(f"missing generated page: {slug}.html")

    for page in sorted(SITE.glob("*.html")):
        text = page.read_text(encoding="utf-8")

        if '.md"' in text:
            problems.append(f"{page.name}: un-rewritten .md link")

        for ch in text:
            if 0x2E80 <= ord(ch) <= 0x9FFF:  # stray CJK blocks = mojibake
                problems.append(f"{page.name}: stray CJK character {ch!r}")
                break

        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            frag_split = href.split("#", 1)
            target, frag = frag_split[0], (frag_split[1] if len(frag_split) > 1 else None)
            if target and not (SITE / target).exists():
                problems.append(f"{page.name}: broken link -> {href}")
                continue
            if frag:
                doc = SITE / (target or page.name)
                if doc.exists() and frag not in anchor_ids(doc.read_text(encoding="utf-8")):
                    problems.append(f"{page.name}: missing anchor #{frag} in {doc.name}")

        # Navigation must link back home and to a couple of key pages.
        for must_link in ("index.html", "worksheet.html", "glossary.html"):
            if f'href="{must_link}"' not in text:
                problems.append(f"{page.name}: nav missing link to {must_link}")

        # Required messages on every page.
        for needle in ("Education only", "not financial advice", "Asdale Dynamics, LLC"):
            if needle not in text:
                problems.append(f"{page.name}: missing disclaimer text {needle!r}")

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if "Copyright (c) 2026 Asdale Dynamics, LLC" not in license_text:
        problems.append("LICENSE: missing exact copyright line")
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    if "Asdale Dynamics, LLC" not in readme_text:
        problems.append("README.md: missing credit line")

    return problems


def main() -> int:
    ok = run_build()
    if not ok:
        print("VERIFY FAIL: build failed")
        return 1
    problems = check()
    if problems:
        print("VERIFY FAIL:")
        for p in problems:
            print(f"  - {p}")
        return 1
    n = len(list(SITE.glob("*.html")))
    print(f"VERIFY OK: {n} pages, all internal links/anchors resolve, required files present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
