import itertools
import sys

def fname():
    return sys._getframe(1).f_code.co_name

#Let store here the points of the results with custom confs
class Points:
    points = set()

#Lets use this to create the analisis functions to compare the data
class Compa:

    analysis = []
    data = []
    size = set()

    class Empty: pass

    class InfiniteSet(object):

        def __and__(self, item):
            return item

        def __rand__(self,item):
            return item

    def __init__(self, size = set()):
        self.size = size

    def _left(self,  params, req):
        if params in self.analysis:
            actual = set(self.analisis[params].points.keys())
            return actual - req
        return req

    def load(self, list):
        ret = []
        for i in list:
            try:
                ret.append(Compa.data.index(i))
            except ValueError:
                Compa.data.append(self.to_bytes(i))
                ret.append(len(Compa.data) - 1)
        ret.sort()
        return ret

    def exist_analysis(self, type, params, mlen = -1, size = -1):
        if size == -1:
            return self._exist_analysis(type, params)
        else:
            return self._exist_analysis_size(type, params, mlen, size)

    def _exist_analysis_size(self, type, params, mlen, size):
        for i in range(len(self.analysis)):
            if self.analysis[i].params == params and self.analysis[i].type == type:
                if size == self.analysis[i].size or self.analysis[i].size == set():
                    return True, i
                else:
                    if size == set():
                        size = set(range(1, self.min_len(mlen) + 1)) - self.analysis[i].size
                    else: 
                        size = size - self.analysis[i].size
        return False, size

    def _exist_analysis(self, type, params):
        for i in range(len(self.analysis)):
            if self.analysis[i].params == params and self.analysis[i].type == type:
                return True, i
        return False, 0

    def equal(self, list, size = None):
        if size == None: size = self.size
        status, size = self.exist_analysis(fname(), [list], list, size)
        if status: return size
        tmp = self.Empty()
        tmp.params = [list]
        tmp.size = size
        tmp.type = fname()
        tmp.data = {}
        trabel = size if size else range(1, self.min_len(list)+1) 
        for i in trabel:
            tmp2 = self._equal(list, i)
            if tmp2: tmp.data.update({i: tmp2})
        self.analysis.append(tmp)
        return len(self.analysis) - 1

    def _equal(self, list, size):
        r = set()
        l = self.min_len(list)
        for i in range(l-size+1):
            e = True
            for j in range(len(list)-1):
                for k in range(j + 1, len(list)):
                    if self.data[list[j]][i:i+size] != \
                       self.data[list[k]][i:i+size]:
                        e = False
                        break
            if e:
                r.add(i)
        return r

    def uniq(self, list, size = None):
        if size == None: size = self.size
        status, size = self.exist_analysis(fname(), [list], list, size)
        if status: return size
        tmp = self.Empty()
        tmp.params = [list]
        tmp.size = size
        tmp.type = fname()
        tmp.data = {}
        trabel = size if size else range(1, self.min_len(list)+1) 
        for i in trabel:
            tmp2 = self._uniq(list, i)
            if tmp2: tmp.data.update({i: tmp2})
        Compa.analysis.append(tmp)
        return len(self.analysis) - 1

    def _uniq(self, list, size):
        r = set()
        l = self.min_len(list)
        for i in range(l-size+1):
            e = True
            for j in range(len(list)-1):
                for k in range(j + 1, len(list)):
                    if self.data[list[j]][i:i+size] == \
                       self.data[list[k]][i:i+size]:
                        e = False
                        break
            if e:
                r.add(i)
        return r

    def a_in_b(self, list1, list2, size = None):
        if size == None: size = self.size
        status, size = self.exist_analysis(fname(), [list1, list2], list1 + list2, size)
        if status: return size
        tmp = self.Empty()
        tmp.params = [list1, list2]
        tmp.size = size
        tmp.type = fname()
        tmp.data = {}
        zero = []
        for i in list2:
            zero.append(self._a_in_b(list1[0], i, size, fname()))
        zero = self.analysis[self.union(zero)].data.copy()
        print(zero)
        t = zero.keys()
        for i in t:
            _p = set(zero[i])
            for p in _p:
                for j in range(1, len(list1)):
                    r = True
                    for q in range(len(list2)):
                        if Compa.data[list1[j]][p[0]:p[0]+i] == Compa.data[list2[q]][p[1]:p[1]+i]:
                            r = False
                    if r:
                        zero[i].remove(p)
                        break
        tmp.data = self.clear(zero)
        Compa.analysis.append(tmp)
        return len(self.analysis) - 1

    def _a_in_b(self, val1, val2, size = None, fn = None):
        if not fn: fn = fname()
        if size == None: size = self.size
        status, size = self.exist_analysis(fn, [[val1], [val2]], [val1, val2], size)
        if status: return size
        tmp = self.Empty()
        tmp.params = [[val1], [val2]]
        tmp.size = size
        tmp.type = fn
        tmp.data = {}
        trabel = size if size else range(1, self.min_len([val1, val2])+1) 
        for i in trabel:
            tmp2 = self.__a_in_b(val1, val2, i)
            if tmp2: tmp.data.update({i: tmp2})
        Compa.analysis.append(tmp)
        return len(self.analysis) - 1

    def __a_in_b(self, val1, val2, size):
        r = set()
        for i in range(len(Compa.data[val1])-size+1):
            for j in range(len(Compa.data[val2])-size+1):
                if Compa.data[val1][i:i+size] == \
                   Compa.data[val2][j:j+size]:
                    r.add((i, j))
        return r

    def intersect(self, list):
        status, size = self.exist_analysis(fname(), list)
        if status: return size
        tmp = self.Empty()
        tmp.params = [list]
        tmp.type = fname()
        tmp.data = {}
        data = []
        for i in list:
            data.append(self.analysis[i].data)
        tmp.data = self._intersect(data)
        Compa.analysis.append(tmp)
        return len(self.analysis) - 1

    def _intersect(self, list):
        ret = {}
        r = list[0].keys()
        for i in range(1, len(list)):
            r = r & list[i].keys()
        for i in r:
            for j in list:
                if i in j.keys():
                    ret.update({i: j[i]})
                    break
        for i in r:
            for j in list:
                if i in j.keys():
                    ret.update({i: ret[i] & j[i]})
        return self.clear(ret)

    def union(self, list):
        status, size = self.exist_analysis(fname(), list)
        if status: return size
        tmp = self.Empty()
        tmp.params = [list]
        tmp.type = fname()
        tmp.data = {}
        data = []
        for i in list:
            data.append(self.analysis[i].data)
        tmp.data = self._union(data)
        Compa.analysis.append(tmp)
        return len(self.analysis) - 1

    def _union(self, list):
        ret = {}
        r = set()
        for i in list:
            r = r | i.keys()
        for i in r:
            for j in list:
                if i in j.keys():
                    if i in ret.keys():
                        ret.update({i: ret[i] | j[i]})
                    else:
                        ret.update({i: j[i]})
        return ret

    def permute(self, list, fin, fout):
        l = []
        for i in list:
            l.append(range(len(i)))
        g = []
        for i in itertools.product(*l):
            s = []
            for j in range(len(i)):
                s.append(list[j][i[j]])
            g.append(fin(s))
        r = fout(g)
        return r

    def clear(self, val):
        for j in val.keys():
            if len(val[j]) == 0:
                del val[j]
                return self.clear(val)
        return val

    def min_len(self, list):
        if len(list) == 0: return 0
        m = len(Compa.data[list[0]])
        for i in range(1, len(list)):
            m = min(m, len(Compa.data[list[i]]))
        return m

a = Compa()
r = a.load(["hola", "colo", "jamo"])
a.uniq(r)


