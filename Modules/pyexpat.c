#include "Python.h"
#include <ctype.h>

#include "compile.h"
#include "frameobject.h"
#include "expat.h"

#define XML_COMBINED_VERSION (10000*XML_MAJOR_VERSION+100*XML_MINOR_VERSION+XML_MICRO_VERSION)

#ifndef PyDoc_STRVAR

/*
 * fdrake says:
 * Don't change the PyDoc_STR macro definition to (str), because
 * '''the parentheses cause compile failures
 * ("non-constant static initializer" or something like that)
 * on some platforms (Irix?)'''
 */
#define PyDoc_STR(str)         str
#define PyDoc_VAR(name)        static char name[]
#define PyDoc_STRVAR(name,str) PyDoc_VAR(name) = PyDoc_STR(str)
#endif

#if (PY_MAJOR_VERSION == 2 && PY_MINOR_VERSION < 2)
/* In Python 2.0 and  2.1, disabling Unicode was not possible. */
#define Py_USING_UNICODE
#define NOFIX_TRACE
#endif

enum HandlerTypes {
    StartElement,
    EndElement,
    ProcessingInstruction,
    CharacterData,
    UnparsedEntityDecl,
    NotationDecl,
    StartNamespaceDecl,
    EndNamespaceDecl,
    Comment,
    StartCdataSection,
    EndCdataSection,
    Default,
    DefaultHandlerExpand,
    NotStandalone,
    ExternalEntityRef,
    StartDoctypeDecl,
    EndDoctypeDecl,
    EntityDecl,
    XmlDecl,
    ElementDecl,
    AttlistDecl,
#if XML_COMBINED_VERSION >= 19504
    SkippedEntity,
#endif
    _DummyDecl
};

static PyObject *ErrorObject;

/* ----------------------------------------------------- */

/* Declarations for objects of type xmlparser */

typedef struct {
    PyObject_HEAD

    XML_Parser itself;
    int returns_unicode;        /* True if Unicode strings are returned;
                                   if false, UTF-8 strings are returned */
    int ordered_attributes;     /* Return attributes as a list. */
    int specified_attributes;   /* Report only specified attributes. */
    int in_callback;            /* Is a callback active? */
    int ns_prefixes;            /* Namespace-triplets mode? */
    XML_Char *buffer;           /* Buffer used when accumulating characters */
                                /* NULL if not enabled */
    int buffer_size;            /* Size of buffer, in XML_Char units */
    int buffer_used;            /* Buffer units in use */
    PyObject *intern;           /* Dictionary to intern strings */
    PyObject **handlers;
} xmlparseobject;

#define CHARACTER_DATA_BUFFER_SIZE 8192

static PyTypeObject Xmlparsetype;

typedef void (*xmlhandlersetter)(XML_Parser self, void *meth);
typedef void* xmlhandler;

struct HandlerInfo {
    const char *name;
    xmlhandlersetter setter;
    xmlhandler handler;
    PyCodeObject *tb_code;
    PyObject *nameobj;
};

static struct HandlerInfo handler_info[64];

/* Set an integer attribute on the error object; return true on success,
 * false on an exception.
 */
static int
set_error_attr(PyObject *err, char *name, int value)
{
    PyObject *v = PyInt_FromLong(value);

    if (v != NULL && PyObject_SetAttrString(err, name, v) == -1) {
        Py_DECREF(v);
        return 0;
    }
    return 1;
}

/* Build and set an Expat exception, including positioning
 * information.  Always returns NULL.
 */
static PyObject *
set_error(xmlparseobject *self, enum XML_Error code)
{
    PyObject *err;
    char buffer[256];
    XML_Parser parser = self->itself;
    int lineno = XML_GetErrorLineNumber(parser);
    int column = XML_GetErrorColumnNumber(parser);

    /* There is no risk of overflowing this buffer, since
       even for 64-bit integers, there is sufficient space. */
    sprintf(buffer, "%.200s: line %i, column %i",
            XML_ErrorString(code), lineno, column);
    err = PyObject_CallFunction(ErrorObject, "s", buffer);
    if (  err != NULL
          && set_error_attr(err, "code", code)
          && set_error_attr(err, "offset", column)
          && set_error_attr(err, "lineno", lineno)) {
        PyErr_SetObject(ErrorObject, err);
    }
    return NULL;
}

static int
have_handler(xmlparseobject *self, int type)
{
    PyObject *handler = self->handlers[type];
    return handler != NULL;
}

static PyObject *
get_handler_name(struct HandlerInfo *hinfo)
{
    PyObject *name = hinfo->nameobj;
    if (name == NULL) {
        name = PyString_FromString(hinfo->name);
        hinfo->nameobj = name;
    }
    Py_XINCREF(name);
    return name;
}


#ifdef Py_USING_UNICODE
/* Convert a string of XML_Chars into a Unicode string.
   Returns None if str is a null pointer. */

static PyObject *
conv_string_to_unicode(const XML_Char *str)
{
    /* XXX currently this code assumes that XML_Char is 8-bit,
       and hence in UTF-8.  */
    /* UTF-8 from Expat, Unicode desired */
    if (str == NULL) {
        Py_INCREF(Py_None);
        return Py_None;
    }
    return PyUnicode_DecodeUTF8(str, strlen(str), "strict");
}

static PyObject *
conv_string_len_to_unicode(const XML_Char *str, int len)
{
    /* XXX currently this code assumes that XML_Char is 8-bit,
       and hence in UTF-8.  */
    /* UTF-8 from Expat, Unicode desired */
    if (str == NULL) {
        Py_INCREF(Py_None);
        return Py_None;
    }
    return PyUnicode_DecodeUTF8((const char *)str, len, "strict");
}
#endif

/* Convert a string of XML_Chars into an 8-bit Python string.
   Returns None if str is a null pointer. */

static PyObject *
conv_string_to_utf8(const XML_Char *str)
{
    /* XXX currently this code assumes that XML_Char is 8-bit,
       and hence in UTF-8.  */
    /* UTF-8 from Expat, UTF-8 desired */
    if (str == NULL) {
        Py_INCREF(Py_None);
        return Py_None;
    }
    return PyString_FromString(str);
}

static PyObject *
conv_string_len_to_utf8(const XML_Char *str, int len)
{
    /* XXX currently this code assumes that XML_Char is 8-bit,
       and hence in UTF-8.  */
    /* UTF-8 from Expat, UTF-8 desired */
    if (str == NULL) {
        Py_INCREF(Py_None);
        return Py_None;
    }
    return PyString_FromStringAndSize((const char *)str, len);
}

/* Callback routines */

static void clear_handlers(xmlparseobject *self, int initial);

/* This handler is used when an error has been detected, in the hope
   that actual parsing can be terminated early.  This will only help
   if an external entity reference is encountered. */
static int
error_external_entity_ref_handler(XML_Parser parser,
                                  const XML_Char *context,
                                  const XML_Char *base,
                                  const XML_Char *systemId,
                                  const XML_Char *publicId)
{
    return 0;
}

static void
flag_error(xmlparseobject *self)
{
    clear_handlers(self, 0);
    XML_SetExternalEntityRefHandler(self->itself,
                                    error_external_entity_ref_handler);
}

static PyCodeObject*
getcode(enum HandlerTypes slot, char* func_name, int lineno)
{
    PyObject *code = NULL;
    PyObject *name = NULL;
    PyObject *nulltuple = NULL;
    PyObject *filename = NULL;

    if (handler_info[slot].tb_code == NULL) {
        code = PyString_FromString("");
        if (code == NULL)
            goto failed;
        name = PyString_FromString(func_name);
        if (name == NULL)
            goto failed;
        nulltuple = PyTuple_New(0);
        if (nulltuple == NULL)
            goto failed;
        filename = PyString_FromString(__FILE__);
        handler_info[slot].tb_code =
            PyCode_New(0,		/* argcount */
                       0,		/* nlocals */
                       0,		/* stacksize */
                       0,		/* flags */
                       code,		/* code */
                       nulltuple,	/* consts */
                       nulltuple,	/* names */
                       nulltuple,	/* varnames */
#if PYTHON_API_VERSION >= 1010
                       nulltuple,	/* freevars */
                       nulltuple,	/* cellvars */
#endif
                       filename,	/* filename */
                       name,		/* name */
                       lineno,		/* firstlineno */
                       code		/* lnotab */
                       );
        if (handler_info[slot].tb_code == NULL)
            goto failed;
        Py_DECREF(code);
        Py_DECREF(nulltuple);
        Py_DECREF(filename);
        Py_DECREF(name);
    }
    return handler_info[slot].tb_code;
 failed:
    Py_XDECREF(code);
    Py_XDECREF(name);
    return NULL;
}

