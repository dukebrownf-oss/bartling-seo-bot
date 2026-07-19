# SEO_REVIEW_RUBRIC.md — Yoast-style advisory for each page
### v2 — July 19, 2026 (matches CLAUDE.md July 2026)

After a page passes compliance (`qc_scan.py` = PASS), evaluate it against the checklist below and
write **only the high-value, *new* suggestions** — things we have NOT already done — into
`reports/<slug>.md`. Quality over quantity: 3–8 strong recommendations beat 30 trivial ones.
Never recommend fee-based directories or anything that violates the rules in CLAUDE.md.

---

## What to evaluate

**1. Title & meta (the Yoast core)**
- Title tag ≤ ~60 chars, leads with the focus keyphrase, includes "Texas," ends with brand
  ("Adam Bartling" or "Adam Bartling | Texas Mortgage Broker" as space allows).
- Meta description ≤ ~155 chars, contains the keyphrase + a concrete hook (broker value / CTA) +
  "Texas." **Never a numeric rate figure.**
- Focus keyphrase appears in: H1, first 100 words, at least one H2, the meta, the slug, one alt text.
- Slug is clean, singular ("…-loan-texas"), matches the canonical. Canonical includes the trailing
  slash (slashless manual canonicals split signals — flag any).

**2. Heading structure & keyword coverage**
- Exactly one H1; logical H2 > H3 nesting; no skipped levels.
- H2s phrased as natural questions where it helps AEO ("What is…", "How much…", "Can I…").
- LSI / variation coverage (e.g., for FHA: "down payment assistance," "MIP," "580 credit score,"
  "first-time buyer," county names) — note gaps.

**3. Internal linking (whitelist only — see CLAUDE.md §7)**
- Does the page link OUT to 3–6 relevant whitelisted cornerstones? Flag under-linking.
- Does it link to the pages a reader would naturally want next (e.g., FHA ↔ First-Time ↔ Conventional)?
- For cornerstones: are city/hub pages linking *up* to it? (orphan-prevention — note if you can tell.)
- Anchor text descriptive, not "click here."
- **Never** suggest links to deleted pages (purchase/build, fix-flip/commercial, state hubs).

**4. AEO / answer-engine readiness (cornerstone/hub/city)**
- Above-fold ~50-word definition paragraph present?
- "Key Takeaways" bullet block near the top?
- Comparison table present and genuinely useful?
- Numbered step list (HowTo) present?
- FAQ: 8+ Q&A, question-phrased, schema count = visible count, collapsed by default, gold `+`.
- TDHCA / TSAHC cited by name with outbound links where DPA is relevant (co-citation strategy).

**5. Schema completeness**
- Single `@graph`, parses clean. Nodes present: WebPage, FinancialService
  (**name = "Adam Bartling | Texas Mortgage Broker"** — retired brand names are a hard FAIL),
  Person, MortgageLoan, BreadcrumbList (item objects), FAQPage, HowTo, ImageObject(hero).
- Person node has knowsAbout / hasOccupation / alumniOf (US Army) / sameAs (NMLS + LinkedIn).
- areaServed = Texas only. BreadcrumbList items are objects with @id+name, **all names lowercase**
  (July 2026 rule — visible crumb and Yoast breadcrumbs-title field lowercase too).
- Note any missing node as a suggestion (e.g., "add HowTo schema for the existing step list").

**6. Images & media**
- Hero: eager + fetchpriority="high" + width/height + keyphrase-bearing alt.
- Below-fold: lazy + width/height + descriptive alt (note thin/duplicate alt text).
- All image URLs return 200 (verify_links_images.py; nmlsconsumeraccess.org 403-to-curl exemption).
- Suggest a relevant image where a long text section has none (engagement + alt-text keyword real estate).

**7. Core Web Vitals / performance hints**
- Hero preloaded in the WPCode head block; fonts preloaded (no @import).
- Explicit width/height on all images (prevents CLS).
- No render-blocking inline `<style>`/`<script>` beyond what's required (WPCode-Snippet pages may
  carry their tool's `<style>`/`<script>` — that's by design).

**8. Content depth & GSC opportunities (refreshed July 19, 2026)**
- Cornerstone ≥ 2,500 words; note thin sections.
- Cross-reference current Search Console clusters:
  * **VA construction is the franchise** — ~5,700 impressions/90d; "va construction loan texas" at
    pos ~11 (page 2). Suggest links UP to /va-construction-loan-texas/ from every relevant page.
  * **VA approved builders** — "va approved builders" 749 imp pos ~28 + Cedar Park / Leander /
    Liberty Hill city variants (~560 imp combined, pos 24–32). /va-approved-builders-texas/ is the
    build-out target; suggest supporting links and sections.
  * **FHA construction** — "fha construction loan texas" 115 imp pos ~17.
  * **Residential construction** — 4,000+ imp but pos ~60; needs consolidation + content depth.
  * Military markets: Killeen/Fort Hood, El Paso/Fort Bliss, JBSA; Houston suburbs Katy/Sugar Land.
- Texas-authority angles competitors miss: 50(a)(6) homestead rules, homestead exemption + property
  tax, Texas Veterans Land Board (VLB), TDHCA/TSAHC DPA, MUD districts, barndominium financing
  ("va loan to build a barndominium" is a live GSC query).

**9. E-E-A-T & trust**
- Author bio with Adam's veteran credentials + NMLS, Army photo, links to /about-us/.
- **Verified Google reviews ONLY** (Clifford Joe, Steven Kinne, Kathaleen Megan Ainsworth, Natasha
  Camacho, Bill Cannon, Joseph Rufo, Matthew Dravis, Jarod Oommen, Liliana Paulino). Review text is
  real Google review text, quoted verbatim — never edited, never invented. Omit the section if no
  real text exists. Review + AggregateRating schema where reviews are shown.
- Broker positioning consistent ("we work for you, not a bank").

**10. CTA & UX**
- Exactly 3 LET'S TALK CTAs (above fold, mid, end) → /contact-us/. JS-rendered CTAs (e.g., prequal
  result screen) count toward the 3. "Apply Now" lives ONLY in header/footer/contact-us.
- Mobile: tap targets ≥ ~44px, tables scroll, no fixed-width overflow.
- Reading flow: scannable, short paragraphs, gold accents per the design system.
- No PDFs / downloadable resources — live pages and live calculators only.

---

## Per-page report template  →  `reports/<slug>.md`

```markdown
# <slug> — page report (<date>)

**Page type:** <cornerstone|hub|city|calculator>   **TX-only marketing:** yes
**File dropped to Drive:** <OUTPUT_DIR>/<slug>.html   **Version:** v<n>

## Compliance (qc_scan v2)
- RESULT: PASS
- Fixed this pass: <bullet list of edits, or "none — page was already clean">
- Images/links: <all 200 | list any fixed | nmlsconsumeraccess 403-exempt>

## Flagged (decisions for Adam — NOT auto-changed)
- <e.g., high-cost county FHA figure, blog slug convention, fact to verify>

## SEO / UX suggestions (new — not yet done)
1. <highest-value first, each with the why + the specific change>
2. ...

## Notes
- <anything Adam should know before pasting back into WordPress>
```
