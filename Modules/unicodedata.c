/* ------------------------------------------------------------------------

   unicodedata -- Provides access to the Unicode 3.0 data base.

   Data was extracted from the Unicode 3.0 UnicodeData.txt file.

   Written by Marc-Andre Lemburg (mal@lemburg.com).
   Modified for Python 2.0 by Fredrik Lundh (fredrik@pythonware.com)

   Copyright (c) Corporation for National Research Initiatives.

   ------------------------------------------------------------------------ */

#include "Python.h"
#include "ucnhash.h"

/* character properties */

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

    if (!PyArg_ParseTuple(args, "O!|O:decimal", &PyUnicode_Type, &v, &defobj))
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

    if (!PyArg_ParseTuple(args, "O!|O:digit", &PyUnicode_Type, &v, &defobj))
        return NULL;
    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
        return NULL;
    }
    rc = Py_UNICODE_TODIGIT(*PyUnicode_AS_UNICODE(v));
    if (rc < 0) {
	if (defobj == NULL) {
	    PyErr_SetString(PyExc_ValueError, "not a digit");
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

    if (!PyArg_ParseTuple(args, "O!|O:numeric", &PyUnicode_Type, &v, &defobj))
        return NULL;
    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
	return NULL;
    }
    rc = Py_UNICODE_TONUMERIC(*PyUnicode_AS_UNICODE(v));
    if (rc < 0) {
	if (defobj == NULL) {
	    PyErr_SetString(PyExc_ValueError, "not a numeric character");
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

/* -------------------------------------------------------------------- */
/* unicode character name tables */

/* data file generated by Tools/unicode/makeunicodedata.py */
#include "unicodename_db.h"

/* -------------------------------------------------------------------- */
/* database code (cut and pasted from the unidb package) */

static unsigned long
gethash(const char *s, int len, int scale)
{
    int i;
    unsigned long h = 0;
    unsigned long ix;
    for (i = 0; i < len; i++) {
        h = (h * scale) + (unsigned char) toupper(s[i]);
        ix = h & 0xff000000;
        if (ix)
            h = (h ^ ((ix>>24) & 0xff)) & 0x00ffffff;
    }
    return h;
}

static int
getname(Py_UCS4 code, char* buffer, int buflen)
{
    int offset;
    int i;
    int word;
    unsigned char* w;

    if (code < 0 || code >= 65536)
        return 0;

    /* get offset into phrasebook */
    offset = phrasebook_offset1[(code>>phrasebook_shift)];
    offset = phrasebook_offset2[(offset<<phrasebook_shift) +
                               (code&((1<<phrasebook_shift)-1))];
    if (!offset)
        return 0;

    i = 0;

    for (;;) {
        /* get word index */
        word = phrasebook[offset] - phrasebook_short;
        if (word >= 0) {
            word = (word << 8) + phrasebook[offset+1];
            offset += 2;
        } else
            word = phrasebook[offset++];
        if (i) {
            if (i > buflen)
                return 0; /* buffer overflow */
            buffer[i++] = ' ';
        }
        /* copy word string from lexicon.  the last character in the
           word has bit 7 set.  the last word in a string ends with
           0x80 */
        w = lexicon + lexicon_offset[word];
        while (*w < 128) {
            if (i >= buflen)
                return 0; /* buffer overflow */
            buffer[i++] = *w++;
        }
        if (i >= buflen)
            return 0; /* buffer overflow */
        buffer[i++] = *w & 127;
        if (*w == 128)
            break; /* end of word */
    }

    return 1;
}

static int
cmpname(int code, const char* name, int namelen)
{
    /* check if code corresponds to the given name */
    int i;
    char buffer[NAME_MAXLEN];
    if (!getname(code, buffer, sizeof(buffer)))
        return 0;
    for (i = 0; i < namelen; i++) {
        if (toupper(name[i]) != buffer[i])
            return 0;
    }
    return buffer[namelen] == '\0';
}

static int
getcode(const char* name, int namelen, Py_UCS4* code)
{
    unsigned int h, v;
    unsigned int mask = code_size-1;
    unsigned int i, incr;

    /* the following is the same as python's dictionary lookup, with
       only minor changes.  see the makeunicodedata script for more
       details */

    h = (unsigned int) gethash(name, namelen, code_magic);
    i = (~h) & mask;
    v = code_hash[i];
    if (!v)
        return 0;
    if (cmpname(v, name, namelen)) {
        *code = v;
        return 1;
    }
    incr = (h ^ (h >> 3)) & mask;
    if (!incr)
        incr = mask;
    for (;;) {
        i = (i + incr) & mask;
        v = code_hash[i];
        if (!v)
            return 0;
        if (cmpname(v, name, namelen)) {
            *code = v;
            return 1;
        }
        incr = incr << 1;
        if (incr > mask)
            incr = incr ^ code_poly;
    }
}

static const _PyUnicode_Name_CAPI hashAPI = 
{
    sizeof(_PyUnicode_Name_CAPI),
    getname,
    getcode
};

/* -------------------------------------------------------------------- */
/* Python bindings */

static PyObject *
unicodedata_name(PyObject* self, PyObject* args)
{
    char name[NAME_MAXLEN];

    PyUnicodeObject* v;
    PyObject* defobj = NULL;
    if (!PyArg_ParseTuple(args, "O!|O:name", &PyUnicode_Type, &v, &defobj))
        return NULL;

    if (PyUnicode_GET_SIZE(v) != 1) {
	PyErr_SetString(PyExc_TypeError,
			"need a single Unicode character as parameter");
	return NULL;
    }

    if (!getname((Py_UCS4) *PyUnicode_AS_UNICODE(v), name, sizeof(name))) {
	if (defobj == NULL) {
	    PyErr_SetString(PyExc_ValueError, "no such name");
            return NULL;
	}
	else {
	    Py_INCREF(defobj);
	    return defobj;
	}
    }

    return Py_BuildValue("s", name);
}

static PyObject *
unicodedata_lookup(PyObject* self, PyObject* args)
{
    Py_UCS4 code;
    Py_UNICODE str[1];

    char* name;
    int namelen;
    if (!PyArg_ParseTuple(args, "s#:lookup", &name, &namelen))
        return NULL;

    if (!getcode(name, namelen, &code)) {
        PyErr_SetString(PyExc_KeyError, "undefined character name");
        return NULL;
    }

    str[0] = (Py_UNICODE) code;
    return PyUnicode_FromUnicode(str, 1);
}

/* XXX Add doc strings. */

static PyMethodDef unicodedata_functions[] = {
    {"decimal", unicodedata_decimal, METH_VARARGS},
    {"digit", unicodedata_digit, METH_VARARGS},
    {"numeric", unicodedata_numeric, METH_VARARGS},
    {"category", unicodedata_category, METH_VARARGS},
    {"bidirectional", unicodedata_bidirectional, METH_VARARGS},
    {"combining", unicodedata_combining, METH_VARARGS},
    {"mirrored", unicodedata_mirrored, METH_VARARGS},
    {"decomposition",unicodedata_decomposition, METH_VARARGS},
    {"name", unicodedata_name, METH_VARARGS},
    {"lookup", unicodedata_lookup, METH_VARARGS},
    {NULL, NULL}		/* sentinel */
};

static char *unicodedata_docstring = "unicode character database";

DL_EXPORT(void)
initunicodedata(void)
{
    PyObject *m, *d, *v;

    m = Py_InitModule4(
        "unicodedata", unicodedata_functions,
        unicodedata_docstring, NULL, PYTHON_API_VERSION);
    if (!m)
        return;

    d = PyModule_GetDict(m);
    if (!d)
        return;

    /* Export C API */
    v = PyCObject_FromVoidPtr((void *) &hashAPI, NULL);
    PyDict_SetItemString(d, "ucnhash_CAPI", v);
    Py_XDECREF(v);

}
