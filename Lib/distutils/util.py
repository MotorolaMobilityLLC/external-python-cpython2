"""distutils.util

Miscellaneous utility functions -- anything that doesn't fit into
one of the other *util.py modules."""

# created 1999/03/08, Greg Ward

__revision__ = "$Id$"

import sys, os, string, re, shutil
from distutils.errors import *
from distutils.spawn import spawn

# for backwards compatibility:
from distutils.file_util import *
from distutils.dir_util import *
from distutils.dep_util import *
from distutils.archive_util import *


def get_platform ():
    """Return a string (suitable for tacking onto directory names) that
       identifies the current platform.  Under Unix, identifies both the OS
       and hardware architecture, e.g. "linux-i586", "solaris-sparc",
       "irix-mips".  For Windows and Mac OS, just returns 'sys.platform' --
       i.e. "???" or "???"."""

    if os.name == 'posix':
        (OS, _, rel, _, arch) = os.uname()
        return "%s%c-%s" % (string.lower (OS), rel[0], string.lower (arch))
    else:
        return sys.platform

# get_platform()


def native_path (pathname):
    """Return 'pathname' as a name that will work on the native
       filesystem, i.e. split it on '/' and put it back together again
       using the current directory separator.  Needed because filenames in
       the setup script are always supplied in Unix style, and have to be
       converted to the local convention before we can actually use them in
       the filesystem.  Raises DistutilsValueError if 'pathname' is
       absolute (starts with '/') or contains local directory separators
       (unless the local separator is '/', of course)."""

    if pathname[0] == '/':
        raise DistutilsValueError, "path '%s' cannot be absolute" % pathname
    if pathname[-1] == '/':
        raise DistutilsValueError, "path '%s' cannot end with '/'" % pathname
    if os.sep != '/' and os.sep in pathname:
        raise DistutilsValueError, \
              "path '%s' cannot contain '%c' character" % \
              (pathname, os.sep)

        paths = string.split (pathname, '/')
        return apply (os.path.join, paths)
    else:
        return pathname

# native_path ()


def _check_environ ():
    """Ensure that 'os.environ' has all the environment variables we
       guarantee that users can use in config files, command-line
       options, etc.  Currently this includes:
         HOME - user's home directory (Unix only)
         PLAT - desription of the current platform, including hardware
                and OS (see 'get_platform()')
    """

    if os.name == 'posix' and not os.environ.has_key('HOME'):
        import pwd
        os.environ['HOME'] = pwd.getpwuid (os.getuid())[5]

    if not os.environ.has_key('PLAT'):
        os.environ['PLAT'] = get_platform ()


def subst_vars (str, local_vars):
    """Perform shell/Perl-style variable substitution on 'string'.
       Every occurence of '$' followed by a name, or a name enclosed in
       braces, is considered a variable.  Every variable is substituted by
       the value found in the 'local_vars' dictionary, or in 'os.environ'
       if it's not in 'local_vars'.  'os.environ' is first checked/
       augmented to guarantee that it contains certain values: see
       '_check_environ()'.  Raise ValueError for any variables not found in
       either 'local_vars' or 'os.environ'."""

    _check_environ ()
    def _subst (match, local_vars=local_vars):
        var_name = match.group(1)
        if local_vars.has_key (var_name):
            return str (local_vars[var_name])
        else:
            return os.environ[var_name]

    return re.sub (r'\$([a-zA-Z_][a-zA-Z_0-9]*)', _subst, str)

# subst_vars ()


