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

/* Signal module -- many thanks to Lance Ellinghaus */

/* XXX Signals should be recorded per thread, now we have thread state. */

#include "Python.h"
#include "intrcheck.h"

#ifdef MS_WIN32
#include <process.h>
#endif

#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif

#include <signal.h>

#ifndef SIG_ERR
#define SIG_ERR ((RETSIGTYPE (*)())-1)
#endif

#ifndef NSIG
#ifdef _SIGMAX
#define NSIG (_SIGMAX + 1)	/* For QNX */
#else
#define NSIG (SIGMAX + 1)	/* for djgpp */
#endif
#endif



/*
   NOTES ON THE INTERACTION BETWEEN SIGNALS AND THREADS

   When threads are supported, we want the following semantics:

   - only the main thread can set a signal handler
   - any thread can get a signal handler
   - signals are only delivered to the main thread

   I.e. we don't support "synchronous signals" like SIGFPE (catching
   this doesn't make much sense in Python anyway) nor do we support
   signals as a means of inter-thread communication, since not all
   thread implementations support that (at least our thread library
   doesn't).

   We still have the problem that in some implementations signals
   generated by the keyboard (e.g. SIGINT) are delivered to all
   threads (e.g. SGI), while in others (e.g. Solaris) such signals are
   delivered to one random thread (an intermediate possibility would
   be to deliver it to the main thread -- POSIX?).  For now, we have
   a working implementation that works in all three cases -- the
   handler ignores signals if getpid() isn't the same as in the main
   thread.  XXX This is a hack.

*/

#ifdef WITH_THREAD
#include <sys/types.h> /* For pid_t */
#include "thread.h"
static long main_thread;
static pid_t main_pid;
#endif

static struct {
        int tripped;
        PyObject *func;
} Handlers[NSIG];

static int is_tripped = 0; /* Speed up sigcheck() when none tripped */

static PyObject *DefaultHandler;
static PyObject *IgnoreHandler;
static PyObject *IntHandler;

static RETSIGTYPE (*old_siginthandler)() = SIG_DFL;



static PyObject *
signal_default_int_handler(self, arg)
	PyObject *self;
	PyObject *arg;
{
	PyErr_SetNone(PyExc_KeyboardInterrupt);
	return NULL;
}


static RETSIGTYPE
signal_handler(sig_num)
	int sig_num;
{
#ifdef WITH_THREAD
	/* See NOTES section above */
	if (getpid() == main_pid) {
#endif
		is_tripped++;
		Handlers[sig_num].tripped = 1;
		Py_AddPendingCall(
			(int (*) Py_PROTO((ANY *)))PyErr_CheckSignals, NULL);
#ifdef WITH_THREAD
	}
#endif
#ifdef SIGCHLD
	if (sig_num == SIGCHLD) {
		/* To avoid infinite recursion, this signal remains
		   reset until explicit re-instated.
		   Don't clear the 'func' field as it is our pointer
		   to the Python handler... */
		return;
	}
#endif
	(void *)signal(sig_num, &signal_handler);
}



#ifdef HAVE_ALARM
static PyObject *
signal_alarm(self, args)
	PyObject *self; /* Not used */
	PyObject *args;
{
	int t;
	if (!PyArg_Parse(args, "i", &t))
		return NULL;
	/* alarm() returns the number of seconds remaining */
	return PyInt_FromLong(alarm(t));
}
#endif

#ifdef HAVE_PAUSE
static PyObject *
signal_pause(self, args)
	PyObject *self; /* Not used */
	PyObject *args;
{
	if (!PyArg_NoArgs(args))
		return NULL;

	Py_BEGIN_ALLOW_THREADS
	(void)pause();
	Py_END_ALLOW_THREADS
	/* make sure that any exceptions that got raised are propagated
	 * back into Python
	 */
	if (PyErr_CheckSignals())
		return NULL;

	Py_INCREF(Py_None);
	return Py_None;
}
#endif


