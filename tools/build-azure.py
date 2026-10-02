#!/usr/bin/env python3
"""Build the Azure static-site tree from the Squarespace embeds.

The embeds use Squarespace slugs; Azure uses clean folder-per-URL paths.
Every occurrence of a path is rewritten - hrefs, the DOCS keys the legal
dialog looks up, and the HPLUS_LINKS map - so they stay consistent.
"""
import io, os, re, shutil, sys, html
from html.parser import HTMLParser

SRC = os.path.expanduser("~/Desktop/H+/code/hplus-squarespace-embeds")
OUT = os.path.expanduser("~/Desktop/H+/handover/hplus-therapy-companion")

PAGES = {
    "brinsupri-registration-embed.html":      "pages/registration.html",
    "brinsupri-account-embed.html":           "pages/account.html",
    "brinsupri-medication-checkin-embed.html":"pages/checkin.html",
    "brinsupri-patient-consent-embed.html":   "pages/consent-patient.html",
    "brinsupri-caregiver-consent-embed.html": "pages/consent-caregiver.html",
}
LEGAL = {
    "therapy-companion-terms-and-conditions.html":            "legal/terms-and-conditions/index.html",
    "therapy-companion-privacy-policy.html":                  "legal/privacy-policy/index.html",
    "therapy-companion-data-processing-agreement.html":       "legal/data-processing-agreement/index.html",
    "therapy-companion-delivery-and-collection-services-de.html":"legal/delivery-and-collection-services-de/index.html",
    "therapy-companion-delivery-and-collection-services-at.html":"legal/delivery-and-collection-services-at/index.html",
}
# longest first so /therapy-companion/x is rewritten before /x
PATHS = [
    ("/therapy-companion/delivery-and-collection-services-de", "/legal/delivery-and-collection-services-de"),
    ("/therapy-companion/delivery-and-collection-services-at", "/legal/delivery-and-collection-services-at"),
    ("/therapy-companion/data-processing-agreement",           "/legal/data-processing-agreement"),
    ("/therapy-companion/terms-and-conditions",                "/legal/terms-and-conditions"),
    ("/therapy-companion/privacy-policy",                      "/legal/privacy-policy"),
    ("/brinsupri-registration",                                "/registration"),
    ("/brinsupri-medication-checkin",                          "/checkin"),
    ("/brinsupri-medication",                                  "/checkin"),
    ("/brinsupri-account",                                     "/account"),
    ("/brinsupri-patient-consent",                             "/-consent-patient"),
    ("/brinsupri-caregiver-consent",                           "/-consent-caregiver"),
    ("/terms-and-conditions",                                  "/legal/terms-and-conditions"),
    ("/privacy-policy",                                        "/legal/privacy-policy"),
]
# folder-per-URL copies: source page -> url folders
ROUTES = {
    "pages/registration.html":      ["", "registration"],
    "pages/account.html":           ["account"],
    "pages/checkin.html":           ["checkin"],
    "pages/consent-patient.html":   ["-consent-patient"],
    "pages/consent-caregiver.html": ["-consent-caregiver"],
}

VOID={'br','hr','img','input','meta','link','source','area','base','col','embed','param','track','wbr',
      'path','circle','rect','line','polygon','polyline','ellipse','use','stop','image',
      'feGaussianBlur','feOffset','feMerge','feMergeNode'}
class Check(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=False); s.stack=[]; s.errs=[]; s.skip=None
    def handle_starttag(s,t,a):
        if s.skip: return
        if t in ('script','style'): s.skip=t; return
        if t not in VOID: s.stack.append(t)
    def handle_endtag(s,t):
        if s.skip:
            if t==s.skip: s.skip=None
            return
        if t in VOID: return
        if s.stack and s.stack[-1]==t: s.stack.pop()
        else:
            for i in range(len(s.stack)-1,-1,-1):
                if s.stack[i]==t:
                    s.errs += [("unclosed",x) for x in s.stack[i+1:]]; del s.stack[i:]; break
            else: s.errs.append(("stray-close",t))

def rewrite(text):
    for old,new in PATHS:
        text = text.replace(old, new)
    return text

def verify(path, text):
    problems=[]
    b=text.encode("utf-8")
    if any(c>126 for c in b): problems.append("non-ASCII bytes")
    if text.count("<script")!=text.count("</script>"): problems.append("script tags unbalanced")
    if text.count("<style")!=text.count("</style>"): problems.append("style tags unbalanced")
    p=Check(); p.feed(text)
    if p.errs: problems.append(f"html parse: {p.errs[:3]}")
    if p.stack: problems.append(f"tags open at EOF: {p.stack[:3]}")
    for old,new in PATHS:
        # the old path is a substring of its own replacement, so only flag real leftovers
        for m in re.finditer(re.escape(old), text):
            if text[max(0,m.start()-6):m.start()] != "/legal":
                problems.append(f"old path left: {old}"); break
    return problems

def main():
    os.makedirs(OUT, exist_ok=True)
    built=[]; failed=0
    for src,dst in {**PAGES, **LEGAL}.items():
        s=io.open(os.path.join(SRC,src),encoding="utf-8",newline="").read()
        out=rewrite(s)
        probs=verify(dst,out)
        target=os.path.join(OUT,dst); os.makedirs(os.path.dirname(target),exist_ok=True)
        io.open(target,"w",encoding="utf-8",newline="").write(out)
        built.append((dst,len(out),probs))
        if probs: failed+=1
    # folder-per-URL copies
    for page,urls in ROUTES.items():
        s=io.open(os.path.join(OUT,page),encoding="utf-8",newline="").read()
        for u in urls:
            d=os.path.join(OUT,u); os.makedirs(d,exist_ok=True)
            io.open(os.path.join(d,"index.html"),"w",encoding="utf-8",newline="").write(s)
    io.open(os.path.join(OUT,".nojekyll"),"w").write("")
    print(f"{'FILE':<52}{'BYTES':>10}  CHECKS")
    for d,n,probs in built:
        print(f"{d:<52}{n:>10,}  {'OK' if not probs else '; '.join(probs)}")
    print(f"\nroutes: " + ", ".join("/"+u for v in ROUTES.values() for u in v))
    print("files with problems:", failed)
    return 1 if failed else 0

sys.exit(main())
