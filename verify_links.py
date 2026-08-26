#!/usr/bin/env python3
"""Verify every link on the portfolio the way an anonymous visitor would see it.

A URL being *correct* and a URL being *publicly reachable* are different
properties. This script only checks the second one, because that is the one a
recruiter experiences. It therefore:

  * sends a real browser User-Agent (bot UAs get different redirects),
  * follows redirects and judges the FINAL url, not the first hop,
  * fails a 200 that lands on a sign-in wall (/-/login, /login, /session),
  * uses no git credentials, so a private repo fails the way a stranger sees it,
  * strips stray CR from hrefs before requesting them.

Usage
    python verify_links.py                     # check ./index.html, assets on disk
    python verify_links.py --base <pages-url>  # fetch index.html from the live site

Exits non-zero if anything fails, so it can gate a deploy.
"""

import argparse
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

try:
    # Some Windows setups reject valid chains with Python's bundled trust store
    # ("Basic Constraints of CA cert not marked critical"). Prefer the OS store
    # when truststore is present; fall back silently everywhere else.
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36')
TIMEOUT = 10
LOGIN_MARKERS = (
    '/-/login',        # Streamlit per-app sign-in
    '/-/auth',         # Streamlit share.streamlit.io auth bounce
    '/login',
    '/signin',
    '/session',
    'redirect_uri=',   # generic OAuth hand-off
)
SKIP_HOSTS = ('fonts.googleapis.com', 'fonts.gstatic.com')


class _Tracker(urllib.request.HTTPRedirectHandler):
    """Records the redirect chain so the first hop can be reported too."""

    def __init__(self):
        self.first = None
        self.last_target = None

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if self.first is None:
            self.first = code
        self.last_target = newurl        # kept even if the chain never completes
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url):
    """Return (initial_status, final_status, final_url, error)."""
    tracker = _Tracker()
    opener = urllib.request.build_opener(tracker)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:
            resp.read(2048)  # touch the body; some hosts only redirect on read
            return tracker.first or resp.status, resp.status, resp.url, None
    except urllib.error.HTTPError as e:
        # A redirect chain that never resolves (e.g. a sign-in bounce) lands here;
        # report where it was last headed so the cause is visible.
        landed = tracker.last_target or e.url or url
        return tracker.first or e.code, e.code, landed, None
    except Exception as e:                      # DNS, TLS, timeout, ...
        detail = str(e).strip() or type(e).__name__
        return None, None, url, '%s: %s' % (type(e).__name__, detail[:120])


def hrefs_from(html):
    """Every href outside HTML comments, de-duplicated, order preserved."""
    live = re.sub(r'<!--.*?-->', '', html, flags=re.S)   # commented-out links are not live
    out = []
    for raw in re.findall(r'href="([^"]+)"', live):
        u = raw.strip().replace('\r', '').replace('\n', '')
        if u and u not in out:
            out.append(u)
    return out


def classify(u):
    if u.startswith('#') or u.startswith('mailto:'):
        return 'skip'
    if any(h in u for h in SKIP_HOSTS):
        return 'skip'
    return 'external' if u.startswith(('http://', 'https://')) else 'asset'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', help='live site URL; omit to check local files')
    ap.add_argument('--file', default='index.html')
    args = ap.parse_args()

    if args.base:
        base = args.base if args.base.endswith('/') else args.base + '/'
        status, _, _, err = fetch(base)
        if err or status != 200:
            print('FATAL: cannot load %s (status=%s err=%s)' % (base, status, err))
            return 2
        req = urllib.request.Request(base, headers={'User-Agent': UA})
        html = urllib.request.urlopen(req, timeout=TIMEOUT).read().decode('utf-8', 'replace')
        print('source: %s (live)\n' % base)
    else:
        base = None
        if not os.path.exists(args.file):
            print('FATAL: %s not found' % args.file)
            return 2
        with open(args.file, encoding='utf-8') as fh:
            html = fh.read()
        print('source: %s (local)\n' % os.path.abspath(args.file))

    failures = []
    externals = [u for u in hrefs_from(html) if classify(u) == 'external']
    assets = [u for u in hrefs_from(html) if classify(u) == 'asset']

    print('=' * 100)
    print('EXTERNAL LINKS  (anonymous, browser UA, redirects followed)')
    print('=' * 100)
    for u in externals:
        first, final, final_url, err = fetch(u)
        # order matters: a sign-in bounce is the more useful diagnosis than the
        # bare status it happens to arrive with
        if err:
            verdict, why = 'FAIL', err
        elif any(m in final_url for m in LOGIN_MARKERS):
            verdict, why = 'FAIL', 'sign-in wall (not publicly viewable)'
        elif final != 200:
            verdict, why = 'FAIL', 'status %s' % final
        else:
            verdict, why = 'PASS', ''
        if verdict == 'FAIL':
            failures.append((u, why))
        print('%-4s %-72s %s->%s' % (verdict, u[:72], first, final))
        if final_url.rstrip('/') != u.rstrip('/'):
            print('       final: %s' % final_url[:110])
        if why:
            print('       reason: %s' % why)

    print()
    print('=' * 100)
    print('RELATIVE ASSETS')
    print('=' * 100)
    for u in assets:
        if base:
            target = urllib.parse.urljoin(base, u)
            _, final, _, err = fetch(target)
            ok = (err is None and final == 200)
            detail = 'HTTP %s' % (err or final)
        else:
            ok = os.path.exists(u)
            detail = ('%d bytes' % os.path.getsize(u)) if ok else 'missing on disk'
        if not ok:
            failures.append((u, detail))
        print('%-4s %-72s %s' % ('PASS' if ok else 'FAIL', u[:72], detail))

    print()
    print('=' * 100)
    total = len(externals) + len(assets)
    if failures:
        print('RESULT: %d of %d checks FAILED' % (len(failures), total))
        for u, why in failures:
            print('  - %s  (%s)' % (u, why))
        return 1
    print('RESULT: all %d checks passed' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
