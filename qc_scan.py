#!/usr/bin/env python3
"""
qc_scan.py — Bartling Lending page compliance scanner.

Usage:
    python scripts/qc_scan.py pages/fha-loan-texas.html

Exit code 0 = no hard FAILs. Exit code 1 = one or more FAILs (must fix).
WARNs are advisory (review, may be intentional). All checks ignore HTML comments
for body rules, since changelog comments legitimately describe removed strings.

This is the same sweep Claude ran by hand, encoded once. Re-run after every edit.
"""
import sys, re, json

FAIL, WARN, INFO = "FAIL", "WARN", "INFO"

# Forbidden substrings in RENDERED BODY (case-insensitive). (label, regex)
FORBIDDEN = [
    ("Movement Mortgage",        r"movement\s+mortgage|movement\.com"),
    (".net domain",              r"bartlinglending\.net"),
    ("'direct lender/lending'",  r"direct\s+lend(er|ing)"),
    ("'30+ States' language",    r"30\s*\+?\s*states|texas\s*&(?:amp;)?\s*30|and\s+30\+?\s+states"),
    ("'40+ States' language",    r"40\s*\+?\s*states"),
    ("'Non-QM'",                 r"non-?qm"),
    ("'ITIN'",                   r"\bITIN\b"),
    ("'Apply Now' in body",      r"apply\s+now"),
    ("Stale 2025 FHA limit",     r"524,?225|\$524k"),
]

# Phone / email in body
RE_PHONE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b")
RE_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

WHITELIST = {
    "/", "/contact-us/", "/about-us/",
    "/va-home-loan-texas/", "/fha-loan-texas/", "/conventional-mortgage-loan-texas/",
    "/first-time-homebuyer-texas/", "/residential-construction-loan-texas/",
    "/va-construction-loan-texas/", "/cash-out-refinance-mortgage-texas/",
    "/refinance-home-loan-texas/", "/home-equity-loan-texas/", "/dscr-loan-texas/",
    "/bank-statement-loan-texas/", "/reverse-mortgage-texas/",
}

def strip_comments(s):
    return re.sub(r"<!--.*?-->", "", s, flags=re.DOTALL)

def scripts_only(s):
    return "\n".join(re.findall(r"<script\b[^>]*>(.*?)</script>", s, flags=re.DOTALL | re.I))

def line_of(src, idx):
    return src.count("\n", 0, idx) + 1

