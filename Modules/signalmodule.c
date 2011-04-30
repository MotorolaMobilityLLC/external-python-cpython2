
/* Signal module -- many thanks to Lance Ellinghaus */

/* XXX Signals should be recorded per thread, now we have thread state. */

#include "Python.h"

#ifdef MS_WINDOWS
#include <Windows.h>
#ifdef HAVE_PROCESS_H
#include <process.h>
#endif
#endif

#ifdef HAVE_SIGNAL_H
#include <signal.h>
#endif
#ifdef HAVE_SYS_STAT_H
#include <sys/stat.h>
#endif
#ifdef HAVE_SYS_TIME_H
#include <sys/time.h>
#endif

#if defined(HAVE_PTHREAD_SIGMASK) && !defined(HAVE_BROKEN_PTHREAD_SIGMASK)
#  define PYPTHREAD_SIGMASK
#endif

#if defined(PYPTHREAD_SIGMASK) && defined(HAVE_PTHREAD_H)
#  include <pthread.h>
#endif

#ifndef SIG_ERR
#define SIG_ERR ((PyOS_sighandler_t)(-1))
#endif

#if defined(PYOS_OS2) && !defined(PYCC_GCC)
#define NSIG 12
#include <process.h>
#endif

#ifndef NSIG
# if defined(_NSIG)
#  define NSIG _NSIG            /* For BSD/SysV */
# elif defined(_SIGMAX)
#  define NSIG (_SIGMAX + 1)    /* For QNX */
# elif defined(SIGMAX)
#  define NSIG (SIGMAX + 1)     /* For djgpp */
# else
#  define NSIG 64               /* Use a reasonable default value */
# endif
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

   GNU pth is a user-space threading library, and as such, all threads
   run within the same process. In this case, if the currently running
   thread is not the main_thread, send the signal to the main_thread.
*/

#ifdef WITH_THREAD
#include <sys/types.h> /* For pid_t */
#include "pythread.h"
static long main_thread;
static pid_t main_pid;
#endif

static struct {
    int tripped;
    PyObject *func;
} Handlers[NSIG];

static sig_atomic_t wakeup_fd = -1;

/* Speed up sigcheck() when none tripped */
static volatile sig_atomic_t is_tripped = 0;

static PyObject *DefaultHandler;
static PyObject *IgnoreHandler;
static PyObject *IntHandler;

/* On Solaris 8, gcc will produce a warning that the function
   declaration is not a prototype. This is caused by the definition of
   SIG_DFL as (void (*)())0; the correct declaration would have been
   (void (*)(int))0. */

static PyOS_sighandler_t old_siginthandler = SIG_DFL;

#ifdef HAVE_GETITIMER
static PyObject *ItimerError;

/* auxiliary functions for setitimer/getitimer */
static void
timeval_from_double(double d, struct timeval *tv)
{
    tv->tv_sec = floor(d);
    tv->tv_usec = fmod(d, 1.0) * 1000000.0;
}

Py_LOCAL_INLINE(double)
double_from_timeval(struct timeval *tv)
{
    return tv->tv_sec + (double)(tv->tv_usec / 1000000.0);
}

static PyObject *
itimer_retval(struct itimerval *iv)
{
    PyObject *r, *v;

    r = PyTuple_New(2);
    if (r == NULL)
    return NULL;

    if(!(v = PyFloat_FromDouble(double_from_timeval(&iv->it_value)))) {
    Py_DECREF(r);
    return NULL;
    }

    PyTuple_SET_ITEM(r, 0, v);

    if(!(v = PyFloat_FromDouble(double_from_timeval(&iv->it_interval)))) {
    Py_DECREF(r);
    return NULL;
    }

    PyTuple_SET_ITEM(r, 1, v);

    return r;
}
#endif

static PyObject *
signal_default_int_handler(PyObject *self, PyObject *args)
{
    PyErr_SetNone(PyExc_KeyboardInterrupt);
    return NULL;
}

PyDoc_STRVAR(default_int_handler_doc,
"default_int_handler(...)\n\
\n\
The default handler for SIGINT installed by Python.\n\
It raises KeyboardInterrupt.");


