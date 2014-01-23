import unittest
import sys
import os
import _testcapi
from test import test_support
from subprocess import Popen, PIPE

# Skip this test if the _tkinter module wasn't built.
_tkinter = test_support.import_module('_tkinter')

from Tkinter import Tcl
from _tkinter import TclError

tcl_version = _tkinter.TCL_VERSION.split('.')
try:
    for i in range(len(tcl_version)):
        tcl_version[i] = int(tcl_version[i])
except ValueError:
    pass
tcl_version = tuple(tcl_version)


class TkinterTest(unittest.TestCase):

    def testFlattenLen(self):
        # flatten(<object with no length>)
        self.assertRaises(TypeError, _tkinter._flatten, True)


class TclTest(unittest.TestCase):

    def setUp(self):
        self.interp = Tcl()
        self.wantobjects = self.interp.tk.wantobjects()

    def testEval(self):
        tcl = self.interp
        tcl.eval('set a 1')
        self.assertEqual(tcl.eval('set a'),'1')

    def testEvalException(self):
        tcl = self.interp
        self.assertRaises(TclError,tcl.eval,'set a')

    def testEvalException2(self):
        tcl = self.interp
        self.assertRaises(TclError,tcl.eval,'this is wrong')

    def testCall(self):
        tcl = self.interp
        tcl.call('set','a','1')
        self.assertEqual(tcl.call('set','a'),'1')

    def testCallException(self):
        tcl = self.interp
        self.assertRaises(TclError,tcl.call,'set','a')

    def testCallException2(self):
        tcl = self.interp
        self.assertRaises(TclError,tcl.call,'this','is','wrong')

    def testSetVar(self):
        tcl = self.interp
        tcl.setvar('a','1')
        self.assertEqual(tcl.eval('set a'),'1')

    def testSetVarArray(self):
        tcl = self.interp
        tcl.setvar('a(1)','1')
        self.assertEqual(tcl.eval('set a(1)'),'1')

    def testGetVar(self):
        tcl = self.interp
        tcl.eval('set a 1')
        self.assertEqual(tcl.getvar('a'),'1')

    def testGetVarArray(self):
        tcl = self.interp
        tcl.eval('set a(1) 1')
        self.assertEqual(tcl.getvar('a(1)'),'1')

    def testGetVarException(self):
        tcl = self.interp
        self.assertRaises(TclError,tcl.getvar,'a')

    def testGetVarArrayException(self):
        tcl = self.interp
        self.assertRaises(TclError,tcl.getvar,'a(1)')

    def testUnsetVar(self):
        tcl = self.interp
        tcl.setvar('a',1)
        self.assertEqual(tcl.eval('info exists a'),'1')
        tcl.unsetvar('a')
        self.assertEqual(tcl.eval('info exists a'),'0')

    def testUnsetVarArray(self):
        tcl = self.interp
        tcl.setvar('a(1)',1)
        tcl.setvar('a(2)',2)
        self.assertEqual(tcl.eval('info exists a(1)'),'1')
        self.assertEqual(tcl.eval('info exists a(2)'),'1')
        tcl.unsetvar('a(1)')
        self.assertEqual(tcl.eval('info exists a(1)'),'0')
        self.assertEqual(tcl.eval('info exists a(2)'),'1')

    def testUnsetVarException(self):
        tcl = self.interp
        self.assertRaises(TclError,tcl.unsetvar,'a')

    def testEvalFile(self):
        tcl = self.interp
        filename = "testEvalFile.tcl"
        fd = open(filename,'w')
        script = """set a 1
        set b 2
        set c [ expr $a + $b ]
        """
        fd.write(script)
        fd.close()
        tcl.evalfile(filename)
        os.remove(filename)
        self.assertEqual(tcl.eval('set a'),'1')
        self.assertEqual(tcl.eval('set b'),'2')
        self.assertEqual(tcl.eval('set c'),'3')

    def testEvalFileException(self):
        tcl = self.interp
        filename = "doesnotexists"
        try:
            os.remove(filename)
        except Exception,e:
            pass
        self.assertRaises(TclError,tcl.evalfile,filename)

    def testPackageRequireException(self):
        tcl = self.interp
        self.assertRaises(TclError,tcl.eval,'package require DNE')

    @unittest.skipUnless(sys.platform == 'win32', "only applies to Windows")
    def testLoadWithUNC(self):
        # Build a UNC path from the regular path.
        # Something like
        #   \\%COMPUTERNAME%\c$\python27\python.exe

        fullname = os.path.abspath(sys.executable)
        if fullname[1] != ':':
            self.skipTest('unusable path: %r' % fullname)
        unc_name = r'\\%s\%s$\%s' % (os.environ['COMPUTERNAME'],
                                    fullname[0],
                                    fullname[3:])

        with test_support.EnvironmentVarGuard() as env:
            env.unset("TCL_LIBRARY")
            cmd = '%s -c "import Tkinter; print Tkinter"' % (unc_name,)

            try:
                p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            except WindowsError as e:
                if e.winerror == 5:
                    self.skipTest('Not permitted to start the child process')
                else:
                    raise

            out_data, err_data = p.communicate()

            msg = '\n\n'.join(['"Tkinter.py" not in output',
                               'Command:', cmd,
                               'stdout:', out_data,
                               'stderr:', err_data])

            self.assertIn('Tkinter.py', out_data, msg)

            self.assertEqual(p.wait(), 0, 'Non-zero exit code')


    def test_passing_values(self):
        def passValue(value):
            return self.interp.call('set', '_', value)

        self.assertEqual(passValue(True), True if self.wantobjects else '1')
        self.assertEqual(passValue(False), False if self.wantobjects else '0')
        self.assertEqual(passValue(u'string'), u'string')
        self.assertEqual(passValue(u'string\u20ac'), u'string\u20ac')
        for i in (0, 1, -1, int(2**31-1), int(-2**31)):
            self.assertEqual(passValue(i), i if self.wantobjects else str(i))
        for f in (0.0, 1.0, -1.0, 1//3, 1/3.0,
                  sys.float_info.min, sys.float_info.max,
                  -sys.float_info.min, -sys.float_info.max):
            if self.wantobjects:
                self.assertEqual(passValue(f), f)
            else:
                self.assertEqual(float(passValue(f)), f)
        if self.wantobjects:
            f = passValue(float('nan'))
            self.assertNotEqual(f, f)
            self.assertEqual(passValue(float('inf')), float('inf'))
            self.assertEqual(passValue(-float('inf')), -float('inf'))
        else:
            f = float(passValue(float('nan')))
            self.assertNotEqual(f, f)
            self.assertEqual(float(passValue(float('inf'))), float('inf'))
            self.assertEqual(float(passValue(-float('inf'))), -float('inf'))
        self.assertEqual(passValue((1, '2', (3.4,))),
                         (1, '2', (3.4,)) if self.wantobjects else '1 2 3.4')

    def test_user_command(self):
        result = []
        def testfunc(arg):
            result.append(arg)
            return arg
        self.interp.createcommand('testfunc', testfunc)
        def check(value, expected):
            del result[:]
            self.assertEqual(self.interp.call('testfunc', value), expected)
            self.assertEqual(result, [expected])

        check(True, '1')
        check(False, '0')
        check('string', 'string')
        check('string\xbd', 'string\xbd')
        check('string\u20ac', 'string\u20ac')
        for i in (0, 1, -1, 2**31-1, -2**31):
            check(i, str(i))
        for f in (0.0, 1.0, -1.0, 1/3,
                  sys.float_info.min, sys.float_info.max,
                  -sys.float_info.min, -sys.float_info.max):
            check(f, repr(f))
        check(float('nan'), 'NaN')
        check(float('inf'), 'Inf')
        check(-float('inf'), '-Inf')
        check((), '')
        check((1, (2,), (3, 4), '5 6', ()), '1 2 {3 4} {5 6} {}')

    def test_splitlist(self):
        splitlist = self.interp.tk.splitlist
        call = self.interp.tk.call
        self.assertRaises(TypeError, splitlist)
        self.assertRaises(TypeError, splitlist, 'a', 'b')
        self.assertRaises(TypeError, splitlist, 2)
        testcases = [
            ('2', ('2',)),
            ('', ()),
            ('{}', ('',)),
            ('""', ('',)),
            ('a\n b\t\r c\n ', ('a', 'b', 'c')),
            (u'a\n b\t\r c\n ', ('a', 'b', 'c')),
            ('a \xe2\x82\xac', ('a', '\xe2\x82\xac')),
            (u'a \u20ac', ('a', '\xe2\x82\xac')),
            ('a {b c}', ('a', 'b c')),
            (r'a b\ c', ('a', 'b c')),
            (('a', 'b c'), ('a', 'b c')),
            ('a 2', ('a', '2')),
            (('a', 2), ('a', 2)),
            ('a 3.4', ('a', '3.4')),
            (('a', 3.4), ('a', 3.4)),
            ((), ()),
            (call('list', 1, '2', (3.4,)),
                (1, '2', (3.4,)) if self.wantobjects else
                ('1', '2', '3.4')),
        ]
        if tcl_version >= (8, 5):
            testcases += [
                (call('dict', 'create', 1, u'\u20ac', '\xe2\x82\xac', (3.4,)),
                    (1, u'\u20ac', u'\u20ac', (3.4,)) if self.wantobjects else
                    ('1', '\xe2\x82\xac', '\xe2\x82\xac', '3.4')),
            ]
        for arg, res in testcases:
            self.assertEqual(splitlist(arg), res)
        self.assertRaises(TclError, splitlist, '{')

    def test_split(self):
        split = self.interp.tk.split
        call = self.interp.tk.call
        self.assertRaises(TypeError, split)
        self.assertRaises(TypeError, split, 'a', 'b')
        self.assertRaises(TypeError, split, 2)
        testcases = [
            ('2', '2'),
            ('', ''),
            ('{}', ''),
            ('""', ''),
            ('{', '{'),
            ('a\n b\t\r c\n ', ('a', 'b', 'c')),
            (u'a\n b\t\r c\n ', ('a', 'b', 'c')),
            ('a \xe2\x82\xac', ('a', '\xe2\x82\xac')),
            (u'a \u20ac', ('a', '\xe2\x82\xac')),
            ('a {b c}', ('a', ('b', 'c'))),
            (r'a b\ c', ('a', ('b', 'c'))),
            (('a', 'b c'), ('a', ('b', 'c'))),
            (('a', u'b c'), ('a', ('b', 'c'))),
            ('a 2', ('a', '2')),
            (('a', 2), ('a', 2)),
            ('a 3.4', ('a', '3.4')),
            (('a', 3.4), ('a', 3.4)),
            (('a', (2, 3.4)), ('a', (2, 3.4))),
            ((), ()),
            (call('list', 1, '2', (3.4,)),
                (1, '2', (3.4,)) if self.wantobjects else
                ('1', '2', '3.4')),
        ]
        if tcl_version >= (8, 5):
            testcases += [
                (call('dict', 'create', 12, u'\u20ac', '\xe2\x82\xac', (3.4,)),
                    (12, u'\u20ac', u'\u20ac', (3.4,)) if self.wantobjects else
                    ('12', '\xe2\x82\xac', '\xe2\x82\xac', '3.4')),
            ]
        for arg, res in testcases:
            self.assertEqual(split(arg), res)


class BigmemTclTest(unittest.TestCase):

    def setUp(self):
        self.interp = Tcl()

    @unittest.skipUnless(_testcapi.INT_MAX < _testcapi.PY_SSIZE_T_MAX,
                         "needs UINT_MAX < SIZE_MAX")
    @test_support.precisionbigmemtest(size=_testcapi.INT_MAX + 1, memuse=5,
                                      dry_run=False)
    def test_huge_string(self, size):
        value = ' ' * size
        self.assertRaises(OverflowError, self.interp.call, 'set', '_', value)


def setUpModule():
    if test_support.verbose:
        tcl = Tcl()
        print 'patchlevel =', tcl.call('info', 'patchlevel')


def test_main():
    test_support.run_unittest(TclTest, TkinterTest, BigmemTclTest)

if __name__ == "__main__":
    test_main()
