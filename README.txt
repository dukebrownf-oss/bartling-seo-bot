# Adam Bartling | Texas Mortgage Broker — SEO Bot for Claude Code

A Claude Code project that scans each bartlinglending.com web page **one at a time**, fixes anything
that breaks the brand/compliance/SEO rules, drops the corrected page into your **Google Drive**, and
writes a short report with **new SEO/UX suggestions** — then stops and waits for your go-ahead before
the next page.

> **Rules version: July 19, 2026.** Brand is FINAL ("Adam Bartling | Texas Mortgage Broker").
> Fix & Flip / Hard Money / Commercial are DISCONTINUED. See `CLAUDE.md` for the full rulebook.

---

## Files

| File | What it is |
|------|-----------|
| `CLAUDE.md` | The rulebook + the page-by-page workflow. Claude Code reads this automatically. **This is the brain.** |
| `scripts/qc_scan.py` | Offline compliance scanner (v2, July 2026 rules). `python scripts/qc_scan.py pages/<slug>.html` → PASS/FAIL + line numbers. |
| `scripts/verify_links_images.py` | Curls every image + internal link → flags anything not HTTP 200. **Exemption:** `nmlsconsumeraccess.org` returns 403 to curl (Cloudflare bot protection) but is live — never flag it. |
| `worklist.csv` | The queue: every page, in priority order, with status (pending/done/skip). |
| `SEO_REVIEW_RUBRIC.md` | The "Yoast-style" advisory checklist + the per-page report template. |
| `pages/` | Page source HTML goes here (one file per page). Claude Code fetches any that are missing. |
| `reports/` | Per-page reports land here. |

---

## One-time setup (5 minutes)

1. **Drop this folder into a Claude Code project** (open the folder in Claude Code, or `cd` into it and run `claude`).
2. **Add your page source files** to `pages/` if you have them (e.g., copy your exported WPCode/Custom-HTML
   blocks). Any page you don't have locally, Claude Code will `web_fetch` from the live URL.
3. **Choose where corrected pages land (your Google Drive).** Two options:
   - **Recommended — Google Drive for Desktop:** install it, then set `OUTPUT_DIR` to the synced path, e.g.
     - macOS: `~/Library/CloudStorage/GoogleDrive-you@gmail.com/My Drive/Bartling-Updated-Pages/`
     - Windows: `G:\My Drive\Bartling-Updated-Pages\`
     Files written there auto-upload to Drive. Tell Claude Code this path in your first message.
   - **Or — Google Drive MCP:** connect the Google Drive connector in Claude Code; it can upload directly.
4. **Confirm Python 3** is available (`python3 --version`). No packages needed — standard library only.

---

## How to run it

Paste this as your first message in Claude Code:

> Read `CLAUDE.md` and `worklist.csv`. My Google Drive output folder is:
> `<paste your OUTPUT_DIR here>`.
> Start with the first `pending` page in the worklist. Load its source (fetch the live URL if it's not in
> `pages/`), run `scripts/qc_scan.py`, fix every FAIL surgically, re-scan until clean, run
> `scripts/verify_links_images.py`, write the corrected file to my Drive folder, write the report to
> `reports/`, update the worklist, then **stop and show me a summary before the next page.**

Then just reply **"next"** to advance one page at a time. To run several at once, say
**"run the next 5 without stopping"** or **"run all pending pages"** — it'll still drop one file +
one report per page to Drive as it goes, and finish with a master summary.

---

## What it will and won't do

**Will (auto-fix as hard FAILs):** Movement Mortgage, "direct lender" (outside the footer disclaimer),
"30+ states"/any multi-state claim, **retired brand strings** ("Bartling Lending", "Bartling Lending
Partners", "Adam Bartling & Team" — verbatim customer review text is the sole exemption), **retired
products** (Fix & Flip / Hard Money / Commercial), links to **deleted pages** (/purchase-a-home-texas/,
/build-a-home/, /commercial-long-term-loans/, fix-and-flip, state-mortgage pages), **wrong NAP**
(Katy/Firethorne/1700 Walger/"Roseberg"), stale `$524,225` FHA limit, phone/email in body, "Apply Now"
in body, PDF/downloadable links, numeric rate figures, same-day/24-hour speed claims, `&&` in scripts,
inline handlers, CTA count, FAQ/schema mismatch, non-lowercase breadcrumb schema names,
FinancialService schema name, `areaServed` United States, off-whitelist internal links, dead images,
and the 4–5 draws rule — then write a clean, paste-ready page to Drive plus a suggestions report.

**Won't (it flags these instead of changing them):**
- **High-cost county FHA figures** — sources conflict for 2026; it uses the $541,287 floor as the safe
  baseline and tells you to confirm specific counties against HUD's lookup.
- **Blog slug convention** — live posts use top-level `/blog-{slug}/` while the prior standard said
  `/blog/{slug}/`. Flagged open; the bot reports which convention each page uses and never moves URLs.
- The **global theme header/footer** — out of scope (those are site-wide, not per-page).
- **Deleted pages** (out-of-state hubs, purchase/build, fix-flip/commercial) — never edited or
  recreated; they are 301-redirected.

---

## Notes

- Each output file is a **standalone block ready to paste back into WordPress.** JS-heavy pages
  (calculators, the homepage prequal tool) are **WPCode HTML Snippets** deployed via shortcode (not
  Custom HTML blocks — WordPress strips `<style>`/`<script>` from those). A `<style>` block is
  **allowed** when the page's changelog comment says "WPCode HTML Snippet"; otherwise it's a FAIL.
- The scanner ignores HTML comments, so changelog notes that mention removed strings (e.g. "removed
  '30+ States'") won't trip a false FAIL.
- The 3-CTA rule counts JS-rendered LET'S TALK buttons (e.g., the prequal result screen) toward the 3.
- Re-run `qc_scan.py` after every edit — it's instant and it's the safety net.
