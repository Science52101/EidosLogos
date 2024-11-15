from functools import reduce

class elog_nodes:

    class node: pass

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
        def __init__(self, n):
            self.s : list[elog_nodes.node] = [n]
        def add(self, n):
            self.s.append(n)
        def __repr__(self) -> str:
            return '{'+reduce(lambda a, b : a+b, [str(x) for x in self.s])+'}'


class elog_parser:
    
    def __init__(self, tkns : list[tuple[str, str]]):

        self.r : list[elog_nodes.node] = list()

        self.tkns : list[tuple[str, str]] = tkns

        self.idx : int = 0

    
    def gowrong(self) -> None:

        raise Exception(f'\n\nThings went crazy at idx={self.idx}, token {self.tkns[self.idx]}\nr={self.r}\n')


    def p_csv(self) -> elog_nodes.node:

        l = elog_nodes.setof(self.p_val())
        
        while True:

            if self.tkns[self.idx][0] == 'COMMA':

                self.idx += 1

                l.add(self.p_expr0())

            else: break
 
        return l


    def p_mat(self) -> elog_nodes.node:

        l = elog_nodes.setof(self.p_val())
        
        while True:

            if self.tkns[self.idx][0] == 'SBE': break

            self.idx += 1

            l.add(self.p_val())
 
        return l

    
    def p_set(self) -> elog_nodes.node:

        l = elog_nodes.setof(self.p_val())
        
        while True:

            if self.tkns[self.idx][0] == 'DCOMMA':

                self.idx += 1

                l.add(self.p_stc())

            else: break
 
        return l


    def p_val(self) -> elog_nodes.node:

        if self.tkns[self.idx][0] == 'PBB':

            self.idx += 1

            l = self.p_stc()

            if self.tkns[self.idx][0] != 'PBE': self.gowrong()

            self.idx += 1

            return l


        elif self.tkns[self.idx][0] == 'CBB':

            self.idx += 1

            l = self.p_set()

            if self.tkns[self.idx][0] != 'CBE': self.gowrong()

            self.idx += 1

            return l


        elif self.tkns[self.idx][0] == 'SBB':

            self.idx += 1

            l = self.p_mat()

            if self.tkns[self.idx][0] != 'SBE': self.gowrong()

            self.idx += 1

            return l



        elif self.tkns[self.idx][0] in ['NUM', 'FNUM', 'TEXT', 'ID']:

            v = elog_nodes.val(self.tkns[self.idx][0], self.tkns[self.idx][1])

            self.idx += 1

            if self.tkns[self.idx][0] == 'PBB':

                self.idx += 1

                l = self.p_csv()

                if self.tkns[self.idx][0] != 'PBE': self.gowrong()

                self.idx += 1

                return elog_nodes.binop(v, 'FUNC', l)
    
            else:

                return v

        else: self.gowrong()

   
    def p_fact(self) -> elog_nodes.node:

        if self.tkns[self.idx][0] in ['SUB', 'NOT']:

            self.idx += 1

            l = elog_nodes.binop(self.p_val(), self.tkns[self.idx-1][0], self.p_fact())

        else: l = self.p_val()


        if self.tkns[self.idx][0] in ['MUL', 'DIV', 'MOD']:

            self.idx += 1

            return elog_nodes.binop(l, self.tkns[self.idx-1][0], self.p_fact())
        
        else:

            return l


    def p_expr(self) -> elog_nodes.node:
        
        l = self.p_fact()


        while True:

            if self.tkns[self.idx][0] in ['ADD', 'SUB']:

                self.idx += 1

                l = elog_nodes.binop(l, self.tkns[self.idx-1][0], self.p_fact())

            else: break


        return l


    def p_expr0(self) -> elog_nodes.node:

        l = self.p_expr()

        while True:


            if self.tkns[self.idx][0] in ['EQ', 'NEQ', 'AND', 'OR', 'XOR', 'IN']:

                self.idx += 1

                l = elog_nodes.binop(l, self.tkns[self.idx-1][0], self.p_expr())

            else: break


        return l


    def p_stc(self) -> elog_nodes.node:

        l = self.p_expr0()


        while True:

            if self.tkns[self.idx][0] == 'IF':
                
                self.idx += 1
                
                s = self.p_expr0()

                if self.tkns[self.idx][0] != 'COMMA': self.gowrong()

                self.idx += 1


                if self.tkns[self.idx][0] == 'ELSE':

                    self.idx += 1

                    l = elog_nodes.triop('IF', l, s, self.p_expr0())

                else:

                    l = elog_nodes.triop('IF', l, s, self.p_stc())


            else: break

        
        return l


    def parsel(self) -> elog_nodes.node:

        if self.tkns[self.idx][0] == 'LET':

            self.idx += 1

            l = self.p_val()

            
            if self.tkns[self.idx][0] == 'DDOT':

                self.idx += 1
            
                l = elog_nodes.binop(l, 'LETIN', self.p_stc())
            

        else:

            l = self.p_stc()


            if self.tkns[self.idx][0] == 'DEF':

                self.idx += 1

                l = elog_nodes.binop(l, 'DEF', self.p_stc())


            else: l = self.p_csv()


        if self.tkns[self.idx][0] == 'WITH': 

            self.idx += 1

            l = elog_nodes.binop(l, 'WITH', self.p_stc())


        return l


    def parse(self) -> list[elog_nodes.node]:

        l = self.parsel()
        
        while self.tkns[self.idx][0] == 'PERIOD':

            self.r.append(l)

            self.idx += 1
            
            l = self.parsel()

        if self.tkns[self.idx][0] != 'EOSCR': self.gowrong()

        self.r.append(l)

        return self.r

