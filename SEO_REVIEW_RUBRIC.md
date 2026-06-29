# SEO_REVIEW_RUBRIC.md — Yoast-style advisory for each page

After a page passes compliance (`qc_scan.py` = PASS), evaluate it against the checklist below and
write **only the high-value, *new* suggestions** — things we have NOT already done — into
`reports/<slug>.md`. Quality over quantity: 3–8 strong recommendations beat 30 trivial ones.
Never recommend fee-based directories or anything that violates the rules in CLAUDE.md.

---

## What to evaluate

**1. Title & meta (the Yoast core)**
- Title tag ≤ ~60 chars, leads with the focus keyphrase, includes "Texas," ends with brand.
- Meta description ≤ ~155 chars, contains the keyphrase + a concrete hook (rate/term/CTA) + "Texas."
- Focus keyphrase appears in: H1, first 100 words, at least one H2, the meta, the slug, one alt text.
- Slug is clean, singular ("…-loan-texas"), matches the canonical.

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

**4. AEO / answer-engine readiness (cornerstone/hub/city)**
- Above-fold ~50-word definition paragraph present?
- "Key Takeaways" bullet block near the top?
- Comparison table present and genuinely useful?
- Numbered step list (HowTo) present?
- FAQ: 8+ Q&A, question-phrased, schema count = visible count.

**5. Schema completeness**
- Single `@graph`, parses clean. Nodes present: WebPage, FinancialService, Person, MortgageLoan,
  BreadcrumbList (item objects), FAQPage, HowTo, ImageObject(hero).
- Person node has knowsAbout / hasOccupation / alumniOf (US Army) / sameAs (NMLS + LinkedIn).
- areaServed = Texas only. BreadcrumbList items are objects with @id+name.
- Note any missing node as a suggestion (e.g., "add HowTo schema for the existing step list").

**6. Images & media**
- Hero: eager + fetchpriority="high" + width/height + keyphrase-bearing alt.
- Below-fold: lazy + width/height + descriptive alt (note thin/duplicate alt text).
- All image URLs return 200 (verify_links_images.py).
- Suggest a relevant image where a long text section has none (engagement + alt-text keyword real estate).

**7. Core Web Vitals / performance hints**
- Hero preloaded in the WPCode head block; fonts preloaded (no @import).
- Explicit width/height on all images (prevents CLS).
- No render-blocking inline `<style>`/`<script>` beyond what's required.

**8. Content depth & GSC opportunities**
- Cornerstone ≥ 2,500 words; note thin sections.
- Cross-reference Search Console opportunities where known (e.g., "VA-approved builders Texas" ~800
  impressions with nothing built; Killeen/Fort Hood; Houston suburbs Katy/Sugar Land/The Woodlands).
  Suggest a section or internal link that captures an existing impression cluster.
- Texas-authority angles competitors miss: 50(a)(6) homestead rules, homestead exemption + property
  tax, Texas Veterans Land Board (VLB), TDHCA/TSAHC DPA, MUD districts.

**9. E-E-A-T & trust**
- Author bio with Adam's veteran credentials + NMLS, links to /about-us/.
- Real testimonials with Review schema where appropriate.
- Broker positioning consistent ("we work for you, not a bank").

**10. CTA & UX**
- Exactly 3 LET'S TALK CTAs (above fold, mid, end) → /contact-us/.
- Mobile: tap targets ≥ ~44px, tables scroll, no fixed-width overflow.
- Reading flow: scannable, short paragraphs, gold accents per the design system.

---

## Per-page report template  →  `reports/<slug>.md`

```markdown
# <slug> — page report (<date>)

**Page type:** <cornerstone|hub|city|calculator>   **TX-only marketing:** yes
**File dropped to Drive:** <OUTPUT_DIR>/<slug>.html   **Version:** v<n>

## Compliance (qc_scan)
- RESULT: PASS
- Fixed this pass: <bullet list of edits, or "none — page was already clean">
- Images/links: <all 200 | list any fixed>

## Flagged (decisions for Adam — NOT auto-changed)
- <e.g., brand name string in use, high-cost county FHA figure, possible duplicate page, fact to verify>

## SEO / UX suggestions (new — not yet done)
1. <highest-value first, each with the why + the specific change>
2. ...

## Notes
- <anything Adam should know before pasting back into WordPress>
```
