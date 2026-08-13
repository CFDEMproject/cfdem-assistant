#!/usr/bin/env python3
"""Fetch a CFDEM coupling docs page and extract one or more <section id="..."> blocks verbatim.

Usage:
    scripts/fetch_section.py <url> --list
    scripts/fetch_section.py <url> <section-id> [<section-id> ...]

--list prints every section id on the page, without extracting content.
Otherwise, prints the exact text of each requested section, in document order,
under a "=== <id> ===" header. No model is involved: this is a plain HTML->text
extraction, meant as a deterministic alternative to a lossy WebFetch-style summary.
"""
import sys
import urllib.request
from html.parser import HTMLParser

BLOCK_TAGS = {"p", "li", "dt", "dd", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "tr"}
SKIP_ANCHOR_CLASSES = {"headerlink", "toc-backref"}


class SectionExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.section_stack = []  # ids of currently open <section> elements
        self.all_ids = []  # every section id seen, in document order
        self.captured = {}  # id -> list of text chunks
        self.capture_depth = None  # section_stack depth at which capture started
        self.skip_anchor_depth = None  # tag-stack depth of an anchor we're skipping text for
        self.tag_depth = 0

    def handle_starttag(self, tag, attrs):
        self.tag_depth += 1
        attrs = dict(attrs)

        if tag == "section":
            section_id = attrs.get("id")
            self.section_stack.append(section_id)
            if section_id:
                self.all_ids.append(section_id)
                if section_id in self.captured and self.capture_depth is None:
                    self.capture_depth = len(self.section_stack)

        if tag == "a" and self.skip_anchor_depth is None:
            classes = set((attrs.get("class") or "").split())
            if classes & SKIP_ANCHOR_CLASSES:
                self.skip_anchor_depth = self.tag_depth

        if self.capture_depth is not None and tag in BLOCK_TAGS:
            self._emit("\n")

    def handle_endtag(self, tag):
        if tag == "section" and self.section_stack:
            self.section_stack.pop()
            if self.capture_depth is not None and len(self.section_stack) < self.capture_depth:
                self.capture_depth = None
        if self.skip_anchor_depth is not None and self.tag_depth == self.skip_anchor_depth:
            self.skip_anchor_depth = None
        self.tag_depth -= 1

    def handle_data(self, data):
        if self.capture_depth is not None and self.skip_anchor_depth is None:
            self._emit(data)

    def _emit(self, text):
        current_id = self.section_stack[self.capture_depth - 1]
        self.captured[current_id].append(text)

    def start_capture(self, section_ids):
        for section_id in section_ids:
            self.captured[section_id] = []


def fetch_html(url):
    with urllib.request.urlopen(url) as resp:
        return resp.read().decode("utf-8", errors="replace")


def render(chunks):
    text = "".join(chunks)
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    args = sys.argv[2:]
    html = fetch_html(url)

    if args == ["--list"]:
        parser = SectionExtractor()
        parser.feed(html)
        for section_id in parser.all_ids:
            print(section_id)
        return

    requested = args
    parser = SectionExtractor()
    parser.start_capture(requested)
    parser.feed(html)

    found_any = False
    for section_id in requested:
        chunks = parser.captured.get(section_id) or []
        if not chunks:
            print(f"=== {section_id} (not found on this page) ===", file=sys.stderr)
            continue
        found_any = True
        print(f"=== {section_id} ===")
        print(render(chunks))
        print()

    if not found_any:
        sys.exit(1)


if __name__ == "__main__":
    main()
