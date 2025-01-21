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

                print("\n\n\nE_LOG --- INITIALIZING TOKENIZER\n\n\n")

                self.tkn = elog_tokenizer()


            elif argv[idx] == 'tokenize':

                print("\n\n\nE_LOG --- TOKENIZING\n\n\n")

                tokens = self.tkn.tokenize(code)


            elif argv[idx] == 'print_tokens':

                print("\n\n\nE_LOG --- PRINTING TOKENS\n\n\n")

                print( *map(lambda x : f'{x[0]} : {x[1]} \t', tokens) )


            elif argv[idx] == 'init_parser':

                print("\n\n\nE_LOG --- INITIALIZING PARSER\n\n\n")

                self.par = elog_parser(tokens)


            elif argv[idx] == 'parse':

                print("\n\n\nE_LOG --- PARSING\n\n\n")

                nodes = self.par.parse()


            elif argv[idx] == 'print_nodes':

                print("\n\n\nE_LOG --- PRINTING PARSED NODES\n\n\n")
                
                print( reduce(lambda a, b : f'{a}\n{b}', nodes) )


            elif argv[idx] == 'init_interpreter':

                print("\n\n\nE_LOG --- INITIALIZING INTERPRETER\n\n\n")

                self.itr = elog_interpreter(nodes)


            elif argv[idx] == 'interpret':

                print("\n\n\nE_LOG --- INTERPRETING\n\n\n")

                nodes = self.itr.itp_all()


            elif argv[idx] == 'run':

                print("\n\n\nE_LOG --- FULL_DEBUG\n\n\n")

                argv += ['init_tokenizer', 'tokenize', 'print_tokens', 'init_parser', 'parse', 'print_nodes', 'init_interpreter', 'interpret']


            idx += 1


if __name__ == '__main__': eidoslogos().main(sys.argv)
