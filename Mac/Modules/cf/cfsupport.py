# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

#error missing SetActionFilter

import string

# Declarations that change for each manager
MODNAME = '_CF'				# The name of the module

# The following is *usually* unchanged but may still require tuning
MODPREFIX = 'CF'			# The prefix for module-wide routines
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Special case generator for the functions that have an AllocatorRef first argument,
# which we skip anyway, and the object as the second arg.
class MethodSkipArg1(MethodGenerator):
	"""Similar to MethodGenerator, but has self as last argument"""

	def parseArgumentList(self, args):
		if len(args) < 2:
			raise ValueError, "MethodSkipArg1 expects at least 2 args"
		a0, a1, args = args[0], args[1], args[2:]
		t0, n0, m0 = a0
		if t0 != "CFAllocatorRef" and m0 != InMode:
			raise ValueError, "MethodSkipArg1 should have dummy AllocatorRef first arg"
		t1, n1, m1 = a1
		if m1 != InMode:
			raise ValueError, "method's 'self' must be 'InMode'"
		dummy = Variable(t0, n0, m0)
		self.argumentList.append(dummy)
		self.itself = Variable(t1, "_self->ob_itself", SelfMode)
		self.argumentList.append(self.itself)
		FunctionGenerator.parseArgumentList(self, args)


# Create the type objects

includestuff = includestuff + """
#ifdef WITHOUT_FRAMEWORKS
#include <CFBase.h>
#include <CFArray.h>
#include <CFData.h>
#include <CFDictionary.h>
#include <CFString.h>
#include <CFURL.h>
#else
#include <CoreServices/CoreServices.h>
#endif

/* For now we declare them forward here. They'll go to mactoolbox later */
staticforward PyObject *CFTypeRefObj_New(CFTypeRef);
staticforward int CFTypeRefObj_Convert(PyObject *, CFTypeRef *);
staticforward PyObject *CFStringRefObj_New(CFStringRef);
staticforward int CFStringRefObj_Convert(PyObject *, CFStringRef *);
staticforward PyObject *CFURLRefObj_New(CFURLRef);
staticforward int CFURLRefObj_Convert(PyObject *, CFURLRef *);

staticforward int CFURLRefObj_Convert(PyObject *, CFURLRef *);

// ADD declarations
#ifdef NOTYET_USE_TOOLBOX_OBJECT_GLUE
//extern PyObject *_CFTypeRefObj_New(CFTypeRef);
//extern int _CFTypeRefObj_Convert(PyObject *, CFTypeRef *);

//#define CFTypeRefObj_New _CFTypeRefObj_New
//#define CFTypeRefObj_Convert _CFTypeRefObj_Convert
#endif

/*
** Parse/generate CFRange records
*/
PyObject *CFRange_New(CFRange *itself)
{

	return Py_BuildValue("ll", (long)itself->location, (long)itself->length);
}

CFRange_Convert(PyObject *v, CFRange *p_itself)
{
	long location, length;
	
	if( !PyArg_ParseTuple(v, "ll", &location, &length) )
		return 0;
	p_itself->location = (CFIndex)location;
	p_itself->length = (CFIndex)length;
	return 1;
}

/* Optional CFURL argument or None (passed as NULL) */
int
OptionalCFURLRefObj_Convert(PyObject *v, CFURLRef *p_itself)
{
    if ( v == Py_None ) {
    	p_itself = NULL;
    	return 1;
    }
    return CFURLRefObj_Convert(v, p_itself);
}

"""

initstuff = initstuff + """
//	PyMac_INIT_TOOLBOX_OBJECT_NEW(Track, TrackObj_New);
//	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(Track, TrackObj_Convert);
"""

