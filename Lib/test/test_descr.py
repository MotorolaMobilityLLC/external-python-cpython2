# Test descriptor-related enhancements

from test_support import verify, verbose
from copy import deepcopy

def testunop(a, res, expr="len(a)", meth="__len__"):
    if verbose: print "checking", expr
    dict = {'a': a}
    verify(eval(expr, dict) == res)
    t = type(a)
    m = getattr(t, meth)
    verify(m == t.__dict__[meth])
    verify(m(a) == res)
    bm = getattr(a, meth)
    verify(bm() == res)

def testbinop(a, b, res, expr="a+b", meth="__add__"):
    if verbose: print "checking", expr
    dict = {'a': a, 'b': b}
    verify(eval(expr, dict) == res)
    t = type(a)
    m = getattr(t, meth)
    verify(m == t.__dict__[meth])
    verify(m(a, b) == res)
    bm = getattr(a, meth)
    verify(bm(b) == res)

def testternop(a, b, c, res, expr="a[b:c]", meth="__getslice__"):
    if verbose: print "checking", expr
    dict = {'a': a, 'b': b, 'c': c}
    verify(eval(expr, dict) == res)
    t = type(a)
    m = getattr(t, meth)
    verify(m == t.__dict__[meth])
    verify(m(a, b, c) == res)
    bm = getattr(a, meth)
    verify(bm(b, c) == res)

def testsetop(a, b, res, stmt="a+=b", meth="__iadd__"):
    if verbose: print "checking", stmt
    dict = {'a': deepcopy(a), 'b': b}
    exec stmt in dict
    verify(dict['a'] == res)
    t = type(a)
    m = getattr(t, meth)
    verify(m == t.__dict__[meth])
    dict['a'] = deepcopy(a)
    m(dict['a'], b)
    verify(dict['a'] == res)
    dict['a'] = deepcopy(a)
    bm = getattr(dict['a'], meth)
    bm(b)
    verify(dict['a'] == res)

def testset2op(a, b, c, res, stmt="a[b]=c", meth="__setitem__"):
    if verbose: print "checking", stmt
    dict = {'a': deepcopy(a), 'b': b, 'c': c}
    exec stmt in dict
    verify(dict['a'] == res)
    t = type(a)
    m = getattr(t, meth)
    verify(m == t.__dict__[meth])
    dict['a'] = deepcopy(a)
    m(dict['a'], b, c)
    verify(dict['a'] == res)
    dict['a'] = deepcopy(a)
    bm = getattr(dict['a'], meth)
    bm(b, c)
    verify(dict['a'] == res)

def testset3op(a, b, c, d, res, stmt="a[b:c]=d", meth="__setslice__"):
    if verbose: print "checking", stmt
    dict = {'a': deepcopy(a), 'b': b, 'c': c, 'd': d}
    exec stmt in dict
    verify(dict['a'] == res)
    t = type(a)
    m = getattr(t, meth)
    verify(m == t.__dict__[meth])
    dict['a'] = deepcopy(a)
    m(dict['a'], b, c, d)
    verify(dict['a'] == res)
    dict['a'] = deepcopy(a)
    bm = getattr(dict['a'], meth)
    bm(b, c, d)
    verify(dict['a'] == res)

def lists():
    if verbose: print "Testing list operations..."
    testbinop([1], [2], [1,2], "a+b", "__add__")
    testbinop([1,2,3], 2, 1, "b in a", "__contains__")
    testbinop([1,2,3], 4, 0, "b in a", "__contains__")
    testbinop([1,2,3], 1, 2, "a[b]", "__getitem__")
    testternop([1,2,3], 0, 2, [1,2], "a[b:c]", "__getslice__")
    testsetop([1], [2], [1,2], "a+=b", "__iadd__")
    testsetop([1,2], 3, [1,2,1,2,1,2], "a*=b", "__imul__")
    testunop([1,2,3], 3, "len(a)", "__len__")
    testbinop([1,2], 3, [1,2,1,2,1,2], "a*b", "__mul__")
    testbinop([1,2], 3, [1,2,1,2,1,2], "b*a", "__rmul__")
    testset2op([1,2], 1, 3, [1,3], "a[b]=c", "__setitem__")
    testset3op([1,2,3,4], 1, 3, [5,6], [1,5,6,4], "a[b:c]=d", "__setslice__")

