#!/usr/bin/env python
"""Generate Python documentation in HTML or text for interactive use.

In the Python interpreter, do "from pydoc import help" to provide online
help.  Calling help(thing) on a Python object documents the object.

Or, at the shell command line outside of Python:

Run "pydoc <name>" to show documentation on something.  <name> may be
the name of a function, module, package, or a dotted reference to a
class or function within a module or module in a package.  If the
argument contains a path segment delimiter (e.g. slash on Unix,
backslash on Windows) it is treated as the path to a Python source file.

Run "pydoc -k <keyword>" to search for a keyword in the synopsis lines
of all available modules.

Run "pydoc -p <port>" to start an HTTP server on a given port on the
local machine to generate documentation web pages.

For platforms without a command line, "pydoc -g" starts the HTTP server
and also pops up a little window for controlling it.

Run "pydoc -w <name>" to write out the HTML documentation for a module
to a file named "<name>.html".
"""

__author__ = "Ka-Ping Yee <ping@lfw.org>"
__date__ = "26 February 2001"
__version__ = "$Revision$"
__credits__ = """Guido van Rossum, for an excellent programming language.
Tommy Burnette, the original creator of manpy.
Paul Prescod, for all his work on onlinehelp.
Richard Chamberlain, for the first implementation of textdoc.

Mynd you, m��se bites Kan be pretty nasti..."""

# Note: this module is designed to deploy instantly and run under any
# version of Python from 1.5 and up.  That's why it's a single file and
# some 2.0 features (like string methods) are conspicuously absent.

# Known bugs that can't be fixed here:
#   - imp.load_module() cannot be prevented from clobbering existing
#     loaded modules, so calling synopsis() on a binary module file
#     changes the contents of any existing module with the same name.
#   - If the __file__ attribute on a module is a relative path and
#     the current directory is changed with os.chdir(), an incorrect
#     path will be displayed.

import sys, imp, os, stat, re, types, inspect
from repr import Repr
from string import expandtabs, find, join, lower, split, strip, rfind, rstrip

# --------------------------------------------------------- common routines

def pathdirs():
    """Convert sys.path into a list of absolute, existing, unique paths."""
    dirs = []
    normdirs = []
    for dir in sys.path:
        dir = os.path.abspath(dir or '.')
        normdir = os.path.normcase(dir)
        if normdir not in normdirs and os.path.isdir(dir):
            dirs.append(dir)
            normdirs.append(normdir)
    return dirs

def getdoc(object):
    """Get the doc string or comments for an object."""
    result = inspect.getdoc(object) or inspect.getcomments(object)
    return result and re.sub('^ *\n', '', rstrip(result)) or ''

def splitdoc(doc):
    """Split a doc string into a synopsis line (if any) and the rest."""
    lines = split(strip(doc), '\n')
    if len(lines) == 1:
        return lines[0], ''
    elif len(lines) >= 2 and not rstrip(lines[1]):
        return lines[0], join(lines[2:], '\n')
    return '', join(lines, '\n')

def classname(object, modname):
    """Get a class name and qualify it with a module name if necessary."""
    name = object.__name__
    if object.__module__ != modname:
        name = object.__module__ + '.' + name
    return name

def isdata(object):
    """Check if an object is of a type that probably means it's data."""
    return not (inspect.ismodule(object) or inspect.isclass(object) or
                inspect.isroutine(object) or inspect.isframe(object) or
                inspect.istraceback(object) or inspect.iscode(object))

def replace(text, *pairs):
    """Do a series of global replacements on a string."""
    while pairs:
        text = join(split(text, pairs[0]), pairs[1])
        pairs = pairs[2:]
    return text

def cram(text, maxlen):
    """Omit part of a string if needed to make it fit in a maximum length."""
    if len(text) > maxlen:
        pre = max(0, (maxlen-3)/2)
        post = max(0, maxlen-3-pre)
        return text[:pre] + '...' + text[len(text)-post:]
    return text

def stripid(text):
    """Remove the hexadecimal id from a Python object representation."""
    # The behaviour of %p is implementation-dependent; we check two cases.
    for pattern in [' at 0x[0-9a-f]{6,}>$', ' at [0-9A-F]{8,}>$']:
        if re.search(pattern, repr(Exception)):
            return re.sub(pattern, '>', text)
    return text

def allmethods(cl):
    methods = {}
    for key, value in inspect.getmembers(cl, inspect.ismethod):
        methods[key] = 1
    for base in cl.__bases__:
        methods.update(allmethods(base)) # all your base are belong to us
    for key in methods.keys():
        methods[key] = getattr(cl, key)
    return methods

# ----------------------------------------------------- module manipulation

def ispackage(path):
    """Guess whether a path refers to a package directory."""
    if os.path.isdir(path):
        for ext in ['.py', '.pyc', '.pyo']:
            if os.path.isfile(os.path.join(path, '__init__' + ext)):
                return 1

def synopsis(filename, cache={}):
    """Get the one-line summary out of a module file."""
    mtime = os.stat(filename)[stat.ST_MTIME]
    lastupdate, result = cache.get(filename, (0, None))
    if lastupdate < mtime:
        info = inspect.getmoduleinfo(filename)
        file = open(filename)
        if info and 'b' in info[2]: # binary modules have to be imported
            try: module = imp.load_module('__temp__', file, filename, info[1:])
            except: return None
            result = split(module.__doc__ or '', '\n')[0]
            del sys.modules['__temp__']
        else: # text modules can be directly examined
            line = file.readline()
            while line[:1] == '#' or not strip(line):
                line = file.readline()
                if not line: break
            line = strip(line)
            if line[:4] == 'r"""': line = line[1:]
            if line[:3] == '"""':
                line = line[3:]
                if line[-1:] == '\\': line = line[:-1]
                while not strip(line):
                    line = file.readline()
                    if not line: break
                result = strip(split(line, '"""')[0])
            else: result = None
        file.close()
        cache[filename] = (mtime, result)
    return result

class ErrorDuringImport(Exception):
    """Errors that occurred while trying to import something to document it."""
    def __init__(self, filename, (exc, value, tb)):
        self.filename = filename
        self.exc = exc
        self.value = value
        self.tb = tb

    def __str__(self):
        exc = self.exc
        if type(exc) is types.ClassType:
            exc = exc.__name__
        return 'problem in %s - %s: %s' % (self.filename, exc, self.value)

def importfile(path):
    """Import a Python source file or compiled file given its path."""
    magic = imp.get_magic()
    file = open(path, 'r')
    if file.read(len(magic)) == magic:
        kind = imp.PY_COMPILED
    else:
        kind = imp.PY_SOURCE
    file.close()
    filename = os.path.basename(path)
    name, ext = os.path.splitext(filename)
    file = open(path, 'r')
    try:
        module = imp.load_module(name, file, path, (ext, 'r', kind))
    except:
        raise ErrorDuringImport(path, sys.exc_info())
    file.close()
    return module

def safeimport(path, forceload=0, cache={}):
    """Import a module; handle errors; return None if the module isn't found.

    If the module *is* found but an exception occurs, it's wrapped in an
    ErrorDuringImport exception and reraised.  Unlike __import__, if a
    package path is specified, the module at the end of the path is returned,
    not the package at the beginning.  If the optional 'forceload' argument
    is 1, we reload the module from disk (unless it's a dynamic extension)."""
    if forceload and sys.modules.has_key(path):
        # This is the only way to be sure.  Checking the mtime of the file
        # isn't good enough (e.g. what if the module contains a class that
        # inherits from another module that has changed?).
        if path not in sys.builtin_module_names:
            # Python never loads a dynamic extension a second time from the
            # same path, even if the file is changed or missing.  Deleting
            # the entry in sys.modules doesn't help for dynamic extensions,
            # so we're not even going to try to keep them up to date.
            info = inspect.getmoduleinfo(sys.modules[path].__file__)
            if info[3] != imp.C_EXTENSION:
                cache[path] = sys.modules[path] # prevent module from clearing
                del sys.modules[path]
    try:
        module = __import__(path)
    except:
        # Did the error occur before or after the module was found?
        (exc, value, tb) = info = sys.exc_info()
        if sys.modules.has_key(path):
            # An error occured while executing the imported module.
            raise ErrorDuringImport(sys.modules[path].__file__, info)
        elif exc is SyntaxError:
            # A SyntaxError occurred before we could execute the module.
            raise ErrorDuringImport(value.filename, info)
        elif exc is ImportError and \
             split(lower(str(value)))[:2] == ['no', 'module']:
            # The module was not found.
            return None
        else:
            # Some other error occurred during the importing process.
            raise ErrorDuringImport(path, sys.exc_info())
    for part in split(path, '.')[1:]:
        try: module = getattr(module, part)
        except AttributeError: return None
    return module

