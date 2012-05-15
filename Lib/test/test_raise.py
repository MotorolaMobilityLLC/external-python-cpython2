# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Tests for the raise statement."""

from test import support, script_helper
import re
import sys
import types
import unittest


try:
    from resource import setrlimit, RLIMIT_CORE, error as resource_error
except ImportError:
    prepare_subprocess = None
else:
    def prepare_subprocess():
        # don't create core file
        try:
            setrlimit(RLIMIT_CORE, (0, 0))
        except (ValueError, resource_error):
            pass



def get_tb():
    try:
        raise OSError()
    except:
        return sys.exc_info()[2]


class Context:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        return True


class TestRaise(unittest.TestCase):
    def test_invalid_reraise(self):
        try:
            raise
        except RuntimeError as e:
            self.assertIn("No active exception", str(e))
        else:
            self.fail("No exception raised")

    def test_reraise(self):
        try:
            try:
                raise IndexError()
            except IndexError as e:
                exc1 = e
                raise
        except IndexError as exc2:
            self.assertTrue(exc1 is exc2)
        else:
            self.fail("No exception raised")

    def test_except_reraise(self):
        def reraise():
            try:
                raise TypeError("foo")
            except:
                try:
                    raise KeyError("caught")
                except KeyError:
                    pass
                raise
        self.assertRaises(TypeError, reraise)

    def test_finally_reraise(self):
        def reraise():
            try:
                raise TypeError("foo")
            except:
                try:
                    raise KeyError("caught")
                finally:
                    raise
        self.assertRaises(KeyError, reraise)

    def test_nested_reraise(self):
        def nested_reraise():
            raise
        def reraise():
            try:
                raise TypeError("foo")
            except:
                nested_reraise()
        self.assertRaises(TypeError, reraise)

    def test_raise_from_None(self):
        try:
            try:
                raise TypeError("foo")
            except:
                raise ValueError() from None
        except ValueError as e:
            self.assertTrue(isinstance(e.__context__, TypeError))
            self.assertIsNone(e.__cause__)

    def test_with_reraise1(self):
        def reraise():
            try:
                raise TypeError("foo")
            except:
                with Context():
                    pass
                raise
        self.assertRaises(TypeError, reraise)

    def test_with_reraise2(self):
        def reraise():
            try:
                raise TypeError("foo")
            except:
                with Context():
                    raise KeyError("caught")
                raise
        self.assertRaises(TypeError, reraise)

    def test_yield_reraise(self):
        def reraise():
            try:
                raise TypeError("foo")
            except:
                yield 1
                raise
        g = reraise()
        next(g)
        self.assertRaises(TypeError, lambda: next(g))
        self.assertRaises(StopIteration, lambda: next(g))

    def test_erroneous_exception(self):
        class MyException(Exception):
            def __init__(self):
                raise RuntimeError()

        try:
            raise MyException
        except RuntimeError:
            pass
        else:
            self.fail("No exception raised")

    def test_new_returns_invalid_instance(self):
        # See issue #11627.
        class MyException(Exception):
            def __new__(cls, *args):
                return object()

        with self.assertRaises(TypeError):
            raise MyException

    def test_assert_with_tuple_arg(self):
        try:
            assert False, (3,)
        except AssertionError as e:
            self.assertEqual(str(e), "(3,)")



class TestCause(unittest.TestCase):

    def testCauseSyntax(self):
        try:
            try:
                try:
                    raise TypeError
                except Exception:
                    raise ValueError from None
            except ValueError as exc:
                self.assertIsNone(exc.__cause__)
                self.assertTrue(exc.__suppress_context__)
                exc.__suppress_context__ = False
                raise exc
        except ValueError as exc:
            e = exc

        self.assertIsNone(e.__cause__)
        self.assertFalse(e.__suppress_context__)
        self.assertIsInstance(e.__context__, TypeError)

    def test_invalid_cause(self):
        try:
            raise IndexError from 5
        except TypeError as e:
            self.assertIn("exception cause", str(e))
        else:
            self.fail("No exception raised")

    def test_class_cause(self):
        try:
            raise IndexError from KeyError
        except IndexError as e:
            self.assertIsInstance(e.__cause__, KeyError)
        else:
            self.fail("No exception raised")

    def test_instance_cause(self):
        cause = KeyError()
        try:
            raise IndexError from cause
        except IndexError as e:
            self.assertTrue(e.__cause__ is cause)
        else:
            self.fail("No exception raised")

    def test_erroneous_cause(self):
        class MyException(Exception):
            def __init__(self):
                raise RuntimeError()

        try:
            raise IndexError from MyException
        except RuntimeError:
            pass
        else:
            self.fail("No exception raised")