def dicts():
    if verbose: print "Testing dict operations..."
    testbinop({1:2}, {2:1}, -1, "cmp(a,b)", "__cmp__")
    testbinop({1:2,3:4}, 1, 1, "b in a", "__contains__")
    testbinop({1:2,3:4}, 2, 0, "b in a", "__contains__")
    testbinop({1:2,3:4}, 1, 2, "a[b]", "__getitem__")
    d = {1:2,3:4}
    l1 = []
    for i in d.keys(): l1.append(i)
    l = []
    for i in iter(d): l.append(i)
    verify(l == l1)
    l = []
    for i in d.__iter__(): l.append(i)
    verify(l == l1)
    l = []
    for i in dictionary.__iter__(d): l.append(i)
    verify(l == l1)
    d = {1:2, 3:4}
    testunop(d, 2, "len(a)", "__len__")
    verify(eval(repr(d), {}) == d)
    verify(eval(d.__repr__(), {}) == d)
    testset2op({1:2,3:4}, 2, 3, {1:2,2:3,3:4}, "a[b]=c", "__setitem__")

binops = {
    'add': '+',
    'sub': '-',
    'mul': '*',
    'div': '/',
    'mod': '%',
    'divmod': 'divmod',
    'pow': '**',
    'lshift': '<<',
    'rshift': '>>',
    'and': '&',
    'xor': '^',
    'or': '|',
    'cmp': 'cmp',
    'lt': '<',
    'le': '<=',
    'eq': '==',
    'ne': '!=',
    'gt': '>',
    'ge': '>=',
    }

for name, expr in binops.items():
    if expr.islower():
        expr = expr + "(a, b)"
    else:
        expr = 'a %s b' % expr
    binops[name] = expr

unops = {
    'pos': '+',
    'neg': '-',
    'abs': 'abs',
    'invert': '~',
    'int': 'int',
    'long': 'long',
    'float': 'float',
    'oct': 'oct',
    'hex': 'hex',
    }

for name, expr in unops.items():
    if expr.islower():
        expr = expr + "(a)"
    else:
        expr = '%s a' % expr
    unops[name] = expr

def numops(a, b, skip=[]):
    dict = {'a': a, 'b': b}
    for name, expr in binops.items():
        if name not in skip:
            name = "__%s__" % name
            if hasattr(a, name):
                res = eval(expr, dict)
                testbinop(a, b, res, expr, name)
    for name, expr in unops.items():
        name = "__%s__" % name
        if hasattr(a, name):
            res = eval(expr, dict)
            testunop(a, res, expr, name)

def ints():
    if verbose: print "Testing int operations..."
    numops(100, 3)

def longs():
    if verbose: print "Testing long operations..."
    numops(100L, 3L)

def floats():
    if verbose: print "Testing float operations..."
    numops(100.0, 3.0)

def complexes():
    if verbose: print "Testing complex operations..."
    numops(100.0j, 3.0j, skip=['lt', 'le', 'gt', 'ge'])
    class Number(complex):
        __slots__ = ['prec']
        def __init__(self, *args, **kwds):
            self.prec = kwds.get('prec', 12)
        def __repr__(self):
            prec = self.prec
            if self.imag == 0.0:
                return "%.*g" % (prec, self.real)
            if self.real == 0.0:
                return "%.*gj" % (prec, self.imag)
            return "(%.*g+%.*gj)" % (prec, self.real, prec, self.imag)
        __str__ = __repr__
    a = Number(3.14, prec=6)
    verify(`a` == "3.14")
    verify(a.prec == 6)

def spamlists():
    if verbose: print "Testing spamlist operations..."
    import copy, xxsubtype as spam
    def spamlist(l, memo=None):
        import xxsubtype as spam
        return spam.spamlist(l)
    # This is an ugly hack:
    copy._deepcopy_dispatch[spam.spamlist] = spamlist

    testbinop(spamlist([1]), spamlist([2]), spamlist([1,2]), "a+b", "__add__")
    testbinop(spamlist([1,2,3]), 2, 1, "b in a", "__contains__")
    testbinop(spamlist([1,2,3]), 4, 0, "b in a", "__contains__")
    testbinop(spamlist([1,2,3]), 1, 2, "a[b]", "__getitem__")
    testternop(spamlist([1,2,3]), 0, 2, spamlist([1,2]),
               "a[b:c]", "__getslice__")
    testsetop(spamlist([1]), spamlist([2]), spamlist([1,2]),
              "a+=b", "__iadd__")
    testsetop(spamlist([1,2]), 3, spamlist([1,2,1,2,1,2]), "a*=b", "__imul__")
    testunop(spamlist([1,2,3]), 3, "len(a)", "__len__")
    testbinop(spamlist([1,2]), 3, spamlist([1,2,1,2,1,2]), "a*b", "__mul__")
    testbinop(spamlist([1,2]), 3, spamlist([1,2,1,2,1,2]), "b*a", "__rmul__")
    testset2op(spamlist([1,2]), 1, 3, spamlist([1,3]), "a[b]=c", "__setitem__")
    testset3op(spamlist([1,2,3,4]), 1, 3, spamlist([5,6]),
               spamlist([1,5,6,4]), "a[b:c]=d", "__setslice__")
    # Test subclassing
    class C(spam.spamlist):
        def foo(self): return 1
    a = C()
    verify(a == [])
    verify(a.foo() == 1)
    a.append(100)
    verify(a == [100])
    verify(a.getstate() == 0)
    a.setstate(42)
    verify(a.getstate() == 42)