static PyObject *
signal_signal(self, args)
	PyObject *self; /* Not used */
	PyObject *args;
{
	PyObject *obj;
	int sig_num;
	PyObject *old_handler;
	RETSIGTYPE (*func)();
	if (!PyArg_Parse(args, "(iO)", &sig_num, &obj))
		return NULL;
#ifdef WITH_THREAD
	if (get_thread_ident() != main_thread) {
		PyErr_SetString(PyExc_ValueError,
				"signal only works in main thread");
		return NULL;
	}
#endif
	if (sig_num < 1 || sig_num >= NSIG) {
		PyErr_SetString(PyExc_ValueError,
				"signal number out of range");
		return NULL;
	}
	if (obj == IgnoreHandler)
		func = SIG_IGN;
	else if (obj == DefaultHandler)
		func = SIG_DFL;
	else if (!PyCallable_Check(obj)) {
		PyErr_SetString(PyExc_TypeError,
"signal handler must be signal.SIG_IGN, signal.SIG_DFL, or a callable object");
		return NULL;
	}
	else
		func = signal_handler;
	if (signal(sig_num, func) == SIG_ERR) {
		PyErr_SetFromErrno(PyExc_RuntimeError);
		return NULL;
	}
	old_handler = Handlers[sig_num].func;
	Handlers[sig_num].tripped = 0;
	Py_INCREF(obj);
	Handlers[sig_num].func = obj;
	return old_handler;
}


static PyObject *
signal_get_signal(self, args)
	PyObject *self; /* Not used */
	PyObject *args;
{
	int sig_num;
	PyObject *old_handler;
	if (!PyArg_Parse(args, "i", &sig_num))
		return NULL;
	if (sig_num < 1 || sig_num >= NSIG) {
		PyErr_SetString(PyExc_ValueError,
				"signal number out of range");
		return NULL;
	}
	old_handler = Handlers[sig_num].func;
	Py_INCREF(old_handler);
	return old_handler;
}



/* List of functions defined in the module */
static PyMethodDef signal_methods[] = {
#ifdef HAVE_ALARM
	{"alarm",	        signal_alarm},
#endif
	{"signal",	        signal_signal},
	{"getsignal",	        signal_get_signal},
#ifdef HAVE_PAUSE
	{"pause",	        signal_pause},
#endif
	{"default_int_handler", signal_default_int_handler},
	{NULL,		NULL}		/* sentinel */
};