#ifndef NOFIX_TRACE
static int
trace_frame(PyThreadState *tstate, PyFrameObject *f, int code, PyObject *val)
{
    int result = 0;
    if (!tstate->use_tracing || tstate->tracing)
	return 0;
    if (tstate->c_profilefunc != NULL) {
	tstate->tracing++;
	result = tstate->c_profilefunc(tstate->c_profileobj,
				       f, code , val);
	tstate->use_tracing = ((tstate->c_tracefunc != NULL)
			       || (tstate->c_profilefunc != NULL));
	tstate->tracing--;
	if (result)
	    return result;
    }
    if (tstate->c_tracefunc != NULL) {
	tstate->tracing++;
	result = tstate->c_tracefunc(tstate->c_traceobj,
				     f, code , val);
	tstate->use_tracing = ((tstate->c_tracefunc != NULL)
			       || (tstate->c_profilefunc != NULL));
	tstate->tracing--;
    }	
    return result;
}
#endif

static PyObject*
call_with_frame(PyCodeObject *c, PyObject* func, PyObject* args)
{
    PyThreadState *tstate = PyThreadState_GET();
    PyFrameObject *f;
    PyObject *res;

    if (c == NULL)
        return NULL;
    
    f = PyFrame_New(
                    tstate,			/*back*/
                    c,				/*code*/
                    PyEval_GetGlobals(),	/*globals*/
                    NULL			/*locals*/
                    );
    if (f == NULL)
        return NULL;
    tstate->frame = f;
#ifndef NOFIX_TRACE
    if (trace_frame(tstate, f, PyTrace_CALL, Py_None)) {
	Py_DECREF(f);
	return NULL;
    }
#endif
    res = PyEval_CallObject(func, args);
    if (res == NULL && tstate->curexc_traceback == NULL)
        PyTraceBack_Here(f);
#ifndef NOFIX_TRACE
    else {
	if (trace_frame(tstate, f, PyTrace_RETURN, res)) {
	    Py_XDECREF(res);
	    res = NULL;
	}
    }
#endif
    tstate->frame = f->f_back;
    Py_DECREF(f);
    return res;
}

#ifndef Py_USING_UNICODE
#define STRING_CONV_FUNC conv_string_to_utf8
#else
/* Python 2.0 and later versions, when built with Unicode support */
#define STRING_CONV_FUNC (self->returns_unicode \
                          ? conv_string_to_unicode : conv_string_to_utf8)
#endif

static PyObject*
string_intern(xmlparseobject *self, const char* str)
{
    PyObject *result = STRING_CONV_FUNC(str);
    PyObject *value;
    if (!self->intern)
	return result;
    value = PyDict_GetItem(self->intern, result);
    if (!value) {
	if (PyDict_SetItem(self->intern, result, result) == 0)
            return result;
        else
            return NULL;
    }
    Py_INCREF(value);
    Py_DECREF(result);
    return value;
}

/* Return 0 on success, -1 on exception.
 * flag_error() will be called before return if needed.
 */
static int
call_character_handler(xmlparseobject *self, const XML_Char *buffer, int len)
{
    PyObject *args;
    PyObject *temp;

    args = PyTuple_New(1);
    if (args == NULL)
        return -1;
#ifdef Py_USING_UNICODE
    temp = (self->returns_unicode 
            ? conv_string_len_to_unicode(buffer, len) 
            : conv_string_len_to_utf8(buffer, len));
#else
    temp = conv_string_len_to_utf8(buffer, len);
#endif
    if (temp == NULL) {
        Py_DECREF(args);
        flag_error(self);
        return -1;
    }
    PyTuple_SET_ITEM(args, 0, temp);
    /* temp is now a borrowed reference; consider it unused. */
    self->in_callback = 1;
    temp = call_with_frame(getcode(CharacterData, "CharacterData", __LINE__),
                           self->handlers[CharacterData], args);
    /* temp is an owned reference again, or NULL */
    self->in_callback = 0;
    Py_DECREF(args);
    if (temp == NULL) {
        flag_error(self);
        return -1;
    }
    Py_DECREF(temp);
    return 0;
}

static int
flush_character_buffer(xmlparseobject *self)
{
    int rc;
    if (self->buffer == NULL || self->buffer_used == 0)
        return 0;
    rc = call_character_handler(self, self->buffer, self->buffer_used);
    self->buffer_used = 0;
    return rc;
}

static void
my_CharacterDataHandler(void *userData, const XML_Char *data, int len) 
{
    xmlparseobject *self = (xmlparseobject *) userData;
    if (self->buffer == NULL)
        call_character_handler(self, data, len);
    else {
        if ((self->buffer_used + len) > self->buffer_size) {
            if (flush_character_buffer(self) < 0)
                return;
            /* handler might have changed; drop the rest on the floor
             * if there isn't a handler anymore
             */
            if (!have_handler(self, CharacterData))
                return;
        }
        if (len > self->buffer_size) {
            call_character_handler(self, data, len);
            self->buffer_used = 0;
        }
        else {
            memcpy(self->buffer + self->buffer_used,
                   data, len * sizeof(XML_Char));
            self->buffer_used += len;
        }
    }
}

static void
my_StartElementHandler(void *userData,
                       const XML_Char *name, const XML_Char *atts[])
{
    xmlparseobject *self = (xmlparseobject *)userData;

    if (have_handler(self, StartElement)) {
        PyObject *container, *rv, *args;
        int i, max;

        if (flush_character_buffer(self) < 0)
            return;
        /* Set max to the number of slots filled in atts[]; max/2 is
         * the number of attributes we need to process.
         */
        if (self->specified_attributes) {
            max = XML_GetSpecifiedAttributeCount(self->itself);
        }
        else {
            max = 0;
            while (atts[max] != NULL)
                max += 2;
        }
        /* Build the container. */
        if (self->ordered_attributes)
            container = PyList_New(max);
        else
            container = PyDict_New();
        if (container == NULL) {
            flag_error(self);
            return;
        }
        for (i = 0; i < max; i += 2) {
            PyObject *n = string_intern(self, (XML_Char *) atts[i]);
            PyObject *v;
            if (n == NULL) {
                flag_error(self);
                Py_DECREF(container);
                return;
            }
            v = STRING_CONV_FUNC((XML_Char *) atts[i+1]);
            if (v == NULL) {
                flag_error(self);
                Py_DECREF(container);
                Py_DECREF(n);
                return;
            }
            if (self->ordered_attributes) {
                PyList_SET_ITEM(container, i, n);
                PyList_SET_ITEM(container, i+1, v);
            }
            else if (PyDict_SetItem(container, n, v)) {
                flag_error(self);
                Py_DECREF(n);
                Py_DECREF(v);
                return;
            }
            else {
                Py_DECREF(n);
                Py_DECREF(v);
            }
        }
	args = Py_BuildValue("(NN)", string_intern(self, name), container);
        if (args == NULL) {
            Py_DECREF(container);
            return;
        }
        /* Container is now a borrowed reference; ignore it. */
        self->in_callback = 1;
        rv = call_with_frame(getcode(StartElement, "StartElement", __LINE__),
                             self->handlers[StartElement], args);
        self->in_callback = 0;
        Py_DECREF(args);
        if (rv == NULL) {
            flag_error(self);
            return;
        }
        Py_DECREF(rv);
    }
}

#define RC_HANDLER(RC, NAME, PARAMS, INIT, PARAM_FORMAT, CONVERSION, \
                RETURN, GETUSERDATA) \
static RC \
my_##NAME##Handler PARAMS {\
    xmlparseobject *self = GETUSERDATA ; \
    PyObject *args = NULL; \
    PyObject *rv = NULL; \
    INIT \
