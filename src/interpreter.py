import elog_nodes, elog_els

class elog_interpreter(object):

  def __init__(self, nodes : list[elog_nodes.node]) -> None:
    
    self.nodes : list[elog_nodes.node] = nodes
    self.ids : dict[str, list[elog_els.id]] = dict()
    self.vls : list[elog_els.val] = list()
    self.idc : list[dict[str, int]] = [dict()]
    self.rls : list[list[elog_els.el]] = [list()]
    self.lns = 1


  def gowrong(self, error : str = 'unknown') -> None:

    raise Exception(f'\n\n[Interpreting error!]\nMsg: {error}\nAt : {self.lns}th line (of content).\n\n')


  def getval(self, e : elog_els.el) -> elog_els.val:
    
    if isinstance(e, elog_els.id):
      if e.idx < len(self.vls): e = self.vls[e.idx]
      else: self.gowrong('Index of ID is not existant yet.')

    if isinstance(e, elog_els.val): return e
    else: self.gowrong('Value can not be fetched. / Value does not have a value.')


  def itp_uop(self, n : elog_nodes.unop) -> elog_els.el:

    if n.o == 'RETURN':
      l = elog_els.val('err:NULL', 0)
      r = self.getval(self.itp_node(n.v))
      l.t = r.t
      l.v = r.v ##########################################################################################################################################################
      self.rls[-1].append(l)

    elif n.o == 'ADD':
      l = self.getval(self.itp_node(n.v))
      if l.t.split(':')[0] == 'num':
        return l

      else: self.gowrong(f'Unary addition operand is not a number. Operand: {l}')

    elif n.o == 'SUB':
      l = self.getval(self.itp_node(n.v))
      if l.t.split(':')[0] == 'num':
        l.v = -l.v
        return l

      else: self.gowrong(f'Unary subtraction operand is not a number. Operand: {l}')

    elif n.o == 'ITP':
      l = self.getval(self.itp_node(n.v))

      if l.t == 'node:block':
        self.idc.append(dict())
        self.rls.append(list())

        self.itp_lines(l.v)

        for idck, idcv in self.idc[-1].items():
          for i in range(idcv): self.ids[idck].pop()

        l = elog_els.val('collection:vector', self.rls[-1])

        self.idc.pop()
        self.rls.pop()

        return l

      else: self.gowrong(f'Interpretation operand is not a block. Operand: {l}')



    else: self.gowrong(f'Uninterpretable unary operation. Operation: {n.o}')


  def itp_bop(self, n : elog_nodes.binop) -> elog_els.el:

    if n.o == 'LETIN':
      if isinstance(n.l, elog_nodes.val) and n.l.t == 'ID':
        self.idc[-1][n.l.v] = self.idc[-1].get(n.l.v, 0) + 1
        self.vls.append(elog_els.val('err:UNSETTED', 0))

        if n.l.v not in self.ids.keys(): self.ids[n.l.v] = list()
        self.ids[n.l.v].append(elog_els.id(n.l.v, len(self.vls) - 1, n.r, True))

      else: self.gowrong(f'Let left operand is not a tokenized ID. Left operand token: {n.l}')

    elif n.o == 'DEF':
      l = self.itp_node(n.l)
      if isinstance(l, elog_els.id):
        r = self.getval(self.itp_node(n.r))
        if l.idx < len(self.vls):
          self.vls[l.idx].t = r.t
          self.vls[l.idx].v = r.v ##########################################################################################################################################################
        else: self.gowrong('Index of the setting ID is not existant yet.')

        return elog_els.val('err:NULL', 0)

      else: self.gowrong('Setting left operand is not an ID.')

    elif n.o == 'ADD':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == 'num' and r.t.split(':')[0] == 'num':
        l.v += r.v
        if r.t.split(':')[1] == 'floating': l.t = r.t
        return l

      else: self.gowrong(f'Addition operand(s) is/are not (a) number(s). Operands: {l}, {r}')

    elif n.o == 'MUL':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == 'num' and r.t.split(':')[0] == 'num':
        l.v *= r.v
        if r.t.split(':')[1] == 'floating': l.t = r.t
        return l

      else: self.gowrong(f'Multiplication operand(s) is/are not (a) number(s). Operands: {l}, {r}')

    elif n.o == 'DIV':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == 'num' and r.t.split(':')[0] == 'num':
        l.v /= float(r.v)
        l.t = 'num:floating'
        return l

    elif n.o == 'POW':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == 'num' and r.t.split(':')[0] == 'num':
        l.v **= r.v
        if r.t.split(':')[1] == 'floating': l.t = r.t
        return l

      else: self.gowrong(f'Multiplication operand(s) is/are not (a) number(s). Operands: {l}, {r}')

    else: self.gowrong(f'Uninterpretable binary operation. Operation: {n.o}')


  def itp_top(self, n : elog_nodes.triop) -> elog_els.el:

    ...


  def itp_set(self, n : elog_nodes.setof) -> elog_els.el:

    if n.t == 'BLOCK':
      return elog_els.val('node:block', n.s)


  def itp_val(self, n : elog_nodes.val) -> elog_els.el:

    if n.t == 'ID':
      if n.v in self.ids.keys(): r = self.ids[n.v][-1]
      else: self.gowrong('ID is not defined.')
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
        r.v = str(n.v)[1:-1]
      else: self.gowrong('Uninterpretable value type.')

    return r


  def itp_node(self, n : elog_nodes.node) -> elog_els.el:

    if isinstance(n, elog_nodes.unop): return self.itp_uop(n)
    elif isinstance(n, elog_nodes.binop): return self.itp_bop(n)
    elif isinstance(n, elog_nodes.triop): return self.itp_top(n)
    elif isinstance(n, elog_nodes.setof): return self.itp_set(n)
    elif isinstance(n, elog_nodes.val): return self.itp_val(n)
    else: self.gowrong('Uninterpretable node type.')


  def itp_lines(self, nl : list[elog_nodes.node], cln : bool = False) -> elog_els.el:

    for l in nl:
        self.itp_node(l)
        if cln: self.lns += 1


  def itp_all(self) -> None:

    self.itp_lines(self.nodes)

    for rl in self.rls[0]:
      print(rl)


