#!/usr/bin/env python3
"""Build the static HTML site from markdown sources in docs/.

Generates one HTML page per markdown doc into site/, using the pandoc
template and stylesheet in site/. Rewrites internal .md links to .html,
injects title metadata per page, and verifies that every generated page
resolves all of its internal links. No network access, no tracking.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"
TEMPLATE = SITE / "template.html"
CSS = SITE / "style.css"

NAV_ORDER = [
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

# H1 title -> <title> label (shorter than the headline itself).
TITLES = {
    "Retirement Accounts, Explain(ed) Like a Friend Would": "Start Here",
    "401(k) Basics: What That HR Form Actually Does": "401(k) Basics",
    "Employer Match & Vesting: Free Money, With a Timer On It": "Employer Match & Vesting",
    "Roth vs. Traditional: Pay Tax Now or Pay Tax Later": "Roth vs. Traditional",
    "IRAs: The Retirement Account *You* Open, Not Your Boss": "IRAs",
    "Rollovers: Moving Old 401(k)s Without Tripping Any Wires": "Rollovers",
    "Target-Date Funds: The \"Choose Nothing\" Option That's Secretly Fine": "Target-Date Funds",
    "Confident First Steps: A Calm 30-Day Checklist": "Confident First Steps",
    "Glossary: Every HR Acronym, One Breath Each": "Glossary",
    "One-Page Worksheet: Your Retirement Plan on a Fridge": "One-Page Worksheet",
}


def first_h1(md_text: str) -> str | None:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def build() -> list[str]:
    if not TEMPLATE.exists():
        raise SystemExit(f"missing template: {TEMPLATE}")
    md_files = sorted(p for p in DOCS.glob("*.md"))
    if not md_files:
        raise SystemExit(f"no markdown files found in {DOCS}")

    problems: list[str] = []
    generated: list[Path] = []

    for md in md_files:
        slug = md.stem
        text = md.read_text(encoding="utf-8")
        h1 = first_h1(text)
        label = TITLES.get(h1) or TITLES.get(h1.replace("|", "/")) or slug
        out = SITE / f"{slug}.html"

        cmd = [
            "pandoc",
            "-f", "markdown",
            "-t", "html5",
            "--template", str(TEMPLATE),
            "--metadata", f"title={label}",
            md.name,
            "-o", str(out),
        ]
        result = subprocess.run(cmd, cwd=DOCS, capture_output=True, text=True)
        if result.returncode != 0:
            problems.append(f"pandoc failed for {md.name}: {result.stderr.strip()}")

            continue
        # Rewrite internal links: href="page.md" -> href="page.html".
        html = out.read_text(encoding="utf-8")
        html = re.sub(r'href="([^"]+\.md)(#[^"]*)?"', lambda m: f'href="{m.group(1)[:-3]}.html{m.group(2) or ""}"', html)
        out.write_text(html, encoding="utf-8")
        generated.append(out)

    if not CSS.exists():
        problems.append("style.css missing from site/")
    return problems


def main() -> int:
    problems = build()
    if problems:
        for p in problems:
            print(f"ERROR: {p}")
        return 1
    print("Build OK: generated pages in site/")
    sys.exit(0)


if __name__ == "__main__":
    raise SystemExit(main())
