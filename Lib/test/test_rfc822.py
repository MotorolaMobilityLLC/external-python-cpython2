import rfc822
import sys
import test_support
import unittest

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class MessageTestCase(unittest.TestCase):
    def create_message(self, msg):
        return rfc822.Message(StringIO(msg))

    def test_get(self):
        msg = self.create_message(
            'To: "last, first" <userid@foo.net>\n\ntest\n')
        self.assert_(msg.get("to") == '"last, first" <userid@foo.net>')
        self.assert_(msg.get("TO") == '"last, first" <userid@foo.net>')
        self.assert_(msg.get("No-Such-Header") == "")
        self.assert_(msg.get("No-Such-Header", "No-Such-Value")
                     == "No-Such-Value")

    def test_setdefault(self):
        msg = self.create_message(
            'To: "last, first" <userid@foo.net>\n\ntest\n')
        self.assert_(not msg.has_key("New-Header"))
        self.assert_(msg.setdefault("New-Header", "New-Value") == "New-Value")
        self.assert_(msg.setdefault("New-Header", "Different-Value")
                     == "New-Value")
        self.assert_(msg["new-header"] == "New-Value")

        self.assert_(msg.setdefault("Another-Header") == "")
        self.assert_(msg["another-header"] == "")

    def check(self, msg, results):
        """Check addresses and the date."""
        m = self.create_message(msg)
        i = 0
        for n, a in m.getaddrlist('to') + m.getaddrlist('cc'):
            try:
                mn, ma = results[i][0], results[i][1]
            except IndexError:
                print 'extra parsed address:', repr(n), repr(a)
                continue
            i = i + 1
            if mn == n and ma == a:
                pass
            else:
                print 'not found:', repr(n), repr(a)

        out = m.getdate('date')
        if out:
            self.assertEqual(out,
                             (1999, 1, 13, 23, 57, 35, 0, 0, 0),
                             "date conversion failed")


    # Note: all test cases must have the same date (in various formats),
    # or no date!

    def test_basic(self):
        self.check(
            'Date:    Wed, 13 Jan 1999 23:57:35 -0500\n'
            'From:    Guido van Rossum <guido@CNRI.Reston.VA.US>\n'
            'To:      "Guido van\n'
            '\t : Rossum" <guido@python.org>\n'
            'Subject: test2\n'
            '\n'
            'test2\n',
            [('Guido van\n\t : Rossum', 'guido@python.org')])

        self.check(
            'From: Barry <bwarsaw@python.org\n'
            'To: guido@python.org (Guido: the Barbarian)\n'
            'Subject: nonsense\n'
            'Date: Wednesday, January 13 1999 23:57:35 -0500\n'
            '\n'
            'test',
            [('Guido: the Barbarian', 'guido@python.org')])

        self.check(
            'From: Barry <bwarsaw@python.org\n'
            'To: guido@python.org (Guido: the Barbarian)\n'
            'Cc: "Guido: the Madman" <guido@python.org>\n'
            'Date:  13-Jan-1999 23:57:35 EST\n'
            '\n'
            'test',
            [('Guido: the Barbarian', 'guido@python.org'),
             ('Guido: the Madman', 'guido@python.org')
             ])

        self.check(
            'To: "The monster with\n'
            '     the very long name: Guido" <guido@python.org>\n'
            'Date:    Wed, 13 Jan 1999 23:57:35 -0500\n'
            '\n'
            'test',
            [('The monster with\n     the very long name: Guido',
              'guido@python.org')])

        self.check(
            'To: "Amit J. Patel" <amitp@Theory.Stanford.EDU>\n'
            'CC: Mike Fletcher <mfletch@vrtelecom.com>,\n'
            '        "\'string-sig@python.org\'" <string-sig@python.org>\n'
            'Cc: fooz@bat.com, bart@toof.com\n'
            'Cc: goit@lip.com\n'
            'Date:    Wed, 13 Jan 1999 23:57:35 -0500\n'
            '\n'
            'test',
            [('Amit J. Patel', 'amitp@Theory.Stanford.EDU'),
             ('Mike Fletcher', 'mfletch@vrtelecom.com'),
             ("'string-sig@python.org'", 'string-sig@python.org'),
             ('', 'fooz@bat.com'),
             ('', 'bart@toof.com'),
             ('', 'goit@lip.com'),
             ])

    def test_twisted(self):
        # This one is just twisted.  I don't know what the proper
        # result should be, but it shouldn't be to infloop, which is
        # what used to happen!
        self.check(
            'To: <[smtp:dd47@mail.xxx.edu]_at_hmhq@hdq-mdm1-imgout.companay.com>\n'
            'Date:    Wed, 13 Jan 1999 23:57:35 -0500\n'
            '\n'
            'test',
            [('', ''),
             ('', 'dd47@mail.xxx.edu'),
             ('', '_at_hmhq@hdq-mdm1-imgout.companay.com'),
             ])

    def test_commas_in_full_name(self):
        # This exercises the old commas-in-a-full-name bug, which
        # should be doing the right thing in recent versions of the
        # module.
        self.check(
            'To: "last, first" <userid@foo.net>\n'
            '\n'
            'test',
            [('last, first', 'userid@foo.net')])

    def test_quoted_name(self):
        self.check(
            'To: (Comment stuff) "Quoted name"@somewhere.com\n'
            '\n'
            'test',
            [('Comment stuff', '"Quoted name"@somewhere.com')])

    def test_bogus_to_header(self):
        self.check(
            'To: :\n'
            'Cc: goit@lip.com\n'
            'Date:    Wed, 13 Jan 1999 23:57:35 -0500\n'
            '\n'
            'test',
            [('', 'goit@lip.com')])

    def test_addr_ipquad(self):
        self.check(
            'To: guido@[132.151.1.21]\n'
            '\n'
            'foo',
            [('', 'guido@[132.151.1.21]')])


test_support.run_unittest(MessageTestCase)
