# This script will generate the Resources interface for Python.
# It uses the "bgen" package to generate C code.
# It execs the file resgen.py which contain the function definitions
# (resgen.py was generated by resscan.py, scanning the <Resources.h> header file).

from macsupport import *

class ResMixIn:

    def checkit(self):
        if self.returntype.__class__ != OSErrType:
            OutLbrace()
            Output("OSErr _err = ResError();")
            Output("if (_err != noErr) return PyMac_Error(_err);")
            OutRbrace()
        FunctionGenerator.checkit(self) # XXX

class ResFunction(ResMixIn, OSErrWeakLinkFunctionGenerator): pass
class ResMethod(ResMixIn, OSErrWeakLinkMethodGenerator): pass

RsrcChainLocation = Type("RsrcChainLocation", "h")
FSCatalogInfoBitmap = FakeType("0") # Type("FSCatalogInfoBitmap", "l")
FSCatalogInfo_ptr = FakeType("(FSCatalogInfo *)0")

# includestuff etc. are imported from macsupport

includestuff = includestuff + """
#include <Carbon/Carbon.h>

#ifdef USE_TOOLBOX_OBJECT_GLUE
extern PyObject *_ResObj_New(Handle);
extern int _ResObj_Convert(PyObject *, Handle *);
extern PyObject *_OptResObj_New(Handle);
extern int _OptResObj_Convert(PyObject *, Handle *);
#define ResObj_New _ResObj_New
#define ResObj_Convert _ResObj_Convert
#define OptResObj_New _OptResObj_New
#define OptResObj_Convert _OptResObj_Convert
#endif

/* Function to dispose a resource, with a "normal" calling sequence */
static void
PyMac_AutoDisposeHandle(Handle h)
{
        DisposeHandle(h);
}
"""

finalstuff = finalstuff + """

/* Alternative version of ResObj_New, which returns None for null argument */
PyObject *OptResObj_New(Handle itself)
{
        if (itself == NULL) {
                Py_INCREF(Py_None);
                return Py_None;
        }
        return ResObj_New(itself);
}

int OptResObj_Convert(PyObject *v, Handle *p_itself)
{
        PyObject *tmp;

        if ( v == Py_None ) {
                *p_itself = NULL;
                return 1;
        }
        if (ResObj_Check(v))
        {
                *p_itself = ((ResourceObject *)v)->ob_itself;
                return 1;
        }
        /* If it isn't a resource yet see whether it is convertible */
        if ( (tmp=PyObject_CallMethod(v, "as_Resource", "")) ) {
                *p_itself = ((ResourceObject *)tmp)->ob_itself;
                Py_DECREF(tmp);
                return 1;
        }
        PyErr_Clear();
        PyErr_SetString(PyExc_TypeError, "Resource required");
        return 0;
}
"""

initstuff = initstuff + """
        PyMac_INIT_TOOLBOX_OBJECT_NEW(Handle, ResObj_New);
        PyMac_INIT_TOOLBOX_OBJECT_CONVERT(Handle, ResObj_Convert);
        PyMac_INIT_TOOLBOX_OBJECT_NEW(Handle, OptResObj_New);
        PyMac_INIT_TOOLBOX_OBJECT_CONVERT(Handle, OptResObj_Convert);
"""

module = MacModule('_Res', 'Res', includestuff, finalstuff, initstuff)

