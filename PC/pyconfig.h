#ifndef Py_CONFIG_H
#define Py_CONFIG_H

/* pyconfig.h.  NOT Generated automatically by configure.

This is a manually maintained version used for the Watcom,
Borland and and Microsoft Visual C++ compilers.  It is a
standard part of the Python distribution.

WINDOWS DEFINES:
The code specific to Windows should be wrapped around one of
the following #defines

MS_WIN64 - Code specific to the MS Win64 API
MS_WIN32 - Code specific to the MS Win32 (and Win64) API (obsolete, this covers all supported APIs)
MS_WINDOWS - Code specific to Windows, but all versions.
Py_ENABLE_SHARED - Code if the Python core is built as a DLL.

Also note that neither "_M_IX86" or "_MSC_VER" should be used for
any purpose other than "Windows Intel x86 specific" and "Microsoft
compiler specific".  Therefore, these should be very rare.


NOTE: The following symbols are deprecated:
NT, WIN32, USE_DL_EXPORT, USE_DL_IMPORT, DL_EXPORT, DL_IMPORT
MS_CORE_DLL.

*/

#include <io.h>
#define HAVE_LIMITS_H
#define HAVE_SYS_UTIME_H
#define HAVE_HYPOT
#define HAVE_TEMPNAM
#define HAVE_TMPFILE
#define HAVE_TMPNAM
#define HAVE_CLOCK
#define HAVE_STRFTIME
#define HAVE_STRERROR
#define DONT_HAVE_SIG_ALARM
#define DONT_HAVE_SIG_PAUSE
#define LONG_BIT	32
#define WORD_BIT 32
#define PREFIX ""
#define EXEC_PREFIX ""

#define MS_WIN32 /* only support win32 and greater. */
#define MS_WINDOWS
#ifndef PYTHONPATH
#	define PYTHONPATH ".\\DLLs;.\\lib;.\\lib\\plat-win;.\\lib\\lib-tk"
#endif
#define NT_THREADS
#define WITH_THREAD
#ifndef NETSCAPE_PI
#define USE_SOCKET
#endif

/* Compiler specific defines */

/* ------------------------------------------------------------------------*/
/* Microsoft C defines _MSC_VER */
#ifdef _MSC_VER

/* MSVC defines _WINxx to differentiate the windows platform types

   Note that for compatibility reasons _WIN32 is defined on Win32
   *and* on Win64. For the same reasons, in Python, MS_WIN32 is
   defined on Win32 *and* Win64. Win32 only code must therefore be
   guarded as follows:
   	#if defined(MS_WIN32) && !defined(MS_WIN64)
*/
#ifdef _WIN64
#define MS_WIN64
#endif

/* set the COMPILER */
#ifdef MS_WIN64
#ifdef _M_IX86
#define COMPILER "[MSC 64 bit (Intel)]"
#elif defined(_M_ALPHA)
#define COMPILER "[MSC 64 bit (Alpha)]"
#else
#define COMPILER "[MSC 64 bit (Unknown)]"
#endif
#endif /* MS_WIN64 */

#if defined(MS_WIN32) && !defined(MS_WIN64)
#ifdef _M_IX86
#define COMPILER "[MSC 32 bit (Intel)]"
#elif defined(_M_ALPHA)
#define COMPILER "[MSC 32 bit (Alpha)]"
#else
#define COMPILER "[MSC (Unknown)]"
#endif
#endif /* MS_WIN32 && !MS_WIN64 */

typedef int pid_t;
#define hypot _hypot

#endif /* _MSC_VER */

/* define some ANSI types that are not defined in earlier Win headers */
#if defined(_MSC_VER) && _MSC_VER >= 1200
/* This file only exists in VC 6.0 or higher */
#include <basetsd.h>
#endif

/* ------------------------------------------------------------------------*/
/* The Borland compiler defines __BORLANDC__ */
/* XXX These defines are likely incomplete, but should be easy to fix. */
#ifdef __BORLANDC__
#define COMPILER "[Borland]"

