# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

import string

# Declarations that change for each manager
MACHEADERFILE = 'Components.h'		# The Apple header file
MODNAME = 'Cm'				# The name of the module

# The following is *usually* unchanged but may still require tuning
MODPREFIX = MODNAME			# The prefix for module-wide routines
C_OBJECTPREFIX = 'CmpObj'	# The prefix for object methods
CI_OBJECTPREFIX = 'CmpInstObj'
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects

includestuff = includestuff + """
#include <%s>""" % MACHEADERFILE + """

/*
** Parse/generate ComponentDescriptor records
*/
PyObject *CmpDesc_New(itself)
	ComponentDescription *itself;
{

	return Py_BuildValue("O&O&O&ll", 
		PyMac_BuildOSType, itself->componentType,
		PyMac_BuildOSType, itself->componentSubType,
		PyMac_BuildOSType, itself->componentManufacturer,
		itself->componentFlags, itself->componentFlagsMask);
}

CmpDesc_Convert(v, p_itself)
	PyObject *v;
	ComponentDescription *p_itself;
{
	return PyArg_ParseTuple(v, "O&O&O&ll",
		PyMac_GetOSType, &p_itself->componentType,
		PyMac_GetOSType, &p_itself->componentSubType,
		PyMac_GetOSType, &p_itself->componentManufacturer,
		&p_itself->componentFlags, &p_itself->componentFlagsMask);
}

"""

ComponentDescription = OpaqueType('ComponentDescription', 'CmpDesc')
Component = OpaqueByValueType('Component', C_OBJECTPREFIX)
ComponentInstance = OpaqueByValueType('ComponentInstance', CI_OBJECTPREFIX)
ComponentResult = Type("ComponentResult", "l")

ComponentResourceHandle = OpaqueByValueType("ComponentResourceHandle", "ResObj")

class MyCIObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					PyErr_SetString(Cm_Error,"NULL ComponentInstance");
					return NULL;
				}""")

class MyCObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("""if (itself == NULL) {
					/* XXXX Or should we return None? */
					PyErr_SetString(Cm_Error,"No such component");
					return NULL;
				}""")
				
	def outputCheckConvertArg(self):
		Output("""if ( v == Py_None ) {
					*p_itself = 0;
					return 1;
		}""")

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)
ci_object = MyCIObjectDefinition('ComponentInstance', CI_OBJECTPREFIX,
		'ComponentInstance')
c_object = MyCObjectDefinition('Component', C_OBJECTPREFIX, 'Component')
module.addobject(ci_object)
module.addobject(c_object)

# Create the generator classes used to populate the lists
Function = OSErrFunctionGenerator
Method = OSErrMethodGenerator

# Create and populate the lists
functions = []
c_methods = []
ci_methods = []
execfile(INPUTFILE)

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in c_methods: c_object.add(f)
for f in ci_methods: ci_object.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()