void
initsignal()
{
	PyObject *m, *d, *x;
	int i;

#ifdef WITH_THREAD
	main_thread = get_thread_ident();
	main_pid = getpid();
#endif

	/* Create the module and add the functions */
	m = Py_InitModule("signal", signal_methods);

	/* Add some symbolic constants to the module */
	d = PyModule_GetDict(m);

	x = DefaultHandler = PyInt_FromLong((long)SIG_DFL);
        if (!x || PyDict_SetItemString(d, "SIG_DFL", x) < 0)
                goto finally;

	x = IgnoreHandler = PyInt_FromLong((long)SIG_IGN);
        if (!x || PyDict_SetItemString(d, "SIG_IGN", x) < 0)
                goto finally;

        x = PyInt_FromLong((long)NSIG);
        if (!x || PyDict_SetItemString(d, "NSIG", x) < 0)
                goto finally;
        Py_DECREF(x);

	x = IntHandler = PyDict_GetItemString(d, "default_int_handler");
        if (!x)
                goto finally;
	Py_INCREF(IntHandler);

	Handlers[0].tripped = 0;
	for (i = 1; i < NSIG; i++) {
		RETSIGTYPE (*t)();
#ifdef HAVE_SIGACTION
		struct sigaction act;
		sigaction(i,  0, &act);
		t = act.sa_handler;
#else
		t = signal(i, SIG_IGN);
		signal(i, t);
#endif
		Handlers[i].tripped = 0;
		if (t == SIG_DFL)
			Handlers[i].func = DefaultHandler;
		else if (t == SIG_IGN)
			Handlers[i].func = IgnoreHandler;
		else
			Handlers[i].func = Py_None; /* None of our business */
		Py_INCREF(Handlers[i].func);
	}
	if (Handlers[SIGINT].func == DefaultHandler) {
		/* Install default int handler */
		Py_INCREF(IntHandler);
		Py_DECREF(Handlers[SIGINT].func);
		Handlers[SIGINT].func = IntHandler;
		old_siginthandler = signal(SIGINT, &signal_handler);
	}

#ifdef SIGHUP
	x = PyInt_FromLong(SIGHUP);
	PyDict_SetItemString(d, "SIGHUP", x);
        Py_XDECREF(x);
#endif
#ifdef SIGINT
	x = PyInt_FromLong(SIGINT);
	PyDict_SetItemString(d, "SIGINT", x);
        Py_XDECREF(x);
#endif
#ifdef SIGQUIT
	x = PyInt_FromLong(SIGQUIT);
	PyDict_SetItemString(d, "SIGQUIT", x);
        Py_XDECREF(x);
#endif
#ifdef SIGILL
	x = PyInt_FromLong(SIGILL);
	PyDict_SetItemString(d, "SIGILL", x);
        Py_XDECREF(x);
#endif
#ifdef SIGTRAP
	x = PyInt_FromLong(SIGTRAP);
	PyDict_SetItemString(d, "SIGTRAP", x);
        Py_XDECREF(x);
#endif
#ifdef SIGIOT
	x = PyInt_FromLong(SIGIOT);
	PyDict_SetItemString(d, "SIGIOT", x);
        Py_XDECREF(x);
#endif
#ifdef SIGABRT
	x = PyInt_FromLong(SIGABRT);
	PyDict_SetItemString(d, "SIGABRT", x);
        Py_XDECREF(x);
#endif
#ifdef SIGEMT
	x = PyInt_FromLong(SIGEMT);
	PyDict_SetItemString(d, "SIGEMT", x);
        Py_XDECREF(x);
#endif
#ifdef SIGFPE
	x = PyInt_FromLong(SIGFPE);
	PyDict_SetItemString(d, "SIGFPE", x);
        Py_XDECREF(x);
#endif
#ifdef SIGKILL
	x = PyInt_FromLong(SIGKILL);
	PyDict_SetItemString(d, "SIGKILL", x);
        Py_XDECREF(x);
#endif
#ifdef SIGBUS
	x = PyInt_FromLong(SIGBUS);
	PyDict_SetItemString(d, "SIGBUS", x);
        Py_XDECREF(x);
#endif
#ifdef SIGSEGV
	x = PyInt_FromLong(SIGSEGV);
	PyDict_SetItemString(d, "SIGSEGV", x);
        Py_XDECREF(x);
#endif
#ifdef SIGSYS
	x = PyInt_FromLong(SIGSYS);
	PyDict_SetItemString(d, "SIGSYS", x);
        Py_XDECREF(x);
#endif
#ifdef SIGPIPE
	x = PyInt_FromLong(SIGPIPE);
	PyDict_SetItemString(d, "SIGPIPE", x);
        Py_XDECREF(x);
#endif
#ifdef SIGALRM
	x = PyInt_FromLong(SIGALRM);
	PyDict_SetItemString(d, "SIGALRM", x);
        Py_XDECREF(x);
#endif
#ifdef SIGTERM
	x = PyInt_FromLong(SIGTERM);
	PyDict_SetItemString(d, "SIGTERM", x);
        Py_XDECREF(x);
#endif
#ifdef SIGUSR1
	x = PyInt_FromLong(SIGUSR1);
	PyDict_SetItemString(d, "SIGUSR1", x);
        Py_XDECREF(x);
#endif
#ifdef SIGUSR2
	x = PyInt_FromLong(SIGUSR2);
	PyDict_SetItemString(d, "SIGUSR2", x);
        Py_XDECREF(x);
#endif
#ifdef SIGCLD
	x = PyInt_FromLong(SIGCLD);
	PyDict_SetItemString(d, "SIGCLD", x);
        Py_XDECREF(x);
#endif
#ifdef SIGCHLD
	x = PyInt_FromLong(SIGCHLD);
	PyDict_SetItemString(d, "SIGCHLD", x);
        Py_XDECREF(x);
#endif
#ifdef SIGPWR
	x = PyInt_FromLong(SIGPWR);
	PyDict_SetItemString(d, "SIGPWR", x);
        Py_XDECREF(x);
#endif
#ifdef SIGIO
	x = PyInt_FromLong(SIGIO);
	PyDict_SetItemString(d, "SIGIO", x);
        Py_XDECREF(x);
#endif
#ifdef SIGURG
	x = PyInt_FromLong(SIGURG);
	PyDict_SetItemString(d, "SIGURG", x);
        Py_XDECREF(x);
#endif
#ifdef SIGWINCH
	x = PyInt_FromLong(SIGWINCH);
	PyDict_SetItemString(d, "SIGWINCH", x);
        Py_XDECREF(x);
#endif
#ifdef SIGPOLL
	x = PyInt_FromLong(SIGPOLL);
	PyDict_SetItemString(d, "SIGPOLL", x);
        Py_XDECREF(x);
#endif
#ifdef SIGSTOP
	x = PyInt_FromLong(SIGSTOP);
	PyDict_SetItemString(d, "SIGSTOP", x);
        Py_XDECREF(x);
#endif
#ifdef SIGTSTP
	x = PyInt_FromLong(SIGTSTP);
	PyDict_SetItemString(d, "SIGTSTP", x);
        Py_XDECREF(x);
#endif
#ifdef SIGCONT
	x = PyInt_FromLong(SIGCONT);
	PyDict_SetItemString(d, "SIGCONT", x);
        Py_XDECREF(x);
#endif
#ifdef SIGTTIN
	x = PyInt_FromLong(SIGTTIN);
	PyDict_SetItemString(d, "SIGTTIN", x);
        Py_XDECREF(x);
#endif
#ifdef SIGTTOU
	x = PyInt_FromLong(SIGTTOU);
	PyDict_SetItemString(d, "SIGTTOU", x);
        Py_XDECREF(x);
#endif
#ifdef SIGVTALRM
	x = PyInt_FromLong(SIGVTALRM);
	PyDict_SetItemString(d, "SIGVTALRM", x);
        Py_XDECREF(x);
#endif
#ifdef SIGPROF
	x = PyInt_FromLong(SIGPROF);
	PyDict_SetItemString(d, "SIGPROF", x);
        Py_XDECREF(x);
#endif
#ifdef SIGXCPU
	x = PyInt_FromLong(SIGXCPU);
	PyDict_SetItemString(d, "SIGXCPU", x);
        Py_XDECREF(x);
#endif
#ifdef SIGXFSZ
	x = PyInt_FromLong(SIGXFSZ);
	PyDict_SetItemString(d, "SIGXFSZ", x);
        Py_XDECREF(x);
#endif
        if (!PyErr_Occurred())
                return;

	/* Check for errors */
  finally:
        return;
}

