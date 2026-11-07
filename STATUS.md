# STATUS.md — retirement-accounts-plain-english-guide

Last updated: 2026-11-07. Built by Asdale Dynamics, LLC.

## What was built

A beginner-friendly, plain-English education guide to U.S. retirement
accounts — written for people who nodded along in HR meetings. It covers:

- 401(k) basics (what the account actually is, paycheck mechanics)
- employer match and vesting (formulas translated into dollars; cliff vs. graded)
- Roth vs. Traditional (tax now vs. tax later, split-the-difference answer)
- IRAs, opened independently of any job (Roth favored for beginners, with honest income-limit caveats)
- rollovers for old 401(k)s (direct rollover stressed; cash-out math shown as the trap it is)
- target-date funds (how to pick the year label, expense-ratio sanity check)
- a calm, ordered 30-day first-steps checklist
- a one-breath-per-term glossary
- a printable one-page fridge worksheet

Format: 10 Markdown documents in `docs/` + a fully static HTML site in
`site/` generated from them by `build.py` (pandoc, custom template).
System fonts only, one stylesheet, zero JavaScript, zero external loaded
resources, zero tracking/analytics/ads. Distinct scope from
workplace-benefits-decoded-guide (job-offer evaluation) and
quarterly-taxes-calm-guide (self-employment taxes) — this one is about
the retirement accounts themselves, education only, never financial
advice, no product picks (provider names are deliberately not used;
IRS.gov and the reader's own plan documents are the only actionable
sources).

## How to run it

Requirements: pandoc and Python 3.10+ (only for rebuilding; the site
itself is plain static HTML and opens fine without any tooling).

```sh
python3 build.py     # regenerate site/*.html from docs/*.md
python3 verify.py    # rebuild + link/anchor/structure check; exits non-zero on problems
python3 -m http.server 8000 --directory site   # optional: view at http://localhost:8000
```

Or simply open `site/index.html` in a browser.

## Verification results (all passing, run 2026-11-07)

- `python3 verify.py` → `VERIFY OK: 11 html files` — all 10 generated pages plus the template;
  every internal href and #anchor resolves; required disclaimers and credits present on every page;
  LICENSE/README checks pass.
- `python3 - <<EOF` asset scan → every page loads zero external resources
  (no `<script>`, no external CSS/fonts/images/frames). Only outbound text
  hyperlinks exist (IRS.gov, Dept. of Labor, choosealicense.com).
- `python3 -m py_compile build.py verify.py` → clean.
- Served via `python3 -m http.server 8765 --directory site` and curl-checked
  `index.html`, `worksheet.html`, `roth-vs-traditional.html`, `style.css` → all HTTP 200; server shut down afterward.

## Known gaps

- Contribution limits/figures are described generically on purpose; the
  guide points to IRS.gov for current-year numbers rather than baking in
  figures that drift every November. (As of writing: 2026 401(k) elective
  deferral ~$24,500, catch-up 50+ ~$8,000, IRA ~$7,500 — *verify these
  yourself at IRS.gov before relying on them*.)
- Niche mechanics deliberately out of scope: SEPP/72(t), in-plan Roth
  conversions backdoor/mega-backdoor specifics, NUA strategy, state-specific
  creditor protection differences.
- Accessibility is solid-by-default (semantic HTML, one stylesheet,
  readable widths) but no automated a11y audit has been run.
- The worksheet prints well from browser print preview; no separate PDF
  is generated (keeps the toolchain minimal).
- `site/` is committed as generated output so the folder works standalone,
  even without pandoc installed.

## Repo layout

```
docs/     10 markdown pages (the source of truth)
site/     generated static HTML + template.html + style.css
build.py  docs/*.md -> site/*.html (pandoc)
verify.py rebuild + full link/anchor/structure check
README.md includes license + credit and run instructions
LICENSE   MIT, Copyright (c) 2026 Asdale Dynamics, LLC
```
