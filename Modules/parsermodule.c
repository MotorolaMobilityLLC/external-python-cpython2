/*  parsermodule.c
 *
 *  Copyright 1995-1996 by Fred L. Drake, Jr. and Virginia Polytechnic
 *  Institute and State University, Blacksburg, Virginia, USA.
 *  Portions copyright 1991-1995 by Stichting Mathematisch Centrum,
 *  Amsterdam, The Netherlands.  Copying is permitted under the terms
 *  associated with the main Python distribution, with the additional
 *  restriction that this additional notice be included and maintained
 *  on all distributed copies.
 *
 *  This module serves to replace the original parser module written
 *  by Guido.  The functionality is not matched precisely, but the
 *  original may be implemented on top of this.  This is desirable
 *  since the source of the text to be parsed is now divorced from
 *  this interface.
 *
 *  Unlike the prior interface, the ability to give a parse tree
 *  produced by Python code as a tuple to the compiler is enabled by
 *  this module.  See the documentation for more details.
 *
 *  I've added some annotations that help with the lint code-checking
 *  program, but they're not complete by a long shot.  The real errors
 *  that lint detects are gone, but there are still warnings with
 *  Py_[X]DECREF() and Py_[X]INCREF() macros.  The lint annotations
 *  look like "NOTE(...)".
 */

#include "Python.h"                     /* general Python API             */
#include "graminit.h"                   /* symbols defined in the grammar */
#include "node.h"                       /* internal parser structure      */
#include "token.h"                      /* token definitions              */
                                        /* ISTERMINAL() / ISNONTERMINAL() */
#include "compile.h"                    /* PyNode_Compile()               */

#ifdef lint
#include <note.h>
#else
#define NOTE(x)
#endif

#ifdef macintosh
char *strdup(char *);
#endif

/*  String constants used to initialize module attributes.
 *
 */
static char*
parser_copyright_string
= "Copyright 1995-1996 by Virginia Polytechnic Institute & State\n\
University, Blacksburg, Virginia, USA, and Fred L. Drake, Jr., Reston,\n\
Virginia, USA.  Portions copyright 1991-1995 by Stichting Mathematisch\n\
Centrum, Amsterdam, The Netherlands.";


static char*
parser_doc_string
= "This is an interface to Python's internal parser.";

static char*
parser_version_string = "0.4";


typedef PyObject* (*SeqMaker) (int length);
typedef int (*SeqInserter) (PyObject* sequence,
                            int index,
                            PyObject* element);

/*  The function below is copyrigthed by Stichting Mathematisch Centrum.  The
 *  original copyright statement is included below, and continues to apply
 *  in full to the function immediately following.  All other material is
 *  original, copyrighted by Fred L. Drake, Jr. and Virginia Polytechnic
 *  Institute and State University.  Changes were made to comply with the
 *  new naming conventions.  Added arguments to provide support for creating
 *  lists as well as tuples, and optionally including the line numbers.
 */

/***********************************************************
Copyright (c) 2000, BeOpen.com.
Copyright (c) 1995-2000, Corporation for National Research Initiatives.
Copyright (c) 1990-1995, Stichting Mathematisch Centrum.
All rights reserved.

See the file "Misc/COPYRIGHT" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.
******************************************************************/

static PyObject*
node2tuple(node *n,                     /* node to convert               */
           SeqMaker mkseq,              /* create sequence               */
           SeqInserter addelem,         /* func. to add elem. in seq.    */
           int lineno)                  /* include line numbers?         */
{
    if (n == NULL) {
        Py_INCREF(Py_None);
        return (Py_None);
    }
    if (ISNONTERMINAL(TYPE(n))) {
        int i;
        PyObject *v;
        PyObject *w;

        v = mkseq(1 + NCH(n));
        if (v == NULL)
            return (v);
        w = PyInt_FromLong(TYPE(n));
        if (w == NULL) {
            Py_DECREF(v);
            return ((PyObject*) NULL);
        }
        (void) addelem(v, 0, w);
        for (i = 0; i < NCH(n); i++) {
            w = node2tuple(CHILD(n, i), mkseq, addelem, lineno);
            if (w == NULL) {
                Py_DECREF(v);
                return ((PyObject*) NULL);
            }
            (void) addelem(v, i+1, w);
        }
        return (v);
    }
    else if (ISTERMINAL(TYPE(n))) {
        PyObject *result = mkseq(2 + lineno);
        if (result != NULL) {
            (void) addelem(result, 0, PyInt_FromLong(TYPE(n)));
            (void) addelem(result, 1, PyString_FromString(STR(n)));
            if (lineno == 1)
                (void) addelem(result, 2, PyInt_FromLong(n->n_lineno));
        }
        return (result);
    }
    else {
        PyErr_SetString(PyExc_SystemError,
                        "unrecognized parse tree node type");
        return ((PyObject*) NULL);
    }
}
/*
 *  End of material copyrighted by Stichting Mathematisch Centrum.
 */



/*  There are two types of intermediate objects we're interested in:
 *  'eval' and 'exec' types.  These constants can be used in the ast_type
 *  field of the object type to identify which any given object represents.
 *  These should probably go in an external header to allow other extensions
 *  to use them, but then, we really should be using C++ too.  ;-)
 *
 *  The PyAST_FRAGMENT type is not currently supported.  Maybe not useful?
 *  Haven't decided yet.
 */

#define PyAST_EXPR      1
#define PyAST_SUITE     2
#define PyAST_FRAGMENT  3


/*  These are the internal objects and definitions required to implement the
 *  AST type.  Most of the internal names are more reminiscent of the 'old'
 *  naming style, but the code uses the new naming convention.
 */

static PyObject*
parser_error = 0;


typedef struct _PyAST_Object {
    PyObject_HEAD                       /* standard object header           */
    node* ast_node;                     /* the node* returned by the parser */
    int   ast_type;                     /* EXPR or SUITE ?                  */
} PyAST_Object;


staticforward void
parser_free(PyAST_Object *ast);

staticforward int
parser_compare(PyAST_Object *left, PyAST_Object *right);

staticforward PyObject *
parser_getattr(PyObject *self, char *name);


static
PyTypeObject PyAST_Type = {
    PyObject_HEAD_INIT(NULL)
    0,
    "ast",                              /* tp_name              */
    (int) sizeof(PyAST_Object),         /* tp_basicsize         */
    0,                                  /* tp_itemsize          */
    (destructor)parser_free,            /* tp_dealloc           */
    0,                                  /* tp_print             */
    parser_getattr,                     /* tp_getattr           */
    0,                                  /* tp_setattr           */
    (cmpfunc)parser_compare,            /* tp_compare           */
    0,                                  /* tp_repr              */
    0,                                  /* tp_as_number         */
    0,                                  /* tp_as_sequence       */
    0,                                  /* tp_as_mapping        */
    0,                                  /* tp_hash              */
    0,                                  /* tp_call              */
    0,                                  /* tp_str               */
    0,                                  /* tp_getattro          */
    0,                                  /* tp_setattro          */

    /* Functions to access object as input/output buffer */
    0,                                  /* tp_as_buffer         */

    Py_TPFLAGS_DEFAULT,                 /* tp_flags             */

    /* __doc__ */
    "Intermediate representation of a Python parse tree."
};  /* PyAST_Type */


static int
parser_compare_nodes(node *left, node *right)
{
    int j;

    if (TYPE(left) < TYPE(right))
        return (-1);

    if (TYPE(right) < TYPE(left))
        return (1);

    if (ISTERMINAL(TYPE(left)))
        return (strcmp(STR(left), STR(right)));

    if (NCH(left) < NCH(right))
        return (-1);

    if (NCH(right) < NCH(left))
        return (1);

    for (j = 0; j < NCH(left); ++j) {
        int v = parser_compare_nodes(CHILD(left, j), CHILD(right, j));

        if (v != 0)
            return (v);
    }
    return (0);
}


/*  int parser_compare(PyAST_Object* left, PyAST_Object* right)
 *
 *  Comparison function used by the Python operators ==, !=, <, >, <=, >=
 *  This really just wraps a call to parser_compare_nodes() with some easy
 *  checks and protection code.
 *
 */
static int
parser_compare(PyAST_Object *left, PyAST_Object *right)
{
    if (left == right)
        return (0);

    if ((left == 0) || (right == 0))
        return (-1);

    return (parser_compare_nodes(left->ast_node, right->ast_node));
}


/*  parser_newastobject(node* ast)
 *
 *  Allocates a new Python object representing an AST.  This is simply the
 *  'wrapper' object that holds a node* and allows it to be passed around in
 *  Python code.
 *
 */
static PyObject*
parser_newastobject(node *ast, int type)
{
    PyAST_Object* o = PyObject_New(PyAST_Object, &PyAST_Type);

    if (o != 0) {
        o->ast_node = ast;
        o->ast_type = type;
    }
    else {
        PyNode_Free(ast);
    }
    return ((PyObject*)o);
}


/*  void parser_free(PyAST_Object* ast)
 *
 *  This is called by a del statement that reduces the reference count to 0.
 *
 */
static void
parser_free(PyAST_Object *ast)
{
    PyNode_Free(ast->ast_node);
    PyObject_Del(ast);
}


/*  parser_ast2tuple(PyObject* self, PyObject* args, PyObject* kw)
 *
 *  This provides conversion from a node* to a tuple object that can be
 *  returned to the Python-level caller.  The AST object is not modified.
 *
 */
static PyObject*
parser_ast2tuple(PyAST_Object *self, PyObject *args, PyObject *kw)
{
    PyObject *line_option = 0;
    PyObject *res = 0;
    int ok;

    static char *keywords[] = {"ast", "line_info", NULL};

    if (self == NULL) {
        ok = PyArg_ParseTupleAndKeywords(args, kw, "O!|O:ast2tuple", keywords,
                                         &PyAST_Type, &self, &line_option);
    }
    else
        ok = PyArg_ParseTupleAndKeywords(args, kw, "|O:totuple", &keywords[1],
                                         &line_option);
    if (ok != 0) {
        int lineno = 0;
        if (line_option != NULL) {
            lineno = (PyObject_IsTrue(line_option) != 0) ? 1 : 0;
        }
        /*
         *  Convert AST into a tuple representation.  Use Guido's function,
         *  since it's known to work already.
         */
        res = node2tuple(((PyAST_Object*)self)->ast_node,
                         PyTuple_New, PyTuple_SetItem, lineno);
    }
    return (res);
}


