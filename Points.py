import Utils

import inspect

class Analysis:

    def __init__(self):
        self.data = dict()

    def add(self, params, value):
        if params in self.data.keys():
            self.data[params] = self.data[params] | value
            return
        self.data[params] = value

    def remove(self, params):
        del self.data[params]

    def contain(self, param):
        if param in self.data.keys():
            return True
        return False

    def __contain__(self, param):
        return self.contain(param)

class SubData:

    def __init__(self, list):

        self.data = list
        self.calc_min_len()

    def calc_min_len (self):
        if len(self.data) == 0: return 0
        m = len(Data.data[self.data[0]])
        for i in range(1, len(self.data)):
            m = min(m, len(Data.data[self.data[i]]))
        self.min_len = m

    def hash(self):
        return tuple(self.data)

    def len(self):
        return len(self.data)

    def read(self, val):
        return Data.data[val]

class Data:

    data = []

    def load(list):
        ret = []
        for i in list:
            try:
                ret.append(Data.data.index(i))
            except ValueError:
                ret.append(len(Data.data))
                Data.data.append(Utils.to_bytes(i))
        ret.sort()
        return SubData(ret)

class Points:

    def __init__(self, points = dict(), full_key = "all", _repr = "Points"):
        self.points = points.copy()
        self.full_key = full_key
        #This can be used for a lot o things, just put here the name for what we will use it"
        self._repr = _repr

    def load(self, data):
        assert isinstance(data, dict), "Wrong input data format"
        self.points = data

    def copy(self):
        t = Points()
        t.full_key = self.full_key
        t._repr = self._repr
        t.points = self.points.copy()

    def __repr__(self): return "{}: {}".format(self._repr, self.points)
#
#    def read_conf(self, conf):
#        assert isinstance(conf, dict), "Config need to be a dict"
#        sconf = ""
#        for i in sorted(conf.keys()):
#            assert ";" not in i, "the configuration can't use \";\" as key"
#            assert ";" not in conf[i], "the configuration can't use \";\" as value"
#            sconf += conf[i] + ";"
#        return sconf

    def add(self, conf, value):
        assert isinstance(value, set), "value is not a set"
#        assert isinstance(conf, str), "conf only support string values"
        if len(value) == 0: return
        if conf not in self.points.keys():
            self.points[conf] = value
            return
        self.points[conf]= value | self.points[conf]

    def equal(self, point):
        return self.points == point.points

    def __eq__(self, point):
        return self.equal(point)

    def remove(self, econf, value):
        conf = self.read_conf(econf)
        assert isinstance(value, set), "value is not a set"
#        assert isinstance(conf, str), "conf only support string values"
        if conf not in self.points.keys():
            return
        self.points[conf] = self.points[conf] - value
        # is this useful?, maybe just remove it
        if len(self.points(conf)) == 0:
            del self.points[conf]

    def union(self, point):
        assert isinstance(point, Points), "Wrong type, I need a Point type"
        npoints = dict()
        kpoint1 = set(self.points.keys())
        kpoint2 = set(point.points.keys())
        for i in (kpoint2 ^ kpoint1):
            if i in kpoint1:
                npoints[i] = self.points[i]
            if i in kpoint2:
                npoints[i] = point.points[i]
        for i in (kpoint2 & kpoint1):
            npoints[i] = self.points[i] | point.points[i]
        t = Points()
        t.points = npoints
        return t

    def __or__(self, point):
        return self.union(point)

    def intersect(self, point):
        assert isinstance(point, Points), "Wrong type, I need a Point type"
        npoints = dict()
        kpoint1 = set(self.points.keys())
        kpoint2 = set(point.points.keys())
        for i in (kpoint2 & kpoint1):
            npoints[i] = self.points[i] & point.points[i]
            # is this useful?, maybe just remove it
            if len(npoints[i]) == 0:
                del npoints[i]
        t = Points()
        t.points = npoints
        return t

    def __and__(self, point):
        return self.intersect(point)

    def difference(self, point):
        assert isinstance(point, Points), "Wrong type, I need a Point type"
        npoints = self.points.copy()
        kpoint1 = set(self.points.keys())
        kpoint2 = set(point.points.keys())
        for i in (kpoint2 & kpoint1):
            npoints[i] = self.point[i] - point.points[i]
            # is this useful?, maybe just remove it
            if len(npoints[i]) == 0:
                del npoints[i]
        t = Points()
        t.points = npoints
        return npoints

    def __sub__(self, point):
        return self.difference(point)

    def simmetric_difference(self, point):
        return (self | point) - (self & point)

    def __xor__(self, point):
        return self.simmentric_difference(point)