\
    if (have_handler(self, NAME)) { \
        if (flush_character_buffer(self) < 0) \
            return RETURN; \
        args = Py_BuildValue PARAM_FORMAT ;\
        if (!args) { flag_error(self); return RETURN;} \
        self->in_callback = 1; \
        rv = call_with_frame(getcode(NAME,#NAME,__LINE__), \
                             self->handlers[NAME], args); \
        self->in_callback = 0; \
        Py_DECREF(args); \
        if (rv == NULL) { \
            flag_error(self); \
            return RETURN; \
        } \
        CONVERSION \
        Py_DECREF(rv); \
    } \
    return RETURN; \
}

#define VOID_HANDLER(NAME, PARAMS, PARAM_FORMAT) \
	RC_HANDLER(void, NAME, PARAMS, ;, PARAM_FORMAT, ;, ;,\
	(xmlparseobject *)userData)

#define INT_HANDLER(NAME, PARAMS, PARAM_FORMAT)\
	RC_HANDLER(int, NAME, PARAMS, int rc=0;, PARAM_FORMAT, \
			rc = PyInt_AsLong(rv);, rc, \
	(xmlparseobject *)userData)

VOID_HANDLER(EndElement,
             (void *userData, const XML_Char *name),
             ("(N)", string_intern(self, name)))

VOID_HANDLER(ProcessingInstruction,
             (void *userData,
              const XML_Char *target,
              const XML_Char *data),
             ("(NO&)", string_intern(self, target), STRING_CONV_FUNC,data))

VOID_HANDLER(UnparsedEntityDecl,
             (void *userData,
              const XML_Char *entityName,
              const XML_Char *base,
              const XML_Char *systemId,
              const XML_Char *publicId,
              const XML_Char *notationName),
             ("(NNNNN)",
              string_intern(self, entityName), string_intern(self, base),
              string_intern(self, systemId), string_intern(self, publicId),
              string_intern(self, notationName)))

#ifndef Py_USING_UNICODE
VOID_HANDLER(EntityDecl,
             (void *userData,
              const XML_Char *entityName,
              int is_parameter_entity,
              const XML_Char *value,
              int value_length,
              const XML_Char *base,
              const XML_Char *systemId,
              const XML_Char *publicId,
              const XML_Char *notationName),
             ("NiNNNNN",
              string_intern(self, entityName), is_parameter_entity,
              conv_string_len_to_utf8(value, value_length),
              string_intern(self, base), string_intern(self, systemId),
              string_intern(self, publicId),
              string_intern(self, notationName)))
#else
VOID_HANDLER(EntityDecl,
             (void *userData,
              const XML_Char *entityName,
              int is_parameter_entity,
              const XML_Char *value,
              int value_length,
              const XML_Char *base,
              const XML_Char *systemId,
              const XML_Char *publicId,
              const XML_Char *notationName),
             ("NiNNNNN",
              string_intern(self, entityName), is_parameter_entity,
              (self->returns_unicode
               ? conv_string_len_to_unicode(value, value_length)
               : conv_string_len_to_utf8(value, value_length)),
              string_intern(self, base), string_intern(self, systemId),
              string_intern(self, publicId),
              string_intern(self, notationName)))
#endif

VOID_HANDLER(XmlDecl,
             (void *userData,
              const XML_Char *version,
              const XML_Char *encoding,
              int standalone),
             ("(O&O&i)",
              STRING_CONV_FUNC,version, STRING_CONV_FUNC,encoding,
              standalone))

static PyObject *
conv_content_model(XML_Content * const model,
                   PyObject *(*conv_string)(const XML_Char *))
{
    PyObject *result = NULL;
    PyObject *children = PyTuple_New(model->numchildren);
    int i;

    if (children != NULL) {
        assert(model->numchildren < INT_MAX);
        for (i = 0; i < (int)model->numchildren; ++i) {
            PyObject *child = conv_content_model(&model->children[i],
                                                 conv_string);
            if (child == NULL) {
                Py_XDECREF(children);
                return NULL;
            }
            PyTuple_SET_ITEM(children, i, child);
        }
        result = Py_BuildValue("(iiO&N)",
                               model->type, model->quant,
                               conv_string,model->name, children);
    }
    return result;
}

static void
my_ElementDeclHandler(void *userData,
                      const XML_Char *name,
                      XML_Content *model)
{
    xmlparseobject *self = (xmlparseobject *)userData;
    PyObject *args = NULL;

    if (have_handler(self, ElementDecl)) {
        PyObject *rv = NULL;
        PyObject *modelobj, *nameobj;

        if (flush_character_buffer(self) < 0)
            goto finally;
#ifdef Py_USING_UNICODE
        modelobj = conv_content_model(model,
                                      (self->returns_unicode
                                       ? conv_string_to_unicode
                                       : conv_string_to_utf8));
#else
        modelobj = conv_content_model(model, conv_string_to_utf8);
#endif
        if (modelobj == NULL) {
            flag_error(self);
            goto finally;
        }
        nameobj = string_intern(self, name);
        if (nameobj == NULL) {
            Py_DECREF(modelobj);
            flag_error(self);
            goto finally;
        }
        args = Py_BuildValue("NN", string_intern(self, name), modelobj);
        if (args == NULL) {
            Py_DECREF(modelobj);
            flag_error(self);
            goto finally;
        }
        self->in_callback = 1;
        rv = call_with_frame(getcode(ElementDecl, "ElementDecl", __LINE__),
                             self->handlers[ElementDecl], args);
        self->in_callback = 0;
        if (rv == NULL) {
            flag_error(self);
            goto finally;
        }
        Py_DECREF(rv);
    }
 finally:
    Py_XDECREF(args);
    XML_FreeContentModel(self->itself, model);
    return;
}

VOID_HANDLER(AttlistDecl,
             (void *userData,
              const XML_Char *elname,
              const XML_Char *attname,
              const XML_Char *att_type,
              const XML_Char *dflt,
              int isrequired),
             ("(NNO&O&i)",
              string_intern(self, elname), string_intern(self, attname),
              STRING_CONV_FUNC,att_type, STRING_CONV_FUNC,dflt,
              isrequired))

#if XML_COMBINED_VERSION >= 19504
VOID_HANDLER(SkippedEntity,
             (void *userData,
              const XML_Char *entityName,
              int is_parameter_entity),
             ("Ni",
              string_intern(self, entityName), is_parameter_entity))
#endif

VOID_HANDLER(NotationDecl,
		(void *userData,
			const XML_Char *notationName,
			const XML_Char *base,
			const XML_Char *systemId,
			const XML_Char *publicId),
                ("(NNNN)",
		 string_intern(self, notationName), string_intern(self, base),
		 string_intern(self, systemId), string_intern(self, publicId)))

VOID_HANDLER(StartNamespaceDecl,
		(void *userData,
		      const XML_Char *prefix,
		      const XML_Char *uri),
                ("(NN)",
                 string_intern(self, prefix), string_intern(self, uri)))

VOID_HANDLER(EndNamespaceDecl,
		(void *userData,
		    const XML_Char *prefix),
                ("(N)", string_intern(self, prefix)))

VOID_HANDLER(Comment,
               (void *userData, const XML_Char *data),
                ("(O&)", STRING_CONV_FUNC,data))

VOID_HANDLER(StartCdataSection,
               (void *userData),
		("()"))

VOID_HANDLER(EndCdataSection,
               (void *userData),
		("()"))

#ifndef Py_USING_UNICODE
VOID_HANDLER(Default,
	      (void *userData, const XML_Char *s, int len),
	      ("(N)", conv_string_len_to_utf8(s,len)))

VOID_HANDLER(DefaultHandlerExpand,
	      (void *userData, const XML_Char *s, int len),
	      ("(N)", conv_string_len_to_utf8(s,len)))
#else
VOID_HANDLER(Default,
	      (void *userData, const XML_Char *s, int len),
	      ("(N)", (self->returns_unicode
		       ? conv_string_len_to_unicode(s,len)
		       : conv_string_len_to_utf8(s,len))))

