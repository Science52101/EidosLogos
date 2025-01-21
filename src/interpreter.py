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
    
    if isinstance(e, elog_els.id):
      if e.idx in self.ids.keys(): e = self.vls[e.idx]
      else: self.gowrong('Index is not defined.')

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
        self.vls.append(elog_els.val('err:UNSETTED', 0))
        if n.l.v not in self.ids.keys(): self.ids[n.l.v] = list()
        self.ids[n.l.v].append(elog_els.id(n.l.v, len(self.vls) - 1, n.r, True))

      else: self.gowrong('Let left operand is not a tokenized ID.')

    elif n.o == 'DEF':
      l = self.itp_node(n.l)
      if isinstance(l, elog_els.id):
        r = self.itp_node(n.r)
        self.vls[l.idx].t = r.t
        self.vls[l.idx].v = r.v

        return elog_els.val('err:NULL', 0)

      else: self.gowrong('Setting left operand is not an ID.')

    elif n.o == 'ADD':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == 'num' and r.t.split(':')[0] == 'num':
        l.v += r.v
        if r.t.split(':')[1] == 'floating': l.t = r.t
        return l

      else: self.gowrong('Addition operand(s) is/are not (a) number(s).')

    elif n.o == 'MUL':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == 'num' and r.t.split(':')[0] == 'num':
        l.v *= r.v
        if r.t.split(':')[1] == 'floating': l.t = r.t
        return l

      else: self.gowrong('Multiplication operand(s) is/are not (a) number(s).')

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
        r.t = 'num:floating'
        r.v = float(n.v)
      elif n.t == 'TEXT':
        r.t = 'text:string'
        r.v = str(n.v)
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


