# IBCarbonsupport.py

from macsupport import *

from CarbonEventsscan import RefObjectTypes

# where should this go? macsupport.py?
CFStringRef = OpaqueByValueType('CFStringRef')

for typ in RefObjectTypes:
	execstr = "%(name)s = OpaqueByValueType('%(name)s')" % {"name": typ}
	exec execstr

# these types will have no methods and will merely be opaque blobs
# should write getattr and setattr for them?

StructObjectTypes = ["EventTypeSpec",
					"HIPoint",
					"HICommand",
					"EventHotKeyID",
					]

for typ in StructObjectTypes:
	execstr = "%(name)s = OpaqueType('%(name)s')" % {"name": typ}
	exec execstr

EventTypeSpec_ptr = OpaqueType("EventTypeSpec *", "EventTypeSpec")

# is this the right type for the void * in GetEventParameter
#void_ptr = FixedInputBufferType(1024)
void_ptr = stringptr
# here are some types that are really other types

EventTime = double
EventTimeout = EventTime
EventTimerInterval = EventTime
EventAttributes = UInt32
EventParamName = OSType
EventParamType = OSType
EventPriority = SInt16
EventMask = UInt16

EventComparatorUPP = FakeType("(EventComparatorUPP)0")
EventLoopTimerUPP = FakeType("(EventLoopTimerUPP)0")
EventHandlerUPP = FakeType("(EventHandlerUPP)0")
EventHandlerUPP = FakeType("(EventHandlerUPP)0")
EventComparatorProcPtr = FakeType("(EventComparatorProcPtr)0")
EventLoopTimerProcPtr = FakeType("(EventLoopTimerProcPtr)0")
EventHandlerProcPtr = FakeType("(EventHandlerProcPtr)0")

CarbonEventsFunction = OSErrFunctionGenerator
CarbonEventsMethod = OSErrMethodGenerator

includestuff = """
#include <Carbon/Carbon.h>
#include "macglue.h"

#define USE_MAC_MP_MULTITHREADING 1

#if USE_MAC_MP_MULTITHREADING
static PyThreadState *_save;
static MPCriticalRegionID reentrantLock;
#endif /* USE_MAC_MP_MULTITHREADING */

extern int CFStringRef_New(CFStringRef *);

extern int CFStringRef_Convert(PyObject *, CFStringRef *);
extern int CFBundleRef_Convert(PyObject *, CFBundleRef *);

int EventTargetRef_Convert(PyObject *, EventTargetRef *);
PyObject *EventHandlerCallRef_New(EventHandlerCallRef itself);
PyObject *EventRef_New(EventRef itself);

/********** EventTypeSpec *******/
static PyObject*
EventTypeSpec_New(EventTypeSpec *in)
{
	return Py_BuildValue("ll", in->eventClass, in->eventKind);
}

static int
EventTypeSpec_Convert(PyObject *v, EventTypeSpec *out)
{
	if (PyArg_ParseTuple(v, "ll", &(out->eventClass), &(out->eventKind)))
		return 1;
	return NULL;
}

/********** end EventTypeSpec *******/

/********** HIPoint *******/

static PyObject*
HIPoint_New(HIPoint *in)
{
	return Py_BuildValue("ff", in->x, in->y);
}

static int
HIPoint_Convert(PyObject *v, HIPoint *out)
{
	if (PyArg_ParseTuple(v, "ff", &(out->x), &(out->y)))
		return 1;
	return NULL;
}

/********** end HIPoint *******/

/********** EventHotKeyID *******/

static PyObject*
EventHotKeyID_New(EventHotKeyID *in)
{
	return Py_BuildValue("ll", in->signature, in->id);
}

static int
EventHotKeyID_Convert(PyObject *v, EventHotKeyID *out)
{
	if (PyArg_ParseTuple(v, "ll", &out->signature, &out->id))
		return 1;
	return NULL;
}

/********** end EventHotKeyID *******/

/******** handlecommand ***********/

pascal OSStatus CarbonEvents_HandleCommand(EventHandlerCallRef handlerRef, EventRef event, void *outPyObject) {
	PyObject *retValue;
	int status;

#if USE_MAC_MP_MULTITHREADING
    MPEnterCriticalRegion(reentrantLock, kDurationForever);
    PyEval_RestoreThread(_save);
#endif /* USE_MAC_MP_MULTITHREADING */

    retValue = PyObject_CallFunction((PyObject *)outPyObject, "O&O&", EventHandlerCallRef_New, handlerRef, EventRef_New, event);
    status = PyInt_AsLong(retValue);

#if USE_MAC_MP_MULTITHREADING
    _save = PyEval_SaveThread();
    MPExitCriticalRegion(reentrantLock);
#endif /* USE_MAC_MP_MULTITHREADING */

    return status;
}

/******** end handlecommand ***********/

"""

module = MacModule('CarbonEvents', 'CarbonEvents', includestuff, finalstuff, initstuff)

#class CFReleaserObj(GlobalObjectDefinition):
#	def outputFreeIt(self, name):
#		Output("CFRelease(%s);" % name)

for typ in RefObjectTypes:
	execstr = typ + 'object = GlobalObjectDefinition(typ)'
	exec execstr
	module.addobject(eval(typ + 'object'))

functions = []
for typ in RefObjectTypes: ## go thru all ObjectTypes as defined in CarbonEventsscan.py
	# initialize the lists for carbongen to fill
	execstr = typ + 'methods = []'
	exec execstr

execfile('CarbonEventsgen.py')

for f in functions: module.add(f)	# add all the functions carboneventsgen put in the list

for typ in RefObjectTypes:				 ## go thru all ObjectTypes as defined in CarbonEventsscan.py
	methods = eval(typ + 'methods')  ## get a reference to the method list 
from the main namespace
	obj = eval(typ + 'object')		  ## get a reference to the object
	for m in methods: obj.add(m)	## add each method in the list to the object

installeventhandler = """
EventTypeSpec inSpec;
PyObject *callback;
EventHandlerRef outRef;
OSStatus _err;
EventHandlerUPP event;

if (!PyArg_ParseTuple(_args, "O&O", EventTypeSpec_Convert, &inSpec, &callback))
	return NULL;

event = NewEventHandlerUPP(CarbonEvents_HandleCommand);
_err = InstallEventHandler(_self->ob_itself, event, 1, &inSpec, (void *)callback, &outRef);
if (_err != noErr) return PyMac_Error(_err);

return Py_BuildValue("l", outRef);
"""

f = ManualGenerator("InstallEventHandler", installeventhandler);
f.docstring = lambda: "(EventTargetRef inTarget, EventTypeSpec inSpec, Method callback) -> (EventHandlerRef outRef)"
EventTargetRefobject.add(f)

runappeventloop = """
#if USE_MAC_MP_MULTITHREADING
if (MPCreateCriticalRegion(&reentrantLock) != noErr) {
	printf("lock failure\n");
	return NULL;
}
_save = PyEval_SaveThread();
#endif /* USE_MAC_MP_MULTITHREADING */

RunApplicationEventLoop();

#if USE_MAC_MP_MULTITHREADING
PyEval_RestoreThread(_save);

MPDeleteCriticalRegion(reentrantLock);
#endif /* USE_MAC_MP_MULTITHREADING */

Py_INCREF(Py_None);

return Py_None;
"""			

f = ManualGenerator("RunApplicationEventLoop", runappeventloop);
f.docstring = lambda: "() -> ()"
module.add(f)

SetOutputFileName('_CarbonEvt.c')
module.generate()

import os
os.system("python setup.py build")