static int
checksignals_witharg(void * unused)
{
    return PyErr_CheckSignals();
}

static void
trip_signal(int sig_num)
{
    Handlers[sig_num].tripped = 1;
    if (is_tripped)
        return;
    /* Set is_tripped after setting .tripped, as it gets
       cleared in PyErr_CheckSignals() before .tripped. */
    is_tripped = 1;
    Py_AddPendingCall(checksignals_witharg, NULL);
    if (wakeup_fd != -1)
        write(wakeup_fd, "\0", 1);
}

static void
signal_handler(int sig_num)
{
    int save_errno = errno;

#if defined(WITH_THREAD) && defined(WITH_PTH)
    if (PyThread_get_thread_ident() != main_thread) {
        pth_raise(*(pth_t *) main_thread, sig_num);
    }
    else
#endif
    {
#ifdef WITH_THREAD
    /* See NOTES section above */
    if (getpid() == main_pid)
#endif
    {
        trip_signal(sig_num);
    }

#ifndef HAVE_SIGACTION
#ifdef SIGCHLD
    /* To avoid infinite recursion, this signal remains
       reset until explicit re-instated.
       Don't clear the 'func' field as it is our pointer
       to the Python handler... */
    if (sig_num != SIGCHLD)
#endif
    /* If the handler was not set up with sigaction, reinstall it.  See
     * Python/pythonrun.c for the implementation of PyOS_setsig which
     * makes this true.  See also issue8354. */
    PyOS_setsig(sig_num, signal_handler);
#endif
    }

    /* Issue #10311: asynchronously executing signal handlers should not
       mutate errno under the feet of unsuspecting C code. */
    errno = save_errno;
}


#ifdef HAVE_ALARM
static PyObject *
signal_alarm(PyObject *self, PyObject *args)
{
    int t;
    if (!PyArg_ParseTuple(args, "i:alarm", &t))
        return NULL;
    /* alarm() returns the number of seconds remaining */
    return PyLong_FromLong((long)alarm(t));
}

PyDoc_STRVAR(alarm_doc,
"alarm(seconds)\n\
\n\
Arrange for SIGALRM to arrive after the given number of seconds.");
#endif

