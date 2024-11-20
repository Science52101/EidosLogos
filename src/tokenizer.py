import re

class elog_tokenizer:

    def __init__(self) -> None:

        self.TOKENP : list[tuple[str, str]] = [
            ('ID',     r'`(\\.|[^`\\])*`'),
            ('TEXT',   r'\'(\\.|[^\'\\])*\''),
            ('CMT',    r'\[~(\\.|[^~\\])+~\]'),
            ('LET',    r'\blet\b'),
            ('IN',     r'\bin\b'),
            ('AS',     r'\bas\b'),
            ('WITH',   r'\bwith\b'),
            ('IF',     r'\bif\b'),
            ('ELSE',   r'\belse\b'),
            ('FORALL', r'\bforall\b'),
            ('FORSOM', r'\bforsome\b'),
            ('ISTRUE', r'\bistrue\b'),
            ('LBD',    r'\blbd\b'),
            ('REF',    r'\bref\b'),
            ('TRUE',   r'\btrue\b'),
            ('FALSE',  r'\bfalse\b'),
            ('AND',    r'\band\b'),
            ('OR',     r'\bor\b'),
            ('XOR',    r'\bxor\b'),
            ('EQ',     r'\beq\b'),
            ('NOT',    r'\bnot\b'),
            ('MOD',    r'\bmod\b'),
            ('PERIOD', r'\.'),
            ('COMMA',  r','),
            ('DCOMMA', r';'),
            ('UNDERL', r'_'),
            ('Label',  r'"[a-zA-Z][a-zA-Z0-9]*'),
            ('ID',     r'[a-zA-Z][a-zA-Z0-9]*'),
            ('FNUM',   r'\d+\.\d+'),
            ('NUM',    r'\d+'),
            ('PBB',    r'\('),
            ('PBE',    r'\)'),
            ('SBB',    r'\['),
            ('SBE',    r'\]'),
            ('CBB',    r'\{'),
            ('CBE',    r'\}'),
            ('DEF',    r':='),
            ('NEQ',    r'/='),
            ('EQ',     r'='),
            ('GRT',    r'>'),
            ('LSS',    r'<'),
            ('GRTEQ',  r'>='),
            ('LSSEQ',  r'<='),
            ('QDOT',   r'::'),
            ('DDOT',   r':'),
            ('ADD',    r'\+'),
            ('SUB',    r'-'),
            ('MUL',    r'\*'),
            ('DIV',    r'/'),
            ('POW',    r'\^'),
            ('INTSEC', r'&'),
            ('UNION',  r'\|'),
            ('MATMUL', r'@'),
            ('WS',     r'\s+'),
            ('MISSM',  r'.')
        ]
        

    def tokenize(self, code : str) -> list[tuple[str, str]]:

        tokens : list[tuple[str, str]] = list()

        matched : bool

        match : re.match

        v : str


        while code:

            matched = False
            

            for t, p in self.TOKENP:

                match = re.match(p, code)

                
                if match:

                    matched = True

                    v = match.group()

                    if t not in ['WS', 'CMT']: tokens.append((t, v))

                    code = code[len(v):]

                    break


            if not matched:

                print(f'Not matched: {code[idx:]}')

        
        tokens.append(('EOSCR', ''))

        return tokens