VOID_HANDLER(DefaultHandlerExpand,
	      (void *userData, const XML_Char *s, int len),
	      ("(N)", (self->returns_unicode
		       ? conv_string_len_to_unicode(s,len)
		       : conv_string_len_to_utf8(s,len))))
#endif

INT_HANDLER(NotStandalone,
		(void *userData),
		("()"))

RC_HANDLER(int, ExternalEntityRef,
		(XML_Parser parser,
		    const XML_Char *context,
		    const XML_Char *base,
		    const XML_Char *systemId,
		    const XML_Char *publicId),
		int rc=0;,
                ("(O&NNN)",
		 STRING_CONV_FUNC,context, string_intern(self, base),
		 string_intern(self, systemId), string_intern(self, publicId)),
		rc = PyInt_AsLong(rv);, rc,
		XML_GetUserData(parser))

/* XXX UnknownEncodingHandler */

VOID_HANDLER(StartDoctypeDecl,
             (void *userData, const XML_Char *doctypeName,
              const XML_Char *sysid, const XML_Char *pubid,
              int has_internal_subset),
             ("(NNNi)", string_intern(self, doctypeName),
              string_intern(self, sysid), string_intern(self, pubid),
              has_internal_subset))

VOID_HANDLER(EndDoctypeDecl, (void *userData), ("()"))

/* ---------------------------------------------------------------- */

static PyObject *
get_parse_result(xmlparseobject *self, int rv)
{
    if (PyErr_Occurred()) {
        return NULL;
    }
    if (rv == 0) {
        return set_error(self, XML_GetErrorCode(self->itself));
    }
    if (flush_character_buffer(self) < 0) {
        return NULL;
    }
    return PyInt_FromLong(rv);
}

PyDoc_STRVAR(xmlparse_Parse__doc__,
"Parse(data[, isfinal])\n\
Parse XML data.  `isfinal' should be true at end of input.");

static PyObject *
xmlparse_Parse(xmlparseobject *self, PyObject *args)
{
    char *s;
    int slen;
    int isFinal = 0;

    if (!PyArg_ParseTuple(args, "s#|i:Parse", &s, &slen, &isFinal))
        return NULL;

    return get_parse_result(self, XML_Parse(self->itself, s, slen, isFinal));
}

/* File reading copied from cPickle */

#define BUF_SIZE 2048

static int
readinst(char *buf, int buf_size, PyObject *meth)
{
    PyObject *arg = NULL;
    PyObject *bytes = NULL;
    PyObject *str = NULL;
    int len = -1;

    if ((bytes = PyInt_FromLong(buf_size)) == NULL)
        goto finally;

    if ((arg = PyTuple_New(1)) == NULL)
        goto finally;

    PyTuple_SET_ITEM(arg, 0, bytes);

    if ((str = PyObject_Call(meth, arg, NULL)) == NULL)
        goto finally;

    /* XXX what to do if it returns a Unicode string? */
    if (!PyString_Check(str)) {
        PyErr_Format(PyExc_TypeError,
                     "read() did not return a string object (type=%.400s)",
                     str->ob_type->tp_name);
        goto finally;
    }
    len = PyString_GET_SIZE(str);
    if (len > buf_size) {
        PyErr_Format(PyExc_ValueError,
                     "read() returned too much data: "
                     "%i bytes requested, %i returned",
                     buf_size, len);
        Py_DECREF(str);
        goto finally;
    }
    memcpy(buf, PyString_AsString(str), len);
finally:
    Py_XDECREF(arg);
    Py_XDECREF(str);
    return len;
}

PyDoc_STRVAR(xmlparse_ParseFile__doc__,
"ParseFile(file)\n\
Parse XML data from file-like object.");

static PyObject *
xmlparse_ParseFile(xmlparseobject *self, PyObject *args)
{
    int rv = 1;
    PyObject *f;
    FILE *fp;
    PyObject *readmethod = NULL;

    if (!PyArg_ParseTuple(args, "O:ParseFile", &f))
        return NULL;

    if (PyFile_Check(f)) {
        fp = PyFile_AsFile(f);
    }
    else{
        fp = NULL;
        readmethod = PyObject_GetAttrString(f, "read");
        if (readmethod == NULL) {
            PyErr_Clear();
            PyErr_SetString(PyExc_TypeError,
                            "argument must have 'read' attribute");
            return NULL;
        }
    }
    for (;;) {
        int bytes_read;
        void *buf = XML_GetBuffer(self->itself, BUF_SIZE);
        if (buf == NULL)
            return PyErr_NoMemory();

        if (fp) {
            bytes_read = fread(buf, sizeof(char), BUF_SIZE, fp);
            if (bytes_read < 0) {
                PyErr_SetFromErrno(PyExc_IOError);
                return NULL;
            }
        }
        else {
            bytes_read = readinst(buf, BUF_SIZE, readmethod);
            if (bytes_read < 0)
                return NULL;
        }
        rv = XML_ParseBuffer(self->itself, bytes_read, bytes_read == 0);
        if (PyErr_Occurred())
            return NULL;

        if (!rv || bytes_read == 0)
            break;
    }
    return get_parse_result(self, rv);
}

PyDoc_STRVAR(xmlparse_SetBase__doc__,
"SetBase(base_url)\n\
Set the base URL for the parser.");

static PyObject *
xmlparse_SetBase(xmlparseobject *self, PyObject *args)
{
    char *base;

    if (!PyArg_ParseTuple(args, "s:SetBase", &base))
        return NULL;
    if (!XML_SetBase(self->itself, base)) {
	return PyErr_NoMemory();
    }
    Py_INCREF(Py_None);
    return Py_None;
}

PyDoc_STRVAR(xmlparse_GetBase__doc__,
"GetBase() -> url\n\
Return base URL string for the parser.");

static PyObject *
xmlparse_GetBase(xmlparseobject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ":GetBase"))
        return NULL;

    return Py_BuildValue("z", XML_GetBase(self->itself));
}

PyDoc_STRVAR(xmlparse_GetInputContext__doc__,
"GetInputContext() -> string\n\
Return the untranslated text of the input that caused the current event.\n\
If the event was generated by a large amount of text (such as a start tag\n\
for an element with many attributes), not all of the text may be available.");

static PyObject *
xmlparse_GetInputContext(xmlparseobject *self, PyObject *args)
{
    PyObject *result = NULL;

    if (PyArg_ParseTuple(args, ":GetInputContext")) {
        if (self->in_callback) {
            int offset, size;
            const char *buffer
                = XML_GetInputContext(self->itself, &offset, &size);

            if (buffer != NULL)
                result = PyString_FromStringAndSize(buffer + offset, size);
            else {
                result = Py_None;
                Py_INCREF(result);
            }
        }
        else {
            result = Py_None;
            Py_INCREF(result);
        }
    }
    return result;
}

PyDoc_STRVAR(xmlparse_ExternalEntityParserCreate__doc__,
"ExternalEntityParserCreate(context[, encoding])\n\
Create a parser for parsing an external entity based on the\n\
information passed to the ExternalEntityRefHandler.");

