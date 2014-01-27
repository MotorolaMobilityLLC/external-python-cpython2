import io
import sys
import os
import marshal
import imp
import struct
import time
import unittest

from test import test_support
from test.test_importhooks import ImportHooksBaseTestCase, test_src, test_co

# some tests can be ran even without zlib
try:
    import zlib
except ImportError:
    zlib = None

from zipfile import ZipFile, ZipInfo, ZIP_STORED, ZIP_DEFLATED

import zipimport
import linecache
import doctest
import inspect
import StringIO
from traceback import extract_tb, extract_stack, print_tb
raise_src = 'def do_raise(): raise TypeError\n'

def make_pyc(co, mtime):
    data = marshal.dumps(co)
    if type(mtime) is type(0.0):
        # Mac mtimes need a bit of special casing
        if mtime < 0x7fffffff:
            mtime = int(mtime)
        else:
            mtime = int(-0x100000000L + long(mtime))
    pyc = imp.get_magic() + struct.pack("<i", int(mtime)) + data
    return pyc

def module_path_to_dotted_name(path):
    return path.replace(os.sep, '.')

NOW = time.time()
test_pyc = make_pyc(test_co, NOW)


if __debug__:
    pyc_ext = ".pyc"
else:
    pyc_ext = ".pyo"


TESTMOD = "ziptestmodule"
TESTPACK = "ziptestpackage"
TESTPACK2 = "ziptestpackage2"
TEMP_ZIP = os.path.abspath("junk95142" + os.extsep + "zip")


def _write_zip_package(zipname, files,
                       data_to_prepend=b"", compression=ZIP_STORED):
    z = ZipFile(zipname, "w")
    try:
        for name, (mtime, data) in files.items():
            zinfo = ZipInfo(name, time.localtime(mtime))
            zinfo.compress_type = compression
            z.writestr(zinfo, data)
    finally:
        z.close()

    if data_to_prepend:
        # Prepend data to the start of the zipfile
        with open(zipname, "rb") as f:
            zip_data = f.read()

        with open(zipname, "wb") as f:
            f.write(data_to_prepend)
            f.write(zip_data)


