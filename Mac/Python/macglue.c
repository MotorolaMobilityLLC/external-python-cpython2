/***********************************************************
Copyright 1991-1995 by Stichting Mathematisch Centrum, Amsterdam,
The Netherlands.

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its 
documentation for any purpose and without fee is hereby granted, 
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in 
supporting documentation, and that the names of Stichting Mathematisch
Centrum or CWI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior permission.

STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

******************************************************************/

#include "Python.h"
#include "macglue.h"

#include <OSUtils.h> /* for Set(Current)A5 */
#include <Resources.h>
#include <Memory.h>
#include <Events.h>
#include <Windows.h>
#include <Desk.h>

/* XXX We should include Errors.h here, but it has a name conflict
** with the python errors.h. */
#define fnfErr -43

/* Convert C to Pascal string. Returns pointer to static buffer. */
unsigned char *
Pstring(char *str)
{
	static Str255 buf;
	int len;

	len = strlen(str);
	if (len > 255)
		len = 255;
	buf[0] = (unsigned char)len;
	strncpy((char *)buf+1, str, len);
	return buf;
}

/* Replace strerror with something that might work */
char *macstrerror(int err)
{
	static char buf[256];
	Handle h;
	char *str;
	
	h = GetResource('Estr', err);
	if ( h ) {
		HLock(h);
		str = (char *)*h;
		memcpy(buf, str+1, (unsigned char)str[0]);
		HUnlock(h);
		ReleaseResource(h);
	} else {
		sprintf(buf, "Mac OS error code %d", err);
	}
	return buf;
}

/* Exception object shared by all Mac specific modules for Mac OS errors */
PyObject *PyMac_OSErrException;

/* Initialize and return PyMac_OSErrException */
PyObject *
PyMac_GetOSErrException()
{
	if (PyMac_OSErrException == NULL)
		PyMac_OSErrException = PyString_FromString("Mac OS Error");
	return PyMac_OSErrException;
}

/* Set a MAC-specific error from errno, and return NULL; return None if no error */
PyObject * 
PyErr_Mac(PyObject *eobj, int err)
{
	char *msg;
	PyObject *v;
	
	if (err == 0 && !PyErr_Occurred()) {
		Py_INCREF(Py_None);
		return Py_None;
	}
	if (err == -1 && PyErr_Occurred())
		return NULL;
	msg = macstrerror(err);
	v = Py_BuildValue("(is)", err, msg);
	PyErr_SetObject(eobj, v);
	Py_DECREF(v);
	return NULL;
}

/* Call PyErr_Mac with PyMac_OSErrException */
PyObject *
PyMac_Error(OSErr err)
{
	return PyErr_Mac(PyMac_GetOSErrException(), err);
}

/*
** Idle routine for busy-wait loops.
** This is rather tricky: if we see an event we check whether it is
** for somebody else (i.e. a click outside our windows) and, if so,
** we pass the event on (so the user can switch processes). However,
** by doing this we loose events meant for our windows. Too bad, I guess...
*/
int
PyMac_Idle()
{
	EventRecord ev;
	WindowPtr wp;

	SystemTask();
	if ( intrpeek() )
		return 0;
	if ( GetNextEvent(0xffff, &ev) ) {
		if ( ev.what == mouseDown ) {
			if ( FindWindow(ev.where, &wp) == inSysWindow )
				SystemClick(&ev, wp);
		}
	}
	return 1;
}


/* Convert a 4-char string object argument to an OSType value */
int
PyMac_GetOSType(PyObject *v, OSType *pr)
{
	if (!PyString_Check(v) || PyString_Size(v) != 4) {
		PyErr_SetString(PyExc_TypeError,
			"OSType arg must be string of 4 chars");
		return 0;
	}
	memcpy((char *)pr, PyString_AsString(v), 4);
	return 1;
}

/* Convert an OSType value to a 4-char string object */
PyObject *
PyMac_BuildOSType(OSType t)
{
	return PyString_FromStringAndSize((char *)&t, 4);
}


