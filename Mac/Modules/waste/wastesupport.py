# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

import string

# Declarations that change for each manager
MACHEADERFILE = 'WASTE.h'		# The Apple header file
MODNAME = 'waste'				# The name of the module
OBJECTNAME = 'waste'			# The basic name of the objects used here
KIND = 'Ptr'				# Usually 'Ptr' or 'Handle'

# The following is *usually* unchanged but may still require tuning
MODPREFIX = MODNAME			# The prefix for module-wide routines
OBJECTTYPE = "WEReference"		# The C type used to represent them
OBJECTPREFIX = MODPREFIX + 'Obj'	# The prefix for object methods
INPUTFILE = 'wastegen.py' # The file generated by the scanner
TYPETESTFILE = 'wastetypetest.py'	# Another file generated by the scanner
OUTPUTFILE = "wastemodule.c"	# The file generated by this program

from macsupport import *

# Create the type objects
WEReference = OpaqueByValueType("WEReference", "wasteObj")
WEObjectReference = OpaqueByValueType("WEObjectReference", "WEOObj")
StScrpHandle = OpaqueByValueType("StScrpHandle", "ResObj")
RgnHandle = OpaqueByValueType("RgnHandle", "ResObj")
EventModifiers = Type("EventModifiers", "h")
FlavorType = OSTypeType("FlavorType")
WESelector = OSTypeType("WESelector")

OptHandle = OpaqueByValueType("Handle", "OptResObj")
OptSoupHandle = OpaqueByValueType("WESoupHandle", "OptResObj")
OptStScrpHandle = OpaqueByValueType("StScrpHandle", "OptResObj")

WEStyleMode = Type("WEStyleMode", "h")
WEActionKind = Type("WEActionKind", "h")
WEAlignment = Type("WEAlignment", "b")
WESoupHandle = OpaqueByValueType("WESoupHandle", "ResObj")
WERunInfo = OpaqueType("WERunInfo", "RunInfo")

TextStyle = OpaqueType("TextStyle", "TextStyle")
TextStyle_ptr = TextStyle
LongPt = OpaqueType("LongPt", "LongPt")
LongPt_ptr = LongPt
LongRect = OpaqueType("LongRect", "LongRect")
LongRect_ptr = LongRect

includestuff = includestuff + """
#include <%s>""" % MACHEADERFILE + """

/* Exported by Qdmodule.c: */
extern PyObject *QdRGB_New(RGBColor *);
extern int QdRGB_Convert(PyObject *, RGBColor *);

/* Forward declaration */
staticforward PyObject *WEOObj_New(WEObjectReference);

/*
** Parse/generate TextStyle records
*/
static
PyObject *TextStyle_New(itself)
	TextStylePtr itself;
{

	return Py_BuildValue("lllO&", (long)itself->tsFont, (long)itself->tsFace, (long)itself->tsSize, QdRGB_New,
				&itself->tsColor);
}

static
TextStyle_Convert(v, p_itself)
	PyObject *v;
	TextStylePtr p_itself;
{
	long font, face, size;
	
	if( !PyArg_ParseTuple(v, "lllO&", &font, &face, &size, QdRGB_Convert, &p_itself->tsColor) )
		return 0;
	p_itself->tsFont = (short)font;
	p_itself->tsFace = (Style)face;
	p_itself->tsSize = (short)size;
	return 1;
}

/*
** Parse/generate RunInfo records
*/
static
PyObject *RunInfo_New(itself)
	WERunInfo *itself;
{

	return Py_BuildValue("llhhO&O&", itself->runStart, itself->runEnd, itself->runHeight,
		itself->runAscent, TextStyle_New, &itself->runStyle, WEOObj_New, itself->runObject);
}

/* Conversion of long points and rects */
int
LongRect_Convert(PyObject *v, LongRect *r)
{
	return PyArg_Parse(v, "(llll)", &r->left, &r->top, &r->right, &r->bottom);
}

PyObject *
LongRect_New(LongRect *r)
{
	return Py_BuildValue("(llll)", r->left, r->top, r->right, r->bottom);
}


LongPt_Convert(PyObject *v, LongPt *p)
{
	return PyArg_Parse(v, "(ll)", &p->h, &p->v);
}

PyObject *
LongPt_New(LongPt *p)
{
	return Py_BuildValue("(ll)", p->h, p->v);
}
"""

class WEMethodGenerator(OSErrMethodGenerator):
	"""Similar to MethodGenerator, but has self as last argument"""

	def parseArgumentList(self, args):
		args, a0 = args[:-1], args[-1]
		t0, n0, m0 = a0
		if m0 != InMode:
			raise ValueError, "method's 'self' must be 'InMode'"
		self.itself = Variable(t0, "_self->ob_itself", SelfMode)
		FunctionGenerator.parseArgumentList(self, args)
		self.argumentList.append(self.itself)



class WEObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(waste_Error,"Cannot create null WE");
					return NULL;
				}""")
	def outputFreeIt(self, itselfname):
		Output("WEDispose(%s);", itselfname)
		
class WEOObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					Py_INCREF(Py_None);
					return Py_None;
				}""")		

# From here on it's basically all boiler plate...

# Test types used for existence
## execfile(TYPETESTFILE)

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)
object = WEObjectDefinition(OBJECTNAME, OBJECTPREFIX, OBJECTTYPE)
object2 = WEOObjectDefinition("WEO", "WEOObj", "WEObjectReference")
module.addobject(object2)
module.addobject(object)

# Create the generator classes used to populate the lists
Function = OSErrFunctionGenerator
Method = WEMethodGenerator
Method2 = OSErrMethodGenerator

# Create and populate the lists
functions = []
methods = []
methods2 = []
execfile(INPUTFILE)

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in methods: object.add(f)
for f in methods2: object2.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()

