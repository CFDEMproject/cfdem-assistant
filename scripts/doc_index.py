#!/usr/bin/env python3
"""Fetch and decompress the CFDEM coupling docs' Sphinx object inventory.

Usage:
    scripts/doc_index.py [filter]

With no argument, prints the full inventory (name domain:role priority uri displayname).
With an argument, prints only lines whose name or displayname contains it (case-insensitive).
"""
import sys
import urllib.request
import zlib

URL = "https://doc.aspherix-dem.com/coupling/objects.inv"


def fetch_inventory(url):
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    # Sphinx objects.inv: 4 header lines, then zlib-compressed body.
    body = data.split(b"\n", 4)[4]
    return zlib.decompress(body).decode()


def main():
    keyword = sys.argv[1].lower() if len(sys.argv) > 1 else None
    text = fetch_inventory(URL)
    for line in text.splitlines():
        if keyword is None or keyword in line.lower():
            print(line)


if __name__ == "__main__":
    main()
