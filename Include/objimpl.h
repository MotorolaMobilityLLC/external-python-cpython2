#ifndef Py_OBJIMPL_H
#define Py_OBJIMPL_H
#ifdef __cplusplus
extern "C" {
#endif

/***********************************************************
Copyright 1991-1995 by Stichting Mathematisch Centrum, Amsterdam,
The Netherlands.

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the names of Stichting Mathematisch
Centrum or CWI or Corporation for National Research Initiatives or
CNRI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior
permission.

While CWI is the initial source for this software, a modified version
is made available by the Corporation for National Research Initiatives
(CNRI) at the Internet address ftp://ftp.python.org.

STICHTING MATHEMATISCH CENTRUM AND CNRI DISCLAIM ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH
CENTRUM OR CNRI BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

******************************************************************/

#include "mymalloc.h"

/*
Functions and macros for modules that implement new object types.
You must first include "object.h".

 - PyObject_New(type, typeobj) allocates memory for a new object of
   the given type; here 'type' must be the C structure type used to
   represent the object and 'typeobj' the address of the corresponding
   type object.  Reference count and type pointer are filled in; the
   rest of the bytes of the object are *undefined*!  The resulting
   expression type is 'type *'.  The size of the object is actually
   determined by the tp_basicsize field of the type object.

 - PyObject_NewVar(type, typeobj, n) is similar but allocates a
   variable-size object with n extra items.  The size is computed as
   tp_basicsize plus n * tp_itemsize.  This fills in the ob_size field
   as well.

 - PyObject_Del(op) releases the memory allocated for an object.

 - PyObject_Init(op, typeobj) and PyObject_InitVar(op, typeobj, n) are
   similar to PyObject_{New, NewVar} except that they don't allocate
   the memory needed for an object. Instead of the 'type' parameter,
   they accept the pointer of a new object (allocated by an arbitrary
   allocator) and initialize its object header fields.

Note that objects created with PyObject_{New, NewVar} are allocated
within the Python heap by an object allocator, the latter being
implemented (by default) on top of the Python raw memory
allocator. This ensures that Python keeps control on the user's
objects regarding their memory management; for instance, they may be
subject to automatic garbage collection.

In case a specific form of memory management is needed, implying that
the objects would not reside in the Python heap (for example standard
malloc heap(s) are mandatory, use of shared memory, C++ local storage
or operator new), you must first allocate the object with your custom
allocator, then pass its pointer to PyObject_{Init, InitVar} for
filling in its Python-specific fields: reference count, type pointer,
possibly others. You should be aware that Python has very limited
control over these objects because they don't cooperate with the
Python memory manager. Such objects may not be eligible for automatic
garbage collection and you have to make sure that they are released
accordingly whenever their destructor gets called (cf. the specific
form of memory management you're using).

Unless you have specific memory management requirements, it is
recommended to use PyObject_{New, NewVar, Del}. */

/* 
 * Core object memory allocator
 * ============================
 */

/* The purpose of the object allocator is to make make the distinction
   between "object memory" and the rest within the Python heap.
   
   Object memory is the one allocated by PyObject_{New, NewVar}, i.e.
   the one that holds the object's representation defined by its C
   type structure, *excluding* any object-specific memory buffers that
   might be referenced by the structure (for type structures that have
   pointer fields).  By default, the object memory allocator is
   implemented on top of the raw memory allocator.

   The PyCore_* macros can be defined to make the interpreter use a
   custom object memory allocator. They are reserved for internal
   memory management purposes exclusively. Both the core and extension
   modules should use the PyObject_* API. */

#ifndef PyCore_OBJECT_MALLOC_FUNC
#undef PyCore_OBJECT_REALLOC_FUNC
#undef PyCore_OBJECT_FREE_FUNC
#define PyCore_OBJECT_MALLOC_FUNC    PyCore_MALLOC_FUNC
#define PyCore_OBJECT_REALLOC_FUNC   PyCore_REALLOC_FUNC
#define PyCore_OBJECT_FREE_FUNC      PyCore_FREE_FUNC
#endif

#ifndef PyCore_OBJECT_MALLOC_PROTO
#undef PyCore_OBJECT_REALLOC_PROTO
#undef PyCore_OBJECT_FREE_PROTO
#define PyCore_OBJECT_MALLOC_PROTO   PyCore_MALLOC_PROTO
#define PyCore_OBJECT_REALLOC_PROTO  PyCore_REALLOC_PROTO
#define PyCore_OBJECT_FREE_PROTO     PyCore_FREE_PROTO
#endif

#ifdef NEED_TO_DECLARE_OBJECT_MALLOC_AND_FRIEND
extern ANY *PyCore_OBJECT_MALLOC_FUNC PyCore_OBJECT_MALLOC_PROTO;
extern ANY *PyCore_OBJECT_REALLOC_FUNC PyCore_OBJECT_REALLOC_PROTO;
extern void PyCore_OBJECT_FREE_FUNC PyCore_OBJECT_FREE_PROTO;
#endif

#ifndef PyCore_OBJECT_MALLOC
#undef PyCore_OBJECT_REALLOC
#undef PyCore_OBJECT_FREE
#define PyCore_OBJECT_MALLOC(n)      PyCore_OBJECT_MALLOC_FUNC(n)
#define PyCore_OBJECT_REALLOC(p, n)  PyCore_OBJECT_REALLOC_FUNC((p), (n))
#define PyCore_OBJECT_FREE(p)        PyCore_OBJECT_FREE_FUNC(p)
#endif

/*
 * Raw object memory interface
 * ===========================
 */

/* The use of this API should be avoided, unless a builtin object
   constructor inlines PyObject_{New, NewVar}, either because the
   latter functions cannot allocate the exact amount of needed memory,
   either for speed. This situation is exceptional, but occurs for
   some object constructors (PyBuffer_New, PyList_New...).  Inlining
   PyObject_{New, NewVar} for objects that are supposed to belong to
   the Python heap is discouraged. If you really have to, make sure
   the object is initialized with PyObject_{Init, InitVar}. Do *not*
   inline PyObject_{Init, InitVar} for user-extension types or you
   might seriously interfere with Python's memory management. */

/* Functions */

/* Wrappers around PyCore_OBJECT_MALLOC and friends; useful if you
   need to be sure that you are using the same object memory allocator
   as Python. These wrappers *do not* make sure that allocating 0
   bytes returns a non-NULL pointer. Returned pointers must be checked
   for NULL explicitly; no action is performed on failure. */
extern DL_IMPORT(ANY *) PyObject_Malloc Py_PROTO((size_t));
extern DL_IMPORT(ANY *) PyObject_Realloc Py_PROTO((ANY *, size_t));
extern DL_IMPORT(void) PyObject_Free Py_PROTO((ANY *));

/* Macros */
#define PyObject_MALLOC(n)           PyCore_OBJECT_MALLOC(n)
#define PyObject_REALLOC(op, n)      PyCore_OBJECT_REALLOC((ANY *)(op), (n))
#define PyObject_FREE(op)            PyCore_OBJECT_FREE((ANY *)(op))

/*
 * Generic object allocator interface
 * ==================================
 */

/* Functions */
extern DL_IMPORT(PyObject *) PyObject_Init Py_PROTO((PyObject *, PyTypeObject *));
extern DL_IMPORT(PyVarObject *) PyObject_InitVar Py_PROTO((PyVarObject *, PyTypeObject *, int));
extern DL_IMPORT(PyObject *) _PyObject_New Py_PROTO((PyTypeObject *));
extern DL_IMPORT(PyVarObject *) _PyObject_NewVar Py_PROTO((PyTypeObject *, int));
extern DL_IMPORT(void) _PyObject_Del Py_PROTO((PyObject *));

#define PyObject_New(type, typeobj) \
		( (type *) _PyObject_New(typeobj) )
#define PyObject_NewVar(type, typeobj, n) \
		( (type *) _PyObject_NewVar((typeobj), (n)) )
#define PyObject_Del(op) _PyObject_Del((PyObject *)(op))

/* Macros trading binary compatibility for speed. See also mymalloc.h.
   Note that these macros expect non-NULL object pointers.*/
#define PyObject_INIT(op, typeobj) \
	( (op)->ob_type = (typeobj), _Py_NewReference((PyObject *)(op)), (op) )
#define PyObject_INIT_VAR(op, typeobj, size) \
	( (op)->ob_size = (size), PyObject_INIT((op), (typeobj)) )

#define _PyObject_SIZE(typeobj) ( (typeobj)->tp_basicsize )
#define _PyObject_VAR_SIZE(typeobj, n) \
	( (typeobj)->tp_basicsize + (n) * (typeobj)->tp_itemsize )

#define PyObject_NEW(type, typeobj) \
( (type *) PyObject_Init( \
	(PyObject *) PyObject_MALLOC( _PyObject_SIZE(typeobj) ), (typeobj)) )
#define PyObject_NEW_VAR(type, typeobj, n) \
( (type *) PyObject_InitVar( \
	(PyVarObject *) PyObject_MALLOC( _PyObject_VAR_SIZE((typeobj),(n)) ),\
	(typeobj), (n)) )
#define PyObject_DEL(op) PyObject_FREE(op)

/* This example code implements an object constructor with a custom
   allocator, where PyObject_New is inlined, and shows the important
   distinction between two steps (at least):
       1) the actual allocation of the object storage;
       2) the initialization of the Python specific fields
          in this storage with PyObject_{Init, InitVar}.

   PyObject *
   YourObject_New(...)
   {
       PyObject *op;

       op = (PyObject *) Your_Allocator(_PyObject_SIZE(YourTypeStruct));
       if (op == NULL)
           return PyErr_NoMemory();

       op = PyObject_Init(op, &YourTypeStruct);
       if (op == NULL)
           return NULL;

       op->ob_field = value;
       ...
       return op;
   }

   Note that in C++, the use of the new operator usually implies that
   the 1st step is performed automatically for you, so in a C++ class
   constructor you would start directly with PyObject_Init/InitVar. */

#ifdef __cplusplus
}
#endif
#endif /* !Py_OBJIMPL_H */
