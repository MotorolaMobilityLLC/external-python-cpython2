#! /usr/bin/env python

"""Convert ESIS events to SGML or XML markup.

This is limited, but seems sufficient for the ESIS generated by the
latex2esis.py script when run over the Python documentation.
"""
__version__ = '$Revision$'

import errno
import esistools
import os
import re
import string

from xml.utils import escape


EMPTIES_FILENAME = "../sgml/empties.dat"
LIST_EMPTIES = 0


def format_attrs(attrs, xml=0):
    attrs = attrs.items()
    attrs.sort()
    s = ''
    for name, value in attrs:
        if xml:
            s = '%s %s="%s"' % (s, name, escape(value))
        else:
            # this is a little bogus, but should do for now
            if name == value and isnmtoken(value):
                s = "%s %s" % (s, value)
            elif istoken(value):
                s = "%s %s=%s" % (s, name, value)
            else:
                s = '%s %s="%s"' % (s, name, escape(value))
    return s


_nmtoken_rx = re.compile("[a-z][-._a-z0-9]*$", re.IGNORECASE)
def isnmtoken(s):
    return _nmtoken_rx.match(s) is not None

_token_rx = re.compile("[a-z0-9][-._a-z0-9]*$", re.IGNORECASE)
def istoken(s):
    return _token_rx.match(s) is not None


def do_convert(ifp, ofp, xml=0, autoclose=()):
    if xml:
        autoclose = ()
    attrs = {}
    lastopened = None
    knownempties = []
    knownempty = 0
    lastempty = 0
    while 1:
        line = ifp.readline()
        if not line:
            break

        type = line[0]
        data = line[1:]
        if data and data[-1] == "\n":
            data = data[:-1]
        if type == "-":
            data = esistools.decode(data)
            ofp.write(escape(data))
            if "\n" in data:
                lastopened = None
            knownempty = 0
            lastempty = 0
        elif type == "(":
            if data == "COMMENT":
                ofp.write("<!--")
                continue
            if knownempty and xml:
                ofp.write("<%s%s/>" % (data, format_attrs(attrs, xml)))
            else:
                ofp.write("<%s%s>" % (data, format_attrs(attrs, xml)))
            if knownempty and data not in knownempties:
                # accumulate knowledge!
                knownempties.append(data)
            attrs = {}
            lastopened = data
            lastempty = knownempty
            knownempty = 0
        elif type == ")":
            if data == "COMMENT":
                ofp.write("-->")
                continue
            if xml:
                if not lastempty:
                    ofp.write("</%s>" % data)
            elif data not in knownempties:
                if data in autoclose:
                    pass
                elif lastopened == data:
                    ofp.write("</>")
                else:
                    ofp.write("</%s>" % data)
            lastopened = None
            lastempty = 0
        elif type == "A":
            name, type, value = string.split(data, " ", 2)
            attrs[name] = esistools.decode(value)
        elif type == "e":
            knownempty = 1

    if LIST_EMPTIES:
        knownempties.append("")
        if os.path.isfile(EMPTIES_FILENAME):
            mode = "a"
        else:
            mode = "w"
        fp = open(EMPTIES_FILENAME, mode)
        fp.write(string.join(knownempties, "\n"))
        fp.close()


def sgml_convert(ifp, ofp, autoclose):
    return do_convert(ifp, ofp, xml=0, autoclose=autoclose)


def xml_convert(ifp, ofp, autoclose):
    return do_convert(ifp, ofp, xml=1, autoclose=autoclose)


AUTOCLOSE = ("para", "term",)


def main():
    import getopt
    import sys
    #
    autoclose = AUTOCLOSE
    convert = sgml_convert
    xml = 0
    xmldecl = 0
    opts, args = getopt.getopt(sys.argv[1:], "adx",
                               ["autoclose", "declare", "xml"])
    for opt, arg in opts:
        if opt in ("-d", "--declare"):
            xmldecl = 1
        elif opt in ("-x", "--xml"):
            xml = 1
            convert = xml_convert
        elif opt in ("-a", "--autoclose"):
            autoclose = string.split(arg, ",")
    if len(args) == 0:
        ifp = sys.stdin
        ofp = sys.stdout
    elif len(args) == 1:
        ifp = open(args[0])
        ofp = sys.stdout
    elif len(args) == 2:
        ifp = open(args[0])
        ofp = open(args[1], "w")
    else:
        usage()
        sys.exit(2)
    # knownempties is ignored in the XML version
    try:
        if xml and xmldecl:
            opf.write('<?xml version="1.0" encoding="iso8859-1"?>\n')
        convert(ifp, ofp, autoclose)
    except IOError, (err, msg):
        if err != errno.EPIPE:
            raise


if __name__ == "__main__":
    main()
