import unittest
import idlelib.CallTips as ct
CTi = ct.CallTips()

class Test_get_entity(unittest.TestCase):
    # In 3.x, get_entity changed from 'instance method' to module function
    # since 'self' not used. Use dummy instance until change 2.7 also.
    def test_bad_entity(self):
        self.assertIsNone(CTi.get_entity('1/0'))
    def test_good_entity(self):
        self.assertIs(CTi.get_entity('int'), int)

if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
