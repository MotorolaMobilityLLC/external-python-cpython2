
/* ========================== Module _Ctl =========================== */

#include "Python.h"



#include "macglue.h"
#include "pymactoolbox.h"

/* Macro to test whether a weak-loaded CFM function exists */
#define PyMac_PRECHECK(rtn) do { if ( &rtn == NULL )  {\
    	PyErr_SetString(PyExc_NotImplementedError, \
    	"Not available in this shared library/OS version"); \
    	return NULL; \
    }} while(0)


#ifdef WITHOUT_FRAMEWORKS
#include <Controls.h>
#include <ControlDefinitions.h>
#else
#include <Carbon/Carbon.h>
#endif

#ifdef USE_TOOLBOX_OBJECT_GLUE
extern PyObject *_CtlObj_New(ControlHandle);
extern int _CtlObj_Convert(PyObject *, ControlHandle *);

#define CtlObj_New _CtlObj_New
#define CtlObj_Convert _CtlObj_Convert
#endif

staticforward PyObject *CtlObj_WhichControl(ControlHandle);

#define as_Control(h) ((ControlHandle)h)
#define as_Resource(ctl) ((Handle)ctl)
#if TARGET_API_MAC_CARBON
#define GetControlRect(ctl, rectp) GetControlBounds(ctl, rectp)
#else
#define GetControlRect(ctl, rectp) (*(rectp) = ((*(ctl))->contrlRect))
#endif

/*
** Parse/generate ControlFontStyleRec records
*/
#if 0 /* Not needed */
static PyObject *
ControlFontStyle_New(ControlFontStyleRec *itself)
{

	return Py_BuildValue("hhhhhhO&O&", itself->flags, itself->font,
		itself->size, itself->style, itself->mode, itself->just,
		QdRGB_New, &itself->foreColor, QdRGB_New, &itself->backColor);
}
#endif

static int
ControlFontStyle_Convert(PyObject *v, ControlFontStyleRec *itself)
{
	return PyArg_ParseTuple(v, "hhhhhhO&O&", &itself->flags,
		&itself->font, &itself->size, &itself->style, &itself->mode,
		&itself->just, QdRGB_Convert, &itself->foreColor,
		QdRGB_Convert, &itself->backColor);
}

/*
** Parse/generate ControlID records
*/
static PyObject *
PyControlID_New(ControlID *itself)
{

	return Py_BuildValue("O&l", PyMac_BuildOSType, itself->signature, itself->id);
}

static int
PyControlID_Convert(PyObject *v, ControlID *itself)
{
	return PyArg_ParseTuple(v, "O&l", PyMac_GetOSType, &itself->signature, &itself->id);
}


/* TrackControl and HandleControlClick callback support */
static PyObject *tracker;
static ControlActionUPP mytracker_upp;
static ControlUserPaneDrawUPP mydrawproc_upp;
static ControlUserPaneIdleUPP myidleproc_upp;
static ControlUserPaneHitTestUPP myhittestproc_upp;
static ControlUserPaneTrackingUPP mytrackingproc_upp;

staticforward int settrackfunc(PyObject *); 	/* forward */
staticforward void clrtrackfunc(void);	/* forward */
staticforward int setcallback(PyObject *, OSType, PyObject *, UniversalProcPtr *);

static PyObject *Ctl_Error;

/* ---------------------- Object type Control ----------------------- */

PyTypeObject Control_Type;

#define CtlObj_Check(x) ((x)->ob_type == &Control_Type)

typedef struct ControlObject {
	PyObject_HEAD
	ControlHandle ob_itself;
	PyObject *ob_callbackdict;
} ControlObject;

PyObject *CtlObj_New(ControlHandle itself)
{
	ControlObject *it;
	if (itself == NULL) return PyMac_Error(resNotFound);
	it = PyObject_NEW(ControlObject, &Control_Type);
	if (it == NULL) return NULL;
	it->ob_itself = itself;
	SetControlReference(itself, (long)it);
	it->ob_callbackdict = NULL;
	return (PyObject *)it;
}
int CtlObj_Convert(PyObject *v, ControlHandle *p_itself)
{
	if (!CtlObj_Check(v))
	{
		PyErr_SetString(PyExc_TypeError, "Control required");
		return 0;
	}
	*p_itself = ((ControlObject *)v)->ob_itself;
	return 1;
}

static void CtlObj_dealloc(ControlObject *self)
{
	Py_XDECREF(self->ob_callbackdict);
	if (self->ob_itself)SetControlReference(self->ob_itself, (long)0); /* Make it forget about us */
	PyMem_DEL(self);
}

static PyObject *CtlObj_HiliteControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	ControlPartCode hiliteState;
#ifndef HiliteControl
	PyMac_PRECHECK(HiliteControl);
#endif
	if (!PyArg_ParseTuple(_args, "h",
	                      &hiliteState))
		return NULL;
	HiliteControl(_self->ob_itself,
	              hiliteState);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_ShowControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
#ifndef ShowControl
	PyMac_PRECHECK(ShowControl);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	ShowControl(_self->ob_itself);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_HideControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
#ifndef HideControl
	PyMac_PRECHECK(HideControl);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	HideControl(_self->ob_itself);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_IsControlActive(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Boolean _rv;
#ifndef IsControlActive
	PyMac_PRECHECK(IsControlActive);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = IsControlActive(_self->ob_itself);
	_res = Py_BuildValue("b",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_IsControlVisible(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Boolean _rv;
#ifndef IsControlVisible
	PyMac_PRECHECK(IsControlVisible);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = IsControlVisible(_self->ob_itself);
	_res = Py_BuildValue("b",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_ActivateControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
#ifndef ActivateControl
	PyMac_PRECHECK(ActivateControl);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = ActivateControl(_self->ob_itself);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_DeactivateControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
#ifndef DeactivateControl
	PyMac_PRECHECK(DeactivateControl);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = DeactivateControl(_self->ob_itself);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SetControlVisibility(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	Boolean inIsVisible;
	Boolean inDoDraw;
#ifndef SetControlVisibility
	PyMac_PRECHECK(SetControlVisibility);
#endif
	if (!PyArg_ParseTuple(_args, "bb",
	                      &inIsVisible,
	                      &inDoDraw))
		return NULL;
	_err = SetControlVisibility(_self->ob_itself,
	                            inIsVisible,
	                            inDoDraw);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_Draw1Control(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
#ifndef Draw1Control
	PyMac_PRECHECK(Draw1Control);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	Draw1Control(_self->ob_itself);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetBestControlRect(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	Rect outRect;
	SInt16 outBaseLineOffset;
#ifndef GetBestControlRect
	PyMac_PRECHECK(GetBestControlRect);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetBestControlRect(_self->ob_itself,
	                          &outRect,
	                          &outBaseLineOffset);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&h",
	                     PyMac_BuildRect, &outRect,
	                     outBaseLineOffset);
	return _res;
}

static PyObject *CtlObj_SetControlFontStyle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	ControlFontStyleRec inStyle;
#ifndef SetControlFontStyle
	PyMac_PRECHECK(SetControlFontStyle);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      ControlFontStyle_Convert, &inStyle))
		return NULL;
	_err = SetControlFontStyle(_self->ob_itself,
	                           &inStyle);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_DrawControlInCurrentPort(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
#ifndef DrawControlInCurrentPort
	PyMac_PRECHECK(DrawControlInCurrentPort);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	DrawControlInCurrentPort(_self->ob_itself);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SetUpControlBackground(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	SInt16 inDepth;
	Boolean inIsColorDevice;
#ifndef SetUpControlBackground
	PyMac_PRECHECK(SetUpControlBackground);
#endif
	if (!PyArg_ParseTuple(_args, "hb",
	                      &inDepth,
	                      &inIsColorDevice))
		return NULL;
	_err = SetUpControlBackground(_self->ob_itself,
	                              inDepth,
	                              inIsColorDevice);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SetUpControlTextColor(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	SInt16 inDepth;
	Boolean inIsColorDevice;
#ifndef SetUpControlTextColor
	PyMac_PRECHECK(SetUpControlTextColor);
#endif
	if (!PyArg_ParseTuple(_args, "hb",
	                      &inDepth,
	                      &inIsColorDevice))
		return NULL;
	_err = SetUpControlTextColor(_self->ob_itself,
	                             inDepth,
	                             inIsColorDevice);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_DragControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Point startPoint;
	Rect limitRect;
	Rect slopRect;
	DragConstraint axis;
#ifndef DragControl
	PyMac_PRECHECK(DragControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&H",
	                      PyMac_GetPoint, &startPoint,
	                      PyMac_GetRect, &limitRect,
	                      PyMac_GetRect, &slopRect,
	                      &axis))
		return NULL;
	DragControl(_self->ob_itself,
	            startPoint,
	            &limitRect,
	            &slopRect,
	            axis);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_TestControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	ControlPartCode _rv;
	Point testPoint;
#ifndef TestControl
	PyMac_PRECHECK(TestControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      PyMac_GetPoint, &testPoint))
		return NULL;
	_rv = TestControl(_self->ob_itself,
	                  testPoint);
	_res = Py_BuildValue("h",
	                     _rv);
	return _res;
}

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_HandleControlContextualMenuClick(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Point inWhere;
	Boolean menuDisplayed;
#ifndef HandleControlContextualMenuClick
	PyMac_PRECHECK(HandleControlContextualMenuClick);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      PyMac_GetPoint, &inWhere))
		return NULL;
	_err = HandleControlContextualMenuClick(_self->ob_itself,
	                                        inWhere,
	                                        &menuDisplayed);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("b",
	                     menuDisplayed);
	return _res;
}
#endif

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_GetControlClickActivation(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Point inWhere;
	EventModifiers inModifiers;
	ClickActivationResult outResult;
#ifndef GetControlClickActivation
	PyMac_PRECHECK(GetControlClickActivation);
#endif
	if (!PyArg_ParseTuple(_args, "O&H",
	                      PyMac_GetPoint, &inWhere,
	                      &inModifiers))
		return NULL;
	_err = GetControlClickActivation(_self->ob_itself,
	                                 inWhere,
	                                 inModifiers,
	                                 &outResult);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     outResult);
	return _res;
}
#endif

static PyObject *CtlObj_HandleControlKey(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	ControlPartCode _rv;
	SInt16 inKeyCode;
	SInt16 inCharCode;
	EventModifiers inModifiers;
#ifndef HandleControlKey
	PyMac_PRECHECK(HandleControlKey);
#endif
	if (!PyArg_ParseTuple(_args, "hhH",
	                      &inKeyCode,
	                      &inCharCode,
	                      &inModifiers))
		return NULL;
	_rv = HandleControlKey(_self->ob_itself,
	                       inKeyCode,
	                       inCharCode,
	                       inModifiers);
	_res = Py_BuildValue("h",
	                     _rv);
	return _res;
}

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_HandleControlSetCursor(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Point localPoint;
	EventModifiers modifiers;
	Boolean cursorWasSet;
#ifndef HandleControlSetCursor
	PyMac_PRECHECK(HandleControlSetCursor);
#endif
	if (!PyArg_ParseTuple(_args, "O&H",
	                      PyMac_GetPoint, &localPoint,
	                      &modifiers))
		return NULL;
	_err = HandleControlSetCursor(_self->ob_itself,
	                              localPoint,
	                              modifiers,
	                              &cursorWasSet);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("b",
	                     cursorWasSet);
	return _res;
}
#endif

static PyObject *CtlObj_MoveControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt16 h;
	SInt16 v;
#ifndef MoveControl
	PyMac_PRECHECK(MoveControl);
#endif
	if (!PyArg_ParseTuple(_args, "hh",
	                      &h,
	                      &v))
		return NULL;
	MoveControl(_self->ob_itself,
	            h,
	            v);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SizeControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt16 w;
	SInt16 h;
#ifndef SizeControl
	PyMac_PRECHECK(SizeControl);
#endif
	if (!PyArg_ParseTuple(_args, "hh",
	                      &w,
	                      &h))
		return NULL;
	SizeControl(_self->ob_itself,
	            w,
	            h);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SetControlTitle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Str255 title;
#ifndef SetControlTitle
	PyMac_PRECHECK(SetControlTitle);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      PyMac_GetStr255, title))
		return NULL;
	SetControlTitle(_self->ob_itself,
	                title);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControlTitle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Str255 title;
#ifndef GetControlTitle
	PyMac_PRECHECK(GetControlTitle);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	GetControlTitle(_self->ob_itself,
	                title);
	_res = Py_BuildValue("O&",
	                     PyMac_BuildStr255, title);
	return _res;
}

static PyObject *CtlObj_SetControlTitleWithCFString(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	CFStringRef inString;
#ifndef SetControlTitleWithCFString
	PyMac_PRECHECK(SetControlTitleWithCFString);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      CFStringRefObj_Convert, &inString))
		return NULL;
	_err = SetControlTitleWithCFString(_self->ob_itself,
	                                   inString);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_CopyControlTitleAsCFString(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	CFStringRef outString;
#ifndef CopyControlTitleAsCFString
	PyMac_PRECHECK(CopyControlTitleAsCFString);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = CopyControlTitleAsCFString(_self->ob_itself,
	                                  &outString);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CFStringRefObj_New, outString);
	return _res;
}

