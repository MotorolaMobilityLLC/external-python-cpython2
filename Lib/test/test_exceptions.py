# Python test set -- part 5, built-in exceptions

import os
import sys
import unittest
import pickle
import weakref

from test.support import TESTFN, unlink, run_unittest, captured_output

# XXX This is not really enough, each *operation* should be tested!

class ExceptionTests(unittest.TestCase):

    def raise_catch(self, exc, excname):
        try:
            raise exc("spam")
        except exc as err:
            buf1 = str(err)
        try:
            raise exc("spam")
        except exc as err:
            buf2 = str(err)
        self.assertEquals(buf1, buf2)
        self.assertEquals(exc.__name__, excname)

    def testRaising(self):
        self.raise_catch(AttributeError, "AttributeError")
        self.assertRaises(AttributeError, getattr, sys, "undefined_attribute")

        self.raise_catch(EOFError, "EOFError")
        fp = open(TESTFN, 'w')
        fp.close()
        fp = open(TESTFN, 'r')
        savestdin = sys.stdin
        try:
            try:
                import marshal
                marshal.loads('')
            except EOFError:
                pass
        finally:
            sys.stdin = savestdin
            fp.close()
            unlink(TESTFN)

        self.raise_catch(IOError, "IOError")
        self.assertRaises(IOError, open, 'this file does not exist', 'r')

        self.raise_catch(ImportError, "ImportError")
        self.assertRaises(ImportError, __import__, "undefined_module")

        self.raise_catch(IndexError, "IndexError")
        x = []
        self.assertRaises(IndexError, x.__getitem__, 10)

        self.raise_catch(KeyError, "KeyError")
        x = {}
        self.assertRaises(KeyError, x.__getitem__, 'key')

        self.raise_catch(KeyboardInterrupt, "KeyboardInterrupt")

        self.raise_catch(MemoryError, "MemoryError")

        self.raise_catch(NameError, "NameError")
        try: x = undefined_variable
        except NameError: pass

        self.raise_catch(OverflowError, "OverflowError")
        x = 1
        for dummy in range(128):
            x += x  # this simply shouldn't blow up

        self.raise_catch(RuntimeError, "RuntimeError")

        self.raise_catch(SyntaxError, "SyntaxError")
        try: exec('/\n')
        except SyntaxError: pass

        self.raise_catch(IndentationError, "IndentationError")

        self.raise_catch(TabError, "TabError")
        try: compile("try:\n\t1/0\n    \t1/0\nfinally:\n pass\n",
                     '<string>', 'exec')
        except TabError: pass
        else: self.fail("TabError not raised")

        self.raise_catch(SystemError, "SystemError")

        self.raise_catch(SystemExit, "SystemExit")
        self.assertRaises(SystemExit, sys.exit, 0)

        self.raise_catch(TypeError, "TypeError")
        try: [] + ()
        except TypeError: pass

        self.raise_catch(ValueError, "ValueError")
        self.assertRaises(ValueError, chr, 17<<16)

        self.raise_catch(ZeroDivisionError, "ZeroDivisionError")
        try: x = 1/0
        except ZeroDivisionError: pass

        self.raise_catch(Exception, "Exception")
        try: x = 1/0
        except Exception as e: pass

    def testSyntaxErrorMessage(self):
        # make sure the right exception message is raised for each of
        # these code fragments

        def ckmsg(src, msg):
            try:
                compile(src, '<fragment>', 'exec')
            except SyntaxError as e:
                if e.msg != msg:
                    self.fail("expected %s, got %s" % (msg, e.msg))
            else:
                self.fail("failed to get expected SyntaxError")

        s = '''while 1:
            try:
                pass
            finally:
                continue'''

        if not sys.platform.startswith('java'):
            ckmsg(s, "'continue' not supported inside 'finally' clause")

        s = '''if 1:
        try:
            continue
        except:
            pass'''

        ckmsg(s, "'continue' not properly in loop")
        ckmsg("continue\n", "'continue' not properly in loop")

    def testSettingException(self):
        # test that setting an exception at the C level works even if the
        # exception object can't be constructed.

        class BadException(Exception):
            def __init__(self_):
                raise RuntimeError("can't instantiate BadException")

        class InvalidException:
            pass

        def test_capi1():
            import _testcapi
            try:
                _testcapi.raise_exception(BadException, 1)
            except TypeError as err:
                exc, err, tb = sys.exc_info()
                co = tb.tb_frame.f_code
                self.assertEquals(co.co_name, "test_capi1")
                self.assertTrue(co.co_filename.endswith('test_exceptions.py'))
            else:
                self.fail("Expected exception")

        def test_capi2():
            import _testcapi
            try:
                _testcapi.raise_exception(BadException, 0)
            except RuntimeError as err:
                exc, err, tb = sys.exc_info()
                co = tb.tb_frame.f_code
                self.assertEquals(co.co_name, "__init__")
                self.assertTrue(co.co_filename.endswith('test_exceptions.py'))
                co2 = tb.tb_frame.f_back.f_code
                self.assertEquals(co2.co_name, "test_capi2")
            else:
                self.fail("Expected exception")

        def test_capi3():
            import _testcapi
            self.assertRaises(SystemError, _testcapi.raise_exception,
                              InvalidException, 1)

        if not sys.platform.startswith('java'):
            test_capi1()
            test_capi2()
            test_capi3()

    def test_WindowsError(self):
        try:
            WindowsError
        except NameError:
            pass
        else:
            self.assertEqual(str(WindowsError(1001)),
                                 "1001")
            self.assertEqual(str(WindowsError(1001, "message")),
                                 "[Error 1001] message")
            self.assertEqual(WindowsError(1001, "message").errno, 22)
            self.assertEqual(WindowsError(1001, "message").winerror, 1001)

    def testAttributes(self):
        # test that exception attributes are happy

        exceptionList = [
            (BaseException, (), {'args' : ()}),
            (BaseException, (1, ), {'args' : (1,)}),
            (BaseException, ('foo',),
                {'args' : ('foo',)}),
            (BaseException, ('foo', 1),
                {'args' : ('foo', 1)}),
            (SystemExit, ('foo',),
                {'args' : ('foo',), 'code' : 'foo'}),
            (IOError, ('foo',),
                {'args' : ('foo',), 'filename' : None,
                 'errno' : None, 'strerror' : None}),
            (IOError, ('foo', 'bar'),
                {'args' : ('foo', 'bar'), 'filename' : None,
                 'errno' : 'foo', 'strerror' : 'bar'}),
            (IOError, ('foo', 'bar', 'baz'),
                {'args' : ('foo', 'bar'), 'filename' : 'baz',
                 'errno' : 'foo', 'strerror' : 'bar'}),
            (IOError, ('foo', 'bar', 'baz', 'quux'),
                {'args' : ('foo', 'bar', 'baz', 'quux')}),
            (EnvironmentError, ('errnoStr', 'strErrorStr', 'filenameStr'),
                {'args' : ('errnoStr', 'strErrorStr'),
                 'strerror' : 'strErrorStr', 'errno' : 'errnoStr',
                 'filename' : 'filenameStr'}),
            (EnvironmentError, (1, 'strErrorStr', 'filenameStr'),
                {'args' : (1, 'strErrorStr'), 'errno' : 1,
                 'strerror' : 'strErrorStr', 'filename' : 'filenameStr'}),
            (SyntaxError, (), {'msg' : None, 'text' : None,
                'filename' : None, 'lineno' : None, 'offset' : None,
                'print_file_and_line' : None}),
            (SyntaxError, ('msgStr',),
                {'args' : ('msgStr',), 'text' : None,
                 'print_file_and_line' : None, 'msg' : 'msgStr',
                 'filename' : None, 'lineno' : None, 'offset' : None}),
            (SyntaxError, ('msgStr', ('filenameStr', 'linenoStr', 'offsetStr',
                           'textStr')),
                {'offset' : 'offsetStr', 'text' : 'textStr',
                 'args' : ('msgStr', ('filenameStr', 'linenoStr',
                                      'offsetStr', 'textStr')),
                 'print_file_and_line' : None, 'msg' : 'msgStr',
                 'filename' : 'filenameStr', 'lineno' : 'linenoStr'}),
            (SyntaxError, ('msgStr', 'filenameStr', 'linenoStr', 'offsetStr',
                           'textStr', 'print_file_and_lineStr'),
                {'text' : None,
                 'args' : ('msgStr', 'filenameStr', 'linenoStr', 'offsetStr',
                           'textStr', 'print_file_and_lineStr'),
                 'print_file_and_line' : None, 'msg' : 'msgStr',
                 'filename' : None, 'lineno' : None, 'offset' : None}),
            (UnicodeError, (), {'args' : (),}),
            (UnicodeEncodeError, ('ascii', 'a', 0, 1,
                                  'ordinal not in range'),
                {'args' : ('ascii', 'a', 0, 1,
                                           'ordinal not in range'),
                 'encoding' : 'ascii', 'object' : 'a',
                 'start' : 0, 'reason' : 'ordinal not in range'}),
            (UnicodeDecodeError, ('ascii', bytearray(b'\xff'), 0, 1,
                                  'ordinal not in range'),
                {'args' : ('ascii', bytearray(b'\xff'), 0, 1,
                                           'ordinal not in range'),
                 'encoding' : 'ascii', 'object' : b'\xff',
                 'start' : 0, 'reason' : 'ordinal not in range'}),
            (UnicodeDecodeError, ('ascii', b'\xff', 0, 1,
                                  'ordinal not in range'),
                {'args' : ('ascii', b'\xff', 0, 1,
                                           'ordinal not in range'),
                 'encoding' : 'ascii', 'object' : b'\xff',
                 'start' : 0, 'reason' : 'ordinal not in range'}),
            (UnicodeTranslateError, ("\u3042", 0, 1, "ouch"),
                {'args' : ('\u3042', 0, 1, 'ouch'),
                 'object' : '\u3042', 'reason' : 'ouch',
                 'start' : 0, 'end' : 1}),
        ]
        try:
            exceptionList.append(
                (WindowsError, (1, 'strErrorStr', 'filenameStr'),
                    {'args' : (1, 'strErrorStr'),
                     'strerror' : 'strErrorStr', 'winerror' : 1,
                     'errno' : 22, 'filename' : 'filenameStr'})
            )
        except NameError:
            pass

        for exc, args, expected in exceptionList:
            try:
                e = exc(*args)
            except:
                print("\nexc=%r, args=%r" % (exc, args), file=sys.stderr)
                raise
            else:
                # Verify module name
                self.assertEquals(type(e).__module__, 'builtins')
                # Verify no ref leaks in Exc_str()
                s = str(e)
                for checkArgName in expected:
                    value = getattr(e, checkArgName)
                    self.assertEquals(repr(value),
                                      repr(expected[checkArgName]),
                                      '%r.%s == %r, expected %r' % (
                                      e, checkArgName,
                                      value, expected[checkArgName]))

                # test for pickling support
                for p in [pickle]:
                    for protocol in range(p.HIGHEST_PROTOCOL + 1):
                        s = p.dumps(e, protocol)
                        new = p.loads(s)
                        for checkArgName in expected:
                            got = repr(getattr(new, checkArgName))
                            want = repr(expected[checkArgName])
                            self.assertEquals(got, want,
                                              'pickled "%r", attribute "%s' %
                                              (e, checkArgName))

    def testWithTraceback(self):
        try:
            raise IndexError(4)
        except:
            tb = sys.exc_info()[2]

        e = BaseException().with_traceback(tb)
        self.assertIsInstance(e, BaseException)
        self.assertEqual(e.__traceback__, tb)

        e = IndexError(5).with_traceback(tb)
        self.assertIsInstance(e, IndexError)
        self.assertEqual(e.__traceback__, tb)

        class MyException(Exception):
            pass

        e = MyException().with_traceback(tb)
        self.assertIsInstance(e, MyException)
        self.assertEqual(e.__traceback__, tb)

    def testInvalidTraceback(self):
        try:
            Exception().__traceback__ = 5
        except TypeError as e:
            self.assertIn("__traceback__ must be a traceback", str(e))
        else:
            self.fail("No exception raised")

    def testInvalidAttrs(self):
        self.assertRaises(TypeError, setattr, Exception(), '__cause__', 1)
        self.assertRaises(TypeError, delattr, Exception(), '__cause__')
        self.assertRaises(TypeError, setattr, Exception(), '__context__', 1)
        self.assertRaises(TypeError, delattr, Exception(), '__context__')

    def testNoneClearsTracebackAttr(self):
        try:
            raise IndexError(4)
        except:
            tb = sys.exc_info()[2]

        e = Exception()
        e.__traceback__ = tb
        e.__traceback__ = None
        self.assertEqual(e.__traceback__, None)

    def testChainingAttrs(self):
        e = Exception()
        self.assertEqual(e.__context__, None)
        self.assertEqual(e.__cause__, None)

        e = TypeError()
        self.assertEqual(e.__context__, None)
        self.assertEqual(e.__cause__, None)

        class MyException(EnvironmentError):
            pass

        e = MyException()
        self.assertEqual(e.__context__, None)
        self.assertEqual(e.__cause__, None)

    def testKeywordArgs(self):
        # test that builtin exception don't take keyword args,
        # but user-defined subclasses can if they want
        self.assertRaises(TypeError, BaseException, a=1)

        class DerivedException(BaseException):
            def __init__(self, fancy_arg):
                BaseException.__init__(self)
                self.fancy_arg = fancy_arg

        x = DerivedException(fancy_arg=42)
        self.assertEquals(x.fancy_arg, 42)

    def testInfiniteRecursion(self):
        def f():
            return f()
        self.assertRaises(RuntimeError, f)

        def g():
            try:
                return g()
            except ValueError:
                return -1
        self.assertRaises(RuntimeError, g)

    def test_str(self):
        # Make sure both instances and classes have a str representation.
        self.assertTrue(str(Exception))
        self.assertTrue(str(Exception('a')))
        self.assertTrue(str(Exception('a', 'b')))

    def testExceptionCleanupNames(self):
        # Make sure the local variable bound to the exception instance by
        # an "except" statement is only visible inside the except block.
        try:
            raise Exception()
        except Exception as e:
            self.assertTrue(e)
            del e
        self.assertNotIn('e', locals())

    def testExceptionCleanupState(self):
        # Make sure exception state is cleaned up as soon as the except
        # block is left. See #2507

        class MyException(Exception):
            def __init__(self, obj):
                self.obj = obj
        class MyObj:
            pass

        def inner_raising_func():
            # Create some references in exception value and traceback
            local_ref = obj
            raise MyException(obj)

        # Qualified "except" with "as"
        obj = MyObj()
        wr = weakref.ref(obj)
        try:
            inner_raising_func()
        except MyException as e:
            pass
        obj = None
        obj = wr()
        self.assertTrue(obj is None, "%s" % obj)

        # Qualified "except" without "as"
        obj = MyObj()
        wr = weakref.ref(obj)
        try:
            inner_raising_func()
        except MyException:
            pass
        obj = None
        obj = wr()
        self.assertTrue(obj is None, "%s" % obj)

        # Bare "except"
        obj = MyObj()
        wr = weakref.ref(obj)
        try:
            inner_raising_func()
        except:
            pass
        obj = None
        obj = wr()
        self.assertTrue(obj is None, "%s" % obj)

        # "except" with premature block leave
        obj = MyObj()
        wr = weakref.ref(obj)
        for i in [0]:
            try:
                inner_raising_func()
            except:
                break
        obj = None
        obj = wr()
        self.assertTrue(obj is None, "%s" % obj)

        # "except" block raising another exception
        obj = MyObj()
        wr = weakref.ref(obj)
        try:
            try:
                inner_raising_func()
            except:
                raise KeyError
        except KeyError as e:
            # We want to test that the except block above got rid of
            # the exception raised in inner_raising_func(), but it
            # also ends up in the __context__ of the KeyError, so we
            # must clear the latter manually for our test to succeed.
            e.__context__ = None
            obj = None
            obj = wr()
            self.assertTrue(obj is None, "%s" % obj)

        # Some complicated construct
        obj = MyObj()
        wr = weakref.ref(obj)
        try:
            inner_raising_func()
        except MyException:
            try:
                try:
                    raise
                finally:
                    raise
            except MyException:
                pass
        obj = None
        obj = wr()
        self.assertTrue(obj is None, "%s" % obj)

        # Inside an exception-silencing "with" block
        class Context:
            def __enter__(self):
                return self
            def __exit__ (self, exc_type, exc_value, exc_tb):
                return True
        obj = MyObj()
        wr = weakref.ref(obj)
        with Context():
            inner_raising_func()
        obj = None
        obj = wr()
        self.assertTrue(obj is None, "%s" % obj)

    def test_generator_leaking(self):
        # Test that generator exception state doesn't leak into the calling
        # frame
        def yield_raise():
            try:
                raise KeyError("caught")
            except KeyError:
                yield sys.exc_info()[0]
                yield sys.exc_info()[0]
            yield sys.exc_info()[0]
        g = yield_raise()
        self.assertEquals(next(g), KeyError)
        self.assertEquals(sys.exc_info()[0], None)
        self.assertEquals(next(g), KeyError)
        self.assertEquals(sys.exc_info()[0], None)
        self.assertEquals(next(g), None)

        # Same test, but inside an exception handler
        try:
            raise TypeError("foo")
        except TypeError:
            g = yield_raise()
            self.assertEquals(next(g), KeyError)
            self.assertEquals(sys.exc_info()[0], TypeError)
            self.assertEquals(next(g), KeyError)
            self.assertEquals(sys.exc_info()[0], TypeError)
            self.assertEquals(next(g), TypeError)
            del g
            self.assertEquals(sys.exc_info()[0], TypeError)

    def test_3114(self):
        # Bug #3114: in its destructor, MyObject retrieves a pointer to
        # obsolete and/or deallocated objects.
        class MyObject:
            def __del__(self):
                nonlocal e
                e = sys.exc_info()
        e = ()
        try:
            raise Exception(MyObject())
        except:
            pass
        self.assertEquals(e, (None, None, None))

    def testUnicodeChangeAttributes(self):
        # See issue 7309. This was a crasher.

        u = UnicodeEncodeError('baz', 'xxxxx', 1, 5, 'foo')
        self.assertEqual(str(u), "'baz' codec can't encode characters in position 1-4: foo")
        u.end = 2
        self.assertEqual(str(u), "'baz' codec can't encode character '\\x78' in position 1: foo")
        u.end = 5
        u.reason = 0x345345345345345345
        self.assertEqual(str(u), "'baz' codec can't encode characters in position 1-4: 965230951443685724997")
        u.encoding = 4000
        self.assertEqual(str(u), "'4000' codec can't encode characters in position 1-4: 965230951443685724997")
        u.start = 1000
        self.assertEqual(str(u), "'4000' codec can't encode characters in position 1000-4: 965230951443685724997")

        u = UnicodeDecodeError('baz', b'xxxxx', 1, 5, 'foo')
        self.assertEqual(str(u), "'baz' codec can't decode bytes in position 1-4: foo")
        u.end = 2
        self.assertEqual(str(u), "'baz' codec can't decode byte 0x78 in position 1: foo")
        u.end = 5
        u.reason = 0x345345345345345345
        self.assertEqual(str(u), "'baz' codec can't decode bytes in position 1-4: 965230951443685724997")
        u.encoding = 4000
        self.assertEqual(str(u), "'4000' codec can't decode bytes in position 1-4: 965230951443685724997")
        u.start = 1000
        self.assertEqual(str(u), "'4000' codec can't decode bytes in position 1000-4: 965230951443685724997")

        u = UnicodeTranslateError('xxxx', 1, 5, 'foo')
        self.assertEqual(str(u), "can't translate characters in position 1-4: foo")
        u.end = 2
        self.assertEqual(str(u), "can't translate character '\\x78' in position 1: foo")
        u.end = 5
        u.reason = 0x345345345345345345
        self.assertEqual(str(u), "can't translate characters in position 1-4: 965230951443685724997")
        u.start = 1000
        self.assertEqual(str(u), "can't translate characters in position 1000-4: 965230951443685724997")

    def test_badisinstance(self):
        # Bug #2542: if issubclass(e, MyException) raises an exception,
        # it should be ignored
        class Meta(type):
            def __subclasscheck__(cls, subclass):
                raise ValueError()
        class MyException(Exception, metaclass=Meta):
            pass

        with captured_output("stderr") as stderr:
            try:
                raise KeyError()
            except MyException as e:
                self.fail("exception should not be a MyException")
            except KeyError:
                pass
            except:
                self.fail("Should have raised KeyError")
            else:
                self.fail("Should have raised KeyError")

        def g():
            try:
                return g()
            except RuntimeError:
                return sys.exc_info()
        e, v, tb = g()
        self.assertTrue(isinstance(v, RuntimeError), type(v))
        self.assertIn("maximum recursion depth exceeded", str(v))


    def test_MemoryError(self):
        # PyErr_NoMemory always raises the same exception instance.
        # Check that the traceback is not doubled.
        import traceback
        from _testcapi import raise_memoryerror
        def raiseMemError():
            try:
                raise_memoryerror()
            except MemoryError as e:
                tb = e.__traceback__
            else:
                self.fail("Should have raises a MemoryError")
            return traceback.format_tb(tb)

        tb1 = raiseMemError()
        tb2 = raiseMemError()
        self.assertEqual(tb1, tb2)

    def test_exception_with_doc(self):
        import _testcapi
        doc2 = "This is a test docstring."
        doc4 = "This is another test docstring."

        self.assertRaises(SystemError, _testcapi.make_exception_with_doc,
                          "error1")

        # test basic usage of PyErr_NewException
        error1 = _testcapi.make_exception_with_doc("_testcapi.error1")
        self.assertIs(type(error1), type)
        self.assertTrue(issubclass(error1, Exception))
        self.assertIsNone(error1.__doc__)

        # test with given docstring
        error2 = _testcapi.make_exception_with_doc("_testcapi.error2", doc2)
        self.assertEqual(error2.__doc__, doc2)

        # test with explicit base (without docstring)
        error3 = _testcapi.make_exception_with_doc("_testcapi.error3",
                                                   base=error2)
        self.assertTrue(issubclass(error3, error2))

        # test with explicit base tuple
        class C(object):
            pass
        error4 = _testcapi.make_exception_with_doc("_testcapi.error4", doc4,
                                                   (error3, C))
        self.assertTrue(issubclass(error4, error3))
        self.assertTrue(issubclass(error4, C))
        self.assertEqual(error4.__doc__, doc4)

        # test with explicit dictionary
        error5 = _testcapi.make_exception_with_doc("_testcapi.error5", "",
                                                   error4, {'a': 1})
        self.assertTrue(issubclass(error5, error4))
        self.assertEqual(error5.a, 1)
        self.assertEqual(error5.__doc__, "")


def test_main():
    run_unittest(ExceptionTests)

if __name__ == '__main__':
    unittest.main()
