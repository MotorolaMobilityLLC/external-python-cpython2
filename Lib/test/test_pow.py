import test.test_support, unittest

class PowTest(unittest.TestCase):

    def powtest(self, type):
        if type != float:
            for i in range(-1000, 1000):
                self.assertEquals(pow(type(i), 0), 1)
                self.assertEquals(pow(type(i), 1), type(i))
                self.assertEquals(pow(type(0), 1), type(0))
                self.assertEquals(pow(type(1), 1), type(1))

            for i in range(-100, 100):
                self.assertEquals(pow(type(i), 3), i*i*i)

            pow2 = 1
            for i in range(0,31):
                self.assertEquals(pow(2, i), pow2)
                if i != 30 : pow2 = pow2*2

            for othertype in int, long:
                for i in range(-10, 0) + range(1, 10):
                    ii = type(i)
                    for j in range(1, 11):
                        jj = -othertype(j)
                        pow(ii, jj)

        for othertype in int, long, float:
            for i in range(1, 100):
                zero = type(0)
                exp = -othertype(i/10.0)
                if exp == 0:
                    continue
                self.assertRaises(ZeroDivisionError, pow, zero, exp)

        il, ih = -20, 20
        jl, jh = -5,   5
        kl, kh = -10, 10
        asseq = self.assertEqual
        if type == float:
            il = 1
            asseq = self.assertAlmostEqual
        elif type == int:
            jl = 0
        elif type == long:
            jl, jh = 0, 15
        for i in range(il, ih+1):
            for j in range(jl, jh+1):
                for k in range(kl, kh+1):
                    if k != 0:
                        if type == float or j < 0:
                            self.assertRaises(TypeError, pow, type(i), j, k)
                            continue
                        asseq(
                            pow(type(i),j,k),
                            pow(type(i),j)% type(k)
                        )

    def test_powint(self):
        self.powtest(int)

    def test_powlong(self):
        self.powtest(long)

    def test_powfloat(self):
        self.powtest(float)

    def test_other(self):
        # Other tests-- not very systematic
        self.assertEquals(pow(3,3) % 8, pow(3,3,8))
        self.assertEquals(pow(3,3) % -8, pow(3,3,-8))
        self.assertEquals(pow(3,2) % -2, pow(3,2,-2))
        self.assertEquals(pow(-3,3) % 8, pow(-3,3,8))
        self.assertEquals(pow(-3,3) % -8, pow(-3,3,-8))
        self.assertEquals(pow(5,2) % -8, pow(5,2,-8))

        self.assertEquals(pow(3L,3L) % 8, pow(3L,3L,8))
        self.assertEquals(pow(3L,3L) % -8, pow(3L,3L,-8))
        self.assertEquals(pow(3L,2) % -2, pow(3L,2,-2))
        self.assertEquals(pow(-3L,3L) % 8, pow(-3L,3L,8))
        self.assertEquals(pow(-3L,3L) % -8, pow(-3L,3L,-8))
        self.assertEquals(pow(5L,2) % -8, pow(5L,2,-8))

        for i in range(-10, 11):
            for j in range(0, 6):
                for k in range(-7, 11):
                    if j >= 0 and k != 0:
                        self.assertEquals(
                            pow(i,j) % k,
                            pow(i,j,k)
                        )
                    if j >= 0 and k != 0:
                        self.assertEquals(
                            pow(long(i),j) % k,
                            pow(long(i),j,k)
                        )

    def test_bug643260(self):
        class TestRpow:
            def __rpow__(self, other):
                return None
        None ** TestRpow() # Won't fail when __rpow__ invoked.  SF bug #643260.


def test_main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PowTest))
    test.test_support.run_suite(suite)

if __name__ == "__main__":
    test_main()