static PyObject *CtlObj_GetControlValue(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt16 _rv;
#ifndef GetControlValue
	PyMac_PRECHECK(GetControlValue);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlValue(_self->ob_itself);
	_res = Py_BuildValue("h",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_SetControlValue(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt16 newValue;
#ifndef SetControlValue
	PyMac_PRECHECK(SetControlValue);
#endif
	if (!PyArg_ParseTuple(_args, "h",
	                      &newValue))
		return NULL;
	SetControlValue(_self->ob_itself,
	                newValue);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControlMinimum(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt16 _rv;
#ifndef GetControlMinimum
	PyMac_PRECHECK(GetControlMinimum);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlMinimum(_self->ob_itself);
	_res = Py_BuildValue("h",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_SetControlMinimum(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt16 newMinimum;
#ifndef SetControlMinimum
	PyMac_PRECHECK(SetControlMinimum);
#endif
	if (!PyArg_ParseTuple(_args, "h",
	                      &newMinimum))
		return NULL;
	SetControlMinimum(_self->ob_itself,
	                  newMinimum);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControlMaximum(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt16 _rv;
#ifndef GetControlMaximum
	PyMac_PRECHECK(GetControlMaximum);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlMaximum(_self->ob_itself);
	_res = Py_BuildValue("h",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_SetControlMaximum(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt16 newMaximum;
#ifndef SetControlMaximum
	PyMac_PRECHECK(SetControlMaximum);
#endif
	if (!PyArg_ParseTuple(_args, "h",
	                      &newMaximum))
		return NULL;
	SetControlMaximum(_self->ob_itself,
	                  newMaximum);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControlViewSize(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt32 _rv;
#ifndef GetControlViewSize
	PyMac_PRECHECK(GetControlViewSize);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlViewSize(_self->ob_itself);
	_res = Py_BuildValue("l",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_SetControlViewSize(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt32 newViewSize;
#ifndef SetControlViewSize
	PyMac_PRECHECK(SetControlViewSize);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &newViewSize))
		return NULL;
	SetControlViewSize(_self->ob_itself,
	                   newViewSize);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControl32BitValue(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt32 _rv;
#ifndef GetControl32BitValue
	PyMac_PRECHECK(GetControl32BitValue);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControl32BitValue(_self->ob_itself);
	_res = Py_BuildValue("l",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_SetControl32BitValue(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt32 newValue;
#ifndef SetControl32BitValue
	PyMac_PRECHECK(SetControl32BitValue);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &newValue))
		return NULL;
	SetControl32BitValue(_self->ob_itself,
	                     newValue);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControl32BitMaximum(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt32 _rv;
#ifndef GetControl32BitMaximum
	PyMac_PRECHECK(GetControl32BitMaximum);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControl32BitMaximum(_self->ob_itself);
	_res = Py_BuildValue("l",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_SetControl32BitMaximum(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt32 newMaximum;
#ifndef SetControl32BitMaximum
	PyMac_PRECHECK(SetControl32BitMaximum);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &newMaximum))
		return NULL;
	SetControl32BitMaximum(_self->ob_itself,
	                       newMaximum);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControl32BitMinimum(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt32 _rv;
#ifndef GetControl32BitMinimum
	PyMac_PRECHECK(GetControl32BitMinimum);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControl32BitMinimum(_self->ob_itself);
	_res = Py_BuildValue("l",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_SetControl32BitMinimum(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt32 newMinimum;
#ifndef SetControl32BitMinimum
	PyMac_PRECHECK(SetControl32BitMinimum);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &newMinimum))
		return NULL;
	SetControl32BitMinimum(_self->ob_itself,
	                       newMinimum);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_IsValidControlHandle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Boolean _rv;
#ifndef IsValidControlHandle
	PyMac_PRECHECK(IsValidControlHandle);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = IsValidControlHandle(_self->ob_itself);
	_res = Py_BuildValue("b",
	                     _rv);
	return _res;
}

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_SetControlID(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	ControlID inID;
#ifndef SetControlID
	PyMac_PRECHECK(SetControlID);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      PyControlID_Convert, &inID))
		return NULL;
	_err = SetControlID(_self->ob_itself,
	                    &inID);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}
#endif

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_GetControlID(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	ControlID outID;
#ifndef GetControlID
	PyMac_PRECHECK(GetControlID);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetControlID(_self->ob_itself,
	                    &outID);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     PyControlID_New, &outID);
	return _res;
}
#endif

static PyObject *CtlObj_SetControlCommandID(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 inCommandID;
#ifndef SetControlCommandID
	PyMac_PRECHECK(SetControlCommandID);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &inCommandID))
		return NULL;
	_err = SetControlCommandID(_self->ob_itself,
	                           inCommandID);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControlCommandID(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 outCommandID;
#ifndef GetControlCommandID
	PyMac_PRECHECK(GetControlCommandID);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetControlCommandID(_self->ob_itself,
	                           &outCommandID);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     outCommandID);
	return _res;
}

static PyObject *CtlObj_RemoveControlProperty(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	OSType propertyCreator;
	OSType propertyTag;
#ifndef RemoveControlProperty
	PyMac_PRECHECK(RemoveControlProperty);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      PyMac_GetOSType, &propertyCreator,
	                      PyMac_GetOSType, &propertyTag))
		return NULL;
	_err = RemoveControlProperty(_self->ob_itself,
	                             propertyCreator,
	                             propertyTag);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_GetControlPropertyAttributes(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	OSType propertyCreator;
	OSType propertyTag;
	UInt32 attributes;
#ifndef GetControlPropertyAttributes
	PyMac_PRECHECK(GetControlPropertyAttributes);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      PyMac_GetOSType, &propertyCreator,
	                      PyMac_GetOSType, &propertyTag))
		return NULL;
	_err = GetControlPropertyAttributes(_self->ob_itself,
	                                    propertyCreator,
	                                    propertyTag,
	                                    &attributes);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     attributes);
	return _res;
}
#endif

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_ChangeControlPropertyAttributes(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	OSType propertyCreator;
	OSType propertyTag;
	UInt32 attributesToSet;
	UInt32 attributesToClear;
#ifndef ChangeControlPropertyAttributes
	PyMac_PRECHECK(ChangeControlPropertyAttributes);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&ll",
	                      PyMac_GetOSType, &propertyCreator,
	                      PyMac_GetOSType, &propertyTag,
	                      &attributesToSet,
	                      &attributesToClear))
		return NULL;
	_err = ChangeControlPropertyAttributes(_self->ob_itself,
	                                       propertyCreator,
	                                       propertyTag,
	                                       attributesToSet,
	                                       attributesToClear);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}
#endif

static PyObject *CtlObj_GetControlRegion(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	ControlPartCode inPart;
	RgnHandle outRegion;
#ifndef GetControlRegion
	PyMac_PRECHECK(GetControlRegion);
#endif
	if (!PyArg_ParseTuple(_args, "hO&",
	                      &inPart,
	                      ResObj_Convert, &outRegion))
		return NULL;
	_err = GetControlRegion(_self->ob_itself,
	                        inPart,
	                        outRegion);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControlVariant(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	ControlVariant _rv;
#ifndef GetControlVariant
	PyMac_PRECHECK(GetControlVariant);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlVariant(_self->ob_itself);
	_res = Py_BuildValue("h",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_SetControlReference(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt32 data;
#ifndef SetControlReference
	PyMac_PRECHECK(SetControlReference);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &data))
		return NULL;
	SetControlReference(_self->ob_itself,
	                    data);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControlReference(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	SInt32 _rv;
#ifndef GetControlReference
	PyMac_PRECHECK(GetControlReference);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlReference(_self->ob_itself);
	_res = Py_BuildValue("l",
	                     _rv);
	return _res;
}

#if !TARGET_API_MAC_CARBON

static PyObject *CtlObj_GetAuxiliaryControlRecord(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Boolean _rv;
	AuxCtlHandle acHndl;
#ifndef GetAuxiliaryControlRecord
	PyMac_PRECHECK(GetAuxiliaryControlRecord);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetAuxiliaryControlRecord(_self->ob_itself,
	                                &acHndl);
	_res = Py_BuildValue("bO&",
	                     _rv,
	                     ResObj_New, acHndl);
	return _res;
}
#endif

#if !TARGET_API_MAC_CARBON

static PyObject *CtlObj_SetControlColor(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	CCTabHandle newColorTable;
#ifndef SetControlColor
	PyMac_PRECHECK(SetControlColor);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      ResObj_Convert, &newColorTable))
		return NULL;
	SetControlColor(_self->ob_itself,
	                newColorTable);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}
#endif

static PyObject *CtlObj_EmbedControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	ControlHandle inContainer;
#ifndef EmbedControl
	PyMac_PRECHECK(EmbedControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      CtlObj_Convert, &inContainer))
		return NULL;
	_err = EmbedControl(_self->ob_itself,
	                    inContainer);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_AutoEmbedControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	WindowPtr inWindow;
#ifndef AutoEmbedControl
	PyMac_PRECHECK(AutoEmbedControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      WinObj_Convert, &inWindow))
		return NULL;
	_err = AutoEmbedControl(_self->ob_itself,
	                        inWindow);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetSuperControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	ControlHandle outParent;
#ifndef GetSuperControl
	PyMac_PRECHECK(GetSuperControl);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetSuperControl(_self->ob_itself,
	                       &outParent);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outParent);
	return _res;
}

static PyObject *CtlObj_CountSubControls(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	UInt16 outNumChildren;
#ifndef CountSubControls
	PyMac_PRECHECK(CountSubControls);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = CountSubControls(_self->ob_itself,
	                        &outNumChildren);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("H",
	                     outNumChildren);
	return _res;
}

static PyObject *CtlObj_GetIndexedSubControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	UInt16 inIndex;
	ControlHandle outSubControl;
#ifndef GetIndexedSubControl
	PyMac_PRECHECK(GetIndexedSubControl);
#endif
	if (!PyArg_ParseTuple(_args, "H",
	                      &inIndex))
		return NULL;
	_err = GetIndexedSubControl(_self->ob_itself,
	                            inIndex,
	                            &outSubControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outSubControl);
	return _res;
}

static PyObject *CtlObj_SetControlSupervisor(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	ControlHandle inBoss;
#ifndef SetControlSupervisor
	PyMac_PRECHECK(SetControlSupervisor);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      CtlObj_Convert, &inBoss))
		return NULL;
	_err = SetControlSupervisor(_self->ob_itself,
	                            inBoss);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetControlFeatures(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	UInt32 outFeatures;
#ifndef GetControlFeatures
	PyMac_PRECHECK(GetControlFeatures);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetControlFeatures(_self->ob_itself,
	                          &outFeatures);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     outFeatures);
	return _res;
}

static PyObject *CtlObj_GetControlDataSize(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	ControlPartCode inPart;
	ResType inTagName;
	Size outMaxSize;
#ifndef GetControlDataSize
	PyMac_PRECHECK(GetControlDataSize);
#endif
	if (!PyArg_ParseTuple(_args, "hO&",
	                      &inPart,
	                      PyMac_GetOSType, &inTagName))
		return NULL;
	_err = GetControlDataSize(_self->ob_itself,
	                          inPart,
	                          inTagName,
	                          &outMaxSize);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     outMaxSize);
	return _res;
}

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_HandleControlDragTracking(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	DragTrackingMessage inMessage;
	DragReference inDrag;
	Boolean outLikesDrag;
#ifndef HandleControlDragTracking
	PyMac_PRECHECK(HandleControlDragTracking);
#endif
	if (!PyArg_ParseTuple(_args, "hO&",
	                      &inMessage,
	                      DragObj_Convert, &inDrag))
		return NULL;
	_err = HandleControlDragTracking(_self->ob_itself,
	                                 inMessage,
	                                 inDrag,
	                                 &outLikesDrag);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("b",
	                     outLikesDrag);
	return _res;
}
#endif

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_HandleControlDragReceive(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	DragReference inDrag;
#ifndef HandleControlDragReceive
	PyMac_PRECHECK(HandleControlDragReceive);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      DragObj_Convert, &inDrag))
		return NULL;
	_err = HandleControlDragReceive(_self->ob_itself,
	                                inDrag);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}
#endif

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_SetControlDragTrackingEnabled(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Boolean tracks;
#ifndef SetControlDragTrackingEnabled
	PyMac_PRECHECK(SetControlDragTrackingEnabled);
#endif
	if (!PyArg_ParseTuple(_args, "b",
	                      &tracks))
		return NULL;
	_err = SetControlDragTrackingEnabled(_self->ob_itself,
	                                     tracks);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}
#endif

#if TARGET_API_MAC_CARBON

static PyObject *CtlObj_IsControlDragTrackingEnabled(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Boolean tracks;
#ifndef IsControlDragTrackingEnabled
	PyMac_PRECHECK(IsControlDragTrackingEnabled);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = IsControlDragTrackingEnabled(_self->ob_itself,
	                                    &tracks);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("b",
	                     tracks);
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_GetControlBounds(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Rect bounds;
#ifndef GetControlBounds
	PyMac_PRECHECK(GetControlBounds);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	GetControlBounds(_self->ob_itself,
	                 &bounds);
	_res = Py_BuildValue("O&",
	                     PyMac_BuildRect, &bounds);
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_IsControlHilited(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Boolean _rv;
#ifndef IsControlHilited
	PyMac_PRECHECK(IsControlHilited);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = IsControlHilited(_self->ob_itself);
	_res = Py_BuildValue("b",
	                     _rv);
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_GetControlHilite(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	UInt16 _rv;
#ifndef GetControlHilite
	PyMac_PRECHECK(GetControlHilite);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlHilite(_self->ob_itself);
	_res = Py_BuildValue("H",
	                     _rv);
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_GetControlOwner(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	WindowPtr _rv;
#ifndef GetControlOwner
	PyMac_PRECHECK(GetControlOwner);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlOwner(_self->ob_itself);
	_res = Py_BuildValue("O&",
	                     WinObj_New, _rv);
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_GetControlDataHandle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Handle _rv;
#ifndef GetControlDataHandle
	PyMac_PRECHECK(GetControlDataHandle);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlDataHandle(_self->ob_itself);
	_res = Py_BuildValue("O&",
	                     ResObj_New, _rv);
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_GetControlPopupMenuHandle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	MenuHandle _rv;
#ifndef GetControlPopupMenuHandle
	PyMac_PRECHECK(GetControlPopupMenuHandle);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlPopupMenuHandle(_self->ob_itself);
	_res = Py_BuildValue("O&",
	                     MenuObj_New, _rv);
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_GetControlPopupMenuID(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	short _rv;
#ifndef GetControlPopupMenuID
	PyMac_PRECHECK(GetControlPopupMenuID);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = GetControlPopupMenuID(_self->ob_itself);
	_res = Py_BuildValue("h",
	                     _rv);
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_SetControlDataHandle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Handle dataHandle;
#ifndef SetControlDataHandle
	PyMac_PRECHECK(SetControlDataHandle);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      ResObj_Convert, &dataHandle))
		return NULL;
	SetControlDataHandle(_self->ob_itself,
	                     dataHandle);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_SetControlBounds(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Rect bounds;
#ifndef SetControlBounds
	PyMac_PRECHECK(SetControlBounds);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      PyMac_GetRect, &bounds))
		return NULL;
	SetControlBounds(_self->ob_itself,
	                 &bounds);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_SetControlPopupMenuHandle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	MenuHandle popupMenu;
#ifndef SetControlPopupMenuHandle
	PyMac_PRECHECK(SetControlPopupMenuHandle);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      MenuObj_Convert, &popupMenu))
		return NULL;
	SetControlPopupMenuHandle(_self->ob_itself,
	                          popupMenu);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS

static PyObject *CtlObj_SetControlPopupMenuID(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	short menuID;
#ifndef SetControlPopupMenuID
	PyMac_PRECHECK(SetControlPopupMenuID);
#endif
	if (!PyArg_ParseTuple(_args, "h",
	                      &menuID))
		return NULL;
	SetControlPopupMenuID(_self->ob_itself,
	                      menuID);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}
#endif

static PyObject *CtlObj_GetBevelButtonMenuValue(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	SInt16 outValue;
#ifndef GetBevelButtonMenuValue
	PyMac_PRECHECK(GetBevelButtonMenuValue);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetBevelButtonMenuValue(_self->ob_itself,
	                               &outValue);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("h",
	                     outValue);
	return _res;
}

static PyObject *CtlObj_SetBevelButtonMenuValue(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	SInt16 inValue;
#ifndef SetBevelButtonMenuValue
	PyMac_PRECHECK(SetBevelButtonMenuValue);
#endif
	if (!PyArg_ParseTuple(_args, "h",
	                      &inValue))
		return NULL;
	_err = SetBevelButtonMenuValue(_self->ob_itself,
	                               inValue);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetBevelButtonMenuHandle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	MenuHandle outHandle;
#ifndef GetBevelButtonMenuHandle
	PyMac_PRECHECK(GetBevelButtonMenuHandle);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetBevelButtonMenuHandle(_self->ob_itself,
	                                &outHandle);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     MenuObj_New, outHandle);
	return _res;
}

static PyObject *CtlObj_SetBevelButtonTransform(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	IconTransformType transform;
#ifndef SetBevelButtonTransform
	PyMac_PRECHECK(SetBevelButtonTransform);
#endif
	if (!PyArg_ParseTuple(_args, "h",
	                      &transform))
		return NULL;
	_err = SetBevelButtonTransform(_self->ob_itself,
	                               transform);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SetDisclosureTriangleLastValue(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	SInt16 inValue;
#ifndef SetDisclosureTriangleLastValue
	PyMac_PRECHECK(SetDisclosureTriangleLastValue);
#endif
	if (!PyArg_ParseTuple(_args, "h",
	                      &inValue))
		return NULL;
	_err = SetDisclosureTriangleLastValue(_self->ob_itself,
	                                      inValue);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetTabContentRect(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	Rect outContentRect;
#ifndef GetTabContentRect
	PyMac_PRECHECK(GetTabContentRect);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetTabContentRect(_self->ob_itself,
	                         &outContentRect);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     PyMac_BuildRect, &outContentRect);
	return _res;
}

static PyObject *CtlObj_SetTabEnabled(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	SInt16 inTabToHilite;
	Boolean inEnabled;
#ifndef SetTabEnabled
	PyMac_PRECHECK(SetTabEnabled);
#endif
	if (!PyArg_ParseTuple(_args, "hb",
	                      &inTabToHilite,
	                      &inEnabled))
		return NULL;
	_err = SetTabEnabled(_self->ob_itself,
	                     inTabToHilite,
	                     inEnabled);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SetImageWellTransform(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	IconTransformType inTransform;
#ifndef SetImageWellTransform
	PyMac_PRECHECK(SetImageWellTransform);
#endif
	if (!PyArg_ParseTuple(_args, "h",
	                      &inTransform))
		return NULL;
	_err = SetImageWellTransform(_self->ob_itself,
	                             inTransform);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserViewStyle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	OSType style;
#ifndef GetDataBrowserViewStyle
	PyMac_PRECHECK(GetDataBrowserViewStyle);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserViewStyle(_self->ob_itself,
	                               &style);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     PyMac_BuildOSType, style);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserViewStyle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	OSType style;
#ifndef SetDataBrowserViewStyle
	PyMac_PRECHECK(SetDataBrowserViewStyle);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      PyMac_GetOSType, &style))
		return NULL;
	_err = SetDataBrowserViewStyle(_self->ob_itself,
	                               style);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_EnableDataBrowserEditCommand(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Boolean _rv;
	UInt32 command;
#ifndef EnableDataBrowserEditCommand
	PyMac_PRECHECK(EnableDataBrowserEditCommand);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &command))
		return NULL;
	_rv = EnableDataBrowserEditCommand(_self->ob_itself,
	                                   command);
	_res = Py_BuildValue("b",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_ExecuteDataBrowserEditCommand(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 command;
#ifndef ExecuteDataBrowserEditCommand
	PyMac_PRECHECK(ExecuteDataBrowserEditCommand);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &command))
		return NULL;
	_err = ExecuteDataBrowserEditCommand(_self->ob_itself,
	                                     command);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserSelectionAnchor(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 first;
	UInt32 last;
#ifndef GetDataBrowserSelectionAnchor
	PyMac_PRECHECK(GetDataBrowserSelectionAnchor);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserSelectionAnchor(_self->ob_itself,
	                                     &first,
	                                     &last);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("ll",
	                     first,
	                     last);
	return _res;
}

