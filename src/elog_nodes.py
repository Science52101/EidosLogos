from functools import reduce

class node:
    def __init__(self) -> None: pass
    def __repr__(self) -> str: pass

class val(node):
    def __init__(self, t, v):
        self.t = t
        self.v = v
    def __repr__(self) -> str:
        return f'( {self.t} {self.v} )'

class unop(node):
    def __init__(self, o, v):
        self.o = o
        self.v = v
    def __repr__(self) -> str:
        return f'[ {self.o} {self.v} ]'

class binop(node):
    def __init__(self, l, o, r):
        self.l = l
        self.o = o
        self.r = r
    def __repr__(self) -> str:
        return f'[ {self.l} {self.o} {self.r} ]'

class triop(node):
    def __init__(self, o, f, s, t):
        self.o = o
        self.f = f
        self.s = s
        self.t = t
    def __repr__(self) -> str:
        return f'[ {self.o} {self.f} {self.s} {self.t} ]'

class setof(node):
    def __init__(self, t, n):
        if isinstance(n, list): self.s = n
        else: self.s = [n]
        self.t = t
    def add(self, n):
        self.s.append(n)
    def __repr__(self) -> str:
        return '{'+f' {self.t} : '+str(self.s)[1:-1]+' }'


