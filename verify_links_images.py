#!/usr/bin/env python3
"""
verify_links_images.py — confirm every image URL and internal link in a page returns HTTP 200.

Usage:
    python scripts/verify_links_images.py pages/fha-loan-texas.html

Never trust a filename from memory — files do 404. Run this before finalizing any page.
Requires network access (uses urllib; no external deps).
"""
import sys, re, urllib.request, urllib.error

def head(url, timeout=12):
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "BartlingQC/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        # some servers reject HEAD; retry GET
        if e.code in (403, 405):
            try:
                req2 = urllib.request.Request(url, headers={"User-Agent": "BartlingQC/1.0"})
                with urllib.request.urlopen(req2, timeout=timeout) as r:
                    return r.status
            except Exception as e2:
                return getattr(e2, "code", f"ERR {e2}")
        return e.code
    except Exception as e:
        return f"ERR {e}"

def main(path):
    raw = open(path, encoding="utf-8").read()
    images = set(re.findall(r'(?:src=|url\()["\']?(https://bartlinglending\.com/wp-content/[^"\')\s]+)', raw))
    links = set(re.findall(r'href="(https://bartlinglending\.com/[^"]*?)"', raw))
    links = {re.sub(r"#.*$", "", l) for l in links if "/wp-content/" not in l}

    bad = 0
    print(f"\n=== LINK/IMAGE CHECK: {path} ===")
    print(f"\nIMAGES ({len(images)}):")
    for u in sorted(images):
        s = head(u)
        flag = "" if s == 200 else "   <-- FIX"
        if s != 200:
            bad += 1
        print(f"  {s}  {u}{flag}")
    print(f"\nINTERNAL LINKS ({len(links)}):")
    for u in sorted(links):
        s = head(u)
        flag = "" if s == 200 else "   <-- CHECK"
        if s != 200:
            bad += 1
        print(f"  {s}  {u}{flag}")
    print(f"\nRESULT: {'ALL 200' if bad == 0 else str(bad) + ' non-200 (fix/flag above)'}\n")
    return 1 if bad else 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/verify_links_images.py <file.html>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