static PyObject *CtlObj_MoveDataBrowserSelectionAnchor(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 direction;
	Boolean extendSelection;
#ifndef MoveDataBrowserSelectionAnchor
	PyMac_PRECHECK(MoveDataBrowserSelectionAnchor);
#endif
	if (!PyArg_ParseTuple(_args, "lb",
	                      &direction,
	                      &extendSelection))
		return NULL;
	_err = MoveDataBrowserSelectionAnchor(_self->ob_itself,
	                                      direction,
	                                      extendSelection);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_OpenDataBrowserContainer(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 container;
#ifndef OpenDataBrowserContainer
	PyMac_PRECHECK(OpenDataBrowserContainer);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &container))
		return NULL;
	_err = OpenDataBrowserContainer(_self->ob_itself,
	                                container);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_CloseDataBrowserContainer(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 container;
#ifndef CloseDataBrowserContainer
	PyMac_PRECHECK(CloseDataBrowserContainer);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &container))
		return NULL;
	_err = CloseDataBrowserContainer(_self->ob_itself,
	                                 container);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SortDataBrowserContainer(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 container;
	Boolean sortChildren;
#ifndef SortDataBrowserContainer
	PyMac_PRECHECK(SortDataBrowserContainer);
#endif
	if (!PyArg_ParseTuple(_args, "lb",
	                      &container,
	                      &sortChildren))
		return NULL;
	_err = SortDataBrowserContainer(_self->ob_itself,
	                                container,
	                                sortChildren);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserItems(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 container;
	Boolean recurse;
	UInt32 state;
	Handle items;
#ifndef GetDataBrowserItems
	PyMac_PRECHECK(GetDataBrowserItems);
#endif
	if (!PyArg_ParseTuple(_args, "lblO&",
	                      &container,
	                      &recurse,
	                      &state,
	                      ResObj_Convert, &items))
		return NULL;
	_err = GetDataBrowserItems(_self->ob_itself,
	                           container,
	                           recurse,
	                           state,
	                           items);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserItemCount(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 container;
	Boolean recurse;
	UInt32 state;
	UInt32 numItems;
#ifndef GetDataBrowserItemCount
	PyMac_PRECHECK(GetDataBrowserItemCount);
#endif
	if (!PyArg_ParseTuple(_args, "lbl",
	                      &container,
	                      &recurse,
	                      &state))
		return NULL;
	_err = GetDataBrowserItemCount(_self->ob_itself,
	                               container,
	                               recurse,
	                               state,
	                               &numItems);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     numItems);
	return _res;
}

static PyObject *CtlObj_IsDataBrowserItemSelected(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Boolean _rv;
	UInt32 item;
#ifndef IsDataBrowserItemSelected
	PyMac_PRECHECK(IsDataBrowserItemSelected);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &item))
		return NULL;
	_rv = IsDataBrowserItemSelected(_self->ob_itself,
	                                item);
	_res = Py_BuildValue("b",
	                     _rv);
	return _res;
}

static PyObject *CtlObj_GetDataBrowserItemState(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 item;
	UInt32 state;
#ifndef GetDataBrowserItemState
	PyMac_PRECHECK(GetDataBrowserItemState);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &item))
		return NULL;
	_err = GetDataBrowserItemState(_self->ob_itself,
	                               item,
	                               &state);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     state);
	return _res;
}

static PyObject *CtlObj_RevealDataBrowserItem(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 item;
	UInt32 propertyID;
	UInt8 options;
#ifndef RevealDataBrowserItem
	PyMac_PRECHECK(RevealDataBrowserItem);
#endif
	if (!PyArg_ParseTuple(_args, "llb",
	                      &item,
	                      &propertyID,
	                      &options))
		return NULL;
	_err = RevealDataBrowserItem(_self->ob_itself,
	                             item,
	                             propertyID,
	                             options);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SetDataBrowserActiveItems(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Boolean active;
#ifndef SetDataBrowserActiveItems
	PyMac_PRECHECK(SetDataBrowserActiveItems);
#endif
	if (!PyArg_ParseTuple(_args, "b",
	                      &active))
		return NULL;
	_err = SetDataBrowserActiveItems(_self->ob_itself,
	                                 active);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserActiveItems(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Boolean active;
#ifndef GetDataBrowserActiveItems
	PyMac_PRECHECK(GetDataBrowserActiveItems);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserActiveItems(_self->ob_itself,
	                                 &active);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("b",
	                     active);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserScrollBarInset(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Rect insetRect;
#ifndef SetDataBrowserScrollBarInset
	PyMac_PRECHECK(SetDataBrowserScrollBarInset);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = SetDataBrowserScrollBarInset(_self->ob_itself,
	                                    &insetRect);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     PyMac_BuildRect, &insetRect);
	return _res;
}

static PyObject *CtlObj_GetDataBrowserScrollBarInset(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Rect insetRect;
#ifndef GetDataBrowserScrollBarInset
	PyMac_PRECHECK(GetDataBrowserScrollBarInset);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserScrollBarInset(_self->ob_itself,
	                                    &insetRect);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     PyMac_BuildRect, &insetRect);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserTarget(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 target;
#ifndef SetDataBrowserTarget
	PyMac_PRECHECK(SetDataBrowserTarget);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &target))
		return NULL;
	_err = SetDataBrowserTarget(_self->ob_itself,
	                            target);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTarget(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 target;
#ifndef GetDataBrowserTarget
	PyMac_PRECHECK(GetDataBrowserTarget);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserTarget(_self->ob_itself,
	                            &target);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     target);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserSortOrder(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt16 order;
#ifndef SetDataBrowserSortOrder
	PyMac_PRECHECK(SetDataBrowserSortOrder);
#endif
	if (!PyArg_ParseTuple(_args, "H",
	                      &order))
		return NULL;
	_err = SetDataBrowserSortOrder(_self->ob_itself,
	                               order);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserSortOrder(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt16 order;
#ifndef GetDataBrowserSortOrder
	PyMac_PRECHECK(GetDataBrowserSortOrder);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserSortOrder(_self->ob_itself,
	                               &order);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("H",
	                     order);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserScrollPosition(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 top;
	UInt32 left;
#ifndef SetDataBrowserScrollPosition
	PyMac_PRECHECK(SetDataBrowserScrollPosition);
#endif
	if (!PyArg_ParseTuple(_args, "ll",
	                      &top,
	                      &left))
		return NULL;
	_err = SetDataBrowserScrollPosition(_self->ob_itself,
	                                    top,
	                                    left);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserScrollPosition(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 top;
	UInt32 left;
#ifndef GetDataBrowserScrollPosition
	PyMac_PRECHECK(GetDataBrowserScrollPosition);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserScrollPosition(_self->ob_itself,
	                                    &top,
	                                    &left);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("ll",
	                     top,
	                     left);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserHasScrollBars(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Boolean horiz;
	Boolean vert;
#ifndef SetDataBrowserHasScrollBars
	PyMac_PRECHECK(SetDataBrowserHasScrollBars);
#endif
	if (!PyArg_ParseTuple(_args, "bb",
	                      &horiz,
	                      &vert))
		return NULL;
	_err = SetDataBrowserHasScrollBars(_self->ob_itself,
	                                   horiz,
	                                   vert);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserHasScrollBars(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Boolean horiz;
	Boolean vert;
#ifndef GetDataBrowserHasScrollBars
	PyMac_PRECHECK(GetDataBrowserHasScrollBars);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserHasScrollBars(_self->ob_itself,
	                                   &horiz,
	                                   &vert);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("bb",
	                     horiz,
	                     vert);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserSortProperty(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 property;
#ifndef SetDataBrowserSortProperty
	PyMac_PRECHECK(SetDataBrowserSortProperty);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &property))
		return NULL;
	_err = SetDataBrowserSortProperty(_self->ob_itself,
	                                  property);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserSortProperty(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 property;
#ifndef GetDataBrowserSortProperty
	PyMac_PRECHECK(GetDataBrowserSortProperty);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserSortProperty(_self->ob_itself,
	                                  &property);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     property);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserSelectionFlags(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 selectionFlags;
#ifndef SetDataBrowserSelectionFlags
	PyMac_PRECHECK(SetDataBrowserSelectionFlags);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &selectionFlags))
		return NULL;
	_err = SetDataBrowserSelectionFlags(_self->ob_itself,
	                                    selectionFlags);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserSelectionFlags(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 selectionFlags;
#ifndef GetDataBrowserSelectionFlags
	PyMac_PRECHECK(GetDataBrowserSelectionFlags);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserSelectionFlags(_self->ob_itself,
	                                    &selectionFlags);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     selectionFlags);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserPropertyFlags(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 property;
	UInt32 flags;
#ifndef SetDataBrowserPropertyFlags
	PyMac_PRECHECK(SetDataBrowserPropertyFlags);
#endif
	if (!PyArg_ParseTuple(_args, "ll",
	                      &property,
	                      &flags))
		return NULL;
	_err = SetDataBrowserPropertyFlags(_self->ob_itself,
	                                   property,
	                                   flags);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserPropertyFlags(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 property;
	UInt32 flags;
#ifndef GetDataBrowserPropertyFlags
	PyMac_PRECHECK(GetDataBrowserPropertyFlags);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &property))
		return NULL;
	_err = GetDataBrowserPropertyFlags(_self->ob_itself,
	                                   property,
	                                   &flags);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     flags);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserEditText(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	CFStringRef text;
#ifndef SetDataBrowserEditText
	PyMac_PRECHECK(SetDataBrowserEditText);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      CFStringRefObj_Convert, &text))
		return NULL;
	_err = SetDataBrowserEditText(_self->ob_itself,
	                              text);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserEditText(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	CFMutableStringRef text;
#ifndef GetDataBrowserEditText
	PyMac_PRECHECK(GetDataBrowserEditText);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      CFMutableStringRefObj_Convert, &text))
		return NULL;
	_err = GetDataBrowserEditText(_self->ob_itself,
	                              text);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SetDataBrowserEditItem(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 item;
	UInt32 property;
#ifndef SetDataBrowserEditItem
	PyMac_PRECHECK(SetDataBrowserEditItem);
#endif
	if (!PyArg_ParseTuple(_args, "ll",
	                      &item,
	                      &property))
		return NULL;
	_err = SetDataBrowserEditItem(_self->ob_itself,
	                              item,
	                              property);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserEditItem(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 item;
	UInt32 property;
#ifndef GetDataBrowserEditItem
	PyMac_PRECHECK(GetDataBrowserEditItem);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserEditItem(_self->ob_itself,
	                              &item,
	                              &property);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("ll",
	                     item,
	                     property);
	return _res;
}

static PyObject *CtlObj_GetDataBrowserItemPartBounds(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 item;
	UInt32 property;
	OSType part;
	Rect bounds;
#ifndef GetDataBrowserItemPartBounds
	PyMac_PRECHECK(GetDataBrowserItemPartBounds);
#endif
	if (!PyArg_ParseTuple(_args, "llO&",
	                      &item,
	                      &property,
	                      PyMac_GetOSType, &part))
		return NULL;
	_err = GetDataBrowserItemPartBounds(_self->ob_itself,
	                                    item,
	                                    property,
	                                    part,
	                                    &bounds);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     PyMac_BuildRect, &bounds);
	return _res;
}

static PyObject *CtlObj_RemoveDataBrowserTableViewColumn(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 column;
#ifndef RemoveDataBrowserTableViewColumn
	PyMac_PRECHECK(RemoveDataBrowserTableViewColumn);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &column))
		return NULL;
	_err = RemoveDataBrowserTableViewColumn(_self->ob_itself,
	                                        column);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewColumnCount(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 numColumns;
#ifndef GetDataBrowserTableViewColumnCount
	PyMac_PRECHECK(GetDataBrowserTableViewColumnCount);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserTableViewColumnCount(_self->ob_itself,
	                                          &numColumns);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     numColumns);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserTableViewHiliteStyle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 hiliteStyle;
#ifndef SetDataBrowserTableViewHiliteStyle
	PyMac_PRECHECK(SetDataBrowserTableViewHiliteStyle);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &hiliteStyle))
		return NULL;
	_err = SetDataBrowserTableViewHiliteStyle(_self->ob_itself,
	                                          hiliteStyle);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewHiliteStyle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 hiliteStyle;
#ifndef GetDataBrowserTableViewHiliteStyle
	PyMac_PRECHECK(GetDataBrowserTableViewHiliteStyle);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserTableViewHiliteStyle(_self->ob_itself,
	                                          &hiliteStyle);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     hiliteStyle);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserTableViewRowHeight(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt16 height;
#ifndef SetDataBrowserTableViewRowHeight
	PyMac_PRECHECK(SetDataBrowserTableViewRowHeight);
#endif
	if (!PyArg_ParseTuple(_args, "H",
	                      &height))
		return NULL;
	_err = SetDataBrowserTableViewRowHeight(_self->ob_itself,
	                                        height);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewRowHeight(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt16 height;
#ifndef GetDataBrowserTableViewRowHeight
	PyMac_PRECHECK(GetDataBrowserTableViewRowHeight);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserTableViewRowHeight(_self->ob_itself,
	                                        &height);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("H",
	                     height);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserTableViewColumnWidth(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt16 width;
#ifndef SetDataBrowserTableViewColumnWidth
	PyMac_PRECHECK(SetDataBrowserTableViewColumnWidth);
#endif
	if (!PyArg_ParseTuple(_args, "H",
	                      &width))
		return NULL;
	_err = SetDataBrowserTableViewColumnWidth(_self->ob_itself,
	                                          width);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewColumnWidth(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt16 width;
#ifndef GetDataBrowserTableViewColumnWidth
	PyMac_PRECHECK(GetDataBrowserTableViewColumnWidth);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserTableViewColumnWidth(_self->ob_itself,
	                                          &width);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("H",
	                     width);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserTableViewItemRowHeight(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 item;
	UInt16 height;
#ifndef SetDataBrowserTableViewItemRowHeight
	PyMac_PRECHECK(SetDataBrowserTableViewItemRowHeight);
#endif
	if (!PyArg_ParseTuple(_args, "lH",
	                      &item,
	                      &height))
		return NULL;
	_err = SetDataBrowserTableViewItemRowHeight(_self->ob_itself,
	                                            item,
	                                            height);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewItemRowHeight(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 item;
	UInt16 height;
#ifndef GetDataBrowserTableViewItemRowHeight
	PyMac_PRECHECK(GetDataBrowserTableViewItemRowHeight);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &item))
		return NULL;
	_err = GetDataBrowserTableViewItemRowHeight(_self->ob_itself,
	                                            item,
	                                            &height);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("H",
	                     height);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserTableViewNamedColumnWidth(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 column;
	UInt16 width;
#ifndef SetDataBrowserTableViewNamedColumnWidth
	PyMac_PRECHECK(SetDataBrowserTableViewNamedColumnWidth);
#endif
	if (!PyArg_ParseTuple(_args, "lH",
	                      &column,
	                      &width))
		return NULL;
	_err = SetDataBrowserTableViewNamedColumnWidth(_self->ob_itself,
	                                               column,
	                                               width);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewNamedColumnWidth(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 column;
	UInt16 width;
#ifndef GetDataBrowserTableViewNamedColumnWidth
	PyMac_PRECHECK(GetDataBrowserTableViewNamedColumnWidth);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &column))
		return NULL;
	_err = GetDataBrowserTableViewNamedColumnWidth(_self->ob_itself,
	                                               column,
	                                               &width);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("H",
	                     width);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserTableViewGeometry(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Boolean variableWidthColumns;
	Boolean variableHeightRows;
#ifndef SetDataBrowserTableViewGeometry
	PyMac_PRECHECK(SetDataBrowserTableViewGeometry);
#endif
	if (!PyArg_ParseTuple(_args, "bb",
	                      &variableWidthColumns,
	                      &variableHeightRows))
		return NULL;
	_err = SetDataBrowserTableViewGeometry(_self->ob_itself,
	                                       variableWidthColumns,
	                                       variableHeightRows);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewGeometry(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Boolean variableWidthColumns;
	Boolean variableHeightRows;
#ifndef GetDataBrowserTableViewGeometry
	PyMac_PRECHECK(GetDataBrowserTableViewGeometry);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserTableViewGeometry(_self->ob_itself,
	                                       &variableWidthColumns,
	                                       &variableHeightRows);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("bb",
	                     variableWidthColumns,
	                     variableHeightRows);
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewItemID(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 row;
	UInt32 item;
#ifndef GetDataBrowserTableViewItemID
	PyMac_PRECHECK(GetDataBrowserTableViewItemID);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &row))
		return NULL;
	_err = GetDataBrowserTableViewItemID(_self->ob_itself,
	                                     row,
	                                     &item);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     item);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserTableViewItemRow(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 item;
	UInt32 row;
#ifndef SetDataBrowserTableViewItemRow
	PyMac_PRECHECK(SetDataBrowserTableViewItemRow);
#endif
	if (!PyArg_ParseTuple(_args, "ll",
	                      &item,
	                      &row))
		return NULL;
	_err = SetDataBrowserTableViewItemRow(_self->ob_itself,
	                                      item,
	                                      row);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewItemRow(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 item;
	UInt32 row;
#ifndef GetDataBrowserTableViewItemRow
	PyMac_PRECHECK(GetDataBrowserTableViewItemRow);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &item))
		return NULL;
	_err = GetDataBrowserTableViewItemRow(_self->ob_itself,
	                                      item,
	                                      &row);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     row);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserTableViewColumnPosition(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 column;
	UInt32 position;
#ifndef SetDataBrowserTableViewColumnPosition
	PyMac_PRECHECK(SetDataBrowserTableViewColumnPosition);
#endif
	if (!PyArg_ParseTuple(_args, "ll",
	                      &column,
	                      &position))
		return NULL;
	_err = SetDataBrowserTableViewColumnPosition(_self->ob_itself,
	                                             column,
	                                             position);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewColumnPosition(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 column;
	UInt32 position;
#ifndef GetDataBrowserTableViewColumnPosition
	PyMac_PRECHECK(GetDataBrowserTableViewColumnPosition);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &column))
		return NULL;
	_err = GetDataBrowserTableViewColumnPosition(_self->ob_itself,
	                                             column,
	                                             &position);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     position);
	return _res;
}

static PyObject *CtlObj_GetDataBrowserTableViewColumnProperty(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 column;
	UInt32 property;
#ifndef GetDataBrowserTableViewColumnProperty
	PyMac_PRECHECK(GetDataBrowserTableViewColumnProperty);
#endif
	if (!PyArg_ParseTuple(_args, "l",
	                      &column))
		return NULL;
	_err = GetDataBrowserTableViewColumnProperty(_self->ob_itself,
	                                             column,
	                                             &property);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     property);
	return _res;
}