def spamdicts():
    if verbose: print "Testing spamdict operations..."
    import copy, xxsubtype as spam
    def spamdict(d, memo=None):
        import xxsubtype as spam
        sd = spam.spamdict()
        for k, v in d.items(): sd[k] = v
        return sd
    # This is an ugly hack:
    copy._deepcopy_dispatch[spam.spamdict] = spamdict

    testbinop(spamdict({1:2}), spamdict({2:1}), -1, "cmp(a,b)", "__cmp__")
    testbinop(spamdict({1:2,3:4}), 1, 1, "b in a", "__contains__")
    testbinop(spamdict({1:2,3:4}), 2, 0, "b in a", "__contains__")
    testbinop(spamdict({1:2,3:4}), 1, 2, "a[b]", "__getitem__")
    d = spamdict({1:2,3:4})
    l1 = []
    for i in d.keys(): l1.append(i)
    l = []
    for i in iter(d): l.append(i)
    verify(l == l1)
    l = []
    for i in d.__iter__(): l.append(i)
    verify(l == l1)
    l = []
    for i in type(spamdict({})).__iter__(d): l.append(i)
    verify(l == l1)
    straightd = {1:2, 3:4}
    spamd = spamdict(straightd)
    testunop(spamd, 2, "len(a)", "__len__")
    testunop(spamd, repr(straightd), "repr(a)", "__repr__")
    testset2op(spamdict({1:2,3:4}), 2, 3, spamdict({1:2,2:3,3:4}),
               "a[b]=c", "__setitem__")
    # Test subclassing
    class C(spam.spamdict):
        def foo(self): return 1
    a = C()
    verify(a.items() == [])
    verify(a.foo() == 1)
    a['foo'] = 'bar'
    verify(a.items() == [('foo', 'bar')])
    verify(a.getstate() == 0)
    a.setstate(100)
    verify(a.getstate() == 100)

def pydicts():
    if verbose: print "Testing Python subclass of dict..."
    verify(issubclass(dictionary, dictionary))
    verify(isinstance({}, dictionary))
    d = dictionary()
    verify(d == {})
    verify(d.__class__ is dictionary)
    verify(isinstance(d, dictionary))
    class C(dictionary):
        state = -1
        def __init__(self, *a, **kw):
            if a:
                assert len(a) == 1
                self.state = a[0]
            if kw:
                for k, v in kw.items(): self[v] = k
        def __getitem__(self, key):
            return self.get(key, 0)
        def __setitem__(self, key, value):
            assert isinstance(key, type(0))
            dictionary.__setitem__(self, key, value)
        def setstate(self, state):
            self.state = state
        def getstate(self):
            return self.state
    verify(issubclass(C, dictionary))
    a1 = C(12)
    verify(a1.state == 12)
    a2 = C(foo=1, bar=2)
    verify(a2[1] == 'foo' and a2[2] == 'bar')
    a = C()
    verify(a.state == -1)
    verify(a.getstate() == -1)
    a.setstate(0)
    verify(a.state == 0)
    verify(a.getstate() == 0)
    a.setstate(10)
    verify(a.state == 10)
    verify(a.getstate() == 10)
    verify(a[42] == 0)
    a[42] = 24
    verify(a[42] == 24)
    if verbose: print "pydict stress test ..."
    N = 50
    for i in range(N):
        a[i] = C()
        for j in range(N):
            a[i][j] = i*j
    for i in range(N):
        for j in range(N):
            verify(a[i][j] == i*j)

def pylists():
    if verbose: print "Testing Python subclass of list..."
    class C(list):
        def __getitem__(self, i):
            return list.__getitem__(self, i) + 100
        def __getslice__(self, i, j):
            return (i, j)
    a = C()
    a.extend([0,1,2])
    verify(a[0] == 100)
    verify(a[1] == 101)
    verify(a[2] == 102)
    verify(a[100:200] == (100,200))

