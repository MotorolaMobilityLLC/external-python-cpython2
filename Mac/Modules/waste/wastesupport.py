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
ExistingWEReference = OpaqueByValueType("WEReference", "ExistingwasteObj")
WEObjectReference = OpaqueByValueType("WEObjectReference", "WEOObj")
StScrpHandle = OpaqueByValueType("StScrpHandle", "ResObj")
RgnHandle = OpaqueByValueType("RgnHandle", "ResObj")
EventModifiers = Type("EventModifiers", "H")
FlavorType = OSTypeType("FlavorType")
WESelector = OSTypeType("WESelector")

OptHandle = OpaqueByValueType("Handle", "OptResObj")
OptSoupHandle = OpaqueByValueType("WESoupHandle", "OptResObj")
OptStScrpHandle = OpaqueByValueType("StScrpHandle", "OptResObj")

WEStyleMode = Type("WEStyleMode", "H")
WEActionKind = Type("WEActionKind", "h")
WEAlignment = Type("WEAlignment", "b")
WEEdge = Type("WEEdge", "b")
WEDirection = Type("WEDirection", "h")
WESoupHandle = OpaqueByValueType("WESoupHandle", "ResObj")
WEFontTableHandle = OpaqueByValueType("WEFontTableHandle", "ResObj")
WEFontTableHandle
WERunInfo = OpaqueType("WERunInfo", "RunInfo")

AppleEvent = OpaqueType('AppleEvent', 'AEDesc')
AppleEvent_ptr = OpaqueType('AppleEvent', 'AEDesc')

TextStyle = OpaqueType("TextStyle", "TextStyle")
TextStyle_ptr = TextStyle
LongPt = OpaqueType("LongPt", "LongPt")
LongPt_ptr = LongPt
LongRect = OpaqueType("LongRect", "LongRect")
LongRect_ptr = LongRect

includestuff = includestuff + """
#include <%s>""" % MACHEADERFILE + """
#include <WEObjectHandlers.h>
#include <WETabs.h>

/* Exported by Qdmodule.c: */
extern PyObject *QdRGB_New(RGBColor *);
extern int QdRGB_Convert(PyObject *, RGBColor *);

/* Exported by AEModule.c: */
extern PyObject *AEDesc_New(AppleEvent *);
extern int AEDesc_Convert(PyObject *, AppleEvent *);

/* Forward declaration */
staticforward PyObject *WEOObj_New(WEObjectReference);
staticforward PyObject *ExistingwasteObj_New(WEReference);

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

/* Stuff for the callbacks: */
static PyObject *callbackdict;
WENewObjectUPP upp_new_handler;
WEDisposeObjectUPP upp_dispose_handler;
WEDrawObjectUPP upp_draw_handler;
WEClickObjectUPP upp_click_handler;

static OSErr
any_handler(WESelector what, WEObjectReference who, PyObject *args, PyObject **rv)
{
	FlavorType tp;
	PyObject *key, *func;
	
	if ( args == NULL ) return errAECorruptData;
	
	tp = WEGetObjectType(who);
	
	if( (key=Py_BuildValue("O&O&", PyMac_BuildOSType, tp, PyMac_BuildOSType, what)) == NULL)
		return errAECorruptData;
	if( (func = PyDict_GetItem(callbackdict, key)) == NULL ) {
		Py_DECREF(key);
		return errAEHandlerNotFound;
	}
	Py_INCREF(func);
	*rv = PyEval_CallObject(func, args);
	Py_DECREF(func);
	Py_DECREF(key);
	if ( *rv == NULL ) {
		PySys_WriteStderr("--Exception in callback: ");
		PyErr_Print();
		return errAEReplyNotArrived;
	}
	return 0;
}

static pascal OSErr
my_new_handler(Point *objectSize, WEObjectReference objref)
{
	PyObject *args=NULL, *rv=NULL;
	OSErr err;
	
	args=Py_BuildValue("(O&)", WEOObj_New, objref);
	err = any_handler(weNewHandler, objref, args, &rv);
	if (!err) {
		if (!PyMac_GetPoint(rv, objectSize) )
			err = errAECoercionFail;
	}
	if ( args ) Py_DECREF(args);
	if ( rv ) Py_DECREF(rv);
	return err;
}

static pascal OSErr
my_dispose_handler(WEObjectReference objref)
{
	PyObject *args=NULL, *rv=NULL;
	OSErr err;
	
	args=Py_BuildValue("(O&)", WEOObj_New, objref);
	err = any_handler(weDisposeHandler, objref, args, &rv);
	if ( args ) Py_DECREF(args);
	if ( rv ) Py_DECREF(rv);
	return err;
}

static pascal OSErr
my_draw_handler(Rect *destRect, WEObjectReference objref)
{
	PyObject *args=NULL, *rv=NULL;
	OSErr err;
	
	args=Py_BuildValue("O&O&", PyMac_BuildRect, destRect, WEOObj_New, objref);
	err = any_handler(weDrawHandler, objref, args, &rv);
	if ( args ) Py_DECREF(args);
	if ( rv ) Py_DECREF(rv);
	return err;
}

static pascal Boolean
my_click_handler(Point hitPt, EventModifiers modifiers,
		unsigned long clickTime, WEObjectReference objref)
{
	PyObject *args=NULL, *rv=NULL;
	int retvalue;
	OSErr err;
	
	args=Py_BuildValue("O&llO&", PyMac_BuildPoint, hitPt,
			(long)modifiers, (long)clickTime, WEOObj_New, objref);
	err = any_handler(weClickHandler, objref, args, &rv);
	if (!err)
		retvalue = PyInt_AsLong(rv);
	else
		retvalue = 0;
	if ( args ) Py_DECREF(args);
	if ( rv ) Py_DECREF(rv);
	return retvalue;
}
		

"""
finalstuff = finalstuff + """
/* Return the object corresponding to the window, or NULL */

PyObject *
ExistingwasteObj_New(w)
	WEReference w;
{
	PyObject *it = NULL;
	
	if (w == NULL)
		it = NULL;
	else
		WEGetInfo(weRefCon, (void *)&it, w);
	if (it == NULL || ((wasteObject *)it)->ob_itself != w)
		it = Py_None;
	Py_INCREF(it);
	return it;
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
	def outputInitStructMembers(self):
		GlobalObjectDefinition.outputInitStructMembers(self)
		Output("WESetInfo(weRefCon, (void *)&it, itself);")
	def outputFreeIt(self, itselfname):
		Output("WEDispose(%s);", itselfname)
		
class WEOObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					Py_INCREF(Py_None);
					return Py_None;
				}""")
				