static PyObject *
xmlparse_ExternalEntityParserCreate(xmlparseobject *self, PyObject *args)
{
    char *context;
    char *encoding = NULL;
    xmlparseobject *new_parser;
    int i;

    if (!PyArg_ParseTuple(args, "z|s:ExternalEntityParserCreate",
                          &context, &encoding)) {
        return NULL;
    }

#ifndef Py_TPFLAGS_HAVE_GC
    /* Python versions 2.0 and 2.1 */
    new_parser = PyObject_New(xmlparseobject, &Xmlparsetype);
#else
    /* Python versions 2.2 and later */
    new_parser = PyObject_GC_New(xmlparseobject, &Xmlparsetype);
#endif

    if (new_parser == NULL)
        return NULL;
    new_parser->buffer_size = self->buffer_size;
    new_parser->buffer_used = 0;
    if (self->buffer != NULL) {
        new_parser->buffer = malloc(new_parser->buffer_size);
        if (new_parser->buffer == NULL) {
#ifndef Py_TPFLAGS_HAVE_GC
            /* Code for versions 2.0 and 2.1 */
            PyObject_Del(new_parser);
#else
            /* Code for versions 2.2 and later. */
            PyObject_GC_Del(new_parser);
#endif
            return PyErr_NoMemory();
        }
    }
    else
        new_parser->buffer = NULL;
    new_parser->returns_unicode = self->returns_unicode;
    new_parser->ordered_attributes = self->ordered_attributes;
    new_parser->specified_attributes = self->specified_attributes;
    new_parser->in_callback = 0;
    new_parser->ns_prefixes = self->ns_prefixes;
    new_parser->itself = XML_ExternalEntityParserCreate(self->itself, context,
							encoding);
    new_parser->handlers = 0;
    new_parser->intern = self->intern;
    Py_XINCREF(new_parser->intern);
#ifdef Py_TPFLAGS_HAVE_GC
    PyObject_GC_Track(new_parser);
#else
    PyObject_GC_Init(new_parser);
#endif

    if (!new_parser->itself) {
        Py_DECREF(new_parser);
        return PyErr_NoMemory();
    }

    XML_SetUserData(new_parser->itself, (void *)new_parser);

    /* allocate and clear handlers first */
    for (i = 0; handler_info[i].name != NULL; i++)
        /* do nothing */;

    new_parser->handlers = malloc(sizeof(PyObject *) * i);
    if (!new_parser->handlers) {
        Py_DECREF(new_parser);
        return PyErr_NoMemory();
    }
    clear_handlers(new_parser, 1);

    /* then copy handlers from self */
    for (i = 0; handler_info[i].name != NULL; i++) {
        PyObject *handler = self->handlers[i];
        if (handler != NULL) {
            Py_INCREF(handler);
            new_parser->handlers[i] = handler;
            handler_info[i].setter(new_parser->itself,
                                   handler_info[i].handler);
        }
    }
    return (PyObject *)new_parser;
}

PyDoc_STRVAR(xmlparse_SetParamEntityParsing__doc__,
"SetParamEntityParsing(flag) -> success\n\
Controls parsing of parameter entities (including the external DTD\n\
subset). Possible flag values are XML_PARAM_ENTITY_PARSING_NEVER,\n\
XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE and\n\
XML_PARAM_ENTITY_PARSING_ALWAYS. Returns true if setting the flag\n\
was successful.");

static PyObject*
xmlparse_SetParamEntityParsing(xmlparseobject *p, PyObject* args)
{
    int flag;
    if (!PyArg_ParseTuple(args, "i", &flag))
        return NULL;
    flag = XML_SetParamEntityParsing(p->itself, flag);
    return PyInt_FromLong(flag);
}


#if XML_COMBINED_VERSION >= 19505
PyDoc_STRVAR(xmlparse_UseForeignDTD__doc__,
"UseForeignDTD([flag])\n\
Allows the application to provide an artificial external subset if one is\n\
not specified as part of the document instance.  This readily allows the\n\
use of a 'default' document type controlled by the application, while still\n\
getting the advantage of providing document type information to the parser.\n\
'flag' defaults to True if not provided.");

static PyObject *
xmlparse_UseForeignDTD(xmlparseobject *self, PyObject *args)
{
    PyObject *flagobj = NULL;
    XML_Bool flag = XML_TRUE;
    enum XML_Error rc;
    if (!PyArg_ParseTuple(args, "|O:UseForeignDTD", &flagobj))
        return NULL;
    if (flagobj != NULL)
        flag = PyObject_IsTrue(flagobj) ? XML_TRUE : XML_FALSE;
    rc = XML_UseForeignDTD(self->itself, flag);
    if (rc != XML_ERROR_NONE) {
        return set_error(self, rc);
    }
    Py_INCREF(Py_None);
    return Py_None;
}
#endif

static struct PyMethodDef xmlparse_methods[] = {
    {"Parse",	  (PyCFunction)xmlparse_Parse,
		  METH_VARARGS,	xmlparse_Parse__doc__},
    {"ParseFile", (PyCFunction)xmlparse_ParseFile,
		  METH_VARARGS,	xmlparse_ParseFile__doc__},
    {"SetBase",   (PyCFunction)xmlparse_SetBase,
		  METH_VARARGS, xmlparse_SetBase__doc__},
    {"GetBase",   (PyCFunction)xmlparse_GetBase,
		  METH_VARARGS, xmlparse_GetBase__doc__},
    {"ExternalEntityParserCreate", (PyCFunction)xmlparse_ExternalEntityParserCreate,
	 	  METH_VARARGS, xmlparse_ExternalEntityParserCreate__doc__},
    {"SetParamEntityParsing", (PyCFunction)xmlparse_SetParamEntityParsing,
		  METH_VARARGS, xmlparse_SetParamEntityParsing__doc__},
    {"GetInputContext", (PyCFunction)xmlparse_GetInputContext,
		  METH_VARARGS, xmlparse_GetInputContext__doc__},
#if XML_COMBINED_VERSION >= 19505
    {"UseForeignDTD", (PyCFunction)xmlparse_UseForeignDTD,
		  METH_VARARGS, xmlparse_UseForeignDTD__doc__},
#endif
    {NULL,	  NULL}		/* sentinel */
};

/* ---------- */


#ifdef Py_USING_UNICODE

/* pyexpat international encoding support.
   Make it as simple as possible.
*/

static char template_buffer[257];
PyObject *template_string = NULL;

static void
init_template_buffer(void)
{
    int i;
    for (i = 0; i < 256; i++) {
	template_buffer[i] = i;
    }
    template_buffer[256] = 0;
}

static int
PyUnknownEncodingHandler(void *encodingHandlerData,
                         const XML_Char *name,
                         XML_Encoding *info)
{
    PyUnicodeObject *_u_string = NULL;
    int result = 0;
    int i;

    /* Yes, supports only 8bit encodings */
    _u_string = (PyUnicodeObject *)
        PyUnicode_Decode(template_buffer, 256, name, "replace");

    if (_u_string == NULL)
	return result;

    for (i = 0; i < 256; i++) {
	/* Stupid to access directly, but fast */
	Py_UNICODE c = _u_string->str[i];
	if (c == Py_UNICODE_REPLACEMENT_CHARACTER)
	    info->map[i] = -1;
	else
	    info->map[i] = c;
    }
    info->data = NULL;
    info->convert = NULL;
    info->release = NULL;
    result = 1;
    Py_DECREF(_u_string);
    return result;
}

#endif

static PyObject *
newxmlparseobject(char *encoding, char *namespace_separator, PyObject *intern)
{
    int i;
    xmlparseobject *self;

#ifdef Py_TPFLAGS_HAVE_GC
    /* Code for versions 2.2 and later */
    self = PyObject_GC_New(xmlparseobject, &Xmlparsetype);
#else
    self = PyObject_New(xmlparseobject, &Xmlparsetype);
#endif
    if (self == NULL)
        return NULL;

#ifdef Py_USING_UNICODE
    self->returns_unicode = 1;
#else
    self->returns_unicode = 0;
#endif

    self->buffer = NULL;
    self->buffer_size = CHARACTER_DATA_BUFFER_SIZE;
    self->buffer_used = 0;
    self->ordered_attributes = 0;
    self->specified_attributes = 0;
    self->in_callback = 0;
    self->ns_prefixes = 0;
    self->handlers = NULL;
    if (namespace_separator != NULL) {
        self->itself = XML_ParserCreateNS(encoding, *namespace_separator);
    }
    else {
        self->itself = XML_ParserCreate(encoding);
    }
    self->intern = intern;
    Py_XINCREF(self->intern);
#ifdef Py_TPFLAGS_HAVE_GC
    PyObject_GC_Track(self);
#else
    PyObject_GC_Init(self);
#endif
    if (self->itself == NULL) {
        PyErr_SetString(PyExc_RuntimeError,
                        "XML_ParserCreate failed");
        Py_DECREF(self);
        return NULL;
    }
    XML_SetUserData(self->itself, (void *)self);
#ifdef Py_USING_UNICODE
    XML_SetUnknownEncodingHandler(self->itself,
                  (XML_UnknownEncodingHandler) PyUnknownEncodingHandler, NULL);
#endif

    for (i = 0; handler_info[i].name != NULL; i++)
        /* do nothing */;

    self->handlers = malloc(sizeof(PyObject *) * i);
    if (!self->handlers) {
        Py_DECREF(self);
        return PyErr_NoMemory();
    }
    clear_handlers(self, 1);

    return (PyObject*)self;
}


