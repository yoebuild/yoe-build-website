#!/usr/bin/env python3
"""Rewrite relative links in generated Atom feeds to absolute URLs.

Feed readers resolve relative links against the ``xml:base`` Zola emits on each
entry, but the email tools that consume this feed do not. Posts that link with a
site-relative path (``/videos/``) or a heading anchor (``#summary``) therefore
arrive in a subscriber's inbox with links that go nowhere.

This runs over the built ``public/`` tree after ``zola build`` and rewrites the
escaped HTML inside every ``<content>`` element so each ``href``/``src`` is
absolute: site-relative paths get the site's base URL, and anchors and
document-relative paths get the entry's own permalink.
"""

import html
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

ENTRY_CONTENT_RE = re.compile(
    r'<content\b[^>]*\bxml:base="(?P<base>[^"]*)"[^>]*>(?P<body>.*?)</content>',
    re.DOTALL,
)
# Matches href/src inside the escaped HTML of a feed entry, where Zola encodes
# the quotes as &quot; and the slashes as &#x2F;.
LINK_RE = re.compile(r'(?P<attr>\b(?:href|src)=)&quot;(?P<url>[^&]*(?:&(?!quot;)[^&]*)*)&quot;')
ABSOLUTE_RE = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//)")


def absolutize(url, base_url, entry_url):
    """Return an absolute form of a link found in feed content."""
    decoded = html.unescape(url)
    if not decoded or ABSOLUTE_RE.match(decoded):
        return url
    target = base_url if decoded.startswith("/") else entry_url
    return html.escape(urljoin(target, decoded), quote=True)


def rewrite_feed(path, base_url):
    """Rewrite one feed in place; return the number of links made absolute."""
    original = path.read_text(encoding="utf-8")
    count = 0

    def fix_entry(match):
        nonlocal count
        entry_url = html.unescape(match.group("base"))

        def fix_link(link):
            nonlocal count
            fixed = absolutize(link.group("url"), base_url, entry_url)
            if fixed == link.group("url"):
                return link.group(0)
            count += 1
            return f'{link.group("attr")}&quot;{fixed}&quot;'

        body = LINK_RE.sub(fix_link, match.group("body"))
        return match.group(0).replace(match.group("body"), body)

    updated = ENTRY_CONTENT_RE.sub(fix_entry, original)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
    return count


def base_url_from_config(config):
    for line in config.read_text(encoding="utf-8").splitlines():
        match = re.match(r'\s*base_url\s*=\s*["\'](?P<url>[^"\']+)', line)
        if match:
            return match.group("url").rstrip("/") + "/"
    return None


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    base_url = base_url_from_config(root / "config.toml")
    if not base_url:
        print("error: could not read base_url from config.toml", file=sys.stderr)
        return 1

    feeds = sorted((root / "public").rglob("atom.xml"))
    if not feeds:
        print("error: no feeds found under public/", file=sys.stderr)
        return 1

    total = sum(rewrite_feed(feed, base_url) for feed in feeds)
    print(f"Made {total} relative link(s) absolute across {len(feeds)} feed(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