def metaclass():
    if verbose: print "Testing __metaclass__..."
    class C:
        __metaclass__ = type
        def __init__(self):
            self.__state = 0
        def getstate(self):
            return self.__state
        def setstate(self, state):
            self.__state = state
    a = C()
    verify(a.getstate() == 0)
    a.setstate(10)
    verify(a.getstate() == 10)
    class D:
        class __metaclass__(type):
            def myself(cls): return cls
    verify(D.myself() == D)
    d = D()
    verify(d.__class__ is D)
    class M1(type):
        def __new__(cls, name, bases, dict):
            dict['__spam__'] = 1
            return type.__new__(cls, name, bases, dict)
    class C:
        __metaclass__ = M1
    verify(C.__spam__ == 1)
    c = C()
    verify(c.__spam__ == 1)
    class _instance(object):
        pass
    class M2(object):
        def __new__(cls, name, bases, dict):
            self = object.__new__(cls)
            self.name = name
            self.bases = bases
            self.dict = dict
            return self
        __new__ = staticmethod(__new__)
        def __call__(self):
            it = _instance()
            # Early binding of methods
            for key in self.dict:
                if key.startswith("__"):
                    continue
                setattr(it, key, self.dict[key].__get__(it, self))
            return it
    class C:
        __metaclass__ = M2
        def spam(self):
            return 42
    verify(C.name == 'C')
    verify(C.bases == ())
    verify('spam' in C.dict)
    c = C()
    verify(c.spam() == 42)

def pymods():
    if verbose: print "Testing Python subclass of module..."
    log = []
    import sys
    MT = type(sys)
    class MM(MT):
        def __init__(self):
            MT.__init__(self)
        def __getattr__(self, name):
            log.append(("getattr", name))
            return MT.__getattr__(self, name)
        def __setattr__(self, name, value):
            log.append(("setattr", name, value))
            MT.__setattr__(self, name, value)
        def __delattr__(self, name):
            log.append(("delattr", name))
            MT.__delattr__(self, name)
    a = MM()
    a.foo = 12
    x = a.foo
    del a.foo
    verify(log == [("setattr", "foo", 12),
                   ("getattr", "foo"),
                   ("delattr", "foo")], log)

def multi():
    if verbose: print "Testing multiple inheritance..."
    class C(object):
        def __init__(self):
            self.__state = 0
        def getstate(self):
            return self.__state
        def setstate(self, state):
            self.__state = state
    a = C()
    verify(a.getstate() == 0)
    a.setstate(10)
    verify(a.getstate() == 10)
    class D(dictionary, C):
        def __init__(self):
            type({}).__init__(self)
            C.__init__(self)
    d = D()
    verify(d.keys() == [])
    d["hello"] = "world"
    verify(d.items() == [("hello", "world")])
    verify(d["hello"] == "world")
    verify(d.getstate() == 0)
    d.setstate(10)
    verify(d.getstate() == 10)
    verify(D.__mro__ == (D, dictionary, C, object))

    # SF bug #442833
    class Node(object):
        def __int__(self):
            return int(self.foo())
        def foo(self):
            return "23"
    class Frag(Node, list):
        def foo(self):
            return "42"
    verify(Node().__int__() == 23)
    verify(int(Node()) == 23)
    verify(Frag().__int__() == 42)
    verify(int(Frag()) == 42)

def diamond():
    if verbose: print "Testing multiple inheritance special cases..."
    class A(object):
        def spam(self): return "A"
    verify(A().spam() == "A")
    class B(A):
        def boo(self): return "B"
        def spam(self): return "B"
    verify(B().spam() == "B")
    verify(B().boo() == "B")
    class C(A):
        def boo(self): return "C"
    verify(C().spam() == "A")
    verify(C().boo() == "C")
    class D(B, C): pass
    verify(D().spam() == "B")
    verify(D().boo() == "B")
    verify(D.__mro__ == (D, B, C, A, object))
    class E(C, B): pass
    verify(E().spam() == "B")
    verify(E().boo() == "C")
    verify(E.__mro__ == (E, C, B, A, object))
    class F(D, E): pass
    verify(F().spam() == "B")
    verify(F().boo() == "B")
    verify(F.__mro__ == (F, D, E, B, C, A, object))
    class G(E, D): pass
    verify(G().spam() == "B")
    verify(G().boo() == "C")
    verify(G.__mro__ == (G, E, D, C, B, A, object))

def objects():
    if verbose: print "Testing object class..."
    a = object()
    verify(a.__class__ == object == type(a))
    b = object()
    verify(a is not b)
    verify(not hasattr(a, "foo"))
    try:
        a.foo = 12
    except (AttributeError, TypeError):
        pass
    else:
        verify(0, "object() should not allow setting a foo attribute")
    verify(not hasattr(object(), "__dict__"))

    class Cdict(object):
        pass
    x = Cdict()
    verify(x.__dict__ is None)
    x.foo = 1
    verify(x.foo == 1)
    verify(x.__dict__ == {'foo': 1})

