#
# XML-RPC CLIENT LIBRARY
# $Id$
#
# an XML-RPC client interface for Python.
#
# the marshalling and response parser code can also be used to
# implement XML-RPC servers.
#
# Notes:
# this version is designed to work with Python 2.1 or newer.
#
# History:
# 1999-01-14 fl  Created
# 1999-01-15 fl  Changed dateTime to use localtime
# 1999-01-16 fl  Added Binary/base64 element, default to RPC2 service
# 1999-01-19 fl  Fixed array data element (from Skip Montanaro)
# 1999-01-21 fl  Fixed dateTime constructor, etc.
# 1999-02-02 fl  Added fault handling, handle empty sequences, etc.
# 1999-02-10 fl  Fixed problem with empty responses (from Skip Montanaro)
# 1999-06-20 fl  Speed improvements, pluggable parsers/transports (0.9.8)
# 2000-11-28 fl  Changed boolean to check the truth value of its argument
# 2001-02-24 fl  Added encoding/Unicode/SafeTransport patches
# 2001-02-26 fl  Added compare support to wrappers (0.9.9/1.0b1)
# 2001-03-28 fl  Make sure response tuple is a singleton
# 2001-03-29 fl  Don't require empty params element (from Nicholas Riley)
# 2001-06-10 fl  Folded in _xmlrpclib accelerator support (1.0b2)
# 2001-08-20 fl  Base xmlrpclib.Error on built-in Exception (from Paul Prescod)
# 2001-09-03 fl  Allow Transport subclass to override getparser
# 2001-09-10 fl  Lazy import of urllib, cgi, xmllib (20x import speedup)
# 2001-10-01 fl  Remove containers from memo cache when done with them
# 2001-10-01 fl  Use faster escape method (80% dumps speedup)
# 2001-10-02 fl  More dumps microtuning
# 2001-10-04 fl  Make sure import expat gets a parser (from Guido van Rossum)
# 2001-10-10 sm  Allow long ints to be passed as ints if they don't overflow
# 2001-10-17 sm  Test for int and long overflow (allows use on 64-bit systems)
# 2001-11-12 fl  Use repr() to marshal doubles (from Paul Felix)
# 2002-03-17 fl  Avoid buffered read when possible (from James Rucker)
# 2002-04-07 fl  Added pythondoc comments
# 2002-04-16 fl  Added __str__ methods to datetime/binary wrappers
# 2002-05-15 fl  Added error constants (from Andrew Kuchling)
# 2002-06-27 fl  Merged with Python CVS version
# 2002-10-22 fl  Added basic authentication (based on code from Phillip Eby)
# 2003-01-22 sm  Add support for the bool type
# 2003-02-27 gvr Remove apply calls
# 2003-04-24 sm  Use cStringIO if available
# 2003-04-25 ak  Add support for nil
# 2003-06-15 gn  Add support for time.struct_time
# 2003-07-12 gp  Correct marshalling of Faults
# 2003-10-31 mvl Add multicall support
# 2004-08-20 mvl Bump minimum supported Python version to 2.1
#
# Copyright (c) 1999-2002 by Secret Labs AB.
# Copyright (c) 1999-2002 by Fredrik Lundh.
#
# info@pythonware.com
# http://www.pythonware.com
#
# --------------------------------------------------------------------
# The XML-RPC client interface is
#
# Copyright (c) 1999-2002 by Secret Labs AB
# Copyright (c) 1999-2002 by Fredrik Lundh
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Secret Labs AB or the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# --------------------------------------------------------------------

#
# things to look into some day:

# TODO: sort out True/False/boolean issues for Python 2.3

"""
An XML-RPC client interface for Python.

The marshalling and response parser code can also be used to
implement XML-RPC servers.

Exported exceptions:

  Error          Base class for client errors
  ProtocolError  Indicates an HTTP protocol error
  ResponseError  Indicates a broken response package
  Fault          Indicates an XML-RPC fault package

Exported classes:

  ServerProxy    Represents a logical connection to an XML-RPC server

  MultiCall      Executor of boxcared xmlrpc requests
  Boolean        boolean wrapper to generate a "boolean" XML-RPC value
  DateTime       dateTime wrapper for an ISO 8601 string or time tuple or
                 localtime integer value to generate a "dateTime.iso8601"
                 XML-RPC value
  Binary         binary data wrapper

  SlowParser     Slow but safe standard parser (based on xmllib)
  Marshaller     Generate an XML-RPC params chunk from a Python data structure
  Unmarshaller   Unmarshal an XML-RPC response from incoming XML event message
  Transport      Handles an HTTP transaction to an XML-RPC server
  SafeTransport  Handles an HTTPS transaction to an XML-RPC server

Exported constants:

  True
  False

Exported functions:

  boolean        Convert any Python value to an XML-RPC boolean
  getparser      Create instance of the fastest available parser & attach
                 to an unmarshalling object
  dumps          Convert an argument tuple or a Fault instance to an XML-RPC
                 request (or response, if the methodresponse option is used).
  loads          Convert an XML-RPC packet to unmarshalled data plus a method
                 name (None if not present).
"""

