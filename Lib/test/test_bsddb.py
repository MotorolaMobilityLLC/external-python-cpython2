#! /usr/bin/env python
"""Test script for the bsddb C module
   Roger E. Masse
"""
import os
import bsddb
import dbhash # Just so we know it's imported
import tempfile
from test_support import verbose, verify

def test(openmethod, what, ondisk=1):

    if verbose:
        print '\nTesting: ', what, (ondisk and "on disk" or "in memory")

    if ondisk:
        fname = tempfile.mktemp()
    else:
        fname = None
    f = openmethod(fname, 'c')
    verify(f.keys() == [])
    if verbose:
        print 'creation...'
    f['0'] = ''
    f['a'] = 'Guido'
    f['b'] = 'van'
    f['c'] = 'Rossum'
    f['d'] = 'invented'
    f['f'] = 'Python'
    if verbose:
        print '%s %s %s' % (f['a'], f['b'], f['c'])

    if what == 'BTree' :
        if verbose:
            print 'key ordering...'
        f.set_location(f.first()[0])
        while 1:
            try:
                rec = f.next()
            except KeyError:
                if rec != f.last():
                    print 'Error, last != last!'
                f.previous()
                break
            if verbose:
                print rec
        if not f.has_key('a'):
            print 'Error, missing key!'

    f.sync()
    f.close()
    if ondisk:
        # if we're using an in-memory only db, we can't reopen it
        # so finish here.
        if verbose:
            print 'modification...'
        f = openmethod(fname, 'w')
        f['d'] = 'discovered'

        if verbose:
            print 'access...'
        for key in f.keys():
            word = f[key]
            if verbose:
                print word

        f.close()
        try:
            os.remove(fname)
        except os.error:
            pass

types = [(bsddb.btopen, 'BTree'),
         (bsddb.hashopen, 'Hash Table'),
         (bsddb.btopen, 'BTree', 0),
         (bsddb.hashopen, 'Hash Table', 0),
         # (bsddb.rnopen,'Record Numbers'), 'put' for RECNO for bsddb 1.85
         #                                   appears broken... at least on
         #                                   Solaris Intel - rmasse 1/97
         ]

for type in types:
    test(*type)