Boolean = Type("Boolean", "l")
CFTypeID = Type("CFTypeID", "l") # XXXX a guess, seems better than OSTypeType.
CFHashCode = Type("CFHashCode", "l")
CFIndex = Type("CFIndex", "l")
CFRange = OpaqueByValueType('CFRange', 'CFRange')
CFOptionFlags = Type("CFOptionFlags", "l")
CFStringEncoding = Type("CFStringEncoding", "l")
CFComparisonResult = Type("CFComparisonResult", "l")  # a bit dangerous, it's an enum
CFURLPathStyle = Type("CFURLPathStyle", "l") #  a bit dangerous, it's an enum

char_ptr = stringptr
return_stringptr = Type("char *", "s")	# ONLY FOR RETURN VALUES!!

CFAllocatorRef = FakeType("(CFAllocatorRef)NULL")
CFArrayCallBacks_ptr = FakeType("&kCFTypeArrayCallBacks")
CFDictionaryKeyCallBacks_ptr = FakeType("&kCFTypeDictionaryKeyCallBacks")
CFDictionaryValueCallBacks_ptr = FakeType("&kCFTypeDictionaryValueCallBacks")
# The real objects
CFTypeRef = OpaqueByValueType("CFTypeRef", "CFTypeRefObj")
CFArrayRef = OpaqueByValueType("CFArrayRef", "CFArrayRefObj")
CFMutableArrayRef = OpaqueByValueType("CFMutableArrayRef", "CFMutableArrayRefObj")
CFArrayRef = OpaqueByValueType("CFArrayRef", "CFArrayRefObj")
CFMutableArrayRef = OpaqueByValueType("CFMutableArrayRef", "CFMutableArrayRefObj")
CFDataRef = OpaqueByValueType("CFDataRef", "CFDataRefObj")
CFMutableDataRef = OpaqueByValueType("CFMutableDataRef", "CFMutableDataRefObj")
CFDictionaryRef = OpaqueByValueType("CFDictionaryRef", "CFDictionaryRefObj")
CFMutableDictionaryRef = OpaqueByValueType("CFMutableDictionaryRef", "CFMutableDictionaryRefObj")
CFStringRef = OpaqueByValueType("CFStringRef", "CFStringRefObj")
CFMutableStringRef = OpaqueByValueType("CFMutableStringRef", "CFMutableStringRefObj")
CFURLRef = OpaqueByValueType("CFURLRef", "CFURLRefObj")
OptionalCFURLRef  = OpaqueByValueType("CFURLRef", "OptionalCFURLRefObj")
# ADD object type here

# Our (opaque) objects

class MyGlobalObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("if (itself == NULL) return PyMac_Error(resNotFound);")
	def outputStructMembers(self):
		GlobalObjectDefinition.outputStructMembers(self)
		Output("void (*ob_freeit)(CFTypeRef ptr);")
	def outputInitStructMembers(self):
		GlobalObjectDefinition.outputInitStructMembers(self)
