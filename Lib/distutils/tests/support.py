"""Support code for distutils test cases."""
import os
import shutil
import tempfile

from distutils import log
from distutils.dist import Distribution

class LoggingSilencer(object):

    def setUp(self):
        super(LoggingSilencer, self).setUp()
        self.threshold = log.set_threshold(log.FATAL)

    def tearDown(self):
        log.set_threshold(self.threshold)
        super(LoggingSilencer, self).tearDown()


class TempdirManager(object):
    """Mix-in class that handles temporary directories for test cases.

    This is intended to be used with unittest.TestCase.
    """

    def setUp(self):
        super(TempdirManager, self).setUp()
        self.tempdirs = []

    def tearDown(self):
        super(TempdirManager, self).tearDown()
        while self.tempdirs:
            d = self.tempdirs.pop()
            shutil.rmtree(d)

    def mkdtemp(self):
        """Create a temporary directory that will be cleaned up.

        Returns the path of the directory.
        """
        d = tempfile.mkdtemp()
        self.tempdirs.append(d)
        return d

    def write_file(self, path, content='xxx'):
        """Writes a file in the given path.

        path can be a string or a sequence.
        """
        if isinstance(path, (list, tuple)):
            path = os.path.join(*path)
        f = open(path, 'w')
        try:
            f.write(content)
        finally:
            f.close()

    def create_dist(self, pkg_name='foo', **kw):
        """Will generate a test environment.

        This function creates:
         - a Distribution instance using keywords
         - a temporary directory with a package structure

        It returns the package directory and the distribution
        instance.
        """
        tmp_dir = self.mkdtemp()
        pkg_dir = os.path.join(tmp_dir, pkg_name)
        os.mkdir(pkg_dir)
        dist = Distribution(attrs=kw)

        return pkg_dir, dist

class DummyCommand:
    """Class to store options for retrieval via set_undefined_options()."""

    def __init__(self, **kwargs):
        for kw, val in kwargs.items():
            setattr(self, kw, val)

    def ensure_finalized(self):
        pass