#ifdef _WIN32
/* tested with BCC 5.5 (__BORLANDC__ >= 0x0550)
 */

typedef int pid_t;
/* BCC55 seems to understand __declspec(dllimport), it is used in its
   own header files (winnt.h, ...) - so we can do nothing and get the default*/

#undef HAVE_SYS_UTIME_H
#define HAVE_UTIME_H
#define HAVE_DIRENT_H

/* rename a few functions for the Borland compiler */
#include <io.h>
#define _chsize chsize
#define _setmode setmode

#else /* !_WIN32 */
#error "Only Win32 and later are supported"
#endif /* !_WIN32 */

#endif /* BORLANDC */

/* ------------------------------------------------------------------------*/
/* egcs/gnu-win32 defines __GNUC__ and _WIN32 */
#if defined(__GNUC__) && defined(_WIN32)
/* XXX These defines are likely incomplete, but should be easy to fix.
   They should be complete enough to build extension modules. */
/* Suggested by Rene Liebscher <R.Liebscher@gmx.de> to avoid a GCC 2.91.*
   bug that requires structure imports.  More recent versions of the
   compiler don't exhibit this bug.
*/
#if (__GNUC__==2) && (__GNUC_MINOR__<=91)
#warning "Please use an up-to-date version of gcc! (>2.91 recommended)"
#endif

#define COMPILER "[gcc]"
#define hypot _hypot
#define LONG_LONG long long
#endif /* GNUC */

/* ------------------------------------------------------------------------*/
/* lcc-win32 defines __LCC__ */
#if defined(__LCC__)
/* XXX These defines are likely incomplete, but should be easy to fix.
   They should be complete enough to build extension modules. */

#define COMPILER "[lcc-win32]"
typedef int pid_t;
/* __declspec() is supported here too - do nothing to get the defaults */

#endif /* LCC */

/* ------------------------------------------------------------------------*/
/* End of compilers - finish up */

#ifndef NO_STDIO_H
#	include <stdio.h>
#endif

/* 64 bit ints are usually spelt __int64 unless compiler has overridden */
#define HAVE_LONG_LONG 1
#ifndef LONG_LONG
#	define LONG_LONG __int64
#endif

/* For Windows the Python core is in a DLL by default.  Test 
Py_NO_ENABLE_SHARED to find out.  Also support MS_NO_COREDLL for b/w compat */
#if !defined(MS_NO_COREDLL) && !defined(Py_NO_ENABLE_SHARED)
#	define Py_ENABLE_SHARED 1 /* standard symbol for shared library */
#	define MS_COREDLL	/* deprecated old symbol */
#endif /* !MS_NO_COREDLL && ... */

/* Deprecated USE_DL_EXPORT macro - please use Py_BUILD_CORE */
#ifdef USE_DL_EXPORT
#	define Py_BUILD_CORE
#endif /* USE_DL_EXPORT */

/*  All windows compilers that use this header support __declspec */
#define HAVE_DECLSPEC_DLL

/* For an MSVC DLL, we can nominate the .lib files used by extensions */
#ifdef MS_COREDLL
#	ifndef Py_BUILD_CORE /* not building the core - must be an ext */
#		if defined(_MSC_VER)
			/* So MSVC users need not specify the .lib file in 
			their Makefile (other compilers are generally
			taken care of by distutils.) */
#			ifdef _DEBUG
#				pragma comment(lib,"python23_d.lib")
#			else
#				pragma comment(lib,"python23.lib")
#			endif /* _DEBUG */
#		endif /* _MSC_VER */
#	endif /* Py_BUILD_CORE */
#endif /* MS_COREDLL */

#if defined(MS_WIN64)
/* maintain "win32" sys.platform for backward compatibility of Python code,
   the Win64 API should be close enough to the Win32 API to make this
   preferable */