def main(path):
    raw = open(path, encoding="utf-8").read()
    body = strip_comments(raw)
    findings = []  # (level, message)

    # ---- forbidden substrings in body ----
    for label, pat in FORBIDDEN:
        for m in re.finditer(pat, body, flags=re.I):
            findings.append((FAIL, f"{label}: '{m.group(0)}' (line ~{line_of(body, m.start())})"))

    # ---- phone / email in body (allow inside JSON-LD identifier/NMLS? no — NMLS is text not phone) ----
    body_no_scripts = re.sub(r"<script\b[^>]*>.*?</script>", "", body, flags=re.DOTALL | re.I)
    for m in RE_PHONE.finditer(body_no_scripts):
        findings.append((FAIL, f"Phone number in body: '{m.group(0)}'"))
    for m in RE_EMAIL.finditer(body_no_scripts):
        findings.append((WARN, f"Possible email in body: '{m.group(0)}' (confirm it's not a schema URL)"))

    # ---- inline event handlers ----
    for m in re.finditer(r"\son(click|input|change|load|submit|mouseover)\s*=", body, flags=re.I):
        findings.append((FAIL, f"Inline event handler 'on{m.group(1)}=' (line ~{line_of(body, m.start())}) — use addEventListener"))

    # ---- && inside <script> ----
    js = scripts_only(raw)
    # exclude JSON-LD blocks from the && check (JSON can't contain &&; this catches real JS)
    real_js = "\n".join(
        b for b in re.findall(r"<script\b(?![^>]*ld\+json)[^>]*>(.*?)</script>", raw, flags=re.DOTALL | re.I)
    )
    if "&&" in real_js:
        findings.append((FAIL, "'&&' found inside a <script> — WordPress encodes it to &#038;; use nested if/while"))

    # ---- <style> blocks ----
    if re.search(r"<style\b", body, flags=re.I):
        findings.append((FAIL, "<style> block present — all CSS must be inline"))

    # ---- CTA count (LET'S TALK buttons → /contact-us/), comments excluded ----
    lets_talk = len(re.findall(r"LET'S TALK", body))
    if lets_talk != 3:
        findings.append((FAIL, f"LET'S TALK CTA count = {lets_talk} (must be exactly 3)"))
    contact_links = re.findall(r'href="https://bartlinglending\.com/contact-us/"', body)
    if len(contact_links) < 3:
        findings.append((WARN, f"Only {len(contact_links)} link(s) to /contact-us/ — expected at least the 3 CTAs"))

    # ---- FAQ <details> vs FAQPage schema ----
    details = len(re.findall(r"<details\b", body))
    # ---- JSON-LD parse + areaServed + FAQ count ----
    faq_q = None
    area_has_us = False
    for block in re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                            raw, flags=re.DOTALL | re.I):
        try:
            data = json.loads(block)
        except Exception as e:
            findings.append((FAIL, f"JSON-LD does not parse: {e}"))
            continue
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else []
        for n in nodes:
            if not isinstance(n, dict):
                continue
            if n.get("@type") == "FAQPage":
                faq_q = len(n.get("mainEntity", []))
            area = n.get("areaServed")
            if area:
                txt = json.dumps(area)
                if "United States" in txt or "Country" in txt:
                    area_has_us = True
    if details < 8:
        findings.append((WARN, f"Only {details} FAQ <details> (minimum 8 for cornerstone/hub/city)"))
    if faq_q is not None and faq_q != details:
        findings.append((FAIL, f"FAQ mismatch: {details} <details> vs {faq_q} FAQPage schema questions"))
    if area_has_us:
        findings.append((FAIL, "schema areaServed includes United States/Country — must be Texas only"))

    # ---- construction draws ----
    if re.search(r"5\s*[–-]\s*7\s*draw", body, flags=re.I) or re.search(r"5\s+to\s+7\s+draw", body, flags=re.I):
        findings.append((FAIL, "Construction draws stated as 5–7 — Texas rule is 4–5"))

    # ---- internal links not on whitelist ----
    for m in re.finditer(r'href="https://bartlinglending\.com(/[^"]*)"', body):
        path_only = m.group(1)
        base = re.sub(r"#.*$", "", path_only)
        if base in WHITELIST:
            continue
        if base.startswith("/blog/") or base.startswith("/learning-center/"):
            continue
        if re.match(r"^/[a-z0-9-]+-[a-z-]+-tx/$", base):  # city page pattern /{loan}-{city}-tx/
            continue
        findings.append((WARN, f"Internal link not on whitelist: {path_only}"))

    # ---- hero image attrs (first <img>) ----
    imgs = re.findall(r"<img\b[^>]*>", body, flags=re.I)
    if imgs:
        hero = imgs[0]
        for attr in ("loading=\"eager\"", "fetchpriority=\"high\"", "width=", "height=", "alt="):
            if attr not in hero:
                findings.append((WARN, f"Hero <img> missing {attr.rstrip('=\"')}"))
        for img in imgs[1:]:
            if "alt=" not in img:
                findings.append((WARN, "Below-fold <img> missing alt text"))
            if 'loading="lazy"' not in img and 'loading="eager"' not in img:
                findings.append((WARN, "Below-fold <img> missing loading attribute"))
    else:
        # background-image heroes are allowed; just inform
        findings.append((INFO, "No <img> hero found (CSS background hero is acceptable; ensure it's preloaded)"))

    # ---- footer line ----
    if "NMLS# 2213358" not in body:
        findings.append((WARN, "NMLS# 2213358 footer line not found"))
    if "Serving Texas" not in body and "Serving All of Texas" not in body:
        findings.append((WARN, "No 'Serving Texas' / 'Serving All of Texas' line found"))

    # ---- word count (rough) ----
    text = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", body, flags=re.DOTALL | re.I))
    words = len(re.sub(r"\s+", " ", text).split())
    if words < 2500:
        findings.append((INFO, f"~{words} words (cornerstones should be 2,500+; OK for shorter page types)"))

    # ---- brand report (do NOT fail) ----
    if "Adam Bartling & Team" in body or "Adam Bartling &amp; Team" in body:
        findings.append((INFO, "Brand string in use: 'Adam Bartling & Team' (working default)"))
    if re.search(r"\bBartling Lending\b(?!\s+Partners)", body):
        findings.append((INFO, "Brand string 'Bartling Lending' also present — confirm intended (open decision)"))

    # ---- report ----
    fails = [f for f in findings if f[0] == FAIL]
    warns = [f for f in findings if f[0] == WARN]
    infos = [f for f in findings if f[0] == INFO]
    print(f"\n=== QC SCAN: {path} ===")
    print(f"~{words} words | {details} FAQ <details>"
          + (f" | {faq_q} schema Qs" if faq_q is not None else " | (no FAQPage schema)"))
    for level, group in ((FAIL, fails), (WARN, warns), (INFO, infos)):
        if group:
            print(f"\n[{level}]  ({len(group)})")
            for _, msg in group:
                print(f"  - {msg}")
    print(f"\nRESULT: {'FAIL' if fails else 'PASS'}  ({len(fails)} fail, {len(warns)} warn)\n")
    return 1 if fails else 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/qc_scan.py <file.html>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
