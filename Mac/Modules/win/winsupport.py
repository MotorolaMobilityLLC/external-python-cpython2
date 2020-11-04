# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

import string

# Declarations that change for each manager
MACHEADERFILE = 'Windows.h'             # The Apple header file
MODNAME = '_Win'                                # The name of the module
OBJECTNAME = 'Window'                   # The basic name of the objects used here

# The following is *usually* unchanged but may still require tuning
MODPREFIX = 'Win'                       # The prefix for module-wide routines
OBJECTTYPE = OBJECTNAME + 'Ptr'         # The C type used to represent them
OBJECTPREFIX = MODPREFIX + 'Obj'        # The prefix for object methods
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
EDITFILE = string.lower(MODPREFIX) + 'edit.py' # The manual definitions
OUTPUTFILE = MODNAME + "module.c"       # The file generated by this program

from macsupport import *

# Create the type objects

WindowPtr = OpaqueByValueType(OBJECTTYPE, OBJECTPREFIX)
WindowRef = WindowPtr
WindowPeek = OpaqueByValueType("WindowPeek", OBJECTPREFIX)
WindowPeek.passInput = lambda name: "(WindowPeek)(%s)" % name
CGrafPtr = OpaqueByValueType("CGrafPtr", "GrafObj")
GrafPtr = OpaqueByValueType("GrafPtr", "GrafObj")

DragReference = OpaqueByValueType("DragReference", "DragObj")

RgnHandle = OpaqueByValueType("RgnHandle", "ResObj")
PicHandle = OpaqueByValueType("PicHandle", "ResObj")
WCTabHandle = OpaqueByValueType("WCTabHandle", "ResObj")
AuxWinHandle = OpaqueByValueType("AuxWinHandle", "ResObj")
PixPatHandle = OpaqueByValueType("PixPatHandle", "ResObj")
AliasHandle = OpaqueByValueType("AliasHandle", "ResObj")
IconRef = OpaqueByValueType("IconRef", "ResObj")

WindowRegionCode = Type("WindowRegionCode", "H")
WindowClass = Type("WindowClass", "l")
WindowAttributes = Type("WindowAttributes", "l")
WindowPositionMethod = Type("WindowPositionMethod", "l")
WindowTransitionEffect = Type("WindowTransitionEffect", "l")
WindowTransitionAction = Type("WindowTransitionAction", "l")
RGBColor = OpaqueType("RGBColor", "QdRGB")
RGBColor_ptr = RGBColor
ScrollWindowOptions = Type("ScrollWindowOptions", "l")
WindowPartCode = Type("WindowPartCode", "h")
WindowDefPartCode = Type("WindowDefPartCode", "h")
WindowModality = Type("WindowModality", "l")
GDHandle = OpaqueByValueType("GDHandle", "ResObj")
WindowConstrainOptions = Type("WindowConstrainOptions", "l")

PropertyCreator = OSTypeType("PropertyCreator")
PropertyTag = OSTypeType("PropertyTag")

includestuff = includestuff + """
#include <Carbon/Carbon.h>

#ifdef USE_TOOLBOX_OBJECT_GLUE
extern PyObject *_WinObj_New(WindowRef);
extern PyObject *_WinObj_WhichWindow(WindowRef);
extern int _WinObj_Convert(PyObject *, WindowRef *);

#define WinObj_New _WinObj_New
#define WinObj_WhichWindow _WinObj_WhichWindow
#define WinObj_Convert _WinObj_Convert
#endif

/* Classic calls that we emulate in carbon mode */
#define GetWindowUpdateRgn(win, rgn) GetWindowRegion((win), kWindowUpdateRgn, (rgn))
#define GetWindowStructureRgn(win, rgn) GetWindowRegion((win), kWindowStructureRgn, (rgn))
#define GetWindowContentRgn(win, rgn) GetWindowRegion((win), kWindowContentRgn, (rgn))

/* Function to dispose a window, with a "normal" calling sequence */
static void
PyMac_AutoDisposeWindow(WindowPtr w)
{
        DisposeWindow(w);
}
"""

finalstuff = finalstuff + """
/* Return the object corresponding to the window, or NULL */

PyObject *
WinObj_WhichWindow(WindowPtr w)
{
        PyObject *it;

        if (w == NULL) {
                it = Py_None;
                Py_INCREF(it);
        } else {
                it = (PyObject *) GetWRefCon(w);
                if (it == NULL || !IsPointerValid((Ptr)it) || ((WindowObject *)it)->ob_itself != w || !WinObj_Check(it)) {
                        it = WinObj_New(w);
                        ((WindowObject *)it)->ob_freeit = NULL;
                } else {
                        Py_INCREF(it);
                }
        }
        return it;
}
"""