/*  parser_ast2list(PyObject* self, PyObject* args, PyObject* kw)
 *
 *  This provides conversion from a node* to a list object that can be
 *  returned to the Python-level caller.  The AST object is not modified.
 *
 */
static PyObject*
parser_ast2list(PyAST_Object *self, PyObject *args, PyObject *kw)
{
    PyObject *line_option = 0;
    PyObject *res = 0;
    int ok;

    static char *keywords[] = {"ast", "line_info", NULL};

    if (self == NULL)
        ok = PyArg_ParseTupleAndKeywords(args, kw, "O!|O:ast2list", keywords,
                                         &PyAST_Type, &self, &line_option);
    else
        ok = PyArg_ParseTupleAndKeywords(args, kw, "|O:tolist", &keywords[1],
                                         &line_option);
    if (ok) {
        int lineno = 0;
        if (line_option != 0) {
            lineno = PyObject_IsTrue(line_option) ? 1 : 0;
        }
        /*
         *  Convert AST into a tuple representation.  Use Guido's function,
         *  since it's known to work already.
         */
        res = node2tuple(self->ast_node,
                         PyList_New, PyList_SetItem, lineno);
    }
    return (res);
}


/*  parser_compileast(PyObject* self, PyObject* args)
 *
 *  This function creates code objects from the parse tree represented by
 *  the passed-in data object.  An optional file name is passed in as well.
 *
 */
static PyObject*
parser_compileast(PyAST_Object *self, PyObject *args, PyObject *kw)
{
    PyObject*     res = 0;
    char*         str = "<ast>";
    int ok;

    static char *keywords[] = {"ast", "filename", NULL};

    if (self == NULL)
        ok = PyArg_ParseTupleAndKeywords(args, kw, "O!|s:compileast", keywords,
                                         &PyAST_Type, &self, &str);
    else
        ok = PyArg_ParseTupleAndKeywords(args, kw, "|s:compile", &keywords[1],
                                         &str);

    if (ok)
        res = (PyObject *)PyNode_Compile(self->ast_node, str);

    return (res);
}


/*  PyObject* parser_isexpr(PyObject* self, PyObject* args)
 *  PyObject* parser_issuite(PyObject* self, PyObject* args)
 *
 *  Checks the passed-in AST object to determine if it is an expression or
 *  a statement suite, respectively.  The return is a Python truth value.
 *
 */
static PyObject*
parser_isexpr(PyAST_Object *self, PyObject *args, PyObject *kw)
{
    PyObject* res = 0;
    int ok;

    static char *keywords[] = {"ast", NULL};

    if (self == NULL)
        ok = PyArg_ParseTupleAndKeywords(args, kw, "O!:isexpr", keywords,
                                         &PyAST_Type, &self);
    else
        ok = PyArg_ParseTupleAndKeywords(args, kw, ":isexpr", &keywords[1]);

    if (ok) {
        /* Check to see if the AST represents an expression or not. */
        res = (self->ast_type == PyAST_EXPR) ? Py_True : Py_False;
        Py_INCREF(res);
    }
    return (res);
}


static PyObject*
parser_issuite(PyAST_Object *self, PyObject *args, PyObject *kw)
{
    PyObject* res = 0;
    int ok;

    static char *keywords[] = {"ast", NULL};

    if (self == NULL)
        ok = PyArg_ParseTupleAndKeywords(args, kw, "O!:issuite", keywords,
                                         &PyAST_Type, &self);
    else
        ok = PyArg_ParseTupleAndKeywords(args, kw, ":issuite", &keywords[1]);

    if (ok) {
        /* Check to see if the AST represents an expression or not. */
        res = (self->ast_type == PyAST_EXPR) ? Py_False : Py_True;
        Py_INCREF(res);
    }
    return (res);
}


#define PUBLIC_METHOD_TYPE (METH_VARARGS|METH_KEYWORDS)

static PyMethodDef
parser_methods[] = {
    {"compile",         (PyCFunction)parser_compileast, PUBLIC_METHOD_TYPE,
        "Compile this AST object into a code object."},
    {"isexpr",          (PyCFunction)parser_isexpr,     PUBLIC_METHOD_TYPE,
        "Determines if this AST object was created from an expression."},
    {"issuite",         (PyCFunction)parser_issuite,    PUBLIC_METHOD_TYPE,
        "Determines if this AST object was created from a suite."},
    {"tolist",          (PyCFunction)parser_ast2list,   PUBLIC_METHOD_TYPE,
        "Creates a list-tree representation of this AST."},
    {"totuple",         (PyCFunction)parser_ast2tuple,  PUBLIC_METHOD_TYPE,
        "Creates a tuple-tree representation of this AST."},

    {NULL, NULL, 0, NULL}
};


static PyObject*
parser_getattr(PyObject *self, char *name)
{
    return (Py_FindMethod(parser_methods, self, name));
}


/*  err_string(char* message)
 *
 *  Sets the error string for an exception of type ParserError.
 *
 */
static void
err_string(char *message)
{
    PyErr_SetString(parser_error, message);
}


/*  PyObject* parser_do_parse(PyObject* args, int type)
 *
 *  Internal function to actually execute the parse and return the result if
 *  successful, or set an exception if not.
 *
 */
static PyObject*
parser_do_parse(PyObject *args, PyObject *kw, char *argspec, int type)
{
    char*     string = 0;
    PyObject* res    = 0;

    static char *keywords[] = {"source", NULL};

    if (PyArg_ParseTupleAndKeywords(args, kw, argspec, keywords, &string)) {
        node* n = PyParser_SimpleParseString(string,
                                             (type == PyAST_EXPR)
                                             ? eval_input : file_input);

        if (n != 0)
            res = parser_newastobject(n, type);
        else
            err_string("Could not parse string.");
    }
    return (res);
}


/*  PyObject* parser_expr(PyObject* self, PyObject* args)
 *  PyObject* parser_suite(PyObject* self, PyObject* args)
 *
 *  External interfaces to the parser itself.  Which is called determines if
 *  the parser attempts to recognize an expression ('eval' form) or statement
 *  suite ('exec' form).  The real work is done by parser_do_parse() above.
 *
 */
static PyObject*
parser_expr(PyAST_Object *self, PyObject *args, PyObject *kw)
{
    NOTE(ARGUNUSED(self))
    return (parser_do_parse(args, kw, "s:expr", PyAST_EXPR));
}


static PyObject*
parser_suite(PyAST_Object *self, PyObject *args, PyObject *kw)
{
    NOTE(ARGUNUSED(self))
    return (parser_do_parse(args, kw, "s:suite", PyAST_SUITE));
}



/*  This is the messy part of the code.  Conversion from a tuple to an AST
 *  object requires that the input tuple be valid without having to rely on
 *  catching an exception from the compiler.  This is done to allow the
 *  compiler itself to remain fast, since most of its input will come from
 *  the parser directly, and therefore be known to be syntactically correct.
 *  This validation is done to ensure that we don't core dump the compile
 *  phase, returning an exception instead.
 *
 *  Two aspects can be broken out in this code:  creating a node tree from
 *  the tuple passed in, and verifying that it is indeed valid.  It may be
 *  advantageous to expand the number of AST types to include funcdefs and
 *  lambdadefs to take advantage of the optimizer, recognizing those ASTs
 *  here.  They are not necessary, and not quite as useful in a raw form.
 *  For now, let's get expressions and suites working reliably.
 */


staticforward node* build_node_tree(PyObject *tuple);
staticforward int   validate_expr_tree(node *tree);
staticforward int   validate_file_input(node *tree);


/*  PyObject* parser_tuple2ast(PyObject* self, PyObject* args)
 *
 *  This is the public function, called from the Python code.  It receives a
 *  single tuple object from the caller, and creates an AST object if the
 *  tuple can be validated.  It does this by checking the first code of the
 *  tuple, and, if acceptable, builds the internal representation.  If this
 *  step succeeds, the internal representation is validated as fully as
 *  possible with the various validate_*() routines defined below.
 *
 *  This function must be changed if support is to be added for PyAST_FRAGMENT
 *  AST objects.
 *
 */
static PyObject*
parser_tuple2ast(PyAST_Object *self, PyObject *args, PyObject *kw)
{
    NOTE(ARGUNUSED(self))
    PyObject *ast = 0;
    PyObject *tuple = 0;
    PyObject *temp = 0;
    int ok;
    int start_sym = 0;

    static char *keywords[] = {"sequence", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kw, "O:tuple2ast", keywords,
                                     &tuple))
        return (0);
    if (!PySequence_Check(tuple)) {
        PyErr_SetString(PyExc_ValueError,
                        "tuple2ast() requires a single sequence argument");
        return (0);
    }
    /*
     *  This mess of tests is written this way so we can use the abstract
     *  object interface (AOI).  Unfortunately, the AOI increments reference
     *  counts, which requires that we store a pointer to retrieved object
     *  so we can DECREF it after the check.  But we really should accept
     *  lists as well as tuples at the very least.
     */
    ok = PyObject_Size(tuple) >= 2;
    if (ok) {
        temp = PySequence_GetItem(tuple, 0);
        ok = (temp != NULL) && PyInt_Check(temp);
        if (ok)
            /* this is used after the initial checks: */
            start_sym = PyInt_AS_LONG(temp);
        Py_XDECREF(temp);
    }
    if (ok) {
        temp = PySequence_GetItem(tuple, 1);
        ok = (temp != NULL) && PySequence_Check(temp);
        Py_XDECREF(temp);
    }
    if (ok) {
        temp = PySequence_GetItem(tuple, 1);
        ok = (temp != NULL) && PyObject_Size(temp) >= 2;
        if (ok) {
            PyObject *temp2 = PySequence_GetItem(temp, 0);
            if (temp2 != NULL) {
                ok = PyInt_Check(temp2);
                Py_DECREF(temp2);
            }
        }
        Py_XDECREF(temp);
    }
    /* If we've failed at some point, get out of here. */
    if (!ok) {
        err_string("malformed sequence for tuple2ast()");
        return (0);
    }
    /*
     *  This might be a valid parse tree, but let's do a quick check
     *  before we jump the gun.
     */
    if (start_sym == eval_input) {
        /*  Might be an eval form.  */
        node* expression = build_node_tree(tuple);

        if ((expression != 0) && validate_expr_tree(expression))
            ast = parser_newastobject(expression, PyAST_EXPR);
    }
    else if (start_sym == file_input) {
        /*  This looks like an exec form so far.  */
        node* suite_tree = build_node_tree(tuple);

        if ((suite_tree != 0) && validate_file_input(suite_tree))
            ast = parser_newastobject(suite_tree, PyAST_SUITE);
    }
    else
        /*  This is a fragment, and is not yet supported.  Maybe they
         *  will be if I find a use for them.
         */
        err_string("Fragmentary parse trees not supported.");

    /*  Make sure we throw an exception on all errors.  We should never
     *  get this, but we'd do well to be sure something is done.
     */
    if ((ast == 0) && !PyErr_Occurred())
        err_string("Unspecified ast error occurred.");

    return (ast);
}


