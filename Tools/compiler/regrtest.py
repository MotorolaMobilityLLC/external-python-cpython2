"""Run the Python regression test using the compiler

This test runs the standard Python test suite using bytecode generated
by this compiler instead of by the builtin compiler.

The regression test is run with the interpreter in verbose mode so
that import problems can be observed easily.
"""

from compiler import compile

import os
import sys
import test
import tempfile

def copy_test_suite():
    dest = tempfile.mktemp()
    os.mkdir(dest)
    os.system("cp -r %s/* %s" % (test.__path__[0], dest))
    print "Creating copy of test suite in", dest
    return dest

def copy_library():
    dest = tempfile.mktemp()
    os.mkdir(dest)
    libdir = os.path.split(test.__path__[0])[0]
    os.system("cp -r %s/* %s" % (libdir, dest))
    print "Creating copy of standard library in", dest
    return dest

def compile_files(dir):
    print "Compiling", dir
    line_len = 10
    for file in os.listdir(dir):
        base, ext = os.path.splitext(file)
        if ext == '.py':
            source = os.path.join(dir, file)
            line_len = line_len + len(file) + 1
            if line_len > 75:
                print "\n\t",
                line_len = len(source) + 9
            print file,
            try:
                compile(source)
            except SyntaxError, err:
                print err
                continue
            # make sure the .pyc file is not over-written
            os.chmod(source + "c", 444)
        else:
            path = os.path.join(dir, file)
            if os.path.isdir(path):
                print
                compile_files(path)
    print

def run_regrtest(lib_dir):
    test_dir = os.path.join(lib_dir, "test")
    os.chdir(test_dir)
    os.system("PYTHONPATH=%s %s -v regrtest.py -r" % (lib_dir, sys.executable))

def cleanup(dir):
    os.system("rm -rf %s" % dir)

def main():
    lib_dir = copy_library()
    compile_files(lib_dir)
    run_regrtest(lib_dir)
    raw_input("Cleanup?")
    cleanup(lib_dir)

if __name__ == "__main__":
    main()