def slots():
    if verbose: print "Testing __slots__..."
    class C0(object):
        __slots__ = []
    x = C0()
    verify(not hasattr(x, "__dict__"))
    verify(not hasattr(x, "foo"))

    class C1(object):
        __slots__ = ['a']
    x = C1()
    verify(not hasattr(x, "__dict__"))
    verify(x.a == None)
    x.a = 1
    verify(x.a == 1)
    del x.a
    verify(x.a == None)

    class C3(object):
        __slots__ = ['a', 'b', 'c']
    x = C3()
    verify(not hasattr(x, "__dict__"))
    verify(x.a is None)
    verify(x.b is None)
    verify(x.c is None)
    x.a = 1
    x.b = 2
    x.c = 3
    verify(x.a == 1)
    verify(x.b == 2)
    verify(x.c == 3)

def dynamics():
    if verbose: print "Testing __dynamic__..."
    verify(object.__dynamic__ == 0)
    verify(list.__dynamic__ == 0)
    class S1:
        __metaclass__ = type
    verify(S1.__dynamic__ == 0)
    class S(object):
        pass
    verify(S.__dynamic__ == 0)
    class D(object):
        __dynamic__ = 1
    verify(D.__dynamic__ == 1)
    class E(D, S):
        pass
    verify(E.__dynamic__ == 1)
    class F(S, D):
        pass
    verify(F.__dynamic__ == 1)
    try:
        S.foo = 1
    except (AttributeError, TypeError):
        pass
    else:
        verify(0, "assignment to a static class attribute should be illegal")
    D.foo = 1
    verify(D.foo == 1)
    # Test that dynamic attributes are inherited
    verify(E.foo == 1)
    verify(F.foo == 1)
    class SS(D):
        __dynamic__ = 0
    verify(SS.__dynamic__ == 0)
    verify(SS.foo == 1)
    try:
        SS.foo = 1
    except (AttributeError, TypeError):
        pass
    else:
        verify(0, "assignment to SS.foo should be illegal")
    # Test dynamic instances
    class C(object):
        __dynamic__ = 1
    a = C()
    verify(not hasattr(a, "foobar"))
    C.foobar = 2
    verify(a.foobar == 2)
    C.method = lambda self: 42
    verify(a.method() == 42)
    C.__repr__ = lambda self: "C()"
    verify(repr(a) == "C()")
    C.__int__ = lambda self: 100
    verify(int(a) == 100)
    verify(a.foobar == 2)
    verify(not hasattr(a, "spam"))
    def mygetattr(self, name):
        if name == "spam":
            return "spam"
        else:
            return object.__getattr__(self, name)
    C.__getattr__ = mygetattr
    verify(a.spam == "spam")
    a.new = 12
    verify(a.new == 12)
    def mysetattr(self, name, value):
        if name == "spam":
            raise AttributeError
        return object.__setattr__(self, name, value)
    C.__setattr__ = mysetattr
    try:
        a.spam = "not spam"
    except AttributeError:
        pass
    else:
        verify(0, "expected AttributeError")
    verify(a.spam == "spam")
    class D(C):
        pass
    d = D()
    d.foo = 1
    verify(d.foo == 1)

def errors():
    if verbose: print "Testing errors..."

    try:
        class C(list, dictionary):
            pass
    except TypeError:
        pass
    else:
        verify(0, "inheritance from both list and dict should be illegal")

    try:
        class C(object, None):
            pass
    except TypeError:
        pass
    else:
        verify(0, "inheritance from non-type should be illegal")
    class Classic:
        pass

    try:
        class C(object, Classic):
            pass
    except TypeError:
        pass
    else:
        verify(0, "inheritance from object and Classic should be illegal")

    try:
        class C(type(len)):
            pass
    except TypeError:
        pass
    else:
        verify(0, "inheritance from CFunction should be illegal")

    try:
        class C(object):
            __slots__ = 1
    except TypeError:
        pass
    else:
        verify(0, "__slots__ = 1 should be illegal")

    try:
        class C(object):
            __slots__ = [1]
    except TypeError:
        pass
    else:
        verify(0, "__slots__ = [1] should be illegal")

def classmethods():
    if verbose: print "Testing class methods..."
    class C(object):
        def foo(*a): return a
        goo = classmethod(foo)
    c = C()
    verify(C.goo(1) == (C, 1))
    verify(c.goo(1) == (C, 1))
    verify(c.foo(1) == (c, 1))
    class D(C):
        pass
    d = D()
    verify(D.goo(1) == (D, 1))
    verify(d.goo(1) == (D, 1))
    verify(d.foo(1) == (d, 1))
    verify(D.foo(d, 1) == (d, 1))

def staticmethods():
    if verbose: print "Testing static methods..."
    class C(object):
        def foo(*a): return a
        goo = staticmethod(foo)
    c = C()
    verify(C.goo(1) == (1,))
    verify(c.goo(1) == (1,))
    verify(c.foo(1) == (c, 1,))
    class D(C):
        pass
    d = D()
    verify(D.goo(1) == (1,))
    verify(d.goo(1) == (1,))
    verify(d.foo(1) == (d, 1))
    verify(D.foo(d, 1) == (d, 1))

