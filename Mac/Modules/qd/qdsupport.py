# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

import string

# Declarations that change for each manager
MACHEADERFILE = 'QuickDraw.h'		# The Apple header file
MODNAME = '_Qd'				# The name of the module
OBJECTNAME = 'Graf'			# The basic name of the objects used here

# The following is *usually* unchanged but may still require tuning
MODPREFIX = 'Qd'			# The prefix for module-wide routines
OBJECTTYPE = OBJECTNAME + 'Ptr'		# The C type used to represent them
OBJECTPREFIX = MODPREFIX + 'Obj'	# The prefix for object methods
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
EXTRAFILE = string.lower(MODPREFIX) + 'edit.py' # A similar file but hand-made
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects

class TextThingieClass(FixedInputBufferType):
	def getargsCheck(self, name):
		Output("/* Fool compiler warnings */")
		Output("%s__in_len__ = %s__in_len__;", name, name)

	def declareSize(self, name):
		Output("int %s__in_len__;", name)

TextThingie = TextThingieClass(None)

# These are temporary!
RgnHandle = OpaqueByValueType("RgnHandle", "ResObj")
OptRgnHandle = OpaqueByValueType("RgnHandle", "OptResObj")
PicHandle = OpaqueByValueType("PicHandle", "ResObj")
PolyHandle = OpaqueByValueType("PolyHandle", "ResObj")
PixMapHandle = OpaqueByValueType("PixMapHandle", "ResObj")
PixPatHandle = OpaqueByValueType("PixPatHandle", "ResObj")
PatHandle = OpaqueByValueType("PatHandle", "ResObj")
CursHandle = OpaqueByValueType("CursHandle", "ResObj")
CCrsrHandle = OpaqueByValueType("CCrsrHandle", "ResObj")
CIconHandle = OpaqueByValueType("CIconHandle", "ResObj")
CTabHandle = OpaqueByValueType("CTabHandle", "ResObj")
ITabHandle = OpaqueByValueType("ITabHandle", "ResObj")
GDHandle = OpaqueByValueType("GDHandle", "ResObj")
CGrafPtr = OpaqueByValueType("CGrafPtr", "GrafObj")
GrafPtr = OpaqueByValueType("GrafPtr", "GrafObj")
BitMap_ptr = OpaqueByValueType("BitMapPtr", "BMObj")
const_BitMap_ptr = OpaqueByValueType("const BitMap *", "BMObj")
BitMap = OpaqueType("BitMap", "BMObj_NewCopied", "BUG")
RGBColor = OpaqueType('RGBColor', 'QdRGB')
RGBColor_ptr = RGBColor
FontInfo = OpaqueType('FontInfo', 'QdFI')
Component = OpaqueByValueType('Component', 'CmpObj')
ComponentInstance = OpaqueByValueType('ComponentInstance', 'CmpInstObj')

Cursor = StructOutputBufferType('Cursor')
Cursor_ptr = StructInputBufferType('Cursor')
Pattern = StructOutputBufferType('Pattern')
Pattern_ptr = StructInputBufferType('Pattern')
PenState = StructOutputBufferType('PenState')
PenState_ptr = StructInputBufferType('PenState')
TruncCode = Type("TruncCode", "h")

