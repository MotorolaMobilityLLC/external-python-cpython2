# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

import string

# Declarations that change for each manager
MACHEADERFILE = 'Components.h'          # The Apple header file
MODNAME = '_Cm'                         # The name of the module

# The following is *usually* unchanged but may still require tuning
MODPREFIX = 'Cm'                        # The prefix for module-wide routines
C_OBJECTPREFIX = 'CmpObj'       # The prefix for object methods
CI_OBJECTPREFIX = 'CmpInstObj'
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"       # The file generated by this program

from macsupport import *

# Create the type objects

includestuff = includestuff + """
#include <Carbon/Carbon.h>

#ifdef USE_TOOLBOX_OBJECT_GLUE
extern PyObject *_CmpObj_New(Component);
extern int _CmpObj_Convert(PyObject *, Component *);
extern PyObject *_CmpInstObj_New(ComponentInstance);
extern int _CmpInstObj_Convert(PyObject *, ComponentInstance *);

#define CmpObj_New _CmpObj_New
#define CmpObj_Convert _CmpObj_Convert
#define CmpInstObj_New _CmpInstObj_New
#define CmpInstObj_Convert _CmpInstObj_Convert
#endif

/*
** Parse/generate ComponentDescriptor records
*/
static PyObject *
CmpDesc_New(ComponentDescription *itself)
{

        return Py_BuildValue("O&O&O&ll",
                PyMac_BuildOSType, itself->componentType,
                PyMac_BuildOSType, itself->componentSubType,
                PyMac_BuildOSType, itself->componentManufacturer,
                itself->componentFlags, itself->componentFlagsMask);
}

static int
CmpDesc_Convert(PyObject *v, ComponentDescription *p_itself)
{
        return PyArg_ParseTuple(v, "O&O&O&ll",
                PyMac_GetOSType, &p_itself->componentType,
                PyMac_GetOSType, &p_itself->componentSubType,
                PyMac_GetOSType, &p_itself->componentManufacturer,
                &p_itself->componentFlags, &p_itself->componentFlagsMask);
}

"""

initstuff = initstuff + """
        PyMac_INIT_TOOLBOX_OBJECT_NEW(Component, CmpObj_New);
        PyMac_INIT_TOOLBOX_OBJECT_CONVERT(Component, CmpObj_Convert);
        PyMac_INIT_TOOLBOX_OBJECT_NEW(ComponentInstance, CmpInstObj_New);
        PyMac_INIT_TOOLBOX_OBJECT_CONVERT(ComponentInstance, CmpInstObj_Convert);
"""

ComponentDescription = OpaqueType('ComponentDescription', 'CmpDesc')
Component = OpaqueByValueType('Component', C_OBJECTPREFIX)
ComponentInstance = OpaqueByValueType('ComponentInstance', CI_OBJECTPREFIX)
ComponentResult = Type("ComponentResult", "l")

ComponentResourceHandle = OpaqueByValueType("ComponentResourceHandle", "ResObj")

class MyCIObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
    def outputCheckNewArg(self):
        Output("""if (itself == NULL) {
                                PyErr_SetString(Cm_Error,"NULL ComponentInstance");
                                return NULL;
                        }""")

class MyCObjectDefinition(PEP253Mixin, GlobalObjectDefinition):
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
Function = OSErrWeakLinkFunctionGenerator
Method = OSErrWeakLinkMethodGenerator

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
