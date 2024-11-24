from functools import reduce

import elog_nodes


class elog_parser:
    
    def __init__(self, tkns : list[tuple[str, str]]):

        self.r : list[elog_nodes.node] = list()

        self.tkns : list[tuple[str, str]] = tkns

        self.idx : int = 0

    
    def gowrong(self) -> None:

        raise Exception(f'\n\nThings went crazy at idx={self.idx}, token {self.tkns[self.idx]}\nr={self.r}\n')


    def p_csv(self) -> elog_nodes.node:

        l = elog_nodes.setof('CSV', self.p_val())
        
        while True:

            if self.tkns[self.idx][0] == 'COMMA':

                self.idx += 1

                l.add(self.p_expr0())

            else: return l
 

    def p_matl(self) -> elog_nodes.node:

        l = elog_nodes.setof('MATL', self.p_val())
        
        while True:

            if self.tkns[self.idx][0] in ['SBE', 'COMMA']: return l

            self.idx += 1

            l.add(self.p_val())
 
    
    def p_mat(self) -> elog_nodes.node:

        l = elog_nodes.setof('MAT', self.p_matl())
        
        while True:

            if self.tkns[self.idx][0] == 'COMMA':

                self.idx += 1

                l.add(self.p_matl())

            else: return l
 

    def p_set(self) -> elog_nodes.node:

        l = elog_nodes.setof('SET', self.p_val())
        
        while True:

            if self.tkns[self.idx][0] == 'DCOMMA':

                self.idx += 1

                l.add(self.p_stc())

            else: return l
 

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

        
        elif self.tkns[self.idx][0] == 'REF':

            self.idx += 1

            l = elog_nodes.unop('REF', self.p_val())

            self.idx += 1
            
            return l


        elif self.tkns[self.idx][0] in ['NUM', 'FNUM', 'TEXT', 'ID']:

            v = elog_nodes.val(self.tkns[self.idx][0], self.tkns[self.idx][1])

            self.idx += 1


            if self.tkns[self.idx][0] == 'UNDERL':

                self.idx += 1

                v = elog_nodes.binop(v, 'SSCR', self.p_csv())

            else:

                while True:

                    if self.tkns[self.idx][0] == 'PBB':

                        self.idx += 1

                        l = self.p_val()

                        if self.tkns[self.idx][0] != 'PBE': self.gowrong()

                        self.idx += 1

                        v = elog_nodes.binop(v, 'FUNC', l)


                    else: return v


        elif self.tkns[self.idx][0] in ['TRUE', 'FALSE']:

            l = elog_nodes.val('BOOL', self.tkns[self.idx][0])

            self.idx += 1

            return l
        

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


            if self.tkns[self.idx][0] in ['EQ', 'NEQ', 'GRT', 'LSS', 'GRTEQ', 'LSSEQ', 'AND', 'OR', 'XOR', 'IN']:

                self.idx += 1

                l = elog_nodes.binop(l, self.tkns[self.idx-1][0], self.p_expr())

            else: break


        return l


    def p_stc(self) -> elog_nodes.node:

        if self.tkns[self.idx][0] == 'LBD':

            self.idx += 1

            l = self.p_val()

            if self.tkns[self.idx][0] != 'DDOT': self.gowrong()

            self.idx += 1

            l = elog_nodes.binop(l, 'LBD', self.p_stc())

        
        else:
            
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

            
            if self.tkns[self.idx][0] == 'IN':

                self.idx += 1
            
                l = elog_nodes.binop(l, 'LETIN', self.p_stc())


            elif self.tkns[self.idx][0] == 'AS':

                self.idx += 1
            
                l = elog_nodes.binop(l, 'LETAS', self.p_stc())

            
            else: self.gowrong()


        else:

            l = self.p_stc()


            if self.tkns[self.idx][0] == 'DEF':

                self.idx += 1

                l = elog_nodes.binop(l, 'DEF', self.p_stc())


            else: l = elog_nodes.unop('RETURN', l)


        if self.tkns[self.idx][0] == 'WITH': 

            self.idx += 1

            l = elog_nodes.binop(l, 'WITH', self.p_stc())


        return l


    def parse(self) -> list[elog_nodes.node]:

        while self.idx < len(self.tkns):

            if self.tkns[self.idx][0] == 'EOSCR': break

            l = self.parsel()

            self.r.append(l)

            if self.tkns[self.idx][0] in ['PERIOD', 'EOSCR']: self.idx += 1

            else: self.gowrong()

        return self.r


