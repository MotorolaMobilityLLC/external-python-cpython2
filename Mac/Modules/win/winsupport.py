# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

import string

# Declarations that change for each manager
MACHEADERFILE = 'Windows.h'		# The Apple header file
MODNAME = 'Win'				# The name of the module
OBJECTNAME = 'Window'			# The basic name of the objects used here

# The following is *usually* unchanged but may still require tuning
MODPREFIX = MODNAME			# The prefix for module-wide routines
OBJECTTYPE = OBJECTNAME + 'Ptr'		# The C type used to represent them
OBJECTPREFIX = MODPREFIX + 'Obj'	# The prefix for object methods
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects

WindowPtr = OpaqueByValueType(OBJECTTYPE, OBJECTPREFIX)
WindowPeek = OpaqueByValueType("WindowPeek", OBJECTPREFIX)
WindowPeek.passInput = lambda name: "(WindowPeek)(%s)" % name

#RgnHandle = FakeType("theWindow->updtRgn") # XXX

includestuff = includestuff + """
#include <%s>""" % MACHEADERFILE + """

#define resNotFound -192 /* Can't include <Errors.h> because of Python's "errors.h" */

#ifdef HAVE_UNIVERSAL_HEADERS
#define WindowPeek WindowPtr
#endif
"""

finalstuff = finalstuff + """
/* Return the object corresponding to the window, or NULL */

PyObject *
WinObj_WhichWindow(w)
	WindowPtr w;
{
	PyObject *it;
	
	/* XXX What if we find a stdwin window or a window belonging
	       to some other package? */
	if (w == NULL)
		it = NULL;
	else
		it = (PyObject *) GetWRefCon(w);
	if (it == NULL || ((WindowObject *)it)->ob_itself != w)
		it = Py_None;
	Py_INCREF(it);
	return it;
}
"""

class MyObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("if (itself == NULL) return PyMac_Error(resNotFound);")
	def outputInitStructMembers(self):
		GlobalObjectDefinition.outputInitStructMembers(self)
		Output("SetWRefCon(itself, (long)it);")
	def outputCheckConvertArg(self):
		OutLbrace("if (DlgObj_Check(v))")
		Output("*p_itself = ((WindowObject *)v)->ob_itself;")
		Output("return 1;")
		OutRbrace()
		Out("""
		if (v == Py_None) { *p_itself = NULL; return 1; }
		if (PyInt_Check(v)) { *p_itself = (WindowPtr)PyInt_AsLong(v); return 1; }
		""")
	def outputFreeIt(self, itselfname):
		Output("DisposeWindow(%s);", itselfname)

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

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in methods: object.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()