##		Output("it->ob_freeit = NULL;")
		Output("it->ob_freeit = CFRelease;")
	def outputCheckConvertArg(self):
		Out("""
		if (v == Py_None) { *p_itself = NULL; return 1; }
		/* Check for other CF objects here */
		""")
	def outputCleanupStructMembers(self):
		Output("if (self->ob_freeit && self->ob_itself)")
		OutLbrace()
		Output("self->ob_freeit((CFTypeRef)self->ob_itself);")
		OutRbrace()
		
	def outputCompare(self):
		Output()
		Output("static int %s_compare(%s *self, %s *other)", self.prefix, self.objecttype, self.objecttype)
		OutLbrace()
		Output("/* XXXX Or should we use CFEqual?? */")
		Output("if ( self->ob_itself > other->ob_itself ) return 1;")
		Output("if ( self->ob_itself < other->ob_itself ) return -1;")
		Output("return 0;")
		OutRbrace()
		
	def outputHash(self):
		Output()
		Output("static int %s_hash(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("/* XXXX Or should we use CFHash?? */")
		Output("return (int)self->ob_itself;")
		OutRbrace()
		
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFTypeRef type-%%d object at 0x%%08.8x for 0x%%08.8x>", CFGetTypeID(self->ob_itself), self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()

class CFTypeRefObjectDefinition(MyGlobalObjectDefinition):
	pass
	
class CFArrayRefObjectDefinition(MyGlobalObjectDefinition):
	basechain = "&CFTypeRefObj_chain"
	
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFArrayRef object at 0x%%08.8x for 0x%%08.8x>", self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()
	
class CFMutableArrayRefObjectDefinition(MyGlobalObjectDefinition):
	basechain = "&CFArrayRefObj_chain"
	
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFMutableArrayRef object at 0x%%08.8x for 0x%%08.8x>", self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()
	
class CFDictionaryRefObjectDefinition(MyGlobalObjectDefinition):
	basechain = "&CFTypeRefObj_chain"
	
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFDictionaryRef object at 0x%%08.8x for 0x%%08.8x>", self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()
	
class CFMutableDictionaryRefObjectDefinition(MyGlobalObjectDefinition):
	basechain = "&CFDictionaryRefObj_chain"
	
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFMutableDictionaryRef object at 0x%%08.8x for 0x%%08.8x>", self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()
	
class CFDataRefObjectDefinition(MyGlobalObjectDefinition):
	basechain = "&CFTypeRefObj_chain"
	
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFDataRef object at 0x%%08.8x for 0x%%08.8x>", self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()
	
class CFMutableDataRefObjectDefinition(MyGlobalObjectDefinition):
	basechain = "&CFDataRefObj_chain"
	
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFMutableDataRef object at 0x%%08.8x for 0x%%08.8x>", self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()

class CFStringRefObjectDefinition(MyGlobalObjectDefinition):
	basechain = "&CFTypeRefObj_chain"
	
	def outputCheckConvertArg(self):
		Out("""
		if (v == Py_None) { *p_itself = NULL; return 1; }
		if (PyString_Check(v)) {
		    char *cStr = PyString_AsString(v);
			*p_itself = CFStringCreateWithCString((CFAllocatorRef)NULL, cStr, 0);
			return 1;
		}
		if (PyUnicode_Check(v)) {
			/* We use the CF types here, if Python was configured differently that will give an error */
			CFIndex size = PyUnicode_GetSize(v);
			UniChar *unichars = PyUnicode_AsUnicode(v);
			if (!unichars) return 0;
			*p_itself = CFStringCreateWithCharacters((CFAllocatorRef)NULL, unichars, size);
			return 1;
		}
			
		""")

	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFStringRef object at 0x%%08.8x for 0x%%08.8x>", self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()

class CFMutableStringRefObjectDefinition(CFStringRefObjectDefinition):
	basechain = "&CFStringRefObj_chain"
	
	def outputCheckConvertArg(self):
		# Mutable, don't allow Python strings
		return MyGlobalObjectDefinition.outputCheckConvertArg(self)
		
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFMutableStringRef object at 0x%%08.8x for 0x%%08.8x>", self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()

class CFURLRefObjectDefinition(MyGlobalObjectDefinition):
	basechain = "&CFTypeRefObj_chain"
	
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFURL object at 0x%%08.8x for 0x%%08.8x>", self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()


# ADD object class here

# From here on it's basically all boiler plate...

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)
CFTypeRef_object = CFTypeRefObjectDefinition('CFTypeRef', 'CFTypeRefObj', 'CFTypeRef')
CFArrayRef_object = CFArrayRefObjectDefinition('CFArrayRef', 'CFArrayRefObj', 'CFArrayRef')
CFMutableArrayRef_object = CFMutableArrayRefObjectDefinition('CFMutableArrayRef', 'CFMutableArrayRefObj', 'CFMutableArrayRef')
CFDictionaryRef_object = CFDictionaryRefObjectDefinition('CFDictionaryRef', 'CFDictionaryRefObj', 'CFDictionaryRef')
CFMutableDictionaryRef_object = CFMutableDictionaryRefObjectDefinition('CFMutableDictionaryRef', 'CFMutableDictionaryRefObj', 'CFMutableDictionaryRef')
CFDataRef_object = CFDataRefObjectDefinition('CFDataRef', 'CFDataRefObj', 'CFDataRef')
CFMutableDataRef_object = CFMutableDataRefObjectDefinition('CFMutableDataRef', 'CFMutableDataRefObj', 'CFMutableDataRef')
CFStringRef_object = CFStringRefObjectDefinition('CFStringRef', 'CFStringRefObj', 'CFStringRef')
CFMutableStringRef_object = CFMutableStringRefObjectDefinition('CFMutableStringRef', 'CFMutableStringRefObj', 'CFMutableStringRef')
CFURLRef_object = CFURLRefObjectDefinition('CFURLRef', 'CFURLRefObj', 'CFURLRef')

