"""Sort performance test."""

import sys
import time
import whrandom
import marshal
import tempfile
import operator
import os

td = tempfile.gettempdir()

def randrange(n):
    """Return a random shuffle of range(n)."""
    fn = os.path.join(td, "rr%06d" % n)
    try:
        fp = open(fn, "rb")
    except IOError:
        result = []
        for i in range(n):
            result.append(whrandom.random())
        try:
            try:
                fp = open(fn, "wb")
                marshal.dump(result, fp)
                fp.close()
                fp = None
            finally:
                if fp:
                    try:
                        os.unlink(fn)
                    except os.error:
                        pass
        except IOError, msg:
            print "can't write", fn, ":", msg
    else:
        result = marshal.load(fp)
        fp.close()
        ##assert len(result) == n
        # Shuffle it a bit...
        for i in range(10):
            i = whrandom.randint(0, n-1)
            temp = result[:i]
            del result[:i]
            temp.reverse()
            result[len(result):] = temp
            del temp
    return result

def fl():
    sys.stdout.flush()

def doit(L):
    t0 = time.clock()
    L.sort()
    t1 = time.clock()
    print "%6.2f" % (t1-t0),
    fl()

def tabulate(r):
    fmt = ("%2s %6s" + " %6s"*5)
    print fmt % ("i", "2**i", "*sort", "\\sort", "/sort", "~sort", "-sort")
    for i in r:
        n = 1<<i
        L = randrange(n)
        ##assert len(L) == n
        print "%2d %6d" % (i, n),
        fl()
        doit(L) # *sort
        L.reverse()
        doit(L) # \sort
        doit(L) # /sort
        if n > 4:
            L = map(operator.neg, map(operator.neg, L[:4]*(n/4)))
        doit(L) # ~sort
        L = map(abs, [-0.5]*n)
        doit(L) # -sort
        print

def main():
    import string
    # default range (inclusive)
    k1 = 15
    k2 = 19
    # one argument: single point
    # two arguments: specify range
    if sys.argv[1:]:
        k1 = string.atoi(sys.argv[1])
        k2 = k1
        if sys.argv[2:]:
            k2 = string.atoi(sys.argv[2])
            if sys.argv[3:]:
                # derive random seed from remaining arguments
                x, y, z = 0, 0, 0
                for a in sys.argv[3:]:
                    h = hash(a)
                    h, d = divmod(h, 256)
                    h = h & 0xffffff
                    x = (x^h^d) & 255
                    h = h>>8
                    y = (y^h^d) & 255
                    h = h>>8
                    z = (z^h^d) & 255
                whrandom.seed(x, y, z)
    r = range(k1, k2+1)
    tabulate(r)

if __name__ == '__main__':
    main()