#	define PLATFORM "win32"
#	define SIZEOF_VOID_P 8
#	define SIZEOF_TIME_T 8
#	define SIZEOF_OFF_T 4
#	define SIZEOF_FPOS_T 8
#	define SIZEOF_HKEY 8
/* configure.in defines HAVE_LARGEFILE_SUPPORT iff HAVE_LONG_LONG,
   sizeof(off_t) > sizeof(long), and sizeof(LONG_LONG) >= sizeof(off_t).
   On Win64 the second condition is not true, but if fpos_t replaces off_t
   then this is true. The uses of HAVE_LARGEFILE_SUPPORT imply that Win64
   should define this. */
#	define HAVE_LARGEFILE_SUPPORT
#elif defined(MS_WIN32)
#	define PLATFORM "win32"
#	define HAVE_LARGEFILE_SUPPORT
#	ifdef _M_ALPHA
#		define SIZEOF_VOID_P 8
#		define SIZEOF_TIME_T 8
#	else
#		define SIZEOF_VOID_P 4
#		define SIZEOF_TIME_T 4
#		define SIZEOF_OFF_T 4
#		define SIZEOF_FPOS_T 8
#		define SIZEOF_HKEY 4
#	endif
#endif

#ifdef _DEBUG
#	define Py_DEBUG
#endif


#ifdef MS_WIN32

#define SIZEOF_SHORT 2
#define SIZEOF_INT 4
#define SIZEOF_LONG 4
#define SIZEOF_LONG_LONG 8

#endif

/* Fairly standard from here! */

/* Define if on AIX 3.
   System headers sometimes define this.
   We just want to avoid a redefinition error message.  */
#ifndef _ALL_SOURCE
/* #undef _ALL_SOURCE */
#endif

/* Define to empty if the keyword does not work.  */
/* #define const  */

/* Define if you have dirent.h.  */
/* #define DIRENT 1 */

/* Define to the type of elements in the array set by `getgroups'.
   Usually this is either `int' or `gid_t'.  */
/* #undef GETGROUPS_T */

/* Define to `int' if <sys/types.h> doesn't define.  */
/* #undef gid_t */

/* Define if your struct tm has tm_zone.  */
/* #undef HAVE_TM_ZONE */

/* Define if you don't have tm_zone but do have the external array
   tzname.  */
#define HAVE_TZNAME

/* Define if on MINIX.  */
/* #undef _MINIX */

/* Define to `int' if <sys/types.h> doesn't define.  */
/* #undef mode_t */

/* Define if you don't have dirent.h, but have ndir.h.  */
/* #undef NDIR */

/* Define to `long' if <sys/types.h> doesn't define.  */
/* #undef off_t */

/* Define to `int' if <sys/types.h> doesn't define.  */
/* #undef pid_t */

/* Define if the system does not provide POSIX.1 features except
   with this defined.  */
/* #undef _POSIX_1_SOURCE */

/* Define if you need to in order for stat and other things to work.  */
/* #undef _POSIX_SOURCE */

/* Define as the return type of signal handlers (int or void).  */
#define RETSIGTYPE void

/* Define to `unsigned' if <sys/types.h> doesn't define.  */
/* #undef size_t */

/* Define to `int' if <sys/types.h> doesn't define.  */
#if _MSC_VER + 0 >= 1300
/* VC.NET typedefs socklen_t in ws2tcpip.h. */
#else
#define socklen_t int
#endif

/* Define if you have the ANSI C header files.  */
#define STDC_HEADERS 1

/* Define if you don't have dirent.h, but have sys/dir.h.  */
/* #undef SYSDIR */

/* Define if you don't have dirent.h, but have sys/ndir.h.  */
/* #undef SYSNDIR */

/* Define if you can safely include both <sys/time.h> and <time.h>.  */
/* #undef TIME_WITH_SYS_TIME */

/* Define if your <sys/time.h> declares struct tm.  */
/* #define TM_IN_SYS_TIME 1 */

