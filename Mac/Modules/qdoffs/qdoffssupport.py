# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

import string

# Declarations that change for each manager
MACHEADERFILE = 'QDOffscreen.h'		# The Apple header file
MODNAME = 'Qdoffs'				# The name of the module
OBJECTNAME = 'GWorld'			# The basic name of the objects used here

# The following is *usually* unchanged but may still require tuning
MODPREFIX = MODNAME			# The prefix for module-wide routines
OBJECTTYPE = OBJECTNAME + 'Ptr'		# The C type used to represent them
OBJECTPREFIX = OBJECTNAME + 'Obj'	# The prefix for object methods
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
#EDITFILE = string.lower(MODPREFIX) + 'edit.py' # The manual definitions
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects

GWorldPtr = OpaqueByValueType(OBJECTTYPE, OBJECTPREFIX)
GWorldFlags = Type("GWorldFlags", "l")
GDHandle = OpaqueByValueType("GDHandle", "ResObj")
OptGDHandle = OpaqueByValueType("GDHandle", "OptResObj")
CTabHandle = OpaqueByValueType("CTabHandle", "OptResObj")
PixPatHandle = OpaqueByValueType("PixPatHandle", "ResObj")
PixMapHandle = OpaqueByValueType("PixMapHandle", "ResObj")
CGrafPtr = OpaqueByValueType("CGrafPtr", "GrafObj")
GrafPtr = OpaqueByValueType("GrafPtr", "GrafObj")
QDErr = OSErrType("QDErr", 'h')

includestuff = includestuff + """
#ifdef WITHOUT_FRAMEWORKS
#include <QDOffscreen.h>
#else
#include <Carbon/Carbon.h>
#endif

#ifdef USE_TOOLBOX_OBJECT_GLUE
extern PyObject *_GWorldObj_New(GWorldPtr);
extern int _GWorldObj_Convert(PyObject *, GWorldPtr *);

#define GWorldObj_New _GWorldObj_New
#define GWorldObj_Convert _GWorldObj_Convert
#endif

#define as_GrafPtr(gworld) ((GrafPtr)(gworld))

"""

initstuff = initstuff + """
	PyMac_INIT_TOOLBOX_OBJECT_NEW(GWorldPtr, GWorldObj_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(GWorldPtr, GWorldObj_Convert);
"""

class MyObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("if (itself == NULL) return PyMac_Error(resNotFound);")
## 	def outputInitStructMembers(self):
## 		GlobalObjectDefinition.outputInitStructMembers(self)
## 		Output("SetWRefCon(itself, (long)it);")
## 	def outputCheckConvertArg(self):
## 		OutLbrace("if (DlgObj_Check(v))")
## 		Output("*p_itself = ((WindowObject *)v)->ob_itself;")
## 		Output("return 1;")
## 		OutRbrace()
## 		Out("""
## 		if (v == Py_None) { *p_itself = NULL; return 1; }
## 		if (PyInt_Check(v)) { *p_itself = (WindowPtr)PyInt_AsLong(v); return 1; }
## 		""")
	def outputFreeIt(self, itselfname):
		Output("DisposeGWorld(%s);", itselfname)
# From here on it's basically all boiler plate...

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)
object = MyObjectDefinition(OBJECTNAME, OBJECTPREFIX, OBJECTTYPE)
module.addobject(object)


# Create the generator classes used to populate the lists
Function = OSErrFunctionGenerator
Method = OSErrMethodGenerator

# Create and populate the lists
functions = []
methods = []
execfile(INPUTFILE)

# A method to convert a GWorldPtr to a GrafPtr
f = Method(GrafPtr, 'as_GrafPtr', (GWorldPtr, 'p', InMode))
methods.append(f)

#
# Manual generator: get data out of a pixmap
pixmapgetbytes_body = """
PixMapHandle pm;
int from, length;
char *cp;

if ( !PyArg_ParseTuple(_args, "O&ii", ResObj_Convert, &pm, &from, &length) )
	return NULL;
cp = GetPixBaseAddr(pm)+from;
return PyString_FromStringAndSize(cp, length);
"""
f = ManualGenerator("GetPixMapBytes", pixmapgetbytes_body)
f.docstring = lambda: """(pixmap, int start, int size) -> string. Return bytes from the pixmap"""
functions.append(f)

# Manual generator: store data in a pixmap
pixmapputbytes_body = """
PixMapHandle pm;
int from, length;
char *cp, *icp;

if ( !PyArg_ParseTuple(_args, "O&is#", ResObj_Convert, &pm, &from, &icp, &length) )
	return NULL;
cp = GetPixBaseAddr(pm)+from;
memcpy(cp, icp, length);
Py_INCREF(Py_None);
return Py_None;
"""
f = ManualGenerator("PutPixMapBytes", pixmapputbytes_body)
f.docstring = lambda: """(pixmap, int start, string data). Store bytes into the pixmap"""
functions.append(f)

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in methods: object.add(f)



# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()