def classic():
    if verbose: print "Testing classic classes..."
    class C:
        def foo(*a): return a
        goo = classmethod(foo)
    c = C()
    verify(C.goo(1) == (C, 1))
    verify(c.goo(1) == (C, 1))
    verify(c.foo(1) == (c, 1))
    class D(C):
        pass
    d = D()
    verify(D.goo(1) == (D, 1))
    verify(d.goo(1) == (D, 1))
    verify(d.foo(1) == (d, 1))
    verify(D.foo(d, 1) == (d, 1))
    class E: # *not* subclassing from C
        foo = C.foo
    verify(E().foo == C.foo) # i.e., unbound
    verify(repr(C.foo.__get__(C())).startswith("<bound method "))

def compattr():
    if verbose: print "Testing computed attributes..."
    class C(object):
        class computed_attribute(object):
            def __init__(self, get, set=None):
                self.__get = get
                self.__set = set
            def __get__(self, obj, type=None):
                return self.__get(obj)
            def __set__(self, obj, value):
                return self.__set(obj, value)
        def __init__(self):
            self.__x = 0
        def __get_x(self):
            x = self.__x
            self.__x = x+1
            return x
        def __set_x(self, x):
            self.__x = x
        x = computed_attribute(__get_x, __set_x)
    a = C()
    verify(a.x == 0)
    verify(a.x == 1)
    a.x = 10
    verify(a.x == 10)
    verify(a.x == 11)

def newslot():
    if verbose: print "Testing __new__ slot override..."
    class C(list):
        def __new__(cls):
            self = list.__new__(cls)
            self.foo = 1
            return self
        def __init__(self):
            self.foo = self.foo + 2
    a = C()
    verify(a.foo == 3)
    verify(a.__class__ is C)
    class D(C):
        pass
    b = D()
    verify(b.foo == 3)
    verify(b.__class__ is D)

def altmro():
    if verbose: print "Testing mro() and overriding it..."
    class A(object):
        def f(self): return "A"
    class B(A):
        pass
    class C(A):
        def f(self): return "C"
    class D(B, C):
        pass
    verify(D.mro() == [D, B, C, A, object] == list(D.__mro__))
    verify(D().f() == "C")
    class PerverseMetaType(type):
        def mro(cls):
            L = type.mro(cls)
            L.reverse()
            return L
    class X(A,B,C,D):
        __metaclass__ = PerverseMetaType
    verify(X.__mro__ == (object, A, C, B, D, X))
    verify(X().f() == "A")

def overloading():
    if verbose: print "Testing operator overloading..."

    class B(object):
        "Intermediate class because object doesn't have a __setattr__"

    class C(B):

        def __getattr__(self, name):
            if name == "foo":
                return ("getattr", name)
            else:
                return B.__getattr__(self, name)
        def __setattr__(self, name, value):
            if name == "foo":
                self.setattr = (name, value)
            else:
                return B.__setattr__(self, name, value)
        def __delattr__(self, name):
            if name == "foo":
                self.delattr = name
            else:
                return B.__delattr__(self, name)

        def __getitem__(self, key):
            return ("getitem", key)
        def __setitem__(self, key, value):
            self.setitem = (key, value)
        def __delitem__(self, key):
            self.delitem = key

        def __getslice__(self, i, j):
            return ("getslice", i, j)
        def __setslice__(self, i, j, value):
            self.setslice = (i, j, value)
        def __delslice__(self, i, j):
            self.delslice = (i, j)

    a = C()
    verify(a.foo == ("getattr", "foo"))
    a.foo = 12
    verify(a.setattr == ("foo", 12))
    del a.foo
    verify(a.delattr == "foo")

    verify(a[12] == ("getitem", 12))
    a[12] = 21
    verify(a.setitem == (12, 21))
    del a[12]
    verify(a.delitem == 12)

    verify(a[0:10] == ("getslice", 0, 10))
    a[0:10] = "foo"
    verify(a.setslice == (0, 10, "foo"))
    del a[0:10]
    verify(a.delslice == (0, 10))

def methods():
    if verbose: print "Testing methods..."
    class C(object):
        def __init__(self, x):
            self.x = x
        def foo(self):
            return self.x
    c1 = C(1)
    verify(c1.foo() == 1)
    class D(C):
        boo = C.foo
        goo = c1.foo
    d2 = D(2)
    verify(d2.foo() == 2)
    verify(d2.boo() == 2)
    verify(d2.goo() == 1)
    class E(object):
        foo = C.foo
    verify(E().foo == C.foo) # i.e., unbound
    verify(repr(C.foo.__get__(C(1))).startswith("<bound method "))