import re, string, time, operator

from types import *

# --------------------------------------------------------------------
# Internal stuff

try:
    unicode
except NameError:
    unicode = None # unicode support not available

try:
    _bool_is_builtin = False.__class__.__name__ == "bool"
except NameError:
    _bool_is_builtin = 0

def _decode(data, encoding, is8bit=re.compile("[\x80-\xff]").search):
    # decode non-ascii string (if possible)
    if unicode and encoding and is8bit(data):
        data = unicode(data, encoding)
    return data

def escape(s, replace=string.replace):
    s = replace(s, "&", "&amp;")
    s = replace(s, "<", "&lt;")
    return replace(s, ">", "&gt;",)

if unicode:
    def _stringify(string):
        # convert to 7-bit ascii if possible
        try:
            return str(string)
        except UnicodeError:
            return string
else:
    def _stringify(string):
        return string

__version__ = "1.0.1"

# xmlrpc integer limits
MAXINT =  2L**31-1
MININT = -2L**31

# --------------------------------------------------------------------
# Error constants (from Dan Libby's specification at
# http://xmlrpc-epi.sourceforge.net/specs/rfc.fault_codes.php)

# Ranges of errors
PARSE_ERROR       = -32700
SERVER_ERROR      = -32600
APPLICATION_ERROR = -32500
SYSTEM_ERROR      = -32400
TRANSPORT_ERROR   = -32300

# Specific errors
NOT_WELLFORMED_ERROR  = -32700
UNSUPPORTED_ENCODING  = -32701
INVALID_ENCODING_CHAR = -32702
INVALID_XMLRPC        = -32600
METHOD_NOT_FOUND      = -32601
INVALID_METHOD_PARAMS = -32602
INTERNAL_ERROR        = -32603

# --------------------------------------------------------------------
# Exceptions

##
# Base class for all kinds of client-side errors.

class Error(Exception):
    """Base class for client errors."""
    def __str__(self):
        return repr(self)

##
# Indicates an HTTP-level protocol error.  This is raised by the HTTP
# transport layer, if the server returns an error code other than 200
# (OK).
#
# @param url The target URL.
# @param errcode The HTTP error code.
# @param errmsg The HTTP error message.
# @param headers The HTTP header dictionary.

class ProtocolError(Error):
    """Indicates an HTTP protocol error."""
    def __init__(self, url, errcode, errmsg, headers):
        Error.__init__(self)
        self.url = url
        self.errcode = errcode
        self.errmsg = errmsg
        self.headers = headers
    def __repr__(self):
        return (
            "<ProtocolError for %s: %s %s>" %
            (self.url, self.errcode, self.errmsg)
            )

##
# Indicates a broken XML-RPC response package.  This exception is
# raised by the unmarshalling layer, if the XML-RPC response is
# malformed.

class ResponseError(Error):
    """Indicates a broken response package."""
    pass

##
# Indicates an XML-RPC fault response package.  This exception is
# raised by the unmarshalling layer, if the XML-RPC response contains
# a fault string.  This exception can also used as a class, to
# generate a fault XML-RPC message.
#
# @param faultCode The XML-RPC fault code.
# @param faultString The XML-RPC fault string.

class Fault(Error):
    """Indicates an XML-RPC fault package."""
    def __init__(self, faultCode, faultString, **extra):
        Error.__init__(self)
        self.faultCode = faultCode
        self.faultString = faultString
    def __repr__(self):
        return (
            "<Fault %s: %s>" %
            (self.faultCode, repr(self.faultString))
            )

# --------------------------------------------------------------------
# Special values

##
# Wrapper for XML-RPC boolean values.  Use the xmlrpclib.True and
# xmlrpclib.False constants, or the xmlrpclib.boolean() function, to
# generate boolean XML-RPC values.
#
# @param value A boolean value.  Any true value is interpreted as True,
#              all other values are interpreted as False.

if _bool_is_builtin:
    boolean = Boolean = bool
    # to avoid breaking code which references xmlrpclib.{True,False}
    True, False = True, False
else:
    class Boolean:
        """Boolean-value wrapper.

        Use True or False to generate a "boolean" XML-RPC value.
        """

        def __init__(self, value = 0):
            self.value = operator.truth(value)

        def encode(self, out):
            out.write("<value><boolean>%d</boolean></value>\n" % self.value)

        def __cmp__(self, other):
            if isinstance(other, Boolean):
                other = other.value
            return cmp(self.value, other)

        def __repr__(self):
            if self.value:
                return "<Boolean True at %x>" % id(self)
            else:
                return "<Boolean False at %x>" % id(self)

        def __int__(self):
            return self.value

        def __nonzero__(self):
            return self.value

    True, False = Boolean(1), Boolean(0)

    ##
    # Map true or false value to XML-RPC boolean values.
    #
    # @def boolean(value)
    # @param value A boolean value.  Any true value is mapped to True,
    #              all other values are mapped to False.
    # @return xmlrpclib.True or xmlrpclib.False.
    # @see Boolean
    # @see True
    # @see False

    def boolean(value, _truefalse=(False, True)):
        """Convert any Python value to XML-RPC 'boolean'."""
        return _truefalse[operator.truth(value)]