/* Define to `int' if <sys/types.h> doesn't define.  */
/* #undef uid_t */

/* Define if the closedir function returns void instead of int.  */
/* #undef VOID_CLOSEDIR */

/* Define if your <unistd.h> contains bad prototypes for exec*()
   (as it does on SGI IRIX 4.x) */
/* #undef BAD_EXEC_PROTOTYPES */

/* Define if getpgrp() must be called as getpgrp(0)
   and (consequently) setpgrp() as setpgrp(0, 0). */
/* #undef GETPGRP_HAVE_ARGS */

/* Define this if your time.h defines altzone */
/* #define HAVE_ALTZONE */

/* Define if you have the putenv function.  */
#define HAVE_PUTENV

/* Define if your compiler supports function prototypes */
#define HAVE_PROTOTYPES

/* Define if  you can safely include both <sys/select.h> and <sys/time.h>
   (which you can't on SCO ODT 3.0). */
/* #undef SYS_SELECT_WITH_SYS_TIME */

/* Define if you want to use SGI (IRIX 4) dynamic linking.
   This requires the "dl" library by Jack Jansen,
   ftp://ftp.cwi.nl/pub/dynload/dl-1.6.tar.Z.
   Don't bother on IRIX 5, it already has dynamic linking using SunOS
   style shared libraries */
/* #undef WITH_SGI_DL */

/* Define if you want to emulate SGI (IRIX 4) dynamic linking.
   This is rumoured to work on VAX (Ultrix), Sun3 (SunOS 3.4),
   Sequent Symmetry (Dynix), and Atari ST.
   This requires the "dl-dld" library,
   ftp://ftp.cwi.nl/pub/dynload/dl-dld-1.1.tar.Z,
   as well as the "GNU dld" library,
   ftp://ftp.cwi.nl/pub/dynload/dld-3.2.3.tar.Z.
   Don't bother on SunOS 4 or 5, they already have dynamic linking using
   shared libraries */
/* #undef WITH_DL_DLD */

/* Define if you want documentation strings in extension modules */
#define WITH_DOC_STRINGS 1

/* Define if you want to compile in rudimentary thread support */
/* #undef WITH_THREAD */

/* Define if you want to use the GNU readline library */
/* #define WITH_READLINE 1 */

/* Define if you want to have a Unicode type. */
#define Py_USING_UNICODE

/* Define as the integral type used for Unicode representation. */
#define PY_UNICODE_TYPE unsigned short

/* Define as the size of the unicode type. */
#define Py_UNICODE_SIZE SIZEOF_SHORT

/* Define if you have a useable wchar_t type defined in wchar.h; useable
   means wchar_t must be 16-bit unsigned type. (see
   Include/unicodeobject.h). */
#if Py_UNICODE_SIZE == 2
#define HAVE_USABLE_WCHAR_T
#endif

/* Use Python's own small-block memory-allocator. */
#define WITH_PYMALLOC 1

/* Enable \n, \r, \r\n line ends on import; also the 'U' mode flag for open. */
#define WITH_UNIVERSAL_NEWLINES 1

/* Define if you have clock.  */
/* #define HAVE_CLOCK */

/* Define when any dynamic module loading is enabled */
#define HAVE_DYNAMIC_LOADING

/* Define if you have ftime.  */
#define HAVE_FTIME

/* Define if you have getpeername.  */
#define HAVE_GETPEERNAME

/* Define if you have getpgrp.  */
/* #undef HAVE_GETPGRP */

/* Define if you have getpid.  */
#define HAVE_GETPID

/* Define if you have gettimeofday.  */
/* #undef HAVE_GETTIMEOFDAY */

/* Define if you have getwd.  */
/* #undef HAVE_GETWD */

/* Define if you have lstat.  */
/* #undef HAVE_LSTAT */

/* Define if you have the mktime function.  */
#define HAVE_MKTIME

/* Define if you have nice.  */
/* #undef HAVE_NICE */

