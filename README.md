# Retirement Accounts, Plain English

A friendly, plain-English explainer of 401(k)s, IRAs, Roth vs. Traditional, employer match and vesting, rollovers, and target-date funds — written for people who nodded along in HR meetings and didn't actually understand a word.

**Education only.** This is not financial advice, and it never recommends any specific product, fund, or company. Contribution limits and rules change every year — verify current numbers at [IRS.gov](https://www.irs.gov/retirement-plans) before acting.

## What's in the repo

- `docs/` — the guide itself, in Markdown (10 pages: start here, 401(k) basics, match & vesting, Roth vs. Traditional, IRAs, rollovers, target-date funds, first steps, glossary, one-page worksheet).
- `site/` — a static HTML version of the same guide, generated from `docs/` by `build.py`. System fonts only, no JavaScript, no tracking, no external assets.
- `build.py` — regenerates `site/` from `docs/` using pandoc.
- `verify.py` — builds the site and checks every internal link and anchor, so a broken doc fails loudly.

## How to run it

You need [pandoc](https://pandoc.org/installing.html) and Python 3.10+.

```sh
python3 build.py     # regenerate site/*.html from docs/*.md
python3 verify.py    # rebuild + link/anchor check; exits non-zero on problems
```

To read locally, either open `site/index.html` directly in a browser, or serve it:

```sh
python3 -m http.server 8000 --directory site
# then visit http://localhost:8000
```

To edit the guide: change files in `docs/`, then rerun `build.py`. The HTML is fully regenerable from the markdown; the template and stylesheet live in `site/template.html` and `site/style.css`.

## Design principles

- Plain English, warmed up. Each idea explained once, like a friend would, never condescending.
- Education only — no product picks, no fund names pitched, no "just call my sponsor" nonsense.
- Checks its own links: `verify.py` fails if a page points anywhere that doesn't exist.
- Local-first and quiet: system fonts, one stylesheet, zero scripts, zero analytics, zero ads.
- Accessible default contrast, print-friendly worksheet page (print your browser view and fill it in with a pen).

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.

Part of Asdale Dynamics, LLC's plain-English education series: beginner-friendly guides and tools, written like a friend would.