##
# Wrapper for XML-RPC DateTime values.  This converts a time value to
# the format used by XML-RPC.
# <p>
# The value can be given as a string in the format
# "yyyymmddThh:mm:ss", as a 9-item time tuple (as returned by
# time.localtime()), or an integer value (as returned by time.time()).
# The wrapper uses time.localtime() to convert an integer to a time
# tuple.
#
# @param value The time, given as an ISO 8601 string, a time
#              tuple, or a integer time value.

class DateTime:
    """DateTime wrapper for an ISO 8601 string or time tuple or
    localtime integer value to generate 'dateTime.iso8601' XML-RPC
    value.
    """

    def __init__(self, value=0):
        if not isinstance(value, StringType):
            if not isinstance(value, (TupleType, time.struct_time)):
                if value == 0:
                    value = time.time()
                value = time.localtime(value)
            value = time.strftime("%Y%m%dT%H:%M:%S", value)
        self.value = value

    def __cmp__(self, other):
        if isinstance(other, DateTime):
            other = other.value
        return cmp(self.value, other)

    ##
    # Get date/time value.
    #
    # @return Date/time value, as an ISO 8601 string.

    def __str__(self):
        return self.value

    def __repr__(self):
        return "<DateTime %s at %x>" % (repr(self.value), id(self))

    def decode(self, data):
        self.value = string.strip(data)

    def encode(self, out):
        out.write("<value><dateTime.iso8601>")
        out.write(self.value)
        out.write("</dateTime.iso8601></value>\n")

def _datetime(data):
    # decode xml element contents into a DateTime structure.
    value = DateTime()
    value.decode(data)
    return value

##
# Wrapper for binary data.  This can be used to transport any kind
# of binary data over XML-RPC, using BASE64 encoding.
#
# @param data An 8-bit string containing arbitrary data.

import base64
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

class Binary:
    """Wrapper for binary data."""

    def __init__(self, data=None):
        self.data = data

    ##
    # Get buffer contents.
    #
    # @return Buffer contents, as an 8-bit string.

    def __str__(self):
        return self.data or ""

    def __cmp__(self, other):
        if isinstance(other, Binary):
            other = other.data
        return cmp(self.data, other)

    def decode(self, data):
        self.data = base64.decodestring(data)

    def encode(self, out):
        out.write("<value><base64>\n")
        base64.encode(StringIO.StringIO(self.data), out)
        out.write("</base64></value>\n")

def _binary(data):
    # decode xml element contents into a Binary structure
    value = Binary()
    value.decode(data)
    return value

WRAPPERS = (DateTime, Binary)
if not _bool_is_builtin:
    WRAPPERS = WRAPPERS + (Boolean,)

# --------------------------------------------------------------------
# XML parsers

try:
    # optional xmlrpclib accelerator.  for more information on this
    # component, contact info@pythonware.com
    import _xmlrpclib
    FastParser = _xmlrpclib.Parser
    FastUnmarshaller = _xmlrpclib.Unmarshaller
except (AttributeError, ImportError):
    FastParser = FastUnmarshaller = None

try:
    import _xmlrpclib
    FastMarshaller = _xmlrpclib.Marshaller
except (AttributeError, ImportError):
    FastMarshaller = None

#
# the SGMLOP parser is about 15x faster than Python's builtin
# XML parser.  SGMLOP sources can be downloaded from:
#
#     http://www.pythonware.com/products/xml/sgmlop.htm
#

try:
    import sgmlop
    if not hasattr(sgmlop, "XMLParser"):
        raise ImportError
except ImportError:
    SgmlopParser = None # sgmlop accelerator not available
else:
    class SgmlopParser:
        def __init__(self, target):

            # setup callbacks
            self.finish_starttag = target.start
            self.finish_endtag = target.end
            self.handle_data = target.data
            self.handle_xml = target.xml

            # activate parser
            self.parser = sgmlop.XMLParser()
            self.parser.register(self)
            self.feed = self.parser.feed
            self.entity = {
                "amp": "&", "gt": ">", "lt": "<",
                "apos": "'", "quot": '"'
                }

        def close(self):
            try:
                self.parser.close()
            finally:
                self.parser = self.feed = None # nuke circular reference

        def handle_proc(self, tag, attr):
            m = re.search("encoding\s*=\s*['\"]([^\"']+)[\"']", attr)
            if m:
                self.handle_xml(m.group(1), 1)

        def handle_entityref(self, entity):
            # <string> entity
            try:
                self.handle_data(self.entity[entity])
            except KeyError:
                self.handle_data("&%s;" % entity)

