import itertools
import sys
from Points import Points, Analysis, Data, SubData
import Utils

import inspect

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

    def a_in_some_b(self, val, list, size = None):
        if size == None: size = self.size
        params = (fname(), tuple([val]), list.hash())
        lsize = self._left(params, size)
        if len(lsize) == 0: return self._request(params, size)
        t = Infinite()
        for i in list.data:
            t = t & self._a_in_some_b(val.data[0], i, lsize, fname())
        self.analysis.add(params, t)
        return t

    def _a_in_some_b(self, val1, val2, size = None, fn = None):
        if not fn: fn = fname()
        if size == None: size = self.size
        params = (fname(), tuple([val1]), tuple([val2]))
        lsize = self._left(params, size)
        if len(lsize) == 0: return self._request(params, size)
        r = Points()
        for i in lsize:
                r.add(i, self.__a_in_some_b(val1, val2, i))
        self.analysis.add(params, r)
        return r

    def __a_in_some_b(self, val1, val2, size):
        r = set()
        for i in range(len(Data.data[val1])-size+1):
            for j in range(len(Data.data[val2])-size+1):
                if Data.data[val1][i:i+size] == \
                   Data.data[val2][j:j+size]:
                    r.add((i, j))
        return r

    def permute(self, connect, struct, keys, sdata):
        r = Inffinite()
        for i in itertools.product(*sdata):
            tstruct = struct
            for j in range(len(keys)):
                tstruct.replace(keys[j], "Data.data[{}]".format(i[j]))
            t = eval(tstruct)
            r = eval("r {} t".format(connect, t))
        return r

    def clear(self, val):
        for j in val.keys():
            if len(val[j]) == 0:
                del val[j]
                return self.clear(val)
        return val