class UncompressedZipImportTestCase(ImportHooksBaseTestCase):

    compression = ZIP_STORED

    def setUp(self):
        # We're reusing the zip archive path, so we must clear the
        # cached directory info and linecache
        linecache.clearcache()
        zipimport._zip_directory_cache.clear()
        ImportHooksBaseTestCase.setUp(self)

    def doTest(self, expected_ext, files, *modules, **kw):
        _write_zip_package(TEMP_ZIP, files, data_to_prepend=kw.get("stuff"),
                           compression=self.compression)
        try:
            sys.path.insert(0, TEMP_ZIP)

            mod = __import__(".".join(modules), globals(), locals(),
                             ["__dummy__"])

            call = kw.get('call')
            if call is not None:
                call(mod)

            if expected_ext:
                file = mod.get_file()
                self.assertEqual(file, os.path.join(TEMP_ZIP,
                                 *modules) + expected_ext)
        finally:
            os.remove(TEMP_ZIP)

    def testAFakeZlib(self):
        #
        # This could cause a stack overflow before: importing zlib.py
        # from a compressed archive would cause zlib to be imported
        # which would find zlib.py in the archive, which would... etc.
        #
        # This test *must* be executed first: it must be the first one
        # to trigger zipimport to import zlib (zipimport caches the
        # zlib.decompress function object, after which the problem being
        # tested here wouldn't be a problem anymore...
        # (Hence the 'A' in the test method name: to make it the first
        # item in a list sorted by name, like unittest.makeSuite() does.)
        #
        # This test fails on platforms on which the zlib module is
        # statically linked, but the problem it tests for can't
        # occur in that case (builtin modules are always found first),
        # so we'll simply skip it then. Bug #765456.
        #
        if "zlib" in sys.builtin_module_names:
            self.skipTest('zlib is a builtin module')
        if "zlib" in sys.modules:
            del sys.modules["zlib"]
        files = {"zlib.py": (NOW, test_src)}
        try:
            self.doTest(".py", files, "zlib")
        except ImportError:
            if self.compression != ZIP_DEFLATED:
                self.fail("expected test to not raise ImportError")
        else:
            if self.compression != ZIP_STORED:
                self.fail("expected test to raise ImportError")

    def testPy(self):
        files = {TESTMOD + ".py": (NOW, test_src)}
        self.doTest(".py", files, TESTMOD)

    def testPyc(self):
        files = {TESTMOD + pyc_ext: (NOW, test_pyc)}
        self.doTest(pyc_ext, files, TESTMOD)

    def testBoth(self):
        files = {TESTMOD + ".py": (NOW, test_src),
                 TESTMOD + pyc_ext: (NOW, test_pyc)}
        self.doTest(pyc_ext, files, TESTMOD)

    def testEmptyPy(self):
        files = {TESTMOD + ".py": (NOW, "")}
        self.doTest(None, files, TESTMOD)

    def testBadMagic(self):
        # make pyc magic word invalid, forcing loading from .py
        m0 = ord(test_pyc[0])
        m0 ^= 0x04  # flip an arbitrary bit
        badmagic_pyc = chr(m0) + test_pyc[1:]
        files = {TESTMOD + ".py": (NOW, test_src),
                 TESTMOD + pyc_ext: (NOW, badmagic_pyc)}
        self.doTest(".py", files, TESTMOD)

    def testBadMagic2(self):
        # make pyc magic word invalid, causing an ImportError
        m0 = ord(test_pyc[0])
        m0 ^= 0x04  # flip an arbitrary bit
        badmagic_pyc = chr(m0) + test_pyc[1:]
        files = {TESTMOD + pyc_ext: (NOW, badmagic_pyc)}
        try:
            self.doTest(".py", files, TESTMOD)
        except ImportError:
            pass
        else:
            self.fail("expected ImportError; import from bad pyc")

    def testBadMTime(self):
        t3 = ord(test_pyc[7])
        t3 ^= 0x02  # flip the second bit -- not the first as that one
                    # isn't stored in the .py's mtime in the zip archive.
        badtime_pyc = test_pyc[:7] + chr(t3) + test_pyc[8:]
        files = {TESTMOD + ".py": (NOW, test_src),
                 TESTMOD + pyc_ext: (NOW, badtime_pyc)}
        self.doTest(".py", files, TESTMOD)

    def testPackage(self):
        packdir = TESTPACK + os.sep
        files = {packdir + "__init__" + pyc_ext: (NOW, test_pyc),
                 packdir + TESTMOD + pyc_ext: (NOW, test_pyc)}
        self.doTest(pyc_ext, files, TESTPACK, TESTMOD)

    def testDeepPackage(self):
        packdir = TESTPACK + os.sep
        packdir2 = packdir + TESTPACK2 + os.sep
        files = {packdir + "__init__" + pyc_ext: (NOW, test_pyc),
                 packdir2 + "__init__" + pyc_ext: (NOW, test_pyc),
                 packdir2 + TESTMOD + pyc_ext: (NOW, test_pyc)}
        self.doTest(pyc_ext, files, TESTPACK, TESTPACK2, TESTMOD)

    def testZipImporterMethods(self):
        packdir = TESTPACK + os.sep
        packdir2 = packdir + TESTPACK2 + os.sep
        files = {packdir + "__init__" + pyc_ext: (NOW, test_pyc),
                 packdir2 + "__init__" + pyc_ext: (NOW, test_pyc),
                 packdir2 + TESTMOD + pyc_ext: (NOW, test_pyc)}

        z = ZipFile(TEMP_ZIP, "w")
        try:
            for name, (mtime, data) in files.items():
                zinfo = ZipInfo(name, time.localtime(mtime))
                zinfo.compress_type = self.compression
                z.writestr(zinfo, data)
            z.close()

            zi = zipimport.zipimporter(TEMP_ZIP)
            self.assertEqual(zi.archive, TEMP_ZIP)
            self.assertEqual(zi.is_package(TESTPACK), True)
            mod = zi.load_module(TESTPACK)
            self.assertEqual(zi.get_filename(TESTPACK), mod.__file__)

            self.assertEqual(zi.is_package(packdir + '__init__'), False)
            self.assertEqual(zi.is_package(packdir + TESTPACK2), True)
            self.assertEqual(zi.is_package(packdir2 + TESTMOD), False)

            mod_path = packdir2 + TESTMOD
            mod_name = module_path_to_dotted_name(mod_path)
            __import__(mod_name)
            mod = sys.modules[mod_name]
            self.assertEqual(zi.get_source(TESTPACK), None)
            self.assertEqual(zi.get_source(mod_path), None)
            self.assertEqual(zi.get_filename(mod_path), mod.__file__)
            # To pass in the module name instead of the path, we must use the right importer
            loader = mod.__loader__
            self.assertEqual(loader.get_source(mod_name), None)
            self.assertEqual(loader.get_filename(mod_name), mod.__file__)

            # test prefix and archivepath members
            zi2 = zipimport.zipimporter(TEMP_ZIP + os.sep + TESTPACK)
            self.assertEqual(zi2.archive, TEMP_ZIP)
            self.assertEqual(zi2.prefix, TESTPACK + os.sep)
        finally:
            z.close()
            os.remove(TEMP_ZIP)

    def testZipImporterMethodsInSubDirectory(self):
        packdir = TESTPACK + os.sep
        packdir2 = packdir + TESTPACK2 + os.sep
        files = {packdir2 + "__init__" + pyc_ext: (NOW, test_pyc),
                 packdir2 + TESTMOD + pyc_ext: (NOW, test_pyc)}

        z = ZipFile(TEMP_ZIP, "w")
        try:
            for name, (mtime, data) in files.items():
                zinfo = ZipInfo(name, time.localtime(mtime))
                zinfo.compress_type = self.compression
                z.writestr(zinfo, data)
            z.close()

            zi = zipimport.zipimporter(TEMP_ZIP + os.sep + packdir)
            self.assertEqual(zi.archive, TEMP_ZIP)
            self.assertEqual(zi.prefix, packdir)
            self.assertEqual(zi.is_package(TESTPACK2), True)
            mod = zi.load_module(TESTPACK2)
            self.assertEqual(zi.get_filename(TESTPACK2), mod.__file__)

            self.assertEqual(zi.is_package(TESTPACK2 + os.sep + '__init__'), False)
            self.assertEqual(zi.is_package(TESTPACK2 + os.sep + TESTMOD), False)

            mod_path = TESTPACK2 + os.sep + TESTMOD
            mod_name = module_path_to_dotted_name(mod_path)
            __import__(mod_name)
            mod = sys.modules[mod_name]
            self.assertEqual(zi.get_source(TESTPACK2), None)
            self.assertEqual(zi.get_source(mod_path), None)
            self.assertEqual(zi.get_filename(mod_path), mod.__file__)
            # To pass in the module name instead of the path, we must use the right importer
            loader = mod.__loader__
            self.assertEqual(loader.get_source(mod_name), None)
            self.assertEqual(loader.get_filename(mod_name), mod.__file__)
        finally:
            z.close()
            os.remove(TEMP_ZIP)

    def testGetData(self):
        z = ZipFile(TEMP_ZIP, "w")
        z.compression = self.compression
        try:
            name = "testdata.dat"
            data = "".join([chr(x) for x in range(256)]) * 500
            z.writestr(name, data)
            z.close()
            zi = zipimport.zipimporter(TEMP_ZIP)
            self.assertEqual(data, zi.get_data(name))
            self.assertIn('zipimporter object', repr(zi))
        finally:
            z.close()
            os.remove(TEMP_ZIP)

    def testImporterAttr(self):
        src = """if 1:  # indent hack
        def get_file():
            return __file__
        if __loader__.get_data("some.data") != "some data":
            raise AssertionError, "bad data"\n"""
        pyc = make_pyc(compile(src, "<???>", "exec"), NOW)
        files = {TESTMOD + pyc_ext: (NOW, pyc),
                 "some.data": (NOW, "some data")}
        self.doTest(pyc_ext, files, TESTMOD)

    def testImport_WithStuff(self):
        # try importing from a zipfile which contains additional
        # stuff at the beginning of the file
        files = {TESTMOD + ".py": (NOW, test_src)}
        self.doTest(".py", files, TESTMOD,
                    stuff="Some Stuff"*31)

    def assertModuleSource(self, module):
        self.assertEqual(inspect.getsource(module), test_src)

    def testGetSource(self):
        files = {TESTMOD + ".py": (NOW, test_src)}
        self.doTest(".py", files, TESTMOD, call=self.assertModuleSource)

    def testGetCompiledSource(self):
        pyc = make_pyc(compile(test_src, "<???>", "exec"), NOW)
        files = {TESTMOD + ".py": (NOW, test_src),
                 TESTMOD + pyc_ext: (NOW, pyc)}
        self.doTest(pyc_ext, files, TESTMOD, call=self.assertModuleSource)

    def runDoctest(self, callback):
        files = {TESTMOD + ".py": (NOW, test_src),
                 "xyz.txt": (NOW, ">>> log.append(True)\n")}
        self.doTest(".py", files, TESTMOD, call=callback)

    def doDoctestFile(self, module):
        log = []
        old_master, doctest.master = doctest.master, None
        try:
            doctest.testfile(
                'xyz.txt', package=module, module_relative=True,
                globs=locals()
            )
        finally:
            doctest.master = old_master
        self.assertEqual(log,[True])

    def testDoctestFile(self):
        self.runDoctest(self.doDoctestFile)

    def doDoctestSuite(self, module):
        log = []
        doctest.DocFileTest(
            'xyz.txt', package=module, module_relative=True,
            globs=locals()
        ).run()
        self.assertEqual(log,[True])

    def testDoctestSuite(self):
        self.runDoctest(self.doDoctestSuite)

    def doTraceback(self, module):
        try:
            module.do_raise()
        except:
            tb = sys.exc_info()[2].tb_next

            f,lno,n,line = extract_tb(tb, 1)[0]
            self.assertEqual(line, raise_src.strip())

            f,lno,n,line = extract_stack(tb.tb_frame, 1)[0]
            self.assertEqual(line, raise_src.strip())

            s = StringIO.StringIO()
            print_tb(tb, 1, s)
            self.assertTrue(s.getvalue().endswith(raise_src))
        else:
            raise AssertionError("This ought to be impossible")

    def testTraceback(self):
        files = {TESTMOD + ".py": (NOW, raise_src)}
        self.doTest(None, files, TESTMOD, call=self.doTraceback)