variablestuff = """
	callbackdict = PyDict_New();
	if (callbackdict == NULL || PyDict_SetItemString(d, "callbacks", callbackdict) != 0)
		return;
	upp_new_handler = NewWENewObjectProc(my_new_handler);
	upp_dispose_handler = NewWEDisposeObjectProc(my_dispose_handler);
	upp_draw_handler = NewWEDrawObjectProc(my_draw_handler);
	upp_click_handler = NewWEClickObjectProc(my_click_handler);
"""


# From here on it's basically all boiler plate...

# Test types used for existence
## execfile(TYPETESTFILE)

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff, variablestuff)
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

# A function written by hand:
stdhandlers_body = """
	OSErr err;
	// install the sample object handlers for pictures and sounds
#define	kTypePicture			'PICT'
#define	kTypeSound				'snd '
	
	if ( !PyArg_ParseTuple(_args, "") ) return NULL;
	
	if ((err = WEInstallObjectHandler(kTypePicture, weNewHandler,
				(UniversalProcPtr) NewWENewObjectProc(HandleNewPicture), NULL)) != noErr)
		goto cleanup;
	
	if ((err = WEInstallObjectHandler(kTypePicture, weDisposeHandler,
				(UniversalProcPtr) NewWEDisposeObjectProc(HandleDisposePicture), NULL)) != noErr)
		goto cleanup;
	
	if ((err = WEInstallObjectHandler(kTypePicture, weDrawHandler,
				(UniversalProcPtr) NewWEDrawObjectProc(HandleDrawPicture), NULL)) != noErr)
		goto cleanup;
	
	if ((err = WEInstallObjectHandler(kTypeSound, weNewHandler,
				(UniversalProcPtr) NewWENewObjectProc(HandleNewSound), NULL)) != noErr)
		goto cleanup;
	
	if ((err = WEInstallObjectHandler(kTypeSound, weDrawHandler,
				(UniversalProcPtr) NewWEDrawObjectProc(HandleDrawSound), NULL)) != noErr)
		goto cleanup;
	
	if ((err = WEInstallObjectHandler(kTypeSound, weClickHandler,
				(UniversalProcPtr) NewWEClickObjectProc(HandleClickSound), NULL)) != noErr)
		goto cleanup;
	Py_INCREF(Py_None);
	return Py_None;
	
cleanup:
	return PyMac_Error(err);
"""

inshandler_body = """
	OSErr err;
	FlavorType objectType;
	WESelector selector;
	PyObject *py_handler;
	UniversalProcPtr handler;
	WEReference we = NULL;
	PyObject *key;
	
	
	if ( !PyArg_ParseTuple(_args, "O&O&O|O&",
			PyMac_GetOSType, &objectType,
			PyMac_GetOSType, &selector,
			&py_handler,
			WEOObj_Convert, &we) ) return NULL;
			
	if ( selector == weNewHandler ) handler = (UniversalProcPtr)upp_new_handler;
	else if ( selector == weDisposeHandler ) handler = (UniversalProcPtr)upp_dispose_handler;
	else if ( selector == weDrawHandler ) handler = (UniversalProcPtr)upp_draw_handler;
	else if ( selector == weClickHandler ) handler = (UniversalProcPtr)upp_click_handler;
	else return PyMac_Error(weUndefinedSelectorErr);
			
	if ((key = Py_BuildValue("O&O&", 
			PyMac_BuildOSType, objectType, 
			PyMac_BuildOSType, selector)) == NULL )
		return NULL;
		
	PyDict_SetItem(callbackdict, key, py_handler);
	
	err = WEInstallObjectHandler(objectType, selector, handler, we);
	if ( err ) return PyMac_Error(err);
	Py_INCREF(Py_None);
	return Py_None;
"""

stdhand = ManualGenerator("STDObjectHandlers", stdhandlers_body)
inshand = ManualGenerator("WEInstallObjectHandler", inshandler_body)


# Tab hook handlers. Could be parsed from WETabs.h, but this is just as simple.
f = Method(OSErr, 'WEInstallTabHooks', (WEReference, 'we', InMode))
methods.append(f)
f = Method(OSErr, 'WERemoveTabHooks', (WEReference, 'we', InMode))
methods.append(f)
f = Method(Boolean, 'WEIsTabHooks', (WEReference, 'we', InMode))
methods.append(f)
f = Method(SInt16, 'WEGetTabSize', (WEReference, 'we', InMode))
methods.append(f)
f = Method(OSErr, 'WESetTabSize', (SInt16, 'tabWidth', InMode), (WEReference, 'we', InMode))
methods.append(f)

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
module.add(stdhand)
module.add(inshand)
for f in methods: object.add(f)
for f in methods2: object2.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()

