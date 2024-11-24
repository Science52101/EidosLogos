import elog_nodes, elog_els

from interpreter import unops, binops, triops, vals, sets


class elog_interpreter:

    def __init__(self, nodes : list[elog_nodes.node]) -> None:
        
        self.nodes : list[elog_nodes.node] = nodes

        self.ids : list[elog_els.id] = list()

        self.vls : list[elog_els.val] = list()


    def gowrong(self) -> None:

        raise Exception('\n\n'+
                        'The logic is wrong with that.'+
                        '\n\n')


    def itp_uop(self, n : elog_nodes.unop) -> elog_els.el:

        ...


    def itp_bop(self, n : elog_nodes.binop) -> elog_els.el:

        ...


    def itp_top(self, n : elog_nodes.triop) -> elog_els.el:

        ...


    def itp_set(self, n : elog_nodes.setof) -> elog_els.el:

        ...


    def itp_val(self, n : elog_nodes.val) -> elog_els.el:

        ...


    def itp_node(self, n : elog_nodes.node) -> elog_els.el:

        if isinstance(n, elog_nodes.unop): return self.itp_uop(n)

        elif isinstance(n, elog_nodes.binop): return self.itp_bop(n)

        elif isinstance(n, elog_nodes.triop): return self.itp_top(n)

        elif isinstance(n, elog_nodes.setof): return self.itp_set(n)

        elif isinstance(n, elog_nodes.val): return self.itp_val(n)

        else: self.gowrong()


    def itp_all(self) -> None:

        for l in nodes: self.itp_node(l)


