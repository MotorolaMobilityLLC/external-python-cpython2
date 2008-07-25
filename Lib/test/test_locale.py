from test.support import run_unittest, TestSkipped, verbose
import unittest
import locale
import sys
import codecs

class BaseLocalizedTest(unittest.TestCase):
    #
    # Base class for tests using a real locale
    #

    if sys.platform.startswith("win"):
        tlocs = ("En", "English")
    else:
        tlocs = ("en_US.UTF-8", "en_US.US-ASCII", "en_US")

    def setUp(self):
        if sys.platform == 'darwin':
            raise TestSkipped(
                "Locale support on MacOSX is minimal and cannot be tested")
        self.oldlocale = locale.setlocale(self.locale_type)
        for tloc in self.tlocs:
            try:
                locale.setlocale(self.locale_type, tloc)
            except locale.Error:
                continue
            break
        else:
            raise TestSkipped(
                "Test locale not supported (tried %s)" % (', '.join(self.tlocs)))
        if verbose:
            print("testing with \"%s\"..." % tloc, end=' ')

    def tearDown(self):
        locale.setlocale(self.locale_type, self.oldlocale)


class BaseCookedTest(unittest.TestCase):
    #
    # Base class for tests using cooked localeconv() values
    #

    def setUp(self):
        locale._override_localeconv = self.cooked_values

    def tearDown(self):
        locale._override_localeconv = {}

class CCookedTest(BaseCookedTest):
    # A cooked "C" locale

    cooked_values = {
        'currency_symbol': '',
        'decimal_point': '.',
        'frac_digits': 127,
        'grouping': [],
        'int_curr_symbol': '',
        'int_frac_digits': 127,
        'mon_decimal_point': '',
        'mon_grouping': [],
        'mon_thousands_sep': '',
        'n_cs_precedes': 127,
        'n_sep_by_space': 127,
        'n_sign_posn': 127,
        'negative_sign': '',
        'p_cs_precedes': 127,
        'p_sep_by_space': 127,
        'p_sign_posn': 127,
        'positive_sign': '',
        'thousands_sep': ''
    }

class EnUSCookedTest(BaseCookedTest):
    # A cooked "en_US" locale

    cooked_values = {
        'currency_symbol': '$',
        'decimal_point': '.',
        'frac_digits': 2,
        'grouping': [3, 3, 0],
        'int_curr_symbol': 'USD ',
        'int_frac_digits': 2,
        'mon_decimal_point': '.',
        'mon_grouping': [3, 3, 0],
        'mon_thousands_sep': ',',
        'n_cs_precedes': 1,
        'n_sep_by_space': 0,
        'n_sign_posn': 1,
        'negative_sign': '-',
        'p_cs_precedes': 1,
        'p_sep_by_space': 0,
        'p_sign_posn': 1,
        'positive_sign': '',
        'thousands_sep': ','
    }


class BaseFormattingTest(object):
    #
    # Utility functions for formatting tests
    #

    def _test_formatfunc(self, format, value, out, func, **format_opts):
        self.assertEqual(
            func(format, value, **format_opts), out)

    def _test_format(self, format, value, out, **format_opts):
        self._test_formatfunc(format, value, out,
            func=locale.format, **format_opts)

    def _test_format_string(self, format, value, out, **format_opts):
        self._test_formatfunc(format, value, out,
            func=locale.format_string, **format_opts)

    def _test_currency(self, value, out, **format_opts):
        self.assertEqual(locale.currency(value, **format_opts), out)


