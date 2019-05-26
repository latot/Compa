import unittest2 as unittest
from Compa2 import Compa
from Points import Data, Points

class TestPoints(unittest.TestCase):

    def test_intersect(self):
        P1 = Points({2: {1, 2, 3}})
        P2 = Points({2: {2, 3, 4}})
        Pi = Points({2: {2, 3}})
        self.assertEqual(P1 & P2, Pi)
        self.assertEqual(P2 & P1, Pi)

    def test_union(self):
        P1 = Points({2: {1, 2, 3}})
        P2 = Points({2: {2, 3, 4}})
        Pu = Points({2: {1, 2, 3, 4}})
        self.assertEqual(P1 | P2, Pu)
        self.assertEqual(P2 | P1, Pu)

if __name__ == "__main__":
    unittest.main()