@unittest.skipUnless(zlib, "requires zlib")
class CompressedZipImportTestCase(UncompressedZipImportTestCase):
    compression = ZIP_DEFLATED


class ZipFileModifiedAfterImportTestCase(ImportHooksBaseTestCase):
    def setUp(self):
        zipimport._zip_directory_cache.clear()
        zipimport._zip_stat_cache.clear()
        # save sys.modules so we can unimport everything done by our tests.
        self._sys_modules_orig = dict(sys.modules)
        ImportHooksBaseTestCase.setUp(self)

    def tearDown(self):
        ImportHooksBaseTestCase.tearDown(self)
        # The closest we can come to un-importing our zipped up test modules.
        sys.modules.clear()
        sys.modules.update(self._sys_modules_orig)
        if os.path.exists(TEMP_ZIP):
            os.remove(TEMP_ZIP)

    def setUpZipFileModuleAndTestImports(self):
        # Create a .zip file to test with
        self.zipfile_path = TEMP_ZIP
        packdir = TESTPACK + os.sep
        files = {packdir + "__init__" + pyc_ext: (NOW, test_pyc),
                 packdir + TESTMOD + ".py": (NOW, "test_value = 38\n"),
                 "ziptest_a.py": (NOW, "test_value = 23\n"),
                 "ziptest_b.py": (NOW, "test_value = 42\n"),
                 "ziptest_c.py": (NOW, "test_value = 1337\n")}
        _write_zip_package(self.zipfile_path, files)
        self.assertTrue(os.path.exists(self.zipfile_path))
        sys.path.insert(0, self.zipfile_path)

        self.testpack_testmod = TESTPACK + "." + TESTMOD

        with io.open(self.zipfile_path, "rb") as orig_zip_file:
            self.orig_zip_file_contents = orig_zip_file.read()

        # Import something out of the zipfile and confirm it is correct.
        testmod = __import__(self.testpack_testmod,
                             globals(), locals(), ["__dummy__"])
        self.assertEqual(testmod.test_value, 38)
        del sys.modules[TESTPACK]
        del sys.modules[self.testpack_testmod]

        # Import something else out of the zipfile and confirm it is correct.
        ziptest_b = __import__("ziptest_b", globals(), locals(), ["test_value"])
        self.assertEqual(ziptest_b.test_value, 42)
        del sys.modules["ziptest_b"]

    def truncateAndFillZipWithNonZipGarbage(self):
        with io.open(self.zipfile_path, "wb") as byebye_valid_zip_file:
            byebye_valid_zip_file.write(b"Tear down this wall!\n"*1987)

    def restoreZipFileWithDifferentHeaderOffsets(self):
        """Make it a valid zipfile with some garbage at the start."""
        # This alters all of the caches offsets within the file.
        with io.open(self.zipfile_path, "wb") as new_zip_file:
            new_zip_file.write(b"X"*1991)  # The year Python was created.
            new_zip_file.write(self.orig_zip_file_contents)

    def testZipFileChangesAfterFirstImport(self):
        """Alter the zip file after caching its index and try an import."""
        self.setUpZipFileModuleAndTestImports()
        # The above call cached the .zip table of contents during its tests.
        self.truncateAndFillZipWithNonZipGarbage()
        # Now that the zipfile has been replaced, import something else from it
        # which should fail as the file contents are now garbage.
        with self.assertRaises(ImportError):
            ziptest_a = __import__("ziptest_a", globals(), locals(),
                                   ["test_value"])
        # The code path used by the __import__ call is different than
        # that used by import statements.  Try these as well.  Some of
        # these may create new zipimporter instances.  We need to
        # function properly using the global zipimport caches
        # regardless of how many zipimporter instances for the same
        # .zip file exist.
        with self.assertRaises(ImportError):
            import ziptest_a
        with self.assertRaises(ImportError):
            from ziptest_a import test_value
        with self.assertRaises(ImportError):
            exec("from {} import {}".format(TESTPACK, TESTMOD))

        # Alters all of the offsets within the file
        self.restoreZipFileWithDifferentHeaderOffsets()

        # Now that the zip file has been "restored" to a valid but different
        # zipfile all zipimporter instances should *successfully* re-read the
        # new file's end of file central index and be able to import again.

        # Importing a submodule triggers a different import code path.
        exec("import " + self.testpack_testmod)
        self.assertEqual(getattr(locals()[TESTPACK], TESTMOD).test_value, 38)
        exec("from {} import {}".format(TESTPACK, TESTMOD))
        self.assertEqual(locals()[TESTMOD].test_value, 38)

        ziptest_a = __import__("ziptest_a", globals(), locals(), ["test_value"])
        self.assertEqual(ziptest_a.test_value, 23)
        ziptest_c = __import__("ziptest_c", globals(), locals(), ["test_value"])
        self.assertEqual(ziptest_c.test_value, 1337)

    def testZipFileSubpackageImport(self):
        """Import via multiple sys.path entries into parts of the zip."""
        self.setUpZipFileModuleAndTestImports()
        # Put a subdirectory within the zip file into the import path.
        sys.path.insert(0, self.zipfile_path + os.sep + TESTPACK)

        testmod = __import__(TESTMOD, globals(), locals(), ["test_value"])
        self.assertEqual(testmod.test_value, 38)
        del sys.modules[TESTMOD]
        exec("from {} import test_value".format(TESTMOD))
        self.assertEqual(test_value, 38)
        del sys.modules[TESTMOD]

        # Confirm that imports from the top level of the zip file
        # (already in sys.path from the setup call above) still work.
        ziptest_a = __import__("ziptest_a", globals(), locals(), ["test_value"])
        self.assertEqual(ziptest_a.test_value, 23)
        del sys.modules["ziptest_a"]
        import ziptest_c
        self.assertEqual(ziptest_c.test_value, 1337)
        del sys.modules["ziptest_c"]

        self.truncateAndFillZipWithNonZipGarbage()
        # Imports should now fail.
        with self.assertRaises(ImportError):
            testmod = __import__(TESTMOD, globals(), locals(), ["test_value"])
        with self.assertRaises(ImportError):
            exec("from {} import test_value".format(TESTMOD))
        with self.assertRaises(ImportError):
            import ziptest_a

        self.restoreZipFileWithDifferentHeaderOffsets()
        # Imports should work again, the central directory TOC will be re-read.
        testmod = __import__(TESTMOD, globals(), locals(), ["test_value"])
        self.assertEqual(testmod.test_value, 38)
        del sys.modules[TESTMOD]
        exec("from {} import test_value".format(TESTMOD))
        self.assertEqual(test_value, 38)

        ziptest_a = __import__("ziptest_a", globals(), locals(), ["test_value"])
        self.assertEqual(ziptest_a.test_value, 23)
        import ziptest_c
        self.assertEqual(ziptest_c.test_value, 1337)


