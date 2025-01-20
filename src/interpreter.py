import elog_nodes, elog_els

class elog_interpreter(object):

  def __init__(self, nodes : list[elog_nodes.node]) -> None:
    
    self.nodes : list[elog_nodes.node] = nodes
    self.ids : dict[str, list[elog_els.id]] = dict()
    self.vls : list[elog_els.val] = list()
    self.idc : list[dict[str, int]] = list()
    self.lns = 0


  def gowrong(self, error : str = 'unknown') -> None:

    raise Exception(f'\n\n[Interpreting error!]\nMsg: {error}\nAt : {self.lns}th line (of content).\n\n')


  def getval(self, e : elog_els.el) -> elog_els.val:
    
    if isinstance(e, elog_els.id): e = self.vls[e.idx]

    if isinstance(e, elog_els.val): return e
    else: self.gowrong('Value can not be fetched. / Value does not have a value.')


  def itp_uop(self, n : elog_nodes.unop) -> elog_els.el:

    if n.o == 'RETURN':
        print(self.getval(self.itp_node(n.v)))

    else: self.gowrong('Uninterpretable binary operation.')


  def itp_bop(self, n : elog_nodes.binop) -> elog_els.el:

    if n.o == 'LETIN':
      if isinstance(n.l, elog_nodes.val) and n.l.t == 'ID':
        self.idc[-1][n.l.v] = self.idc[-1].get(n.l.v, 0) + 1
        self.vls.append(elog_els.val('UNDEFINED', 0))
        if n.l.v not in self.ids.keys(): self.ids[n.l.v] = list()
        self.ids[n.l.v].append(elog_els.id(n.l.v, len(self.vls) - 1, n.r, lambda : True))

      else: self.gowrong('Let left operand is not an ID.')

    else: self.gowrong('Uninterpretable binary operation.')


  def itp_top(self, n : elog_nodes.triop) -> elog_els.el:

    ...


  def itp_set(self, n : elog_nodes.setof) -> elog_els.el:

    ...


  def itp_val(self, n : elog_nodes.val) -> elog_els.el:

    if n.t == 'ID':
      r = self.ids[n.v][-1]
    else:
      r = elog_els.val('', 0)

      if n.t == 'NUM':
        r.t = 'num:integer'
        r.v = int(n.v)
      elif n.t == 'FNUM':
        v.t = 'num:floating'
        v.v = float(n.v)
      elif n.t == 'TEXT':
        v.t = 'text:string'
        v.v = str(n.v)
      else: self.gowrong('Uninterpretable value type.')

    return r


  def itp_node(self, n : elog_nodes.node) -> elog_els.el:

    if isinstance(n, elog_nodes.unop): return self.itp_uop(n)
    elif isinstance(n, elog_nodes.binop): return self.itp_bop(n)
    elif isinstance(n, elog_nodes.triop): return self.itp_top(n)
    elif isinstance(n, elog_nodes.setof): return self.itp_set(n)
    elif isinstance(n, elog_nodes.val): return self.itp_val(n)
    else: self.gowrong('Uninterpretable node type.')


  def itp_all(self) -> None:

    self.idc.append(dict())

    for l in self.nodes:
        self.itp_node(l)
        self.lns += 1


