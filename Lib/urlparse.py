"""Parse (absolute and relative) URLs.

urlparse module is based upon the following RFC specifications.

RFC 3986 (STD66): "Uniform Resource Identifiers" by T. Berners-Lee, R. Fielding
and L.  Masinter, January 2005.

RFC2396:  "Uniform Resource Identifiers (URI)": Generic Syntax by T.
Berners-Lee, R. Fielding, and L. Masinter, August 1998.

RFC2368: "The mailto URL scheme", by P.Hoffman , L Masinter, J. Zwinski, July 1998.

RFC 1808: "Relative Uniform Resource Locators", by R. Fielding, UC Irvine, June
1995.

RFC1738: "Uniform Resource Locators (URL)" by T. Berners-Lee, L. Masinter, M.
McCahill, December 1994

RFC 3986 is considered the current standard and any changes to urlparse module
should conform to this.  urlparse module is not entirely compliant with this.
The defacto scenarios of parsing are considered sometimes and for backward
compatiblity purposes, older RFC uses of parsing are retained. The testcases in
test_urlparse.py provides a good indicator of parsing behavior.

"""

__all__ = ["urlparse", "urlunparse", "urljoin", "urldefrag",
           "urlsplit", "urlunsplit", "parse_qs", "parse_qsl"]

# A classification of schemes ('' means apply by default)
uses_relative = ['ftp', 'http', 'gopher', 'nntp', 'imap',
                 'wais', 'file', 'https', 'shttp', 'mms',
                 'prospero', 'rtsp', 'rtspu', '', 'sftp']
uses_netloc = ['ftp', 'http', 'gopher', 'nntp', 'telnet',
               'imap', 'wais', 'file', 'mms', 'https', 'shttp',
               'snews', 'prospero', 'rtsp', 'rtspu', 'rsync', '',
               'svn', 'svn+ssh', 'sftp']
non_hierarchical = ['gopher', 'hdl', 'mailto', 'news',
                    'telnet', 'wais', 'imap', 'snews', 'sip', 'sips']
uses_params = ['ftp', 'hdl', 'prospero', 'http', 'imap',
               'https', 'shttp', 'rtsp', 'rtspu', 'sip', 'sips',
               'mms', '', 'sftp']
uses_query = ['http', 'wais', 'imap', 'https', 'shttp', 'mms',
              'gopher', 'rtsp', 'rtspu', 'sip', 'sips', '']
uses_fragment = ['ftp', 'hdl', 'http', 'gopher', 'news',
                 'nntp', 'wais', 'https', 'shttp', 'snews',
                 'file', 'prospero', '']

# Characters valid in scheme names
scheme_chars = ('abcdefghijklmnopqrstuvwxyz'
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                '0123456789'
                '+-.')

MAX_CACHE_SIZE = 20
_parse_cache = {}

def clear_cache():
    """Clear the parse cache."""
    _parse_cache.clear()


class ResultMixin(object):
    """Shared methods for the parsed result objects."""

    @property
    def username(self):
        netloc = self.netloc
        if "@" in netloc:
            userinfo = netloc.rsplit("@", 1)[0]
            if ":" in userinfo:
                userinfo = userinfo.split(":", 1)[0]
            return userinfo
        return None

    @property
    def password(self):
        netloc = self.netloc
        if "@" in netloc:
            userinfo = netloc.rsplit("@", 1)[0]
            if ":" in userinfo:
                return userinfo.split(":", 1)[1]
        return None

    @property
    def hostname(self):
        netloc = self.netloc
        if "@" in netloc:
            netloc = netloc.rsplit("@", 1)[1]
        if ":" in netloc:
            netloc = netloc.split(":", 1)[0]
        return netloc.lower() or None

    @property
    def port(self):
        netloc = self.netloc
        if "@" in netloc:
            netloc = netloc.rsplit("@", 1)[1]
        if ":" in netloc:
            port = netloc.split(":", 1)[1]
            return int(port, 10)
        return None

from collections import namedtuple

class SplitResult(namedtuple('SplitResult', 'scheme netloc path query fragment'), ResultMixin):

    __slots__ = ()

    def geturl(self):
        return urlunsplit(self)


class ParseResult(namedtuple('ParseResult', 'scheme netloc path params query fragment'), ResultMixin):

    __slots__ = ()

    def geturl(self):
        return urlunparse(self)


def urlparse(url, scheme='', allow_fragments=True):
    """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    Return a 6-tuple: (scheme, netloc, path, params, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes."""
    tuple = urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = tuple
    if scheme in uses_params and ';' in url:
        url, params = _splitparams(url)
    else:
        params = ''
    return ParseResult(scheme, netloc, url, params, query, fragment)

def _splitparams(url):
    if '/'  in url:
        i = url.find(';', url.rfind('/'))
        if i < 0:
            return url, ''
    else:
        i = url.find(';')
    return url[:i], url[i+1:]