# ---------------------------------------------------- formatter base class

class Doc:
    def document(self, object, name=None, *args):
        """Generate documentation for an object."""
        args = (object, name) + args
        if inspect.ismodule(object): return apply(self.docmodule, args)
        if inspect.isclass(object): return apply(self.docclass, args)
        if inspect.isroutine(object): return apply(self.docroutine, args)
        return apply(self.docother, args)

    def fail(self, object, name=None, *args):
        """Raise an exception for unimplemented types."""
        message = "don't know how to document object%s of type %s" % (
            name and ' ' + repr(name), type(object).__name__)
        raise TypeError, message

    docmodule = docclass = docroutine = docother = fail

# -------------------------------------------- HTML documentation generator

class HTMLRepr(Repr):
    """Class for safely making an HTML representation of a Python object."""
    def __init__(self):
        Repr.__init__(self)
        self.maxlist = self.maxtuple = 20
        self.maxdict = 10
        self.maxstring = self.maxother = 100

    def escape(self, text):
        return replace(text, '&', '&amp;', '<', '&lt;', '>', '&gt;')

    def repr(self, object):
        return Repr.repr(self, object)

    def repr1(self, x, level):
        methodname = 'repr_' + join(split(type(x).__name__), '_')
        if hasattr(self, methodname):
            return getattr(self, methodname)(x, level)
        else:
            return self.escape(cram(stripid(repr(x)), self.maxother))

    def repr_string(self, x, level):
        test = cram(x, self.maxstring)
        testrepr = repr(test)
        if '\\' in test and '\\' not in replace(testrepr, r'\\', ''):
            # Backslashes are only literal in the string and are never
            # needed to make any special characters, so show a raw string.
            return 'r' + testrepr[0] + self.escape(test) + testrepr[0]
        return re.sub(r'((\\[\\abfnrtv\'"]|\\[0-9]..|\\x..|\\u....)+)',
                      r'<font color="#c040c0">\1</font>',
                      self.escape(testrepr))

    def repr_instance(self, x, level):
        try:
            return self.escape(cram(stripid(repr(x)), self.maxstring))
        except:
            return self.escape('<%s instance>' % x.__class__.__name__)

    repr_unicode = repr_string

