"""Define names for all type symbols known in the standard interpreter.

Types that are part of optional modules (e.g. array) are not listed.
"""
from __future__ import generators

import sys

NoneType = type(None)
TypeType = type
ObjectType = object

IntType = int
LongType = long
FloatType = float
try:
    ComplexType = complex
except NameError:
    pass

StringType = str
UnicodeType = unicode
BufferType = type(buffer(''))

TupleType = tuple
ListType = list
DictType = DictionaryType = dictionary

def _f(): pass
FunctionType = type(_f)
LambdaType = type(lambda: None)         # Same as FunctionType
try:
    CodeType = type(_f.func_code)
except:
    pass

def g():
    yield 1
GeneratorType = type(g())
del g

class _C:
    def _m(self): pass
ClassType = type(_C)
UnboundMethodType = type(_C._m)         # Same as MethodType
_x = _C()
InstanceType = type(_x)
MethodType = type(_x._m)

BuiltinFunctionType = type(len)
BuiltinMethodType = type([].append)     # Same as BuiltinFunctionType

ModuleType = type(sys)

try:
    FileType = type(sys.__stdin__)
except:
    pass
XRangeType = type(xrange(0))

try:
    raise TypeError
except TypeError:
    try:
        tb = sys.exc_info()[2]
        TracebackType = type(tb)
        FrameType = type(tb.tb_frame)
    except:
        pass
    tb = None; del tb

SliceType = type(slice(0))
EllipsisType = type(Ellipsis)

DictIterType = type(iter({}))
SequenceIterType = type(iter([]))
FunctionIterType = type(iter(lambda: 0, 0))
DictProxyType = type(TypeType.__dict__)

del sys, _f, _C, _x                     # Not for export
