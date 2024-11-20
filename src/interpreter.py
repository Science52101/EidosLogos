from parser import *

class elog_els:

    class el: pass

    class val(el):
        def __init__(self, t, c, v):
            self.t = t
            self.c = c
            self.v = v

    class id(el):
        def __init__(self, idf, idx):
            self.idf = idf
            self.idx = idx


class elog_interpreter:

    def __init__(self, nodes : list[elog_nodes.node]) -> None:
        
        self.nodes : list[elog_nodes.node] = nodes

        self.ids : list[elog_els.id] = list()

        self.vls : list[elog_els.val] = list()


    def itp_lin(self) -> elog_els.el:

        ...


    def itp_all(self) -> None:

        ...