initstuff = initstuff + """
        PyMac_INIT_TOOLBOX_OBJECT_NEW(WindowPtr, WinObj_New);
        PyMac_INIT_TOOLBOX_OBJECT_NEW(WindowPtr, WinObj_WhichWindow);
        PyMac_INIT_TOOLBOX_OBJECT_CONVERT(WindowPtr, WinObj_Convert);
"""

class MyObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
    def outputCheckNewArg(self):
        Output("if (itself == NULL) return PyMac_Error(resNotFound);")
        Output("/* XXXX Or should we use WhichWindow code here? */")
    def outputStructMembers(self):
        GlobalObjectDefinition.outputStructMembers(self)
        Output("void (*ob_freeit)(%s ptr);", self.itselftype)
    def outputInitStructMembers(self):
        GlobalObjectDefinition.outputInitStructMembers(self)
        Output("it->ob_freeit = NULL;")
        Output("if (GetWRefCon(itself) == 0)")
        OutLbrace()
        Output("SetWRefCon(itself, (long)it);")
        Output("it->ob_freeit = PyMac_AutoDisposeWindow;")
        OutRbrace()
    def outputCheckConvertArg(self):
        Out("""
        if (v == Py_None) { *p_itself = NULL; return 1; }
        if (PyInt_Check(v)) { *p_itself = (WindowPtr)PyInt_AsLong(v); return 1; }
        """)
        OutLbrace()
        Output("DialogRef dlg;")
        OutLbrace("if (DlgObj_Convert(v, &dlg) && dlg)")
        Output("*p_itself = GetDialogWindow(dlg);")
        Output("return 1;")
        OutRbrace()
        Output("PyErr_Clear();")
        OutRbrace()
    def outputCleanupStructMembers(self):
        Output("if (self->ob_freeit && self->ob_itself)")
        OutLbrace()
        Output("SetWRefCon(self->ob_itself, 0);")
        Output("self->ob_freeit(self->ob_itself);")
        OutRbrace()
        Output("self->ob_itself = NULL;")
        Output("self->ob_freeit = NULL;")

    def outputCompare(self):
        Output()
        Output("static int %s_compare(%s *self, %s *other)", self.prefix, self.objecttype, self.objecttype)
        OutLbrace()
        Output("if ( self->ob_itself > other->ob_itself ) return 1;")
        Output("if ( self->ob_itself < other->ob_itself ) return -1;")
        Output("return 0;")
        OutRbrace()

    def outputHash(self):
        Output()
        Output("static int %s_hash(%s *self)", self.prefix, self.objecttype)
        OutLbrace()
        Output("return (int)self->ob_itself;")
        OutRbrace()

    def outputRepr(self):
        Output()
        Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
        OutLbrace()
        Output("char buf[100];")
        Output("""sprintf(buf, "<Window object at 0x%%8.8x for 0x%%8.8x>", (unsigned)self, (unsigned)self->ob_itself);""")
        Output("return PyString_FromString(buf);")
        OutRbrace()

##      def outputFreeIt(self, itselfname):
##              Output("DisposeWindow(%s);", itselfname)
# From here on it's basically all boiler plate...

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)
object = MyObjectDefinition(OBJECTNAME, OBJECTPREFIX, OBJECTTYPE)
module.addobject(object)

# Create the generator classes used to populate the lists
Function = OSErrWeakLinkFunctionGenerator
Method = OSErrWeakLinkMethodGenerator

# Create and populate the lists
functions = []
methods = []
execfile(INPUTFILE)

# Add manual routines for converting integer WindowPtr's (as returned by
# various event routines)  and Dialog objects to a WindowObject.
whichwin_body = """
long ptr;

if ( !PyArg_ParseTuple(_args, "i", &ptr) )
        return NULL;
_res = WinObj_WhichWindow((WindowPtr)ptr);
return _res;
"""

f = ManualGenerator("WhichWindow", whichwin_body)
f.docstring = lambda : "Resolve an integer WindowPtr address to a Window object"

functions.append(f)

# And add the routines that access the internal bits of a window struct. They
# are currently #defined in Windows.h, they will be real routines in Copland
# (at which time this execfile can go)
execfile(EDITFILE)

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in methods: object.add(f)



# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()