def specials():
    # Test operators like __hash__ for which a built-in default exists
    if verbose: print "Testing special operators..."
    # Test the default behavior for static classes
    class C(object):
        def __getitem__(self, i):
            if 0 <= i < 10: return i
            raise IndexError
    c1 = C()
    c2 = C()
    verify(not not c1)
    verify(hash(c1) == id(c1))
    verify(cmp(c1, c2) == cmp(id(c1), id(c2)))
    verify(c1 == c1)
    verify(c1 != c2)
    verify(not c1 != c1)
    verify(not c1 == c2)
    # Note that the module name appears in str/repr, and that varies
    # depending on whether this test is run standalone or from a framework.
    verify(str(c1).find('C instance at ') >= 0)
    verify(str(c1) == repr(c1))
    verify(-1 not in c1)
    for i in range(10):
        verify(i in c1)
    verify(10 not in c1)
    # Test the default behavior for dynamic classes
    class D(object):
        __dynamic__ = 1
        def __getitem__(self, i):
            if 0 <= i < 10: return i
            raise IndexError
    d1 = D()
    d2 = D()
    verify(not not d1)
    verify(hash(d1) == id(d1))
    verify(cmp(d1, d2) == cmp(id(d1), id(d2)))
    verify(d1 == d1)
    verify(d1 != d2)
    verify(not d1 != d1)
    verify(not d1 == d2)
    # Note that the module name appears in str/repr, and that varies
    # depending on whether this test is run standalone or from a framework.
    verify(str(d1).find('D instance at ') >= 0)
    verify(str(d1) == repr(d1))
    verify(-1 not in d1)
    for i in range(10):
        verify(i in d1)
    verify(10 not in d1)
    # Test overridden behavior for static classes
    class Proxy(object):
        def __init__(self, x):
            self.x = x
        def __nonzero__(self):
            return not not self.x
        def __hash__(self):
            return hash(self.x)
        def __eq__(self, other):
            return self.x == other
        def __ne__(self, other):
            return self.x != other
        def __cmp__(self, other):
            return cmp(self.x, other.x)
        def __str__(self):
            return "Proxy:%s" % self.x
        def __repr__(self):
            return "Proxy(%r)" % self.x
        def __contains__(self, value):
            return value in self.x
    p0 = Proxy(0)
    p1 = Proxy(1)
    p_1 = Proxy(-1)
    verify(not p0)
    verify(not not p1)
    verify(hash(p0) == hash(0))
    verify(p0 == p0)
    verify(p0 != p1)
    verify(not p0 != p0)
    verify(not p0 == p1)
    verify(cmp(p0, p1) == -1)
    verify(cmp(p0, p0) == 0)
    verify(cmp(p0, p_1) == 1)
    verify(str(p0) == "Proxy:0")
    verify(repr(p0) == "Proxy(0)")
    p10 = Proxy(range(10))
    verify(-1 not in p10)
    for i in range(10):
        verify(i in p10)
    verify(10 not in p10)
    # Test overridden behavior for dynamic classes
    class DProxy(object):
        __dynamic__ = 1
        def __init__(self, x):
            self.x = x
        def __nonzero__(self):
            return not not self.x
        def __hash__(self):
            return hash(self.x)
        def __eq__(self, other):
            return self.x == other
        def __ne__(self, other):
            return self.x != other
        def __cmp__(self, other):
            return cmp(self.x, other.x)
        def __str__(self):
            return "DProxy:%s" % self.x
        def __repr__(self):
            return "DProxy(%r)" % self.x
        def __contains__(self, value):
            return value in self.x
    p0 = DProxy(0)
    p1 = DProxy(1)
    p_1 = DProxy(-1)
    verify(not p0)
    verify(not not p1)
    verify(hash(p0) == hash(0))
    verify(p0 == p0)
    verify(p0 != p1)
    verify(not p0 != p0)
    verify(not p0 == p1)
    verify(cmp(p0, p1) == -1)
    verify(cmp(p0, p0) == 0)
    verify(cmp(p0, p_1) == 1)
    verify(str(p0) == "DProxy:0")
    verify(repr(p0) == "DProxy(0)")
    p10 = DProxy(range(10))
    verify(-1 not in p10)
    for i in range(10):
        verify(i in p10)
    verify(10 not in p10)