static PyObject *CtlObj_AutoSizeDataBrowserListViewColumns(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
#ifndef AutoSizeDataBrowserListViewColumns
	PyMac_PRECHECK(AutoSizeDataBrowserListViewColumns);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = AutoSizeDataBrowserListViewColumns(_self->ob_itself);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_SetDataBrowserListViewHeaderBtnHeight(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt16 height;
#ifndef SetDataBrowserListViewHeaderBtnHeight
	PyMac_PRECHECK(SetDataBrowserListViewHeaderBtnHeight);
#endif
	if (!PyArg_ParseTuple(_args, "H",
	                      &height))
		return NULL;
	_err = SetDataBrowserListViewHeaderBtnHeight(_self->ob_itself,
	                                             height);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserListViewHeaderBtnHeight(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt16 height;
#ifndef GetDataBrowserListViewHeaderBtnHeight
	PyMac_PRECHECK(GetDataBrowserListViewHeaderBtnHeight);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserListViewHeaderBtnHeight(_self->ob_itself,
	                                             &height);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("H",
	                     height);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserListViewUsePlainBackground(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Boolean usePlainBackground;
#ifndef SetDataBrowserListViewUsePlainBackground
	PyMac_PRECHECK(SetDataBrowserListViewUsePlainBackground);
#endif
	if (!PyArg_ParseTuple(_args, "b",
	                      &usePlainBackground))
		return NULL;
	_err = SetDataBrowserListViewUsePlainBackground(_self->ob_itself,
	                                                usePlainBackground);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserListViewUsePlainBackground(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Boolean usePlainBackground;
#ifndef GetDataBrowserListViewUsePlainBackground
	PyMac_PRECHECK(GetDataBrowserListViewUsePlainBackground);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserListViewUsePlainBackground(_self->ob_itself,
	                                                &usePlainBackground);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("b",
	                     usePlainBackground);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserListViewDisclosureColumn(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 column;
	Boolean expandableRows;
#ifndef SetDataBrowserListViewDisclosureColumn
	PyMac_PRECHECK(SetDataBrowserListViewDisclosureColumn);
#endif
	if (!PyArg_ParseTuple(_args, "lb",
	                      &column,
	                      &expandableRows))
		return NULL;
	_err = SetDataBrowserListViewDisclosureColumn(_self->ob_itself,
	                                              column,
	                                              expandableRows);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserListViewDisclosureColumn(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 column;
	Boolean expandableRows;
#ifndef GetDataBrowserListViewDisclosureColumn
	PyMac_PRECHECK(GetDataBrowserListViewDisclosureColumn);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserListViewDisclosureColumn(_self->ob_itself,
	                                              &column,
	                                              &expandableRows);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("lb",
	                     column,
	                     expandableRows);
	return _res;
}

static PyObject *CtlObj_GetDataBrowserColumnViewPath(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	Handle path;
#ifndef GetDataBrowserColumnViewPath
	PyMac_PRECHECK(GetDataBrowserColumnViewPath);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      ResObj_Convert, &path))
		return NULL;
	_err = GetDataBrowserColumnViewPath(_self->ob_itself,
	                                    path);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserColumnViewPathLength(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	UInt32 pathLength;
#ifndef GetDataBrowserColumnViewPathLength
	PyMac_PRECHECK(GetDataBrowserColumnViewPathLength);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserColumnViewPathLength(_self->ob_itself,
	                                          &pathLength);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("l",
	                     pathLength);
	return _res;
}

static PyObject *CtlObj_SetDataBrowserColumnViewDisplayType(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	OSType propertyType;
#ifndef SetDataBrowserColumnViewDisplayType
	PyMac_PRECHECK(SetDataBrowserColumnViewDisplayType);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      PyMac_GetOSType, &propertyType))
		return NULL;
	_err = SetDataBrowserColumnViewDisplayType(_self->ob_itself,
	                                           propertyType);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *CtlObj_GetDataBrowserColumnViewDisplayType(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	OSType propertyType;
#ifndef GetDataBrowserColumnViewDisplayType
	PyMac_PRECHECK(GetDataBrowserColumnViewDisplayType);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_err = GetDataBrowserColumnViewDisplayType(_self->ob_itself,
	                                           &propertyType);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     PyMac_BuildOSType, propertyType);
	return _res;
}

static PyObject *CtlObj_as_Resource(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Handle _rv;
#ifndef as_Resource
	PyMac_PRECHECK(as_Resource);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	_rv = as_Resource(_self->ob_itself);
	_res = Py_BuildValue("O&",
	                     ResObj_New, _rv);
	return _res;
}

static PyObject *CtlObj_GetControlRect(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	Rect rect;
#ifndef GetControlRect
	PyMac_PRECHECK(GetControlRect);
#endif
	if (!PyArg_ParseTuple(_args, ""))
		return NULL;
	GetControlRect(_self->ob_itself,
	               &rect);
	_res = Py_BuildValue("O&",
	                     PyMac_BuildRect, &rect);
	return _res;
}

static PyObject *CtlObj_DisposeControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;

		if (!PyArg_ParseTuple(_args, ""))
			return NULL;
		if ( _self->ob_itself ) {
			SetControlReference(_self->ob_itself, (long)0); /* Make it forget about us */
			DisposeControl(_self->ob_itself);
			_self->ob_itself = NULL;
		}
		Py_INCREF(Py_None);
		_res = Py_None;
		return _res;

}

static PyObject *CtlObj_TrackControl(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;

	ControlPartCode _rv;
	Point startPoint;
	ControlActionUPP upp = 0;
	PyObject *callback = 0;

	if (!PyArg_ParseTuple(_args, "O&|O",
	                      PyMac_GetPoint, &startPoint, &callback))
		return NULL;
	if (callback && callback != Py_None) {
		if (PyInt_Check(callback) && PyInt_AS_LONG(callback) == -1)
			upp = (ControlActionUPP)-1;
		else {
			settrackfunc(callback);
			upp = mytracker_upp;
		}
	}
	_rv = TrackControl(_self->ob_itself,
	                   startPoint,
	                   upp);
	clrtrackfunc();
	_res = Py_BuildValue("h",
	                     _rv);
	return _res;

}

static PyObject *CtlObj_HandleControlClick(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;

	ControlPartCode _rv;
	Point startPoint;
	SInt16 modifiers;
	ControlActionUPP upp = 0;
	PyObject *callback = 0;

	if (!PyArg_ParseTuple(_args, "O&h|O",
	                      PyMac_GetPoint, &startPoint,
	                      &modifiers,
	                      &callback))
		return NULL;
	if (callback && callback != Py_None) {
		if (PyInt_Check(callback) && PyInt_AS_LONG(callback) == -1)
			upp = (ControlActionUPP)-1;
		else {
			settrackfunc(callback);
			upp = mytracker_upp;
		}
	}
	_rv = HandleControlClick(_self->ob_itself,
	                   startPoint,
	                   modifiers,
	                   upp);
	clrtrackfunc();
	_res = Py_BuildValue("h",
	                     _rv);
	return _res;

}

static PyObject *CtlObj_SetControlData(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;

	OSErr _err;
	ControlPartCode inPart;
	ResType inTagName;
	Size bufferSize;
	Ptr buffer;

	if (!PyArg_ParseTuple(_args, "hO&s#",
	                      &inPart,
	                      PyMac_GetOSType, &inTagName,
	                      &buffer, &bufferSize))
		return NULL;

	_err = SetControlData(_self->ob_itself,
		              inPart,
		              inTagName,
		              bufferSize,
	                      buffer);

	if (_err != noErr)
		return PyMac_Error(_err);
	_res = Py_None;
	return _res;

}

static PyObject *CtlObj_GetControlData(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;

	OSErr _err;
	ControlPartCode inPart;
	ResType inTagName;
	Size bufferSize;
	Ptr buffer;
	Size outSize;

	if (!PyArg_ParseTuple(_args, "hO&",
	                      &inPart,
	                      PyMac_GetOSType, &inTagName))
		return NULL;

	/* allocate a buffer for the data */
	_err = GetControlDataSize(_self->ob_itself,
		                  inPart,
		                  inTagName,
	                          &bufferSize);
	if (_err != noErr)
		return PyMac_Error(_err);
	buffer = PyMem_NEW(char, bufferSize);
	if (buffer == NULL)
		return PyErr_NoMemory();

	_err = GetControlData(_self->ob_itself,
		              inPart,
		              inTagName,
		              bufferSize,
	                      buffer,
	                      &outSize);

	if (_err != noErr) {
		PyMem_DEL(buffer);
		return PyMac_Error(_err);
	}
	_res = Py_BuildValue("s#", buffer, outSize);
	PyMem_DEL(buffer);
	return _res;

}

static PyObject *CtlObj_SetControlData_Handle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;

	OSErr _err;
	ControlPartCode inPart;
	ResType inTagName;
	Handle buffer;

	if (!PyArg_ParseTuple(_args, "hO&O&",
	                      &inPart,
	                      PyMac_GetOSType, &inTagName,
	                      OptResObj_Convert, &buffer))
		return NULL;

	_err = SetControlData(_self->ob_itself,
		              inPart,
		              inTagName,
		              sizeof(buffer),
	                      (Ptr)&buffer);

	if (_err != noErr)
		return PyMac_Error(_err);
	_res = Py_None;
	return _res;

}

static PyObject *CtlObj_GetControlData_Handle(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;

	OSErr _err;
	ControlPartCode inPart;
	ResType inTagName;
	Size bufferSize;
	Handle hdl;

	if (!PyArg_ParseTuple(_args, "hO&",
	                      &inPart,
	                      PyMac_GetOSType, &inTagName))
		return NULL;

	/* Check it is handle-sized */
	_err = GetControlDataSize(_self->ob_itself,
		                  inPart,
		                  inTagName,
	                          &bufferSize);
	if (_err != noErr)
		return PyMac_Error(_err);
	if (bufferSize != sizeof(Handle)) {
		PyErr_SetString(Ctl_Error, "GetControlDataSize() != sizeof(Handle)");
		return NULL;
	}

	_err = GetControlData(_self->ob_itself,
		              inPart,
		              inTagName,
		              sizeof(Handle),
	                      (Ptr)&hdl,
	                      &bufferSize);

	if (_err != noErr) {
		return PyMac_Error(_err);
	}
	_res = Py_BuildValue("O&", OptResObj_New, hdl);
	return _res;

}

static PyObject *CtlObj_SetControlData_Callback(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;

	OSErr _err;
	ControlPartCode inPart;
	ResType inTagName;
	PyObject *callback;
	UniversalProcPtr c_callback;

	if (!PyArg_ParseTuple(_args, "hO&O",
	                      &inPart,
	                      PyMac_GetOSType, &inTagName,
	                      &callback))
		return NULL;

	if ( setcallback((PyObject *)_self, inTagName, callback, &c_callback) < 0 )
		return NULL;
	_err = SetControlData(_self->ob_itself,
		              inPart,
		              inTagName,
		              sizeof(c_callback),
	                      (Ptr)&c_callback);

	if (_err != noErr)
		return PyMac_Error(_err);
	_res = Py_None;
	return _res;

}

#if !TARGET_API_MAC_CARBON

static PyObject *CtlObj_GetPopupData(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;

	PopupPrivateDataHandle hdl;

	if ( (*_self->ob_itself)->contrlData == NULL ) {
		PyErr_SetString(Ctl_Error, "No contrlData handle in control");
		return 0;
	}
	hdl = (PopupPrivateDataHandle)(*_self->ob_itself)->contrlData;
	HLock((Handle)hdl);
	_res = Py_BuildValue("O&i", MenuObj_New, (*hdl)->mHandle, (int)(*hdl)->mID);
	HUnlock((Handle)hdl);
	return _res;

}
#endif

#if !TARGET_API_MAC_CARBON

static PyObject *CtlObj_SetPopupData(ControlObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;

	PopupPrivateDataHandle hdl;
	MenuHandle mHandle;
	short mID;

	if (!PyArg_ParseTuple(_args, "O&h", MenuObj_Convert, &mHandle, &mID) )
		return 0;
	if ( (*_self->ob_itself)->contrlData == NULL ) {
		PyErr_SetString(Ctl_Error, "No contrlData handle in control");
		return 0;
	}
	hdl = (PopupPrivateDataHandle)(*_self->ob_itself)->contrlData;
	(*hdl)->mHandle = mHandle;
	(*hdl)->mID = mID;
	Py_INCREF(Py_None);
	return Py_None;

}
#endif

static PyMethodDef CtlObj_methods[] = {
	{"HiliteControl", (PyCFunction)CtlObj_HiliteControl, 1,
	 "(ControlPartCode hiliteState) -> None"},
	{"ShowControl", (PyCFunction)CtlObj_ShowControl, 1,
	 "() -> None"},
	{"HideControl", (PyCFunction)CtlObj_HideControl, 1,
	 "() -> None"},
	{"IsControlActive", (PyCFunction)CtlObj_IsControlActive, 1,
	 "() -> (Boolean _rv)"},
	{"IsControlVisible", (PyCFunction)CtlObj_IsControlVisible, 1,
	 "() -> (Boolean _rv)"},
	{"ActivateControl", (PyCFunction)CtlObj_ActivateControl, 1,
	 "() -> None"},
	{"DeactivateControl", (PyCFunction)CtlObj_DeactivateControl, 1,
	 "() -> None"},
	{"SetControlVisibility", (PyCFunction)CtlObj_SetControlVisibility, 1,
	 "(Boolean inIsVisible, Boolean inDoDraw) -> None"},
	{"Draw1Control", (PyCFunction)CtlObj_Draw1Control, 1,
	 "() -> None"},
	{"GetBestControlRect", (PyCFunction)CtlObj_GetBestControlRect, 1,
	 "() -> (Rect outRect, SInt16 outBaseLineOffset)"},
	{"SetControlFontStyle", (PyCFunction)CtlObj_SetControlFontStyle, 1,
	 "(ControlFontStyleRec inStyle) -> None"},
	{"DrawControlInCurrentPort", (PyCFunction)CtlObj_DrawControlInCurrentPort, 1,
	 "() -> None"},
	{"SetUpControlBackground", (PyCFunction)CtlObj_SetUpControlBackground, 1,
	 "(SInt16 inDepth, Boolean inIsColorDevice) -> None"},
	{"SetUpControlTextColor", (PyCFunction)CtlObj_SetUpControlTextColor, 1,
	 "(SInt16 inDepth, Boolean inIsColorDevice) -> None"},
	{"DragControl", (PyCFunction)CtlObj_DragControl, 1,
	 "(Point startPoint, Rect limitRect, Rect slopRect, DragConstraint axis) -> None"},
	{"TestControl", (PyCFunction)CtlObj_TestControl, 1,
	 "(Point testPoint) -> (ControlPartCode _rv)"},

#if TARGET_API_MAC_CARBON
	{"HandleControlContextualMenuClick", (PyCFunction)CtlObj_HandleControlContextualMenuClick, 1,
	 "(Point inWhere) -> (Boolean menuDisplayed)"},
#endif

#if TARGET_API_MAC_CARBON
	{"GetControlClickActivation", (PyCFunction)CtlObj_GetControlClickActivation, 1,
	 "(Point inWhere, EventModifiers inModifiers) -> (ClickActivationResult outResult)"},
#endif
	{"HandleControlKey", (PyCFunction)CtlObj_HandleControlKey, 1,
	 "(SInt16 inKeyCode, SInt16 inCharCode, EventModifiers inModifiers) -> (ControlPartCode _rv)"},

#if TARGET_API_MAC_CARBON
	{"HandleControlSetCursor", (PyCFunction)CtlObj_HandleControlSetCursor, 1,
	 "(Point localPoint, EventModifiers modifiers) -> (Boolean cursorWasSet)"},
#endif
	{"MoveControl", (PyCFunction)CtlObj_MoveControl, 1,
	 "(SInt16 h, SInt16 v) -> None"},
	{"SizeControl", (PyCFunction)CtlObj_SizeControl, 1,
	 "(SInt16 w, SInt16 h) -> None"},
	{"SetControlTitle", (PyCFunction)CtlObj_SetControlTitle, 1,
	 "(Str255 title) -> None"},
	{"GetControlTitle", (PyCFunction)CtlObj_GetControlTitle, 1,
	 "() -> (Str255 title)"},
	{"SetControlTitleWithCFString", (PyCFunction)CtlObj_SetControlTitleWithCFString, 1,
	 "(CFStringRef inString) -> None"},
	{"CopyControlTitleAsCFString", (PyCFunction)CtlObj_CopyControlTitleAsCFString, 1,
	 "() -> (CFStringRef outString)"},
	{"GetControlValue", (PyCFunction)CtlObj_GetControlValue, 1,
	 "() -> (SInt16 _rv)"},
	{"SetControlValue", (PyCFunction)CtlObj_SetControlValue, 1,
	 "(SInt16 newValue) -> None"},
	{"GetControlMinimum", (PyCFunction)CtlObj_GetControlMinimum, 1,
	 "() -> (SInt16 _rv)"},
	{"SetControlMinimum", (PyCFunction)CtlObj_SetControlMinimum, 1,
	 "(SInt16 newMinimum) -> None"},
	{"GetControlMaximum", (PyCFunction)CtlObj_GetControlMaximum, 1,
	 "() -> (SInt16 _rv)"},
	{"SetControlMaximum", (PyCFunction)CtlObj_SetControlMaximum, 1,
	 "(SInt16 newMaximum) -> None"},
	{"GetControlViewSize", (PyCFunction)CtlObj_GetControlViewSize, 1,
	 "() -> (SInt32 _rv)"},
	{"SetControlViewSize", (PyCFunction)CtlObj_SetControlViewSize, 1,
	 "(SInt32 newViewSize) -> None"},
	{"GetControl32BitValue", (PyCFunction)CtlObj_GetControl32BitValue, 1,
	 "() -> (SInt32 _rv)"},
	{"SetControl32BitValue", (PyCFunction)CtlObj_SetControl32BitValue, 1,
	 "(SInt32 newValue) -> None"},
	{"GetControl32BitMaximum", (PyCFunction)CtlObj_GetControl32BitMaximum, 1,
	 "() -> (SInt32 _rv)"},
	{"SetControl32BitMaximum", (PyCFunction)CtlObj_SetControl32BitMaximum, 1,
	 "(SInt32 newMaximum) -> None"},
	{"GetControl32BitMinimum", (PyCFunction)CtlObj_GetControl32BitMinimum, 1,
	 "() -> (SInt32 _rv)"},
	{"SetControl32BitMinimum", (PyCFunction)CtlObj_SetControl32BitMinimum, 1,
	 "(SInt32 newMinimum) -> None"},
	{"IsValidControlHandle", (PyCFunction)CtlObj_IsValidControlHandle, 1,
	 "() -> (Boolean _rv)"},

#if TARGET_API_MAC_CARBON
	{"SetControlID", (PyCFunction)CtlObj_SetControlID, 1,
	 "(ControlID inID) -> None"},
#endif

#if TARGET_API_MAC_CARBON
	{"GetControlID", (PyCFunction)CtlObj_GetControlID, 1,
	 "() -> (ControlID outID)"},
#endif
	{"SetControlCommandID", (PyCFunction)CtlObj_SetControlCommandID, 1,
	 "(UInt32 inCommandID) -> None"},
	{"GetControlCommandID", (PyCFunction)CtlObj_GetControlCommandID, 1,
	 "() -> (UInt32 outCommandID)"},
	{"RemoveControlProperty", (PyCFunction)CtlObj_RemoveControlProperty, 1,
	 "(OSType propertyCreator, OSType propertyTag) -> None"},

#if TARGET_API_MAC_CARBON
	{"GetControlPropertyAttributes", (PyCFunction)CtlObj_GetControlPropertyAttributes, 1,
	 "(OSType propertyCreator, OSType propertyTag) -> (UInt32 attributes)"},
#endif

#if TARGET_API_MAC_CARBON
	{"ChangeControlPropertyAttributes", (PyCFunction)CtlObj_ChangeControlPropertyAttributes, 1,
	 "(OSType propertyCreator, OSType propertyTag, UInt32 attributesToSet, UInt32 attributesToClear) -> None"},
#endif
	{"GetControlRegion", (PyCFunction)CtlObj_GetControlRegion, 1,
	 "(ControlPartCode inPart, RgnHandle outRegion) -> None"},
	{"GetControlVariant", (PyCFunction)CtlObj_GetControlVariant, 1,
	 "() -> (ControlVariant _rv)"},
	{"SetControlReference", (PyCFunction)CtlObj_SetControlReference, 1,
	 "(SInt32 data) -> None"},
	{"GetControlReference", (PyCFunction)CtlObj_GetControlReference, 1,
	 "() -> (SInt32 _rv)"},

#if !TARGET_API_MAC_CARBON
	{"GetAuxiliaryControlRecord", (PyCFunction)CtlObj_GetAuxiliaryControlRecord, 1,
	 "() -> (Boolean _rv, AuxCtlHandle acHndl)"},
#endif

#if !TARGET_API_MAC_CARBON
	{"SetControlColor", (PyCFunction)CtlObj_SetControlColor, 1,
	 "(CCTabHandle newColorTable) -> None"},
#endif
	{"EmbedControl", (PyCFunction)CtlObj_EmbedControl, 1,
	 "(ControlHandle inContainer) -> None"},
	{"AutoEmbedControl", (PyCFunction)CtlObj_AutoEmbedControl, 1,
	 "(WindowPtr inWindow) -> None"},
	{"GetSuperControl", (PyCFunction)CtlObj_GetSuperControl, 1,
	 "() -> (ControlHandle outParent)"},
	{"CountSubControls", (PyCFunction)CtlObj_CountSubControls, 1,
	 "() -> (UInt16 outNumChildren)"},
	{"GetIndexedSubControl", (PyCFunction)CtlObj_GetIndexedSubControl, 1,
	 "(UInt16 inIndex) -> (ControlHandle outSubControl)"},
	{"SetControlSupervisor", (PyCFunction)CtlObj_SetControlSupervisor, 1,
	 "(ControlHandle inBoss) -> None"},
	{"GetControlFeatures", (PyCFunction)CtlObj_GetControlFeatures, 1,
	 "() -> (UInt32 outFeatures)"},
	{"GetControlDataSize", (PyCFunction)CtlObj_GetControlDataSize, 1,
	 "(ControlPartCode inPart, ResType inTagName) -> (Size outMaxSize)"},

#if TARGET_API_MAC_CARBON
	{"HandleControlDragTracking", (PyCFunction)CtlObj_HandleControlDragTracking, 1,
	 "(DragTrackingMessage inMessage, DragReference inDrag) -> (Boolean outLikesDrag)"},
#endif

#if TARGET_API_MAC_CARBON
	{"HandleControlDragReceive", (PyCFunction)CtlObj_HandleControlDragReceive, 1,
	 "(DragReference inDrag) -> None"},
#endif

#if TARGET_API_MAC_CARBON
	{"SetControlDragTrackingEnabled", (PyCFunction)CtlObj_SetControlDragTrackingEnabled, 1,
	 "(Boolean tracks) -> None"},
#endif

#if TARGET_API_MAC_CARBON
	{"IsControlDragTrackingEnabled", (PyCFunction)CtlObj_IsControlDragTrackingEnabled, 1,
	 "() -> (Boolean tracks)"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"GetControlBounds", (PyCFunction)CtlObj_GetControlBounds, 1,
	 "() -> (Rect bounds)"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"IsControlHilited", (PyCFunction)CtlObj_IsControlHilited, 1,
	 "() -> (Boolean _rv)"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"GetControlHilite", (PyCFunction)CtlObj_GetControlHilite, 1,
	 "() -> (UInt16 _rv)"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"GetControlOwner", (PyCFunction)CtlObj_GetControlOwner, 1,
	 "() -> (WindowPtr _rv)"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"GetControlDataHandle", (PyCFunction)CtlObj_GetControlDataHandle, 1,
	 "() -> (Handle _rv)"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"GetControlPopupMenuHandle", (PyCFunction)CtlObj_GetControlPopupMenuHandle, 1,
	 "() -> (MenuHandle _rv)"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"GetControlPopupMenuID", (PyCFunction)CtlObj_GetControlPopupMenuID, 1,
	 "() -> (short _rv)"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"SetControlDataHandle", (PyCFunction)CtlObj_SetControlDataHandle, 1,
	 "(Handle dataHandle) -> None"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"SetControlBounds", (PyCFunction)CtlObj_SetControlBounds, 1,
	 "(Rect bounds) -> None"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"SetControlPopupMenuHandle", (PyCFunction)CtlObj_SetControlPopupMenuHandle, 1,
	 "(MenuHandle popupMenu) -> None"},
#endif

#if ACCESSOR_CALLS_ARE_FUNCTIONS
	{"SetControlPopupMenuID", (PyCFunction)CtlObj_SetControlPopupMenuID, 1,
	 "(short menuID) -> None"},
#endif
	{"GetBevelButtonMenuValue", (PyCFunction)CtlObj_GetBevelButtonMenuValue, 1,
	 "() -> (SInt16 outValue)"},
	{"SetBevelButtonMenuValue", (PyCFunction)CtlObj_SetBevelButtonMenuValue, 1,
	 "(SInt16 inValue) -> None"},
	{"GetBevelButtonMenuHandle", (PyCFunction)CtlObj_GetBevelButtonMenuHandle, 1,
	 "() -> (MenuHandle outHandle)"},
	{"SetBevelButtonTransform", (PyCFunction)CtlObj_SetBevelButtonTransform, 1,
	 "(IconTransformType transform) -> None"},
	{"SetDisclosureTriangleLastValue", (PyCFunction)CtlObj_SetDisclosureTriangleLastValue, 1,
	 "(SInt16 inValue) -> None"},
	{"GetTabContentRect", (PyCFunction)CtlObj_GetTabContentRect, 1,
	 "() -> (Rect outContentRect)"},
	{"SetTabEnabled", (PyCFunction)CtlObj_SetTabEnabled, 1,
	 "(SInt16 inTabToHilite, Boolean inEnabled) -> None"},
	{"SetImageWellTransform", (PyCFunction)CtlObj_SetImageWellTransform, 1,
	 "(IconTransformType inTransform) -> None"},
	{"GetDataBrowserViewStyle", (PyCFunction)CtlObj_GetDataBrowserViewStyle, 1,
	 "() -> (OSType style)"},
	{"SetDataBrowserViewStyle", (PyCFunction)CtlObj_SetDataBrowserViewStyle, 1,
	 "(OSType style) -> None"},
	{"EnableDataBrowserEditCommand", (PyCFunction)CtlObj_EnableDataBrowserEditCommand, 1,
	 "(UInt32 command) -> (Boolean _rv)"},
	{"ExecuteDataBrowserEditCommand", (PyCFunction)CtlObj_ExecuteDataBrowserEditCommand, 1,
	 "(UInt32 command) -> None"},
	{"GetDataBrowserSelectionAnchor", (PyCFunction)CtlObj_GetDataBrowserSelectionAnchor, 1,
	 "() -> (UInt32 first, UInt32 last)"},
	{"MoveDataBrowserSelectionAnchor", (PyCFunction)CtlObj_MoveDataBrowserSelectionAnchor, 1,
	 "(UInt32 direction, Boolean extendSelection) -> None"},
	{"OpenDataBrowserContainer", (PyCFunction)CtlObj_OpenDataBrowserContainer, 1,
	 "(UInt32 container) -> None"},
	{"CloseDataBrowserContainer", (PyCFunction)CtlObj_CloseDataBrowserContainer, 1,
	 "(UInt32 container) -> None"},
	{"SortDataBrowserContainer", (PyCFunction)CtlObj_SortDataBrowserContainer, 1,
	 "(UInt32 container, Boolean sortChildren) -> None"},
	{"GetDataBrowserItems", (PyCFunction)CtlObj_GetDataBrowserItems, 1,
	 "(UInt32 container, Boolean recurse, UInt32 state, Handle items) -> None"},
	{"GetDataBrowserItemCount", (PyCFunction)CtlObj_GetDataBrowserItemCount, 1,
	 "(UInt32 container, Boolean recurse, UInt32 state) -> (UInt32 numItems)"},
	{"IsDataBrowserItemSelected", (PyCFunction)CtlObj_IsDataBrowserItemSelected, 1,
	 "(UInt32 item) -> (Boolean _rv)"},
	{"GetDataBrowserItemState", (PyCFunction)CtlObj_GetDataBrowserItemState, 1,
	 "(UInt32 item) -> (UInt32 state)"},
	{"RevealDataBrowserItem", (PyCFunction)CtlObj_RevealDataBrowserItem, 1,
	 "(UInt32 item, UInt32 propertyID, UInt8 options) -> None"},
	{"SetDataBrowserActiveItems", (PyCFunction)CtlObj_SetDataBrowserActiveItems, 1,
	 "(Boolean active) -> None"},
	{"GetDataBrowserActiveItems", (PyCFunction)CtlObj_GetDataBrowserActiveItems, 1,
	 "() -> (Boolean active)"},
	{"SetDataBrowserScrollBarInset", (PyCFunction)CtlObj_SetDataBrowserScrollBarInset, 1,
	 "() -> (Rect insetRect)"},
	{"GetDataBrowserScrollBarInset", (PyCFunction)CtlObj_GetDataBrowserScrollBarInset, 1,
	 "() -> (Rect insetRect)"},
	{"SetDataBrowserTarget", (PyCFunction)CtlObj_SetDataBrowserTarget, 1,
	 "(UInt32 target) -> None"},
	{"GetDataBrowserTarget", (PyCFunction)CtlObj_GetDataBrowserTarget, 1,
	 "() -> (UInt32 target)"},
	{"SetDataBrowserSortOrder", (PyCFunction)CtlObj_SetDataBrowserSortOrder, 1,
	 "(UInt16 order) -> None"},
	{"GetDataBrowserSortOrder", (PyCFunction)CtlObj_GetDataBrowserSortOrder, 1,
	 "() -> (UInt16 order)"},
	{"SetDataBrowserScrollPosition", (PyCFunction)CtlObj_SetDataBrowserScrollPosition, 1,
	 "(UInt32 top, UInt32 left) -> None"},
	{"GetDataBrowserScrollPosition", (PyCFunction)CtlObj_GetDataBrowserScrollPosition, 1,
	 "() -> (UInt32 top, UInt32 left)"},
	{"SetDataBrowserHasScrollBars", (PyCFunction)CtlObj_SetDataBrowserHasScrollBars, 1,
	 "(Boolean horiz, Boolean vert) -> None"},
	{"GetDataBrowserHasScrollBars", (PyCFunction)CtlObj_GetDataBrowserHasScrollBars, 1,
	 "() -> (Boolean horiz, Boolean vert)"},
	{"SetDataBrowserSortProperty", (PyCFunction)CtlObj_SetDataBrowserSortProperty, 1,
	 "(UInt32 property) -> None"},
	{"GetDataBrowserSortProperty", (PyCFunction)CtlObj_GetDataBrowserSortProperty, 1,
	 "() -> (UInt32 property)"},
	{"SetDataBrowserSelectionFlags", (PyCFunction)CtlObj_SetDataBrowserSelectionFlags, 1,
	 "(UInt32 selectionFlags) -> None"},
	{"GetDataBrowserSelectionFlags", (PyCFunction)CtlObj_GetDataBrowserSelectionFlags, 1,
	 "() -> (UInt32 selectionFlags)"},
	{"SetDataBrowserPropertyFlags", (PyCFunction)CtlObj_SetDataBrowserPropertyFlags, 1,
	 "(UInt32 property, UInt32 flags) -> None"},
	{"GetDataBrowserPropertyFlags", (PyCFunction)CtlObj_GetDataBrowserPropertyFlags, 1,
	 "(UInt32 property) -> (UInt32 flags)"},
	{"SetDataBrowserEditText", (PyCFunction)CtlObj_SetDataBrowserEditText, 1,
	 "(CFStringRef text) -> None"},
	{"GetDataBrowserEditText", (PyCFunction)CtlObj_GetDataBrowserEditText, 1,
	 "(CFMutableStringRef text) -> None"},
	{"SetDataBrowserEditItem", (PyCFunction)CtlObj_SetDataBrowserEditItem, 1,
	 "(UInt32 item, UInt32 property) -> None"},
	{"GetDataBrowserEditItem", (PyCFunction)CtlObj_GetDataBrowserEditItem, 1,
	 "() -> (UInt32 item, UInt32 property)"},
	{"GetDataBrowserItemPartBounds", (PyCFunction)CtlObj_GetDataBrowserItemPartBounds, 1,
	 "(UInt32 item, UInt32 property, OSType part) -> (Rect bounds)"},
	{"RemoveDataBrowserTableViewColumn", (PyCFunction)CtlObj_RemoveDataBrowserTableViewColumn, 1,
	 "(UInt32 column) -> None"},
	{"GetDataBrowserTableViewColumnCount", (PyCFunction)CtlObj_GetDataBrowserTableViewColumnCount, 1,
	 "() -> (UInt32 numColumns)"},
	{"SetDataBrowserTableViewHiliteStyle", (PyCFunction)CtlObj_SetDataBrowserTableViewHiliteStyle, 1,
	 "(UInt32 hiliteStyle) -> None"},
	{"GetDataBrowserTableViewHiliteStyle", (PyCFunction)CtlObj_GetDataBrowserTableViewHiliteStyle, 1,
	 "() -> (UInt32 hiliteStyle)"},
	{"SetDataBrowserTableViewRowHeight", (PyCFunction)CtlObj_SetDataBrowserTableViewRowHeight, 1,
	 "(UInt16 height) -> None"},
	{"GetDataBrowserTableViewRowHeight", (PyCFunction)CtlObj_GetDataBrowserTableViewRowHeight, 1,
	 "() -> (UInt16 height)"},
	{"SetDataBrowserTableViewColumnWidth", (PyCFunction)CtlObj_SetDataBrowserTableViewColumnWidth, 1,
	 "(UInt16 width) -> None"},
	{"GetDataBrowserTableViewColumnWidth", (PyCFunction)CtlObj_GetDataBrowserTableViewColumnWidth, 1,
	 "() -> (UInt16 width)"},
	{"SetDataBrowserTableViewItemRowHeight", (PyCFunction)CtlObj_SetDataBrowserTableViewItemRowHeight, 1,
	 "(UInt32 item, UInt16 height) -> None"},
	{"GetDataBrowserTableViewItemRowHeight", (PyCFunction)CtlObj_GetDataBrowserTableViewItemRowHeight, 1,
	 "(UInt32 item) -> (UInt16 height)"},
	{"SetDataBrowserTableViewNamedColumnWidth", (PyCFunction)CtlObj_SetDataBrowserTableViewNamedColumnWidth, 1,
	 "(UInt32 column, UInt16 width) -> None"},
	{"GetDataBrowserTableViewNamedColumnWidth", (PyCFunction)CtlObj_GetDataBrowserTableViewNamedColumnWidth, 1,
	 "(UInt32 column) -> (UInt16 width)"},
	{"SetDataBrowserTableViewGeometry", (PyCFunction)CtlObj_SetDataBrowserTableViewGeometry, 1,
	 "(Boolean variableWidthColumns, Boolean variableHeightRows) -> None"},
	{"GetDataBrowserTableViewGeometry", (PyCFunction)CtlObj_GetDataBrowserTableViewGeometry, 1,
	 "() -> (Boolean variableWidthColumns, Boolean variableHeightRows)"},
	{"GetDataBrowserTableViewItemID", (PyCFunction)CtlObj_GetDataBrowserTableViewItemID, 1,
	 "(UInt32 row) -> (UInt32 item)"},
	{"SetDataBrowserTableViewItemRow", (PyCFunction)CtlObj_SetDataBrowserTableViewItemRow, 1,
	 "(UInt32 item, UInt32 row) -> None"},
	{"GetDataBrowserTableViewItemRow", (PyCFunction)CtlObj_GetDataBrowserTableViewItemRow, 1,
	 "(UInt32 item) -> (UInt32 row)"},
	{"SetDataBrowserTableViewColumnPosition", (PyCFunction)CtlObj_SetDataBrowserTableViewColumnPosition, 1,
	 "(UInt32 column, UInt32 position) -> None"},
	{"GetDataBrowserTableViewColumnPosition", (PyCFunction)CtlObj_GetDataBrowserTableViewColumnPosition, 1,
	 "(UInt32 column) -> (UInt32 position)"},
	{"GetDataBrowserTableViewColumnProperty", (PyCFunction)CtlObj_GetDataBrowserTableViewColumnProperty, 1,
	 "(UInt32 column) -> (UInt32 property)"},
	{"AutoSizeDataBrowserListViewColumns", (PyCFunction)CtlObj_AutoSizeDataBrowserListViewColumns, 1,
	 "() -> None"},
	{"SetDataBrowserListViewHeaderBtnHeight", (PyCFunction)CtlObj_SetDataBrowserListViewHeaderBtnHeight, 1,
	 "(UInt16 height) -> None"},
	{"GetDataBrowserListViewHeaderBtnHeight", (PyCFunction)CtlObj_GetDataBrowserListViewHeaderBtnHeight, 1,
	 "() -> (UInt16 height)"},
	{"SetDataBrowserListViewUsePlainBackground", (PyCFunction)CtlObj_SetDataBrowserListViewUsePlainBackground, 1,
	 "(Boolean usePlainBackground) -> None"},
	{"GetDataBrowserListViewUsePlainBackground", (PyCFunction)CtlObj_GetDataBrowserListViewUsePlainBackground, 1,
	 "() -> (Boolean usePlainBackground)"},
	{"SetDataBrowserListViewDisclosureColumn", (PyCFunction)CtlObj_SetDataBrowserListViewDisclosureColumn, 1,
	 "(UInt32 column, Boolean expandableRows) -> None"},
	{"GetDataBrowserListViewDisclosureColumn", (PyCFunction)CtlObj_GetDataBrowserListViewDisclosureColumn, 1,
	 "() -> (UInt32 column, Boolean expandableRows)"},
	{"GetDataBrowserColumnViewPath", (PyCFunction)CtlObj_GetDataBrowserColumnViewPath, 1,
	 "(Handle path) -> None"},
	{"GetDataBrowserColumnViewPathLength", (PyCFunction)CtlObj_GetDataBrowserColumnViewPathLength, 1,
	 "() -> (UInt32 pathLength)"},
	{"SetDataBrowserColumnViewDisplayType", (PyCFunction)CtlObj_SetDataBrowserColumnViewDisplayType, 1,
	 "(OSType propertyType) -> None"},
	{"GetDataBrowserColumnViewDisplayType", (PyCFunction)CtlObj_GetDataBrowserColumnViewDisplayType, 1,
	 "() -> (OSType propertyType)"},
	{"as_Resource", (PyCFunction)CtlObj_as_Resource, 1,
	 "() -> (Handle _rv)"},
	{"GetControlRect", (PyCFunction)CtlObj_GetControlRect, 1,
	 "() -> (Rect rect)"},
	{"DisposeControl", (PyCFunction)CtlObj_DisposeControl, 1,
	 "() -> None"},
	{"TrackControl", (PyCFunction)CtlObj_TrackControl, 1,
	 "(Point startPoint [,trackercallback]) -> (ControlPartCode _rv)"},
	{"HandleControlClick", (PyCFunction)CtlObj_HandleControlClick, 1,
	 "(Point startPoint, Integer modifiers, [,trackercallback]) -> (ControlPartCode _rv)"},
	{"SetControlData", (PyCFunction)CtlObj_SetControlData, 1,
	 "(stuff) -> None"},
	{"GetControlData", (PyCFunction)CtlObj_GetControlData, 1,
	 "(part, type) -> String"},
	{"SetControlData_Handle", (PyCFunction)CtlObj_SetControlData_Handle, 1,
	 "(ResObj) -> None"},
	{"GetControlData_Handle", (PyCFunction)CtlObj_GetControlData_Handle, 1,
	 "(part, type) -> ResObj"},
	{"SetControlData_Callback", (PyCFunction)CtlObj_SetControlData_Callback, 1,
	 "(callbackfunc) -> None"},

#if !TARGET_API_MAC_CARBON
	{"GetPopupData", (PyCFunction)CtlObj_GetPopupData, 1,
	 NULL},
#endif

#if !TARGET_API_MAC_CARBON
	{"SetPopupData", (PyCFunction)CtlObj_SetPopupData, 1,
	 NULL},
#endif
	{NULL, NULL, 0}
};

PyMethodChain CtlObj_chain = { CtlObj_methods, NULL };

static PyObject *CtlObj_getattr(ControlObject *self, char *name)
{
	return Py_FindMethodInChain(&CtlObj_chain, (PyObject *)self, name);
}

#define CtlObj_setattr NULL

static int CtlObj_compare(ControlObject *self, ControlObject *other)
{
	unsigned long v, w;

	if (!CtlObj_Check((PyObject *)other))
	{
		v=(unsigned long)self;
		w=(unsigned long)other;
	}
	else
	{
		v=(unsigned long)self->ob_itself;
		w=(unsigned long)other->ob_itself;
	}
	if( v < w ) return -1;
	if( v > w ) return 1;
	return 0;
}

#define CtlObj_repr NULL

static long CtlObj_hash(ControlObject *self)
{
	return (long)self->ob_itself;
}

PyTypeObject Control_Type = {
	PyObject_HEAD_INIT(NULL)
	0, /*ob_size*/
	"_Ctl.Control", /*tp_name*/
	sizeof(ControlObject), /*tp_basicsize*/
	0, /*tp_itemsize*/
	/* methods */
	(destructor) CtlObj_dealloc, /*tp_dealloc*/
	0, /*tp_print*/
	(getattrfunc) CtlObj_getattr, /*tp_getattr*/
	(setattrfunc) CtlObj_setattr, /*tp_setattr*/
	(cmpfunc) CtlObj_compare, /*tp_compare*/
	(reprfunc) CtlObj_repr, /*tp_repr*/
	(PyNumberMethods *)0, /* tp_as_number */
	(PySequenceMethods *)0, /* tp_as_sequence */
	(PyMappingMethods *)0, /* tp_as_mapping */
	(hashfunc) CtlObj_hash, /*tp_hash*/
};

/* -------------------- End object type Control --------------------- */


static PyObject *Ctl_NewControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	ControlHandle _rv;
	WindowPtr owningWindow;
	Rect boundsRect;
	Str255 controlTitle;
	Boolean initiallyVisible;
	SInt16 initialValue;
	SInt16 minimumValue;
	SInt16 maximumValue;
	SInt16 procID;
	SInt32 controlReference;
#ifndef NewControl
	PyMac_PRECHECK(NewControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&bhhhhl",
	                      WinObj_Convert, &owningWindow,
	                      PyMac_GetRect, &boundsRect,
	                      PyMac_GetStr255, controlTitle,
	                      &initiallyVisible,
	                      &initialValue,
	                      &minimumValue,
	                      &maximumValue,
	                      &procID,
	                      &controlReference))
		return NULL;
	_rv = NewControl(owningWindow,
	                 &boundsRect,
	                 controlTitle,
	                 initiallyVisible,
	                 initialValue,
	                 minimumValue,
	                 maximumValue,
	                 procID,
	                 controlReference);
	_res = Py_BuildValue("O&",
	                     CtlObj_New, _rv);
	return _res;
}

