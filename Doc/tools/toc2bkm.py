#! /usr/bin/env python

"""Convert a LaTeX .toc file to some PDFTeX magic to create that neat outline.

The output file has an extension of '.bkm' instead of '.out', since hyperref
already uses that extension.  Let's avoid clashing.
"""

import os
import re
import string
import sys


# Ench item in an entry is a tuple of:
#
#   Section #,  Title String,  Page #,  List of Sub-entries

cline_re = r"""^
\\contentsline\ \{([a-z]*)}             # type of section in $1
\{(?:\\numberline\ \{([0-9.A-Z]+)})?     # section number
(.*)}                                   # title string
\{(\d+)}$"""				# page number

cline_rx = re.compile(cline_re, re.VERBOSE)

OUTER_TO_INNER = -1

_transition_map = {
    ('chapter', 'section'): OUTER_TO_INNER,
    ('section', 'subsection'): OUTER_TO_INNER,
    ('subsection', 'subsubsection'): OUTER_TO_INNER,
    ('subsubsection', 'subsection'): 1,
    ('subsection', 'section'): 1,
    ('section', 'chapter'): 1,
    ('subsection', 'chapter'): 2,
    ('subsubsection', 'section'): 2,
    ('subsubsection', 'chapter'): 3,
    }

def parse_toc(fp):
    toc = top = []
    stack = [toc]
    level = 'chapter'
    lineno = 0
    while 1:
	line = fp.readline()
	if not line:
	    break
	lineno = lineno + 1
	m = cline_rx.match(line)
	if m:
	    stype, snum, title, pageno = m.group(1, 2, 3, 4)
	    title = clean_title(title)
	    entry = (stype, snum, title, string.atoi(pageno), [])
	    if stype == level:
		toc.append(entry)
	    else:
		direction = _transition_map[(level, stype)]
		if direction == OUTER_TO_INNER:
		    toc = toc[-1][-1]
		    stack.insert(0, toc)
		    toc.append(entry)
		else:
		    for i in range(direction):
			del stack[0]
			toc = stack[0]
		    toc.append(entry)
		level = stype
	else:
	    sys.stderr.write("l.%s: " + line)
    return top


hackscore_rx = re.compile(r"\\(hackscore|raisebox)\s*{[^}]*}")
title_rx = re.compile(r"\\[a-zA-Z]+\s*")
title_trans = string.maketrans("", "")

def clean_title(title):
    title = hackscore_rx.sub("_", title)
    while 1:
	m = title_rx.search(title)
	if m:
	    title = title[:m.start()] + title[m.end():]
	else:
	    break
    return string.translate(title, title_trans, "{}")


def write_toc(toc, fp):
    for entry in toc:
	write_toc_entry(entry, fp, 0)

def write_toc_entry(entry, fp, layer):
    stype, snum, title, pageno, toc = entry
    s = "\\pdfoutline goto name{page.%d}" % pageno
    if toc:
	s = "%s count -%d" % (s, len(toc))
    if snum:
	title = "%s %s" % (snum, title)
    s = "%s {%s}\n" % (s, title)
    fp.write(s)
    for entry in toc:
	write_toc_entry(entry, fp, layer + 1)


def main():
    base, ext = os.path.splitext(sys.argv[1])
    ext = ext or ".toc"
    toc = parse_toc(open(base + ext))
    write_toc(toc, open(base + ".bkm", "w"))


if __name__ == "__main__":
    main()