def weakrefs():
    if verbose: print "Testing weak references..."
    import weakref
    class C(object):
        pass
    c = C()
    r = weakref.ref(c)
    verify(r() is c)
    del c
    verify(r() is None)
    del r
    class NoWeak(object):
        __slots__ = ['foo']
    no = NoWeak()
    try:
        weakref.ref(no)
    except TypeError, msg:
        verify(str(msg).find("weakly") >= 0)
    else:
        verify(0, "weakref.ref(no) should be illegal")
    class Weak(object):
        __slots__ = ['foo', '__weakref__']
    yes = Weak()
    r = weakref.ref(yes)
    verify(r() is yes)
    del yes
    verify(r() is None)
    del r

def getsets():
    if verbose: print "Testing getset..."
    class C(object):
        def getx(self):
            return self.__x
        def setx(self, value):
            self.__x = value
        def delx(self):
            del self.__x
        x = getset(getx, setx, delx)
    a = C()
    verify(not hasattr(a, "x"))
    a.x = 42
    verify(a._C__x == 42)
    verify(a.x == 42)
    del a.x
    verify(not hasattr(a, "x"))
    verify(not hasattr(a, "_C__x"))
    C.x.__set__(a, 100)
    verify(C.x.__get__(a) == 100)
##    C.x.__set__(a)
##    verify(not hasattr(a, "x"))

def supers():
    if verbose: print "Testing super..."

    class A(object):
        def meth(self, a):
            return "A(%r)" % a

    verify(A().meth(1) == "A(1)")

    class B(A):
        def __init__(self):
            self.__super = super(B, self)
        def meth(self, a):
            return "B(%r)" % a + self.__super.meth(a)

    verify(B().meth(2) == "B(2)A(2)")

    class C(A):
        __dynamic__ = 1
        def meth(self, a):
            return "C(%r)" % a + self.__super.meth(a)
    C._C__super = super(C)

    verify(C().meth(3) == "C(3)A(3)")

    class D(C, B):
        def meth(self, a):
            return "D(%r)" % a + super(D, self).meth(a)

    verify (D().meth(4) == "D(4)C(4)B(4)A(4)")

def inherits():
    if verbose: print "Testing inheritance from basic types..."

    class hexint(int):
        def __repr__(self):
            return hex(self)
        def __add__(self, other):
            return hexint(int.__add__(self, other))
        # (Note that overriding __radd__ doesn't work,
        # because the int type gets first dibs.)
    verify(repr(hexint(7) + 9) == "0x10")
    verify(repr(hexint(1000) + 7) == "0x3ef")

    class octlong(long):
        __slots__ = []
        def __str__(self):
            s = oct(self)
            if s[-1] == 'L':
                s = s[:-1]
            return s
        def __add__(self, other):
            return self.__class__(super(octlong, self).__add__(other))
        __radd__ = __add__
    verify(str(octlong(3) + 5) == "010")
    # (Note that overriding __radd__ here only seems to work
    # because the example uses a short int left argument.)
    verify(str(5 + octlong(3000)) == "05675")

    class precfloat(float):
        __slots__ = ['prec']
        def __init__(self, value=0.0, prec=12):
            self.prec = int(prec)
            float.__init__(value)
        def __repr__(self):
            return "%.*g" % (self.prec, self)
    verify(repr(precfloat(1.1)) == "1.1")

    class madtuple(tuple):
        _rev = None
        def rev(self):
            if self._rev is not None:
                return self._rev
            L = list(self)
            L.reverse()
            self._rev = self.__class__(L)
            return self._rev
    a = madtuple((1,2,3,4,5,6,7,8,9,0))
    verify(a.rev() == madtuple((0,9,8,7,6,5,4,3,2,1)))
    verify(a.rev().rev() == madtuple((1,2,3,4,5,6,7,8,9,0)))
    for i in range(512):
        t = madtuple(range(i))
        u = t.rev()
        v = u.rev()
        verify(v == t)

    class madstring(str):
        _rev = None
        def rev(self):
            if self._rev is not None:
                return self._rev
            L = list(self)
            L.reverse()
            self._rev = self.__class__("".join(L))
            return self._rev
    s = madstring("abcdefghijklmnopqrstuvwxyz")
    verify(s.rev() == madstring("zyxwvutsrqponmlkjihgfedcba"))
    verify(s.rev().rev() == madstring("abcdefghijklmnopqrstuvwxyz"))
    for i in range(256):
        s = madstring("".join(map(chr, range(i))))
        t = s.rev()
        u = t.rev()
        verify(u == s)

def all():
    lists()
    dicts()
    ints()
    longs()
    floats()
    complexes()
    spamlists()
    spamdicts()
    pydicts()
    pylists()
    metaclass()
    pymods()
    multi()
    diamond()
    objects()
    slots()
    dynamics()
    errors()
    classmethods()
    staticmethods()
    classic()
    compattr()
    newslot()
    altmro()
    overloading()
    methods()
    specials()
    weakrefs()
    getsets()
    supers()
    inherits()

all()

if verbose: print "All OK"