static void
xmlparse_dealloc(xmlparseobject *self)
{
    int i;
#ifdef Py_TPFLAGS_HAVE_GC
    PyObject_GC_UnTrack(self);
#else
    PyObject_GC_Fini(self);
#endif
    if (self->itself != NULL)
        XML_ParserFree(self->itself);
    self->itself = NULL;

    if (self->handlers != NULL) {
        PyObject *temp;
        for (i = 0; handler_info[i].name != NULL; i++) {
            temp = self->handlers[i];
            self->handlers[i] = NULL;
            Py_XDECREF(temp);
        }
        free(self->handlers);
        self->handlers = NULL;
    }
    if (self->buffer != NULL) {
        free(self->buffer);
        self->buffer = NULL;
    }
    Py_XDECREF(self->intern);
#ifndef Py_TPFLAGS_HAVE_GC
    /* Code for versions 2.0 and 2.1 */
    PyObject_Del(self);
#else
    /* Code for versions 2.2 and later. */
    PyObject_GC_Del(self);
#endif
}

static int
handlername2int(const char *name)
{
    int i;
    for (i = 0; handler_info[i].name != NULL; i++) {
        if (strcmp(name, handler_info[i].name) == 0) {
            return i;
        }
    }
    return -1;
}

static PyObject *
get_pybool(int istrue)
{
    PyObject *result = istrue ? Py_True : Py_False;
    Py_INCREF(result);
    return result;
}

static PyObject *
xmlparse_getattr(xmlparseobject *self, char *name)
{
    int handlernum = handlername2int(name);

    if (handlernum != -1) {
        PyObject *result = self->handlers[handlernum];
        if (result == NULL)
            result = Py_None;
        Py_INCREF(result);
        return result;
    }
    if (name[0] == 'E') {
        if (strcmp(name, "ErrorCode") == 0)
            return PyInt_FromLong((long)
                                  XML_GetErrorCode(self->itself));
        if (strcmp(name, "ErrorLineNumber") == 0)
            return PyInt_FromLong((long)
                                  XML_GetErrorLineNumber(self->itself));
        if (strcmp(name, "ErrorColumnNumber") == 0)
            return PyInt_FromLong((long)
                                  XML_GetErrorColumnNumber(self->itself));
        if (strcmp(name, "ErrorByteIndex") == 0)
            return PyInt_FromLong((long)
                                  XML_GetErrorByteIndex(self->itself));
    }
    if (name[0] == 'b') {
        if (strcmp(name, "buffer_size") == 0)
            return PyInt_FromLong((long) self->buffer_size);
        if (strcmp(name, "buffer_text") == 0)
            return get_pybool(self->buffer != NULL);
        if (strcmp(name, "buffer_used") == 0)
            return PyInt_FromLong((long) self->buffer_used);
    }
    if (strcmp(name, "namespace_prefixes") == 0)
        return get_pybool(self->ns_prefixes);
    if (strcmp(name, "ordered_attributes") == 0)
        return get_pybool(self->ordered_attributes);
    if (strcmp(name, "returns_unicode") == 0)
        return get_pybool((long) self->returns_unicode);
    if (strcmp(name, "specified_attributes") == 0)
        return get_pybool((long) self->specified_attributes);
    if (strcmp(name, "intern") == 0) {
        if (self->intern == NULL) {
            Py_INCREF(Py_None);
            return Py_None;
        }
        else {
            Py_INCREF(self->intern);
            return self->intern;
        }
    }

#define APPEND(list, str)				\
        do {						\
                PyObject *o = PyString_FromString(str);	\
                if (o != NULL)				\
        	        PyList_Append(list, o);		\
                Py_XDECREF(o);				\
        } while (0)

    if (strcmp(name, "__members__") == 0) {
        int i;
        PyObject *rc = PyList_New(0);
        for (i = 0; handler_info[i].name != NULL; i++) {
            PyObject *o = get_handler_name(&handler_info[i]);
            if (o != NULL)
                PyList_Append(rc, o);
            Py_XDECREF(o);
        }
        APPEND(rc, "ErrorCode");
        APPEND(rc, "ErrorLineNumber");
        APPEND(rc, "ErrorColumnNumber");
        APPEND(rc, "ErrorByteIndex");
        APPEND(rc, "buffer_size");
        APPEND(rc, "buffer_text");
        APPEND(rc, "buffer_used");
        APPEND(rc, "namespace_prefixes");
        APPEND(rc, "ordered_attributes");
        APPEND(rc, "returns_unicode");
        APPEND(rc, "specified_attributes");
        APPEND(rc, "intern");

#undef APPEND
        return rc;
    }
    return Py_FindMethod(xmlparse_methods, (PyObject *)self, name);
}

static int
sethandler(xmlparseobject *self, const char *name, PyObject* v)
{
    int handlernum = handlername2int(name);
    if (handlernum >= 0) {
        xmlhandler c_handler = NULL;
        PyObject *temp = self->handlers[handlernum];

        if (v == Py_None)
            v = NULL;
        else if (v != NULL) {
            Py_INCREF(v);
            c_handler = handler_info[handlernum].handler;
        }
        self->handlers[handlernum] = v;
        Py_XDECREF(temp);
        handler_info[handlernum].setter(self->itself, c_handler);
        return 1;
    }
    return 0;
}

static int
xmlparse_setattr(xmlparseobject *self, char *name, PyObject *v)
{
    /* Set attribute 'name' to value 'v'. v==NULL means delete */
    if (v == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Cannot delete attribute");
        return -1;
    }
    if (strcmp(name, "buffer_text") == 0) {
        if (PyObject_IsTrue(v)) {
            if (self->buffer == NULL) {
                self->buffer = malloc(self->buffer_size);
                if (self->buffer == NULL) {
                    PyErr_NoMemory();
                    return -1;
                }
                self->buffer_used = 0;
            }
        }
        else if (self->buffer != NULL) {
            if (flush_character_buffer(self) < 0)
                return -1;
            free(self->buffer);
            self->buffer = NULL;
        }
        return 0;
    }
    if (strcmp(name, "namespace_prefixes") == 0) {
        if (PyObject_IsTrue(v))
            self->ns_prefixes = 1;
        else
            self->ns_prefixes = 0;
        XML_SetReturnNSTriplet(self->itself, self->ns_prefixes);
        return 0;
    }
    if (strcmp(name, "ordered_attributes") == 0) {
        if (PyObject_IsTrue(v))
            self->ordered_attributes = 1;
        else
            self->ordered_attributes = 0;
        return 0;
    }
    if (strcmp(name, "returns_unicode") == 0) {
        if (PyObject_IsTrue(v)) {
#ifndef Py_USING_UNICODE
            PyErr_SetString(PyExc_ValueError,
                            "Unicode support not available");
            return -1;
#else
            self->returns_unicode = 1;
#endif
        }
        else
            self->returns_unicode = 0;
        return 0;
    }
    if (strcmp(name, "specified_attributes") == 0) {
        if (PyObject_IsTrue(v))
            self->specified_attributes = 1;
        else
            self->specified_attributes = 0;
        return 0;
    }
    if (strcmp(name, "CharacterDataHandler") == 0) {
        /* If we're changing the character data handler, flush all
         * cached data with the old handler.  Not sure there's a
         * "right" thing to do, though, but this probably won't
         * happen.
         */
        if (flush_character_buffer(self) < 0)
            return -1;
    }
    if (sethandler(self, name, v)) {
        return 0;
    }
    PyErr_SetString(PyExc_AttributeError, name);
    return -1;
}

#ifdef WITH_CYCLE_GC
static int
xmlparse_traverse(xmlparseobject *op, visitproc visit, void *arg)
{
    int i, err;
    for (i = 0; handler_info[i].name != NULL; i++) {
        if (!op->handlers[i])
            continue;
        err = visit(op->handlers[i], arg);
        if (err)
            return err;
    }
    return 0;
}

static int
xmlparse_clear(xmlparseobject *op)
{
    clear_handlers(op, 0);
    Py_XDECREF(op->intern);
    op->intern = 0;
    return 0;
}
#endif