class BadFileZipImportTestCase(unittest.TestCase):
    def assertZipFailure(self, filename):
        self.assertRaises(zipimport.ZipImportError,
                          zipimport.zipimporter, filename)

    def testNoFile(self):
        self.assertZipFailure('AdfjdkFJKDFJjdklfjs')

    def testEmptyFilename(self):
        self.assertZipFailure('')

    def testBadArgs(self):
        self.assertRaises(TypeError, zipimport.zipimporter, None)
        self.assertRaises(TypeError, zipimport.zipimporter, TESTMOD, kwd=None)

    def testFilenameTooLong(self):
        self.assertZipFailure('A' * 33000)

    def testEmptyFile(self):
        test_support.unlink(TESTMOD)
        open(TESTMOD, 'w+').close()
        self.assertZipFailure(TESTMOD)

    def testFileUnreadable(self):
        test_support.unlink(TESTMOD)
        fd = os.open(TESTMOD, os.O_CREAT, 000)
        try:
            os.close(fd)
            self.assertZipFailure(TESTMOD)
        finally:
            # If we leave "the read-only bit" set on Windows, nothing can
            # delete TESTMOD, and later tests suffer bogus failures.
            os.chmod(TESTMOD, 0666)
            test_support.unlink(TESTMOD)

    def testNotZipFile(self):
        test_support.unlink(TESTMOD)
        fp = open(TESTMOD, 'w+')
        fp.write('a' * 22)
        fp.close()
        self.assertZipFailure(TESTMOD)

    # XXX: disabled until this works on Big-endian machines
    def _testBogusZipFile(self):
        test_support.unlink(TESTMOD)
        fp = open(TESTMOD, 'w+')
        fp.write(struct.pack('=I', 0x06054B50))
        fp.write('a' * 18)
        fp.close()
        z = zipimport.zipimporter(TESTMOD)

        try:
            self.assertRaises(TypeError, z.find_module, None)
            self.assertRaises(TypeError, z.load_module, None)
            self.assertRaises(TypeError, z.is_package, None)
            self.assertRaises(TypeError, z.get_code, None)
            self.assertRaises(TypeError, z.get_data, None)
            self.assertRaises(TypeError, z.get_source, None)

            error = zipimport.ZipImportError
            self.assertEqual(z.find_module('abc'), None)

            self.assertRaises(error, z.load_module, 'abc')
            self.assertRaises(error, z.get_code, 'abc')
            self.assertRaises(IOError, z.get_data, 'abc')
            self.assertRaises(error, z.get_source, 'abc')
            self.assertRaises(error, z.is_package, 'abc')
        finally:
            zipimport._zip_directory_cache.clear()


def test_main():
    try:
        test_support.run_unittest(
              UncompressedZipImportTestCase,
              CompressedZipImportTestCase,
              BadFileZipImportTestCase,
              ZipFileModifiedAfterImportTestCase,
            )
    finally:
        test_support.unlink(TESTMOD)

if __name__ == "__main__":
    test_main()