class ResDefinition(PEP253Mixin, GlobalObjectDefinition):
    getsetlist = [
            ('data',
            """
            PyObject *res;
            char state;

            state = HGetState(self->ob_itself);
            HLock(self->ob_itself);
            res = PyString_FromStringAndSize(
                    *self->ob_itself,
                    GetHandleSize(self->ob_itself));
            HUnlock(self->ob_itself);
            HSetState(self->ob_itself, state);
            return res;
            """,
            """
            char *data;
            long size;

            if ( v == NULL )
                    return -1;
            if ( !PyString_Check(v) )
                    return -1;
            size = PyString_Size(v);
            data = PyString_AsString(v);
            /* XXXX Do I need the GetState/SetState calls? */
            SetHandleSize(self->ob_itself, size);
            if ( MemError())
                    return -1;
            HLock(self->ob_itself);
            memcpy((char *)*self->ob_itself, data, size);
            HUnlock(self->ob_itself);
            /* XXXX Should I do the Changed call immedeately? */
            return 0;
            """,
            'The resource data'
            ), (
            'size',
            'return PyInt_FromLong(GetHandleSize(self->ob_itself));',
            None,
            'The length of the resource data'
            )]

    def outputCheckNewArg(self):
        Output("if (itself == NULL) return PyMac_Error(resNotFound);")

    def outputCheckConvertArg(self):
        # if it isn't a resource we may be able to coerce it
        Output("if (!%s_Check(v))", self.prefix)
        OutLbrace()
        Output("PyObject *tmp;")
        Output('if ( (tmp=PyObject_CallMethod(v, "as_Resource", "")) )')
        OutLbrace()
        Output("*p_itself = ((ResourceObject *)tmp)->ob_itself;")
        Output("Py_DECREF(tmp);")
        Output("return 1;")
        OutRbrace()
        Output("PyErr_Clear();")
        OutRbrace()

    def outputStructMembers(self):
        GlobalObjectDefinition.outputStructMembers(self)
        Output("void (*ob_freeit)(%s ptr);", self.itselftype)

    def outputInitStructMembers(self):
        GlobalObjectDefinition.outputInitStructMembers(self)
        Output("it->ob_freeit = NULL;")

    def outputCleanupStructMembers(self):
        Output("if (self->ob_freeit && self->ob_itself)")
        OutLbrace()
        Output("self->ob_freeit(self->ob_itself);")
        OutRbrace()
        Output("self->ob_itself = NULL;")

    def output_tp_newBody(self):
        Output("PyObject *self;")
        Output
        Output("if ((self = type->tp_alloc(type, 0)) == NULL) return NULL;")
        Output("((%s *)self)->ob_itself = NULL;", self.objecttype)
        Output("((%s *)self)->ob_freeit = NULL;", self.objecttype)
        Output("return self;")

    def output_tp_initBody(self):
        Output("char *srcdata = NULL;")
        Output("int srclen = 0;")
        Output("%s itself;", self.itselftype);
        Output("char *kw[] = {\"itself\", 0};")
        Output()
        Output("if (PyArg_ParseTupleAndKeywords(args, kwds, \"O&\", kw, %s_Convert, &itself))",
                self.prefix);
        OutLbrace()
        Output("((%s *)self)->ob_itself = itself;", self.objecttype)
        Output("return 0;")
        OutRbrace()
        Output("PyErr_Clear();")
        Output("if (!PyArg_ParseTupleAndKeywords(args, kwds, \"|s#\", kw, &srcdata, &srclen)) return -1;")
        Output("if ((itself = NewHandle(srclen)) == NULL)")
        OutLbrace()
        Output("PyErr_NoMemory();")
        Output("return 0;")
        OutRbrace()
        Output("((%s *)self)->ob_itself = itself;", self.objecttype)
# XXXX          Output("((%s *)self)->ob_freeit = PyMac_AutoDisposeHandle;")
        Output("if (srclen && srcdata)")
        OutLbrace()
        Output("HLock(itself);")
        Output("memcpy(*itself, srcdata, srclen);")
        Output("HUnlock(itself);")
        OutRbrace()
        Output("return 0;")

resobject = ResDefinition('Resource', 'ResObj', 'Handle')
module.addobject(resobject)

functions = []
resmethods = []

execfile('resgen.py')
execfile('resedit.py')

for f in functions: module.add(f)
for f in resmethods: resobject.add(f)

SetOutputFileName('_Resmodule.c')
module.generate()
