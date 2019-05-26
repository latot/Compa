##Just some vars to play while debugging

from Compa2 import Compa
from Points import Data, Points

a = Compa({1, 2, 3, 4})
r = Data.load(["holo", "colo", "jamo"])
j=a.uniq(r)

s = Data.load([b"o"])
y=a.a_in_b(s, r)

P1 = Points({2: {1, 2, 3}})
P2 = Points({2: {2, 3, 4}})
Pi = Points({2: {2, 3}})
Pu = Points({2: {1, 2, 3, 4}})