class HTMLDoc(Doc):
    """Formatter class for HTML documentation."""

    # ------------------------------------------- HTML formatting utilities

    _repr_instance = HTMLRepr()
    repr = _repr_instance.repr
    escape = _repr_instance.escape

    def page(self, title, contents):
        """Format an HTML page."""
        return '''
<!doctype html public "-//W3C//DTD HTML 4.0 Transitional//EN">
<html><head><title>Python: %s</title>
<style type="text/css"><!--
TT { font-family: lucidatypewriter, lucida console, courier }
--></style></head><body bgcolor="#f0f0f8">
%s
</body></html>''' % (title, contents)

    def heading(self, title, fgcol, bgcol, extras=''):
        """Format a page heading."""
        return '''
<table width="100%%" cellspacing=0 cellpadding=2 border=0>
<tr bgcolor="%s">
<td valign=bottom><small>&nbsp;<br></small
><font color="%s" face="helvetica, arial">&nbsp;<br>%s</font></td
><td align=right valign=bottom
><font color="%s" face="helvetica, arial">%s</font></td></tr></table>
    ''' % (bgcol, fgcol, title, fgcol, extras or '&nbsp;')

    def section(self, title, fgcol, bgcol, contents, width=10,
                prelude='', marginalia=None, gap='&nbsp;&nbsp;'):
        """Format a section with a heading."""
        if marginalia is None:
            marginalia = '<tt>' + '&nbsp;' * width + '</tt>'
        result = '''
<p><table width="100%%" cellspacing=0 cellpadding=2 border=0>
<tr bgcolor="%s">
<td colspan=3 valign=bottom><small><small>&nbsp;<br></small></small
><font color="%s" face="helvetica, arial">%s</font></td></tr>
    ''' % (bgcol, fgcol, title)
        if prelude:
            result = result + '''
<tr bgcolor="%s"><td rowspan=2>%s</td>
<td colspan=2>%s</td></tr>
<tr><td>%s</td>''' % (bgcol, marginalia, prelude, gap)
        else:
            result = result + '''
<tr><td bgcolor="%s">%s</td><td>%s</td>''' % (bgcol, marginalia, gap)

        return result + '\n<td width="100%%">%s</td></tr></table>' % contents

    def bigsection(self, title, *args):
        """Format a section with a big heading."""
        title = '<big><strong>%s</strong></big>' % title
        return apply(self.section, (title,) + args)

    def preformat(self, text):
        """Format literal preformatted text."""
        text = self.escape(expandtabs(text))
        return replace(text, '\n\n', '\n \n', '\n\n', '\n \n',
                             ' ', '&nbsp;', '\n', '<br>\n')

    def multicolumn(self, list, format, cols=4):
        """Format a list of items into a multi-column list."""
        result = ''
        rows = (len(list)+cols-1)/cols
        for col in range(cols):
            result = result + '<td width="%d%%" valign=top>' % (100/cols)
            for i in range(rows*col, rows*col+rows):
                if i < len(list):
                    result = result + format(list[i]) + '<br>\n'
            result = result + '</td>'
        return '<table width="100%%"><tr>%s</tr></table>' % result

    def small(self, text): return '<small>%s</small>' % text
    def grey(self, text): return '<font color="#909090">%s</font>' % text

    def namelink(self, name, *dicts):
        """Make a link for an identifier, given name-to-URL mappings."""
        for dict in dicts:
            if dict.has_key(name):
                return '<a href="%s">%s</a>' % (dict[name], name)
        return name

    def classlink(self, object, modname):
        """Make a link for a class."""
        name, module = object.__name__, sys.modules.get(object.__module__)
        if hasattr(module, name) and getattr(module, name) is object:
            return '<a href="%s.html#%s">%s</a>' % (
                module.__name__, name, classname(object, modname))
        return classname(object, modname)

    def modulelink(self, object):
        """Make a link for a module."""
        return '<a href="%s.html">%s</a>' % (object.__name__, object.__name__)

    def modpkglink(self, (name, path, ispackage, shadowed)):
        """Make a link for a module or package to display in an index."""
        if shadowed:
            return self.grey(name)
        if path:
            url = '%s.%s.html' % (path, name)
        else:
            url = '%s.html' % name
        if ispackage:
            text = '<strong>%s</strong>&nbsp;(package)' % name
        else:
            text = name
        return '<a href="%s">%s</a>' % (url, text)

    def markup(self, text, escape=None, funcs={}, classes={}, methods={}):
        """Mark up some plain text, given a context of symbols to look for.
        Each context dictionary maps object names to anchor names."""
        escape = escape or self.escape
        results = []
        here = 0
        pattern = re.compile(r'\b((http|ftp)://\S+[\w/]|'
                                r'RFC[- ]?(\d+)|'
                                r'PEP[- ]?(\d+)|'
                                r'(self\.)?(\w+))\b')
        while 1:
            match = pattern.search(text, here)
            if not match: break
            start, end = match.span()
            results.append(escape(text[here:start]))

            all, scheme, rfc, pep, selfdot, name = match.groups()
            if scheme:
                results.append('<a href="%s">%s</a>' % (all, escape(all)))
            elif rfc:
                url = 'http://www.rfc-editor.org/rfc/rfc%d.txt' % int(rfc)
                results.append('<a href="%s">%s</a>' % (url, escape(all)))
            elif pep:
                url = 'http://www.python.org/peps/pep-%04d.html' % int(pep)
                results.append('<a href="%s">%s</a>' % (url, escape(all)))
            elif text[end:end+1] == '(':
                results.append(self.namelink(name, methods, funcs, classes))
            elif selfdot:
                results.append('self.<strong>%s</strong>' % name)
            else:
                results.append(self.namelink(name, classes))
            here = end
        results.append(escape(text[here:]))
        return join(results, '')

    # ---------------------------------------------- type-specific routines

    def formattree(self, tree, modname, parent=None):
        """Produce HTML for a class tree as given by inspect.getclasstree()."""
        result = ''
        for entry in tree:
            if type(entry) is type(()):
                c, bases = entry
                result = result + '<dt><font face="helvetica, arial"><small>'
                result = result + self.classlink(c, modname)
                if bases and bases != (parent,):
                    parents = []
                    for base in bases:
                        parents.append(self.classlink(base, modname))
                    result = result + '(' + join(parents, ', ') + ')'
                result = result + '\n</small></font></dt>'
            elif type(entry) is type([]):
                result = result + '<dd>\n%s</dd>\n' % self.formattree(
                    entry, modname, c)
        return '<dl>\n%s</dl>\n' % result

    def docmodule(self, object, name=None, mod=None):
        """Produce HTML documentation for a module object."""
        name = object.__name__ # ignore the passed-in name
        parts = split(name, '.')
        links = []
        for i in range(len(parts)-1):
            links.append(
                '<a href="%s.html"><font color="#ffffff">%s</font></a>' %
                (join(parts[:i+1], '.'), parts[i]))
        linkedname = join(links + parts[-1:], '.')
        head = '<big><big><strong>%s</strong></big></big>' % linkedname
        try:
            path = inspect.getabsfile(object)
            url = path
            if sys.platform == 'win32':
                import nturl2path
                url = nturl2path.pathname2url(path)
            filelink = '<a href="file:%s">%s</a>' % (url, path)
        except TypeError:
            filelink = '(built-in)'
        info = []
        if hasattr(object, '__version__'):
            version = str(object.__version__)
            if version[:11] == '$' + 'Revision: ' and version[-1:] == '$':
                version = strip(version[11:-1])
            info.append('version %s' % self.escape(version))
        if hasattr(object, '__date__'):
            info.append(self.escape(str(object.__date__)))
        if info:
            head = head + ' (%s)' % join(info, ', ')
        result = self.heading(
            head, '#ffffff', '#7799ee', '<a href=".">index</a><br>' + filelink)

        modules = inspect.getmembers(object, inspect.ismodule)

        classes, cdict = [], {}
        for key, value in inspect.getmembers(object, inspect.isclass):
            if (inspect.getmodule(value) or object) is object:
                classes.append((key, value))
                cdict[key] = cdict[value] = '#' + key
        for key, value in classes:
            for base in value.__bases__:
                key, modname = base.__name__, base.__module__
                module = sys.modules.get(modname)
                if modname != name and module and hasattr(module, key):
                    if getattr(module, key) is base:
                        if not cdict.has_key(key):
                            cdict[key] = cdict[base] = modname + '.html#' + key
        funcs, fdict = [], {}
        for key, value in inspect.getmembers(object, inspect.isroutine):
            if inspect.isbuiltin(value) or inspect.getmodule(value) is object:
                funcs.append((key, value))
                fdict[key] = '#-' + key
                if inspect.isfunction(value): fdict[value] = fdict[key]
        data = []
        for key, value in inspect.getmembers(object, isdata):
            if key not in ['__builtins__', '__doc__']:
                data.append((key, value))

        doc = self.markup(getdoc(object), self.preformat, fdict, cdict)
        doc = doc and '<tt>%s</tt>' % doc
        result = result + '<p>%s</p>\n' % self.small(doc)

        if hasattr(object, '__path__'):
            modpkgs = []
            modnames = []
            for file in os.listdir(object.__path__[0]):
                path = os.path.join(object.__path__[0], file)
                modname = inspect.getmodulename(file)
                if modname and modname not in modnames:
                    modpkgs.append((modname, name, 0, 0))
                    modnames.append(modname)
                elif ispackage(path):
                    modpkgs.append((file, name, 1, 0))
            modpkgs.sort()
            contents = self.multicolumn(modpkgs, self.modpkglink)
            result = result + self.bigsection(
                'Package Contents', '#ffffff', '#aa55cc', contents)
        elif modules:
            contents = self.multicolumn(
                modules, lambda (key, value), s=self: s.modulelink(value))
            result = result + self.bigsection(
                'Modules', '#fffff', '#aa55cc', contents)

        if classes:
            classlist = map(lambda (key, value): value, classes)
            contents = [
                self.formattree(inspect.getclasstree(classlist, 1), name)]
            for key, value in classes:
                contents.append(self.document(value, key, name, fdict, cdict))
            result = result + self.bigsection(
                'Classes', '#ffffff', '#ee77aa', join(contents))
        if funcs:
            contents = []
            for key, value in funcs:
                contents.append(self.document(value, key, name, fdict, cdict))
            result = result + self.bigsection(
                'Functions', '#ffffff', '#eeaa77', join(contents))
        if data:
            contents = []
            for key, value in data:
                contents.append(self.document(value, key))
            result = result + self.bigsection(
                'Data', '#ffffff', '#55aa55', join(contents, '<br>\n'))
        if hasattr(object, '__author__'):
            contents = self.markup(str(object.__author__), self.preformat)
            result = result + self.bigsection(
                'Author', '#ffffff', '#7799ee', contents)
        if hasattr(object, '__credits__'):
            contents = self.markup(str(object.__credits__), self.preformat)
            result = result + self.bigsection(
                'Credits', '#ffffff', '#7799ee', contents)

        return result

    def docclass(self, object, name=None, mod=None, funcs={}, classes={}):
        """Produce HTML documentation for a class object."""
        realname = object.__name__
        name = name or realname
        bases = object.__bases__
        contents = ''

        methods, mdict = allmethods(object).items(), {}
        methods.sort()
        for key, value in methods:
            mdict[key] = mdict[value] = '#' + name + '-' + key
        for key, value in methods:
            contents = contents + self.document(
                value, key, mod, funcs, classes, mdict, object)

        if name == realname:
            title = '<a name="%s">class <strong>%s</strong></a>' % (
                name, realname)
        else:
            title = '<strong>%s</strong> = <a name="%s">class %s</a>' % (
                name, name, realname)
        if bases:
            parents = []
            for base in bases:
                parents.append(self.classlink(base, object.__module__))
            title = title + '(%s)' % join(parents, ', ')
        doc = self.markup(
            getdoc(object), self.preformat, funcs, classes, mdict)
        doc = self.small(doc and '<tt>%s<br>&nbsp;</tt>' % doc or
                                 self.small('&nbsp;'))
        return self.section(title, '#000000', '#ffc8d8', contents, 5, doc)

    def formatvalue(self, object):
        """Format an argument default value as text."""
        return self.small(self.grey('=' + self.repr(object)))

    def docroutine(self, object, name=None, mod=None,
                   funcs={}, classes={}, methods={}, cl=None):
        """Produce HTML documentation for a function or method object."""
        realname = object.__name__
        name = name or realname
        anchor = (cl and cl.__name__ or '') + '-' + name
        note = ''
        skipdocs = 0
        if inspect.ismethod(object):
            imclass = object.im_class
            if cl:
                if imclass is not cl:
                    note = ' from ' + self.classlink(imclass, mod)
                    skipdocs = 1
            else:
                if object.im_self:
                    note = ' method of %s instance' % self.classlink(
                        object.im_self.__class__, mod)
                else:
                    note = ' unbound %s method' % self.classlink(imclass,mod)
            object = object.im_func

        if name == realname:
            title = '<a name="%s"><strong>%s</strong></a>' % (anchor, realname)
        else:
            if (cl and cl.__dict__.has_key(realname) and
                cl.__dict__[realname] is object):
                reallink = '<a href="#%s">%s</a>' % (
                    cl.__name__ + '-' + realname, realname)
                skipdocs = 1
            else:
                reallink = realname
            title = '<a name="%s"><strong>%s</strong></a> = %s' % (
                anchor, name, reallink)
        if inspect.isbuiltin(object):
            argspec = '(...)'
        else:
            args, varargs, varkw, defaults = inspect.getargspec(object)
            argspec = inspect.formatargspec(
                args, varargs, varkw, defaults, formatvalue=self.formatvalue)
            if realname == '<lambda>':
                decl = '<em>lambda</em>'
                argspec = argspec[1:-1] # remove parentheses

        decl = title + argspec + (note and self.small(self.grey(
            '<font face="helvetica, arial">%s</font>' % note)))

        if skipdocs:
            return '<dl><dt>%s</dl>\n' % decl
        else:
            doc = self.markup(
                getdoc(object), self.preformat, funcs, classes, methods)
            doc = doc and '<dd>' + self.small('<tt>%s</tt>' % doc)
            return '<dl><dt>%s%s</dl>\n' % (decl, doc)

    def docother(self, object, name=None, mod=None):
        """Produce HTML documentation for a data object."""
        lhs = name and '<strong>%s</strong> = ' % name or ''
        return lhs + self.repr(object)

    def index(self, dir, shadowed=None):
        """Generate an HTML index for a directory of modules."""
        modpkgs = []
        if shadowed is None: shadowed = {}
        seen = {}
        files = os.listdir(dir)

        def found(name, ispackage,
                  modpkgs=modpkgs, shadowed=shadowed, seen=seen):
            if not seen.has_key(name):
                modpkgs.append((name, '', ispackage, shadowed.has_key(name)))
                seen[name] = 1
                shadowed[name] = 1

        # Package spam/__init__.py takes precedence over module spam.py.
        for file in files:
            path = os.path.join(dir, file)
            if ispackage(path): found(file, 1)
        for file in files:
            path = os.path.join(dir, file)
            if os.path.isfile(path):
                modname = inspect.getmodulename(file)
                if modname: found(modname, 0)

        modpkgs.sort()
        contents = self.multicolumn(modpkgs, self.modpkglink)
        return self.bigsection(dir, '#ffffff', '#ee77aa', contents)