static PyObject *Ctl_GetNewControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	ControlHandle _rv;
	SInt16 resourceID;
	WindowPtr owningWindow;
#ifndef GetNewControl
	PyMac_PRECHECK(GetNewControl);
#endif
	if (!PyArg_ParseTuple(_args, "hO&",
	                      &resourceID,
	                      WinObj_Convert, &owningWindow))
		return NULL;
	_rv = GetNewControl(resourceID,
	                    owningWindow);
	_res = Py_BuildValue("O&",
	                     CtlObj_New, _rv);
	return _res;
}

static PyObject *Ctl_DrawControls(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	WindowPtr theWindow;
#ifndef DrawControls
	PyMac_PRECHECK(DrawControls);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      WinObj_Convert, &theWindow))
		return NULL;
	DrawControls(theWindow);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *Ctl_UpdateControls(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	WindowPtr theWindow;
	RgnHandle updateRegion;
#ifndef UpdateControls
	PyMac_PRECHECK(UpdateControls);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      WinObj_Convert, &theWindow,
	                      ResObj_Convert, &updateRegion))
		return NULL;
	UpdateControls(theWindow,
	               updateRegion);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *Ctl_FindControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	ControlPartCode _rv;
	Point testPoint;
	WindowPtr theWindow;
	ControlHandle theControl;