try:
    from xml.parsers import expat
    if not hasattr(expat, "ParserCreate"):
        raise ImportError
except ImportError:
    ExpatParser = None # expat not available
else:
    class ExpatParser:
        # fast expat parser for Python 2.0 and later.  this is about
        # 50% slower than sgmlop, on roundtrip testing
        def __init__(self, target):
            self._parser = parser = expat.ParserCreate(None, None)
            self._target = target
            parser.StartElementHandler = target.start
            parser.EndElementHandler = target.end
            parser.CharacterDataHandler = target.data
            encoding = None
            if not parser.returns_unicode:
                encoding = "utf-8"
            target.xml(encoding, None)

        def feed(self, data):
            self._parser.Parse(data, 0)

        def close(self):
            self._parser.Parse("", 1) # end of data
            del self._target, self._parser # get rid of circular references

class SlowParser:
    """Default XML parser (based on xmllib.XMLParser)."""
    # this is about 10 times slower than sgmlop, on roundtrip
    # testing.
    def __init__(self, target):
        import xmllib # lazy subclassing (!)
        if xmllib.XMLParser not in SlowParser.__bases__:
            SlowParser.__bases__ = (xmllib.XMLParser,)
        self.handle_xml = target.xml
        self.unknown_starttag = target.start
        self.handle_data = target.data
        self.handle_cdata = target.data
        self.unknown_endtag = target.end
        try:
            xmllib.XMLParser.__init__(self, accept_utf8=1)
        except TypeError:
            xmllib.XMLParser.__init__(self) # pre-2.0

# --------------------------------------------------------------------
# XML-RPC marshalling and unmarshalling code

##
# XML-RPC marshaller.
#
# @param encoding Default encoding for 8-bit strings.  The default
#     value is None (interpreted as UTF-8).
# @see dumps

class Marshaller:
    """Generate an XML-RPC params chunk from a Python data structure.

    Create a Marshaller instance for each set of parameters, and use
    the "dumps" method to convert your data (represented as a tuple)
    to an XML-RPC params chunk.  To write a fault response, pass a
    Fault instance instead.  You may prefer to use the "dumps" module
    function for this purpose.
    """

    # by the way, if you don't understand what's going on in here,
    # that's perfectly ok.

    def __init__(self, encoding=None, allow_none=0):
        self.memo = {}
        self.data = None
        self.encoding = encoding
        self.allow_none = allow_none

    dispatch = {}

    def dumps(self, values):
        out = []
        write = out.append
        dump = self.__dump
        if isinstance(values, Fault):
            # fault instance
            write("<fault>\n")
            dump({'faultCode': values.faultCode,
                  'faultString': values.faultString},
                 write)
            write("</fault>\n")
        else:
            # parameter block
            # FIXME: the xml-rpc specification allows us to leave out
            # the entire <params> block if there are no parameters.
            # however, changing this may break older code (including
            # old versions of xmlrpclib.py), so this is better left as
            # is for now.  See @XMLRPC3 for more information. /F
            write("<params>\n")
            for v in values:
                write("<param>\n")
                dump(v, write)
                write("</param>\n")
            write("</params>\n")
        result = string.join(out, "")
        return result

    def __dump(self, value, write):
        try:
            f = self.dispatch[type(value)]
        except KeyError:
            raise TypeError, "cannot marshal %s objects" % type(value)
        else:
            f(self, value, write)

    def dump_nil (self, value, write):
        if not self.allow_none:
            raise TypeError, "cannot marshal None unless allow_none is enabled"
        write("<value><nil/></value>")
    dispatch[NoneType] = dump_nil

    def dump_int(self, value, write):
        # in case ints are > 32 bits
        if value > MAXINT or value < MININT:
            raise OverflowError, "int exceeds XML-RPC limits"
        write("<value><int>")
        write(str(value))
        write("</int></value>\n")
    dispatch[IntType] = dump_int

    if _bool_is_builtin:
        def dump_bool(self, value, write):
            write("<value><boolean>")
            write(value and "1" or "0")
            write("</boolean></value>\n")
        dispatch[bool] = dump_bool

    def dump_long(self, value, write):
        if value > MAXINT or value < MININT:
            raise OverflowError, "long int exceeds XML-RPC limits"
        write("<value><int>")
        write(str(int(value)))
        write("</int></value>\n")
    dispatch[LongType] = dump_long

    def dump_double(self, value, write):
        write("<value><double>")
        write(repr(value))
        write("</double></value>\n")
    dispatch[FloatType] = dump_double

    def dump_string(self, value, write, escape=escape):
        write("<value><string>")
        write(escape(value))
        write("</string></value>\n")
    dispatch[StringType] = dump_string

    if unicode:
        def dump_unicode(self, value, write, escape=escape):
            value = value.encode(self.encoding)
            write("<value><string>")
            write(escape(value))
            write("</string></value>\n")
        dispatch[UnicodeType] = dump_unicode

    def dump_array(self, value, write):
        i = id(value)
        if self.memo.has_key(i):
            raise TypeError, "cannot marshal recursive sequences"
        self.memo[i] = None
        dump = self.__dump
        write("<value><array><data>\n")
        for v in value:
            dump(v, write)
        write("</data></array></value>\n")
        del self.memo[i]
    dispatch[TupleType] = dump_array
    dispatch[ListType] = dump_array

    def dump_struct(self, value, write, escape=escape):
        i = id(value)
        if self.memo.has_key(i):
            raise TypeError, "cannot marshal recursive dictionaries"
        self.memo[i] = None
        dump = self.__dump
        write("<value><struct>\n")
        for k, v in value.items():
            write("<member>\n")
            if type(k) is not StringType:
                if unicode and type(k) is UnicodeType:
                    k = k.encode(self.encoding)
                else:
                    raise TypeError, "dictionary key must be string"
            write("<name>%s</name>\n" % escape(k))
            dump(v, write)
            write("</member>\n")
        write("</struct></value>\n")
        del self.memo[i]
    dispatch[DictType] = dump_struct

    def dump_instance(self, value, write):
        # check for special wrappers
        if value.__class__ in WRAPPERS:
            self.write = write
            value.encode(self)
            del self.write
        else:
            # store instance attributes as a struct (really?)
            self.dump_struct(value.__dict__, write)
    dispatch[InstanceType] = dump_instance

