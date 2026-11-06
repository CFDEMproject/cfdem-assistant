#!/usr/bin/env python3
"""Read and decompress the CFDEM coupling docs's Sphinx object inventory.

Reads the documentation of the installed Aspherix (found via the `aspherix` binary); --docs
online|<path> chooses another source, and exit code 3 means it could not be resolved. See
doc_source.py. A note on stderr says which source was used.

Usage:
    scripts/doc_index.py [--docs online|<path>] [--product solver|calibration|coupling|gui|main] [filter]

With no filter, prints the full inventory (name domain:role priority uri displayname).
With a filter, prints only lines whose name or displayname contains it (case-insensitive).
--product selects the docs section (default: coupling).
"""
import sys
import zlib

from doc_source import read, split_docs_arg


def fetch_inventory(product, choice=None):
    try:
        data, _ = read(product, "objects.inv", choice, binary=True)
    except OSError as e:
        sys.exit(f"inventory not found for {product}: {e}")
    # Sphinx objects.inv: 4 header lines, then zlib-compressed body.
    body = data.split(b"\n", 4)[4]
    return zlib.decompress(body).decode()


def main():
    choice, args = split_docs_arg(sys.argv[1:])
    product = "coupling"
    if args[:1] == ["--product"]:
        if len(args) < 2:
            sys.exit("usage: doc_index.py [--docs online|<path>] [--product solver|calibration|coupling|gui|main] [filter]")
        product, args = args[1], args[2:]
    keyword = args[0].lower() if args else None
    text = fetch_inventory(product, choice)
    for line in text.splitlines():
        if keyword is None or keyword in line.lower():
            print(line)


if __name__ == "__main__":
    main()
