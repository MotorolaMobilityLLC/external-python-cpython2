"""distutils.filelist

Provides the FileList class, used for poking about the filesystem
and building lists of files.
"""

# created 2000/07/17, Rene Liebscher (as template.py)
# most parts taken from commands/sdist.py
# renamed 2000/07/29 (to filelist.py) and officially added to
#  the Distutils source, Greg Ward 

__revision__ = "$Id$"

import sys, os, string, re
import fnmatch
from types import *
from glob import glob
from distutils.util import convert_path

class FileList:

    files = None # reference to files list to mainpulate
    allfiles = None # list of all files, if None will be filled
                    # at first use from directory self.dir
    dir = None # directory from which files will be taken
               # to fill self.allfiles if it was not set otherwise

    # next both functions (callable objects) can be set by the user
    # warn: warning function
    # debug_print: debug function  

    def __init__(self, 
                 files=[], 
                 dir=os.curdir, 
                 allfiles=None, 
                 warn=None, 
                 debug_print=None):
        # use standard warning and debug functions, if no other given
        if warn is None: warn = self.__warn 
        if debug_print is None: debug_print = self.__debug_print
        self.warn = warn
        self.debug_print = debug_print
        self.files = files
        self.dir = dir
        self.allfiles = allfiles 
             # if None, it will be filled, when used for first time


    # standard warning and debug functions, if no other given
    def __warn (self, msg):
        sys.stderr.write ("warning: template: %s\n" % msg)
        
    def __debug_print (self, msg):
        """Print 'msg' to stdout if the global DEBUG (taken from the
        DISTUTILS_DEBUG environment variable) flag is true.
        """
        from distutils.core import DEBUG
        if DEBUG:
            print msg

    
    def process_line(self, line):    

            words = string.split (line)
            action = words[0]

            # First, check that the right number of words are present
            # for the given action (which is the first word)
            if action in ('include','exclude',
                          'global-include','global-exclude'):
                if len (words) < 2:
                    self.warn \
                        ("invalid template line: " +
                         "'%s' expects <pattern1> <pattern2> ..." %
                         action)
                    return

                pattern_list = map(convert_path, words[1:])

            elif action in ('recursive-include','recursive-exclude'):
                if len (words) < 3:
                    self.warn \
                        ("invalid template line: " +
                         "'%s' expects <dir> <pattern1> <pattern2> ..." %
                         action)
                    return

                dir = convert_path(words[1])
                pattern_list = map (convert_path, words[2:])

            elif action in ('graft','prune'):
                if len (words) != 2:
                    self.warn \
                        ("invalid template line: " +
                         "'%s' expects a single <dir_pattern>" %
                         action)
                    return

                dir_pattern = convert_path (words[1])

            else:
                self.warn ("invalid template line: " +
                               "unknown action '%s'" % action)
                return

            # OK, now we know that the action is valid and we have the
            # right number of words on the line for that action -- so we
            # can proceed with minimal error-checking.  Also, we have
            # defined either (pattern), (dir and pattern), or
            # (dir_pattern) -- so we don't have to spend any time
            # digging stuff up out of 'words'.

            if action == 'include':
                self.debug_print("include " + string.join(pattern_list))
                for pattern in pattern_list:
                    if not self.select_pattern (pattern, anchor=1):
                        self.warn ("no files found matching '%s'" %
                                       pattern)

            elif action == 'exclude':
                self.debug_print("exclude " + string.join(pattern_list))
                for pattern in pattern_list:
                    if not self.exclude_pattern (pattern, anchor=1):
                        self.warn (
                            "no previously-included files found matching '%s'"%
                            pattern)

            elif action == 'global-include':
                self.debug_print("global-include " + string.join(pattern_list))
                for pattern in pattern_list:
                    if not self.select_pattern (pattern, anchor=0):
                        self.warn (("no files found matching '%s' " +
                                        "anywhere in distribution") %
                                       pattern)

            elif action == 'global-exclude':
                self.debug_print("global-exclude " + string.join(pattern_list))
                for pattern in pattern_list:
                    if not self.exclude_pattern (pattern, anchor=0):
                        self.warn \
                            (("no previously-included files matching '%s' " +
                              "found anywhere in distribution") %
                             pattern)

            elif action == 'recursive-include':
                self.debug_print("recursive-include %s %s" %
                                 (dir, string.join(pattern_list)))
                for pattern in pattern_list:
                    if not self.select_pattern (pattern, prefix=dir):
                        self.warn (("no files found matching '%s' " +
                                        "under directory '%s'") %
                                       (pattern, dir))

            elif action == 'recursive-exclude':
                self.debug_print("recursive-exclude %s %s" %
                                 (dir, string.join(pattern_list)))
                for pattern in pattern_list:
                    if not self.exclude_pattern(pattern, prefix=dir):
                        self.warn \
                            (("no previously-included files matching '%s' " +
                              "found under directory '%s'") %
                             (pattern, dir))

            elif action == 'graft':
                self.debug_print("graft " + dir_pattern)
                if not self.select_pattern(None, prefix=dir_pattern):
                    self.warn ("no directories found matching '%s'" %
                                   dir_pattern)

            elif action == 'prune':
                self.debug_print("prune " + dir_pattern)
                if not self.exclude_pattern(None, prefix=dir_pattern):
                    self.warn \
                        (("no previously-included directories found " +
                          "matching '%s'") %
                         dir_pattern)
            else:
                raise RuntimeError, \
                      "this cannot happen: invalid action '%s'" % action

    # process_line ()




    def select_pattern (self, pattern,
                        anchor=1, prefix=None, is_regex=0):
        """Select strings (presumably filenames) from 'files' that match
        'pattern', a Unix-style wildcard (glob) pattern.  Patterns are not
        quite the same as implemented by the 'fnmatch' module: '*' and '?'
        match non-special characters, where "special" is platform-dependent:
        slash on Unix, colon, slash, and backslash on DOS/Windows, and colon on
        Mac OS.

        If 'anchor' is true (the default), then the pattern match is more
        stringent: "*.py" will match "foo.py" but not "foo/bar.py".  If
        'anchor' is false, both of these will match.

        If 'prefix' is supplied, then only filenames starting with 'prefix'
        (itself a pattern) and ending with 'pattern', with anything in between
        them, will match.  'anchor' is ignored in this case.

        If 'is_regex' is true, 'anchor' and 'prefix' are ignored, and
        'pattern' is assumed to be either a string containing a regex or a
        regex object -- no translation is done, the regex is just compiled
        and used as-is.

        Selected strings will be added to self.files.

        Return 1 if files are found.
        """
        files_found = 0
        pattern_re = translate_pattern (pattern, anchor, prefix, is_regex)
        self.debug_print("select_pattern: applying regex r'%s'" %
                         pattern_re.pattern)

        # delayed loading of allfiles list
        if self.allfiles is None: self.allfiles = findall (self.dir)

        for name in self.allfiles:
            if pattern_re.search (name):
                self.debug_print(" adding " + name)
                self.files.append (name)
                files_found = 1
    
        return files_found

    # select_pattern ()


    def exclude_pattern (self, pattern,
                         anchor=1, prefix=None, is_regex=0):
        """Remove strings (presumably filenames) from 'files' that match
        'pattern'.  Other parameters are the same as for
        'select_pattern()', above.  
        The list 'self.files' is modified in place.
        Return 1 if files are found.
        """
        files_found = 0
        pattern_re = translate_pattern (pattern, anchor, prefix, is_regex)
        self.debug_print("exclude_pattern: applying regex r'%s'" %
                         pattern_re.pattern)
        for i in range (len(self.files)-1, -1, -1):
            if pattern_re.search (self.files[i]):
                self.debug_print(" removing " + self.files[i])
                del self.files[i]
                files_found = 1
    
        return files_found

    # exclude_pattern ()


    def recursive_exclude_pattern (self, dir, pattern=None):
        """Remove filenames from 'self.files' that are under 'dir' and
        whose basenames match 'pattern'.
        Return 1 if files are found.
        """
        files_found = 0
        self.debug_print("recursive_exclude_pattern: dir=%s, pattern=%s" %
                         (dir, pattern))
        if pattern is None:
            pattern_re = None
        else:
            pattern_re = translate_pattern (pattern)

        for i in range (len (self.files)-1, -1, -1):
            (cur_dir, cur_base) = os.path.split (self.files[i])
            if (cur_dir == dir and
                (pattern_re is None or pattern_re.match (cur_base))):
                self.debug_print("removing %s" % self.files[i])
                del self.files[i]
                files_found = 1
    
        return files_found

