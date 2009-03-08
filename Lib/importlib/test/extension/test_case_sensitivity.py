import sys
from test import support
import unittest
import importlib
from .. import util
from . import util as ext_util


@util.case_insensitive_tests
class ExtensionModuleCaseSensitivityTest(unittest.TestCase):

    def find_module(self):
        good_name = ext_util.NAME
        bad_name = good_name.upper()
        assert good_name != bad_name
        finder = importlib.ExtensionFileFinder(ext_util.PATH)
        return finder.find_module(bad_name)

    def test_case_sensitive(self):
        with support.EnvironmentVarGuard() as env:
            env.unset('PYTHONCASEOK')
            loader = self.find_module()
            self.assert_(loader is None)

    def test_case_insensitivity(self):
        with support.EnvironmentVarGuard() as env:
            env.set('PYTHONCASEOK', '1')
            loader = self.find_module()
            self.assert_(hasattr(loader, 'load_module'))




def test_main():
    if ext_util.FILENAME is None:
        return
    support.run_unittest(ExtensionModuleCaseSensitivityTest)


if __name__ == '__main__':
    test_main()
