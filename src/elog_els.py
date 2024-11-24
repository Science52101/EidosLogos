class el: pass

class val(el):
    def __init__(self, t, v):
        self.t = t
        self.v = v

class id(el):
    def __init__(self, idf, idx, t, c):
        self.idf = idf
        self.idx = idx
        self.t = t
        self.c = c