# -------------------------------------------- text documentation generator

class TextRepr(Repr):
    """Class for safely making a text representation of a Python object."""
    def __init__(self):
        Repr.__init__(self)
        self.maxlist = self.maxtuple = 20
        self.maxdict = 10
        self.maxstring = self.maxother = 100

    def repr1(self, x, level):
        methodname = 'repr_' + join(split(type(x).__name__), '_')
        if hasattr(self, methodname):
            return getattr(self, methodname)(x, level)
        else:
            return cram(stripid(repr(x)), self.maxother)

    def repr_string(self, x, level):
        test = cram(x, self.maxstring)
        testrepr = repr(test)
        if '\\' in test and '\\' not in replace(testrepr, r'\\', ''):
            # Backslashes are only literal in the string and are never
            # needed to make any special characters, so show a raw string.
            return 'r' + testrepr[0] + test + testrepr[0]
        return testrepr

    def repr_instance(self, x, level):
        try:
            return cram(stripid(repr(x)), self.maxstring)
        except:
            return '<%s instance>' % x.__class__.__name__

class TextDoc(Doc):
    """Formatter class for text documentation."""

    # ------------------------------------------- text formatting utilities

    _repr_instance = TextRepr()
    repr = _repr_instance.repr

    def bold(self, text):
        """Format a string in bold by overstriking."""
        return join(map(lambda ch: ch + '\b' + ch, text), '')

    def indent(self, text, prefix='    '):
        """Indent text by prepending a given prefix to each line."""
        if not text: return ''
        lines = split(text, '\n')
        lines = map(lambda line, prefix=prefix: prefix + line, lines)
        if lines: lines[-1] = rstrip(lines[-1])
        return join(lines, '\n')

    def section(self, title, contents):
        """Format a section with a given heading."""
        return self.bold(title) + '\n' + rstrip(self.indent(contents)) + '\n\n'

    # ---------------------------------------------- type-specific routines

    def formattree(self, tree, modname, parent=None, prefix=''):
        """Render in text a class tree as returned by inspect.getclasstree()."""
        result = ''
        for entry in tree:
            if type(entry) is type(()):
                c, bases = entry
                result = result + prefix + classname(c, modname)
                if bases and bases != (parent,):
                    parents = map(lambda c, m=modname: classname(c, m), bases)
                    result = result + '(%s)' % join(parents, ', ')
                result = result + '\n'
            elif type(entry) is type([]):
                result = result + self.formattree(
                    entry, modname, c, prefix + '    ')
        return result

    def docmodule(self, object, name=None, mod=None):
        """Produce text documentation for a given module object."""
        name = object.__name__ # ignore the passed-in name
        synop, desc = splitdoc(getdoc(object))
        result = self.section('NAME', name + (synop and ' - ' + synop))

        try:
            file = inspect.getabsfile(object)
        except TypeError:
            file = '(built-in)'
        result = result + self.section('FILE', file)
        if desc:
            result = result + self.section('DESCRIPTION', desc)

        classes = []
        for key, value in inspect.getmembers(object, inspect.isclass):
            if (inspect.getmodule(value) or object) is object:
                classes.append((key, value))
        funcs = []
        for key, value in inspect.getmembers(object, inspect.isroutine):
            if inspect.isbuiltin(value) or inspect.getmodule(value) is object:
                funcs.append((key, value))
        data = []
        for key, value in inspect.getmembers(object, isdata):
            if key not in ['__builtins__', '__doc__']:
                data.append((key, value))

        if hasattr(object, '__path__'):
            modpkgs = []
            for file in os.listdir(object.__path__[0]):
                path = os.path.join(object.__path__[0], file)
                modname = inspect.getmodulename(file)
                if modname and modname not in modpkgs:
                    modpkgs.append(modname)
                elif ispackage(path):
                    modpkgs.append(file + ' (package)')
            modpkgs.sort()
            result = result + self.section(
                'PACKAGE CONTENTS', join(modpkgs, '\n'))

        if classes:
            classlist = map(lambda (key, value): value, classes)
            contents = [self.formattree(
                inspect.getclasstree(classlist, 1), name)]
            for key, value in classes:
                contents.append(self.document(value, key, name))
            result = result + self.section('CLASSES', join(contents, '\n'))

        if funcs:
            contents = []
            for key, value in funcs:
                contents.append(self.document(value, key, name))
            result = result + self.section('FUNCTIONS', join(contents, '\n'))

        if data:
            contents = []
            for key, value in data:
                contents.append(self.docother(value, key, name, 70))
            result = result + self.section('DATA', join(contents, '\n'))

        if hasattr(object, '__version__'):
            version = str(object.__version__)
            if version[:11] == '$' + 'Revision: ' and version[-1:] == '$':
                version = strip(version[11:-1])
            result = result + self.section('VERSION', version)
        if hasattr(object, '__date__'):
            result = result + self.section('DATE', str(object.__date__))
        if hasattr(object, '__author__'):
            result = result + self.section('AUTHOR', str(object.__author__))
        if hasattr(object, '__credits__'):
            result = result + self.section('CREDITS', str(object.__credits__))
        return result

    def docclass(self, object, name=None, mod=None):
        """Produce text documentation for a given class object."""
        realname = object.__name__
        name = name or realname
        bases = object.__bases__

        if name == realname:
            title = 'class ' + self.bold(realname)
        else:
            title = self.bold(name) + ' = class ' + realname
        if bases:
            def makename(c, m=object.__module__): return classname(c, m)
            parents = map(makename, bases)
            title = title + '(%s)' % join(parents, ', ')

        doc = getdoc(object)
        contents = doc and doc + '\n'
        methods = allmethods(object).items()
        methods.sort()
        for key, value in methods:
            contents = contents + '\n' + self.document(value, key, mod, object)

        if not contents: return title + '\n'
        return title + '\n' + self.indent(rstrip(contents), ' |  ') + '\n'

    def formatvalue(self, object):
        """Format an argument default value as text."""
        return '=' + self.repr(object)

    def docroutine(self, object, name=None, mod=None, cl=None):
        """Produce text documentation for a function or method object."""
        realname = object.__name__
        name = name or realname
        note = ''
        skipdocs = 0
        if inspect.ismethod(object):
            imclass = object.im_class
            if cl:
                if imclass is not cl:
                    note = ' from ' + classname(imclass, mod)
                    skipdocs = 1
            else:
                if object.im_self:
                    note = ' method of %s instance' % classname(
                        object.im_self.__class__, mod)
                else:
                    note = ' unbound %s method' % classname(imclass,mod)
            object = object.im_func

        if name == realname:
            title = self.bold(realname)
        else:
            if (cl and cl.__dict__.has_key(realname) and
                cl.__dict__[realname] is object):
                skipdocs = 1
            title = self.bold(name) + ' = ' + realname
        if inspect.isbuiltin(object):
            argspec = '(...)'
        else:
            args, varargs, varkw, defaults = inspect.getargspec(object)
            argspec = inspect.formatargspec(
                args, varargs, varkw, defaults, formatvalue=self.formatvalue)
            if realname == '<lambda>':
                title = 'lambda'
                argspec = argspec[1:-1] # remove parentheses
        decl = title + argspec + note

        if skipdocs:
            return decl + '\n'
        else:
            doc = getdoc(object) or ''
            return decl + '\n' + (doc and rstrip(self.indent(doc)) + '\n')

    def docother(self, object, name=None, mod=None, maxlen=None):
        """Produce text documentation for a data object."""
        repr = self.repr(object)
        if maxlen:
            line = (name and name + ' = ' or '') + repr
            chop = maxlen - len(line)
            if chop < 0: repr = repr[:chop] + '...'
        line = (name and self.bold(name) + ' = ' or '') + repr
        return line

# --------------------------------------------------------- user interfaces

def pager(text):
    """The first time this is called, determine what kind of pager to use."""
    global pager
    pager = getpager()
    pager(text)