includestuff = includestuff + """
#ifdef WITHOUT_FRAMEWORKS
#include <QuickDraw.h>
#else
#include <Carbon/Carbon.h>
#endif

#ifdef USE_TOOLBOX_OBJECT_GLUE
extern PyObject *_GrafObj_New(GrafPtr);
extern int _GrafObj_Convert(PyObject *, GrafPtr *);
extern PyObject *_BMObj_New(BitMapPtr);
extern int _BMObj_Convert(PyObject *, BitMapPtr *);
extern PyObject *_QdRGB_New(RGBColorPtr);
extern int _QdRGB_Convert(PyObject *, RGBColorPtr);

#define GrafObj_New _GrafObj_New
#define GrafObj_Convert _GrafObj_Convert
#define BMObj_New _BMObj_New
#define BMObj_Convert _BMObj_Convert
#define QdRGB_New _QdRGB_New
#define QdRGB_Convert _QdRGB_Convert
#endif

#if !ACCESSOR_CALLS_ARE_FUNCTIONS
#define GetPortBitMapForCopyBits(port) ((const struct BitMap *)&((GrafPort *)(port))->portBits)
#define GetPortPixMap(port) (((CGrafPtr)(port))->portPixMap)
#define GetPortBounds(port, bounds) (*(bounds) = (port)->portRect, (bounds))
#define GetPortForeColor(port, color) (*(color) = (port)->rgbFgColor, (color))
#define GetPortBackColor(port, color) (*(color) = (port)->rgbBkColor, (color))
#define GetPortOpColor(port, color) (*(color) = (*(GVarHandle)((port)->grafVars))->rgbOpColor, (color))
#define GetPortHiliteColor(port, color) (*(color) = (*(GVarHandle)((port)->grafVars))->rgbHiliteColor, (color))
#define GetPortTextFont(port) ((port)->txFont)
#define GetPortTextFace(port) ((port)->txFace)
#define GetPortTextMode(port) ((port)->txMode)
#define GetPortTextSize(port) ((port)->txSize)
#define GetPortChExtra(port) ((port)->chExtra)
#define GetPortFracHPenLocation(port) ((port)->pnLocHFrac)
#define GetPortSpExtra(port) ((port)->spExtra)
#define GetPortPenVisibility(port) ((port)->pnVis)
#define GetPortVisibleRegion(port, rgn) ((rgn) = (port)->visRgn, (rgn))
#define GetPortClipRegion(port, rgn) ((rgn) = (port)->clipRgn, (rgn))
#define GetPortBackPixPat(port, pat) ((pat) = (port)->bkPixPat, (pat))
#define GetPortPenPixPat(port, pat) ((pat) = (port)->pnPixPat, (pat))
#define GetPortFillPixPat(port, pat) ((pat) = (port)->fillPixPat, (pat))
#define GetPortPenSize(port, pensize) (*(pensize) = (port)->pnSize, (pensize))
#define GetPortPenMode(port) ((port)->pnMode)
#define GetPortPenLocation(port, location) ((*location) = (port)->pnLoc, (location))
#define IsPortRegionBeingDefined(port) (!!((port)->rgnSave))
#define IsPortPictureBeingDefined(port) (!!((port)->picSave))
/* #define IsPortOffscreen(port) */
/* #define IsPortColor(port) */

#define SetPortBounds(port, bounds) ((port)->portRect = *(bounds))
#define SetPortOpColor(port, color) ((*(GVarHandle)((port)->grafVars))->rgbOpColor = *(color))
#define SetPortVisibleRegion(port, rgn) ((port)->visRgn = (rgn))
#define SetPortClipRegion(port, rgn) ((port)->clipRgn = (rgn))
#define SetPortBackPixPat(port, pat) ((port)->bkPixPat = (pat))
#define SetPortPenPixPat(port, pat) ((port)->pnPixPat = (pat))
#define SetPortFillPixPat(port, pat) ((port)->fillPixPat = (pat))
#define SetPortPenSize(port, pensize) ((port)->pnSize = (pensize))
#define SetPortPenMode(port, mode) ((port)->pnMode = (mode))
#define SetPortFracHPenLocation(port, frac) ((port)->pnLocHFrac = (frac))

/* On pixmaps */
#define GetPixBounds(pixmap, rect) (*(rect) = (*(pixmap))->bounds, (rect))
#define GetPixDepth(pixmap) ((*(pixmap))->pixelSize)

/* On regions */
#define GetRegionBounds(rgn, rect) (*(rect) = (*(rgn))->rgnBBox, (rect))

/* On QD Globals */
#define GetQDGlobalsRandomSeed() (qd.randSeed)
#define GetQDGlobalsScreenBits(bits) (*(bits) = qd.screenBits, (bits))
#define GetQDGlobalsArrow(crsr) (*(crsr) = qd.arrow, (crsr))
#define GetQDGlobalsDarkGray(pat) (*(pat) = qd.dkGray, (pat))
#define GetQDGlobalsLightGray(pat) (*(pat) = qd.ltGray, (pat))
#define GetQDGlobalsGray(pat) (*(pat) = qd.gray, (pat))
#define GetQDGlobalsBlack(pat) (*(pat) = qd.black, (pat))
#define GetQDGlobalsWhite(pat) (*(pat) = qd.white, (pat))
#define GetQDGlobalsThePort() ((CGrafPtr)qd.thePort)

#define SetQDGlobalsRandomSeed(seed) (qd.randSeed = (seed))
#define SetQDGlobalsArrow(crsr) (qd.arrow = *(crsr))

#endif /* ACCESSOR_CALLS_ARE_FUNCTIONS */

static PyObject *BMObj_NewCopied(BitMapPtr);

/*
** Parse/generate RGB records
*/
PyObject *QdRGB_New(RGBColorPtr itself)
{

	return Py_BuildValue("lll", (long)itself->red, (long)itself->green, (long)itself->blue);
}

int QdRGB_Convert(PyObject *v, RGBColorPtr p_itself)
{
	long red, green, blue;
	
	if( !PyArg_ParseTuple(v, "lll", &red, &green, &blue) )
		return 0;
	p_itself->red = (unsigned short)red;
	p_itself->green = (unsigned short)green;
	p_itself->blue = (unsigned short)blue;
	return 1;
}

/*
** Generate FontInfo records
*/
static
PyObject *QdFI_New(FontInfo *itself)
{

	return Py_BuildValue("hhhh", itself->ascent, itself->descent,
			itself->widMax, itself->leading);
}
"""