# class FileList


# ----------------------------------------------------------------------
# Utility functions

def findall (dir = os.curdir):
    """Find all files under 'dir' and return the list of full filenames
    (relative to 'dir').
    """
    from stat import ST_MODE, S_ISREG, S_ISDIR, S_ISLNK

    list = []
    stack = [dir]
    pop = stack.pop
    push = stack.append

    while stack:
        dir = pop()
        names = os.listdir (dir)

        for name in names:
            if dir != os.curdir:        # avoid the dreaded "./" syndrome
                fullname = os.path.join (dir, name)
            else:
                fullname = name

            # Avoid excess stat calls -- just one will do, thank you!
            stat = os.stat(fullname)
            mode = stat[ST_MODE]
            if S_ISREG(mode):
                list.append (fullname)
            elif S_ISDIR(mode) and not S_ISLNK(mode):
                push (fullname)

    return list


def glob_to_re (pattern):
    """Translate a shell-like glob pattern to a regular expression; return
    a string containing the regex.  Differs from 'fnmatch.translate()' in
    that '*' does not match "special characters" (which are
    platform-specific).
    """
    pattern_re = fnmatch.translate (pattern)

    # '?' and '*' in the glob pattern become '.' and '.*' in the RE, which
    # IMHO is wrong -- '?' and '*' aren't supposed to match slash in Unix,
    # and by extension they shouldn't match such "special characters" under
    # any OS.  So change all non-escaped dots in the RE to match any
    # character except the special characters.
    # XXX currently the "special characters" are just slash -- i.e. this is
    # Unix-only.
    pattern_re = re.sub (r'(^|[^\\])\.', r'\1[^/]', pattern_re)
    return pattern_re

# glob_to_re ()


def translate_pattern (pattern, anchor=1, prefix=None, is_regex=0):
    """Translate a shell-like wildcard pattern to a compiled regular
    expression.  Return the compiled regex.  If 'is_regex' true,
    then 'pattern' is directly compiled to a regex (if it's a string)
    or just returned as-is (assumes it's a regex object).
    """
    if is_regex:
        if type(pattern) is StringType:
            return re.compile(pattern)
        else:
            return pattern

    if pattern:
        pattern_re = glob_to_re (pattern)
    else:
        pattern_re = ''
        
    if prefix is not None:
        prefix_re = (glob_to_re (prefix))[0:-1] # ditch trailing $
        pattern_re = "^" + os.path.join (prefix_re, ".*" + pattern_re)
    else:                               # no prefix -- respect anchor flag
        if anchor:
            pattern_re = "^" + pattern_re
        
    return re.compile (pattern_re)

# translate_pattern ()
