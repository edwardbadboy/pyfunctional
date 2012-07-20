#!/usr/bin/env python
import tokenize
from token import tok_name
from token import ERRORTOKEN, NAME, OP
import sys
from pprint import pprint

_NORMAL = 0
_INPARTIAL = 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s file1 file2 ...\n' %
                         sys.argv[0])
        exit(1)

    for fname in sys.argv[1:]:
        with open(fname) as f:
            tokens = tokenize.generate_tokens(f.readline)
            #print '"%s" tokens:' % fname

            result = []
            st = _NORMAL
            for i, tk in enumerate(tokens):
                tktype, tkstr, tkstart, tkend, tkline = tk
                #pprint((tok_name[tktype], tkstr))
                if st == _INPARTIAL:
                    if (tktype, tkstr) == (OP, '('):
                        result.append((OP, ','))
                        st = _NORMAL
                    else:
                        result.append((tktype, tkstr))
                elif tktype == ERRORTOKEN and tkstr == '$':
                    result.extend(
                            [(NAME, 'superPartial'),
                             (OP, '(')])
                    st = _INPARTIAL
                else:
                    result.append((tktype, tkstr))
            print "from functools import partial as superPartial\n"
            print tokenize.untokenize(result)
            print
