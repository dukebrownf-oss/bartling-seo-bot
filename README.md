# Bartling Lending — SEO Bot for Claude Code

A Claude Code project that scans each Bartling Lending web page **one at a time**, fixes anything that
breaks the brand/compliance/SEO rules, drops the corrected page into your **Google Drive**, and writes
a short report with **new SEO/UX suggestions** — then stops and waits for your go-ahead before the next page.

---

## Files

| File | What it is |
|------|-----------|
| `CLAUDE.md` | The rulebook + the page-by-page workflow. Claude Code reads this automatically. **This is the brain.** |
| `scripts/qc_scan.py` | Offline compliance scanner. `python scripts/qc_scan.py pages/<slug>.html` → PASS/FAIL + line numbers. |
| `scripts/verify_links_images.py` | Curls every image + internal link → flags anything not HTTP 200. |
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

**Will:** detect + fix Movement Mortgage, "direct lender," "30+ states," stale `$524,225` FHA limit,
phone/email in body, `&&` in scripts, `<style>` blocks, inline handlers, CTA count, FAQ/schema mismatch,
`areaServed` United States, off-whitelist internal links, dead images, and the 4–5 draws rule — then
write a clean, paste-ready page to Drive plus a suggestions report.

**Won't (it flags these instead of changing them):**
- **Brand name** — `Adam Bartling & Team` vs `Bartling Lending` is an **open decision**; it leaves the
  existing string alone and reports it. Resolve this once and it can auto-apply going forward.
- **High-cost county FHA figures** — sources conflict for 2026; it uses the $541,287 floor as the safe
  baseline and tells you to confirm specific counties against HUD's lookup.
- The **global theme header/footer** — out of scope (those are site-wide, not per-page).
- **Abandoned out-of-state hubs** (CA/FL/AZ/etc.) — marked `skip`; those get 301-redirected, not edited.

---

## Notes

- Each output file is a **standalone block ready to paste back into WordPress.** Calculator pages are
  **WPCode HTML Snippets** (not Custom HTML blocks — WordPress strips `<style>`/`<script>` from those).
- The scanner ignores HTML comments, so changelog notes that mention removed strings (e.g. "removed
  '30+ States'") won't trip a false FAIL.
- Re-run `qc_scan.py` after every edit — it's instant and it's the safety net.