#ifndef FindControl
	PyMac_PRECHECK(FindControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      PyMac_GetPoint, &testPoint,
	                      WinObj_Convert, &theWindow))
		return NULL;
	_rv = FindControl(testPoint,
	                  theWindow,
	                  &theControl);
	_res = Py_BuildValue("hO&",
	                     _rv,
	                     CtlObj_WhichControl, theControl);
	return _res;
}

static PyObject *Ctl_FindControlUnderMouse(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	ControlHandle _rv;
	Point inWhere;
	WindowPtr inWindow;
	SInt16 outPart;
#ifndef FindControlUnderMouse
	PyMac_PRECHECK(FindControlUnderMouse);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      PyMac_GetPoint, &inWhere,
	                      WinObj_Convert, &inWindow))
		return NULL;
	_rv = FindControlUnderMouse(inWhere,
	                            inWindow,
	                            &outPart);
	_res = Py_BuildValue("O&h",
	                     CtlObj_New, _rv,
	                     outPart);
	return _res;
}

static PyObject *Ctl_IdleControls(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	WindowPtr inWindow;
#ifndef IdleControls
	PyMac_PRECHECK(IdleControls);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      WinObj_Convert, &inWindow))
		return NULL;
	IdleControls(inWindow);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

#if TARGET_API_MAC_CARBON