static void
finisignal()
{
	int i;

	signal(SIGINT, old_siginthandler);

	for (i = 1; i < NSIG; i++) {
		Handlers[i].tripped = 0;
		Py_XDECREF(Handlers[i].func);
		Handlers[i].func = NULL;
	}

	Py_XDECREF(IntHandler);
	IntHandler = NULL;
	Py_XDECREF(DefaultHandler);
	DefaultHandler = NULL;
	Py_XDECREF(IgnoreHandler);
	IgnoreHandler = NULL;
}



/* Declared in pyerrors.h */
int
PyErr_CheckSignals()
{
	int i;
	PyObject *f;

	if (!is_tripped)
		return 0;
#ifdef WITH_THREAD
	if (get_thread_ident() != main_thread)
		return 0;
#endif
	if (!(f = PyEval_GetFrame()))
		f = Py_None;
	
	for (i = 1; i < NSIG; i++) {
		if (Handlers[i].tripped) {
			PyObject *result = NULL;
			PyObject *arglist = Py_BuildValue("(iO)", i, f);
			Handlers[i].tripped = 0;

			if (arglist) {
				result = PyEval_CallObject(Handlers[i].func,
							   arglist);
				Py_DECREF(arglist);
			}
			if (!result)
				return -1;

			Py_DECREF(result);
		}
	}
	is_tripped = 0;
	return 0;
}


/* Replacements for intrcheck.c functionality
 * Declared in pyerrors.h
 */
void
PyErr_SetInterrupt()
{
	is_tripped++;
	Handlers[SIGINT].tripped = 1;
	Py_AddPendingCall((int (*) Py_PROTO((ANY *)))PyErr_CheckSignals, NULL);
}

void
PyOS_InitInterrupts()
{
	initsignal();
	_PyImport_FixupExtension("signal", "signal");
}

void
PyOS_FiniInterrupts()
{
	finisignal();
}

int
PyOS_InterruptOccurred()
{
	if (Handlers[SIGINT].tripped) {
#ifdef WITH_THREAD
		if (get_thread_ident() != main_thread)
			return 0;
#endif
		Handlers[SIGINT].tripped = 0;
		return 1;
	}
	return 0;
}