def getpager():
    """Decide what method to use for paging through text."""
    if type(sys.stdout) is not types.FileType:
        return plainpager
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return plainpager
    if os.environ.has_key('PAGER'):
        if sys.platform == 'win32': # pipes completely broken in Windows
            return lambda text: tempfilepager(plain(text), os.environ['PAGER'])
        elif os.environ.get('TERM') in ['dumb', 'emacs']:
            return lambda text: pipepager(plain(text), os.environ['PAGER'])
        else:
            return lambda text: pipepager(text, os.environ['PAGER'])
    if sys.platform == 'win32':
        return lambda text: tempfilepager(plain(text), 'more <')
    if hasattr(os, 'system') and os.system('less 2>/dev/null') == 0:
        return lambda text: pipepager(text, 'less')

    import tempfile
    filename = tempfile.mktemp()
    open(filename, 'w').close()
    try:
        if hasattr(os, 'system') and os.system('more %s' % filename) == 0:
            return lambda text: pipepager(text, 'more')
        else:
            return ttypager
    finally:
        os.unlink(filename)

def plain(text):
    """Remove boldface formatting from text."""
    return re.sub('.\b', '', text)

def pipepager(text, cmd):
    """Page through text by feeding it to another program."""
    pipe = os.popen(cmd, 'w')
    try:
        pipe.write(text)
        pipe.close()
    except IOError:
        pass # Ignore broken pipes caused by quitting the pager program.

def tempfilepager(text, cmd):
    """Page through text by invoking a program on a temporary file."""
    import tempfile
    filename = tempfile.mktemp()
    file = open(filename, 'w')
    file.write(text)
    file.close()
    try:
        os.system(cmd + ' ' + filename)
    finally:
        os.unlink(filename)

def ttypager(text):
    """Page through text on a text terminal."""
    lines = split(plain(text), '\n')
    try:
        import tty
        fd = sys.stdin.fileno()
        old = tty.tcgetattr(fd)
        tty.setcbreak(fd)
        getchar = lambda: sys.stdin.read(1)
    except (ImportError, AttributeError):
        tty = None
        getchar = lambda: sys.stdin.readline()[:-1][:1]

    try:
        r = inc = os.environ.get('LINES', 25) - 1
        sys.stdout.write(join(lines[:inc], '\n') + '\n')
        while lines[r:]:
            sys.stdout.write('-- more --')
            sys.stdout.flush()
            c = getchar()

            if c in ['q', 'Q']:
                sys.stdout.write('\r          \r')
                break
            elif c in ['\r', '\n']:
                sys.stdout.write('\r          \r' + lines[r] + '\n')
                r = r + 1
                continue
            if c in ['b', 'B', '\x1b']:
                r = r - inc - inc
                if r < 0: r = 0
            sys.stdout.write('\n' + join(lines[r:r+inc], '\n') + '\n')
            r = r + inc

    finally:
        if tty:
            tty.tcsetattr(fd, tty.TCSAFLUSH, old)

def plainpager(text):
    """Simply print unformatted text.  This is the ultimate fallback."""
    sys.stdout.write(plain(text))

def describe(thing):
    """Produce a short description of the given thing."""
    if inspect.ismodule(thing):
        if thing.__name__ in sys.builtin_module_names:
            return 'built-in module ' + thing.__name__
        if hasattr(thing, '__path__'):
            return 'package ' + thing.__name__
        else:
            return 'module ' + thing.__name__
    if inspect.isbuiltin(thing):
        return 'built-in function ' + thing.__name__
    if inspect.isclass(thing):
        return 'class ' + thing.__name__
    if inspect.isfunction(thing):
        return 'function ' + thing.__name__
    if inspect.ismethod(thing):
        return 'method ' + thing.__name__
    if type(thing) is types.InstanceType:
        return 'instance of ' + thing.__class__.__name__
    return type(thing).__name__

def locate(path, forceload=0):
    """Locate an object by name or dotted path, importing as necessary."""
    parts = split(path, '.')
    module, n = None, 0
    while n < len(parts):
        nextmodule = safeimport(join(parts[:n+1], '.'), forceload)
        if nextmodule: module, n = nextmodule, n + 1
        else: break
    if module:
        object = module
        for part in parts[n:]:
            try: object = getattr(object, part)
            except AttributeError: return None
        return object
    else:
        import __builtin__
        if hasattr(__builtin__, path):
            return getattr(__builtin__, path)

# --------------------------------------- interactive interpreter interface

text = TextDoc()
html = HTMLDoc()

def doc(thing, title='Python Library Documentation: %s', forceload=0):
    """Display text documentation, given an object or a path to an object."""
    suffix, name = '', None
    if type(thing) is type(''):
        try:
            object = locate(thing, forceload)
        except ErrorDuringImport, value:
            print value
            return
        if not object:
            print 'no Python documentation found for %s' % repr(thing)
            return
        parts = split(thing, '.')
        if len(parts) > 1: suffix = ' in ' + join(parts[:-1], '.')
        name = parts[-1]
        thing = object

    desc = describe(thing)
    module = inspect.getmodule(thing)
    if not suffix and module and module is not thing:
        suffix = ' in module ' + module.__name__
    pager(title % (desc + suffix) + '\n\n' + text.document(thing, name))

def writedoc(key, forceload=0):
    """Write HTML documentation to a file in the current directory."""
    try:
        object = locate(key, forceload)
    except ErrorDuringImport, value:
        print value
    else:
        if object:
            page = html.page(describe(object),
                             html.document(object, object.__name__))
            file = open(key + '.html', 'w')
            file.write(page)
            file.close()
            print 'wrote', key + '.html'
        else:
            print 'no Python documentation found for %s' % repr(key)

def writedocs(dir, pkgpath='', done=None):
    """Write out HTML documentation for all modules in a directory tree."""
    if done is None: done = {}
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if ispackage(path):
            writedocs(path, pkgpath + file + '.', done)
        elif os.path.isfile(path):
            modname = inspect.getmodulename(path)
            if modname:
                modname = pkgpath + modname
                if not done.has_key(modname):
                    done[modname] = 1
                    writedoc(modname)