# ADD object here

module.addobject(CFTypeRef_object)
module.addobject(CFArrayRef_object)
module.addobject(CFMutableArrayRef_object)
module.addobject(CFDictionaryRef_object)
module.addobject(CFMutableDictionaryRef_object)
module.addobject(CFDataRef_object)
module.addobject(CFMutableDataRef_object)
module.addobject(CFStringRef_object)
module.addobject(CFMutableStringRef_object)
module.addobject(CFURLRef_object)
# ADD addobject call here

# Create the generator classes used to populate the lists
Function = OSErrWeakLinkFunctionGenerator
Method = OSErrWeakLinkMethodGenerator

# Create and populate the lists
functions = []
CFTypeRef_methods = []
CFArrayRef_methods = []
CFMutableArrayRef_methods = []
CFDictionaryRef_methods = []
CFMutableDictionaryRef_methods = []
CFDataRef_methods = []
CFMutableDataRef_methods = []
CFStringRef_methods = []
CFMutableStringRef_methods = []
CFURLRef_methods = []

# ADD _methods initializer here
execfile(INPUTFILE)


# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in CFTypeRef_methods: CFTypeRef_object.add(f)
for f in CFArrayRef_methods: CFArrayRef_object.add(f)
for f in CFMutableArrayRef_methods: CFMutableArrayRef_object.add(f)
for f in CFDictionaryRef_methods: CFDictionaryRef_object.add(f)
for f in CFMutableDictionaryRef_methods: CFMutableDictionaryRef_object.add(f)
for f in CFDataRef_methods: CFDataRef_object.add(f)
for f in CFMutableDataRef_methods: CFMutableDataRef_object.add(f)
for f in CFStringRef_methods: CFStringRef_object.add(f)
for f in CFMutableStringRef_methods: CFMutableStringRef_object.add(f)
for f in CFURLRef_methods: CFURLRef_object.add(f)

# Manual generators for getting data out of strings

getasstring_body = """
int size = CFStringGetLength(_self->ob_itself)+1;
char *data = malloc(size);

if( data == NULL ) return PyErr_NoMemory();
if ( CFStringGetCString(_self->ob_itself, data, size, 0) ) {
	_res = (PyObject *)PyString_FromString(data);
} else {
	PyErr_SetString(PyExc_RuntimeError, "CFStringGetCString could not fit the string");
	_res = NULL;
}
free(data);
return _res;
"""

f = ManualGenerator("CFStringGetString", getasstring_body);
f.docstring = lambda: "() -> (string _rv)"
CFStringRef_object.add(f)

getasunicode_body = """
int size = CFStringGetLength(_self->ob_itself)+1;
Py_UNICODE *data = malloc(size*sizeof(Py_UNICODE));
CFRange range;

range.location = 0;
range.length = size;
if( data == NULL ) return PyErr_NoMemory();
CFStringGetCharacters(_self->ob_itself, range, data);
_res = (PyObject *)PyUnicode_FromUnicode(data, size);
free(data);
return _res;
"""

f = ManualGenerator("CFStringGetUnicode", getasunicode_body);
f.docstring = lambda: "() -> (unicode _rv)"
CFStringRef_object.add(f)

# ADD add forloop here

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()