/* Convert a Python string object to a Str255 */
int
PyMac_GetStr255(PyObject *v, Str255 pbuf)
{
	int len;
	if (!PyString_Check(v) || (len = PyString_Size(v)) > 255) {
		PyErr_SetString(PyExc_TypeError,
			"Str255 arg must be string of at most 255 chars");
		return 0;
	}
	pbuf[0] = len;
	memcpy((char *)(pbuf+1), PyString_AsString(v), len);
	return 1;
}

/* Convert a Str255 to a Python string object */
PyObject *
PyMac_BuildStr255(Str255 s)
{
	return PyString_FromStringAndSize((char *)&s[1], (int)s[0]);
}


/*
** Convert a Python object to an FSSpec.
** The object may either be a full pathname or a triple
** (vrefnum, dirid, path).
** NOTE: This routine will fail on pre-sys7 machines. 
** The caller is responsible for not calling this routine
** in those cases (which is fine, since everyone calling
** this is probably sys7 dependent anyway).
*/
int
PyMac_GetFSSpec(PyObject *v, FSSpec *fs)
{
	Str255 path;
	short refnum;
	long parid;
	OSErr err;

	if ( PyString_Check(v) ) {
		/* It's a pathname */
		if( !PyArg_Parse(v, "O&", PyMac_GetStr255, &path) )
			return 0;
		refnum = 0; /* XXXX Should get CurWD here... */
		parid = 0;
	} else {
		if( !PyArg_Parse(v, "(hlO&); FSSpec should be fullpath or (vrefnum,dirid,path)",
							&refnum, &parid, PyMac_GetStr255, &path)) {
			return 0;
		}
	}
	err = FSMakeFSSpec(refnum, parid, path, fs);
	if ( err && err != fnfErr ) {
		PyErr_Mac(PyExc_ValueError, err);
		return 0;
	}
	return 1;
}

/* Convert an FSSpec to a Python object -- a triple (vrefnum, dirid, path) */
PyObject *
PyMac_BuildFSSpec(FSSpec *fs)
{
	return Py_BuildValue("(iis#)", fs->vRefNum, fs->parID, &fs->name[1], fs->name[0]);
}


/* Convert a Python object to a Rect.
   The object must be a (top, left, bottom, right) tuple.
   (Unfortunately this is different from STDWIN's convention). */
int
PyMac_GetRect(PyObject *v, Rect *r)
{
	return PyArg_Parse(v, "(hhhh)", &r->top, &r->left, &r->bottom, &r->right);
}

/* Convert a Rect to a Python object */
PyObject *
PyMac_BuildRect(Rect *r)
{
	return Py_BuildValue("(hhhh)", r->top, r->left, r->bottom, r->right);
}


/* Convert a Python object to a Point.
   The object must be a (v, h) tuple.
   (Unfortunately this is different from STDWIN's convention). */
int
PyMac_GetPoint(PyObject *v, Point *p)
{
	return PyArg_Parse(v, "(hh)", &p->v, &p->h);
}

/* Convert a Point to a Python object */
PyObject *
PyMac_BuildPoint(Point p)
{
	return Py_BuildValue("(hh)", p.v, p.h);
}


/* Convert a Python object to an EventRecord.
   The object must be a (what, message, when, (v, h), modifiers) tuple. */
int
PyMac_GetEventRecord(PyObject *v, EventRecord *e)
{
	return PyArg_Parse(v, "(hll(hh)h)",
	                   &e->what,
	                   &e->message,
	                   &e->when,
	                   &e->where.v,                   
	                   &e->where.h,
	                   &e->modifiers);
}

/* Convert a Rect to an EventRecord object */
PyObject *
PyMac_BuildEventRecord(EventRecord *e)
{
	return Py_BuildValue("(hll(hh)h)",
	                     e->what,
	                     e->message,
	                     e->when,
	                     e->where.v,
	                     e->where.h,
	                     e->modifiers);
}