/*  int check_terminal_tuple()
 *
 *  Check a tuple to determine that it is indeed a valid terminal
 *  node.  The node is known to be required as a terminal, so we throw
 *  an exception if there is a failure.
 *
 *  The format of an acceptable terminal tuple is "(is[i])": the fact
 *  that elem is a tuple and the integer is a valid terminal symbol
 *  has been established before this function is called.  We must
 *  check the length of the tuple and the type of the second element
 *  and optional third element.  We do *NOT* check the actual text of
 *  the string element, which we could do in many cases.  This is done
 *  by the validate_*() functions which operate on the internal
 *  representation.
 */
static int
check_terminal_tuple(PyObject *elem)
{
    int   len = PyObject_Size(elem);
    int   res = 1;
    char* str = "Illegal terminal symbol; bad node length.";

    if ((len == 2) || (len == 3)) {
        PyObject *temp = PySequence_GetItem(elem, 1);
        res = PyString_Check(temp);
        str = "Illegal terminal symbol; expected a string.";
        if (res && (len == 3)) {
            PyObject* third = PySequence_GetItem(elem, 2);
            res = PyInt_Check(third);
            str = "Invalid third element of terminal node.";
            Py_XDECREF(third);
        }
        Py_XDECREF(temp);
    }
    else {
        res = 0;
    }
    if (!res) {
        elem = Py_BuildValue("(os)", elem, str);
        PyErr_SetObject(parser_error, elem);
    }
    return (res);
}


/*  node* build_node_children()
 *
 *  Iterate across the children of the current non-terminal node and build
 *  their structures.  If successful, return the root of this portion of
 *  the tree, otherwise, 0.  Any required exception will be specified already,
 *  and no memory will have been deallocated.
 *
 */
static node*
build_node_children(PyObject *tuple, node *root, int *line_num)
{
    int len = PyObject_Size(tuple);
    int i;

    for (i = 1; i < len; ++i) {
        /* elem must always be a tuple, however simple */
        PyObject* elem = PySequence_GetItem(tuple, i);
        int ok = elem != NULL;
        long  type = 0;
        char *strn = 0;

        if (ok)
            ok = PySequence_Check(elem);
        if (ok) {
            PyObject *temp = PySequence_GetItem(elem, 0);
            if (temp == NULL)
                ok = 0;
            else {
                ok = PyInt_Check(temp);
                if (ok)
                    type = PyInt_AS_LONG(temp);
                Py_DECREF(temp);
            }
        }
        if (!ok) {
            PyErr_SetObject(parser_error,
                            Py_BuildValue("(os)", elem,
                                          "Illegal node construct."));
            Py_XDECREF(elem);
            return (0);
        }
        if (ISTERMINAL(type)) {
            if (check_terminal_tuple(elem)) {
                PyObject *temp = PySequence_GetItem(elem, 1);

                /* check_terminal_tuple() already verified it's a string */
                strn = (char *)PyMem_MALLOC(PyString_GET_SIZE(temp) + 1);
                if (strn != NULL)
                    (void) strcpy(strn, PyString_AS_STRING(temp));
                Py_DECREF(temp);

                if (PyObject_Size(elem) == 3) {
                    PyObject* temp = PySequence_GetItem(elem, 2);
                    *line_num = PyInt_AsLong(temp);
                    Py_DECREF(temp);
                }
            }
            else {
                Py_XDECREF(elem);
                return (0);
            }
        }
        else if (!ISNONTERMINAL(type)) {
            /*
             *  It has to be one or the other; this is an error.
             *  Throw an exception.
             */
            PyErr_SetObject(parser_error,
                            Py_BuildValue("(os)", elem,
                                          "Unknown node type."));
            Py_XDECREF(elem);
            return (0);
        }
        PyNode_AddChild(root, type, strn, *line_num);

        if (ISNONTERMINAL(type)) {
            node* new_child = CHILD(root, i - 1);

            if (new_child != build_node_children(elem, new_child, line_num)) {
                Py_XDECREF(elem);
                return (0);
            }
        }
        else if (type == NEWLINE) {     /* It's true:  we increment the     */
            ++(*line_num);              /* line number *after* the newline! */
        }
        Py_XDECREF(elem);
    }
    return (root);
}


static node*
build_node_tree(PyObject *tuple)
{
    node* res = 0;
    PyObject *temp = PySequence_GetItem(tuple, 0);
    long  num = -1;

    if (temp != NULL)
        num = PyInt_AsLong(temp);
    Py_XDECREF(temp);
    if (ISTERMINAL(num)) {
        /*
         *  The tuple is simple, but it doesn't start with a start symbol.
         *  Throw an exception now and be done with it.
         */
        tuple = Py_BuildValue("(os)", tuple,
                    "Illegal ast tuple; cannot start with terminal symbol.");
        PyErr_SetObject(parser_error, tuple);
    }
    else if (ISNONTERMINAL(num)) {
        /*
         *  Not efficient, but that can be handled later.
         */
        int line_num = 0;

        res = PyNode_New(num);
        if (res != build_node_children(tuple, res, &line_num)) {
            PyNode_Free(res);
            res = 0;
        }
    }
    else
        /*  The tuple is illegal -- if the number is neither TERMINAL nor
         *  NONTERMINAL, we can't use it.
         */
        PyErr_SetObject(parser_error,
                        Py_BuildValue("(os)", tuple,
                                      "Illegal component tuple."));

    return (res);
}


#define VALIDATER(n)    static int validate_##n(node *tree)


/*
 *  Validation routines used within the validation section:
 */
staticforward int validate_terminal(node *terminal, int type, char *string);

#define validate_ampersand(ch)  validate_terminal(ch,      AMPER, "&")
#define validate_circumflex(ch) validate_terminal(ch, CIRCUMFLEX, "^")
#define validate_colon(ch)      validate_terminal(ch,      COLON, ":")
#define validate_comma(ch)      validate_terminal(ch,      COMMA, ",")
#define validate_dedent(ch)     validate_terminal(ch,     DEDENT, "")
#define validate_equal(ch)      validate_terminal(ch,      EQUAL, "=")
#define validate_indent(ch)     validate_terminal(ch,     INDENT, (char*)NULL)
#define validate_lparen(ch)     validate_terminal(ch,       LPAR, "(")
#define validate_newline(ch)    validate_terminal(ch,    NEWLINE, (char*)NULL)
#define validate_rparen(ch)     validate_terminal(ch,       RPAR, ")")
#define validate_semi(ch)       validate_terminal(ch,       SEMI, ";")
#define validate_star(ch)       validate_terminal(ch,       STAR, "*")
#define validate_vbar(ch)       validate_terminal(ch,       VBAR, "|")
#define validate_doublestar(ch) validate_terminal(ch, DOUBLESTAR, "**")
#define validate_dot(ch)        validate_terminal(ch,        DOT, ".")
#define validate_name(ch, str)  validate_terminal(ch,       NAME, str)

VALIDATER(node);                VALIDATER(small_stmt);
VALIDATER(class);               VALIDATER(node);
VALIDATER(parameters);          VALIDATER(suite);
VALIDATER(testlist);            VALIDATER(varargslist);
VALIDATER(fpdef);               VALIDATER(fplist);
VALIDATER(stmt);                VALIDATER(simple_stmt);
VALIDATER(expr_stmt);           VALIDATER(power);
VALIDATER(print_stmt);          VALIDATER(del_stmt);
VALIDATER(return_stmt);
VALIDATER(raise_stmt);          VALIDATER(import_stmt);
VALIDATER(global_stmt);
VALIDATER(assert_stmt);
VALIDATER(exec_stmt);           VALIDATER(compound_stmt);
VALIDATER(while);               VALIDATER(for);
VALIDATER(try);                 VALIDATER(except_clause);
VALIDATER(test);                VALIDATER(and_test);
VALIDATER(not_test);            VALIDATER(comparison);
VALIDATER(comp_op);             VALIDATER(expr);
VALIDATER(xor_expr);            VALIDATER(and_expr);
VALIDATER(shift_expr);          VALIDATER(arith_expr);
VALIDATER(term);                VALIDATER(factor);
VALIDATER(atom);                VALIDATER(lambdef);
VALIDATER(trailer);             VALIDATER(subscript);
VALIDATER(subscriptlist);       VALIDATER(sliceop);
VALIDATER(exprlist);            VALIDATER(dictmaker);
VALIDATER(arglist);             VALIDATER(argument);


#define is_even(n)      (((n) & 1) == 0)
#define is_odd(n)       (((n) & 1) == 1)


