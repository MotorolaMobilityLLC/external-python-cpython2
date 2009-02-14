"""Tests for distutils.command.sdist."""
import os
import unittest
import shutil
import zipfile
from os.path import join
import sys
import tempfile

from distutils.command.sdist import sdist
from distutils.core import Distribution
from distutils.tests.test_config import PyPIRCCommandTestCase
from distutils.errors import DistutilsExecError
from distutils.spawn import find_executable

SETUP_PY = """
from distutils.core import setup
import somecode

setup(name='fake')
"""

MANIFEST_IN = """
recursive-include somecode *
"""

class sdistTestCase(PyPIRCCommandTestCase):

    def setUp(self):
        # PyPIRCCommandTestCase creates a temp dir already
        # and put it in self.tmp_dir
        PyPIRCCommandTestCase.setUp(self)
        # setting up an environment
        self.old_path = os.getcwd()
        os.mkdir(join(self.tmp_dir, 'somecode'))
        os.mkdir(join(self.tmp_dir, 'dist'))
        # creating a MANIFEST, a package, and a README
        self._write(join(self.tmp_dir, 'MANIFEST.in'), MANIFEST_IN)
        self._write(join(self.tmp_dir, 'README'), 'xxx')
        self._write(join(self.tmp_dir, 'somecode', '__init__.py'), '#')
        self._write(join(self.tmp_dir, 'setup.py'), SETUP_PY)
        os.chdir(self.tmp_dir)

    def tearDown(self):
        # back to normal
        os.chdir(self.old_path)
        PyPIRCCommandTestCase.tearDown(self)

    def _write(self, path, content):
        f = open(path, 'w')
        try:
            f.write(content)
        finally:
            f.close()

    def test_prune_file_list(self):
        # this test creates a package with some vcs dirs in it
        # and launch sdist to make sure they get pruned
        # on all systems

        # creating VCS directories with some files in them
        os.mkdir(join(self.tmp_dir, 'somecode', '.svn'))
        self._write(join(self.tmp_dir, 'somecode', '.svn', 'ok.py'), 'xxx')

        os.mkdir(join(self.tmp_dir, 'somecode', '.hg'))
        self._write(join(self.tmp_dir, 'somecode', '.hg',
                         'ok'), 'xxx')

        os.mkdir(join(self.tmp_dir, 'somecode', '.git'))
        self._write(join(self.tmp_dir, 'somecode', '.git',
                         'ok'), 'xxx')

        # now building a sdist
        dist = Distribution()
        dist.script_name = 'setup.py'
        dist.metadata.name = 'fake'
        dist.metadata.version = '1.0'
        dist.metadata.url = 'http://xxx'
        dist.metadata.author = dist.metadata.author_email = 'xxx'
        dist.packages = ['somecode']
        dist.include_package_data = True
        cmd = sdist(dist)
        cmd.manifest = 'MANIFEST'
        cmd.template = 'MANIFEST.in'
        cmd.dist_dir = 'dist'

        # zip is available universally
        # (tar might not be installed under win32)
        cmd.formats = ['zip']
        cmd.run()

        # now let's check what we have
        dist_folder = join(self.tmp_dir, 'dist')
        files = os.listdir(dist_folder)
        self.assertEquals(files, ['fake-1.0.zip'])

        zip_file = zipfile.ZipFile(join(dist_folder, 'fake-1.0.zip'))
        try:
            content = zip_file.namelist()
        finally:
            zip_file.close()

        # making sure everything has been pruned correctly
        self.assertEquals(len(content), 4)

    def test_make_distribution(self):

        # check if tar and gzip are installed
        if (find_executable('tar') is None or
            find_executable('gzip') is None):
            return

        # now building a sdist
        dist = Distribution()
        dist.script_name = 'setup.py'
        dist.metadata.name = 'fake'
        dist.metadata.version = '1.0'
        dist.metadata.url = 'http://xxx'
        dist.metadata.author = dist.metadata.author_email = 'xxx'
        dist.packages = ['somecode']
        dist.include_package_data = True
        cmd = sdist(dist)
        cmd.manifest = 'MANIFEST'
        cmd.template = 'MANIFEST.in'
        cmd.dist_dir = 'dist'

        # creating a gztar then a tar
        cmd.formats = ['gztar', 'tar']
        cmd.run()

        # making sure we have two files
        dist_folder = join(self.tmp_dir, 'dist')
        result = os.listdir(dist_folder)
        result.sort()
        self.assertEquals(result,
                          ['fake-1.0.tar', 'fake-1.0.tar.gz'] )

        os.remove(join(dist_folder, 'fake-1.0.tar'))
        os.remove(join(dist_folder, 'fake-1.0.tar.gz'))

        # now trying a tar then a gztar
        cmd.formats = ['tar', 'gztar']
        cmd.run()

        result = os.listdir(dist_folder)
        result.sort()
        self.assertEquals(result,
                ['fake-1.0.tar', 'fake-1.0.tar.gz'])

def test_suite():
    return unittest.makeSuite(sdistTestCase)

if __name__ == "__main__":
    unittest.main(defaultTest="test_suite")
