from .. import util
from . import util as import_util
from types import MethodType
import unittest


class CallingOrder(unittest.TestCase):

    """Calls to the importers on sys.meta_path happen in order that they are
    specified in the sequence, starting with the first importer
    [first called], and then continuing on down until one is found that doesn't
    return None [continuing]."""


    def test_first_called(self):
        # [first called]
        mod = 'top_level'
        first = util.mock_modules(mod)
        second = util.mock_modules(mod)
        with util.mock_modules(mod) as first, util.mock_modules(mod) as second:
            first.modules[mod] = 42
            second.modules[mod] = -13
            with util.import_state(meta_path=[first, second]):
                self.assertEquals(import_util.import_(mod), 42)

    def test_continuing(self):
        # [continuing]
        mod_name = 'for_real'
        with util.mock_modules('nonexistent') as first, \
             util.mock_modules(mod_name) as second:
            first.find_module = lambda self, fullname, path=None: None
            second.modules[mod_name] = 42
            with util.import_state(meta_path=[first, second]):
                self.assertEquals(import_util.import_(mod_name), 42)


class CallSignature(unittest.TestCase):

    """If there is no __path__ entry on the parent module, then 'path' is None
    [no path]. Otherwise, the value for __path__ is passed in for the 'path'
    argument [path set]."""

    def log(self, fxn):
        log = []
        def wrapper(self, *args, **kwargs):
            log.append([args, kwargs])
            return fxn(*args, **kwargs)
        return log, wrapper


    def test_no_path(self):
        # [no path]
        mod_name = 'top_level'
        assert '.' not in mod_name
        with util.mock_modules(mod_name) as importer:
            log, wrapped_call = self.log(importer.find_module)
            importer.find_module = MethodType(wrapped_call, importer)
            with util.import_state(meta_path=[importer]):
                import_util.import_(mod_name)
                assert len(log) == 1
                args = log[0][0]
                kwargs = log[0][1]
                # Assuming all arguments are positional.
                self.assertEquals(len(args), 2)
                self.assertEquals(len(kwargs), 0)
                self.assertEquals(args[0], mod_name)
                self.assertTrue(args[1] is None)

    def test_with_path(self):
        # [path set]
        pkg_name = 'pkg'
        mod_name = pkg_name + '.module'
        path = [42]
        assert '.' in mod_name
        with util.mock_modules(pkg_name+'.__init__', mod_name) as importer:
            importer.modules[pkg_name].__path__ = path
            log, wrapped_call = self.log(importer.find_module)
            importer.find_module = MethodType(wrapped_call, importer)
            with util.import_state(meta_path=[importer]):
                import_util.import_(mod_name)
                assert len(log) == 2
                args = log[1][0]
                kwargs = log[1][1]
                # Assuming all arguments are positional.
                self.assertTrue(not kwargs)
                self.assertEquals(args[0], mod_name)
                self.assertTrue(args[1] is path)



def test_main():
    from test.support import run_unittest
    run_unittest(CallingOrder, CallSignature)


if __name__ == '__main__':
    test_main()