class Helper:
    keywords = {
        'and': 'BOOLEAN',
        'assert': ('ref/assert', ''),
        'break': ('ref/break', 'while for'),
        'class': ('ref/class', 'CLASSES SPECIALMETHODS'),
        'continue': ('ref/continue', 'while for'),
        'def': ('ref/function', ''),
        'del': ('ref/del', 'BASICMETHODS'),
        'elif': 'if',
        'else': ('ref/if', 'while for'),
        'except': 'try',
        'exec': ('ref/exec', ''),
        'finally': 'try',
        'for': ('ref/for', 'break continue while'),
        'from': 'import',
        'global': ('ref/global', 'NAMESPACES'),
        'if': ('ref/if', 'TRUTHVALUE'),
        'import': ('ref/import', 'MODULES'),
        'in': ('ref/comparisons', 'SEQUENCEMETHODS2'),
        'is': 'COMPARISON',
        'lambda': ('ref/lambda', 'FUNCTIONS'),
        'not': 'BOOLEAN',
        'or': 'BOOLEAN',
        'pass': 'PASS',
        'print': ('ref/print', ''),
        'raise': ('ref/raise', 'EXCEPTIONS'),
        'return': ('ref/return', 'FUNCTIONS'),
        'try': ('ref/try', 'EXCEPTIONS'),
        'while': ('ref/while', 'break continue if TRUTHVALUE'),
    }

    topics = {
        'TYPES': ('ref/types', 'STRINGS UNICODE NUMBERS SEQUENCES MAPPINGS FUNCTIONS CLASSES MODULES FILES inspect'),
        'STRINGS': ('ref/strings', 'str UNICODE SEQUENCES STRINGMETHODS FORMATTING TYPES'),
        'STRINGMETHODS': ('lib/string-methods', 'STRINGS FORMATTING'),
        'FORMATTING': ('lib/typesseq-strings', 'OPERATORS'),
        'UNICODE': ('ref/unicode', 'encodings unicode TYPES STRING'),
        'NUMBERS': ('ref/numbers', 'INTEGER FLOAT COMPLEX TYPES'),
        'INTEGER': ('ref/integers', 'int range'),
        'FLOAT': ('ref/floating', 'float math'),
        'COMPLEX': ('ref/imaginary', 'complex cmath'),
        'SEQUENCES': ('lib/typesseq', 'STRINGMETHODS FORMATTING xrange LISTS'),
        'MAPPINGS': 'DICTIONARIES',
        'FUNCTIONS': ('lib/typesfunctions', 'def TYPES'),
        'METHODS': ('lib/typesmethods', 'class def CLASSES TYPES'),
        'CODEOBJECTS': ('lib/bltin-code-objects', 'compile FUNCTIONS TYPES'),
        'TYPEOBJECTS': ('lib/bltin-type-objects', 'types TYPES'),
        'FRAMEOBJECTS': 'TYPES',
        'TRACEBACKS': 'TYPES',
        'NONE': ('lib/bltin-null-object', ''),
        'ELLIPSIS': ('lib/bltin-ellipsis-object', 'SLICINGS'),
        'FILES': ('lib/bltin-file-objects', ''),
        'SPECIALATTRIBUTES': ('lib/specialattrs', ''),
        'CLASSES': ('ref/types', 'class SPECIALMETHODS PRIVATENAMES'),
        'MODULES': ('lib/typesmodules', 'import'),
        'PACKAGES': 'import',
        'EXPRESSIONS': ('ref/summary', 'lambda or and not in is BOOLEAN COMPARISON BITWISE SHIFTING BINARY FORMATTING POWER UNARY ATTRIBUTES SUBSCRIPTS SLICINGS CALLS TUPLES LISTS DICTIONARIES BACKQUOTES'),
        'OPERATORS': 'EXPRESSIONS',
        'PRECEDENCE': 'EXPRESSIONS',
        'OBJECTS': ('ref/objects', 'TYPES'),
        'SPECIALMETHODS': ('ref/specialnames', 'BASICMETHODS ATTRIBUTEMETHODS CALLABLEMETHODS SEQUENCEMETHODS1 MAPPINGMETHODS SEQUENCEMETHODS2 NUMBERMETHODS CLASSES'),
        'BASICMETHODS': ('ref/customization', 'cmp hash repr str SPECIALMETHODS'),
        'ATTRIBUTEMETHODS': ('ref/attribute-access', 'ATTRIBUTES SPECIALMETHODS'),
        'CALLABLEMETHODS': ('ref/callable-types', 'CALLS SPECIALMETHODS'),
        'SEQUENCEMETHODS1': ('ref/sequence-types', 'SEQUENCES SEQUENCEMETHODS2 SPECIALMETHODS'),
        'SEQUENCEMETHODS2': ('ref/sequence-methods', 'SEQUENCES SEQUENCEMETHODS1 SPECIALMETHODS'),
        'MAPPINGMETHODS': ('ref/sequence-types', 'MAPPINGS SPECIALMETHODS'),
        'NUMBERMETHODS': ('ref/numeric-types', 'NUMBERS AUGMENTEDASSIGNMENT SPECIALMETHODS'),
        'EXECUTION': ('ref/execframes', ''),
        'NAMESPACES': ('ref/execframes', 'global ASSIGNMENT DELETION'),
        'SCOPING': 'NAMESPACES',
        'FRAMES': 'NAMESPACES',
        'EXCEPTIONS': ('ref/exceptions', 'try except finally raise'),
        'COERCIONS': 'CONVERSIONS',
        'CONVERSIONS': ('ref/conversions', ''),
        'IDENTIFIERS': ('ref/identifiers', 'keywords SPECIALIDENTIFIERS'),
        'SPECIALIDENTIFIERS': ('ref/id-classes', ''),
        'PRIVATENAMES': ('ref/atom-identifiers', ''),
        'LITERALS': ('ref/atom-literals', 'STRINGS BACKQUOTES NUMBERS TUPLELITERALS LISTLITERALS DICTIONARYLITERALS'),
        'TUPLES': 'SEQUENCES',
        'TUPLELITERALS': ('ref/exprlists', 'TUPLES LITERALS'),
        'LISTS': ('lib/typesseq-mutable', 'LISTLITERALS'),
        'LISTLITERALS': ('ref/lists', 'LISTS LITERALS'),
        'DICTIONARIES': ('lib/typesmapping', 'DICTIONARYLITERALS'),
        'DICTIONARYLITERALS': ('ref/dict', 'DICTIONARIES LITERALS'),
        'BACKQUOTES': ('ref/string-conversions', 'repr str STRINGS LITERALS'),
        'ATTRIBUTES': ('ref/attribute-references', 'getattr hasattr setattr ATTRIBUTEMETHODS'),
        'SUBSCRIPTS': ('ref/subscriptions', 'SEQUENCEMETHODS1'),
        'SLICINGS': ('ref/slicings', 'SEQUENCEMETHODS2'),
        'CALLS': ('ref/calls', 'EXPRESSIONS'),
        'POWER': ('ref/power', 'EXPRESSIONS'),
        'UNARY': ('ref/unary', 'EXPRESSIONS'),
        'BINARY': ('ref/binary', 'EXPRESSIONS'),
        'SHIFTING': ('ref/shifting', 'EXPRESSIONS'),
        'BITWISE': ('ref/bitwise', 'EXPRESSIONS'),
        'COMPARISON': ('ref/comparisons', 'EXPRESSIONS BASICMETHODS'),
        'BOOLEAN': ('ref/lambda', 'EXPRESSIONS TRUTHVALUE'),
        'ASSERTION': 'assert',
        'ASSIGNMENT': ('ref/assignment', 'AUGMENTEDASSIGNMENT'),
        'AUGMENTEDASSIGNMENT': ('ref/augassign', 'NUMBERMETHODS'),
        'DELETION': 'del',
        'PRINTING': 'print',
        'RETURNING': 'return',
        'IMPORTING': 'import',
        'CONDITIONAL': 'if',
        'LOOPING': ('ref/compound', 'for while break continue'),
        'TRUTHVALUE': ('lib/truth', 'if while and or not BASICMETHODS'),
        'DEBUGGING': ('lib/module-pdb', 'pdb'),
    }

    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.docdir = None
        execdir = os.path.dirname(sys.executable)
        homedir = os.environ.get('PYTHONHOME')
        for dir in [os.environ.get('PYTHONDOCS'),
                    homedir and os.path.join(homedir, 'doc'),
                    os.path.join(execdir, 'doc'),
                    '/usr/doc/python-docs-' + split(sys.version)[0],
                    '/usr/doc/python-' + split(sys.version)[0],
                    '/usr/doc/python-docs-' + sys.version[:3],
                    '/usr/doc/python-' + sys.version[:3]]:
            if dir and os.path.isdir(os.path.join(dir, 'lib')):
                self.docdir = dir

    def __repr__(self):
        if inspect.stack()[1][3] == '?':
            self()
            return ''
        return '<pydoc.Helper instance>'

    def __call__(self, request=None):
        if request is not None:
            self.help(request)
        else:
            self.intro()
            self.interact()
            self.output.write('''
You are now leaving help and returning to the Python interpreter.
If you want to ask for help on a particular object directly from the
interpreter, you can type "help(object)".  Executing "help('string')"
has the same effect as typing a particular string at the help> prompt.
''')

    def interact(self):
        self.output.write('\n')
        while 1:
            self.output.write('help> ')
            self.output.flush()
            try:
                request = self.input.readline()
                if not request: break
            except KeyboardInterrupt: break
            request = strip(replace(request, '"', '', "'", ''))
            if lower(request) in ['q', 'quit']: break
            self.help(request)

    def help(self, request):
        if type(request) is type(''):
            if request == 'help': self.intro()
            elif request == 'keywords': self.listkeywords()
            elif request == 'topics': self.listtopics()
            elif request == 'modules': self.listmodules()
            elif request[:8] == 'modules ':
                self.listmodules(split(request)[1])
            elif self.keywords.has_key(request): self.showtopic(request)
            elif self.topics.has_key(request): self.showtopic(request)
            elif request: doc(request, 'Help on %s:')
        elif isinstance(request, Helper): self()
        else: doc(request, 'Help on %s:')
        self.output.write('\n')

    def intro(self):
        self.output.write('''
Welcome to Python %s!  This is the online help utility.

If this is your first time using Python, you should definitely check out
the tutorial on the Internet at http://www.python.org/doc/tut/.

Enter the name of any module, keyword, or topic to get help on writing
Python programs and using Python modules.  To quit this help utility and
return to the interpreter, just type "quit".

To get a list of available modules, keywords, or topics, type "modules",
"keywords", or "topics".  Each module also comes with a one-line summary
of what it does; to list the modules whose summaries contain a given word
such as "spam", type "modules spam".
''' % sys.version[:3])

    def list(self, items, columns=4, width=80):
        items = items[:]
        items.sort()
        colw = width / columns
        rows = (len(items) + columns - 1) / columns
        for row in range(rows):
            for col in range(columns):
                i = col * rows + row
                if i < len(items):
                    self.output.write(items[i])
                    if col < columns - 1:
                        self.output.write(' ' + ' ' * (colw-1 - len(items[i])))
            self.output.write('\n')

    def listkeywords(self):
        self.output.write('''
Here is a list of the Python keywords.  Enter any keyword to get more help.

''')
        self.list(self.keywords.keys())

    def listtopics(self):
        self.output.write('''
Here is a list of available topics.  Enter any topic name to get more help.

''')
        self.list(self.topics.keys())

    def showtopic(self, topic):
        if not self.docdir:
            self.output.write('''
Sorry, topic and keyword documentation is not available because the Python
HTML documentation files could not be found.  If you have installed them,
please set the environment variable PYTHONDOCS to indicate their location.
''')
            return
        target = self.topics.get(topic, self.keywords.get(topic))
        if not target:
            self.output.write('no documentation found for %s\n' % repr(topic))
            return
        if type(target) is type(''):
            return self.showtopic(target)

        filename, xrefs = target
        filename = self.docdir + '/' + filename + '.html'
        try:
            file = open(filename)
        except:
            self.output.write('could not read docs from %s\n' % filename)
            return

        divpat = re.compile('<div[^>]*navigat.*?</div.*?>', re.I | re.S)
        addrpat = re.compile('<address.*?>.*?</address.*?>', re.I | re.S)
        document = re.sub(addrpat, '', re.sub(divpat, '', file.read()))
        file.close()

        import htmllib, formatter, StringIO
        buffer = StringIO.StringIO()
        parser = htmllib.HTMLParser(
            formatter.AbstractFormatter(formatter.DumbWriter(buffer)))
        parser.start_table = parser.do_p
        parser.end_table = lambda parser=parser: parser.do_p({})
        parser.start_tr = parser.do_br
        parser.start_td = parser.start_th = lambda a, b=buffer: b.write('\t')
        parser.feed(document)
        buffer = replace(buffer.getvalue(), '\xa0', ' ', '\n', '\n  ')
        pager('  ' + strip(buffer) + '\n')
        if xrefs:
            buffer = StringIO.StringIO()
            formatter.DumbWriter(buffer).send_flowing_data(
                'Related help topics: ' + join(split(xrefs), ', ') + '\n')
            self.output.write('\n%s\n' % buffer.getvalue())

    def listmodules(self, key=''):
        if key:
            self.output.write('''
Here is a list of matching modules.  Enter any module name to get more help.

''')
            apropos(key)
        else:
            self.output.write('''
Please wait a moment while I gather a list of all available modules...

''')
            modules = {}
            def callback(path, modname, desc, modules=modules):
                if modname and modname[-9:] == '.__init__':
                    modname = modname[:-9] + ' (package)'
                if find(modname, '.') < 0:
                    modules[modname] = 1
            ModuleScanner().run(callback)
            self.list(modules.keys())
            self.output.write('''
Enter any module name to get more help.  Or, type "modules spam" to search
for modules whose descriptions contain the word "spam".
''')