static PyObject *Ctl_GetControlByID(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr inWindow;
	ControlID inID;
	ControlHandle outControl;
#ifndef GetControlByID
	PyMac_PRECHECK(GetControlByID);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      WinObj_Convert, &inWindow,
	                      PyControlID_Convert, &inID))
		return NULL;
	_err = GetControlByID(inWindow,
	                      &inID,
	                      &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}
#endif

static PyObject *Ctl_DumpControlHierarchy(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	WindowPtr inWindow;
	FSSpec inDumpFile;
#ifndef DumpControlHierarchy
	PyMac_PRECHECK(DumpControlHierarchy);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      WinObj_Convert, &inWindow,
	                      PyMac_GetFSSpec, &inDumpFile))
		return NULL;
	_err = DumpControlHierarchy(inWindow,
	                            &inDumpFile);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *Ctl_CreateRootControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	WindowPtr inWindow;
	ControlHandle outControl;
#ifndef CreateRootControl
	PyMac_PRECHECK(CreateRootControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      WinObj_Convert, &inWindow))
		return NULL;
	_err = CreateRootControl(inWindow,
	                         &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_GetRootControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	WindowPtr inWindow;
	ControlHandle outControl;
#ifndef GetRootControl
	PyMac_PRECHECK(GetRootControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      WinObj_Convert, &inWindow))
		return NULL;
	_err = GetRootControl(inWindow,
	                      &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_GetKeyboardFocus(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	WindowPtr inWindow;
	ControlHandle outControl;
#ifndef GetKeyboardFocus
	PyMac_PRECHECK(GetKeyboardFocus);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      WinObj_Convert, &inWindow))
		return NULL;
	_err = GetKeyboardFocus(inWindow,
	                        &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_SetKeyboardFocus(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	WindowPtr inWindow;
	ControlHandle inControl;
	ControlFocusPart inPart;
#ifndef SetKeyboardFocus
	PyMac_PRECHECK(SetKeyboardFocus);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&h",
	                      WinObj_Convert, &inWindow,
	                      CtlObj_Convert, &inControl,
	                      &inPart))
		return NULL;
	_err = SetKeyboardFocus(inWindow,
	                        inControl,
	                        inPart);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *Ctl_AdvanceKeyboardFocus(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	WindowPtr inWindow;
#ifndef AdvanceKeyboardFocus
	PyMac_PRECHECK(AdvanceKeyboardFocus);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      WinObj_Convert, &inWindow))
		return NULL;
	_err = AdvanceKeyboardFocus(inWindow);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *Ctl_ReverseKeyboardFocus(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	WindowPtr inWindow;
#ifndef ReverseKeyboardFocus
	PyMac_PRECHECK(ReverseKeyboardFocus);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      WinObj_Convert, &inWindow))
		return NULL;
	_err = ReverseKeyboardFocus(inWindow);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

static PyObject *Ctl_ClearKeyboardFocus(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSErr _err;
	WindowPtr inWindow;
#ifndef ClearKeyboardFocus
	PyMac_PRECHECK(ClearKeyboardFocus);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      WinObj_Convert, &inWindow))
		return NULL;
	_err = ClearKeyboardFocus(inWindow);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}

#if TARGET_API_MAC_CARBON

static PyObject *Ctl_SetAutomaticControlDragTrackingEnabledForWindow(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr theWindow;
	Boolean tracks;
#ifndef SetAutomaticControlDragTrackingEnabledForWindow
	PyMac_PRECHECK(SetAutomaticControlDragTrackingEnabledForWindow);
#endif
	if (!PyArg_ParseTuple(_args, "O&b",
	                      WinObj_Convert, &theWindow,
	                      &tracks))
		return NULL;
	_err = SetAutomaticControlDragTrackingEnabledForWindow(theWindow,
	                                                       tracks);
	if (_err != noErr) return PyMac_Error(_err);
	Py_INCREF(Py_None);
	_res = Py_None;
	return _res;
}
#endif

#if TARGET_API_MAC_CARBON

static PyObject *Ctl_IsAutomaticControlDragTrackingEnabledForWindow(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr theWindow;
	Boolean tracks;
#ifndef IsAutomaticControlDragTrackingEnabledForWindow
	PyMac_PRECHECK(IsAutomaticControlDragTrackingEnabledForWindow);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      WinObj_Convert, &theWindow))
		return NULL;
	_err = IsAutomaticControlDragTrackingEnabledForWindow(theWindow,
	                                                      &tracks);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("b",
	                     tracks);
	return _res;
}
#endif

static PyObject *Ctl_CreateDisclosureTriangleControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	UInt16 orientation;
	CFStringRef title;
	SInt32 initialValue;
	Boolean drawTitle;
	Boolean autoToggles;
	ControlHandle outControl;
