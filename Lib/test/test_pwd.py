import unittest
from test import test_support

import pwd

class PwdTest(unittest.TestCase):

    def test_values(self):
        entries = pwd.getpwall()

        for e in entries:
            self.assertEqual(len(e), 7)
            self.assertEqual(e[0], e.pw_name)
            self.assert_(isinstance(e.pw_name, basestring))
            self.assertEqual(e[1], e.pw_passwd)
            self.assert_(isinstance(e.pw_passwd, basestring))
            self.assertEqual(e[2], e.pw_uid)
            self.assert_(isinstance(e.pw_uid, int))
            self.assertEqual(e[3], e.pw_gid)
            self.assert_(isinstance(e.pw_gid, int))
            self.assertEqual(e[4], e.pw_gecos)
            self.assert_(isinstance(e.pw_gecos, basestring))
            self.assertEqual(e[5], e.pw_dir)
            self.assert_(isinstance(e.pw_dir, basestring))
            self.assertEqual(e[6], e.pw_shell)
            self.assert_(isinstance(e.pw_shell, basestring))

            self.assertEqual(pwd.getpwnam(e.pw_name), e)
            self.assertEqual(pwd.getpwuid(e.pw_uid), e)

    def test_errors(self):
        self.assertRaises(TypeError, pwd.getpwuid)
        self.assertRaises(TypeError, pwd.getpwnam)
        self.assertRaises(TypeError, pwd.getpwall, 42)

        # try to get some errors
        bynames = {}
        byuids = {}
        for (n, p, u, g, gecos, d, s) in pwd.getpwall():
            bynames[n] = u
            byuids[u] = n

        allnames = bynames.keys()
        namei = 0
        fakename = allnames[namei]
        while fakename in bynames:
            chars = map(None, fakename)
            for i in xrange(len(chars)):
                if chars[i] == 'z':
                    chars[i] = 'A'
                    break
                elif chars[i] == 'Z':
                    continue
                else:
                    chars[i] = chr(ord(chars[i]) + 1)
                    break
            else:
                namei = namei + 1
                try:
                    fakename = allnames[namei]
                except IndexError:
                    # should never happen... if so, just forget it
                    break
            fakename = ''.join(map(None, chars))

        self.assertRaises(KeyError, pwd.getpwnam, fakename)

        # Choose a non-existent uid.
        fakeuid = 4127
        while fakeuid in byuids:
            fakeuid = (fakeuid * 3) % 0x10000

        self.assertRaises(KeyError, pwd.getpwuid, fakeuid)

def test_main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PwdTest))
    test_support.run_suite(suite)

if __name__ == "__main__":
    test_main()

