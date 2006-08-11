"""CallTips.py - An IDLE Extension to Jog Your Memory

Call Tips are floating windows which display function, class, and method
parameter and docstring information when you type an opening parenthesis, and
which disappear when you type a closing parenthesis.
"""
import sys
import types

import CallTipWindow
from HyperParser import HyperParser

import __main__

class CallTips:

    menudefs = [
        ('edit', [
            ("Show call tip", "<<force-open-calltip>>"),
        ])
    ]

    def __init__(self, editwin=None):
        if editwin is None:  # subprocess and test
            self.editwin = None
            return
        self.editwin = editwin
        self.text = editwin.text
        self.calltip = None
        self._make_calltip_window = self._make_tk_calltip_window

    def close(self):
        self._make_calltip_window = None

    def _make_tk_calltip_window(self):
        # See __init__ for usage
        return CallTipWindow.CallTip(self.text)

    def _remove_calltip_window(self, event=None):
        if self.calltip:
            self.calltip.hidetip()
            self.calltip = None

    def force_open_calltip_event(self, event):
        """Happens when the user really wants to open a CallTip, even if a
        function call is needed.
        """
        self.open_calltip(True)

    def try_open_calltip_event(self, event):
        """Happens when it would be nice to open a CallTip, but not really
        neccesary, for example after an opening bracket, so function calls
        won't be made.
        """
        self.open_calltip(False)

    def refresh_calltip_event(self, event):
        """If there is already a calltip window, check if it is still needed,
        and if so, reload it.
        """
        if self.calltip and self.calltip.is_active():
            self.open_calltip(False)

    def open_calltip(self, evalfuncs):
        self._remove_calltip_window()

        hp = HyperParser(self.editwin, "insert")
        sur_paren = hp.get_surrounding_brackets('(')
        if not sur_paren:
            return
        hp.set_index(sur_paren[0])
        name = hp.get_expression()
        if not name or (not evalfuncs and name.find('(') != -1):
            return
        arg_text = self.fetch_tip(name)
        if not arg_text:
            return
        self.calltip = self._make_calltip_window()
        self.calltip.showtip(arg_text, sur_paren[0], sur_paren[1])

    def fetch_tip(self, name):
        """Return the argument list and docstring of a function or class

        If there is a Python subprocess, get the calltip there.  Otherwise,
        either fetch_tip() is running in the subprocess itself or it was called
        in an IDLE EditorWindow before any script had been run.

        The subprocess environment is that of the most recently run script.  If
        two unrelated modules are being edited some calltips in the current
        module may be inoperative if the module was not the last to run.

        """
        try:
            rpcclt = self.editwin.flist.pyshell.interp.rpcclt
        except:
            rpcclt = None
        if rpcclt:
            return rpcclt.remotecall("exec", "get_the_calltip",
                                     (name,), {})
        else:
            entity = self.get_entity(name)
            return get_arg_text(entity)

    def get_entity(self, name):
        "Lookup name in a namespace spanning sys.modules and __main.dict__"
        if name:
            namespace = sys.modules.copy()
            namespace.update(__main__.__dict__)
            try:
                return eval(name, namespace)
            except:
                return None

def _find_constructor(class_ob):
    # Given a class object, return a function object used for the
    # constructor (ie, __init__() ) or None if we can't find one.
    try:
        return class_ob.__init__.im_func
    except AttributeError:
        for base in class_ob.__bases__:
            rc = _find_constructor(base)
            if rc is not None: return rc
    return None

def get_arg_text(ob):
    """Get a string describing the arguments for the given object"""
    argText = ""
    if ob is not None:
        argOffset = 0
        if type(ob) in (types.ClassType, types.TypeType):
            # Look for the highest __init__ in the class chain.
            fob = _find_constructor(ob)
            if fob is None:
                fob = lambda: None
            else:
                argOffset = 1
        elif type(ob)==types.MethodType:
            # bit of a hack for methods - turn it into a function
            # but we drop the "self" param.
            fob = ob.im_func
            argOffset = 1
        else:
            fob = ob
        # Try and build one for Python defined functions
        if type(fob) in [types.FunctionType, types.LambdaType]:
            try:
                realArgs = fob.func_code.co_varnames[argOffset:fob.func_code.co_argcount]
                defaults = fob.func_defaults or []
                defaults = list(map(lambda name: "=%s" % repr(name), defaults))
                defaults = [""] * (len(realArgs)-len(defaults)) + defaults
                items = map(lambda arg, dflt: arg+dflt, realArgs, defaults)
                if fob.func_code.co_flags & 0x4:
                    items.append("...")
                if fob.func_code.co_flags & 0x8:
                    items.append("***")
                argText = ", ".join(items)
                argText = "(%s)" % argText
            except:
                pass
        # See if we can use the docstring
        doc = getattr(ob, "__doc__", "")
        if doc:
            doc = doc.lstrip()
            pos = doc.find("\n")
            if pos < 0 or pos > 70:
                pos = 70
            if argText:
                argText += "\n"
            argText += doc[:pos]
    return argText

#################################################
#
# Test code
#
if __name__=='__main__':

    def t1(): "()"
    def t2(a, b=None): "(a, b=None)"
    def t3(a, *args): "(a, ...)"
    def t4(*args): "(...)"
    def t5(a, *args): "(a, ...)"
    def t6(a, b=None, *args, **kw): "(a, b=None, ..., ***)"

    class TC:
        "(a=None, ...)"
        def __init__(self, a=None, *b): "(a=None, ...)"
        def t1(self): "()"
        def t2(self, a, b=None): "(a, b=None)"
        def t3(self, a, *args): "(a, ...)"
        def t4(self, *args): "(...)"
        def t5(self, a, *args): "(a, ...)"
        def t6(self, a, b=None, *args, **kw): "(a, b=None, ..., ***)"

    def test(tests):
        ct = CallTips()
        failed=[]
        for t in tests:
            expected = t.__doc__ + "\n" + t.__doc__
            name = t.__name__
            arg_text = ct.fetch_tip(name)
            if arg_text != expected:
                failed.append(t)
                print "%s - expected %s, but got %s" % (t, expected,
                                                        get_arg_text(entity))
        print "%d of %d tests failed" % (len(failed), len(tests))

    tc = TC()
    tests = (t1, t2, t3, t4, t5, t6,
             TC, tc.t1, tc.t2, tc.t3, tc.t4, tc.t5, tc.t6)

    test(tests)