static int
validate_ntype(node *n, int t)
{
    int res = (TYPE(n) == t);

    if (!res) {
        char buffer[128];
        (void) sprintf(buffer, "Expected node type %d, got %d.", t, TYPE(n));
        err_string(buffer);
    }
    return (res);
}


/*  Verifies that the number of child nodes is exactly 'num', raising
 *  an exception if it isn't.  The exception message does not indicate
 *  the exact number of nodes, allowing this to be used to raise the
 *  "right" exception when the wrong number of nodes is present in a
 *  specific variant of a statement's syntax.  This is commonly used
 *  in that fashion.
 */
static int
validate_numnodes(node *n, int num, const char *const name)
{
    if (NCH(n) != num) {
        char buff[60];
        (void) sprintf(buff, "Illegal number of children for %s node.", name);
        err_string(buff);
    }
    return (NCH(n) == num);
}


static int
validate_terminal(node *terminal, int type, char *string)
{
    int res = (validate_ntype(terminal, type)
               && ((string == 0) || (strcmp(string, STR(terminal)) == 0)));

    if (!res && !PyErr_Occurred()) {
        char buffer[60];
        (void) sprintf(buffer, "Illegal terminal: expected \"%s\"", string);
        err_string(buffer);
    }
    return (res);
}


/*  X (',' X) [',']
 */
static int
validate_repeating_list(node *tree, int ntype, int (*vfunc)(),
                        const char *const name)
{
    int nch = NCH(tree);
    int res = (nch && validate_ntype(tree, ntype)
               && vfunc(CHILD(tree, 0)));

    if (!res && !PyErr_Occurred())
        (void) validate_numnodes(tree, 1, name);
    else {
        if (is_even(nch))
            res = validate_comma(CHILD(tree, --nch));
        if (res && nch > 1) {
            int pos = 1;
            for ( ; res && pos < nch; pos += 2)
                res = (validate_comma(CHILD(tree, pos))
                       && vfunc(CHILD(tree, pos + 1)));
        }
    }
    return (res);
}


/*  VALIDATE(class)
 *
 *  classdef:
 *      'class' NAME ['(' testlist ')'] ':' suite
 */
static int
validate_class(node *tree)
{
    int nch = NCH(tree);
    int res = validate_ntype(tree, classdef) && ((nch == 4) || (nch == 7));

    if (res) {
        res = (validate_name(CHILD(tree, 0), "class")
               && validate_ntype(CHILD(tree, 1), NAME)
               && validate_colon(CHILD(tree, nch - 2))
               && validate_suite(CHILD(tree, nch - 1)));
    }
    else
        (void) validate_numnodes(tree, 4, "class");
    if (res && (nch == 7)) {
        res = (validate_lparen(CHILD(tree, 2))
               && validate_testlist(CHILD(tree, 3))
               && validate_rparen(CHILD(tree, 4)));
    }
    return (res);
}


/*  if_stmt:
 *      'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]
 */
static int
validate_if(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, if_stmt)
               && (nch >= 4)
               && validate_name(CHILD(tree, 0), "if")
               && validate_test(CHILD(tree, 1))
               && validate_colon(CHILD(tree, 2))
               && validate_suite(CHILD(tree, 3)));

    if (res && ((nch % 4) == 3)) {
        /*  ... 'else' ':' suite  */
        res = (validate_name(CHILD(tree, nch - 3), "else")
               && validate_colon(CHILD(tree, nch - 2))
               && validate_suite(CHILD(tree, nch - 1)));
        nch -= 3;
    }
    else if (!res && !PyErr_Occurred())
        (void) validate_numnodes(tree, 4, "if");
    if ((nch % 4) != 0)
        /* Will catch the case for nch < 4 */
        res = validate_numnodes(tree, 0, "if");
    else if (res && (nch > 4)) {
        /*  ... ('elif' test ':' suite)+ ...  */
        int j = 4;
        while ((j < nch) && res) {
            res = (validate_name(CHILD(tree, j), "elif")
                   && validate_colon(CHILD(tree, j + 2))
                   && validate_test(CHILD(tree, j + 1))
                   && validate_suite(CHILD(tree, j + 3)));
            j += 4;
        }
    }
    return (res);
}


/*  parameters:
 *      '(' [varargslist] ')'
 *
 */
static int
validate_parameters(node *tree)
{
    int nch = NCH(tree);
    int res = validate_ntype(tree, parameters) && ((nch == 2) || (nch == 3));

    if (res) {
        res = (validate_lparen(CHILD(tree, 0))
               && validate_rparen(CHILD(tree, nch - 1)));
        if (res && (nch == 3))
            res = validate_varargslist(CHILD(tree, 1));
    }
    else {
        (void) validate_numnodes(tree, 2, "parameters");
    }
    return (res);
}


/*  VALIDATE(suite)
 *
 *  suite:
 *      simple_stmt
 *    | NEWLINE INDENT stmt+ DEDENT
 */
static int
validate_suite(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, suite) && ((nch == 1) || (nch >= 4)));

    if (res && (nch == 1))
        res = validate_simple_stmt(CHILD(tree, 0));
    else if (res) {
        /*  NEWLINE INDENT stmt+ DEDENT  */
        res = (validate_newline(CHILD(tree, 0))
               && validate_indent(CHILD(tree, 1))
               && validate_stmt(CHILD(tree, 2))
               && validate_dedent(CHILD(tree, nch - 1)));

        if (res && (nch > 4)) {
            int i = 3;
            --nch;                      /* forget the DEDENT     */
            for ( ; res && (i < nch); ++i)
                res = validate_stmt(CHILD(tree, i));
        }
        else if (nch < 4)
            res = validate_numnodes(tree, 4, "suite");
    }
    return (res);
}


static int
validate_testlist(node *tree)
{
    return (validate_repeating_list(tree, testlist,
                                    validate_test, "testlist"));
}


/*  VALIDATE(varargslist)
 *
 *  varargslist:
 *      (fpdef ['=' test] ',')* ('*' NAME [',' '*' '*' NAME] | '*' '*' NAME)
 *    | fpdef ['=' test] (',' fpdef ['=' test])* [',']
 *
 *      (fpdef ['=' test] ',')*
 *           ('*' NAME [',' ('**'|'*' '*') NAME]
 *         | ('**'|'*' '*') NAME)
 *    | fpdef ['=' test] (',' fpdef ['=' test])* [',']
 *
 */
static int
validate_varargslist(node *tree)
{
    int nch = NCH(tree);
    int res = validate_ntype(tree, varargslist) && (nch != 0);

    if (res && (nch >= 2) && (TYPE(CHILD(tree, nch - 1)) == NAME)) {
        /*  (fpdef ['=' test] ',')*
         *  ('*' NAME [',' '*' '*' NAME] | '*' '*' NAME)
         */
        int pos = 0;
        int remaining = nch;

        while (res && (TYPE(CHILD(tree, pos)) == fpdef)) {
            res = validate_fpdef(CHILD(tree, pos));
            if (res) {
                if (TYPE(CHILD(tree, pos + 1)) == EQUAL) {
                    res = validate_test(CHILD(tree, pos + 2));
                    pos += 2;
                }
                res = res && validate_comma(CHILD(tree, pos + 1));
                pos += 2;
            }
        }
        if (res) {
            remaining = nch - pos;
            res = ((remaining == 2) || (remaining == 3)
                   || (remaining == 5) || (remaining == 6));
            if (!res)
                (void) validate_numnodes(tree, 2, "varargslist");
            else if (TYPE(CHILD(tree, pos)) == DOUBLESTAR)
                return ((remaining == 2)
                        && validate_ntype(CHILD(tree, pos+1), NAME));
            else {
                res = validate_star(CHILD(tree, pos++));
                --remaining;
            }
        }
        if (res) {
            if (remaining == 2) {
                res = (validate_star(CHILD(tree, pos))
                       && validate_ntype(CHILD(tree, pos + 1), NAME));
            }
            else {
                res = validate_ntype(CHILD(tree, pos++), NAME);
                if (res && (remaining >= 4)) {
                    res = validate_comma(CHILD(tree, pos));
                    if (--remaining == 3)
                        res = (validate_star(CHILD(tree, pos + 1))
                               && validate_star(CHILD(tree, pos + 2)));
                    else
                        res = validate_ntype(CHILD(tree, pos + 1), DOUBLESTAR);
                }
            }
        }
        if (!res && !PyErr_Occurred())
            err_string("Incorrect validation of variable arguments list.");
    }
    else if (res) {
        /*  fpdef ['=' test] (',' fpdef ['=' test])* [',']  */
        if (TYPE(CHILD(tree, nch - 1)) == COMMA)
            --nch;

        /*  fpdef ['=' test] (',' fpdef ['=' test])*  */
        res = (is_odd(nch)
               && validate_fpdef(CHILD(tree, 0)));

        if (res && (nch > 1)) {
            int pos = 1;
            if (TYPE(CHILD(tree, 1)) == EQUAL) {
                res = validate_test(CHILD(tree, 2));
                pos += 2;
            }
            /*  ... (',' fpdef ['=' test])*  */
            for ( ; res && (pos < nch); pos += 2) {
                /* ',' fpdef */
                res = (validate_comma(CHILD(tree, pos))
                       && validate_fpdef(CHILD(tree, pos + 1)));
                if (res
                    && ((nch - pos) > 2)
                    && (TYPE(CHILD(tree, pos + 2)) == EQUAL)) {
                    /* ['=' test] */
                    res = validate_test(CHILD(tree, pos + 3));
                    pos += 2;
                }
            }
        }
    }
    else {
        err_string("Improperly formed argument list.");
    }
    return (res);
}


/*  VALIDATE(fpdef)
 *
 *  fpdef:
 *      NAME
 *    | '(' fplist ')'
 */
static int
validate_fpdef(node *tree)
{
    int nch = NCH(tree);
    int res = validate_ntype(tree, fpdef);

    if (res) {
        if (nch == 1)
            res = validate_ntype(CHILD(tree, 0), NAME);
        else if (nch == 3)
            res = (validate_lparen(CHILD(tree, 0))
                   && validate_fplist(CHILD(tree, 1))
                   && validate_rparen(CHILD(tree, 2)));
        else
            res = validate_numnodes(tree, 1, "fpdef");
    }
    return (res);
}


