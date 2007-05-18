/* Cell object implementation */

#include "Python.h"

PyObject *
PyCell_New(PyObject *obj)
{
	PyCellObject *op;

	op = (PyCellObject *)PyObject_GC_New(PyCellObject, &PyCell_Type);
	if (op == NULL)
		return NULL;
	op->ob_ref = obj;
	Py_XINCREF(obj);

	_PyObject_GC_TRACK(op);
	return (PyObject *)op;
}

PyObject *
PyCell_Get(PyObject *op)
{
	if (!PyCell_Check(op)) {
		PyErr_BadInternalCall();
		return NULL;
	}
	Py_XINCREF(((PyCellObject*)op)->ob_ref);
	return PyCell_GET(op);
}

int
PyCell_Set(PyObject *op, PyObject *obj)
{
	if (!PyCell_Check(op)) {
		PyErr_BadInternalCall();
		return -1;
	}
	Py_XDECREF(((PyCellObject*)op)->ob_ref);
	Py_XINCREF(obj);
	PyCell_SET(op, obj);
	return 0;
}

static void
cell_dealloc(PyCellObject *op)
{
	_PyObject_GC_UNTRACK(op);
	Py_XDECREF(op->ob_ref);
	PyObject_GC_Del(op);
}

static PyObject *
cell_repr(PyCellObject *op)
{
	if (op->ob_ref == NULL)
		return PyUnicode_FromFormat("<cell at %p: empty>", op);

	return PyUnicode_FromFormat("<cell at %p: %.80s object at %p>",
				   op, op->ob_ref->ob_type->tp_name,
				   op->ob_ref);
}

static int
cell_traverse(PyCellObject *op, visitproc visit, void *arg)
{
	Py_VISIT(op->ob_ref);
	return 0;
}

static int
cell_clear(PyCellObject *op)
{
	Py_CLEAR(op->ob_ref);
	return 0;
}

static PyObject *
cell_get_contents(PyCellObject *op, void *closure)
{
	Py_XINCREF(op->ob_ref);
	return op->ob_ref;
}

static PyGetSetDef cell_getsetlist[] = {
	{"cell_contents", (getter)cell_get_contents, NULL},
	{NULL} /* sentinel */
};

PyTypeObject PyCell_Type = {
	PyObject_HEAD_INIT(&PyType_Type)
	0,
	"cell",
	sizeof(PyCellObject),
	0,
	(destructor)cell_dealloc,               /* tp_dealloc */
	0,                                      /* tp_print */
	0,	                                /* tp_getattr */
	0,					/* tp_setattr */
	0,					/* tp_compare */
	(reprfunc)cell_repr,			/* tp_repr */
	0,					/* tp_as_number */
	0,			                /* tp_as_sequence */
	0,					/* tp_as_mapping */
	0,					/* tp_hash */
	0,					/* tp_call */
	0,					/* tp_str */
	PyObject_GenericGetAttr,		/* tp_getattro */
	0,					/* tp_setattro */
	0,					/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,/* tp_flags */
 	0,					/* tp_doc */
 	(traverseproc)cell_traverse,		/* tp_traverse */
 	(inquiry)cell_clear,			/* tp_clear */
	0,					/* tp_richcompare */
	0,					/* tp_weaklistoffset */
	0, 					/* tp_iter */
	0,					/* tp_iternext */
	0,					/* tp_methods */
	0,					/* tp_members */
	cell_getsetlist,			/* tp_getset */
};
