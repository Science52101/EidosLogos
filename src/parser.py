from functools import reduce

import elog_nodes


class elog_parser:
    
    def __init__(self, tkns : list[tuple[str, str]]):

        self.r : list[elog_nodes.node] = list()
        self.tkns : list[tuple[str, str]] = tkns
        self.idx : int = 0
        self.lns : int = 1

    
    def gowrong(self, error : str = 'unknown') -> None:

        raise Exception(f'\n\n[Parsing error!]\nMsg: {error}\nAt : {self.lns}th line (of content), {self.idx}th token, {self.tkns[self.idx]}\nExt: r = {self.r}\n\n')


    def p_csv(self) -> elog_nodes.node:

        l = elog_nodes.setof('CSV', self.p_pval())
        
        while True:

            if self.tkns[self.idx][0] == 'COMMA':
                self.idx += 1

                l.add(self.p_expr0())

            else: return l
 

    def p_matl(self) -> elog_nodes.node:

        l = elog_nodes.setof('MATL', self.p_pval())
        
        while True:

            if self.tkns[self.idx][0] in ['SBE', 'COMMA']: return l
            self.idx += 1

            l.add(self.p_pval())
 
    
    def p_mat(self) -> elog_nodes.node:

        l = elog_nodes.setof('MAT', self.p_matl())
        
        while True:

            if self.tkns[self.idx][0] == 'COMMA':
                self.idx += 1

                l.add(self.p_matl())

            else: return l
 

    def p_set(self) -> elog_nodes.node:

        l = elog_nodes.setof('SET', self.p_pval())
        
        while True:

            if self.tkns[self.idx][0] == 'DCOMMA':

                self.idx += 1

                l.add(self.p_stc())

            else: return l
 

    def p_val(self) -> elog_nodes.node:

        if self.tkns[self.idx][0] == 'PBB':
            self.idx += 1

            l = self.p_stc()

            if self.tkns[self.idx][0] != 'PBE': self.gowrong("Expected end of parenthesis ()).")
            self.idx += 1

            return l


        elif self.tkns[self.idx][0] == 'CBB':
            self.idx += 1

            l = self.p_set()

            if self.tkns[self.idx][0] != 'CBE': self.gowrong("Expected end of braces (}).")
            self.idx += 1

            return l


        elif self.tkns[self.idx][0] == 'SBB':

            self.idx += 1

            l = self.p_mat()

            if self.tkns[self.idx][0] != 'SBE': self.gowrong()

            self.idx += 1

            return l


        elif self.tkns[self.idx][0] in ['REF', 'ITP']:
            self.idx += 1

            return elog_nodes.unop(self.tkns[self.idx-1][0], self.p_pval())


        elif self.tkns[self.idx][0] == 'QDOT':

            self.idx += 1

            if not self.tkns[self.idx][0] == 'CBB':
                self.gowrong("Expected beginning braces ({).")
            self.idx += 1

            l = elog_nodes.setof('BLOCK', [])

            self.parse(end = 'CBE', cln = False, addf = l.add)

            if self.tkns[self.idx][0] != 'CBE': self.gowrong("Expected end of braces (}).")
            self.idx += 1

            
            return l


        elif self.tkns[self.idx][0] in ['NUM', 'FNUM', 'TEXT', 'ID']:

            if self.tkns[self.idx][0] == 'TEXT' or (self.tkns[self.idx][0] == 'ID' and self.tkns[self.idx][1][0] == '`'):
                v = elog_nodes.val(self.tkns[self.idx][0], self.tkns[self.idx][1][1:-1])
            else:
                v = elog_nodes.val(self.tkns[self.idx][0], self.tkns[self.idx][1])
            self.idx += 1

            return v

        elif self.tkns[self.idx][0] in ['TRUE', 'FALSE']:

            v = elog_nodes.val('BOOL', self.tkns[self.idx][0].title())

            self.idx += 1

            return v


        elif self.tkns[self.idx][0] in ['SUB', 'NOT']:
            self.idx += 1

            return elog_nodes.unop(self.tkns[self.idx-1][0], self.p_pval())


        elif self.tkns[self.idx][0] == 'ADD':
            self.idx += 1

            return self.p_pval()
        

        else: self.gowrong("Could not parse value. / Expected value.")


    def p_pval(self) -> elog_nodes.node:

        v = self.p_val()

        while True:

            if self.tkns[self.idx][0] == 'UNDERL':
                self.idx += 1

                v = elog_nodes.binop(v, 'SSCR', self.p_val())

            elif self.tkns[self.idx][0] == 'PBB':
                self.idx += 1

                r = self.p_val()

                if self.tkns[self.idx][0] != 'PBE': self.gowrong("Expected end of parenthesis.")
                self.idx += 1

                return elog_nodes.binop(v, 'FUNC', r)

            else: break

        return v
   

    def p_pows(self) -> elog_nodes.node:
        l = self.p_pval()

        while True:

            if self.tkns[self.idx][0] == 'POW':
                self.idx += 1

                l = elog_nodes.binop(l, self.tkns[self.idx-1][0], self.p_pval())

            else: break

        return l


    def p_fact(self) -> elog_nodes.node:
        l = self.p_pows()

        while True:

            if self.tkns[self.idx][0] in ['MUL', 'DIV', 'MOD']:
                self.idx += 1

                l = elog_nodes.binop(l, self.tkns[self.idx-1][0], self.p_pows())

            else: break

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

            l = self.p_pval()

            if self.tkns[self.idx][0] != 'DDOT': self.gowrong('Expected a double dot (:).')
            self.idx += 1

            l = elog_nodes.binop(l, 'LBD', self.p_stc())
        
        elif self.tkns[self.idx][0] == 'IF':
            self.idx += 1

            s = self.p_expr0()

            if self.tkns[self.idx][0] != 'COMMA': self.gowrong("Expected a comma (,).")
            self.idx += 1
            
            l = self.p_expr0()

            if self.tkns[self.idx][0] not in ['COMMA', 'DCOMMA']: self.gowrong("Expected a comma (,) or a semicolon (;).")
            self.idx += 1

            if self.tkns[self.idx][0] == 'ELSE':
                self.idx += 1

                if self.tkns[self.idx][0] == 'COMMA': self.idx += 1

                l = elog_nodes.triop('IF', s, l, self.p_expr0())

            else:
                l = elog_nodes.triop('IF', s, l, self.p_stc())
        
        else: l = self.p_expr0()

        
        return l


    def parsel(self) -> elog_nodes.node:

        if self.tkns[self.idx][0] == 'LET':
            self.idx += 1

            l = self.p_pval()

            
            if self.tkns[self.idx][0] == 'DDOT':
                self.idx += 1

                l = elog_nodes.binop(l, 'LETIN', self.p_stc())


            elif self.tkns[self.idx][0] == 'AS':
                self.idx += 1

                l = elog_nodes.triop('LETAS', l, self.p_stc(), self.p_stc())
            
            else: self.gowrong("LET token without token after structure.")

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


    def parse(self, end : str = 'EOSCR', cln : bool = True, addf : callable = None) -> list[elog_nodes.node]:
        if not addf: addf = self.r.append

        while self.idx < len(self.tkns):
            if self.tkns[self.idx][0] == end: break
            elif cln: self.lns += 1

            l = self.parsel()
            addf(l)

            if self.tkns[self.idx][0] in ['PERIOD', end]: self.idx += 1
            else: self.gowrong('Expected an end of line.')

        return self.r