#ifdef HAVE_PAUSE
static PyObject *
signal_pause(PyObject *self)
{
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
PyDoc_STRVAR(pause_doc,
"pause()\n\
\n\
Wait until a signal arrives.");

#endif


static PyObject *
signal_signal(PyObject *self, PyObject *args)
{
    PyObject *obj;
    int sig_num;
    PyObject *old_handler;
    void (*func)(int);
    if (!PyArg_ParseTuple(args, "iO:signal", &sig_num, &obj))
        return NULL;
#ifdef MS_WINDOWS
    /* Validate that sig_num is one of the allowable signals */
    switch (sig_num) {
        case SIGABRT: break;
#ifdef SIGBREAK
        /* Issue #10003: SIGBREAK is not documented as permitted, but works
           and corresponds to CTRL_BREAK_EVENT. */
        case SIGBREAK: break;
#endif
        case SIGFPE: break;
        case SIGILL: break;
        case SIGINT: break;
        case SIGSEGV: break;
        case SIGTERM: break;
        default:
            PyErr_SetString(PyExc_ValueError, "invalid signal value");
            return NULL;
    }
#endif
#ifdef WITH_THREAD
    if (PyThread_get_thread_ident() != main_thread) {
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
    if (PyOS_setsig(sig_num, func) == SIG_ERR) {
        PyErr_SetFromErrno(PyExc_RuntimeError);
        return NULL;
    }
    old_handler = Handlers[sig_num].func;
    Handlers[sig_num].tripped = 0;
    Py_INCREF(obj);
    Handlers[sig_num].func = obj;
    return old_handler;
}

PyDoc_STRVAR(signal_doc,
"signal(sig, action) -> action\n\
\n\
Set the action for the given signal.  The action can be SIG_DFL,\n\
SIG_IGN, or a callable Python object.  The previous action is\n\
returned.  See getsignal() for possible return values.\n\
\n\
*** IMPORTANT NOTICE ***\n\
A signal handler function is called with two arguments:\n\
the first is the signal number, the second is the interrupted stack frame.");


static PyObject *
signal_getsignal(PyObject *self, PyObject *args)
{
    int sig_num;
    PyObject *old_handler;
    if (!PyArg_ParseTuple(args, "i:getsignal", &sig_num))
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

PyDoc_STRVAR(getsignal_doc,
"getsignal(sig) -> action\n\
\n\
Return the current action for the given signal.  The return value can be:\n\
SIG_IGN -- if the signal is being ignored\n\
SIG_DFL -- if the default action for the signal is in effect\n\
None -- if an unknown handler is in effect\n\
anything else -- the callable Python object used as a handler");

#ifdef HAVE_SIGINTERRUPT
PyDoc_STRVAR(siginterrupt_doc,
"siginterrupt(sig, flag) -> None\n\
change system call restart behaviour: if flag is False, system calls\n\
will be restarted when interrupted by signal sig, else system calls\n\
will be interrupted.");

static PyObject *
signal_siginterrupt(PyObject *self, PyObject *args)
{
    int sig_num;
    int flag;

    if (!PyArg_ParseTuple(args, "ii:siginterrupt", &sig_num, &flag))
        return NULL;
    if (sig_num < 1 || sig_num >= NSIG) {
        PyErr_SetString(PyExc_ValueError,
                        "signal number out of range");
        return NULL;
    }
    if (siginterrupt(sig_num, flag)<0) {
        PyErr_SetFromErrno(PyExc_RuntimeError);
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

#endif

static PyObject *
signal_set_wakeup_fd(PyObject *self, PyObject *args)
{
    struct stat buf;
    int fd, old_fd;
    if (!PyArg_ParseTuple(args, "i:set_wakeup_fd", &fd))
        return NULL;
#ifdef WITH_THREAD
    if (PyThread_get_thread_ident() != main_thread) {
        PyErr_SetString(PyExc_ValueError,
                        "set_wakeup_fd only works in main thread");
        return NULL;
    }
#endif
    if (fd != -1 && fstat(fd, &buf) != 0) {
        PyErr_SetString(PyExc_ValueError, "invalid fd");
        return NULL;
    }
    old_fd = wakeup_fd;
    wakeup_fd = fd;
    return PyLong_FromLong(old_fd);
}

PyDoc_STRVAR(set_wakeup_fd_doc,
"set_wakeup_fd(fd) -> fd\n\
\n\
Sets the fd to be written to (with '\\0') when a signal\n\
comes in.  A library can use this to wakeup select or poll.\n\
The previous fd is returned.\n\
\n\
The fd must be non-blocking.");

/* C API for the same, without all the error checking */
int
PySignal_SetWakeupFd(int fd)
{
    int old_fd = wakeup_fd;
    if (fd < 0)
        fd = -1;
    wakeup_fd = fd;
    return old_fd;
}


#ifdef HAVE_SETITIMER
static PyObject *
signal_setitimer(PyObject *self, PyObject *args)
{
    double first;
    double interval = 0;
    int which;
    struct itimerval new, old;

    if(!PyArg_ParseTuple(args, "id|d:setitimer", &which, &first, &interval))
    return NULL;

    timeval_from_double(first, &new.it_value);
    timeval_from_double(interval, &new.it_interval);
    /* Let OS check "which" value */
    if (setitimer(which, &new, &old) != 0) {
    PyErr_SetFromErrno(ItimerError);
    return NULL;
    }

    return itimer_retval(&old);
}

PyDoc_STRVAR(setitimer_doc,
"setitimer(which, seconds[, interval])\n\
\n\
Sets given itimer (one of ITIMER_REAL, ITIMER_VIRTUAL\n\
or ITIMER_PROF) to fire after value seconds and after\n\
that every interval seconds.\n\
The itimer can be cleared by setting seconds to zero.\n\
\n\
Returns old values as a tuple: (delay, interval).");
#endif


#ifdef HAVE_GETITIMER
static PyObject *
signal_getitimer(PyObject *self, PyObject *args)
{
    int which;
    struct itimerval old;

    if (!PyArg_ParseTuple(args, "i:getitimer", &which))
    return NULL;

    if (getitimer(which, &old) != 0) {
    PyErr_SetFromErrno(ItimerError);
    return NULL;
    }

    return itimer_retval(&old);
}

PyDoc_STRVAR(getitimer_doc,
"getitimer(which)\n\
\n\
Returns current value of given itimer.");
#endif

#ifdef PYPTHREAD_SIGMASK
/* Convert an iterable to a sigset.
   Return 0 on success, return -1 and raise an exception on error. */

static int
iterable_to_sigset(PyObject *iterable, sigset_t *mask)
{
    int result = -1;
    PyObject *iterator, *item;
    long signum;
    int err;

    sigemptyset(mask);

    iterator = PyObject_GetIter(iterable);
    if (iterator == NULL)
        goto error;

    while (1)
    {
        item = PyIter_Next(iterator);
        if (item == NULL) {
            if (PyErr_Occurred())
                goto error;
            else
                break;
        }

        signum = PyLong_AsLong(item);
        Py_DECREF(item);
        if (signum == -1 && PyErr_Occurred())
            goto error;
        if (0 < signum && signum < NSIG)
            err = sigaddset(mask, (int)signum);
        else
            err = 1;
        if (err) {
            PyErr_Format(PyExc_ValueError,
                         "signal number %ld out of range", signum);
            goto error;
        }
    }
    result = 0;

error:
    Py_XDECREF(iterator);
    return result;
}

static PyObject *
signal_pthread_sigmask(PyObject *self, PyObject *args)
{
    int how, sig;
    PyObject *signals, *result, *signum;
    sigset_t mask, previous;
    int err;

    if (!PyArg_ParseTuple(args, "iO:pthread_sigmask", &how, &signals))
        return NULL;

    if (iterable_to_sigset(signals, &mask))
        return NULL;

    err = pthread_sigmask(how, &mask, &previous);
    if (err != 0) {
        errno = err;
        PyErr_SetFromErrno(PyExc_RuntimeError);
        return NULL;
    }

    result = PyList_New(0);
    if (result == NULL)
        return NULL;

    for (sig = 1; sig < NSIG; sig++) {
        if (sigismember(&previous, sig) != 1)
            continue;

        /* Handle the case where it is a member by adding the signal to
           the result list.  Ignore the other cases because they mean the
           signal isn't a member of the mask or the signal was invalid,
           and an invalid signal must have been our fault in constructing
           the loop boundaries. */
        signum = PyLong_FromLong(sig);
        if (signum == NULL) {
            Py_DECREF(result);
            return NULL;
        }
        if (PyList_Append(result, signum) == -1) {
            Py_DECREF(signum);
            Py_DECREF(result);
            return NULL;
        }
        Py_DECREF(signum);
    }
    return result;
}

PyDoc_STRVAR(signal_pthread_sigmask_doc,
"pthread_sigmask(how, mask) -> old mask\n\
\n\
Fetch and/or change the signal mask of the calling thread.");
#endif   /* #ifdef PYPTHREAD_SIGMASK */


/* List of functions defined in the module */
static PyMethodDef signal_methods[] = {
#ifdef HAVE_ALARM
    {"alarm",                   signal_alarm, METH_VARARGS, alarm_doc},
#endif
#ifdef HAVE_SETITIMER
    {"setitimer",       signal_setitimer, METH_VARARGS, setitimer_doc},
#endif
#ifdef HAVE_GETITIMER
    {"getitimer",       signal_getitimer, METH_VARARGS, getitimer_doc},
#endif
    {"signal",                  signal_signal, METH_VARARGS, signal_doc},
    {"getsignal",               signal_getsignal, METH_VARARGS, getsignal_doc},
    {"set_wakeup_fd",           signal_set_wakeup_fd, METH_VARARGS, set_wakeup_fd_doc},
#ifdef HAVE_SIGINTERRUPT
    {"siginterrupt",            signal_siginterrupt, METH_VARARGS, siginterrupt_doc},
#endif
#ifdef HAVE_PAUSE
    {"pause",                   (PyCFunction)signal_pause,
     METH_NOARGS, pause_doc},
#endif
    {"default_int_handler", signal_default_int_handler,
     METH_VARARGS, default_int_handler_doc},
#ifdef PYPTHREAD_SIGMASK
    {"pthread_sigmask",         (PyCFunction)signal_pthread_sigmask,
     METH_VARARGS, signal_pthread_sigmask_doc},
#endif
    {NULL,                      NULL}           /* sentinel */
};


PyDoc_STRVAR(module_doc,
"This module provides mechanisms to use signal handlers in Python.\n\
\n\
Functions:\n\
\n\
alarm() -- cause SIGALRM after a specified time [Unix only]\n\
setitimer() -- cause a signal (described below) after a specified\n\
               float time and the timer may restart then [Unix only]\n\
getitimer() -- get current value of timer [Unix only]\n\
signal() -- set the action for a given signal\n\
getsignal() -- get the signal action for a given signal\n\
pause() -- wait until a signal arrives [Unix only]\n\
default_int_handler() -- default SIGINT handler\n\
\n\
signal constants:\n\
SIG_DFL -- used to refer to the system default handler\n\
SIG_IGN -- used to ignore the signal\n\
NSIG -- number of defined signals\n\
SIGINT, SIGTERM, etc. -- signal numbers\n\
\n\
itimer constants:\n\
ITIMER_REAL -- decrements in real time, and delivers SIGALRM upon\n\
               expiration\n\
ITIMER_VIRTUAL -- decrements only when the process is executing,\n\
               and delivers SIGVTALRM upon expiration\n\
ITIMER_PROF -- decrements both when the process is executing and\n\
               when the system is executing on behalf of the process.\n\
               Coupled with ITIMER_VIRTUAL, this timer is usually\n\
               used to profile the time spent by the application\n\
               in user and kernel space. SIGPROF is delivered upon\n\
               expiration.\n\
\n\n\
*** IMPORTANT NOTICE ***\n\
A signal handler function is called with two arguments:\n\
the first is the signal number, the second is the interrupted stack frame.");

static struct PyModuleDef signalmodule = {
    PyModuleDef_HEAD_INIT,
    "signal",
    module_doc,
    -1,
    signal_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC
PyInit_signal(void)
{
    PyObject *m, *d, *x;
    int i;

#ifdef WITH_THREAD
    main_thread = PyThread_get_thread_ident();
    main_pid = getpid();
#endif

    /* Create the module and add the functions */
    m = PyModule_Create(&signalmodule);
    if (m == NULL)
        return NULL;

    /* Add some symbolic constants to the module */
    d = PyModule_GetDict(m);

    x = DefaultHandler = PyLong_FromVoidPtr((void *)SIG_DFL);
    if (!x || PyDict_SetItemString(d, "SIG_DFL", x) < 0)
        goto finally;

    x = IgnoreHandler = PyLong_FromVoidPtr((void *)SIG_IGN);
    if (!x || PyDict_SetItemString(d, "SIG_IGN", x) < 0)
        goto finally;

    x = PyLong_FromLong((long)NSIG);
    if (!x || PyDict_SetItemString(d, "NSIG", x) < 0)
        goto finally;
    Py_DECREF(x);

#ifdef SIG_BLOCK
    x = PyLong_FromLong(SIG_BLOCK);
    if (!x || PyDict_SetItemString(d, "SIG_BLOCK", x) < 0)
        goto finally;
    Py_DECREF(x);
#endif

#ifdef SIG_UNBLOCK
    x = PyLong_FromLong(SIG_UNBLOCK);
    if (!x || PyDict_SetItemString(d, "SIG_UNBLOCK", x) < 0)
        goto finally;
    Py_DECREF(x);
#endif

#ifdef SIG_SETMASK
    x = PyLong_FromLong(SIG_SETMASK);
    if (!x || PyDict_SetItemString(d, "SIG_SETMASK", x) < 0)
        goto finally;
    Py_DECREF(x);
#endif

    x = IntHandler = PyDict_GetItemString(d, "default_int_handler");
    if (!x)
        goto finally;
    Py_INCREF(IntHandler);

    Handlers[0].tripped = 0;
    for (i = 1; i < NSIG; i++) {
        void (*t)(int);
        t = PyOS_getsig(i);
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
        old_siginthandler = PyOS_setsig(SIGINT, signal_handler);
    }

#ifdef SIGHUP
    x = PyLong_FromLong(SIGHUP);
    PyDict_SetItemString(d, "SIGHUP", x);
    Py_XDECREF(x);
#endif
#ifdef SIGINT
    x = PyLong_FromLong(SIGINT);
    PyDict_SetItemString(d, "SIGINT", x);
    Py_XDECREF(x);
#endif
#ifdef SIGBREAK
    x = PyLong_FromLong(SIGBREAK);
    PyDict_SetItemString(d, "SIGBREAK", x);
    Py_XDECREF(x);
#endif
#ifdef SIGQUIT
    x = PyLong_FromLong(SIGQUIT);
    PyDict_SetItemString(d, "SIGQUIT", x);
    Py_XDECREF(x);
#endif
#ifdef SIGILL
    x = PyLong_FromLong(SIGILL);
    PyDict_SetItemString(d, "SIGILL", x);
    Py_XDECREF(x);
#endif
#ifdef SIGTRAP
    x = PyLong_FromLong(SIGTRAP);
    PyDict_SetItemString(d, "SIGTRAP", x);
    Py_XDECREF(x);
#endif
#ifdef SIGIOT
    x = PyLong_FromLong(SIGIOT);
    PyDict_SetItemString(d, "SIGIOT", x);
    Py_XDECREF(x);
#endif
#ifdef SIGABRT
    x = PyLong_FromLong(SIGABRT);
    PyDict_SetItemString(d, "SIGABRT", x);
    Py_XDECREF(x);
#endif
#ifdef SIGEMT
    x = PyLong_FromLong(SIGEMT);
    PyDict_SetItemString(d, "SIGEMT", x);
    Py_XDECREF(x);
#endif
#ifdef SIGFPE
    x = PyLong_FromLong(SIGFPE);
    PyDict_SetItemString(d, "SIGFPE", x);
    Py_XDECREF(x);
#endif
#ifdef SIGKILL
    x = PyLong_FromLong(SIGKILL);
    PyDict_SetItemString(d, "SIGKILL", x);
    Py_XDECREF(x);
#endif
#ifdef SIGBUS
    x = PyLong_FromLong(SIGBUS);
    PyDict_SetItemString(d, "SIGBUS", x);
    Py_XDECREF(x);
#endif
#ifdef SIGSEGV
    x = PyLong_FromLong(SIGSEGV);
    PyDict_SetItemString(d, "SIGSEGV", x);
    Py_XDECREF(x);
#endif
#ifdef SIGSYS
    x = PyLong_FromLong(SIGSYS);
    PyDict_SetItemString(d, "SIGSYS", x);
    Py_XDECREF(x);
#endif
#ifdef SIGPIPE
    x = PyLong_FromLong(SIGPIPE);
    PyDict_SetItemString(d, "SIGPIPE", x);
    Py_XDECREF(x);
#endif
#ifdef SIGALRM
    x = PyLong_FromLong(SIGALRM);
    PyDict_SetItemString(d, "SIGALRM", x);
    Py_XDECREF(x);
#endif
#ifdef SIGTERM
    x = PyLong_FromLong(SIGTERM);
    PyDict_SetItemString(d, "SIGTERM", x);
    Py_XDECREF(x);
#endif
#ifdef SIGUSR1
    x = PyLong_FromLong(SIGUSR1);
    PyDict_SetItemString(d, "SIGUSR1", x);
    Py_XDECREF(x);
#endif
#ifdef SIGUSR2
    x = PyLong_FromLong(SIGUSR2);
    PyDict_SetItemString(d, "SIGUSR2", x);
    Py_XDECREF(x);
#endif
#ifdef SIGCLD
    x = PyLong_FromLong(SIGCLD);
    PyDict_SetItemString(d, "SIGCLD", x);
    Py_XDECREF(x);
#endif
#ifdef SIGCHLD
    x = PyLong_FromLong(SIGCHLD);
    PyDict_SetItemString(d, "SIGCHLD", x);
    Py_XDECREF(x);
#endif
#ifdef SIGPWR
    x = PyLong_FromLong(SIGPWR);
    PyDict_SetItemString(d, "SIGPWR", x);
    Py_XDECREF(x);
#endif
#ifdef SIGIO
    x = PyLong_FromLong(SIGIO);
    PyDict_SetItemString(d, "SIGIO", x);
    Py_XDECREF(x);
#endif
#ifdef SIGURG
    x = PyLong_FromLong(SIGURG);
    PyDict_SetItemString(d, "SIGURG", x);
    Py_XDECREF(x);
#endif
#ifdef SIGWINCH
    x = PyLong_FromLong(SIGWINCH);
    PyDict_SetItemString(d, "SIGWINCH", x);
    Py_XDECREF(x);
#endif
#ifdef SIGPOLL
    x = PyLong_FromLong(SIGPOLL);
    PyDict_SetItemString(d, "SIGPOLL", x);
    Py_XDECREF(x);
#endif
#ifdef SIGSTOP
    x = PyLong_FromLong(SIGSTOP);
    PyDict_SetItemString(d, "SIGSTOP", x);
    Py_XDECREF(x);
#endif
#ifdef SIGTSTP
    x = PyLong_FromLong(SIGTSTP);
    PyDict_SetItemString(d, "SIGTSTP", x);
    Py_XDECREF(x);
#endif
#ifdef SIGCONT
    x = PyLong_FromLong(SIGCONT);
    PyDict_SetItemString(d, "SIGCONT", x);
    Py_XDECREF(x);
#endif
#ifdef SIGTTIN
    x = PyLong_FromLong(SIGTTIN);
    PyDict_SetItemString(d, "SIGTTIN", x);
    Py_XDECREF(x);
#endif
#ifdef SIGTTOU
    x = PyLong_FromLong(SIGTTOU);
    PyDict_SetItemString(d, "SIGTTOU", x);
    Py_XDECREF(x);
#endif
#ifdef SIGVTALRM
    x = PyLong_FromLong(SIGVTALRM);
    PyDict_SetItemString(d, "SIGVTALRM", x);
    Py_XDECREF(x);
#endif
#ifdef SIGPROF
    x = PyLong_FromLong(SIGPROF);
    PyDict_SetItemString(d, "SIGPROF", x);
    Py_XDECREF(x);
#endif
#ifdef SIGXCPU
    x = PyLong_FromLong(SIGXCPU);
    PyDict_SetItemString(d, "SIGXCPU", x);
    Py_XDECREF(x);
#endif
#ifdef SIGXFSZ
    x = PyLong_FromLong(SIGXFSZ);
    PyDict_SetItemString(d, "SIGXFSZ", x);
    Py_XDECREF(x);
#endif
#ifdef SIGRTMIN
    x = PyLong_FromLong(SIGRTMIN);
    PyDict_SetItemString(d, "SIGRTMIN", x);
    Py_XDECREF(x);
#endif
#ifdef SIGRTMAX
    x = PyLong_FromLong(SIGRTMAX);
    PyDict_SetItemString(d, "SIGRTMAX", x);
    Py_XDECREF(x);
#endif
#ifdef SIGINFO
    x = PyLong_FromLong(SIGINFO);
    PyDict_SetItemString(d, "SIGINFO", x);
    Py_XDECREF(x);
#endif

#ifdef ITIMER_REAL
    x = PyLong_FromLong(ITIMER_REAL);
    PyDict_SetItemString(d, "ITIMER_REAL", x);
    Py_DECREF(x);
#endif
#ifdef ITIMER_VIRTUAL
    x = PyLong_FromLong(ITIMER_VIRTUAL);
    PyDict_SetItemString(d, "ITIMER_VIRTUAL", x);
    Py_DECREF(x);
#endif
#ifdef ITIMER_PROF
    x = PyLong_FromLong(ITIMER_PROF);
    PyDict_SetItemString(d, "ITIMER_PROF", x);
    Py_DECREF(x);
#endif

#if defined (HAVE_SETITIMER) || defined (HAVE_GETITIMER)
    ItimerError = PyErr_NewException("signal.ItimerError",
     PyExc_IOError, NULL);
    if (ItimerError != NULL)
    PyDict_SetItemString(d, "ItimerError", ItimerError);
#endif

#ifdef CTRL_C_EVENT
    x = PyLong_FromLong(CTRL_C_EVENT);
    PyDict_SetItemString(d, "CTRL_C_EVENT", x);
    Py_DECREF(x);
#endif

#ifdef CTRL_BREAK_EVENT
    x = PyLong_FromLong(CTRL_BREAK_EVENT);
    PyDict_SetItemString(d, "CTRL_BREAK_EVENT", x);
    Py_DECREF(x);
#endif

    if (PyErr_Occurred()) {
        Py_DECREF(m);
        m = NULL;
    }

  finally:
    return m;
}

static void
finisignal(void)
{
    int i;
    PyObject *func;

    PyOS_setsig(SIGINT, old_siginthandler);
    old_siginthandler = SIG_DFL;

    for (i = 1; i < NSIG; i++) {
        func = Handlers[i].func;
        Handlers[i].tripped = 0;
        Handlers[i].func = NULL;
        if (i != SIGINT && func != NULL && func != Py_None &&
            func != DefaultHandler && func != IgnoreHandler)
            PyOS_setsig(i, SIG_DFL);
        Py_XDECREF(func);
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
PyErr_CheckSignals(void)
{
    int i;
    PyObject *f;

    if (!is_tripped)
        return 0;

#ifdef WITH_THREAD
    if (PyThread_get_thread_ident() != main_thread)
        return 0;
#endif

    /*
     * The is_tripped variable is meant to speed up the calls to
     * PyErr_CheckSignals (both directly or via pending calls) when no
     * signal has arrived. This variable is set to 1 when a signal arrives
     * and it is set to 0 here, when we know some signals arrived. This way
     * we can run the registered handlers with no signals blocked.
     *
     * NOTE: with this approach we can have a situation where is_tripped is
     *       1 but we have no more signals to handle (Handlers[i].tripped
     *       is 0 for every signal i). This won't do us any harm (except
     *       we're gonna spent some cycles for nothing). This happens when
     *       we receive a signal i after we zero is_tripped and before we
     *       check Handlers[i].tripped.
     */
    is_tripped = 0;

    if (!(f = (PyObject *)PyEval_GetFrame()))
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

    return 0;
}


/* Replacements for intrcheck.c functionality
 * Declared in pyerrors.h
 */
void
PyErr_SetInterrupt(void)
{
    trip_signal(SIGINT);
}

void
PyOS_InitInterrupts(void)
{
    PyObject *m = PyInit_signal();
    if (m) {
        _PyImport_FixupBuiltin(m, "signal");
        Py_DECREF(m);
    }
}

void
PyOS_FiniInterrupts(void)
{
    finisignal();
}

int
PyOS_InterruptOccurred(void)
{
    if (Handlers[SIGINT].tripped) {
#ifdef WITH_THREAD
        if (PyThread_get_thread_ident() != main_thread)
            return 0;
#endif
        Handlers[SIGINT].tripped = 0;
        return 1;
    }
    return 0;
}

void
PyOS_AfterFork(void)
{
#ifdef WITH_THREAD
    _PyGILState_Reinit();
    PyEval_ReInitThreads();
    main_thread = PyThread_get_thread_ident();
    main_pid = getpid();
    _PyImport_ReInitLock();
    PyThread_ReInitTLS();
#endif
}