help = Helper(sys.stdin, sys.stdout)

class Scanner:
    """A generic tree iterator."""
    def __init__(self, roots, children, descendp):
        self.roots = roots[:]
        self.state = []
        self.children = children
        self.descendp = descendp

    def next(self):
        if not self.state:
            if not self.roots:
                return None
            root = self.roots.pop(0)
            self.state = [(root, self.children(root))]
        node, children = self.state[-1]
        if not children:
            self.state.pop()
            return self.next()
        child = children.pop(0)
        if self.descendp(child):
            self.state.append((child, self.children(child)))
        return child

class ModuleScanner(Scanner):
    """An interruptible scanner that searches module synopses."""
    def __init__(self):
        roots = map(lambda dir: (dir, ''), pathdirs())
        Scanner.__init__(self, roots, self.submodules, self.isnewpackage)
        self.inodes = map(lambda (dir, pkg): os.stat(dir)[1], roots)

    def submodules(self, (dir, package)):
        children = []
        for file in os.listdir(dir):
            path = os.path.join(dir, file)
            if ispackage(path):
                children.append((path, package + (package and '.') + file))
            else:
                children.append((path, package))
        children.sort() # so that spam.py comes before spam.pyc or spam.pyo
        return children

    def isnewpackage(self, (dir, package)):
        inode = os.path.exists(dir) and os.stat(dir)[1]
        if not (os.path.islink(dir) and inode in self.inodes):
            self.inodes.append(inode) # detect circular symbolic links
            return ispackage(dir)

    def run(self, callback, key=None, completer=None):
        if key: key = lower(key)
        self.quit = 0
        seen = {}

        for modname in sys.builtin_module_names:
            if modname != '__main__':
                seen[modname] = 1
                if key is None:
                    callback(None, modname, '')
                else:
                    desc = split(__import__(modname).__doc__ or '', '\n')[0]
                    if find(lower(modname + ' - ' + desc), key) >= 0:
                        callback(None, modname, desc)

        while not self.quit:
            node = self.next()
            if not node: break
            path, package = node
            modname = inspect.getmodulename(path)
            if os.path.isfile(path) and modname:
                modname = package + (package and '.') + modname
                if not seen.has_key(modname):
                    seen[modname] = 1 # if we see spam.py, skip spam.pyc
                    if key is None:
                        callback(path, modname, '')
                    else:
                        desc = synopsis(path) or ''
                        if find(lower(modname + ' - ' + desc), key) >= 0:
                            callback(path, modname, desc)
        if completer: completer()

def apropos(key):
    """Print all the one-line module summaries that contain a substring."""
    def callback(path, modname, desc):
        if modname[-9:] == '.__init__':
            modname = modname[:-9] + ' (package)'
        print modname, desc and '- ' + desc
    try: import warnings
    except ImportError: pass
    else: warnings.filterwarnings('ignore') # ignore problems during import
    ModuleScanner().run(callback, key)

# --------------------------------------------------- web browser interface

def serve(port, callback=None, completer=None):
    import BaseHTTPServer, mimetools, select

    # Patch up mimetools.Message so it doesn't break if rfc822 is reloaded.
    class Message(mimetools.Message):
        def __init__(self, fp, seekable=1):
            Message = self.__class__
            Message.__bases__[0].__bases__[0].__init__(self, fp, seekable)
            self.encodingheader = self.getheader('content-transfer-encoding')
            self.typeheader = self.getheader('content-type')
            self.parsetype()
            self.parseplist()

    class DocHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def send_document(self, title, contents):
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(html.page(title, contents))
            except IOError: pass

        def do_GET(self):
            path = self.path
            if path[-5:] == '.html': path = path[:-5]
            if path[:1] == '/': path = path[1:]
            if path and path != '.':
                try:
                    obj = locate(path, forceload=1)
                except ErrorDuringImport, value:
                    self.send_document(path, html.escape(str(value)))
                    return
                if obj:
                    self.send_document(describe(obj), html.document(obj, path))
                else:
                    self.send_document(path,
'no Python documentation found for %s' % repr(path))
            else:
                heading = html.heading(
'<big><big><strong>Python: Index of Modules</strong></big></big>',
'#ffffff', '#7799ee')
                def bltinlink(name):
                    return '<a href="%s.html">%s</a>' % (name, name)
                names = filter(lambda x: x != '__main__',
                               sys.builtin_module_names)
                contents = html.multicolumn(names, bltinlink)
                indices = ['<p>' + html.bigsection(
                    'Built-in Modules', '#ffffff', '#ee77aa', contents)]

                seen = {}
                for dir in pathdirs():
                    indices.append(html.index(dir, seen))
                contents = heading + join(indices) + '''<p align=right>
<small><small><font color="#909090" face="helvetica, arial"><strong>
pydoc</strong> by Ka-Ping Yee &lt;ping@lfw.org&gt;</font></small></small>'''
                self.send_document('Index of Modules', contents)

        def log_message(self, *args): pass

    class DocServer(BaseHTTPServer.HTTPServer):
        def __init__(self, port, callback):
            host = (sys.platform == 'mac') and '127.0.0.1' or 'localhost'
            self.address = ('', port)
            self.url = 'http://%s:%d/' % (host, port)
            self.callback = callback
            self.base.__init__(self, self.address, self.handler)

        def serve_until_quit(self):
            import select
            self.quit = 0
            while not self.quit:
                rd, wr, ex = select.select([self.socket.fileno()], [], [], 1)
                if rd: self.handle_request()

        def server_activate(self):
            self.base.server_activate(self)
            if self.callback: self.callback(self)

    DocServer.base = BaseHTTPServer.HTTPServer
    DocServer.handler = DocHandler
    DocHandler.MessageClass = Message
    try:
        try:
            DocServer(port, callback).serve_until_quit()
        except (KeyboardInterrupt, select.error):
            pass
    finally:
        if completer: completer()

# ----------------------------------------------------- graphical interface

