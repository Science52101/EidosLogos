import sys
from parser import *
from tokenizer import *
from interpreter import *


class eidoslogos(object):

    def __init__(self) -> None:
        
        self.tkn : elog_tokenizer
        self.par : elog_parser
        self.itr : elog_interpreter
   

    def main(self, argv : list[str]) -> None:

        if len(argv) < 2:

            print('Please give arguments')

            return

        code : str = str()

        tokens : list[tuple[str, str]] = list()

        nodes : list[elog_nodes.node] = list()

        idx : int = 1

        while idx < len(argv):

            if argv[idx] == 'open':

                idx += 1

                with open(argv[idx], 'r') as tmp: code = tmp.read()


            elif argv[idx] == 'init_tokenizer':

                self.tkn = elog_tokenizer()


            elif argv[idx] == 'tokenize':

                tokens = self.tkn.tokenize(code)


            elif argv[idx] == 'print_tokens':

                print( *map(lambda x : f'\n{x[0]}\t| {x[1]}', tokens) )


            elif argv[idx] == 'init_parser':

                self.par = elog_parser(tokens)


            elif argv[idx] == 'parse':

                nodes = self.par.parse()


            elif argv[idx] == 'print_nodes':
                
                print( reduce(lambda a, b : f'{a}\n{b}', nodes) )


            elif argv[idx] == 'init_interpreter':

                self.itr = elog_interpreter(nodes)


            elif argv[idx] == 'interpret':

                nodes = self.itr.itp_all()


            elif argv[idx] == 'run':

                argv += ['init_tokenizer', 'tokenize', 'print_tokens', 'init_parser', 'parse', 'print_nodes', 'init_interpreter', 'interpret']


            idx += 1


if __name__ == '__main__': eidoslogos().main(sys.argv)