#ifndef CreateDisclosureTriangleControl
	PyMac_PRECHECK(CreateDisclosureTriangleControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&HO&lbb",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      &orientation,
	                      CFStringRefObj_Convert, &title,
	                      &initialValue,
	                      &drawTitle,
	                      &autoToggles))
		return NULL;
	_err = CreateDisclosureTriangleControl(window,
	                                       &boundsRect,
	                                       orientation,
	                                       title,
	                                       initialValue,
	                                       drawTitle,
	                                       autoToggles,
	                                       &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateProgressBarControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	SInt32 value;
	SInt32 minimum;
	SInt32 maximum;
	Boolean indeterminate;
	ControlHandle outControl;
#ifndef CreateProgressBarControl
	PyMac_PRECHECK(CreateProgressBarControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&lllb",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      &value,
	                      &minimum,
	                      &maximum,
	                      &indeterminate))
		return NULL;
	_err = CreateProgressBarControl(window,
	                                &boundsRect,
	                                value,
	                                minimum,
	                                maximum,
	                                indeterminate,
	                                &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateLittleArrowsControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	SInt32 value;
	SInt32 minimum;
	SInt32 maximum;
	SInt32 increment;
	ControlHandle outControl;
#ifndef CreateLittleArrowsControl
	PyMac_PRECHECK(CreateLittleArrowsControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&llll",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      &value,
	                      &minimum,
	                      &maximum,
	                      &increment))
		return NULL;
	_err = CreateLittleArrowsControl(window,
	                                 &boundsRect,
	                                 value,
	                                 minimum,
	                                 maximum,
	                                 increment,
	                                 &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateChasingArrowsControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	ControlHandle outControl;
#ifndef CreateChasingArrowsControl
	PyMac_PRECHECK(CreateChasingArrowsControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect))
		return NULL;
	_err = CreateChasingArrowsControl(window,
	                                  &boundsRect,
	                                  &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateSeparatorControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	ControlHandle outControl;
#ifndef CreateSeparatorControl
	PyMac_PRECHECK(CreateSeparatorControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect))
		return NULL;
	_err = CreateSeparatorControl(window,
	                              &boundsRect,
	                              &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateGroupBoxControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	CFStringRef title;
	Boolean primary;
	ControlHandle outControl;
#ifndef CreateGroupBoxControl
	PyMac_PRECHECK(CreateGroupBoxControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&b",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      CFStringRefObj_Convert, &title,
	                      &primary))
		return NULL;
	_err = CreateGroupBoxControl(window,
	                             &boundsRect,
	                             title,
	                             primary,
	                             &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateCheckGroupBoxControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	CFStringRef title;
	SInt32 initialValue;
	Boolean primary;
	Boolean autoToggle;
	ControlHandle outControl;
#ifndef CreateCheckGroupBoxControl
	PyMac_PRECHECK(CreateCheckGroupBoxControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&lbb",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      CFStringRefObj_Convert, &title,
	                      &initialValue,
	                      &primary,
	                      &autoToggle))
		return NULL;
	_err = CreateCheckGroupBoxControl(window,
	                                  &boundsRect,
	                                  title,
	                                  initialValue,
	                                  primary,
	                                  autoToggle,
	                                  &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreatePopupGroupBoxControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	CFStringRef title;
	Boolean primary;
	SInt16 menuID;
	Boolean variableWidth;
	SInt16 titleWidth;
	SInt16 titleJustification;
	Style titleStyle;
	ControlHandle outControl;
#ifndef CreatePopupGroupBoxControl
	PyMac_PRECHECK(CreatePopupGroupBoxControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&bhbhhb",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      CFStringRefObj_Convert, &title,
	                      &primary,
	                      &menuID,
	                      &variableWidth,
	                      &titleWidth,
	                      &titleJustification,
	                      &titleStyle))
		return NULL;
	_err = CreatePopupGroupBoxControl(window,
	                                  &boundsRect,
	                                  title,
	                                  primary,
	                                  menuID,
	                                  variableWidth,
	                                  titleWidth,
	                                  titleJustification,
	                                  titleStyle,
	                                  &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreatePopupArrowControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	UInt16 orientation;
	UInt16 size;
	ControlHandle outControl;
#ifndef CreatePopupArrowControl
	PyMac_PRECHECK(CreatePopupArrowControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&HH",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      &orientation,
	                      &size))
		return NULL;
	_err = CreatePopupArrowControl(window,
	                               &boundsRect,
	                               orientation,
	                               size,
	                               &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreatePlacardControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	ControlHandle outControl;
#ifndef CreatePlacardControl
	PyMac_PRECHECK(CreatePlacardControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect))
		return NULL;
	_err = CreatePlacardControl(window,
	                            &boundsRect,
	                            &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateClockControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	UInt16 clockType;
	UInt32 clockFlags;
	ControlHandle outControl;
#ifndef CreateClockControl
	PyMac_PRECHECK(CreateClockControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&Hl",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      &clockType,
	                      &clockFlags))
		return NULL;
	_err = CreateClockControl(window,
	                          &boundsRect,
	                          clockType,
	                          clockFlags,
	                          &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateUserPaneControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	UInt32 features;
	ControlHandle outControl;
#ifndef CreateUserPaneControl
	PyMac_PRECHECK(CreateUserPaneControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&l",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      &features))
		return NULL;
	_err = CreateUserPaneControl(window,
	                             &boundsRect,
	                             features,
	                             &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateEditTextControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	CFStringRef text;
	Boolean isPassword;
	Boolean useInlineInput;
	ControlFontStyleRec style;
	ControlHandle outControl;
#ifndef CreateEditTextControl
	PyMac_PRECHECK(CreateEditTextControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&bbO&",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      CFStringRefObj_Convert, &text,
	                      &isPassword,
	                      &useInlineInput,
	                      ControlFontStyle_Convert, &style))
		return NULL;
	_err = CreateEditTextControl(window,
	                             &boundsRect,
	                             text,
	                             isPassword,
	                             useInlineInput,
	                             &style,
	                             &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateStaticTextControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	CFStringRef text;
	ControlFontStyleRec style;
	ControlHandle outControl;
#ifndef CreateStaticTextControl
	PyMac_PRECHECK(CreateStaticTextControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&O&",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      CFStringRefObj_Convert, &text,
	                      ControlFontStyle_Convert, &style))
		return NULL;
	_err = CreateStaticTextControl(window,
	                               &boundsRect,
	                               text,
	                               &style,
	                               &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateWindowHeaderControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	Boolean isListHeader;
	ControlHandle outControl;
#ifndef CreateWindowHeaderControl
	PyMac_PRECHECK(CreateWindowHeaderControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&b",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      &isListHeader))
		return NULL;
	_err = CreateWindowHeaderControl(window,
	                                 &boundsRect,
	                                 isListHeader,
	                                 &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreatePushButtonControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	CFStringRef title;
	ControlHandle outControl;
#ifndef CreatePushButtonControl
	PyMac_PRECHECK(CreatePushButtonControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      CFStringRefObj_Convert, &title))
		return NULL;
	_err = CreatePushButtonControl(window,
	                               &boundsRect,
	                               title,
	                               &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateRadioButtonControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	CFStringRef title;
	SInt32 initialValue;
	Boolean autoToggle;
	ControlHandle outControl;
#ifndef CreateRadioButtonControl
	PyMac_PRECHECK(CreateRadioButtonControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&lb",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      CFStringRefObj_Convert, &title,
	                      &initialValue,
	                      &autoToggle))
		return NULL;
	_err = CreateRadioButtonControl(window,
	                                &boundsRect,
	                                title,
	                                initialValue,
	                                autoToggle,
	                                &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateCheckBoxControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	CFStringRef title;
	SInt32 initialValue;
	Boolean autoToggle;
	ControlHandle outControl;
#ifndef CreateCheckBoxControl
	PyMac_PRECHECK(CreateCheckBoxControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&lb",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      CFStringRefObj_Convert, &title,
	                      &initialValue,
	                      &autoToggle))
		return NULL;
	_err = CreateCheckBoxControl(window,
	                             &boundsRect,
	                             title,
	                             initialValue,
	                             autoToggle,
	                             &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreatePopupButtonControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	CFStringRef title;
	SInt16 menuID;
	Boolean variableWidth;
	SInt16 titleWidth;
	SInt16 titleJustification;
	Style titleStyle;
	ControlHandle outControl;
#ifndef CreatePopupButtonControl
	PyMac_PRECHECK(CreatePopupButtonControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&hbhhb",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      CFStringRefObj_Convert, &title,
	                      &menuID,
	                      &variableWidth,
	                      &titleWidth,
	                      &titleJustification,
	                      &titleStyle))
		return NULL;
	_err = CreatePopupButtonControl(window,
	                                &boundsRect,
	                                title,
	                                menuID,
	                                variableWidth,
	                                titleWidth,
	                                titleJustification,
	                                titleStyle,
	                                &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateRadioGroupControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	ControlHandle outControl;
#ifndef CreateRadioGroupControl
	PyMac_PRECHECK(CreateRadioGroupControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect))
		return NULL;
	_err = CreateRadioGroupControl(window,
	                               &boundsRect,
	                               &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateScrollingTextBoxControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	SInt16 contentResID;
	Boolean autoScroll;
	UInt32 delayBeforeAutoScroll;
	UInt32 delayBetweenAutoScroll;
	UInt16 autoScrollAmount;
	ControlHandle outControl;
#ifndef CreateScrollingTextBoxControl
	PyMac_PRECHECK(CreateScrollingTextBoxControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&hbllH",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      &contentResID,
	                      &autoScroll,
	                      &delayBeforeAutoScroll,
	                      &delayBetweenAutoScroll,
	                      &autoScrollAmount))
		return NULL;
	_err = CreateScrollingTextBoxControl(window,
	                                     &boundsRect,
	                                     contentResID,
	                                     autoScroll,
	                                     delayBeforeAutoScroll,
	                                     delayBetweenAutoScroll,
	                                     autoScrollAmount,
	                                     &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_CreateDataBrowserControl(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	OSStatus _err;
	WindowPtr window;
	Rect boundsRect;
	OSType style;
	ControlHandle outControl;
#ifndef CreateDataBrowserControl
	PyMac_PRECHECK(CreateDataBrowserControl);
#endif
	if (!PyArg_ParseTuple(_args, "O&O&O&",
	                      WinObj_Convert, &window,
	                      PyMac_GetRect, &boundsRect,
	                      PyMac_GetOSType, &style))
		return NULL;
	_err = CreateDataBrowserControl(window,
	                                &boundsRect,
	                                style,
	                                &outControl);
	if (_err != noErr) return PyMac_Error(_err);
	_res = Py_BuildValue("O&",
	                     CtlObj_WhichControl, outControl);
	return _res;
}

static PyObject *Ctl_as_Control(PyObject *_self, PyObject *_args)
{
	PyObject *_res = NULL;
	ControlHandle _rv;
	Handle h;
#ifndef as_Control
	PyMac_PRECHECK(as_Control);
#endif
	if (!PyArg_ParseTuple(_args, "O&",
	                      ResObj_Convert, &h))
		return NULL;
	_rv = as_Control(h);
	_res = Py_BuildValue("O&",
	                     CtlObj_New, _rv);
	return _res;
}

static PyMethodDef Ctl_methods[] = {
	{"NewControl", (PyCFunction)Ctl_NewControl, 1,
	 "(WindowPtr owningWindow, Rect boundsRect, Str255 controlTitle, Boolean initiallyVisible, SInt16 initialValue, SInt16 minimumValue, SInt16 maximumValue, SInt16 procID, SInt32 controlReference) -> (ControlHandle _rv)"},
	{"GetNewControl", (PyCFunction)Ctl_GetNewControl, 1,
	 "(SInt16 resourceID, WindowPtr owningWindow) -> (ControlHandle _rv)"},
	{"DrawControls", (PyCFunction)Ctl_DrawControls, 1,
	 "(WindowPtr theWindow) -> None"},
	{"UpdateControls", (PyCFunction)Ctl_UpdateControls, 1,
	 "(WindowPtr theWindow, RgnHandle updateRegion) -> None"},
	{"FindControl", (PyCFunction)Ctl_FindControl, 1,
	 "(Point testPoint, WindowPtr theWindow) -> (ControlPartCode _rv, ControlHandle theControl)"},
	{"FindControlUnderMouse", (PyCFunction)Ctl_FindControlUnderMouse, 1,
	 "(Point inWhere, WindowPtr inWindow) -> (ControlHandle _rv, SInt16 outPart)"},
	{"IdleControls", (PyCFunction)Ctl_IdleControls, 1,
	 "(WindowPtr inWindow) -> None"},

#if TARGET_API_MAC_CARBON
	{"GetControlByID", (PyCFunction)Ctl_GetControlByID, 1,
	 "(WindowPtr inWindow, ControlID inID) -> (ControlHandle outControl)"},
#endif
	{"DumpControlHierarchy", (PyCFunction)Ctl_DumpControlHierarchy, 1,
	 "(WindowPtr inWindow, FSSpec inDumpFile) -> None"},
	{"CreateRootControl", (PyCFunction)Ctl_CreateRootControl, 1,
	 "(WindowPtr inWindow) -> (ControlHandle outControl)"},
	{"GetRootControl", (PyCFunction)Ctl_GetRootControl, 1,
	 "(WindowPtr inWindow) -> (ControlHandle outControl)"},
	{"GetKeyboardFocus", (PyCFunction)Ctl_GetKeyboardFocus, 1,
	 "(WindowPtr inWindow) -> (ControlHandle outControl)"},
	{"SetKeyboardFocus", (PyCFunction)Ctl_SetKeyboardFocus, 1,
	 "(WindowPtr inWindow, ControlHandle inControl, ControlFocusPart inPart) -> None"},
	{"AdvanceKeyboardFocus", (PyCFunction)Ctl_AdvanceKeyboardFocus, 1,
	 "(WindowPtr inWindow) -> None"},
	{"ReverseKeyboardFocus", (PyCFunction)Ctl_ReverseKeyboardFocus, 1,
	 "(WindowPtr inWindow) -> None"},
	{"ClearKeyboardFocus", (PyCFunction)Ctl_ClearKeyboardFocus, 1,
	 "(WindowPtr inWindow) -> None"},

#if TARGET_API_MAC_CARBON
	{"SetAutomaticControlDragTrackingEnabledForWindow", (PyCFunction)Ctl_SetAutomaticControlDragTrackingEnabledForWindow, 1,
	 "(WindowPtr theWindow, Boolean tracks) -> None"},
#endif

#if TARGET_API_MAC_CARBON
	{"IsAutomaticControlDragTrackingEnabledForWindow", (PyCFunction)Ctl_IsAutomaticControlDragTrackingEnabledForWindow, 1,
	 "(WindowPtr theWindow) -> (Boolean tracks)"},
#endif
	{"CreateDisclosureTriangleControl", (PyCFunction)Ctl_CreateDisclosureTriangleControl, 1,
	 "(WindowPtr window, Rect boundsRect, UInt16 orientation, CFStringRef title, SInt32 initialValue, Boolean drawTitle, Boolean autoToggles) -> (ControlHandle outControl)"},
	{"CreateProgressBarControl", (PyCFunction)Ctl_CreateProgressBarControl, 1,
	 "(WindowPtr window, Rect boundsRect, SInt32 value, SInt32 minimum, SInt32 maximum, Boolean indeterminate) -> (ControlHandle outControl)"},
	{"CreateLittleArrowsControl", (PyCFunction)Ctl_CreateLittleArrowsControl, 1,
	 "(WindowPtr window, Rect boundsRect, SInt32 value, SInt32 minimum, SInt32 maximum, SInt32 increment) -> (ControlHandle outControl)"},
	{"CreateChasingArrowsControl", (PyCFunction)Ctl_CreateChasingArrowsControl, 1,
	 "(WindowPtr window, Rect boundsRect) -> (ControlHandle outControl)"},
	{"CreateSeparatorControl", (PyCFunction)Ctl_CreateSeparatorControl, 1,
	 "(WindowPtr window, Rect boundsRect) -> (ControlHandle outControl)"},
	{"CreateGroupBoxControl", (PyCFunction)Ctl_CreateGroupBoxControl, 1,
	 "(WindowPtr window, Rect boundsRect, CFStringRef title, Boolean primary) -> (ControlHandle outControl)"},
	{"CreateCheckGroupBoxControl", (PyCFunction)Ctl_CreateCheckGroupBoxControl, 1,
	 "(WindowPtr window, Rect boundsRect, CFStringRef title, SInt32 initialValue, Boolean primary, Boolean autoToggle) -> (ControlHandle outControl)"},
	{"CreatePopupGroupBoxControl", (PyCFunction)Ctl_CreatePopupGroupBoxControl, 1,
	 "(WindowPtr window, Rect boundsRect, CFStringRef title, Boolean primary, SInt16 menuID, Boolean variableWidth, SInt16 titleWidth, SInt16 titleJustification, Style titleStyle) -> (ControlHandle outControl)"},
	{"CreatePopupArrowControl", (PyCFunction)Ctl_CreatePopupArrowControl, 1,
	 "(WindowPtr window, Rect boundsRect, UInt16 orientation, UInt16 size) -> (ControlHandle outControl)"},
	{"CreatePlacardControl", (PyCFunction)Ctl_CreatePlacardControl, 1,
	 "(WindowPtr window, Rect boundsRect) -> (ControlHandle outControl)"},
	{"CreateClockControl", (PyCFunction)Ctl_CreateClockControl, 1,
	 "(WindowPtr window, Rect boundsRect, UInt16 clockType, UInt32 clockFlags) -> (ControlHandle outControl)"},
	{"CreateUserPaneControl", (PyCFunction)Ctl_CreateUserPaneControl, 1,
	 "(WindowPtr window, Rect boundsRect, UInt32 features) -> (ControlHandle outControl)"},
	{"CreateEditTextControl", (PyCFunction)Ctl_CreateEditTextControl, 1,
	 "(WindowPtr window, Rect boundsRect, CFStringRef text, Boolean isPassword, Boolean useInlineInput, ControlFontStyleRec style) -> (ControlHandle outControl)"},
	{"CreateStaticTextControl", (PyCFunction)Ctl_CreateStaticTextControl, 1,
	 "(WindowPtr window, Rect boundsRect, CFStringRef text, ControlFontStyleRec style) -> (ControlHandle outControl)"},
	{"CreateWindowHeaderControl", (PyCFunction)Ctl_CreateWindowHeaderControl, 1,
	 "(WindowPtr window, Rect boundsRect, Boolean isListHeader) -> (ControlHandle outControl)"},
	{"CreatePushButtonControl", (PyCFunction)Ctl_CreatePushButtonControl, 1,
	 "(WindowPtr window, Rect boundsRect, CFStringRef title) -> (ControlHandle outControl)"},
	{"CreateRadioButtonControl", (PyCFunction)Ctl_CreateRadioButtonControl, 1,
	 "(WindowPtr window, Rect boundsRect, CFStringRef title, SInt32 initialValue, Boolean autoToggle) -> (ControlHandle outControl)"},
	{"CreateCheckBoxControl", (PyCFunction)Ctl_CreateCheckBoxControl, 1,
	 "(WindowPtr window, Rect boundsRect, CFStringRef title, SInt32 initialValue, Boolean autoToggle) -> (ControlHandle outControl)"},
	{"CreatePopupButtonControl", (PyCFunction)Ctl_CreatePopupButtonControl, 1,
	 "(WindowPtr window, Rect boundsRect, CFStringRef title, SInt16 menuID, Boolean variableWidth, SInt16 titleWidth, SInt16 titleJustification, Style titleStyle) -> (ControlHandle outControl)"},
	{"CreateRadioGroupControl", (PyCFunction)Ctl_CreateRadioGroupControl, 1,
	 "(WindowPtr window, Rect boundsRect) -> (ControlHandle outControl)"},
	{"CreateScrollingTextBoxControl", (PyCFunction)Ctl_CreateScrollingTextBoxControl, 1,
	 "(WindowPtr window, Rect boundsRect, SInt16 contentResID, Boolean autoScroll, UInt32 delayBeforeAutoScroll, UInt32 delayBetweenAutoScroll, UInt16 autoScrollAmount) -> (ControlHandle outControl)"},
	{"CreateDataBrowserControl", (PyCFunction)Ctl_CreateDataBrowserControl, 1,
	 "(WindowPtr window, Rect boundsRect, OSType style) -> (ControlHandle outControl)"},
	{"as_Control", (PyCFunction)Ctl_as_Control, 1,
	 "(Handle h) -> (ControlHandle _rv)"},
	{NULL, NULL, 0}
};



static PyObject *
CtlObj_NewUnmanaged(ControlHandle itself)
{
	ControlObject *it;
	if (itself == NULL) return PyMac_Error(resNotFound);
	it = PyObject_NEW(ControlObject, &Control_Type);
	if (it == NULL) return NULL;
	it->ob_itself = itself;
	it->ob_callbackdict = NULL;
	return (PyObject *)it;
}

static PyObject *
CtlObj_WhichControl(ControlHandle c)
{
	PyObject *it;

	if (c == NULL)
		it = Py_None;
	else {
		it = (PyObject *) GetControlReference(c);
		/*
		** If the refcon is zero or doesn't point back to the Python object
		** the control is not ours. Return a temporary object.
		*/
		if (it == NULL || ((ControlObject *)it)->ob_itself != c)
			return CtlObj_NewUnmanaged(c);
	}
	Py_INCREF(it);
	return it;
}

static int
settrackfunc(PyObject *obj)
{
	if (tracker) {
		PyErr_SetString(Ctl_Error, "Tracker function in use");
		return 0;
	}
	tracker = obj;
	Py_INCREF(tracker);
	return 1;
}

static void
clrtrackfunc(void)
{
	Py_XDECREF(tracker);
	tracker = 0;
}

static pascal void
mytracker(ControlHandle ctl, short part)
{
	PyObject *args, *rv=0;

	args = Py_BuildValue("(O&i)", CtlObj_WhichControl, ctl, (int)part);
	if (args && tracker) {
		rv = PyEval_CallObject(tracker, args);
		Py_DECREF(args);
	}
	if (rv)
		Py_DECREF(rv);
	else
		PySys_WriteStderr("TrackControl or HandleControlClick: exception in tracker function\n");
}

static int
setcallback(PyObject *myself, OSType which, PyObject *callback, UniversalProcPtr *uppp)
{
	ControlObject *self = (ControlObject *)myself;
	char keybuf[9];
	
	if ( which == kControlUserPaneDrawProcTag )
		*uppp = (UniversalProcPtr)mydrawproc_upp;
	else if ( which == kControlUserPaneIdleProcTag )
		*uppp = (UniversalProcPtr)myidleproc_upp;
	else if ( which == kControlUserPaneHitTestProcTag )
		*uppp = (UniversalProcPtr)myhittestproc_upp;
	else if ( which == kControlUserPaneTrackingProcTag )
		*uppp = (UniversalProcPtr)mytrackingproc_upp;
	else
		return -1;
	/* Only now do we test for clearing of the callback: */
	if ( callback == Py_None )
		*uppp = NULL;
	/* Create the dict if it doesn't exist yet (so we don't get such a dict for every control) */
	if ( self->ob_callbackdict == NULL )
		if ( (self->ob_callbackdict = PyDict_New()) == NULL )
			return -1;
	/* And store the Python callback */
	sprintf(keybuf, "%x", (unsigned)which);
	if (PyDict_SetItemString(self->ob_callbackdict, keybuf, callback) < 0)
		return -1;
	return 0;
}

static PyObject *
callcallback(ControlObject *self, OSType which, PyObject *arglist)
{
	char keybuf[9];
	PyObject *func, *rv;
	
	sprintf(keybuf, "%x", (unsigned)which);
	if ( self->ob_callbackdict == NULL ||
			(func = PyDict_GetItemString(self->ob_callbackdict, keybuf)) == NULL ) {
		PySys_WriteStderr("Control callback %x without callback object\n", (unsigned)which);
		return NULL;
	}
	rv = PyEval_CallObject(func, arglist);
	if ( rv == NULL )
		PySys_WriteStderr("Exception in control callback %x handler\n", (unsigned)which);
	return rv;
}

static pascal void
mydrawproc(ControlHandle control, SInt16 part)
{
	ControlObject *ctl_obj;
	PyObject *arglist, *rv;
	
	ctl_obj = (ControlObject *)CtlObj_WhichControl(control);
	arglist = Py_BuildValue("Oh", ctl_obj, part);
	rv = callcallback(ctl_obj, kControlUserPaneDrawProcTag, arglist);
	Py_XDECREF(arglist);
	Py_XDECREF(rv);
}

static pascal void
myidleproc(ControlHandle control)
{
	ControlObject *ctl_obj;
	PyObject *arglist, *rv;
	
	ctl_obj = (ControlObject *)CtlObj_WhichControl(control);
	arglist = Py_BuildValue("O", ctl_obj);
	rv = callcallback(ctl_obj, kControlUserPaneIdleProcTag, arglist);
	Py_XDECREF(arglist);
	Py_XDECREF(rv);
}

static pascal ControlPartCode
myhittestproc(ControlHandle control, Point where)
{
	ControlObject *ctl_obj;
	PyObject *arglist, *rv;
	short c_rv = -1;

	ctl_obj = (ControlObject *)CtlObj_WhichControl(control);
	arglist = Py_BuildValue("OO&", ctl_obj, PyMac_BuildPoint, where);
	rv = callcallback(ctl_obj, kControlUserPaneHitTestProcTag, arglist);
	Py_XDECREF(arglist);
	/* Ignore errors, nothing we can do about them */
	if ( rv )
		PyArg_Parse(rv, "h", &c_rv);
	Py_XDECREF(rv);
	return (ControlPartCode)c_rv;
}

static pascal ControlPartCode
mytrackingproc(ControlHandle control, Point startPt, ControlActionUPP actionProc)
{
	ControlObject *ctl_obj;
	PyObject *arglist, *rv;
	short c_rv = -1;

	ctl_obj = (ControlObject *)CtlObj_WhichControl(control);
	/* We cannot pass the actionProc without lots of work */
	arglist = Py_BuildValue("OO&", ctl_obj, PyMac_BuildPoint, startPt);
	rv = callcallback(ctl_obj, kControlUserPaneTrackingProcTag, arglist);
	Py_XDECREF(arglist);
	if ( rv )
		PyArg_Parse(rv, "h", &c_rv);
	Py_XDECREF(rv);
	return (ControlPartCode)c_rv;
}


void init_Ctl(void)
{
	PyObject *m;
	PyObject *d;



	mytracker_upp = NewControlActionUPP(mytracker);
	mydrawproc_upp = NewControlUserPaneDrawUPP(mydrawproc);
	myidleproc_upp = NewControlUserPaneIdleUPP(myidleproc);
	myhittestproc_upp = NewControlUserPaneHitTestUPP(myhittestproc);
	mytrackingproc_upp = NewControlUserPaneTrackingUPP(mytrackingproc);
	PyMac_INIT_TOOLBOX_OBJECT_NEW(ControlHandle, CtlObj_New);
	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(ControlHandle, CtlObj_Convert);


	m = Py_InitModule("_Ctl", Ctl_methods);
	d = PyModule_GetDict(m);
	Ctl_Error = PyMac_GetOSErrException();
	if (Ctl_Error == NULL ||
	    PyDict_SetItemString(d, "Error", Ctl_Error) != 0)
		return;
	Control_Type.ob_type = &PyType_Type;
	Py_INCREF(&Control_Type);
	if (PyDict_SetItemString(d, "ControlType", (PyObject *)&Control_Type) != 0)
		Py_FatalError("can't initialize ControlType");
}

/* ======================== End module _Ctl ========================= */