def _splitnetloc(url, start=0):
    delim = len(url)   # position of end of domain part of url, default is end
    for c in '/?#':    # look for delimiters; the order is NOT important
        wdelim = url.find(c, start)        # find first of this delim
        if wdelim >= 0:                    # if found
            delim = min(delim, wdelim)     # use earliest delim position
    return url[start:delim], url[delim:]   # return (domain, rest)

def urlsplit(url, scheme='', allow_fragments=True):
    """Parse a URL into 5 components:
    <scheme>://<netloc>/<path>?<query>#<fragment>
    Return a 5-tuple: (scheme, netloc, path, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes."""
    allow_fragments = bool(allow_fragments)
    key = url, scheme, allow_fragments, type(url), type(scheme)
    cached = _parse_cache.get(key, None)
    if cached:
        return cached
    if len(_parse_cache) >= MAX_CACHE_SIZE: # avoid runaway growth
        clear_cache()
    netloc = query = fragment = ''
    i = url.find(':')
    if i > 0:
        if url[:i] == 'http': # optimize the common case
            scheme = url[:i].lower()
            url = url[i+1:]
            if url[:2] == '//':
                netloc, url = _splitnetloc(url, 2)
            if allow_fragments and '#' in url:
                url, fragment = url.split('#', 1)
            if '?' in url:
                url, query = url.split('?', 1)
            v = SplitResult(scheme, netloc, url, query, fragment)
            _parse_cache[key] = v
            return v
        for c in url[:i]:
            if c not in scheme_chars:
                break
        else:
            scheme, url = url[:i].lower(), url[i+1:]

    if url[:2] == '//':
        netloc, url = _splitnetloc(url, 2)
    if allow_fragments and scheme in uses_fragment and '#' in url:
        url, fragment = url.split('#', 1)
    if scheme in uses_query and '?' in url:
        url, query = url.split('?', 1)
    v = SplitResult(scheme, netloc, url, query, fragment)
    _parse_cache[key] = v
    return v

def urlunparse(data):
    """Put a parsed URL back together again.  This may result in a
    slightly different, but equivalent URL, if the URL that was parsed
    originally had redundant delimiters, e.g. a ? with an empty query
    (the draft states that these are equivalent)."""
    scheme, netloc, url, params, query, fragment = data
    if params:
        url = "%s;%s" % (url, params)
    return urlunsplit((scheme, netloc, url, query, fragment))

def urlunsplit(data):
    scheme, netloc, url, query, fragment = data
    if netloc or (scheme and scheme in uses_netloc and url[:2] != '//'):
        if url and url[:1] != '/': url = '/' + url
        url = '//' + (netloc or '') + url
    if scheme:
        url = scheme + ':' + url
    if query:
        url = url + '?' + query
    if fragment:
        url = url + '#' + fragment
    return url

def urljoin(base, url, allow_fragments=True):
    """Join a base URL and a possibly relative URL to form an absolute
    interpretation of the latter."""
    if not base:
        return url
    if not url:
        return base
    bscheme, bnetloc, bpath, bparams, bquery, bfragment = \
            urlparse(base, '', allow_fragments)
    scheme, netloc, path, params, query, fragment = \
            urlparse(url, bscheme, allow_fragments)
    if scheme != bscheme or scheme not in uses_relative:
        return url
    if scheme in uses_netloc:
        if netloc:
            return urlunparse((scheme, netloc, path,
                               params, query, fragment))
        netloc = bnetloc
    if path[:1] == '/':
        return urlunparse((scheme, netloc, path,
                           params, query, fragment))
    if not path:
        path = bpath
        if not params:
            params = bparams
        else:
            path = path[:-1]
            return urlunparse((scheme, netloc, path,
                                params, query, fragment))
        if not query:
            query = bquery
        return urlunparse((scheme, netloc, path,
                           params, query, fragment))
    segments = bpath.split('/')[:-1] + path.split('/')
    # XXX The stuff below is bogus in various ways...
    if segments[-1] == '.':
        segments[-1] = ''
    while '.' in segments:
        segments.remove('.')
    while 1:
        i = 1
        n = len(segments) - 1
        while i < n:
            if (segments[i] == '..'
                and segments[i-1] not in ('', '..')):
                del segments[i-1:i+1]
                break
            i = i+1
        else:
            break
    if segments == ['', '..']:
        segments[-1] = ''
    elif len(segments) >= 2 and segments[-1] == '..':
        segments[-2:] = ['']
    return urlunparse((scheme, netloc, '/'.join(segments),
                       params, query, fragment))

def urldefrag(url):
    """Removes any existing fragment from URL.

    Returns a tuple of the defragmented URL and the fragment.  If
    the URL contained no fragments, the second element is the
    empty string.
    """
    if '#' in url:
        s, n, p, a, q, frag = urlparse(url)
        defrag = urlunparse((s, n, p, a, q, ''))
        return defrag, frag
    else:
        return url, ''