##
# XML-RPC unmarshaller.
#
# @see loads

class Unmarshaller:
    """Unmarshal an XML-RPC response, based on incoming XML event
    messages (start, data, end).  Call close() to get the resulting
    data structure.

    Note that this reader is fairly tolerant, and gladly accepts bogus
    XML-RPC data without complaining (but not bogus XML).
    """

    # and again, if you don't understand what's going on in here,
    # that's perfectly ok.

    def __init__(self):
        self._type = None
        self._stack = []
        self._marks = []
        self._data = []
        self._methodname = None
        self._encoding = "utf-8"
        self.append = self._stack.append

    def close(self):
        # return response tuple and target method
        if self._type is None or self._marks:
            raise ResponseError()
        if self._type == "fault":
            raise Fault(**self._stack[0])
        return tuple(self._stack)

    def getmethodname(self):
        return self._methodname

    #
    # event handlers

    def xml(self, encoding, standalone):
        self._encoding = encoding
        # FIXME: assert standalone == 1 ???

    def start(self, tag, attrs):
        # prepare to handle this element
        if tag == "array" or tag == "struct":
            self._marks.append(len(self._stack))
        self._data = []
        self._value = (tag == "value")

    def data(self, text):
        self._data.append(text)

    def end(self, tag, join=string.join):
        # call the appropriate end tag handler
        try:
            f = self.dispatch[tag]
        except KeyError:
            pass # unknown tag ?
        else:
            return f(self, join(self._data, ""))

    #
    # accelerator support

    def end_dispatch(self, tag, data):
        # dispatch data
        try:
            f = self.dispatch[tag]
        except KeyError:
            pass # unknown tag ?
        else:
            return f(self, data)

    #
    # element decoders

    dispatch = {}

    def end_nil (self, data):
        self.append(None)
        self._value = 0
    dispatch["nil"] = end_nil

    def end_boolean(self, data):
        if data == "0":
            self.append(False)
        elif data == "1":
            self.append(True)
        else:
            raise TypeError, "bad boolean value"
        self._value = 0
    dispatch["boolean"] = end_boolean

    def end_int(self, data):
        self.append(int(data))
        self._value = 0
    dispatch["i4"] = end_int
    dispatch["int"] = end_int

    def end_double(self, data):
        self.append(float(data))
        self._value = 0
    dispatch["double"] = end_double

    def end_string(self, data):
        if self._encoding:
            data = _decode(data, self._encoding)
        self.append(_stringify(data))
        self._value = 0
    dispatch["string"] = end_string
    dispatch["name"] = end_string # struct keys are always strings

    def end_array(self, data):
        mark = self._marks.pop()
        # map arrays to Python lists
        self._stack[mark:] = [self._stack[mark:]]
        self._value = 0
    dispatch["array"] = end_array

    def end_struct(self, data):
        mark = self._marks.pop()
        # map structs to Python dictionaries
        dict = {}
        items = self._stack[mark:]
        for i in range(0, len(items), 2):
            dict[_stringify(items[i])] = items[i+1]
        self._stack[mark:] = [dict]
        self._value = 0
    dispatch["struct"] = end_struct

    def end_base64(self, data):
        value = Binary()
        value.decode(data)
        self.append(value)
        self._value = 0
    dispatch["base64"] = end_base64

    def end_dateTime(self, data):
        value = DateTime()
        value.decode(data)
        self.append(value)
    dispatch["dateTime.iso8601"] = end_dateTime

    def end_value(self, data):
        # if we stumble upon a value element with no internal
        # elements, treat it as a string element
        if self._value:
            self.end_string(data)
    dispatch["value"] = end_value

    def end_params(self, data):
        self._type = "params"
    dispatch["params"] = end_params

    def end_fault(self, data):
        self._type = "fault"
    dispatch["fault"] = end_fault

    def end_methodName(self, data):
        if self._encoding:
            data = _decode(data, self._encoding)
        self._methodname = data
        self._type = "methodName" # no params
    dispatch["methodName"] = end_methodName

