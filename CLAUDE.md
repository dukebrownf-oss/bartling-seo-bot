# CLAUDE.md — Bartling Lending SEO Bot (Page Scan & Fix)

> Claude Code reads this file automatically at the start of every session.
> These are non-negotiable rules for every page in this project.
> **When any request or page conflicts with a rule below, STOP and flag it — never "fix" it silently.**
> Last updated: June 2026 (Texas-only pivot).

---

## 0. What this project does

You (Claude Code) scan the HTML source for each Bartling Lending web page **one page at a time**,
detect anything that violates the rules below, fix it **surgically** (smallest edit that resolves
the issue — do not rewrite working layout/schema), QC the result until clean, drop the corrected
file into the output folder (Adam's Google Drive), write a short per-page report, then **STOP and
wait for Adam's go-ahead before the next page.** See **§10 Workflow**.

You also produce, per page, a short **SEO/UX suggestions** section for improvements we have **not**
already made — only where genuinely relevant (see `SEO_REVIEW_RUBRIC.md`).

Business context: Bartling Lending is a **veteran-owned, 100% mortgage-broker** brokerage. Owner/LO
is **Adam Bartling, NMLS# 2213358**, a retired Army Captain, sponsored by Texas Lending Pro, Inc.
NMLS# 2322982. Canonical domain: **bartlinglending.com**.

---

## 1. Brand & identity

- **Working brand name = "Adam Bartling & Team"** — this matches the live site and every page Adam
  has deployed. Use it in page titles, schema `name`, the author bio, and the footer line.
  - ⚠️ **OPEN DECISION:** an earlier note proposed switching structural brand to **"Bartling Lending"**
    (with "Adam and his team" as the body voice). This is **NOT yet confirmed.** **Do NOT mass-rewrite
    brand names.** Leave each page's existing brand string as-is and report which one it uses. If Adam
    confirms the switch, change this line and re-run.
- **Legal entity** (Bartling Lending Partners LLC): legal/footer context only — keep OUT of marketing copy.
- **Sponsor** (Texas Lending Pro, Inc. NMLS# 2322982): disclose ONLY on `/contact-us/` + the global
  theme footer — never in page body.
- **Per-page footer line** (bottom of every page only):
  `Adam Bartling & Team · Loan Officer NMLS# 2213358 · Serving Texas · Equal Housing Lender`
- Positioning is **100% mortgage broker**: "we shop multiple lenders, they compete for your business,
  we work for you, not a bank." **Never** "direct lender" / "direct lending."

---

## 2. Forbidden content (absolute — hard QC failures)

These are auto-flagged by `scripts/qc_scan.py`. Fix every one found in **rendered body** (HTML
comments are exempt — they may describe what was removed).

| # | Forbidden | Replace with / action |
|---|-----------|----------------------|
| 1 | "Movement Mortgage" (or `movement.com`) anywhere | remove entirely |
| 2 | `bartlinglending.net` | `bartlinglending.com` |
| 3 | "direct lender" / "direct lending" | broker language ("independent mortgage broker", "we shop multiple lenders") |
| 4 | "30+ States" / "30 states" / "Texas & 30+ States" / "Texas and 30+ states" | "Serving Texas" / "Serving All of Texas" |
| 5 | "40+ States" anywhere | "Serving Texas" / "Serving All of Texas" |
| 6 | "Non-QM" | "DSCR Loans" or "Investor Loans" |
| 7 | "ITIN" (not offered) | remove |
| 8 | "Apply Now" in page **body** (header/footer only) | "LET'S TALK" → `/contact-us/` |
| 9 | Phone number or email address in page **body** | remove (lives in header/footer/contact page) |
| 10 | Inline event handlers (`onclick`, `oninput`, `onchange`, …) | `addEventListener` + `data-*` |
| 11 | `&&` inside any `<script>` | nested `if`/`while` (WordPress encodes `&&` → `&#038;`) |
| 12 | `<style>` blocks | 100% inline CSS |
| 13 | Plural "loans" in a URL **slug** | singular (`fha-loan-texas`, not `fha-loans-texas`) |
| 14 | Stale 2025 FHA floor `$524,225` / `$524K` | 2026 floor **`$541,287` / `$541K`** (see §4) |

> **NOTE — these are NOT forbidden (the pivot changed this):** Fix & Flip, Hard Money, and Commercial
> **ARE offered** (Adam confirmed June 2026). Keep their pages live. Do not flag or remove them.

---

## 3. Business scope & licensing — MARKETING IS 100% TEXAS-ONLY

- **Every page reads "Serving Texas" / "Serving All of Texas."** Never "Texas & 30+ States",
  "30+ states", or "40+ states" — on **any** page, including DSCR, construction, and commercial.
  (Adam is *licensed* in ~30 states for DSCR/Investor, Residential Construction, and Commercial as a
  capability, but this is **not marketed** and must not appear in copy.)
- Schema `areaServed` = Texas only. Remove any `{"@type":"Country","name":"United States"}` node.
- Products offered (build/keep pages, market Texas-only): Conventional, FHA, VA, VA IRRRL,
  VA Construction, Reverse, First-Time Homebuyer, HELOC/Home Equity, Refinance, Cash-Out,
  Bank Statement, DSCR/Investor, Residential Construction, **Commercial, Fix & Flip / Hard Money**.

---

## 4. Compliance & factual rules

- **Texas Section 50(a)(6):** VA and FHA cash-out refinance are **PROHIBITED on Texas homesteads** —
  conventional cash-out only. Treat as a competitive differentiator; apply on relevant pages.
- **VA cash-out is NOT available in Texas** under 50(a)(6).
- **TX construction loans: 4–5 draws only (never 5–7).** Texas does not require state-level GC
  licensing — lender approval + insurance instead.
- **Fort Hood:** Fort Cavazos reverted to Fort Hood (June 2025). Use "Fort Hood"; preserve historical
  naming context for SEO.
- **2026 loan limits (verified June 2026):**
  - FHA **floor** (most TX counties): **$541,287** (this replaced 2025's $524,225).
  - Conforming (conventional, statewide TX): **$832,750**.
  - FHA high-cost metros vary by county and **sources conflict** — Austin/Travis commonly cited at
    **$571,550**, and some lenders place Travis/Dallas/Collin/Denton/Harris at **$563,500**. **Do not
    assert a specific high-cost county figure as fact without confirming against HUD's official lookup**
    (`entp.hud.gov/idapp/html/hicostlook.cfm`). Use the $541,287 floor as the safe baseline and flag.
- **Never invent a number.** If a factual/rate/limit claim is time-sensitive or you're unsure, web-search
  to confirm before changing it, and note the source in the page report.

---

## 5. Per-page requirements checklist

- Exactly **3 "LET'S TALK" CTAs**, each linking to `https://bartlinglending.com/contact-us/` only.
  (Inline text links like "Ask us anything →" to `/contact-us/` are allowed and don't count as the 3.)
- Minimum **8 FAQ `<details>` elements**, collapsed by default, gold `+` indicator, native
  `<details>/<summary>` — and the **FAQPage schema question count MUST equal the visible `<details>` count.**
- **Single `@graph` JSON-LD block** that parses cleanly. Nodes: WebPage, FinancialService, Person
  (Adam: knowsAbout / hasOccupation / alumniOf: US Army / sameAs: NMLS + LinkedIn), MortgageLoan per
  product, BreadcrumbList (`item` = **object** with `@id`+`name`, never a bare string), FAQPage, HowTo,
  ImageObject (hero). Link nodes via `@id` refs.
- **Hero image:** `loading="eager"` `fetchpriority="high"` + explicit width/height + descriptive alt.
- **Below-fold images:** `loading="lazy"` + width/height + descriptive alt.
- **Yoast Quick Reference** comment at top: slug, title, meta, focus keyphrase, canonical.
- **Cornerstones: 2,500+ words.**
- One H1, proper H1 > H2 > H3 hierarchy.
- Per-page NMLS footer line (see §1).
- **All CSS 100% inline.** No `<style>` blocks. No `&&` in scripts. No inline `on*` handlers.

## 6. AEO requirements (every cornerstone / hub / city page)

1. Above-fold definition paragraph (~50 words). 2. Comparison table. 3. FAQPage schema.
4. Numbered step lists. 5. "Key Takeaways" bullet block near top. 6. Question-phrased H2s.

## 7. Internal-link whitelist (body content only)

Link **only** to these slugs from body copy:
`/va-home-loan-texas/`, `/fha-loan-texas/`, `/conventional-mortgage-loan-texas/`,
`/first-time-homebuyer-texas/`, `/residential-construction-loan-texas/`, `/va-construction-loan-texas/`,
`/cash-out-refinance-mortgage-texas/`, `/refinance-home-loan-texas/`, `/home-equity-loan-texas/`,
`/dscr-loan-texas/`, `/bank-statement-loan-texas/`, `/reverse-mortgage-texas/`, `/contact-us/`.
Also acceptable: `/about-us/` (author E-E-A-T), `/learning-center/` and its `/category/{x}/` archives.
Blog posts: `/blog/{slug}/` (never `/learning-center/{slug}/`). City pages: `/{loan-type}-{city}-tx/`
with **singular** loan-type prefixes.

## 8. Design system

Navy `#1E3A5F` · Navy-dark `#0F2744` · Gold `#C9A227` · Gold-hover `#E0B82E` · Cream `#FAF9F6` ·
Text `#2C3E50` · Muted `#5A6C7D`. Headings **Merriweather** (700/900); body **Open Sans** (400/600/700).
Fonts via `<link rel="preload">` only (never `@import`); preconnect googleapis + gstatic.
Max-width 900px centered. Hero overlay ~67% `rgba(15,39,68,0.67)`.

## 9. Images — verify before trusting

- **Never guess a filename.** Before using/keeping any image URL, confirm HTTP 200 with
  `scripts/verify_links_images.py` (it `curl`s each URL). A "confirmed-live" memory is not enough —
  files do 404 (e.g., `parents-children-relax-sofa-scaled.jpg` was dead despite being listed live).
- Confirmed-live (re-verify anyway): `/2025/11/Adam-LO-with-Army.png`,
  `/2025/11/happy-multiracial-family-diverse-parents-playing-with-son-cozy-kitchen-weekend-day-home-scaled.jpg`,
  `/2026/01/kid-playing-with-paper-plane-scaled.jpg`, `/2026/01/people-recording-their-house-tour-scaled.jpg`,
  `/2026/01/premium-quality-images-construction-site-scaled.jpg`,
  `/2026/01/modern-home-construction-with-gypsum-plaster-walls-building-industry-scaled.jpg`.

---

## 10. THE WORKFLOW (one page at a time)

For each row in `worklist.csv` with `status = pending`, in `order`:

1. **Load the source.** If `source_file` exists in `pages/`, read it. If not, `web_fetch` the
   `live_url`, extract the editable content block (the page body between the theme header/footer —
   i.e., the WPCode/Custom-HTML content, NOT the Astra theme chrome), and save it to `pages/<slug>.html`.
   **Never edit theme header/footer** — those are global and out of scope.
2. **Scan:** run `python scripts/qc_scan.py pages/<slug>.html`. This prints categorized FAIL/WARN
   findings with line numbers.
3. **Decide:** if 0 FAIL and nothing material → mark `no-change` and still write the SEO suggestions
   report (§11). If FAILs exist → fix them **surgically** (smallest edit; preserve layout & schema).
   - For loan-limit / rate / date-sensitive facts: **web-search to confirm** before editing (§4).
   - For brand name and high-cost county figures: **report, do not auto-change** (open decisions).
4. **Re-scan** until `qc_scan.py` exits clean (0 FAIL). Then run
   `python scripts/verify_links_images.py pages/<slug>.html` and fix/flag any non-200 image or link.
5. **Write the corrected file** to `OUTPUT_DIR/<slug>.html` (see §12 — this is Adam's Google Drive).
   Bump the changelog comment at the top (`v{n}` + what changed + date).
6. **Write the report** `reports/<slug>.md` using the template in `SEO_REVIEW_RUBRIC.md`:
   what was fixed, what passed, and NEW SEO/UX suggestions.
7. **Update `worklist.csv`:** set `status = done`, add a one-line note.
8. **STOP.** Print a 4–6 line summary (page, fixes made, suggestions count, file dropped to Drive)
   and **wait for Adam to say "next" / "go"** before starting the next page.
   - If Adam says "run the whole batch," you may proceed through all `pending` rows without stopping,
     but still write one file + one report per page to Drive as you go, and end with a master summary.

**Cadence rule:** default to ONE page per turn unless Adam explicitly authorizes a batch. Never edit
more than one page's source in a single step without saving + reporting it first.

## 11. SEO / UX suggestions (the "Yoast-style" advisory)

Per page, after compliance is clean, evaluate against `SEO_REVIEW_RUBRIC.md` and list only
**new, relevant** improvements we haven't already made (internal-link gaps, missing AEO blocks,
schema gaps, thin alt text, title/meta tuning, GSC content-gap opportunities, CWV hints). Keep it
to the highest-value items — quality over quantity. Never recommend fee-based "directories."

## 12. Output & Google Drive

- Set `OUTPUT_DIR` (top of `worklist.csv` header comment or an env note) to the folder where corrected
  pages should land. **Recommended:** a **Google Drive for Desktop** synced path so files auto-upload,
  e.g. macOS `~/Library/CloudStorage/GoogleDrive-<you>/My Drive/Bartling-Updated-Pages/` or
  Windows `G:\My Drive\Bartling-Updated-Pages\`.
- Alternative: if the **Google Drive MCP** is connected to Claude Code, upload via that tool instead.
- Each corrected page is a **standalone WPCode/Custom-HTML block** ready to paste back into WordPress.
  (JS-heavy pages — calculators — must go in a **WPCode HTML Snippet**, not a Custom HTML block.)

## 13. Guardrails

- One page at a time; save + report before moving on.
- Surgical edits only — don't refactor working layout or schema you weren't asked to touch.
- Flag (don't silently change): **brand name**, **high-cost county FHA figures**, anything where a rule
  conflicts with the page or where a fact needs verification.
- Don't touch the global theme header/footer.
- Never invent facts, filenames, or attributions. Verify images (200) and time-sensitive numbers (web).
- If a page is one of the **abandoned out-of-state hubs** (California/Florida/Arizona/Colorado/Georgia/
  NC/Tennessee/Virginia mortgage), do **not** update it — it should be **301-redirected** to the
  homepage, not edited. Flag it for the redirect map instead.