PyDoc_STRVAR(Xmlparsetype__doc__, "XML parser");

static PyTypeObject Xmlparsetype = {
	PyObject_HEAD_INIT(NULL)
	0,				/*ob_size*/
	"pyexpat.xmlparser",		/*tp_name*/
	sizeof(xmlparseobject) + PyGC_HEAD_SIZE,/*tp_basicsize*/
	0,				/*tp_itemsize*/
	/* methods */
	(destructor)xmlparse_dealloc,	/*tp_dealloc*/
	(printfunc)0,		/*tp_print*/
	(getattrfunc)xmlparse_getattr,	/*tp_getattr*/
	(setattrfunc)xmlparse_setattr,	/*tp_setattr*/
	(cmpfunc)0,		/*tp_compare*/
	(reprfunc)0,		/*tp_repr*/
	0,			/*tp_as_number*/
	0,		/*tp_as_sequence*/
	0,		/*tp_as_mapping*/
	(hashfunc)0,		/*tp_hash*/
	(ternaryfunc)0,		/*tp_call*/
	(reprfunc)0,		/*tp_str*/
	0,		/* tp_getattro */
	0,		/* tp_setattro */
	0,		/* tp_as_buffer */
#ifdef Py_TPFLAGS_HAVE_GC
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC, /*tp_flags*/
#else
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_GC, /*tp_flags*/
#endif
	Xmlparsetype__doc__, /* tp_doc - Documentation string */
#ifdef WITH_CYCLE_GC
	(traverseproc)xmlparse_traverse,	/* tp_traverse */
	(inquiry)xmlparse_clear		/* tp_clear */
#else
	0, 0
#endif
};

/* End of code for xmlparser objects */
/* -------------------------------------------------------- */

PyDoc_STRVAR(pyexpat_ParserCreate__doc__,
"ParserCreate([encoding[, namespace_separator]]) -> parser\n\
Return a new XML parser object.");

static PyObject *
pyexpat_ParserCreate(PyObject *notused, PyObject *args, PyObject *kw)
{
    char *encoding = NULL;
    char *namespace_separator = NULL;
    PyObject *intern = NULL;
    PyObject *result;
    int intern_decref = 0;
    static char *kwlist[] = {"encoding", "namespace_separator",
			     "intern", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kw, "|zzO:ParserCreate", kwlist,
                                     &encoding, &namespace_separator, &intern))
        return NULL;
    if (namespace_separator != NULL
        && strlen(namespace_separator) > 1) {
        PyErr_SetString(PyExc_ValueError,
                        "namespace_separator must be at most one"
                        " character, omitted, or None");
        return NULL;
    }
    /* Explicitly passing None means no interning is desired.
       Not passing anything means that a new dictionary is used. */
    if (intern == Py_None)
	intern = NULL;
    else if (intern == NULL) {
	intern = PyDict_New();
	if (!intern)
	    return NULL;
	intern_decref = 1;
    }
    else if (!PyDict_Check(intern)) {
	PyErr_SetString(PyExc_TypeError, "intern must be a dictionary");
	return NULL;
    }

    result = newxmlparseobject(encoding, namespace_separator, intern);
    if (intern_decref) {
	Py_DECREF(intern);
    }
    return result;
}

PyDoc_STRVAR(pyexpat_ErrorString__doc__,
"ErrorString(errno) -> string\n\
Returns string error for given number.");

static PyObject *
pyexpat_ErrorString(PyObject *self, PyObject *args)
{
    long code = 0;

    if (!PyArg_ParseTuple(args, "l:ErrorString", &code))
        return NULL;
    return Py_BuildValue("z", XML_ErrorString((int)code));
}

/* List of methods defined in the module */

static struct PyMethodDef pyexpat_methods[] = {
    {"ParserCreate",	(PyCFunction)pyexpat_ParserCreate,
     METH_VARARGS|METH_KEYWORDS, pyexpat_ParserCreate__doc__},
    {"ErrorString",	(PyCFunction)pyexpat_ErrorString,
     METH_VARARGS,	pyexpat_ErrorString__doc__},

    {NULL,	 (PyCFunction)NULL, 0, NULL}		/* sentinel */
};

/* Module docstring */

PyDoc_STRVAR(pyexpat_module_documentation,
"Python wrapper for Expat parser.");

/* Return a Python string that represents the version number without the
 * extra cruft added by revision control, even if the right options were
 * given to the "cvs export" command to make it not include the extra
 * cruft.
 */
static PyObject *
get_version_string(void)
{
    static char *rcsid = "$Revision$";
    char *rev = rcsid;
    int i = 0;

    while (!isdigit((int)*rev))
        ++rev;
    while (rev[i] != ' ' && rev[i] != '\0')
        ++i;

    return PyString_FromStringAndSize(rev, i);
}

/* Initialization function for the module */

#ifndef MODULE_NAME
#define MODULE_NAME "pyexpat"
#endif

#ifndef MODULE_INITFUNC
#define MODULE_INITFUNC initpyexpat
#endif

#ifndef PyMODINIT_FUNC
#   ifdef MS_WINDOWS
#       define PyMODINIT_FUNC __declspec(dllexport) void
#   else
#       define PyMODINIT_FUNC void
#   endif
#endif

PyMODINIT_FUNC MODULE_INITFUNC(void);  /* avoid compiler warnings */