static int
validate_fplist(node *tree)
{
    return (validate_repeating_list(tree, fplist,
                                    validate_fpdef, "fplist"));
}


/*  simple_stmt | compound_stmt
 *
 */
static int
validate_stmt(node *tree)
{
    int res = (validate_ntype(tree, stmt)
               && validate_numnodes(tree, 1, "stmt"));

    if (res) {
        tree = CHILD(tree, 0);

        if (TYPE(tree) == simple_stmt)
            res = validate_simple_stmt(tree);
        else
            res = validate_compound_stmt(tree);
    }
    return (res);
}


/*  small_stmt (';' small_stmt)* [';'] NEWLINE
 *
 */
static int
validate_simple_stmt(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, simple_stmt)
               && (nch >= 2)
               && validate_small_stmt(CHILD(tree, 0))
               && validate_newline(CHILD(tree, nch - 1)));

    if (nch < 2)
        res = validate_numnodes(tree, 2, "simple_stmt");
    --nch;                              /* forget the NEWLINE    */
    if (res && is_even(nch))
        res = validate_semi(CHILD(tree, --nch));
    if (res && (nch > 2)) {
        int i;

        for (i = 1; res && (i < nch); i += 2)
            res = (validate_semi(CHILD(tree, i))
                   && validate_small_stmt(CHILD(tree, i + 1)));
    }
    return (res);
}


static int
validate_small_stmt(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_numnodes(tree, 1, "small_stmt")
               && ((TYPE(CHILD(tree, 0)) == expr_stmt)
                   || (TYPE(CHILD(tree, 0)) == print_stmt)
                   || (TYPE(CHILD(tree, 0)) == del_stmt)
                   || (TYPE(CHILD(tree, 0)) == pass_stmt)
                   || (TYPE(CHILD(tree, 0)) == flow_stmt)
                   || (TYPE(CHILD(tree, 0)) == import_stmt)
                   || (TYPE(CHILD(tree, 0)) == global_stmt)
                   || (TYPE(CHILD(tree, 0)) == assert_stmt)
                   || (TYPE(CHILD(tree, 0)) == exec_stmt)));

    if (res)
        res = validate_node(CHILD(tree, 0));
    else if (nch == 1) {
        char buffer[60];
        (void) sprintf(buffer, "Unrecognized child node of small_stmt: %d.",
                       TYPE(CHILD(tree, 0)));
        err_string(buffer);
    }
    return (res);
}


/*  compound_stmt:
 *      if_stmt | while_stmt | for_stmt | try_stmt | funcdef | classdef
 */
static int
validate_compound_stmt(node *tree)
{
    int res = (validate_ntype(tree, compound_stmt)
               && validate_numnodes(tree, 1, "compound_stmt"));

    if (!res)
        return (0);

    tree = CHILD(tree, 0);
    res = ((TYPE(tree) == if_stmt)
           || (TYPE(tree) == while_stmt)
           || (TYPE(tree) == for_stmt)
           || (TYPE(tree) == try_stmt)
           || (TYPE(tree) == funcdef)
           || (TYPE(tree) == classdef));
    if (res)
        res = validate_node(tree);
    else {
        char buffer[60];
        (void) sprintf(buffer, "Illegal compound statement type: %d.",
                       TYPE(tree));
        err_string(buffer);
    }
    return (res);
}


static int
validate_expr_stmt(node *tree)
{
    int j;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, expr_stmt)
               && is_odd(nch)
               && validate_testlist(CHILD(tree, 0)));

    for (j = 1; res && (j < nch); j += 2)
        res = (validate_equal(CHILD(tree, j))
               && validate_testlist(CHILD(tree, j + 1)));

    return (res);
}


/*  print_stmt:
 *
 *      'print' (test ',')* [test]
 *
 */
static int
validate_print_stmt(node *tree)
{
    int j;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, print_stmt)
               && (nch != 0)
               && validate_name(CHILD(tree, 0), "print"));

    if (res && is_even(nch)) {
        res = validate_test(CHILD(tree, nch - 1));
        --nch;
    }
    else if (!res && !PyErr_Occurred())
        (void) validate_numnodes(tree, 1, "print_stmt");
    for (j = 1; res && (j < nch); j += 2)
        res = (validate_test(CHILD(tree, j))
               && validate_ntype(CHILD(tree, j + 1), COMMA));

    return (res);
}


static int
validate_del_stmt(node *tree)
{
    return (validate_numnodes(tree, 2, "del_stmt")
            && validate_name(CHILD(tree, 0), "del")
            && validate_exprlist(CHILD(tree, 1)));
}


static int
validate_return_stmt(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, return_stmt)
               && ((nch == 1) || (nch == 2))
               && validate_name(CHILD(tree, 0), "return"));

    if (res && (nch == 2))
        res = validate_testlist(CHILD(tree, 1));

    return (res);
}


static int
validate_raise_stmt(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, raise_stmt)
               && ((nch == 1) || (nch == 2) || (nch == 4) || (nch == 6)));

    if (res) {
        res = validate_name(CHILD(tree, 0), "raise");
        if (res && (nch >= 2))
            res = validate_test(CHILD(tree, 1));
        if (res && nch > 2) {
            res = (validate_comma(CHILD(tree, 2))
                   && validate_test(CHILD(tree, 3)));
            if (res && (nch > 4))
                res = (validate_comma(CHILD(tree, 4))
                       && validate_test(CHILD(tree, 5)));
        }
    }
    else
        (void) validate_numnodes(tree, 2, "raise");
    if (res && (nch == 4))
        res = (validate_comma(CHILD(tree, 2))
               && validate_test(CHILD(tree, 3)));

    return (res);
}


/*  import_stmt:
 *
 *    'import' dotted_name (',' dotted_name)*
 *  | 'from' dotted_name 'import' ('*' | NAME (',' NAME)*)
 */
static int
validate_import_stmt(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, import_stmt)
               && (nch >= 2) && is_even(nch)
               && validate_ntype(CHILD(tree, 0), NAME)
               && validate_ntype(CHILD(tree, 1), dotted_name));

    if (res && (strcmp(STR(CHILD(tree, 0)), "import") == 0)) {
        int j;

        for (j = 2; res && (j < nch); j += 2)
            res = (validate_comma(CHILD(tree, j))
                   && validate_ntype(CHILD(tree, j + 1), dotted_name));
    }
    else if (res && validate_name(CHILD(tree, 0), "from")) {
        res = ((nch >= 4) && is_even(nch)
               && validate_name(CHILD(tree, 2), "import"));
        if (nch == 4) {
            res = ((TYPE(CHILD(tree, 3)) == NAME)
                   || (TYPE(CHILD(tree, 3)) == STAR));
            if (!res)
                err_string("Illegal import statement.");
        }
        else {
            /*  'from' NAME 'import' NAME (',' NAME)+  */
            int j;
            res = validate_ntype(CHILD(tree, 3), NAME);
            for (j = 4; res && (j < nch); j += 2)
                res = (validate_comma(CHILD(tree, j))
                       && validate_ntype(CHILD(tree, j + 1), NAME));
        }
    }
    else
        res = 0;

    return (res);
}


static int
validate_global_stmt(node *tree)
{
    int j;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, global_stmt)
               && is_even(nch) && (nch >= 2));

    if (res)
        res = (validate_name(CHILD(tree, 0), "global")
               && validate_ntype(CHILD(tree, 1), NAME));
    for (j = 2; res && (j < nch); j += 2)
        res = (validate_comma(CHILD(tree, j))
               && validate_ntype(CHILD(tree, j + 1), NAME));

    return (res);
}


/*  exec_stmt:
 *
 *  'exec' expr ['in' test [',' test]]
 */
static int
validate_exec_stmt(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, exec_stmt)
               && ((nch == 2) || (nch == 4) || (nch == 6))
               && validate_name(CHILD(tree, 0), "exec")
               && validate_expr(CHILD(tree, 1)));

    if (!res && !PyErr_Occurred())
        err_string("Illegal exec statement.");
    if (res && (nch > 2))
        res = (validate_name(CHILD(tree, 2), "in")
               && validate_test(CHILD(tree, 3)));
    if (res && (nch == 6))
        res = (validate_comma(CHILD(tree, 4))
               && validate_test(CHILD(tree, 5)));

    return (res);
}


/*  assert_stmt:
 *
 *  'assert' test [',' test]
 */
static int
validate_assert_stmt(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, assert_stmt)
               && ((nch == 2) || (nch == 4))
               && (validate_name(CHILD(tree, 0), "__assert__") ||
                   validate_name(CHILD(tree, 0), "assert"))
               && validate_test(CHILD(tree, 1)));

    if (!res && !PyErr_Occurred())
        err_string("Illegal assert statement.");
    if (res && (nch > 2))
        res = (validate_comma(CHILD(tree, 2))
               && validate_test(CHILD(tree, 3)));

    return (res);
}


static int
validate_while(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, while_stmt)
               && ((nch == 4) || (nch == 7))
               && validate_name(CHILD(tree, 0), "while")
               && validate_test(CHILD(tree, 1))
               && validate_colon(CHILD(tree, 2))
               && validate_suite(CHILD(tree, 3)));

    if (res && (nch == 7))
        res = (validate_name(CHILD(tree, 4), "else")
               && validate_colon(CHILD(tree, 5))
               && validate_suite(CHILD(tree, 6)));

    return (res);
}


static int
validate_for(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, for_stmt)
               && ((nch == 6) || (nch == 9))
               && validate_name(CHILD(tree, 0), "for")
               && validate_exprlist(CHILD(tree, 1))
               && validate_name(CHILD(tree, 2), "in")
               && validate_testlist(CHILD(tree, 3))
               && validate_colon(CHILD(tree, 4))
               && validate_suite(CHILD(tree, 5)));

    if (res && (nch == 9))
        res = (validate_name(CHILD(tree, 6), "else")
               && validate_colon(CHILD(tree, 7))
               && validate_suite(CHILD(tree, 8)));

    return (res);
}