# unquote method for parse_qs and parse_qsl
# Cannot use directly from urllib as it would create circular reference.
# urllib uses urlparse methods ( urljoin)


_hexdig = '0123456789ABCDEFabcdef'
_hextochr = dict((a+b, chr(int(a+b,16))) for a in _hexdig for b in _hexdig)

def unquote(s):
    """unquote('abc%20def') -> 'abc def'."""
    res = s.split('%')
    for i in xrange(1, len(res)):
        item = res[i]
        try:
            res[i] = _hextochr[item[:2]] + item[2:]
        except KeyError:
            res[i] = '%' + item
        except UnicodeDecodeError:
            res[i] = unichr(int(item[:2], 16)) + item[2:]
    return "".join(res)

def parse_qs(qs, keep_blank_values=0, strict_parsing=0):
    """Parse a query given as a string argument.

        Arguments:

        qs: URL-encoded query string to be parsed

        keep_blank_values: flag indicating whether blank values in
            URL encoded queries should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.

        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.
    """
    dict = {}
    for name, value in parse_qsl(qs, keep_blank_values, strict_parsing):
        if name in dict:
            dict[name].append(value)
        else:
            dict[name] = [value]
    return dict

def parse_qsl(qs, keep_blank_values=0, strict_parsing=0):
    """Parse a query given as a string argument.

    Arguments:

    qs: URL-encoded query string to be parsed

    keep_blank_values: flag indicating whether blank values in
        URL encoded queries should be treated as blank strings.  A
        true value indicates that blanks should be retained as blank
        strings.  The default false value indicates that blank values
        are to be ignored and treated as if they were  not included.

    strict_parsing: flag indicating what to do with parsing errors. If
        false (the default), errors are silently ignored. If true,
        errors raise a ValueError exception.

    Returns a list, as G-d intended.
    """
    pairs = [s2 for s1 in qs.split('&') for s2 in s1.split(';')]
    r = []
    for name_value in pairs:
        if not name_value and not strict_parsing:
            continue
        nv = name_value.split('=', 1)
        if len(nv) != 2:
            if strict_parsing:
                raise ValueError, "bad query field: %r" % (name_value,)
            # Handle case of a control-name with no equal sign
            if keep_blank_values:
                nv.append('')
            else:
                continue
        if len(nv[1]) or keep_blank_values:
            name = unquote(nv[0].replace('+', ' '))
            value = unquote(nv[1].replace('+', ' '))
            r.append((name, value))

    return r


test_input = """
      http://a/b/c/d

      g:h        = <URL:g:h>
      http:g     = <URL:http://a/b/c/g>
      http:      = <URL:http://a/b/c/d>
      g          = <URL:http://a/b/c/g>
      ./g        = <URL:http://a/b/c/g>
      g/         = <URL:http://a/b/c/g/>
      /g         = <URL:http://a/g>
      //g        = <URL:http://g>
      ?y         = <URL:http://a/b/c/d?y>
      g?y        = <URL:http://a/b/c/g?y>
      g?y/./x    = <URL:http://a/b/c/g?y/./x>
      .          = <URL:http://a/b/c/>
      ./         = <URL:http://a/b/c/>
      ..         = <URL:http://a/b/>
      ../        = <URL:http://a/b/>
      ../g       = <URL:http://a/b/g>
      ../..      = <URL:http://a/>
      ../../g    = <URL:http://a/g>
      ../../../g = <URL:http://a/../g>
      ./../g     = <URL:http://a/b/g>
      ./g/.      = <URL:http://a/b/c/g/>
      /./g       = <URL:http://a/./g>
      g/./h      = <URL:http://a/b/c/g/h>
      g/../h     = <URL:http://a/b/c/h>
      http:g     = <URL:http://a/b/c/g>
      http:      = <URL:http://a/b/c/d>
      http:?y         = <URL:http://a/b/c/d?y>
      http:g?y        = <URL:http://a/b/c/g?y>
      http:g?y/./x    = <URL:http://a/b/c/g?y/./x>
"""

def test():
    import sys
    base = ''
    if sys.argv[1:]:
        fn = sys.argv[1]
        if fn == '-':
            fp = sys.stdin
        else:
            fp = open(fn)
    else:
        try:
            from cStringIO import StringIO
        except ImportError:
            from StringIO import StringIO
        fp = StringIO(test_input)
    for line in fp:
        words = line.split()
        if not words:
            continue
        url = words[0]
        parts = urlparse(url)
        print '%-10s : %s' % (url, parts)
        abs = urljoin(base, url)
        if not base:
            base = abs
        wrapped = '<URL:%s>' % abs
        print '%-10s = %s' % (url, wrapped)
        if len(words) == 3 and words[1] == '=':
            if wrapped != words[2]:
                print 'EXPECTED', words[2], '!!!!!!!!!!'

if __name__ == '__main__':
    test()
