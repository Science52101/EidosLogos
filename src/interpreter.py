from copy import deepcopy

import elog_nodes, elog_els
from elog_params import *

class elog_interpreter(object):

  TYNAMES : dict[str, str] = {
    'NUM': 'number',
      'INT': 'integer',
      'FLT': 'floating',
    'TXT': 'text',
      'STR': 'string', 
    'BOO': 'boolean',
    'LNK': 'link',
      'REF': 'reference',
    'COL': 'collection',
      'VEC': 'vector',
      'MTX': 'matrix',
    'NOD': 'node',
      'BLK': 'block',
    'ERR': 'error',
      'NUL': 'null',
      'UNS': 'unsetted', 
    'ANY': 'any'
  }

  TYNAMESL : dict[str, str] = {
    'NUM': 'numerus',
      'INT': 'integer',
      'FLT': 'fluctuans',
    'TXT': 'textus',
      'STR': 'catenarius', 
    'BOO': 'veritas',
    'LNK': 'necto',
      'REF': 'referentia',
    'COL': 'collectio',
      'VEC': 'vector',
      'MTX': 'matrix',
    'NOD': 'nodus',
      'BLK': 'moles',
    'ERR': 'error',
      'NUL': 'nihil',
      'UNS': 'indefinitus', 
    'ANY': 'quilibet'
  }

  def __init__(self, nodes : list[elog_nodes.node]) -> None:
    
    self.nodes : list[elog_nodes.node] = nodes
    self.ids : dict[str, list[elog_els.id]] = dict()
    self.vls : list[elog_els.val] = list()
    self.idc : list[dict[str, int]] = [dict()]
    self.rls : list[list[elog_els.el]] = [list()]
    self.lns = 1
    self.TYNA : dict[str, str] = self.TYNAMESL if elog_params.latin else self.TYNAMES


  def gowrong(self, error : str = 'unknown') -> None:

    raise Exception(f'\n\n[Interpreting error!]\nMsg: {error}\nAt : {self.lns}th line (of content).\n\n')


  def getval(self, e : elog_els.el) -> elog_els.val:
    
    if isinstance(e, elog_els.id):
      if isinstance(e, elog_els.id2i):
        e = e.get()
      else:
        if e.idx < len(self.vls): e = self.vls[e.idx]
        else: self.gowrong('Index of ID is not existant yet.')

    if isinstance(e, elog_els.val): return e
    else: self.gowrong('Value can not be fetched. / Value does not have a value.')


  def itp_uop(self, n : elog_nodes.unop) -> elog_els.el:

    if n.o == 'RETURN':
      l = elog_els.val(f'{self.TYNA["ERR"]}:{self.TYNA["NUL"]}', 0)
      r = self.getval(self.itp_node(n.v))
      l.t = r.t
      l.v = deepcopy(r.v)
      self.rls[-1].append(l)

    elif n.o == 'ADD':
      l = self.getval(self.itp_node(n.v))
      if l.t.split(':')[0] == self.TYNA["NUM"]:
        return elog_els.val(l.t, +l.v)

      else: self.gowrong(f'Unary addition operand is not a number. Operand: {l}')

    elif n.o == 'SUB':
      l = self.getval(self.itp_node(n.v))
      if l.t.split(':')[0] == self.TYNA["NUM"]:
        return elog_els.val(l.t, -l.v)

      else: self.gowrong(f'Unary subtraction operand is not a number. Operand: {l}')

    elif n.o == 'NOT':
      l = self.getval(self.itp_node(n.v))
      if l.t.split(':')[0] == self.TYNA["BOO"]:
        return elog_els.val(l.t, not l.v)

      else: self.gowrong(f'Negation operand is not a boolean. Operand: {l}')


    elif n.o == 'REF':
      l = self.itp_node(n.v)
      if isinstance(l, elog_els.id):
        return elog_els.val(f'{self.TYNA["LNK"]}:{self.TYNA["REF"]}', (l.t, l.idx))

      else: self.gowrong(f'Reference operand is not an ID. Operand: {l}')

    elif n.o == 'ITP':
      l = self.getval(self.itp_node(n.v))

      if l.t == f'{self.TYNA["NOD"]}:{self.TYNA["BLK"]}':
        self.idc.append(dict())
        self.rls.append(list())

        self.itp_lines(l.v)

        for idck, idcv in self.idc[-1].items():
          for i in range(idcv): self.ids[idck].pop()

        l = elog_els.val(f'{self.TYNA["COL"]}:{self.TYNA["VEC"]}:{self.TYNA["ANY"]}', self.rls[-1])

        self.idc.pop()
        self.rls.pop()

        return l

      else: self.gowrong(f'Interpretation operand is not a block. Operand: {l}')



    else: self.gowrong(f'Uninterpretable unary operation. Operation: {n.o}')


  def itp_bop(self, n : elog_nodes.binop) -> elog_els.el:

    if n.o == 'LETIN':
      if not isinstance(n.l, elog_nodes.val) or n.l.t != 'ID':
        self.gowrong(f'LetIn ID is not a tokenized ID. Left operand token: {n.l}')
      if n.r.t != 'LABEL':
        self.gowrong(f'LetIn type is not a tokenized label. Right operand token: {n.r}')

      self.idc[-1][n.l.v] = self.idc[-1].get(n.l.v, 0) + 1
      self.vls.append(elog_els.val(f'{self.TYNA["ERR"]}:{self.TYNA["UNS"]}', 0))

      if n.l.v not in self.ids.keys(): self.ids[n.l.v] = list()
      self.ids[n.l.v].append(elog_els.id(n.l.v, len(self.vls) - 1, n.r.v))


    elif n.o == 'DEF':
      l = self.itp_node(n.l)
      
      if isinstance(l, elog_els.v_function):
        ... # TODO

      elif isinstance(l, elog_els.id):
        r = self.getval(self.itp_node(n.r))

        ltmp = l.t.split(':')
        rtmp = r.t.split(':')
        for i in range(len(ltmp)):
          if i < len(rtmp):
            if ltmp[i] != rtmp[i] and ltmp[i] != 'any' and rtmp[i] != 'any':
              self.gowrong(f'Setting value is not of the ID type. ID type: {l.t}; value type: {r.t}')

        if isinstance(l, elog_els.id2i):
          l.get().t = r.t
          l.get().v = deepcopy(r.v)

        elif r.t == f'{self.TYNA["LNK"]}:{self.TYNA["REF"]}':
          l.t = r.v[0]
          l.idx = r.v[1]

        elif l.idx < len(self.vls):

          self.vls[l.idx].t = r.t
          self.vls[l.idx].v = deepcopy(r.v)

        else: self.gowrong('Index of the setting ID is not existant yet.')

        return elog_els.val(f'{self.TYNA["ERR"]}:{self.TYNA["NUL"]}', 0)

      else: self.gowrong('Setting left operand is not an ID.')

    elif n.o == 'ADD':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == self.TYNA["NUM"] and r.t.split(':')[0] == self.TYNA["NUM"]:
        return elog_els.val(r.t if r.t.split(':')[1] == self.TYNA["FLT"] else l.t, l.v + r.v)

      else: self.gowrong(f'Addition operand(s) is/are not (a) number(s). Operands: {l}, {r}')

    elif n.o == 'SUB':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == self.TYNA["NUM"] and r.t.split(':')[0] == self.TYNA["NUM"]:
        return elog_els.val(r.t if r.t.split(':')[1] == self.TYNA["FLT"] else l.t, l.v - r.v)

      else: self.gowrong(f'Subtraction operand(s) is/are not (a) number(s). Operands: {l}, {r}')


    elif n.o == 'MUL':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == self.TYNA["NUM"] and r.t.split(':')[0] == self.TYNA["NUM"]:
        return elog_els.val(r.t if r.t.split(':')[1] == self.TYNA["FLT"] else l.t, l.v * r.v)

      else: self.gowrong(f'Multiplication operand(s) is/are not (a) number(s). Operands: {l}, {r}')

    elif n.o == 'DIV':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == self.TYNA["NUM"] and r.t.split(':')[0] == self.TYNA["NUM"]:
        return elog_els.val(f'{self.TYNA["NUM"]}:{self.TYNA["FLT"]}', float(l.v) / float(r.v))

      else: self.gowrong(f'Division operand(s) is/are not (a) number(s). Operands: {l}, {r}')

    elif n.o == 'POW':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == self.TYNA["NUM"] and r.t.split(':')[0] == self.TYNA["NUM"]:
        return elog_els.val(r.t if r.t.split(':')[1] == self.TYNA["FLT"] else l.t, l.v ** r.v)

      else: self.gowrong(f'Power operand(s) is/are not (a) number(s). Operands: {l}, {r}')

    elif n.o == 'AND':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == self.TYNA["BOO"] and r.t.split(':')[0] == self.TYNA["BOO"]:
        return elog_els.val(self.TYNA["BOO"], l.v and r.v)

      else: self.gowrong(f'Logical AND operand(s) is/are not (a) boolean(s). Operands: {l}, {r}')

    elif n.o == 'OR':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == self.TYNA["BOO"] and r.t.split(':')[0] == self.TYNA["BOO"]:
        return elog_els.val(self.TYNA["BOO"], l.v or r.v)

      else: self.gowrong(f'Logical OR operand(s) is/are not (a) boolean(s). Operands: {l}, {r}')

    elif n.o == 'XOR':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == self.TYNA["BOO"] and r.t.split(':')[0] == self.TYNA["BOO"]:
        return elog_els.val(self.TYNA["BOO"], l.v != r.v)

      else: self.gowrong(f'Logical XOR operand(s) is/are not (a) boolean(s). Operands: {l}, {r}')

    elif n.o == 'EQ':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == r.t.split(':')[0]:
        return elog_els.val(self.TYNA["BOO"], l.v == r.v)

      else: self.gowrong(f'Equality operands are not of a single basic type. Operands: {l}, {r}')

    elif n.o == 'NEQ':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == r.t.split(':')[0]:
        l = elog_els.val(self.TYNA["BOO"], l.v != r.v)
        return l

      else: self.gowrong(f'Unequality operands are not of a single basic type. Operands: {l}, {r}')

    elif n.o == 'GRT':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == r.t.split(':')[0]:
        l = elog_els.val(self.TYNA["BOO"], l.v > r.v)
        return l

      else: self.gowrong(f'Comparision operands are not of a single basic type. Operands: {l}, {r}')

    elif n.o == 'LSS':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == r.t.split(':')[0]:
        l = elog_els.val(self.TYNA["BOO"], l.v < r.v)
        return l

      else: self.gowrong(f'Comparision operands are not of a single basic type. Operands: {l}, {r}')

    elif n.o == 'GRTEQ':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == r.t.split(':')[0]:
        l = elog_els.val(self.TYNA["BOO"], l.v >= r.v)
        return l

      else: self.gowrong(f'Comparision operands are not of a single basic type. Operands: {l}, {r}')

    elif n.o == 'LSSEQ':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))
      if l.t.split(':')[0] == r.t.split(':')[0]:
        l = elog_els.val(self.TYNA["BOO"], l.v <= r.v)
        return l

      else: self.gowrong(f'Comparision operands are not of a single basic type. Operands: {l}, {r}')


    elif n.o == 'SSCR':
      l = self.getval(self.itp_node(n.l))
      r = self.getval(self.itp_node(n.r))

      lt = l.t.split(':')
      if lt[0] == self.TYNA["COL"]:
        if lt[1] == self.TYNA["VEC"]:
          if r.t == f'{self.TYNA["NUM"]}:{self.TYNA["INT"]}' and r.v != 0 and r.v <= len(l.v):
            return elog_els.id2i(l.t[len(lt[0]) + len(lt[0]):], r.v - (1 if r.v > 0 else 0), l.v[0].t, l.v)

        else: self.gowrong(f'Subscript right operand is not a count (integer number different to 0) in range. Operand: {l}')
      else: self.gowrong(f'Subscript left operand is not of a valid types. Operand: {l}')

    else: self.gowrong(f'Uninterpretable binary operation. Operation: {n.o}')


  def itp_top(self, n : elog_nodes.triop) -> elog_els.el:

    if n.o == 'IF':
      c = self.getval(self.itp_node(n.f))

      if c.t.split(':')[0] == self.TYNA["BOO"]:
        if c.v: return self.itp_node(n.s)
        else: return self.itp_node(n.t)

      else: self.gowrong(f'Conditional deviation condition is not a boolean. Operand: {c}')

    elif n.o == 'LETAS':
      if not isinstance(n.f, elog_nodes.val) or n.f.t != 'ID':
        self.gowrong(f'LetAs ID operand is not a tokenized ID. Left operand token: {n.f}')
      if n.s.t != 'LABEL':
        self.gowrong(f'LetAs type is not a tokenized label. Right operand token: {n.s}')

      self.idc[-1][n.f.v] = self.idc[-1].get(n.f.v, 0) + 1

      li = elog_els.val(n.s.v, 0)
      r = self.getval(self.itp_node(n.t))

      ltmp = li.t.split(':')
      rtmp = r.t.split(':')
      for i in range(len(ltmp)):
        if i < len(rtmp):
          if ltmp[i] != rtmp[i] and ltmp[i] != 'any' and rtmp[i] != 'any':
            self.gowrong(f'LetAs value is not of the given type. given type: {n.s.v}; value type: {r.t}')
  
      if li.t == f'{self.TYNA["LNK"]}:{self.TYNA["REF"]}':
        li.t = r.v[0]
        li.idx = r.v[1]

      else:
        li.v = r.v
        li.t = r.t

      self.vls.append(li)

      if n.f.v not in self.ids.keys(): self.ids[n.f.v] = list()
      self.ids[n.f.v].append(elog_els.id(n.f.v, len(self.vls) - 1, n.s.v))


    else: self.gowrong(f'Uninterpretable ternary operation. Operation: {n.o}')


  def itp_set(self, n : elog_nodes.setof) -> elog_els.el:

    if n.t == 'BLOCK':
      return elog_els.val(f'{self.TYNA["NOD"]}:{self.TYNA["BLK"]}', n.s)

  # elif n.t == 'MAT':
  #    return elog_els.val(f'{self.TYNA["COL"]}:{self.TYNA["VEC"]}', n.v)
  # TODO: REDO

    else: self.gowrong(f'Uninterpretable binary operation. Operation: {n.o}')


  def itp_val(self, n : elog_nodes.val) -> elog_els.el:

    if n.t == 'ID':
      if n.v in self.ids.keys(): r = self.ids[n.v][-1]
      else: self.gowrong('ID is not defined.')
    else:
      r = elog_els.val('', 0)

      if n.t == 'NUM':
        r.t = f'{self.TYNA["NUM"]}:{self.TYNA["INT"]}'
        r.v = int(n.v)
      elif n.t == 'FNUM':
        r.t = f'{self.TYNA["NUM"]}:{self.TYNA["FLT"]}'
        r.v = float(n.v)
      elif n.t == 'TEXT':
        r.t = f'{self.TYNA["TXT"]}:{self.TYNA["STR"]}'
        r.v = str(n.v)
      elif n.t == 'BOOL':
        r.t = f'{self.TYNA["BOO"]}'
        r.v = eval(n.v)
      else: self.gowrong('Uninterpretable value type.')

    return r


  def itp_node(self, n : elog_nodes.node) -> elog_els.el:

    if isinstance(n, elog_nodes.unop): return self.itp_uop(n)
    elif isinstance(n, elog_nodes.binop): return self.itp_bop(n)
    elif isinstance(n, elog_nodes.triop): return self.itp_top(n)
    elif isinstance(n, elog_nodes.setof): return self.itp_set(n)
    elif isinstance(n, elog_nodes.val): return self.itp_val(n)
    else: self.gowrong('Uninterpretable node type.')


  def itp_lines(self, nl : list[elog_nodes.node], cln : bool = True) -> elog_els.el:

    for l in nl:
        self.itp_node(l)
        if cln: self.lns += 1


  def itp_all(self) -> None:

    self.itp_lines(self.nodes)

    for rl in self.rls[0]:
      print(rl)


