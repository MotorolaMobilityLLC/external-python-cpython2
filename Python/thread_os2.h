/* This code implemented by cvale@netcom.com */

#define INCL_DOSPROCESS
#define INCL_DOSSEMAPHORES
#include "os2.h"
#include "limits.h"

#include "process.h"

long PyThread_get_thread_ident(void);


/*
 * Initialization of the C package, should not be needed.
 */
static void
PyThread__init_thread(void)
{
}

/*
 * Thread support.
 */
long
PyThread_start_new_thread(void (*func)(void *), void *arg)
{
  int aThread;
  int success = 0;

  aThread = _beginthread(func,NULL,65536,arg);

  if( aThread == -1 ) {
    success = -1;
    fprintf(stderr,"aThread failed == %d",aThread);
    dprintf(("_beginthread failed. return %ld\n", errno));
  }

  return success;
}

long
PyThread_get_thread_ident(void)
{
  PPIB pib;
  PTIB tib;

  if (!initialized)
    PyThread_init_thread();
        
  DosGetInfoBlocks(&tib,&pib);
  return tib->tib_ptib2->tib2_ultid;
}

static void
do_PyThread_exit_thread(int no_cleanup)
{
  dprintf(("%ld: PyThread_exit_thread called\n", PyThread_get_thread_ident()));
  if (!initialized)
    if (no_cleanup)
      _exit(0);
    else
      exit(0);
  _endthread();
}

void 
PyThread_exit_thread(void)
{
  do_PyThread_exit_thread(0);
}

void 
PyThread__exit_thread(void)
{
  do_PyThread_exit_thread(1);
}

#ifndef NO_EXIT_PROG
static void 
do_PyThread_exit_prog(int status, int no_cleanup)
{
  dprintf(("PyThread_exit_prog(%d) called\n", status));
  if (!initialized)
    if (no_cleanup)
      _exit(status);
    else
      exit(status);
}

void 
PyThread_exit_prog(int status)
{
  do_PyThread_exit_prog(status, 0);
}

void 
PyThread__exit_prog(int status)
{
  do_PyThread_exit_prog(status, 1);
}
#endif /* NO_EXIT_PROG */

/*
 * Lock support.  This is implemented with an event semaphore and critical
 * sections to make it behave more like a posix mutex than its OS/2 
 # counterparts.
 */

typedef struct os2_lock_t {
  int is_set;
  HEV changed;
} *type_os2_lock;

PyThread_type_lock 
PyThread_allocate_lock(void)
{
  APIRET rc;
  type_os2_lock lock = (type_os2_lock)malloc(sizeof(struct os2_lock_t));

  dprintf(("PyThread_allocate_lock called\n"));
  if (!initialized)
    PyThread_init_thread();

  lock->is_set = 0;

  DosCreateEventSem(NULL, &lock->changed, 0, 0);

  dprintf(("%ld: PyThread_allocate_lock() -> %p\n", 
           PyThread_get_thread_ident(), 
           lock->changed));

  return (PyThread_type_lock) lock;
}

void 
PyThread_free_lock(PyThread_type_lock aLock)
{
  type_os2_lock lock = (type_os2_lock)aLock;
  dprintf(("%ld: PyThread_free_lock(%p) called\n", PyThread_get_thread_ident(),aLock));

  DosCloseEventSem(lock->changed);
  free(aLock);
}

/*
 * Return 1 on success if the lock was acquired
 *
 * and 0 if the lock was not acquired.
 */
int 
PyThread_acquire_lock(PyThread_type_lock aLock, int waitflag)
{
  int   done = 0;
  ULONG count;
  PID   pid = 0;
  TID   tid = 0;
  type_os2_lock lock = (type_os2_lock)aLock;

  dprintf(("%ld: PyThread_acquire_lock(%p, %d) called\n", PyThread_get_thread_ident(),
           aLock, waitflag));

  while (!done) {
    /* if the lock is currently set, we have to wait for the state to change */
    if (lock->is_set) {
      if (!waitflag)
        return 0;
      DosWaitEventSem(lock->changed, SEM_INDEFINITE_WAIT);
    }
    
    /* 
     * enter a critical section and try to get the semaphore.  If
     * it is still locked, we will try again.
     */
    if (DosEnterCritSec())
      return 0;

    if (!lock->is_set) {
      lock->is_set = 1;
      DosResetEventSem(lock->changed, &count);
      done = 1;
    }

    DosExitCritSec();
  }

  return 1;
}

void PyThread_release_lock(PyThread_type_lock aLock)
{
  type_os2_lock lock = (type_os2_lock)aLock;
  dprintf(("%ld: PyThread_release_lock(%p) called\n", PyThread_get_thread_ident(),aLock));

  if (!lock->is_set) {
    dprintf(("%ld: Could not PyThread_release_lock(%p) error: %l\n",
             PyThread_get_thread_ident(), aLock, GetLastError()));
    return;
  }


  if (DosEnterCritSec()) {
    dprintf(("%ld: Could not PyThread_release_lock(%p) error: %l\n",
             PyThread_get_thread_ident(), aLock, GetLastError()));
    return;
  }
  
  lock->is_set = 0;
  DosPostEventSem(lock->changed);
  
  DosExitCritSec();
}
