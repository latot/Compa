import itertools
import sys
from Points import Points, Analysis, Data, SubData
import Utils

def fname():
    return sys._getframe(1).f_code.co_name

class Infinite(object):

    def __and__(self, item):
        return item

    def __rand__(self,item):
        return item

#Lets use this to create the analisis functions to compare the data
class Compa:

    analysis = Analysis()
    data = []

    def __init__(self, size = set()):
        self.size = size

    def _left(self,  params, req):
        if params in self.analysis.data.keys():
            actual = set(self.analysis[params].points.keys())
            return actual - req
        return req

    def _request(self, params, req):
        r = Points()
        for i in list(req): ## Fix latter, travel set
            r.add(self.analysis[params].points[i])
        return r

    def equal(self, list, size = None):
        if size == None: size = self.size
        params = (fname(), list.hash())
        lsize = self._left(params, size)
        if len(lsize) == 0: return self._request(params, size)
        r = Points()
        for i in lsize:
            r.add(i, self._equal(list, i))
        self.analysis.add(params, r)
        return r

    def _equal(self, list, size):
        r = set()
        l = list.min_len
        for i in range(l-size+1):
            e = True
            for j in range(list.len() -1):
                for k in range(j + 1, list.len()):
                    if list.read(j)[i:i+size] != \
                       list.read(k)[i:i+size]:
                        e = False
                        break
            if e:
                r.add(i)
        return r

    def uniq(self, list, size = None):
        if size == None: size = self.size
        params = (fname(), list.hash())
        lsize = self._left(params, size)
        if len(lsize) == 0: return self._request(params, size)
        r = Points()
        for i in lsize:
            r.add(i, self._uniq(list, i))
        self.analysis.add(params, r)
        return r

    def _uniq(self, list, size):
        r = set()
        l = list.min_len
        for i in range(l-size+1):
            e = True
            for j in range(list.len()-1):
                for k in range(j + 1, list.len()):
                    if list.read(j)[i:i+size] == \
                       list.read(k)[i:i+size]:
                        e = False
                        break
                if not e: break
            if e:
                r.add(i)
        return r

    def a_in_b(self, val1, val2, size = None):
        if size == None: size = self.size
        size = set(range(1, min(len(val1.read(0)), len(val2.read(0)))+1))
        params = (fname(), tuple([val1]), tuple([val2]))
        lsize = self._left(params, size)
        if len(lsize) == 0: return self._request(params, size)
        r = Points()
        for i in lsize:
            r.add(i, self._a_in_b(val1, val2, i))
        self.analysis.add(params, r)
        return r

    def _a_in_b(self, val1, val2, size):
        assert val1.len() == 1, "Wrong data size of val1"
        assert val2.len() == 1, "Wrong data size of val2"
        r = set()
        for i in range(len(val1.read(0))-size+1):
            for j in range(len(val2.read(0))-size+1):
                if val1.read(0)[i:i+size] == \
                   val2.read(0)[j:j+size]:
                    r.add((i, j))
        return r

    def permute(self, connect, struct, keys, cdata, size = None):
        r = []
        sdata = tuple()
        for i in range(len(cdata)):
            cdata[i] = tuple(cdata[i].data)
        if size == None: size = self.size
        params = (fname(), connect, struct, tuple(keys), tuple(cdata))
        lsize = self._left(params, size)
        if len(lsize) == 0: return self._request(params, size)
        for i in itertools.product(*cdata):
            tstruct = struct
            for j in range(len(keys)):
                tstruct = tstruct.replace(keys[j], "SubData([{}])".format(i[j]))
            r.append(eval(tstruct))
        if len(r) == 1: return r[0]
        t = r[0]
        for i in range(1, len(r)):
            t = eval("t {} r[{}]".format(connect, i))
        return t

    def clear(self, val):
        for j in val.keys():
            if len(val[j]) == 0:
                del val[j]
                return self.clear(val)
        return val