## Multicall support
#

class _MultiCallMethod:
    # some lesser magic to store calls made to a MultiCall object
    # for batch execution
    def __init__(self, call_list, name):
        self.__call_list = call_list
        self.__name = name
    def __getattr__(self, name):
        return _MultiCallMethod(self.__call_list, "%s.%s" % (self.__name, name))
    def __call__(self, *args):
        self.__call_list.append((self.__name, args))

class MultiCallIterator:
    """Iterates over the results of a multicall. Exceptions are
    thrown in response to xmlrpc faults."""

    def __init__(self, results):
        self.results = results

    def __getitem__(self, i):
        item = self.results[i]
        if type(item) == type({}):
            raise Fault(item['faultCode'], item['faultString'])
        elif type(item) == type([]):
            return item[0]
        else:
            raise ValueError,\
                  "unexpected type in multicall result"

class MultiCall:
    """server -> a object used to boxcar method calls

    server should be a ServerProxy object.

    Methods can be added to the MultiCall using normal
    method call syntax e.g.:

    multicall = MultiCall(server_proxy)
    multicall.add(2,3)
    multicall.get_address("Guido")

    To execute the multicall, call the MultiCall object e.g.:

    add_result, address = multicall()
    """

    def __init__(self, server):
        self.__server = server
        self.__call_list = []

    def __repr__(self):
        return "<MultiCall at %x>" % id(self)

    __str__ = __repr__

    def __getattr__(self, name):
        return _MultiCallMethod(self.__call_list, name)

    def __call__(self):
        marshalled_list = []
        for name, args in self.__call_list:
            marshalled_list.append({'methodName' : name, 'params' : args})

        return MultiCallIterator(self.__server.system.multicall(marshalled_list))

# --------------------------------------------------------------------
# convenience functions

##
# Create a parser object, and connect it to an unmarshalling instance.
# This function picks the fastest available XML parser.
#
# return A (parser, unmarshaller) tuple.

def getparser():
    """getparser() -> parser, unmarshaller

    Create an instance of the fastest available parser, and attach it
    to an unmarshalling object.  Return both objects.
    """
    if FastParser and FastUnmarshaller:
        target = FastUnmarshaller(True, False, _binary, _datetime, Fault)
        parser = FastParser(target)
    else:
        target = Unmarshaller()
        if FastParser:
            parser = FastParser(target)
        elif SgmlopParser:
            parser = SgmlopParser(target)
        elif ExpatParser:
            parser = ExpatParser(target)
        else:
            parser = SlowParser(target)
    return parser, target

##
# Convert a Python tuple or a Fault instance to an XML-RPC packet.
#
# @def dumps(params, **options)
# @param params A tuple or Fault instance.
# @keyparam methodname If given, create a methodCall request for
#     this method name.
# @keyparam methodresponse If given, create a methodResponse packet.
#     If used with a tuple, the tuple must be a singleton (that is,
#     it must contain exactly one element).
# @keyparam encoding The packet encoding.
# @return A string containing marshalled data.

def dumps(params, methodname=None, methodresponse=None, encoding=None,
          allow_none=0):
    """data [,options] -> marshalled data

    Convert an argument tuple or a Fault instance to an XML-RPC
    request (or response, if the methodresponse option is used).

    In addition to the data object, the following options can be given
    as keyword arguments:

        methodname: the method name for a methodCall packet

        methodresponse: true to create a methodResponse packet.
        If this option is used with a tuple, the tuple must be
        a singleton (i.e. it can contain only one element).

        encoding: the packet encoding (default is UTF-8)

    All 8-bit strings in the data structure are assumed to use the
    packet encoding.  Unicode strings are automatically converted,
    where necessary.
    """

    assert isinstance(params, TupleType) or isinstance(params, Fault),\
           "argument must be tuple or Fault instance"

    if isinstance(params, Fault):
        methodresponse = 1
    elif methodresponse and isinstance(params, TupleType):
        assert len(params) == 1, "response tuple must be a singleton"

    if not encoding:
        encoding = "utf-8"

    if FastMarshaller:
        m = FastMarshaller(encoding)
    else:
        m = Marshaller(encoding, allow_none)

    data = m.dumps(params)

    if encoding != "utf-8":
        xmlheader = "<?xml version='1.0' encoding='%s'?>\n" % str(encoding)
    else:
        xmlheader = "<?xml version='1.0'?>\n" # utf-8 is default

    # standard XML-RPC wrappings
    if methodname:
        # a method call
        if not isinstance(methodname, StringType):
            methodname = methodname.encode(encoding)
        data = (
            xmlheader,
            "<methodCall>\n"
            "<methodName>", methodname, "</methodName>\n",
            data,
            "</methodCall>\n"
            )
    elif methodresponse:
        # a method response, or a fault structure
        data = (
            xmlheader,
            "<methodResponse>\n",
            data,
            "</methodResponse>\n"
            )
    else:
        return data # return as is
    return string.join(data, "")

