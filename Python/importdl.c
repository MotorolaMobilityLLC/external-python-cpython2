
/* Support for dynamic loading of extension modules */

#include "Python.h"

/* ./configure sets HAVE_DYNAMIC_LOADING if dynamic loading of modules is
   supported on this platform. configure will then compile and link in one
   of the dynload_*.c files, as appropriate. We will call a function in
   those modules to get a function pointer to the module's init function.
*/
#ifdef HAVE_DYNAMIC_LOADING

#include "importdl.h"

extern dl_funcptr _PyImport_GetDynLoadFunc(const char *shortname,
                                           const char *pathname, FILE *fp);



PyObject *
_PyImport_LoadDynamicModule(char *name, char *pathname, FILE *fp)
{
    PyObject *m;
    PyObject *path;
    char *lastdot, *shortname, *packagecontext, *oldcontext;
    dl_funcptr p0;
    PyObject* (*p)(void);
    struct PyModuleDef *def;
    PyObject *nameobj, *result;

    path = PyUnicode_DecodeFSDefault(pathname);
    if (path == NULL)
        return NULL;

    nameobj = PyUnicode_FromString(name);
    if (nameobj == NULL)
        return NULL;
    m = _PyImport_FindExtensionObject(nameobj, path);
    if (m != NULL) {
        Py_DECREF(nameobj);
        Py_INCREF(m);
        result = m;
        goto finally;
    }
    Py_DECREF(nameobj);
    lastdot = strrchr(name, '.');
    if (lastdot == NULL) {
        packagecontext = NULL;
        shortname = name;
    }
    else {
        packagecontext = name;
        shortname = lastdot+1;
    }

    p0 = _PyImport_GetDynLoadFunc(shortname, pathname, fp);
    p = (PyObject*(*)(void))p0;
    if (PyErr_Occurred())
        goto error;
    if (p == NULL) {
        PyErr_Format(PyExc_ImportError,
           "dynamic module does not define init function (PyInit_%.200s)",
                     shortname);
        goto error;
    }
    oldcontext = _Py_PackageContext;
    _Py_PackageContext = packagecontext;
    m = (*p)();
    _Py_PackageContext = oldcontext;
    if (m == NULL)
        goto error;

    if (PyErr_Occurred()) {
        Py_DECREF(m);
        PyErr_Format(PyExc_SystemError,
                     "initialization of %s raised unreported exception",
                     shortname);
        goto error;
    }

    /* Remember pointer to module init function. */
    def = PyModule_GetDef(m);
    def->m_base.m_init = p;

    /* Remember the filename as the __file__ attribute */
    if (PyModule_AddObject(m, "__file__", path) < 0)
        PyErr_Clear(); /* Not important enough to report */
    else
        Py_INCREF(path);

    nameobj = PyUnicode_FromString(name);
    if (nameobj == NULL)
        return NULL;
    if (_PyImport_FixupExtensionObject(m, nameobj, path) < 0) {
        Py_DECREF(nameobj);
        goto error;
    }
    if (Py_VerboseFlag)
        PySys_FormatStderr(
            "import %U # dynamically loaded from %s\n",
            nameobj, pathname);
    Py_DECREF(nameobj);
    result = m;
    goto finally;

error:
    result = NULL;
finally:
    Py_DECREF(path);
    return result;
}

#endif /* HAVE_DYNAMIC_LOADING */
