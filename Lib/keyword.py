#! /usr/bin/env python
#
#  Keywords (from "graminit.c")
#
#  This file is automatically generated; please don't muck it up!
#
#  To update the symbols in this file, 'cd' to the top directory of
#  the python source tree after building the interpreter and run:
#
#    PYTHONPATH=./Lib ./python Lib/keyword.py
#
#  (this path allows the import of string.py and regexmodule.so
#  for a site with no installation in place)

kwlist = [
#--start keywords--
        'and',
        'break',
        'class',
        'continue',
        'def',
        'del',
        'elif',
        'else',
        'except',
        'exec',
        'finally',
        'for',
        'from',
        'global',
        'if',
        'import',
        'in',
        'is',
        'lambda',
        'not',
        'or',
        'pass',
        'print',
        'raise',
        'return',
        'try',
        'while',
#--end keywords--
        ]

kwdict = {}
for keyword in kwlist:
    kwdict[keyword] = 1

iskeyword = kwdict.has_key

def main():
    import sys, regex, string

    args = sys.argv[1:]
    iptfile = args and args[0] or "Python/graminit.c"
    if len(args) > 1: optfile = args[1]
    else: optfile = "Lib/keyword.py"

    # scan the source file for keywords
    try:
        fp = open(iptfile)
    except IOError, err:
        sys.stderr.write("I/O error reading from %s: %s\n" % (optfile, err))
        sys.exit(1)

    strprog = regex.compile('"\([^"]+\)"')
    labelprog = regex.compile('static[ \t]+label.*=[ \t]+{')
    keywordlist = []
    while 1:
        line = fp.readline()
        if not line: break
        if labelprog.search(line) > -1: break
    while line:
        line = fp.readline()
        if string.find(line, ';') > -1: break
        if strprog.search(line) > -1: keywordlist.append(strprog.group(1))
    fp.close()

    keywordlist.sort()
    keywordlist.remove("EMPTY")

    # load the output skeleton from the target
    try:
        fp = open(optfile)
        format = fp.readlines()
        fp.close()
    except IOError, err:
        sys.stderr.write("I/O error reading from %s: %s\n" % (optfile, err))
        sys.exit(2)

    try:
        start = format.index("#--start keywords--\n") + 1
        end = format.index("#--end keywords--\n")
    except ValueError:
        sys.stderr.write("target does not contain format markers\n")
        sys.exit(3)

    # insert the lines of keywords
    lines = []
    for keyword in keywordlist:
        lines.append("        '" + keyword + "',\n")
    format[start:end] = lines

    # write the output file
    try:
        fp = open(optfile, 'w')
    except IOError, err:
        sys.stderr.write("I/O error writing to %s: %s\n" % (optfile, err))
        sys.exit(4)
    fp.write(string.join(format, ''))
    fp.close()

if __name__ == "__main__":
    main()
