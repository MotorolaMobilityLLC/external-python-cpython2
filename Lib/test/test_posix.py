"Test posix functions"

from test_support import TestSkipped, TestFailed, TESTFN, run_suite

try:
    import posix
except ImportError:
    raise TestSkipped, "posix is not available"

import time
import os
import sys
import unittest
import warnings
warnings.filterwarnings('ignore', '.* potential security risk .*',
                        RuntimeWarning)

class PosixTester(unittest.TestCase):

    def setUp(self):
        # create empty file
        fp = open(TESTFN, 'w+')
        fp.close()

    def tearDown(self):
        os.unlink(TESTFN)

    def testNoArgFunctions(self):
        # test posix functions which take no arguments and have
        # no side-effects which we need to cleanup (e.g., fork, wait, abort)
        NO_ARG_FUNCTIONS = [ "ctermid", "getcwd", "getcwdu", "uname",
                             "times", "getlogin", "getloadavg", "tmpnam",
                             "getegid", "geteuid", "getgid", "getgroups",
                             "getpid", "getpgrp", "getppid", "getuid",
                           ]
        for name in NO_ARG_FUNCTIONS:
            posix_func = getattr(posix, name, None)
            if posix_func is not None:
                posix_func()
                try:
                    posix_func(1)
                except TypeError:
                    pass
                else:
                    raise TestFailed, '%s should take no arguments' % name

    def test_statvfs(self):
        if hasattr(posix, 'statvfs'):
            posix.statvfs(os.curdir)

    def test_fstatvfs(self):
        if hasattr(posix, 'fstatvfs'):
            fp = open(TESTFN)
            try:
                posix.fstatvfs(fp.fileno())
            finally:
                fp.close()

    def test_ftruncate(self):
        if hasattr(posix, 'ftruncate'):
            fp = open(TESTFN, 'w+')
            try:
                # we need to have some data to truncate
                fp.write('test')
                fp.flush()
                posix.ftruncate(fp.fileno(), 0)
            finally:
                fp.close()

    def test_dup(self):
        if hasattr(posix, 'dup'):
            fp = open(TESTFN)
            try:
                fd = posix.dup(fp.fileno())
                os.close(fd)
            finally:
                fp.close()

    def test_dup2(self):
        if hasattr(posix, 'dup2'):
            fp1 = open(TESTFN)
            fp2 = open(TESTFN)
            try:
                posix.dup2(fp1.fileno(), fp2.fileno())
            finally:
                fp1.close()
                fp2.close()

    def fdopen_helper(self, *args):
        fd = os.open(TESTFN, os.O_RDONLY)
        fp2 = posix.fdopen(fd, *args)
        fp2.close()

    def test_fdopen(self):
        if hasattr(posix, 'fdopen'):
            self.fdopen_helper()
            self.fdopen_helper('r')
            self.fdopen_helper('r', 100)

    def test_fstat(self):
        if hasattr(posix, 'fstat'):
            fp = open(TESTFN)
            try:
                posix.fstat(fp.fileno())
            finally:
                fp.close()

    def test_stat(self):
        if hasattr(posix, 'stat'):
            posix.stat(TESTFN)

    def test_chdir(self):
        if hasattr(posix, 'chdir'):
            posix.chdir(os.curdir)
            try:
                posix.chdir(TESTFN)
            except OSError:
                pass
            else:
                raise TestFailed, \
                      'should not be able to change directory to a file'

    def test_lsdir(self):
        if hasattr(posix, 'lsdir'):
            if TESTFN not in posix.lsdir(os.curdir):
                raise TestFailed, \
                      '%s should exist in current directory' % TESTFN

    def test_access(self):
        if hasattr(posix, 'access'):
            if not posix.access(TESTFN, os.R_OK):
                raise TestFailed, 'should have read access to: %s' % TESTFN

    def test_umask(self):
        if hasattr(posix, 'umask'):
            old_mask = posix.umask(0)
            posix.umask(old_mask)

    def test_strerror(self):
        if hasattr(posix, 'strerror'):
            posix.strerror(0)

    def test_pipe(self):
        if hasattr(posix, 'pipe'):
            reader, writer = posix.pipe()
            os.close(reader)
            os.close(writer)

    def test_tempnam(self):
        if hasattr(posix, 'tempnam'):
            posix.tempnam()
            posix.tempnam(os.curdir)
            posix.tempnam(os.curdir, 'blah')

    def test_tmpfile(self):
        if hasattr(posix, 'tmpfile'):
            fp = posix.tmpfile()
            fp.close()

    def test_utime(self):
        if hasattr(posix, 'utime'):
            now = time.time()
            posix.utime(TESTFN, None)
            posix.utime(TESTFN, (now, now))

def test_main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PosixTester))
    run_suite(suite)

if __name__ == '__main__':
    test_main()
