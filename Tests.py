import unittest2 as unittest
from Compa2 import Compa
from Points import Data, Points

class TestPoints(unittest.TestCase):

    P1 = Points({2: {1, 2, 3}, 3: {0, 1, 2}})
    P2 = Points({2: {2, 3, 4}, 4: {0, 1, 2}})

    def test_intersect(self):
        Pi = Points({2: {2, 3}})
        self.assertEqual(self.P1 & self.P2, Pi)
        self.assertEqual(self.P2 & self.P1, Pi)

    def test_union(self):
        Pu = Points({2: {1, 2, 3, 4}, 3: {0, 1, 2}, 4: {0, 1, 2}})
        self.assertEqual(self.P1 | self.P2, Pu)
        self.assertEqual(self.P2 | self.P1, Pu)

class TestCompa(unittest.TestCase):

    a = Compa({1, 2, 3, 4})
    r = Data.load(["holo", "colo", "jamo"])

    def test_uniq(self):
        j=self.a.uniq(self.r)
        self.assertEqual(j, Points({1: {0}, 2: {0}, 3: {0}, 4: {0}}))

    def test_equal(self):
        j=self.a.equal(self.r)
        self.assertEqual(j, Points({1: {3}}))

    def test_a_in_b(self):
        pass

if __name__ == "__main__":
    unittest.main()
