#!/usr/bin/env python3
"""Shorten URLs using the free is.gd API (no API key needed).

Usage:
    python3 main.py https://www.example.com/some/very/long/path
    python3 main.py --file urls.txt
    python3 main.py https://example.com --custom my-link
"""
import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://is.gd/create.php"


def shorten(long_url, timeout, custom=None):
    """Return (short_url or None, error message or None)."""
    params = {"format": "simple", "url": long_url}
    if custom:
        params["shorturl"] = custom
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(
        f"{API_URL}?{query}",
        headers={"User-Agent": "url-shortener-cli/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace").strip()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace").strip()
        return None, f"HTTP {exc.code}: {detail or exc.reason}"
    except urllib.error.URLError as exc:
        return None, str(exc.reason)
    except (TimeoutError, ValueError) as exc:
        return None, str(exc)
    if body.startswith("Error:"):
        return None, body
    return body, None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Shorten URLs with the free is.gd API (no key needed).")
    parser.add_argument("urls", nargs="*", help="URL(s) to shorten")
    parser.add_argument("--file", "-f", help="file with one URL per line")
    parser.add_argument("--custom", help="custom short name (single URL only)")
    parser.add_argument("--timeout", type=float, default=10,
                        help="request timeout in seconds (default: 10)")
    args = parser.parse_args(argv)

    urls = list(args.urls)
    if args.file:
        with open(args.file, encoding="utf-8") as handle:
            urls.extend(line.strip() for line in handle if line.strip())
    if not urls:
        parser.error("no URLs given (pass URLs or --file)")
    if args.custom and len(urls) > 1:
        parser.error("--custom can only be used with a single URL")
    urls = [u if "://" in u else "https://" + u for u in urls]

    failures = 0
    for url in urls:
        short, error = shorten(url, args.timeout, args.custom)
        if error:
            print(f"{url} -> ERROR: {error}", file=sys.stderr)
            failures += 1
        else:
            print(f"{url} -> {short}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
