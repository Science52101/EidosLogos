import sys
from parser import *
from tokenizer import *

class eidoslogos(object):

    def __init__(self) -> None:
        
        self.tkn : elog_tokenizer
        self.par : elog_parser
   

    def main(self, argv : list[str]) -> None:

        if len(argv) != 2:

            print('Please give file argument.')

            return

        self.tkn = elog_tokenizer()

        tokens : list[tuple[str, str]] = self.tkn.tokenize(open(argv[1], 'r').read());

        print( *map(lambda x : f'{x[0]} | {x[1]}\n', tokens) )
        
        self.par = elog_parser(tokens);

        nodes = self.par.parse();

        print( *nodes )



if __name__ == '__main__': eidoslogos().main(sys.argv)
