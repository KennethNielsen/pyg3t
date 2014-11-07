from __future__ import print_function
import sys
from pyg3t.gtparse import PoError, PoHeaderError
# will this eventually become a circular import?
# Maybe PoSyntaxError should be defined un util so that all modules
# can use util without util using any of them

class Encoder:
    def __init__(self, fd, encoding):
        self.fd = fd
        self.encoding = encoding
        
    def write(self, txt):
        self.fd.write(txt.encode(encoding=self.encoding))


colors = {'blue': '0;34',
          'light red': '1;31',
          'light purple': '1;35',
          'brown': '0;33',
          'purple': '0;35',
          'yellow': '1;33',
          'dark gray': '1;30',
          'light cyan': '1;36',
          'black': '0;30',
          'light green': '1;32',
          'cyan': '0;36',
          'green': '0;32',
          'light blue': '1;34',
          'light gray': '0;37',
          'white': '1;37',
          'red': '0;31',
          'old': '1;31;41', # To do: proper names, reorganize
          'new': '1;33;42', # These are used by gtprevmsgdiff
          None: None}

def colorize(string, id):
    if id is None:
        return string
    tokens = []
    for line in string.split('\n'):
        if len(line) > 0:
            line = '\x1b[%sm%s\x1b[0m' % (id, line)
        tokens.append(line)
    return '\n'.join(tokens)


class Colorizer:
    def __init__(self, colorname):
        self.color = colors[colorname]

    def colorize(self, string):
        return colorize(string, self.color)

class NullDevice:
    def write(self, txt):
        pass

def getfiles(args):
    for arg in args:
        if arg == '-':
            name = '<stdin>'
            yield name, sys.stdin
        else:
            fd = open(arg)
            yield arg, fd


# Decorator for all main functions in pyg3t
def pyg3tmain(main):
    def main_decorator():
        try:
            main()
        except KeyboardInterrupt:
            print('Interrupted by keyboard', file=sys.stderr)
            raise SystemExit(1)
        except PoError as err:
            maxlength = len('%d' % err.lineno)
            print(err.errmsg, file=sys.stderr)
            print('-' * len(err.errmsg), file=sys.stderr)
            lineoffset = 1 + err.lineno - len(err.last_lines)
            for i, line in enumerate(err.last_lines):
                lineno = lineoffset + i
                print(('%d' % lineno).rjust(maxlength), line, end='',
                      file=sys.stderr)
            print(file=sys.stderr)
            raise SystemExit(-1)
        except PoHeaderError as err:
            for arg in err.args:
                print(arg, file=sys.stderr)
            raise SystemExit(-1)
    return main_decorator