class EnUSNumberFormatting(BaseFormattingTest):

    def setUp(self):
        # NOTE: On Solaris 10, the thousands_sep is the empty string
        self.sep = locale.localeconv()['thousands_sep']

    def test_grouping(self):
        self._test_format("%f", 1024, grouping=1, out='1%s024.000000' % self.sep)
        self._test_format("%f", 102, grouping=1, out='102.000000')
        self._test_format("%f", -42, grouping=1, out='-42.000000')
        self._test_format("%+f", -42, grouping=1, out='-42.000000')

    def test_grouping_and_padding(self):
        self._test_format("%20.f", -42, grouping=1, out='-42'.rjust(20))
        self._test_format("%+10.f", -4200, grouping=1,
            out=('-4%s200' % self.sep).rjust(10))
        self._test_format("%-10.f", -4200, grouping=1,
            out=('-4%s200' % self.sep).ljust(10))

    def test_integer_grouping(self):
        self._test_format("%d", 4200, grouping=True, out='4%s200' % self.sep)
        self._test_format("%+d", 4200, grouping=True, out='+4%s200' % self.sep)
        self._test_format("%+d", -4200, grouping=True, out='-4%s200' % self.sep)

    def test_simple(self):
        self._test_format("%f", 1024, grouping=0, out='1024.000000')
        self._test_format("%f", 102, grouping=0, out='102.000000')
        self._test_format("%f", -42, grouping=0, out='-42.000000')
        self._test_format("%+f", -42, grouping=0, out='-42.000000')

    def test_padding(self):
        self._test_format("%20.f", -42, grouping=0, out='-42'.rjust(20))
        self._test_format("%+10.f", -4200, grouping=0, out='-4200'.rjust(10))
        self._test_format("%-10.f", 4200, grouping=0, out='4200'.ljust(10))

    def test_complex_formatting(self):
        # Spaces in formatting string
        self._test_format_string("One million is %i", 1000000, grouping=1,
            out='One million is 1%s000%s000' % (self.sep, self.sep))
        self._test_format_string("One  million is %i", 1000000, grouping=1,
            out='One  million is 1%s000%s000' % (self.sep, self.sep))
        # Dots in formatting string
        self._test_format_string(".%f.", 1000.0, out='.1000.000000.')
        # Padding
        self._test_format_string("-->  %10.2f", 4200, grouping=1,
            out='-->  ' + ('4%s200.00' % self.sep).rjust(10))
        # Asterisk formats
        self._test_format_string("%10.*f", (2, 1000), grouping=0,
            out='1000.00'.rjust(10))
        self._test_format_string("%*.*f", (10, 2, 1000), grouping=1,
            out=('1%s000.00' % self.sep).rjust(10))
        # Test more-in-one
        self._test_format_string("int %i float %.2f str %s",
            (1000, 1000.0, 'str'), grouping=1,
            out='int 1%s000 float 1%s000.00 str str' % (self.sep, self.sep))


class TestNumberFormatting(BaseLocalizedTest, EnUSNumberFormatting):
    # Test number formatting with a real English locale.

    locale_type = locale.LC_NUMERIC

    def setUp(self):
        BaseLocalizedTest.setUp(self)
        EnUSNumberFormatting.setUp(self)


class TestEnUSNumberFormatting(EnUSCookedTest, EnUSNumberFormatting):
    # Test number formatting with a cooked "en_US" locale.

    def setUp(self):
        EnUSCookedTest.setUp(self)
        EnUSNumberFormatting.setUp(self)

    def test_currency(self):
        self._test_currency(50000, "$50000.00")
        self._test_currency(50000, "$50,000.00", grouping=True)
        self._test_currency(50000, "USD 50,000.00",
            grouping=True, international=True)


class TestCNumberFormatting(CCookedTest, BaseFormattingTest):
    # Test number formatting with a cooked "C" locale.

    def test_grouping(self):
        self._test_format("%.2f", 12345.67, grouping=True, out='12345.67')

    def test_grouping_and_padding(self):
        self._test_format("%9.2f", 12345.67, grouping=True, out=' 12345.67')


class TestMiscellaneous(unittest.TestCase):
    def test_getpreferredencoding(self):
        # Invoke getpreferredencoding to make sure it does not cause exceptions.
        enc = locale.getpreferredencoding()
        if enc:
            # If encoding non-empty, make sure it is valid
            codecs.lookup(enc)

    if hasattr(locale, "strcoll"):
        def test_strcoll_3303(self):
            # test crasher from bug #3303
            self.assertRaises(TypeError, locale.strcoll, "a", None)
            self.assertRaises(TypeError, locale.strcoll, b"a", None)


def test_main():
    run_unittest(__name__)

if __name__ == '__main__':
    test_main()
