/* ------------------------------------------------------------------------

   unicodedata -- Provides access to the Unicode 3.0 data base.

   Data was extracted from the Unicode 3.0 UnicodeData.txt file.

   Written by Marc-Andre Lemburg (mal@lemburg.com).
   Modified for Python 2.0 by Fredrik Lundh (fredrik@pythonware.com)

   Copyright (c) Corporation for National Research Initiatives.

   ------------------------------------------------------------------------ */

#include "Python.h"
#include "unicodedatabase.h"

typedef struct {
    const unsigned char category;	/* index into
					   _PyUnicode_CategoryNames */
    const unsigned char	combining; 	/* combining class value 0 - 255 */
    const unsigned char	bidirectional; 	/* index into
					   _PyUnicode_BidirectionalNames */
    const unsigned char mirrored;	/* true if mirrored in bidir mode */
} _PyUnicode_DatabaseRecord;

/* data file generated by Tools/unicode/makeunicodedata.py */
#include "unicodedata_db.h"

static const _PyUnicode_DatabaseRecord*
getrecord(PyUnicodeObject* v)
{
    int code;
    int index;

    code = (int) *PyUnicode_AS_UNICODE(v);

    if (code < 0 || code >= 65536)
        index = 0;
    else {
        index = index1[(code>>SHIFT)];
        index = index2[(index<<SHIFT)+(code&((1<<SHIFT)-1))];
    }

    return &_PyUnicode_Database_Records[index];
}

/* --- Module API --------------------------------------------------------- */

static PyObject *
unicodedata_decimal(PyObject *self, PyObject *args)
{
    PyUnicodeObject *v;
    PyObject *defobj = NULL;
    long rc;

    if (!PyArg_ParseTuple(args, "O!|O:decimal",
			  &PyUnicode_Type, &v, &defobj))
        return NULL;
    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
        return NULL;
    }
    rc = Py_UNICODE_TODECIMAL(*PyUnicode_AS_UNICODE(v));
    if (rc < 0) {
	if (defobj == NULL) {
	    PyErr_SetString(PyExc_ValueError,
			    "not a decimal");
            return NULL;
	}
	else {
	    Py_INCREF(defobj);
	    return defobj;
	}
    }
    return PyInt_FromLong(rc);
}

static PyObject *
unicodedata_digit(PyObject *self, PyObject *args)
{
    PyUnicodeObject *v;
    PyObject *defobj = NULL;
    long rc;

    if (!PyArg_ParseTuple(args, "O!|O:digit",
			  &PyUnicode_Type, &v, &defobj))
        return NULL;
    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
        return NULL;
    }
    rc = Py_UNICODE_TODIGIT(*PyUnicode_AS_UNICODE(v));
    if (rc < 0) {
	if (defobj == NULL) {
	    PyErr_SetString(PyExc_ValueError,
			    "not a digit");
            return NULL;
	}
	else {
	    Py_INCREF(defobj);
	    return defobj;
	}
    }
    return PyInt_FromLong(rc);
}

static PyObject *
unicodedata_numeric(PyObject *self, PyObject *args)
{
    PyUnicodeObject *v;
    PyObject *defobj = NULL;
    double rc;

    if (!PyArg_ParseTuple(args, "O!|O:numeric",
			  &PyUnicode_Type, &v, &defobj))
        return NULL;
    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
	return NULL;
    }
    rc = Py_UNICODE_TONUMERIC(*PyUnicode_AS_UNICODE(v));
    if (rc < 0) {
	if (defobj == NULL) {
	    PyErr_SetString(PyExc_ValueError,
			    "not a numeric character");
	    return NULL;
	}
	else {
	    Py_INCREF(defobj);
	    return defobj;
	}
    }
    return PyFloat_FromDouble(rc);
}

static PyObject *
unicodedata_category(PyObject *self, PyObject *args)
{
    PyUnicodeObject *v;
    int index;

    if (!PyArg_ParseTuple(args, "O!:category",
			  &PyUnicode_Type, &v))
	return NULL;
    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
	return NULL;
    }
    index = (int) getrecord(v)->category;
    return PyString_FromString(_PyUnicode_CategoryNames[index]);
}

static PyObject *
unicodedata_bidirectional(PyObject *self, PyObject *args)
{
    PyUnicodeObject *v;
    int index;

    if (!PyArg_ParseTuple(args, "O!:bidirectional",
			  &PyUnicode_Type, &v))
	return NULL;
    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
	return NULL;
    }
    index = (int) getrecord(v)->bidirectional;
    return PyString_FromString(_PyUnicode_BidirectionalNames[index]);
}

static PyObject *
unicodedata_combining(PyObject *self, PyObject *args)
{
    PyUnicodeObject *v;

    if (!PyArg_ParseTuple(args, "O!:combining",
			  &PyUnicode_Type, &v))
	return NULL;
    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
	return NULL;
    }
    return PyInt_FromLong((int) getrecord(v)->combining);
}

static PyObject *
unicodedata_mirrored(PyObject *self, PyObject *args)
{
    PyUnicodeObject *v;

    if (!PyArg_ParseTuple(args, "O!:mirrored",
			  &PyUnicode_Type, &v))
	return NULL;
    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
	return NULL;
    }
    return PyInt_FromLong((int) getrecord(v)->mirrored);
}

static PyObject *
unicodedata_decomposition(PyObject *self, PyObject *args)
{
    PyUnicodeObject *v;
    char decomp[256];
    int code, index, count, i;

    if (!PyArg_ParseTuple(args, "O!:decomposition",
			  &PyUnicode_Type, &v))
	return NULL;
    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
	return NULL;
    }

    code = (int) *PyUnicode_AS_UNICODE(v);

    if (code < 0 || code >= 65536)
        index = 0;
    else {
        index = decomp_index1[(code>>DECOMP_SHIFT)];
        index = decomp_index2[(index<<DECOMP_SHIFT)+
                             (code&((1<<DECOMP_SHIFT)-1))];
    }

    /* high byte is of hex bytes (usually one or two), low byte
       is prefix code (from*/
    count = decomp_data[index] >> 8;

    /* XXX: could allocate the PyString up front instead
       (strlen(prefix) + 5 * count + 1 bytes) */

    /* copy prefix */
    i = strlen(decomp_prefix[decomp_data[index] & 255]);
    memcpy(decomp, decomp_prefix[decomp_data[index] & 255], i);

    while (count-- > 0) {
        if (i)
            decomp[i++] = ' ';
        sprintf(decomp + i, "%04X", decomp_data[++index]);
        i += strlen(decomp + i);
    }
    
    decomp[i] = '\0';

    return PyString_FromString(decomp);
}

/* XXX Add doc strings. */

static PyMethodDef unicodedata_functions[] = {
    {"decimal",		unicodedata_decimal,			1},
    {"digit",		unicodedata_digit,			1},
    {"numeric",		unicodedata_numeric,			1},
    {"category",	unicodedata_category,			1},
    {"bidirectional",	unicodedata_bidirectional,		1},
    {"combining",	unicodedata_combining,			1},
    {"mirrored",	unicodedata_mirrored,			1},
    {"decomposition",	unicodedata_decomposition,		1},
    {NULL, NULL}		/* sentinel */
};

DL_EXPORT(void)
initunicodedata(void)
{
    Py_InitModule("unicodedata", unicodedata_functions);
}