finalstuff = finalstuff + """
/* Like BMObj_New, but the original bitmap data structure is copied (and
** released when the object is released)
*/
PyObject *BMObj_NewCopied(BitMapPtr itself)
{
	BitMapObject *it;
	BitMapPtr itself_copy;
	
	if ((itself_copy=(BitMapPtr)malloc(sizeof(BitMap))) == NULL)
		return PyErr_NoMemory();
	*itself_copy = *itself;
	it = (BitMapObject *)BMObj_New(itself_copy);
	it->referred_bitmap = itself_copy;
	return (PyObject *)it;
}

"""

variablestuff = ""

initstuff = initstuff + """
	PyMac_INIT_TOOLBOX_OBJECT_NEW(BitMapPtr, BMObj_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(BitMapPtr, BMObj_Convert);
	PyMac_INIT_TOOLBOX_OBJECT_NEW(GrafPtr, GrafObj_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(GrafPtr, GrafObj_Convert);
	PyMac_INIT_TOOLBOX_OBJECT_NEW(RGBColorPtr, QdRGB_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(RGBColor, QdRGB_Convert);
"""

## not yet...
##
##class Region_ObjectDefinition(GlobalObjectDefinition):
##	def outputCheckNewArg(self):
##		Output("if (itself == NULL) return PyMac_Error(resNotFound);")
##	def outputFreeIt(self, itselfname):
##		Output("DisposeRegion(%s);", itselfname)
##
##class Polygon_ObjectDefinition(GlobalObjectDefinition):
##	def outputCheckNewArg(self):
##		Output("if (itself == NULL) return PyMac_Error(resNotFound);")
##	def outputFreeIt(self, itselfname):
##		Output("KillPoly(%s);", itselfname)

class MyGRObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
	getsetlist = [
		('visRgn',
		"""RgnHandle h=NewRgn(); /* XXXX wrong dispose routine */
		return Py_BuildValue("O&", ResObj_New, (Handle)GetPortVisibleRegion(self->ob_itself, h));
		""",
		None,
		"Convenience attribute: return a copy of the visible region"
		), (
		'clipRgn',
		"""RgnHandle h=NewRgn(); /* XXXX wrong dispose routine */
		return Py_BuildValue("O&", ResObj_New, (Handle)GetPortClipRegion(self->ob_itself, h));
		""",
		None,
		"Convenience attribute: return a copy of the clipping region"
		)]
	def outputCheckNewArg(self):
		Output("if (itself == NULL) return PyMac_Error(resNotFound);")
	def outputCheckConvertArg(self):
		Output("#if 1")
		OutLbrace()
		Output("WindowRef win;")
		OutLbrace("if (WinObj_Convert(v, &win) && v)")
		Output("*p_itself = (GrafPtr)GetWindowPort(win);")
		Output("return 1;")
		OutRbrace()
		Output("PyErr_Clear();")
		OutRbrace()
		Output("#else")
		OutLbrace("if (DlgObj_Check(v))")
		Output("DialogRef dlg = (DialogRef)((GrafPortObject *)v)->ob_itself;")
		Output("*p_itself = (GrafPtr)GetWindowPort(GetDialogWindow(dlg));")
		Output("return 1;")
		OutRbrace()
		OutLbrace("if (WinObj_Check(v))")
		Output("WindowRef win = (WindowRef)((GrafPortObject *)v)->ob_itself;")
		Output("*p_itself = (GrafPtr)GetWindowPort(win);")
		Output("return 1;")
		OutRbrace()
		Output("#endif")

class MyBMObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
	getsetlist = [
	(
	'baseAddr',
	'return PyInt_FromLong((long)self->ob_itself->baseAddr);',
	None,
	None
	), (
	'rowBytes',
	'return PyInt_FromLong((long)self->ob_itself->rowBytes);',
	None,
	None
	), (
	'bounds',
	'return Py_BuildValue("O&", PyMac_BuildRect, &self->ob_itself->bounds);',
	None,
	None
	), (
	'bitmap_data',
	'return PyString_FromStringAndSize((char *)self->ob_itself, sizeof(BitMap));',
	None,
	None
	), (
	'pixmap_data',
	'return PyString_FromStringAndSize((char *)self->ob_itself, sizeof(PixMap));',
	None,
	None
	)]
	def outputCheckNewArg(self):
		Output("if (itself == NULL) return PyMac_Error(resNotFound);")
	def outputStructMembers(self):
		# We need to more items: a pointer to privately allocated data
		# and a python object we're referring to.
		Output("%s ob_itself;", self.itselftype)
		Output("PyObject *referred_object;")
		Output("BitMap *referred_bitmap;")
	def outputInitStructMembers(self):
		Output("it->ob_itself = %sitself;", self.argref)
		Output("it->referred_object = NULL;")
		Output("it->referred_bitmap = NULL;")
	def outputCleanupStructMembers(self):
		Output("Py_XDECREF(self->referred_object);")
		Output("if (self->referred_bitmap) free(self->referred_bitmap);")		

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff, variablestuff)
##r_object = Region_ObjectDefinition('Region', 'QdRgn', 'RgnHandle')
##po_object = Polygon_ObjectDefinition('Polygon', 'QdPgn', 'PolyHandle')
##module.addobject(r_object)
##module.addobject(po_object)
gr_object = MyGRObjectDefinition("GrafPort", "GrafObj", "GrafPtr")
module.addobject(gr_object)
bm_object = MyBMObjectDefinition("BitMap", "BMObj", "BitMapPtr")
module.addobject(bm_object)


# Create the generator classes used to populate the lists
Function = OSErrWeakLinkFunctionGenerator
Method = OSErrWeakLinkMethodGenerator

# Create and populate the lists
functions = []
gr_methods = []
bm_methods = []
#methods = []
execfile(INPUTFILE)
execfile(EXTRAFILE)

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in gr_methods: gr_object.add(f)
for f in bm_methods: bm_object.add(f)

# Manual generator: get data out of a bitmap
getdata_body = """
int from, length;
char *cp;

if ( !PyArg_ParseTuple(_args, "ii", &from, &length) )
	return NULL;
cp = _self->ob_itself->baseAddr+from;
_res = PyString_FromStringAndSize(cp, length);
return _res;
"""
f = ManualGenerator("getdata", getdata_body)
f.docstring = lambda: """(int start, int size) -> string. Return bytes from the bitmap"""
bm_object.add(f)

# Manual generator: store data in a bitmap
putdata_body = """
int from, length;
char *cp, *icp;

if ( !PyArg_ParseTuple(_args, "is#", &from, &icp, &length) )
	return NULL;
cp = _self->ob_itself->baseAddr+from;
memcpy(cp, icp, length);
Py_INCREF(Py_None);
_res = Py_None;
return _res;
"""
f = ManualGenerator("putdata", putdata_body)
f.docstring = lambda: """(int start, string data). Store bytes into the bitmap"""
bm_object.add(f)

#
# We manually generate a routine to create a BitMap from python data.
#
BitMap_body = """
BitMap *ptr;
PyObject *source;
Rect bounds;
int rowbytes;
char *data;

if ( !PyArg_ParseTuple(_args, "O!iO&", &PyString_Type, &source, &rowbytes, PyMac_GetRect,
		&bounds) )
	return NULL;
data = PyString_AsString(source);
if ((ptr=(BitMap *)malloc(sizeof(BitMap))) == NULL )
	return PyErr_NoMemory();
ptr->baseAddr = (Ptr)data;
ptr->rowBytes = rowbytes;
ptr->bounds = bounds;
if ( (_res = BMObj_New(ptr)) == NULL ) {
	free(ptr);
	return NULL;
}
((BitMapObject *)_res)->referred_object = source;
Py_INCREF(source);
((BitMapObject *)_res)->referred_bitmap = ptr;
return _res;
"""
	
f = ManualGenerator("BitMap", BitMap_body)
f.docstring = lambda: """Take (string, int, Rect) argument and create BitMap"""
module.add(f)

#
# And again, for turning a correctly-formatted structure into the object
#
RawBitMap_body = """
BitMap *ptr;
PyObject *source;

if ( !PyArg_ParseTuple(_args, "O!", &PyString_Type, &source) )
	return NULL;
if ( PyString_Size(source) != sizeof(BitMap) && PyString_Size(source) != sizeof(PixMap) ) {
	PyErr_Format(PyExc_TypeError, 
		"Argument size was %d, should be %d (sizeof BitMap) or %d (sizeof PixMap)", 
		PyString_Size(source), sizeof(BitMap), sizeof(PixMap));
	return NULL;
}
ptr = (BitMapPtr)PyString_AsString(source);
if ( (_res = BMObj_New(ptr)) == NULL ) {
	return NULL;
}
((BitMapObject *)_res)->referred_object = source;
Py_INCREF(source);
return _res;
"""
	
f = ManualGenerator("RawBitMap", RawBitMap_body)
f.docstring = lambda: """Take string BitMap and turn into BitMap object"""
module.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()
SetOutputFile() # Close it