/*  try_stmt:
 *      'try' ':' suite (except_clause ':' suite)+ ['else' ':' suite]
 *    | 'try' ':' suite 'finally' ':' suite
 *
 */
static int
validate_try(node *tree)
{
    int nch = NCH(tree);
    int pos = 3;
    int res = (validate_ntype(tree, try_stmt)
               && (nch >= 6) && ((nch % 3) == 0));

    if (res)
        res = (validate_name(CHILD(tree, 0), "try")
               && validate_colon(CHILD(tree, 1))
               && validate_suite(CHILD(tree, 2))
               && validate_colon(CHILD(tree, nch - 2))
               && validate_suite(CHILD(tree, nch - 1)));
    else {
        const char* name = "except";
        char buffer[60];
        if (TYPE(CHILD(tree, nch - 3)) != except_clause)
            name = STR(CHILD(tree, nch - 3));
        (void) sprintf(buffer,
                       "Illegal number of children for try/%s node.", name);
        err_string(buffer);
    }
    /*  Skip past except_clause sections:  */
    while (res && (TYPE(CHILD(tree, pos)) == except_clause)) {
        res = (validate_except_clause(CHILD(tree, pos))
               && validate_colon(CHILD(tree, pos + 1))
               && validate_suite(CHILD(tree, pos + 2)));
        pos += 3;
    }
    if (res && (pos < nch)) {
        res = validate_ntype(CHILD(tree, pos), NAME);
        if (res && (strcmp(STR(CHILD(tree, pos)), "finally") == 0))
            res = (validate_numnodes(tree, 6, "try/finally")
                   && validate_colon(CHILD(tree, 4))
                   && validate_suite(CHILD(tree, 5)));
        else if (res) {
            if (nch == (pos + 3)) {
                res = ((strcmp(STR(CHILD(tree, pos)), "except") == 0)
                       || (strcmp(STR(CHILD(tree, pos)), "else") == 0));
                if (!res)
                    err_string("Illegal trailing triple in try statement.");
            }
            else if (nch == (pos + 6)) {
                res = (validate_name(CHILD(tree, pos), "except")
                       && validate_colon(CHILD(tree, pos + 1))
                       && validate_suite(CHILD(tree, pos + 2))
                       && validate_name(CHILD(tree, pos + 3), "else"));
            }
            else
                res = validate_numnodes(tree, pos + 3, "try/except");
        }
    }
    return (res);
}


static int
validate_except_clause(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, except_clause)
               && ((nch == 1) || (nch == 2) || (nch == 4))
               && validate_name(CHILD(tree, 0), "except"));

    if (res && (nch > 1))
        res = validate_test(CHILD(tree, 1));
    if (res && (nch == 4))
        res = (validate_comma(CHILD(tree, 2))
               && validate_test(CHILD(tree, 3)));

    return (res);
}


static int
validate_test(node *tree)
{
    int nch = NCH(tree);
    int res = validate_ntype(tree, test) && is_odd(nch);

    if (res && (TYPE(CHILD(tree, 0)) == lambdef))
        res = ((nch == 1)
               && validate_lambdef(CHILD(tree, 0)));
    else if (res) {
        int pos;
        res = validate_and_test(CHILD(tree, 0));
        for (pos = 1; res && (pos < nch); pos += 2)
            res = (validate_name(CHILD(tree, pos), "or")
                   && validate_and_test(CHILD(tree, pos + 1)));
    }
    return (res);
}


static int
validate_and_test(node *tree)
{
    int pos;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, and_test)
               && is_odd(nch)
               && validate_not_test(CHILD(tree, 0)));

    for (pos = 1; res && (pos < nch); pos += 2)
        res = (validate_name(CHILD(tree, pos), "and")
               && validate_not_test(CHILD(tree, 0)));

    return (res);
}


static int
validate_not_test(node *tree)
{
    int nch = NCH(tree);
    int res = validate_ntype(tree, not_test) && ((nch == 1) || (nch == 2));

    if (res) {
        if (nch == 2)
            res = (validate_name(CHILD(tree, 0), "not")
                   && validate_not_test(CHILD(tree, 1)));
        else if (nch == 1)
            res = validate_comparison(CHILD(tree, 0));
    }
    return (res);
}


static int
validate_comparison(node *tree)
{
    int pos;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, comparison)
               && is_odd(nch)
               && validate_expr(CHILD(tree, 0)));

    for (pos = 1; res && (pos < nch); pos += 2)
        res = (validate_comp_op(CHILD(tree, pos))
               && validate_expr(CHILD(tree, pos + 1)));

    return (res);
}


static int
validate_comp_op(node *tree)
{
    int res = 0;
    int nch = NCH(tree);

    if (!validate_ntype(tree, comp_op))
        return (0);
    if (nch == 1) {
        /*
         *  Only child will be a terminal with a well-defined symbolic name
         *  or a NAME with a string of either 'is' or 'in'
         */
        tree = CHILD(tree, 0);
        switch (TYPE(tree)) {
            case LESS:
            case GREATER:
            case EQEQUAL:
            case EQUAL:
            case LESSEQUAL:
            case GREATEREQUAL:
            case NOTEQUAL:
              res = 1;
              break;
            case NAME:
              res = ((strcmp(STR(tree), "in") == 0)
                     || (strcmp(STR(tree), "is") == 0));
              if (!res) {
                  char buff[128];
                  (void) sprintf(buff, "Illegal operator: '%s'.", STR(tree));
                  err_string(buff);
              }
              break;
          default:
              err_string("Illegal comparison operator type.");
              break;
        }
    }
    else if ((res = validate_numnodes(tree, 2, "comp_op")) != 0) {
        res = (validate_ntype(CHILD(tree, 0), NAME)
               && validate_ntype(CHILD(tree, 1), NAME)
               && (((strcmp(STR(CHILD(tree, 0)), "is") == 0)
                    && (strcmp(STR(CHILD(tree, 1)), "not") == 0))
                   || ((strcmp(STR(CHILD(tree, 0)), "not") == 0)
                       && (strcmp(STR(CHILD(tree, 1)), "in") == 0))));
        if (!res && !PyErr_Occurred())
            err_string("Unknown comparison operator.");
    }
    return (res);
}


static int
validate_expr(node *tree)
{
    int j;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, expr)
               && is_odd(nch)
               && validate_xor_expr(CHILD(tree, 0)));

    for (j = 2; res && (j < nch); j += 2)
        res = (validate_xor_expr(CHILD(tree, j))
               && validate_vbar(CHILD(tree, j - 1)));

    return (res);
}


static int
validate_xor_expr(node *tree)
{
    int j;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, xor_expr)
               && is_odd(nch)
               && validate_and_expr(CHILD(tree, 0)));

    for (j = 2; res && (j < nch); j += 2)
        res = (validate_circumflex(CHILD(tree, j - 1))
               && validate_and_expr(CHILD(tree, j)));

    return (res);
}


static int
validate_and_expr(node *tree)
{
    int pos;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, and_expr)
               && is_odd(nch)
               && validate_shift_expr(CHILD(tree, 0)));

    for (pos = 1; res && (pos < nch); pos += 2)
        res = (validate_ampersand(CHILD(tree, pos))
               && validate_shift_expr(CHILD(tree, pos + 1)));

    return (res);
}


static int
validate_chain_two_ops(node *tree, int (*termvalid)(node *), int op1, int op2)
 {
    int pos = 1;
    int nch = NCH(tree);
    int res = (is_odd(nch)
               && (*termvalid)(CHILD(tree, 0)));

    for ( ; res && (pos < nch); pos += 2) {
        if (TYPE(CHILD(tree, pos)) != op1)
            res = validate_ntype(CHILD(tree, pos), op2);
        if (res)
            res = (*termvalid)(CHILD(tree, pos + 1));
    }
    return (res);
}


static int
validate_shift_expr(node *tree)
{
    return (validate_ntype(tree, shift_expr)
            && validate_chain_two_ops(tree, validate_arith_expr,
                                      LEFTSHIFT, RIGHTSHIFT));
}


static int
validate_arith_expr(node *tree)
{
    return (validate_ntype(tree, arith_expr)
            && validate_chain_two_ops(tree, validate_term, PLUS, MINUS));
}


static int
validate_term(node *tree)
{
    int pos = 1;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, term)
               && is_odd(nch)
               && validate_factor(CHILD(tree, 0)));

    for ( ; res && (pos < nch); pos += 2)
        res = (((TYPE(CHILD(tree, pos)) == STAR)
               || (TYPE(CHILD(tree, pos)) == SLASH)
               || (TYPE(CHILD(tree, pos)) == PERCENT))
               && validate_factor(CHILD(tree, pos + 1)));

    return (res);
}


/*  factor:
 *
 *  factor: ('+'|'-'|'~') factor | power
 */
static int
validate_factor(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, factor)
               && (((nch == 2)
                    && ((TYPE(CHILD(tree, 0)) == PLUS)
                        || (TYPE(CHILD(tree, 0)) == MINUS)
                        || (TYPE(CHILD(tree, 0)) == TILDE))
                    && validate_factor(CHILD(tree, 1)))
                   || ((nch == 1)
                       && validate_power(CHILD(tree, 0)))));
    return (res);
}


/*  power:
 *
 *  power: atom trailer* ('**' factor)*
 */
static int
validate_power(node *tree)
{
    int pos = 1;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, power) && (nch >= 1)
               && validate_atom(CHILD(tree, 0)));

    while (res && (pos < nch) && (TYPE(CHILD(tree, pos)) == trailer))
        res = validate_trailer(CHILD(tree, pos++));
    if (res && (pos < nch)) {
        if (!is_even(nch - pos)) {
            err_string("Illegal number of nodes for 'power'.");
            return (0);
        }
        for ( ; res && (pos < (nch - 1)); pos += 2)
            res = (validate_doublestar(CHILD(tree, pos))
                   && validate_factor(CHILD(tree, pos + 1)));
    }
    return (res);
}