PyMODINIT_FUNC
MODULE_INITFUNC(void)
{
    PyObject *m, *d;
    PyObject *errmod_name = PyString_FromString(MODULE_NAME ".errors");
    PyObject *errors_module;
    PyObject *modelmod_name;
    PyObject *model_module;
    PyObject *sys_modules;

    if (errmod_name == NULL)
        return;
    modelmod_name = PyString_FromString(MODULE_NAME ".model");
    if (modelmod_name == NULL)
        return;

    Xmlparsetype.ob_type = &PyType_Type;

    /* Create the module and add the functions */
    m = Py_InitModule3(MODULE_NAME, pyexpat_methods,
                       pyexpat_module_documentation);

    /* Add some symbolic constants to the module */
    if (ErrorObject == NULL) {
        ErrorObject = PyErr_NewException("xml.parsers.expat.ExpatError",
                                         NULL, NULL);
        if (ErrorObject == NULL)
            return;
    }
    Py_INCREF(ErrorObject);
    PyModule_AddObject(m, "error", ErrorObject);
    Py_INCREF(ErrorObject);
    PyModule_AddObject(m, "ExpatError", ErrorObject);
    Py_INCREF(&Xmlparsetype);
    PyModule_AddObject(m, "XMLParserType", (PyObject *) &Xmlparsetype);

    PyModule_AddObject(m, "__version__", get_version_string());
    PyModule_AddStringConstant(m, "EXPAT_VERSION",
                               (char *) XML_ExpatVersion());
    {
        XML_Expat_Version info = XML_ExpatVersionInfo();
        PyModule_AddObject(m, "version_info",
                           Py_BuildValue("(iii)", info.major,
                                         info.minor, info.micro));
    }
#ifdef Py_USING_UNICODE
    init_template_buffer();
#endif
    /* XXX When Expat supports some way of figuring out how it was
       compiled, this should check and set native_encoding
       appropriately.
    */
    PyModule_AddStringConstant(m, "native_encoding", "UTF-8");

    sys_modules = PySys_GetObject("modules");
    d = PyModule_GetDict(m);
    errors_module = PyDict_GetItem(d, errmod_name);
    if (errors_module == NULL) {
        errors_module = PyModule_New(MODULE_NAME ".errors");
        if (errors_module != NULL) {
            PyDict_SetItem(sys_modules, errmod_name, errors_module);
            /* gives away the reference to errors_module */
            PyModule_AddObject(m, "errors", errors_module);
        }
    }
    Py_DECREF(errmod_name);
    model_module = PyDict_GetItem(d, modelmod_name);
    if (model_module == NULL) {
        model_module = PyModule_New(MODULE_NAME ".model");
        if (model_module != NULL) {
            PyDict_SetItem(sys_modules, modelmod_name, model_module);
            /* gives away the reference to model_module */
            PyModule_AddObject(m, "model", model_module);
        }
    }
    Py_DECREF(modelmod_name);
    if (errors_module == NULL || model_module == NULL)
        /* Don't core dump later! */
        return;
    
#if XML_COMBINED_VERSION > 19505
    {
        const XML_Feature *features = XML_GetFeatureList();
        PyObject *list = PyList_New(0);
        if (list == NULL)
            /* just ignore it */
            PyErr_Clear();
        else {
            int i = 0;
            for (; features[i].feature != XML_FEATURE_END; ++i) {
                int ok;
                PyObject *item = Py_BuildValue("si", features[i].name,
                                               features[i].value);
                if (item == NULL) {
                    Py_DECREF(list);
                    list = NULL;
                    break;
                }
                ok = PyList_Append(list, item);
                Py_DECREF(item);
                if (ok < 0) {
                    PyErr_Clear();
                    break;
                }
            }
            if (list != NULL)
                PyModule_AddObject(m, "features", list);
        }
    }
#endif

#define MYCONST(name) \
    PyModule_AddStringConstant(errors_module, #name, \
                               (char*)XML_ErrorString(name))

    MYCONST(XML_ERROR_NO_MEMORY);
    MYCONST(XML_ERROR_SYNTAX);
    MYCONST(XML_ERROR_NO_ELEMENTS);
    MYCONST(XML_ERROR_INVALID_TOKEN);
    MYCONST(XML_ERROR_UNCLOSED_TOKEN);
    MYCONST(XML_ERROR_PARTIAL_CHAR);
    MYCONST(XML_ERROR_TAG_MISMATCH);
    MYCONST(XML_ERROR_DUPLICATE_ATTRIBUTE);
    MYCONST(XML_ERROR_JUNK_AFTER_DOC_ELEMENT);
    MYCONST(XML_ERROR_PARAM_ENTITY_REF);
    MYCONST(XML_ERROR_UNDEFINED_ENTITY);
    MYCONST(XML_ERROR_RECURSIVE_ENTITY_REF);
    MYCONST(XML_ERROR_ASYNC_ENTITY);
    MYCONST(XML_ERROR_BAD_CHAR_REF);
    MYCONST(XML_ERROR_BINARY_ENTITY_REF);
    MYCONST(XML_ERROR_ATTRIBUTE_EXTERNAL_ENTITY_REF);
    MYCONST(XML_ERROR_MISPLACED_XML_PI);
    MYCONST(XML_ERROR_UNKNOWN_ENCODING);
    MYCONST(XML_ERROR_INCORRECT_ENCODING);
    MYCONST(XML_ERROR_UNCLOSED_CDATA_SECTION);
    MYCONST(XML_ERROR_EXTERNAL_ENTITY_HANDLING);
    MYCONST(XML_ERROR_NOT_STANDALONE);

    PyModule_AddStringConstant(errors_module, "__doc__",
                               "Constants used to describe error conditions.");

#undef MYCONST

#define MYCONST(c) PyModule_AddIntConstant(m, #c, c)
    MYCONST(XML_PARAM_ENTITY_PARSING_NEVER);
    MYCONST(XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE);
    MYCONST(XML_PARAM_ENTITY_PARSING_ALWAYS);
#undef MYCONST

#define MYCONST(c) PyModule_AddIntConstant(model_module, #c, c)
    PyModule_AddStringConstant(model_module, "__doc__",
                     "Constants used to interpret content model information.");

    MYCONST(XML_CTYPE_EMPTY);
    MYCONST(XML_CTYPE_ANY);
    MYCONST(XML_CTYPE_MIXED);
    MYCONST(XML_CTYPE_NAME);
    MYCONST(XML_CTYPE_CHOICE);
    MYCONST(XML_CTYPE_SEQ);

    MYCONST(XML_CQUANT_NONE);
    MYCONST(XML_CQUANT_OPT);
    MYCONST(XML_CQUANT_REP);
    MYCONST(XML_CQUANT_PLUS);
#undef MYCONST
}

static void
clear_handlers(xmlparseobject *self, int initial)
{
    int i = 0;
    PyObject *temp;

    for (; handler_info[i].name != NULL; i++) {
        if (initial)
	    self->handlers[i] = NULL;
	else {
            temp = self->handlers[i];
            self->handlers[i] = NULL;
            Py_XDECREF(temp);
	    handler_info[i].setter(self->itself, NULL);
        }
    }
}

static struct HandlerInfo handler_info[] = {
    {"StartElementHandler",
     (xmlhandlersetter)XML_SetStartElementHandler,
     (xmlhandler)my_StartElementHandler},
    {"EndElementHandler",
     (xmlhandlersetter)XML_SetEndElementHandler,
     (xmlhandler)my_EndElementHandler},
    {"ProcessingInstructionHandler",
     (xmlhandlersetter)XML_SetProcessingInstructionHandler,
     (xmlhandler)my_ProcessingInstructionHandler},
    {"CharacterDataHandler",
     (xmlhandlersetter)XML_SetCharacterDataHandler,
     (xmlhandler)my_CharacterDataHandler},
    {"UnparsedEntityDeclHandler",
     (xmlhandlersetter)XML_SetUnparsedEntityDeclHandler,
     (xmlhandler)my_UnparsedEntityDeclHandler},
    {"NotationDeclHandler",
     (xmlhandlersetter)XML_SetNotationDeclHandler,
     (xmlhandler)my_NotationDeclHandler},
    {"StartNamespaceDeclHandler",
     (xmlhandlersetter)XML_SetStartNamespaceDeclHandler,
     (xmlhandler)my_StartNamespaceDeclHandler},
    {"EndNamespaceDeclHandler",
     (xmlhandlersetter)XML_SetEndNamespaceDeclHandler,
     (xmlhandler)my_EndNamespaceDeclHandler},
    {"CommentHandler",
     (xmlhandlersetter)XML_SetCommentHandler,
     (xmlhandler)my_CommentHandler},
    {"StartCdataSectionHandler",
     (xmlhandlersetter)XML_SetStartCdataSectionHandler,
     (xmlhandler)my_StartCdataSectionHandler},
    {"EndCdataSectionHandler",
     (xmlhandlersetter)XML_SetEndCdataSectionHandler,
     (xmlhandler)my_EndCdataSectionHandler},
    {"DefaultHandler",
     (xmlhandlersetter)XML_SetDefaultHandler,
     (xmlhandler)my_DefaultHandler},
    {"DefaultHandlerExpand",
     (xmlhandlersetter)XML_SetDefaultHandlerExpand,
     (xmlhandler)my_DefaultHandlerExpandHandler},
    {"NotStandaloneHandler",
     (xmlhandlersetter)XML_SetNotStandaloneHandler,
     (xmlhandler)my_NotStandaloneHandler},
    {"ExternalEntityRefHandler",
     (xmlhandlersetter)XML_SetExternalEntityRefHandler,
     (xmlhandler)my_ExternalEntityRefHandler},
    {"StartDoctypeDeclHandler",
     (xmlhandlersetter)XML_SetStartDoctypeDeclHandler,
     (xmlhandler)my_StartDoctypeDeclHandler},
    {"EndDoctypeDeclHandler",
     (xmlhandlersetter)XML_SetEndDoctypeDeclHandler,
     (xmlhandler)my_EndDoctypeDeclHandler},
    {"EntityDeclHandler",
     (xmlhandlersetter)XML_SetEntityDeclHandler,
     (xmlhandler)my_EntityDeclHandler},
    {"XmlDeclHandler",
     (xmlhandlersetter)XML_SetXmlDeclHandler,
     (xmlhandler)my_XmlDeclHandler},
    {"ElementDeclHandler",
     (xmlhandlersetter)XML_SetElementDeclHandler,
     (xmlhandler)my_ElementDeclHandler},
    {"AttlistDeclHandler",
     (xmlhandlersetter)XML_SetAttlistDeclHandler,
     (xmlhandler)my_AttlistDeclHandler},
#if XML_COMBINED_VERSION >= 19504
    {"SkippedEntityHandler",
     (xmlhandlersetter)XML_SetSkippedEntityHandler,
     (xmlhandler)my_SkippedEntityHandler},
#endif

    {NULL, NULL, NULL} /* sentinel */
};
