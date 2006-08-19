import sys, os

# Delay import _tkinter until we have set TCL_LIBRARY,
# so that Tcl_FindExecutable has a chance to locate its
# encoding directory.

# Unfortunately, we cannot know the TCL_LIBRARY directory
# if we don't know the tcl version, which we cannot find out
# without import Tcl. Fortunately, Tcl will itself look in
# <TCL_LIBRARY>\..\tcl<TCL_VERSION>, so anything close to
# the real Tcl library will do.

prefix = os.path.join(sys.prefix,"tcl")
# if this does not exist, no further search is needed
if os.path.exists(prefix):
    if "TCL_LIBRARY" not in os.environ:
        for name in os.listdir(prefix):
            if name.startswith("tcl"):
                tcldir = os.path.join(prefix,name)
                if os.path.isdir(tcldir):
                    os.environ["TCL_LIBRARY"] = tcldir
    # Compute TK_LIBRARY, knowing that it has the same version
    # as Tcl
    import _tkinter
    ver = str(_tkinter.TCL_VERSION)
    if "TK_LIBRARY" not in os.environ:
        v = os.path.join(prefix, 'tk'+ver)
        if os.path.exists(os.path.join(v, "tclIndex")):
            os.environ['TK_LIBRARY'] = v
    # We don't know the Tix version, so we must search the entire
    # directory
    if "TIX_LIBRARY" not in os.environ:
        for name in os.listdir(prefix):
            if name.startswith("tix"):
                tixdir = os.path.join(prefix,name)
                if os.path.isdir(tixdir):
                    os.environ["TIX_LIBRARY"] = tixdir