static int
validate_atom(node *tree)
{
    int pos;
    int nch = NCH(tree);
    int res = validate_ntype(tree, atom) && (nch >= 1);

    if (res) {
        switch (TYPE(CHILD(tree, 0))) {
          case LPAR:
            res = ((nch <= 3)
                   && (validate_rparen(CHILD(tree, nch - 1))));

            if (res && (nch == 3))
                res = validate_testlist(CHILD(tree, 1));
            break;
          case LSQB:
            res = ((nch <= 3)
                   && validate_ntype(CHILD(tree, nch - 1), RSQB));

            if (res && (nch == 3))
                res = validate_testlist(CHILD(tree, 1));
            break;
          case LBRACE:
            res = ((nch <= 3)
                   && validate_ntype(CHILD(tree, nch - 1), RBRACE));

            if (res && (nch == 3))
                res = validate_dictmaker(CHILD(tree, 1));
            break;
          case BACKQUOTE:
            res = ((nch == 3)
                   && validate_testlist(CHILD(tree, 1))
                   && validate_ntype(CHILD(tree, 2), BACKQUOTE));
            break;
          case NAME:
          case NUMBER:
            res = (nch == 1);
            break;
          case STRING:
            for (pos = 1; res && (pos < nch); ++pos)
                res = validate_ntype(CHILD(tree, pos), STRING);
            break;
          default:
            res = 0;
            break;
        }
    }
    return (res);
}


/*  funcdef:
 *      'def' NAME parameters ':' suite
 *
 */
static int
validate_funcdef(node *tree)
{
    return (validate_ntype(tree, funcdef)
            && validate_numnodes(tree, 5, "funcdef")
            && validate_name(CHILD(tree, 0), "def")
            && validate_ntype(CHILD(tree, 1), NAME)
            && validate_colon(CHILD(tree, 3))
            && validate_parameters(CHILD(tree, 2))
            && validate_suite(CHILD(tree, 4)));
}


static int
validate_lambdef(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, lambdef)
               && ((nch == 3) || (nch == 4))
               && validate_name(CHILD(tree, 0), "lambda")
               && validate_colon(CHILD(tree, nch - 2))
               && validate_test(CHILD(tree, nch - 1)));

    if (res && (nch == 4))
        res = validate_varargslist(CHILD(tree, 1));
    else if (!res && !PyErr_Occurred())
        (void) validate_numnodes(tree, 3, "lambdef");

    return (res);
}


/*  arglist:
 *
 *  (argument ',')* (argument* [','] | '*' test [',' '**' test] | '**' test)
 */
static int
validate_arglist(node *tree)
{
    int nch = NCH(tree);
    int i, ok = 1;
    node *last;

    if (nch <= 0)
        /* raise the right error from having an invalid number of children */
        return validate_numnodes(tree, nch + 1, "arglist");

    last = CHILD(tree, nch - 1);
    if (TYPE(last) == test) {
        /* Extended call syntax introduced in Python 1.6 has been used;
         * validate and strip that off and continue;
         * adjust nch to perform the cut, and ensure resulting nch is even
         * (validation of the first part doesn't require that).
         */
        if (nch < 2) {
            validate_numnodes(tree, nch + 1, "arglist");
            return 0;
        }
        ok = validate_test(last);
        if (ok) {
            node *prev = CHILD(tree, nch - 2);
            /* next must be '*' or '**' */
            if (validate_doublestar(prev)) {
                nch -= 2;
                if (nch >= 3) {
                    /* may include:  '*' test ',' */
                    last = CHILD(tree, nch - 1);
                    prev = CHILD(tree, nch - 2);
                    if (TYPE(prev) == test) {
                        ok = validate_comma(last)
                             && validate_test(prev)
                             && validate_star(CHILD(tree, nch - 3));
                        if (ok)
                            nch -= 3;
                    }
                    /* otherwise, nothing special */
                }
            }
            else {
                /* must be only:  '*' test */
                PyErr_Clear();
                ok = validate_star(prev);
                nch -= 2;
            }
            if (ok && is_odd(nch)) {
                /* Illegal number of nodes before extended call syntax;
                 * validation of the "normal" arguments does not require
                 * a trailing comma, but requiring an even number of
                 * children will effect the same requirement.
                 */
                return validate_numnodes(tree, nch + 1, "arglist");
            }
        }
    }
    /* what remains must be:  (argument ",")* [argument [","]] */
    i = 0;
    while (ok && nch - i >= 2) {
        ok = validate_argument(CHILD(tree, i))
             && validate_comma(CHILD(tree, i + 1));
        i += 2;
    }
    if (ok && i < nch) {
        ok = validate_comma(CHILD(tree, i));
        ++i;
    }
    if (i != nch) {
        /* internal error! */
        ok = 0;
        err_string("arglist: internal error; nch != i");
    }
    return (ok);
}



/*  argument:
 *
 *  [test '='] test
 */
static int
validate_argument(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, argument)
               && ((nch == 1) || (nch == 3))
               && validate_test(CHILD(tree, 0)));

    if (res && (nch == 3))
        res = (validate_equal(CHILD(tree, 1))
               && validate_test(CHILD(tree, 2)));

    return (res);
}



/*  trailer:
 *
 *  '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
 */
static int
validate_trailer(node *tree)
{
    int nch = NCH(tree);
    int res = validate_ntype(tree, trailer) && ((nch == 2) || (nch == 3));

    if (res) {
        switch (TYPE(CHILD(tree, 0))) {
          case LPAR:
            res = validate_rparen(CHILD(tree, nch - 1));
            if (res && (nch == 3))
                res = validate_arglist(CHILD(tree, 1));
            break;
          case LSQB:
            res = (validate_numnodes(tree, 3, "trailer")
                   && validate_subscriptlist(CHILD(tree, 1))
                   && validate_ntype(CHILD(tree, 2), RSQB));
            break;
          case DOT:
            res = (validate_numnodes(tree, 2, "trailer")
                   && validate_ntype(CHILD(tree, 1), NAME));
            break;
          default:
            res = 0;
            break;
        }
    }
    else {
        (void) validate_numnodes(tree, 2, "trailer");
    }
    return (res);
}


/*  subscriptlist:
 *
 *  subscript (',' subscript)* [',']
 */
static int
validate_subscriptlist(node *tree)
{
    return (validate_repeating_list(tree, subscriptlist,
                                    validate_subscript, "subscriptlist"));
}


/*  subscript:
 *
 *  '.' '.' '.' | test | [test] ':' [test] [sliceop]
 */
static int
validate_subscript(node *tree)
{
    int offset = 0;
    int nch = NCH(tree);
    int res = validate_ntype(tree, subscript) && (nch >= 1) && (nch <= 4);

    if (!res) {
        if (!PyErr_Occurred())
            err_string("invalid number of arguments for subscript node");
        return (0);
    }
    if (TYPE(CHILD(tree, 0)) == DOT)
        /* take care of ('.' '.' '.') possibility */
        return (validate_numnodes(tree, 3, "subscript")
                && validate_dot(CHILD(tree, 0))
                && validate_dot(CHILD(tree, 1))
                && validate_dot(CHILD(tree, 2)));
    if (nch == 1) {
        if (TYPE(CHILD(tree, 0)) == test)
            res = validate_test(CHILD(tree, 0));
        else
            res = validate_colon(CHILD(tree, 0));
        return (res);
    }
    /*  Must be [test] ':' [test] [sliceop],
     *  but at least one of the optional components will
     *  be present, but we don't know which yet.
     */
    if ((TYPE(CHILD(tree, 0)) != COLON) || (nch == 4)) {
        res = validate_test(CHILD(tree, 0));
        offset = 1;
    }
    if (res)
        res = validate_colon(CHILD(tree, offset));
    if (res) {
        int rem = nch - ++offset;
        if (rem) {
            if (TYPE(CHILD(tree, offset)) == test) {
                res = validate_test(CHILD(tree, offset));
                ++offset;
                --rem;
            }
            if (res && rem)
                res = validate_sliceop(CHILD(tree, offset));
        }
    }
    return (res);
}


static int
validate_sliceop(node *tree)
{
    int nch = NCH(tree);
    int res = ((nch == 1) || validate_numnodes(tree, 2, "sliceop"))
              && validate_ntype(tree, sliceop);
    if (!res && !PyErr_Occurred()) {
        res = validate_numnodes(tree, 1, "sliceop");
    }
    if (res)
        res = validate_colon(CHILD(tree, 0));
    if (res && (nch == 2))
        res = validate_test(CHILD(tree, 1));

    return (res);
}


static int
validate_exprlist(node *tree)
{
    return (validate_repeating_list(tree, exprlist,
                                    validate_expr, "exprlist"));
}


static int
validate_dictmaker(node *tree)
{
    int nch = NCH(tree);
    int res = (validate_ntype(tree, dictmaker)
               && (nch >= 3)
               && validate_test(CHILD(tree, 0))
               && validate_colon(CHILD(tree, 1))
               && validate_test(CHILD(tree, 2)));

    if (res && ((nch % 4) == 0))
        res = validate_comma(CHILD(tree, --nch));
    else if (res)
        res = ((nch % 4) == 3);

    if (res && (nch > 3)) {
        int pos = 3;
        /*  ( ',' test ':' test )*  */
        while (res && (pos < nch)) {
            res = (validate_comma(CHILD(tree, pos))
                   && validate_test(CHILD(tree, pos + 1))
                   && validate_colon(CHILD(tree, pos + 2))
                   && validate_test(CHILD(tree, pos + 3)));
            pos += 4;
        }
    }
    return (res);
}


static int
validate_eval_input(node *tree)
{
    int pos;
    int nch = NCH(tree);
    int res = (validate_ntype(tree, eval_input)
               && (nch >= 2)
               && validate_testlist(CHILD(tree, 0))
               && validate_ntype(CHILD(tree, nch - 1), ENDMARKER));

    for (pos = 1; res && (pos < (nch - 1)); ++pos)
        res = validate_ntype(CHILD(tree, pos), NEWLINE);

    return (res);
}