##
# Convert an XML-RPC packet to a Python object.  If the XML-RPC packet
# represents a fault condition, this function raises a Fault exception.
#
# @param data An XML-RPC packet, given as an 8-bit string.
# @return A tuple containing the unpacked data, and the method name
#     (None if not present).
# @see Fault

def loads(data):
    """data -> unmarshalled data, method name

    Convert an XML-RPC packet to unmarshalled data plus a method
    name (None if not present).

    If the XML-RPC packet represents a fault condition, this function
    raises a Fault exception.
    """
    p, u = getparser()
    p.feed(data)
    p.close()
    return u.close(), u.getmethodname()


# --------------------------------------------------------------------
# request dispatcher

class _Method:
    # some magic to bind an XML-RPC method to an RPC server.
    # supports "nested" methods (e.g. examples.getStateName)
    def __init__(self, send, name):
        self.__send = send
        self.__name = name
    def __getattr__(self, name):
        return _Method(self.__send, "%s.%s" % (self.__name, name))
    def __call__(self, *args):
        return self.__send(self.__name, args)

##
# Standard transport class for XML-RPC over HTTP.
# <p>
# You can create custom transports by subclassing this method, and
# overriding selected methods.

class Transport:
    """Handles an HTTP transaction to an XML-RPC server."""

    # client identifier (may be overridden)
    user_agent = "xmlrpclib.py/%s (by www.pythonware.com)" % __version__

    ##
    # Send a complete request, and parse the response.
    #
    # @param host Target host.
    # @param handler Target PRC handler.
    # @param request_body XML-RPC request body.
    # @param verbose Debugging flag.
    # @return Parsed response.

    def request(self, host, handler, request_body, verbose=0):
        # issue XML-RPC request

        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)

        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)

        errcode, errmsg, headers = h.getreply()

        if errcode != 200:
            raise ProtocolError(
                host + handler,
                errcode, errmsg,
                headers
                )

        self.verbose = verbose

        try:
            sock = h._conn.sock
        except AttributeError:
            sock = None

        return self._parse_response(h.getfile(), sock)

    ##
    # Create parser.
    #
    # @return A 2-tuple containing a parser and a unmarshaller.

    def getparser(self):
        # get parser and unmarshaller
        return getparser()

    ##
    # Get authorization info from host parameter
    # Host may be a string, or a (host, x509-dict) tuple; if a string,
    # it is checked for a "user:pw@host" format, and a "Basic
    # Authentication" header is added if appropriate.
    #
    # @param host Host descriptor (URL or (URL, x509 info) tuple).
    # @return A 3-tuple containing (actual host, extra headers,
    #     x509 info).  The header and x509 fields may be None.

    def get_host_info(self, host):

        x509 = {}
        if isinstance(host, TupleType):
            host, x509 = host

        import urllib
        auth, host = urllib.splituser(host)

        if auth:
            import base64
            auth = base64.encodestring(urllib.unquote(auth))
            auth = string.join(string.split(auth), "") # get rid of whitespace
            extra_headers = [
                ("Authorization", "Basic " + auth)
                ]
        else:
            extra_headers = None

        return host, extra_headers, x509

    ##
    # Connect to server.
    #
    # @param host Target host.
    # @return A connection handle.

    def make_connection(self, host):
        # create a HTTP connection object from a host descriptor
        import httplib
        host, extra_headers, x509 = self.get_host_info(host)
        return httplib.HTTP(host)

    ##
    # Send request header.
    #
    # @param connection Connection handle.
    # @param handler Target RPC handler.
    # @param request_body XML-RPC body.

    def send_request(self, connection, handler, request_body):
        connection.putrequest("POST", handler)

    ##
    # Send host name.
    #
    # @param connection Connection handle.
    # @param host Host name.

    def send_host(self, connection, host):
        host, extra_headers, x509 = self.get_host_info(host)
        connection.putheader("Host", host)
        if extra_headers:
            if isinstance(extra_headers, DictType):
                extra_headers = extra_headers.items()
            for key, value in extra_headers:
                connection.putheader(key, value)

    ##
    # Send user-agent identifier.
    #
    # @param connection Connection handle.

    def send_user_agent(self, connection):
        connection.putheader("User-Agent", self.user_agent)

    ##
    # Send request body.
    #
    # @param connection Connection handle.
    # @param request_body XML-RPC request body.

    def send_content(self, connection, request_body):
        connection.putheader("Content-Type", "text/xml")
        connection.putheader("Content-Length", str(len(request_body)))
        connection.endheaders()
        if request_body:
            connection.send(request_body)

    ##
    # Parse response.
    #
    # @param file Stream.
    # @return Response tuple and target method.

    def parse_response(self, file):
        # compatibility interface
        return self._parse_response(file, None)

    ##
    # Parse response (alternate interface).  This is similar to the
    # parse_response method, but also provides direct access to the
    # underlying socket object (where available).
    #
    # @param file Stream.
    # @param sock Socket handle (or None, if the socket object
    #    could not be accessed).
    # @return Response tuple and target method.

    def _parse_response(self, file, sock):
        # read response from input file/socket, and parse it

        p, u = self.getparser()

        while 1:
            if sock:
                response = sock.recv(1024)
            else:
                response = file.read(1024)
            if not response:
                break
            if self.verbose:
                print "body:", repr(response)
            p.feed(response)

        file.close()
        p.close()

        return u.close()

