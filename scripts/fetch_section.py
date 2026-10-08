#!/usr/bin/env python3
"""Read a CFDEM coupling docs page and extract one or more <section id="..."> blocks verbatim.

Usage:
    scripts/fetch_section.py [--docs online|<path>] <url> --list
    scripts/fetch_section.py [--docs online|<path>] <url> <section-id> [<section-id> ...]

<url> is a https://doc.aspherix-dem.com/coupling/<page>.html URL (or just coupling/<page>.html).
The page is read from the documentation of the installed Aspherix (found via the `aspherix` binary);
--docs online|<path> chooses another source; exit code 3 means the source could not be resolved
(the agent then asks the user). See doc_source.py.

--list prints every section id on the page, without extracting content.
Otherwise, prints the exact text of each requested section, in document order,
under a "=== <id> ===" header. No model is involved: this is a plain HTML->text
extraction, meant as a deterministic alternative to a lossy WebFetch-style summary.
Code/config blocks (Sphinx "highlight" <pre> blocks — the actual dictionary
syntax) are wrapped in ``` fences so they're visibly distinct from surrounding
prose.
"""
import sys
from html.parser import HTMLParser

from doc_source import ONLINE, read, split_docs_arg

BLOCK_TAGS = {"p", "li", "dt", "dd", "h1", "h2", "h3", "h4", "h5", "h6", "tr"}
SKIP_ANCHOR_CLASSES = {"headerlink", "toc-backref"}
CODE_START = "\x00CODE_START\x00"
CODE_END = "\x00CODE_END\x00"


class SectionExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.section_stack = []  # ids of currently open <section> elements
        self.all_ids = []  # every section id seen, in document order
        self.captured = {}  # id -> list of text chunks
        self.capture_depth = None  # section_stack depth at which capture started
        self.skip_anchor_depth = None  # tag-stack depth of an anchor we're skipping text for
        self.pre_depth = None  # tag-stack depth of a <pre> code block we're inside
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

        if tag == "pre" and self.capture_depth is not None and self.pre_depth is None:
            self.pre_depth = self.tag_depth
            self._emit(CODE_START)
        elif self.capture_depth is not None and self.pre_depth is None and tag in BLOCK_TAGS:
            self._emit("\n")

    def handle_endtag(self, tag):
        if tag == "section" and self.section_stack:
            self.section_stack.pop()
            if self.capture_depth is not None and len(self.section_stack) < self.capture_depth:
                self.capture_depth = None
        if self.pre_depth is not None and self.tag_depth == self.pre_depth:
            self._emit(CODE_END)
            self.pre_depth = None
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


def fetch_html(url, choice=None):
    rel = url[len(ONLINE):] if url.startswith(ONLINE) else url.lstrip("/")
    product, _, page = rel.partition("/")
    try:
        html, _ = read(product, page.split("#")[0], choice)
    except OSError as e:  # missing local file, or urllib.error.HTTPError/URLError
        sys.exit(f"page not found: {product}/{page}: {e}\n(it may be newer than the installed version, "
                 "or not enabled by the licence)")
    return html


def render(chunks):
    text = "".join(chunks)
    pieces = []
    for i, part in enumerate(text.split(CODE_START)):
        if i == 0:
            pieces.append(_render_prose(part))
            continue
        code, _, rest = part.partition(CODE_END)
        pieces.append("```\n" + code.strip("\n") + "\n```")
        pieces.append(_render_prose(rest))
    return "\n".join(p for p in pieces if p)


def _render_prose(text):
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def main():
    choice, argv = split_docs_arg(sys.argv[1:])
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    url = argv[0]
    args = argv[1:]
    html = fetch_html(url, choice)

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
