# Test some Unicode file name semantics
# We dont test many operations on files other than
# that their names can be used with Unicode characters.
import os, glob, time, shutil

import unittest
from test.test_support import run_suite, TestSkipped, TESTFN_UNICODE
from test.test_support import TESTFN_ENCODING, TESTFN_UNICODE_UNENCODEABLE
try:
    TESTFN_ENCODED = TESTFN_UNICODE.encode(TESTFN_ENCODING)
except (UnicodeError, TypeError):
    # Either the file system encoding is None, or the file name
    # cannot be encoded in the file system encoding.
    raise TestSkipped("No Unicode filesystem semantics on this platform.")

def remove_if_exists(filename):
    if os.path.exists(filename):
        os.unlink(filename)

class TestUnicodeFiles(unittest.TestCase):
    # The 'do_' functions are the actual tests.  They generally assume the
    # file already exists etc.
    
    # Do all the tests we can given only a single filename.  The file should
    # exist.
    def _do_single(self, filename):
        self.failUnless(os.path.exists(filename))
        self.failUnless(os.path.isfile(filename))
        self.failUnless(os.path.exists(os.path.abspath(filename)))
        self.failUnless(os.path.isfile(os.path.abspath(filename)))
        os.chmod(filename, 0777)
        os.utime(filename, None)
        os.utime(filename, (time.time(), time.time()))
        # Copy/rename etc tests using the same filename
        self._do_copyish(filename, filename)
        # Filename should appear in glob output
        self.failUnless(
            os.path.abspath(filename)==os.path.abspath(glob.glob(filename)[0]))
        # basename should appear in listdir.
        path, base = os.path.split(os.path.abspath(filename))
        self.failUnless(base in os.listdir(path))
    
    # Do as many "equivalancy' tests as we can - ie, check that although we
    # have different types for the filename, they refer to the same file.
    def _do_equivilent(self, filename1, filename2):
        # Note we only check "filename1 against filename2" - we don't bother
        # checking "filename2 against 1", as we assume we are called again with
        # the args reversed.
        self.failUnless(type(filename1)!=type(filename2),
                    "No point checking equivalent filenames of the same type")
        # stat and lstat should return the same results.
        self.failUnlessEqual(os.stat(filename1),
                             os.stat(filename2))
        self.failUnlessEqual(os.lstat(filename1),
                             os.lstat(filename2))
        # Copy/rename etc tests using equivalent filename
        self._do_copyish(filename1, filename2)

    # Tests that copy, move, etc one file to another.
    def _do_copyish(self, filename1, filename2):
        # Should be able to rename the file using either name.
        self.failUnless(os.path.isfile(filename1)) # must exist.
        os.rename(filename1, filename2 + ".new")
        self.failUnless(os.path.isfile(filename1+".new"))
        os.rename(filename1 + ".new", filename2)
        self.failUnless(os.path.isfile(filename2))

        # Try using shutil on the filenames.
        try:
            filename1==filename2
        except UnicodeDecodeError:
            # these filenames can't be compared - shutil.copy tries to do
            # just that.  This is really a bug in 'shutil' - if one of shutil's
            # 2 params are Unicode and the other isn't, it should coerce the
            # string to Unicode with the filesystem encoding before comparison.
            pass
        else:
            # filenames can be compared.
            shutil.copy(filename1, filename2 + ".new")
            os.unlink(filename1 + ".new") # remove using equiv name.
            # And a couple of moves, one using each name.
            shutil.move(filename1, filename2 + ".new")
            self.failUnless(not os.path.exists(filename2))
            shutil.move(filename1 + ".new", filename2)
            self.failUnless(os.path.exists(filename1))
            # Note - due to the implementation of shutil.move,
            # it tries a rename first.  This only fails on Windows when on
            # different file systems - and this test can't ensure that.
            # So we test the shutil.copy2 function, which is the thing most
            # likely to fail.
            shutil.copy2(filename1, filename2 + ".new")
            os.unlink(filename1 + ".new")

    def _do_directory(self, make_name, chdir_name, getcwd_func):
        cwd = os.getcwd()
        if os.path.isdir(make_name):
            os.rmdir(make_name)
        os.mkdir(make_name)
        try:
            os.chdir(chdir_name)
            try:
                self.failUnlessEqual(os.path.basename(getcwd_func()),
                                     make_name)
            finally:
                os.chdir(cwd)
        finally:
            os.rmdir(make_name)

    # The '_test' functions 'entry points with params' - ie, what the
    # top-level 'test' functions would be if they could take params
    def _test_single(self, filename):
        remove_if_exists(filename)
        f = file(filename, "w")
        f.close()
        try:
            self._do_single(filename)
        finally:
            os.unlink(filename)
        self.failUnless(not os.path.exists(filename))
        # and again with os.open.
        f = os.open(filename, os.O_CREAT)
        os.close(f)
        try:
            self._do_single(filename)
        finally:
            os.unlink(filename)
    
    def _test_equivalent(self, filename1, filename2):
        remove_if_exists(filename1)
        self.failUnless(not os.path.exists(filename2))
        f = file(filename1, "w")
        f.close()
        try:
            self._do_equivilent(filename1, filename2)
        finally:
            os.unlink(filename1)

    # The 'test' functions are unittest entry points, and simply call our
    # _test functions with each of the filename combinations we wish to test
    def test_single_files(self):
        self._test_single(TESTFN_ENCODED)
        self._test_single(TESTFN_UNICODE)
        if TESTFN_UNICODE_UNENCODEABLE is not None:
            self._test_single(TESTFN_UNICODE_UNENCODEABLE)

    def test_equivalent_files(self):
        self._test_equivalent(TESTFN_ENCODED, TESTFN_UNICODE)
        self._test_equivalent(TESTFN_UNICODE, TESTFN_ENCODED)

    def test_directories(self):
        # For all 'equivilent' combinations:
        #  Make dir with encoded, chdir with unicode, checkdir with encoded
        #  (or unicode/encoded/unicode, etc
        ext = ".dir"
        self._do_directory(TESTFN_ENCODED+ext, TESTFN_ENCODED+ext, os.getcwd)
        self._do_directory(TESTFN_ENCODED+ext, TESTFN_UNICODE+ext, os.getcwd)
        self._do_directory(TESTFN_UNICODE+ext, TESTFN_ENCODED+ext, os.getcwdu)
        self._do_directory(TESTFN_UNICODE+ext, TESTFN_UNICODE+ext, os.getcwdu)
        # Our directory name that can't use a non-unicode name.
        if TESTFN_UNICODE_UNENCODEABLE is not None:
            self._do_directory(TESTFN_UNICODE_UNENCODEABLE+ext,
                               TESTFN_UNICODE_UNENCODEABLE+ext,
                               os.getcwdu)

def test_main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUnicodeFiles))
    run_suite(suite)

if __name__ == "__main__":
    test_main()
