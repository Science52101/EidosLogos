import elog_nodes

class el:
    def __init__(self) -> None: pass
    def __repr__(self) -> str: pass

class val(el):
    def __init__(self, t, v):
        self.t = t
        self.v = v
    def __repr__(self) -> str:
        return f'[{self.t}]: {self.v}'

class id(el):
    def __init__(self, idf, idx, t, c):
        self.idf = idf
        self.idx = idx
        self.t = t
        self.c = c
    def __repr__(self) -> str:
        return f'[{self.idf} : {self.t}]: {self.idx} - {self.c}'
        
class v_function(el):
    def __init__(self, i : list[str], n : elog_nodes.node):
        self.i = i
        self.n = n
    def __repr__(self) -> str:
        return f'[function]: {self.i} -> {self.n}'