##
# Standard transport class for XML-RPC over HTTPS.

class SafeTransport(Transport):
    """Handles an HTTPS transaction to an XML-RPC server."""

    # FIXME: mostly untested

    def make_connection(self, host):
        # create a HTTPS connection object from a host descriptor
        # host may be a string, or a (host, x509-dict) tuple
        import httplib
        host, extra_headers, x509 = self.get_host_info(host)
        try:
            HTTPS = httplib.HTTPS
        except AttributeError:
            raise NotImplementedError(
                "your version of httplib doesn't support HTTPS"
                )
        else:
            return HTTPS(host, None, **(x509 or {}))

##
# Standard server proxy.  This class establishes a virtual connection
# to an XML-RPC server.
# <p>
# This class is available as ServerProxy and Server.  New code should
# use ServerProxy, to avoid confusion.
#
# @def ServerProxy(uri, **options)
# @param uri The connection point on the server.
# @keyparam transport A transport factory, compatible with the
#    standard transport class.
# @keyparam encoding The default encoding used for 8-bit strings
#    (default is UTF-8).
# @keyparam verbose Use a true value to enable debugging output.
#    (printed to standard output).
# @see Transport

class ServerProxy:
    """uri [,options] -> a logical connection to an XML-RPC server

    uri is the connection point on the server, given as
    scheme://host/target.

    The standard implementation always supports the "http" scheme.  If
    SSL socket support is available (Python 2.0), it also supports
    "https".

    If the target part and the slash preceding it are both omitted,
    "/RPC2" is assumed.

    The following options can be given as keyword arguments:

        transport: a transport factory
        encoding: the request encoding (default is UTF-8)

    All 8-bit strings passed to the server proxy are assumed to use
    the given encoding.
    """

    def __init__(self, uri, transport=None, encoding=None, verbose=0,
                 allow_none=0):
        # establish a "logical" server connection

        # get the url
        import urllib
        type, uri = urllib.splittype(uri)
        if type not in ("http", "https"):
            raise IOError, "unsupported XML-RPC protocol"
        self.__host, self.__handler = urllib.splithost(uri)
        if not self.__handler:
            self.__handler = "/RPC2"

        if transport is None:
            if type == "https":
                transport = SafeTransport()
            else:
                transport = Transport()
        self.__transport = transport

        self.__encoding = encoding
        self.__verbose = verbose
        self.__allow_none = allow_none

    def __request(self, methodname, params):
        # call a method on the remote server

        request = dumps(params, methodname, encoding=self.__encoding,
                        allow_none=self.__allow_none)

        response = self.__transport.request(
            self.__host,
            self.__handler,
            request,
            verbose=self.__verbose
            )

        if len(response) == 1:
            response = response[0]

        return response

    def __repr__(self):
        return (
            "<ServerProxy for %s%s>" %
            (self.__host, self.__handler)
            )

    __str__ = __repr__

    def __getattr__(self, name):
        # magic method dispatcher
        return _Method(self.__request, name)

    # note: to call a remote object with an non-standard name, use
    # result getattr(server, "strange-python-name")(args)

# compatibility

Server = ServerProxy

# --------------------------------------------------------------------
# test code

if __name__ == "__main__":

    # simple test program (from the XML-RPC specification)

    # server = ServerProxy("http://localhost:8000") # local server
    server = ServerProxy("http://time.xmlrpc.com/RPC2")

    print server

    try:
        print server.currentTime.getCurrentTime()
    except Error, v:
        print "ERROR", v

    multi = MultiCall(server)
    multi.currentTime.getCurrentTime()
    multi.currentTime.getCurrentTime()
    try:
        for response in multi():
            print response
    except Error, v:
        print "ERROR", v