def gui():
    """Graphical interface (starts web server and pops up a control window)."""
    class GUI:
        def __init__(self, window, port=7464):
            self.window = window
            self.server = None
            self.scanner = None

            import Tkinter
            self.server_frm = Tkinter.Frame(window)
            self.title_lbl = Tkinter.Label(self.server_frm,
                text='Starting server...\n ')
            self.open_btn = Tkinter.Button(self.server_frm,
                text='open browser', command=self.open, state='disabled')
            self.quit_btn = Tkinter.Button(self.server_frm,
                text='quit serving', command=self.quit, state='disabled')

            self.search_frm = Tkinter.Frame(window)
            self.search_lbl = Tkinter.Label(self.search_frm, text='Search for')
            self.search_ent = Tkinter.Entry(self.search_frm)
            self.search_ent.bind('<Return>', self.search)
            self.stop_btn = Tkinter.Button(self.search_frm,
                text='stop', pady=0, command=self.stop, state='disabled')
            if sys.platform == 'win32':
                # Trying to hide and show this button crashes under Windows.
                self.stop_btn.pack(side='right')

            self.window.title('pydoc')
            self.window.protocol('WM_DELETE_WINDOW', self.quit)
            self.title_lbl.pack(side='top', fill='x')
            self.open_btn.pack(side='left', fill='x', expand=1)
            self.quit_btn.pack(side='right', fill='x', expand=1)
            self.server_frm.pack(side='top', fill='x')

            self.search_lbl.pack(side='left')
            self.search_ent.pack(side='right', fill='x', expand=1)
            self.search_frm.pack(side='top', fill='x')
            self.search_ent.focus_set()

            font = ('helvetica', sys.platform == 'win32' and 8 or 10)
            self.result_lst = Tkinter.Listbox(window, font=font, height=6)
            self.result_lst.bind('<Button-1>', self.select)
            self.result_lst.bind('<Double-Button-1>', self.goto)
            self.result_scr = Tkinter.Scrollbar(window,
                orient='vertical', command=self.result_lst.yview)
            self.result_lst.config(yscrollcommand=self.result_scr.set)

            self.result_frm = Tkinter.Frame(window)
            self.goto_btn = Tkinter.Button(self.result_frm,
                text='go to selected', command=self.goto)
            self.hide_btn = Tkinter.Button(self.result_frm,
                text='hide results', command=self.hide)
            self.goto_btn.pack(side='left', fill='x', expand=1)
            self.hide_btn.pack(side='right', fill='x', expand=1)

            self.window.update()
            self.minwidth = self.window.winfo_width()
            self.minheight = self.window.winfo_height()
            self.bigminheight = (self.server_frm.winfo_reqheight() +
                                 self.search_frm.winfo_reqheight() +
                                 self.result_lst.winfo_reqheight() +
                                 self.result_frm.winfo_reqheight())
            self.bigwidth, self.bigheight = self.minwidth, self.bigminheight
            self.expanded = 0
            self.window.wm_geometry('%dx%d' % (self.minwidth, self.minheight))
            self.window.wm_minsize(self.minwidth, self.minheight)

            import threading
            threading.Thread(
                target=serve, args=(port, self.ready, self.quit)).start()

        def ready(self, server):
            self.server = server
            self.title_lbl.config(
                text='Python documentation server at\n' + server.url)
            self.open_btn.config(state='normal')
            self.quit_btn.config(state='normal')

        def open(self, event=None, url=None):
            url = url or self.server.url
            try:
                import webbrowser
                webbrowser.open(url)
            except ImportError: # pre-webbrowser.py compatibility
                if sys.platform == 'win32':
                    os.system('start "%s"' % url)
                elif sys.platform == 'mac':
                    try: import ic
                    except ImportError: pass
                    else: ic.launchurl(url)
                else:
                    rc = os.system('netscape -remote "openURL(%s)" &' % url)
                    if rc: os.system('netscape "%s" &' % url)

        def quit(self, event=None):
            if self.server:
                self.server.quit = 1
            self.window.quit()

        def search(self, event=None):
            key = self.search_ent.get()
            self.stop_btn.pack(side='right')
            self.stop_btn.config(state='normal')
            self.search_lbl.config(text='Searching for "%s"...' % key)
            self.search_ent.forget()
            self.search_lbl.pack(side='left')
            self.result_lst.delete(0, 'end')
            self.goto_btn.config(state='disabled')
            self.expand()

            import threading
            if self.scanner:
                self.scanner.quit = 1
            self.scanner = ModuleScanner()
            threading.Thread(target=self.scanner.run,
                             args=(self.update, key, self.done)).start()

        def update(self, path, modname, desc):
            if modname[-9:] == '.__init__':
                modname = modname[:-9] + ' (package)'
            self.result_lst.insert('end',
                modname + ' - ' + (desc or '(no description)'))

        def stop(self, event=None):
            if self.scanner:
                self.scanner.quit = 1
                self.scanner = None

        def done(self):
            self.scanner = None
            self.search_lbl.config(text='Search for')
            self.search_lbl.pack(side='left')
            self.search_ent.pack(side='right', fill='x', expand=1)
            if sys.platform != 'win32': self.stop_btn.forget()
            self.stop_btn.config(state='disabled')

        def select(self, event=None):
            self.goto_btn.config(state='normal')

        def goto(self, event=None):
            selection = self.result_lst.curselection()
            if selection:
                modname = split(self.result_lst.get(selection[0]))[0]
                self.open(url=self.server.url + modname + '.html')

        def collapse(self):
            if not self.expanded: return
            self.result_frm.forget()
            self.result_scr.forget()
            self.result_lst.forget()
            self.bigwidth = self.window.winfo_width()
            self.bigheight = self.window.winfo_height()
            self.window.wm_geometry('%dx%d' % (self.minwidth, self.minheight))
            self.window.wm_minsize(self.minwidth, self.minheight)
            self.expanded = 0

        def expand(self):
            if self.expanded: return
            self.result_frm.pack(side='bottom', fill='x')
            self.result_scr.pack(side='right', fill='y')
            self.result_lst.pack(side='top', fill='both', expand=1)
            self.window.wm_geometry('%dx%d' % (self.bigwidth, self.bigheight))
            self.window.wm_minsize(self.minwidth, self.bigminheight)
            self.expanded = 1

        def hide(self, event=None):
            self.stop()
            self.collapse()

    import Tkinter
    try:
        gui = GUI(Tkinter.Tk())
        Tkinter.mainloop()
    except KeyboardInterrupt:
        pass

# -------------------------------------------------- command-line interface

def ispath(x):
    return type(x) is types.StringType and find(x, os.sep) >= 0

def cli():
    """Command-line interface (looks at sys.argv to decide what to do)."""
    import getopt
    class BadUsage: pass

    # Scripts don't get the current directory in their path by default.
    scriptdir = os.path.dirname(sys.argv[0])
    if scriptdir in sys.path:
        sys.path.remove(scriptdir)
    sys.path.insert(0, '.')

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'gk:p:w')
        writing = 0

        for opt, val in opts:
            if opt == '-g':
                gui()
                return
            if opt == '-k':
                apropos(val)
                return
            if opt == '-p':
                try:
                    port = int(val)
                except ValueError:
                    raise BadUsage
                def ready(server):
                    print 'pydoc server ready at %s' % server.url
                def stopped():
                    print 'pydoc server stopped'
                serve(port, ready, stopped)
                return
            if opt == '-w':
                writing = 1

        if not args: raise BadUsage
        for arg in args:
            try:
                if ispath(arg) and os.path.isfile(arg):
                    arg = importfile(arg)
                if writing:
                    if ispath(arg) and os.path.isdir(arg):
                        writedocs(arg)
                    else:
                        writedoc(arg)
                else:
                    doc(arg)
            except ErrorDuringImport, value:
                print value

    except (getopt.error, BadUsage):
        cmd = sys.argv[0]
        print """pydoc - the Python documentation tool

%s <name> ...
    Show text documentation on something.  <name> may be the name of a
    function, module, or package, or a dotted reference to a class or
    function within a module or module in a package.  If <name> contains
    a '%s', it is used as the path to a Python source file to document.

%s -k <keyword>
    Search for a keyword in the synopsis lines of all available modules.

%s -p <port>
    Start an HTTP server on the given port on the local machine.

%s -g
    Pop up a graphical interface for finding and serving documentation.

%s -w <name> ...
    Write out the HTML documentation for a module to a file in the current
    directory.  If <name> contains a '%s', it is treated as a filename; if
    it names a directory, documentation is written for all the contents.
""" % (cmd, os.sep, cmd, cmd, cmd, cmd, os.sep)

if __name__ == '__main__': cli()