class TestTraceback(unittest.TestCase):

    def get_output(self, code, filename=None):
        """
        Run the specified code in Python (in a new child process) and read the
        output from the standard error or from a file (if filename is set).
        Return the output lines as a list.
        """
        options = {}
        if prepare_subprocess:
            options['preexec_fn'] = prepare_subprocess
        process = script_helper.spawn_python('-c', code, **options)
        stdout, stderr = process.communicate()
        exitcode = process.wait()
        output = support.strip_python_stderr(stdout)
        output = output.decode('ascii', 'backslashreplace')
        if filename:
            self.assertEqual(output, '')
            with open(filename, "rb") as fp:
                output = fp.read()
            output = output.decode('ascii', 'backslashreplace')
        output = re.sub('Current thread 0x[0-9a-f]+',
                        'Current thread XXX',
                        output)
        return output.splitlines(), exitcode

    def test_traceback_verbiage(self):
        code = """
try:
    raise ValueError
except:
    raise NameError from None
"""
        text, exitcode = self.get_output(code)
        self.assertEqual(len(text), 3)
        self.assertTrue(text[0].startswith('Traceback'))
        self.assertTrue(text[1].startswith('  File '))
        self.assertTrue(text[2].startswith('NameError'))

    def test_sets_traceback(self):
        try:
            raise IndexError()
        except IndexError as e:
            self.assertIsInstance(e.__traceback__, types.TracebackType)
        else:
            self.fail("No exception raised")

    def test_accepts_traceback(self):
        tb = get_tb()
        try:
            raise IndexError().with_traceback(tb)
        except IndexError as e:
            self.assertNotEqual(e.__traceback__, tb)
            self.assertEqual(e.__traceback__.tb_next, tb)
        else:
            self.fail("No exception raised")


class TestContext(unittest.TestCase):
    def test_instance_context_instance_raise(self):
        context = IndexError()
        try:
            try:
                raise context
            except:
                raise OSError()
        except OSError as e:
            self.assertEqual(e.__context__, context)
        else:
            self.fail("No exception raised")

    def test_class_context_instance_raise(self):
        context = IndexError
        try:
            try:
                raise context
            except:
                raise OSError()
        except OSError as e:
            self.assertNotEqual(e.__context__, context)
            self.assertIsInstance(e.__context__, context)
        else:
            self.fail("No exception raised")

    def test_class_context_class_raise(self):
        context = IndexError
        try:
            try:
                raise context
            except:
                raise OSError
        except OSError as e:
            self.assertNotEqual(e.__context__, context)
            self.assertIsInstance(e.__context__, context)
        else:
            self.fail("No exception raised")

    def test_c_exception_context(self):
        try:
            try:
                1/0
            except:
                raise OSError
        except OSError as e:
            self.assertIsInstance(e.__context__, ZeroDivisionError)
        else:
            self.fail("No exception raised")

    def test_c_exception_raise(self):
        try:
            try:
                1/0
            except:
                xyzzy
        except NameError as e:
            self.assertIsInstance(e.__context__, ZeroDivisionError)
        else:
            self.fail("No exception raised")

    def test_noraise_finally(self):
        try:
            try:
                pass
            finally:
                raise OSError
        except OSError as e:
            self.assertTrue(e.__context__ is None)
        else:
            self.fail("No exception raised")

    def test_raise_finally(self):
        try:
            try:
                1/0
            finally:
                raise OSError
        except OSError as e:
            self.assertIsInstance(e.__context__, ZeroDivisionError)
        else:
            self.fail("No exception raised")

    def test_context_manager(self):
        class ContextManager:
            def __enter__(self):
                pass
            def __exit__(self, t, v, tb):
                xyzzy
        try:
            with ContextManager():
                1/0
        except NameError as e:
            self.assertIsInstance(e.__context__, ZeroDivisionError)
        else:
            self.fail("No exception raised")

    def test_cycle_broken(self):
        # Self-cycles (when re-raising a caught exception) are broken
        try:
            try:
                1/0
            except ZeroDivisionError as e:
                raise e
        except ZeroDivisionError as e:
            self.assertTrue(e.__context__ is None, e.__context__)

    def test_reraise_cycle_broken(self):
        # Non-trivial context cycles (through re-raising a previous exception)
        # are broken too.
        try:
            try:
                xyzzy
            except NameError as a:
                try:
                    1/0
                except ZeroDivisionError:
                    raise a
        except NameError as e:
            self.assertTrue(e.__context__.__context__ is None)

    def test_3118(self):
        # deleting the generator caused the __context__ to be cleared
        def gen():
            try:
                yield 1
            finally:
                pass

        def f():
            g = gen()
            next(g)
            try:
                try:
                    raise ValueError
                except:
                    del g
                    raise KeyError
            except Exception as e:
                self.assertIsInstance(e.__context__, ValueError)

        f()

    def test_3611(self):
        # A re-raised exception in a __del__ caused the __context__
        # to be cleared
        class C:
            def __del__(self):
                try:
                    1/0
                except:
                    raise

        def f():
            x = C()
            try:
                try:
                    x.x
                except AttributeError:
                    del x
                    raise TypeError
            except Exception as e:
                self.assertNotEqual(e.__context__, None)
                self.assertIsInstance(e.__context__, AttributeError)

        with support.captured_output("stderr"):
            f()

class TestRemovedFunctionality(unittest.TestCase):
    def test_tuples(self):
        try:
            raise (IndexError, KeyError) # This should be a tuple!
        except TypeError:
            pass
        else:
            self.fail("No exception raised")

    def test_strings(self):
        try:
            raise "foo"
        except TypeError:
            pass
        else:
            self.fail("No exception raised")


def test_main():
    support.run_unittest(__name__)

if __name__ == "__main__":
    unittest.main()
