#!/usr/bin/env python3
"""Read and decompress the CFDEM coupling docs' Sphinx object inventory.

Reads the documentation of the installed Aspherix (found via the `aspherix` binary); --docs
online|<path> chooses another source, and exit code 3 means it could not be resolved. See
doc_source.py. A note on stderr says which source was used.

Usage:
    scripts/doc_index.py [--docs online|<path>] [filter]

With no argument, prints the full inventory (name domain:role priority uri displayname).
With an argument, prints only lines whose name or displayname contains it (case-insensitive).
"""
import sys
import zlib

from doc_source import read, split_docs_arg


def fetch_inventory(product="coupling", choice=None):
    try:
        data, _ = read(product, "objects.inv", choice, binary=True)
    except OSError as e:
        sys.exit(f"inventory not found for {product}: {e}")
    # Sphinx objects.inv: 4 header lines, then zlib-compressed body.
    body = data.split(b"\n", 4)[4]
    return zlib.decompress(body).decode()


def main():
    choice, args = split_docs_arg(sys.argv[1:])
    keyword = args[0].lower() if args else None
    text = fetch_inventory(choice=choice)
    for line in text.splitlines():
        if keyword is None or keyword in line.lower():
            print(line)


if __name__ == "__main__":
    main()
