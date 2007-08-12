# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

#error missing SetActionFilter

import string

# Declarations that change for each manager
MODNAME = '_CG'                         # The name of the module

# The following is *usually* unchanged but may still require tuning
MODPREFIX = 'CG'                        # The prefix for module-wide routines
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"       # The file generated by this program

from macsupport import *

CGrafPtr = OpaqueByValueType("CGrafPtr", "GrafObj")
RgnHandle = OpaqueByValueType("RgnHandle", "ResObj")

# Create the type objects

includestuff = includestuff + """
#include <ApplicationServices/ApplicationServices.h>

extern int GrafObj_Convert(PyObject *, GrafPtr *);

/*
** Manual converters
*/

PyObject *CGPoint_New(CGPoint *itself)
{

        return Py_BuildValue("(ff)",
                        itself->x,
                        itself->y);
}

int
CGPoint_Convert(PyObject *v, CGPoint *p_itself)
{
        if( !PyArg_Parse(v, "(ff)",
                        &p_itself->x,
                        &p_itself->y) )
                return 0;
        return 1;
}

PyObject *CGRect_New(CGRect *itself)
{

        return Py_BuildValue("(ffff)",
                        itself->origin.x,
                        itself->origin.y,
                        itself->size.width,
                        itself->size.height);
}

int
CGRect_Convert(PyObject *v, CGRect *p_itself)
{
        if( !PyArg_Parse(v, "(ffff)",
                        &p_itself->origin.x,
                        &p_itself->origin.y,
                        &p_itself->size.width,
                        &p_itself->size.height) )
                return 0;
        return 1;
}

PyObject *CGAffineTransform_New(CGAffineTransform *itself)
{

        return Py_BuildValue("(ffffff)",
                        itself->a,
                        itself->b,
                        itself->c,
                        itself->d,
                        itself->tx,
                        itself->ty);
}

int
CGAffineTransform_Convert(PyObject *v, CGAffineTransform *p_itself)
{
        if( !PyArg_Parse(v, "(ffffff)",
                        &p_itself->a,
                        &p_itself->b,
                        &p_itself->c,
                        &p_itself->d,
                        &p_itself->tx,
                        &p_itself->ty) )
                return 0;
        return 1;
}
"""

class MyOpaqueByValueType(OpaqueByValueType):
    """Sort of a mix between OpaqueByValueType and OpaqueType."""
    def mkvalueArgs(self, name):
        return "%s, &%s" % (self.new, name)

CGPoint = MyOpaqueByValueType('CGPoint', 'CGPoint')
CGRect = MyOpaqueByValueType('CGRect', 'CGRect')
CGAffineTransform = MyOpaqueByValueType('CGAffineTransform', 'CGAffineTransform')

char_ptr = Type("char *", "s")

CGTextEncoding = int
CGLineCap = int
CGLineJoin = int
CGTextDrawingMode = int
CGPathDrawingMode = int
CGInterpolationQuality = int

# The real objects
CGContextRef = OpaqueByValueType("CGContextRef", "CGContextRefObj")


class MyObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
    def outputStructMembers(self):
        ObjectDefinition.outputStructMembers(self)
    def outputCleanupStructMembers(self):
        Output("CGContextRelease(self->ob_itself);")


# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)

CGContextRef_object = MyObjectDefinition('CGContextRef', 'CGContextRefObj', 'CGContextRef')


# ADD object here

module.addobject(CGContextRef_object)



Function = FunctionGenerator
Method = MethodGenerator

CGContextRef_methods = []

# ADD _methods initializer here
exec(open(INPUTFILE).read())

# manual method, lives in Quickdraw.h
f = Method(void, 'SyncCGContextOriginWithPort',
    (CGContextRef, 'ctx', InMode),
    (CGrafPtr, 'port', InMode),
)
CGContextRef_methods.append(f)

# manual method, lives in Quickdraw.h
f = Method(void, 'ClipCGContextToRegion',
    (CGContextRef, 'ctx', InMode),
    (Rect, 'portRect', InMode),
    (RgnHandle, 'region', InMode),
)
CGContextRef_methods.append(f)


CreateCGContextForPort_body = """\
GrafPtr port;
CGContextRef ctx;
OSStatus _err;

if (!PyArg_ParseTuple(_args, "O&", GrafObj_Convert, &port))
        return NULL;

_err = CreateCGContextForPort(port, &ctx);
if (_err != noErr)
        if (_err != noErr) return PyMac_Error(_err);
_res = Py_BuildValue("O&", CGContextRefObj_New, ctx);
return _res;
"""

f = ManualGenerator("CreateCGContextForPort", CreateCGContextForPort_body);
f.docstring = lambda: "(CGrafPtr) -> CGContextRef"
module.add(f)


# ADD add forloop here
for f in CGContextRef_methods:
    CGContextRef_object.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()