/* Define if you have readlink.  */
/* #undef HAVE_READLINK */

/* Define if you have select.  */
/* #undef HAVE_SELECT */

/* Define if you have setpgid.  */
/* #undef HAVE_SETPGID */

/* Define if you have setpgrp.  */
/* #undef HAVE_SETPGRP */

/* Define if you have setsid.  */
/* #undef HAVE_SETSID */

/* Define if you have setvbuf.  */
#define HAVE_SETVBUF

/* Define if you have siginterrupt.  */
/* #undef HAVE_SIGINTERRUPT */

/* Define if you have symlink.  */
/* #undef HAVE_SYMLINK */

/* Define if you have tcgetpgrp.  */
/* #undef HAVE_TCGETPGRP */

/* Define if you have tcsetpgrp.  */
/* #undef HAVE_TCSETPGRP */

/* Define if you have times.  */
/* #undef HAVE_TIMES */

/* Define if you have uname.  */
/* #undef HAVE_UNAME */

/* Define if you have waitpid.  */
/* #undef HAVE_WAITPID */

/* Define if you have the <dlfcn.h> header file.  */
/* #undef HAVE_DLFCN_H */

/* Define if you have the <fcntl.h> header file.  */
#define HAVE_FCNTL_H 1

/* Define if you have the <signal.h> header file.  */
#define HAVE_SIGNAL_H 1

/* Define if you have the <stdarg.h> header file.  */
#define HAVE_STDARG_H 1

/* Define if you have the <stdarg.h> prototypes.  */
#define HAVE_STDARG_PROTOTYPES

/* Define if you have the <stddef.h> header file.  */
#define HAVE_STDDEF_H 1

/* Define if you have the <stdlib.h> header file.  */
#define HAVE_STDLIB_H 1

/* Define if you have the <sys/audioio.h> header file.  */
/* #undef HAVE_SYS_AUDIOIO_H */

/* Define if you have the <sys/param.h> header file.  */
/* #define HAVE_SYS_PARAM_H 1 */

/* Define if you have the <sys/select.h> header file.  */
/* #define HAVE_SYS_SELECT_H 1 */

/* Define if you have the <sys/time.h> header file.  */
/* #define HAVE_SYS_TIME_H 1 */

/* Define if you have the <sys/times.h> header file.  */
/* #define HAVE_SYS_TIMES_H 1 */

/* Define if you have the <sys/un.h> header file.  */
/* #define HAVE_SYS_UN_H 1 */

/* Define if you have the <sys/utime.h> header file.  */
/* #define HAVE_SYS_UTIME_H 1 */

/* Define if you have the <sys/utsname.h> header file.  */
/* #define HAVE_SYS_UTSNAME_H 1 */

/* Define if you have the <thread.h> header file.  */
/* #undef HAVE_THREAD_H */

/* Define if you have the <unistd.h> header file.  */
/* #define HAVE_UNISTD_H 1 */

/* Define if you have the <utime.h> header file.  */
/* #define HAVE_UTIME_H 1 */

/* Define if you have the dl library (-ldl).  */
/* #undef HAVE_LIBDL */

/* Define if you have the mpc library (-lmpc).  */
/* #undef HAVE_LIBMPC */

/* Define if you have the nsl library (-lnsl).  */
#define HAVE_LIBNSL 1

/* Define if you have the seq library (-lseq).  */
/* #undef HAVE_LIBSEQ */

/* Define if you have the socket library (-lsocket).  */
#define HAVE_LIBSOCKET 1

/* Define if you have the sun library (-lsun).  */
/* #undef HAVE_LIBSUN */

/* Define if you have the termcap library (-ltermcap).  */
/* #undef HAVE_LIBTERMCAP */

/* Define if you have the termlib library (-ltermlib).  */
/* #undef HAVE_LIBTERMLIB */

/* Define if you have the thread library (-lthread).  */
/* #undef HAVE_LIBTHREAD */
#endif /* !Py_CONFIG_H */