static int
validate_node(node *tree)
{
    int   nch  = 0;                     /* num. children on current node  */
    int   res  = 1;                     /* result value                   */
    node* next = 0;                     /* node to process after this one */

    while (res & (tree != 0)) {
        nch  = NCH(tree);
        next = 0;
        switch (TYPE(tree)) {
            /*
             *  Definition nodes.
             */
          case funcdef:
            res = validate_funcdef(tree);
            break;
          case classdef:
            res = validate_class(tree);
            break;
            /*
             *  "Trivial" parse tree nodes.
             *  (Why did I call these trivial?)
             */
          case stmt:
            res = validate_stmt(tree);
            break;
          case small_stmt:
            /*
             *  expr_stmt | print_stmt  | del_stmt | pass_stmt | flow_stmt
             *  | import_stmt | global_stmt | exec_stmt | assert_stmt
             */
            res = validate_small_stmt(tree);
            break;
          case flow_stmt:
            res  = (validate_numnodes(tree, 1, "flow_stmt")
                    && ((TYPE(CHILD(tree, 0)) == break_stmt)
                        || (TYPE(CHILD(tree, 0)) == continue_stmt)
                        || (TYPE(CHILD(tree, 0)) == return_stmt)
                        || (TYPE(CHILD(tree, 0)) == raise_stmt)));
            if (res)
                next = CHILD(tree, 0);
            else if (nch == 1)
                err_string("Illegal flow_stmt type.");
            break;
            /*
             *  Compound statements.
             */
          case simple_stmt:
            res = validate_simple_stmt(tree);
            break;
          case compound_stmt:
            res = validate_compound_stmt(tree);
            break;
            /*
             *  Fundemental statements.
             */
          case expr_stmt:
            res = validate_expr_stmt(tree);
            break;
          case print_stmt:
            res = validate_print_stmt(tree);
            break;
          case del_stmt:
            res = validate_del_stmt(tree);
            break;
          case pass_stmt:
            res = (validate_numnodes(tree, 1, "pass")
                   && validate_name(CHILD(tree, 0), "pass"));
            break;
          case break_stmt:
            res = (validate_numnodes(tree, 1, "break")
                   && validate_name(CHILD(tree, 0), "break"));
            break;
          case continue_stmt:
            res = (validate_numnodes(tree, 1, "continue")
                   && validate_name(CHILD(tree, 0), "continue"));
            break;
          case return_stmt:
            res = validate_return_stmt(tree);
            break;
          case raise_stmt:
            res = validate_raise_stmt(tree);
            break;
          case import_stmt:
            res = validate_import_stmt(tree);
            break;
          case global_stmt:
            res = validate_global_stmt(tree);
            break;
          case exec_stmt:
            res = validate_exec_stmt(tree);
            break;
          case assert_stmt:
            res = validate_assert_stmt(tree);
            break;
          case if_stmt:
            res = validate_if(tree);
            break;
          case while_stmt:
            res = validate_while(tree);
            break;
          case for_stmt:
            res = validate_for(tree);
            break;
          case try_stmt:
            res = validate_try(tree);
            break;
          case suite:
            res = validate_suite(tree);
            break;
            /*
             *  Expression nodes.
             */
          case testlist:
            res = validate_testlist(tree);
            break;
          case test:
            res = validate_test(tree);
            break;
          case and_test:
            res = validate_and_test(tree);
            break;
          case not_test:
            res = validate_not_test(tree);
            break;
          case comparison:
            res = validate_comparison(tree);
            break;
          case exprlist:
            res = validate_exprlist(tree);
            break;
          case comp_op:
            res = validate_comp_op(tree);
            break;
          case expr:
            res = validate_expr(tree);
            break;
          case xor_expr:
            res = validate_xor_expr(tree);
            break;
          case and_expr:
            res = validate_and_expr(tree);
            break;
          case shift_expr:
            res = validate_shift_expr(tree);
            break;
          case arith_expr:
            res = validate_arith_expr(tree);
            break;
          case term:
            res = validate_term(tree);
            break;
          case factor:
            res = validate_factor(tree);
            break;
          case power:
            res = validate_power(tree);
            break;
          case atom:
            res = validate_atom(tree);
            break;

          default:
            /* Hopefully never reached! */
            err_string("Unrecogniged node type.");
            res = 0;
            break;
        }
        tree = next;
    }
    return (res);
}


static int
validate_expr_tree(node *tree)
{
    int res = validate_eval_input(tree);

    if (!res && !PyErr_Occurred())
        err_string("Could not validate expression tuple.");

    return (res);
}


/*  file_input:
 *      (NEWLINE | stmt)* ENDMARKER
 */
static int
validate_file_input(node *tree)
{
    int j   = 0;
    int nch = NCH(tree) - 1;
    int res = ((nch >= 0)
               && validate_ntype(CHILD(tree, nch), ENDMARKER));

    for ( ; res && (j < nch); ++j) {
        if (TYPE(CHILD(tree, j)) == stmt)
            res = validate_stmt(CHILD(tree, j));
        else
            res = validate_newline(CHILD(tree, j));
    }
    /*  This stays in to prevent any internal failues from getting to the
     *  user.  Hopefully, this won't be needed.  If a user reports getting
     *  this, we have some debugging to do.
     */
    if (!res && !PyErr_Occurred())
        err_string("VALIDATION FAILURE: report this to the maintainer!.");

    return (res);
}


static PyObject*
pickle_constructor = NULL;


static PyObject*
parser__pickler(PyObject *self, PyObject *args)
{
    NOTE(ARGUNUSED(self))
    PyObject *result = NULL;
    PyObject *ast = NULL;
    PyObject *empty_dict = NULL;

    if (PyArg_ParseTuple(args, "O!:_pickler", &PyAST_Type, &ast)) {
        PyObject *newargs;
        PyObject *tuple;

        if ((empty_dict = PyDict_New()) == NULL)
            goto finally;
        if ((newargs = Py_BuildValue("Oi", ast, 1)) == NULL)
            goto finally;
        tuple = parser_ast2tuple((PyAST_Object*)NULL, newargs, empty_dict);
        if (tuple != NULL) {
            result = Py_BuildValue("O(O)", pickle_constructor, tuple);
            Py_DECREF(tuple);
        }
        Py_DECREF(empty_dict);
        Py_DECREF(newargs);
    }
  finally:
    Py_XDECREF(empty_dict);

    return (result);
}


/*  Functions exported by this module.  Most of this should probably
 *  be converted into an AST object with methods, but that is better
 *  done directly in Python, allowing subclasses to be created directly.
 *  We'd really have to write a wrapper around it all anyway to allow
 *  inheritance.
 */
static PyMethodDef parser_functions[] =  {
    {"ast2tuple",       (PyCFunction)parser_ast2tuple,  PUBLIC_METHOD_TYPE,
        "Creates a tuple-tree representation of an AST."},
    {"ast2list",        (PyCFunction)parser_ast2list,   PUBLIC_METHOD_TYPE,
        "Creates a list-tree representation of an AST."},
    {"compileast",      (PyCFunction)parser_compileast, PUBLIC_METHOD_TYPE,
        "Compiles an AST object into a code object."},
    {"expr",            (PyCFunction)parser_expr,       PUBLIC_METHOD_TYPE,
        "Creates an AST object from an expression."},
    {"isexpr",          (PyCFunction)parser_isexpr,     PUBLIC_METHOD_TYPE,
        "Determines if an AST object was created from an expression."},
    {"issuite",         (PyCFunction)parser_issuite,    PUBLIC_METHOD_TYPE,
        "Determines if an AST object was created from a suite."},
    {"suite",           (PyCFunction)parser_suite,      PUBLIC_METHOD_TYPE,
        "Creates an AST object from a suite."},
    {"sequence2ast",    (PyCFunction)parser_tuple2ast,  PUBLIC_METHOD_TYPE,
        "Creates an AST object from a tree representation."},
    {"tuple2ast",       (PyCFunction)parser_tuple2ast,  PUBLIC_METHOD_TYPE,
        "Creates an AST object from a tree representation."},

    /* private stuff: support pickle module */
    {"_pickler",        (PyCFunction)parser__pickler,   METH_VARARGS,
        "Returns the pickle magic to allow ast objects to be pickled."},

    {NULL, NULL, 0, NULL}
    };


DL_EXPORT(void)
initparser()
 {
    PyObject* module;
    PyObject* dict;
        
    PyAST_Type.ob_type = &PyType_Type;
    module = Py_InitModule("parser", parser_functions);
    dict = PyModule_GetDict(module);

    if (parser_error == 0)
        parser_error = PyErr_NewException("parser.ParserError", NULL, NULL);
    else
        puts("parser module initialized more than once!");

    if ((parser_error == 0)
        || (PyDict_SetItemString(dict, "ParserError", parser_error) != 0)) {
        /*
         *  This is serious.
         */
        Py_FatalError("can't define parser.ParserError");
    }
    /*
     *  Nice to have, but don't cry if we fail.
     */
    Py_INCREF(&PyAST_Type);
    PyDict_SetItemString(dict, "ASTType", (PyObject*)&PyAST_Type);

    PyDict_SetItemString(dict, "__copyright__",
                         PyString_FromString(parser_copyright_string));
    PyDict_SetItemString(dict, "__doc__",
                         PyString_FromString(parser_doc_string));
    PyDict_SetItemString(dict, "__version__",
                         PyString_FromString(parser_version_string));

    /* register to support pickling */
    module = PyImport_ImportModule("copy_reg");
    if (module != NULL) {
        PyObject *func, *pickler;

        func = PyObject_GetAttrString(module, "pickle");
        pickle_constructor = PyDict_GetItemString(dict, "sequence2ast");
        pickler = PyDict_GetItemString(dict, "_pickler");
        Py_XINCREF(pickle_constructor);
        if ((func != NULL) && (pickle_constructor != NULL)
            && (pickler != NULL)) {
            PyObject *res;

            res = PyObject_CallFunction(
                    func, "OOO", &PyAST_Type, pickler, pickle_constructor);
            Py_XDECREF(res);
        }
        Py_XDECREF(func);
        Py_DECREF(module);
    }
}
