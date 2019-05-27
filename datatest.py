##Just some vars to play while debugging

from Compa2 import Compa
from Points import Data, Points

#import pdb;pdb.set_trace()

a = Compa({1, 2, 3, 4})
r = Data.load(["holo", "colo", "jamo"])

#pdb.run("a.uniq(r)")
#pdb.run("j == Points({1: {0}, 2: {0}, 3: {0}, 4: {0}})")


a = Compa({1, 2, 3, 4})
r = Data.load(["holo", "colo", "jamo"])
j=a.uniq(r)

s = Data.load([b"o"])
y=a.a_in_some_b(s, r)

P1 = Points({2: {1, 2, 3}})
P2 = Points({2: {2, 3, 4}})
Pi = Points({2: {2, 3}})
Pu = Points({2: {1, 2, 3, 4}})
