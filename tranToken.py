#!/usr/bin/env python
import tokenize
from token import tok_name
from token import ERRORTOKEN, NAME, OP
import sys
from pprint import pprint

_NORMAL = 0
_PARTIAL_SUBJECT = 1
_UNTIL_LEFT_PARENTHESIS = 2
_PARTIAL_IN_PARENTHESES = 3
_UNTIL_RIGHT_PARENTHESIS = 4


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
            subject_lp = 0
            paren_lp = 0
            st_stack = []

            for i, tk in enumerate(tokens):
                tktype, tkstr, tkstart, tkend, tkline = tk
                #pprint((tok_name[tktype], tkstr))
                if st == _PARTIAL_SUBJECT:
                    if (tktype, tkstr) == (OP, '('):
                        result.append((tktype, tkstr))
                        subject_lp = 1
                        st = _PARTIAL_IN_PARENTHESES
                    else:
                        result.append((tktype, tkstr))
                        st = _UNTIL_LEFT_PARENTHESIS

                elif st == _PARTIAL_IN_PARENTHESES:
                    if (tktype, tkstr) == (OP, '('):
                        result.append((tktype, tkstr))
                        subject_lp += 1
                    elif (tktype, tkstr) == (OP, ')'):
                        subject_lp -= 1
                        if subject_lp < 0:
                            raise Exception(
                                    "Parentheses don't match on line "
                                    "%d, col %d" % tkline, tkstart)
                        result.append((tktype, tkstr))
                        if subject_lp == 0:
                            st = _UNTIL_LEFT_PARENTHESIS
                    elif (tktype, tkstr) == (ERRORTOKEN, '$'):
                        result.extend(
                                [(NAME, 'superPartial'),
                                 (OP, '(')])
                        st_stack.append((st, subject_lp, paren_lp))
                        subject_lp = 0
                        paren_lp = 0
                        st = _PARTIAL_SUBJECT
                    else:
                        result.append((tktype, tkstr))

                elif st == _UNTIL_LEFT_PARENTHESIS:
                    if (tktype, tkstr) == (OP, '('):
                        result.append((OP, ','))
                        paren_lp = 1
                        st = _UNTIL_RIGHT_PARENTHESIS
                    else:
                        result.append((tktype, tkstr))

                elif st == _UNTIL_RIGHT_PARENTHESIS:
                    if (tktype, tkstr) == (OP, '('):
                        result.append((tktype, tkstr))
                        paren_lp += 1
                    elif (tktype, tkstr) == (OP, ')'):
                        paren_lp -= 1
                        if paren_lp < 0:
                            raise Exception(
                                    "Parentheses don't match on line "
                                    "%d, col %d" % tkline, tkstart)
                        result.append((tktype, tkstr))
                        if paren_lp == 0:
                            st, subject_lp, paren_lp = st_stack.pop()
                    elif (tktype, tkstr) == (ERRORTOKEN, '$'):
                        result.extend(
                                [(NAME, 'superPartial'),
                                 (OP, '(')])
                        st_stack.append((st, subject_lp, paren_lp))
                        subject_lp = 0
                        paren_lp = 0
                        st = _PARTIAL_SUBJECT
                    else:
                        result.append((tktype, tkstr))

                elif st == _NORMAL:
                    if (tktype, tkstr) == (ERRORTOKEN, '$'):
                        result.extend(
                                [(NAME, 'superPartial'),
                                 (OP, '(')])
                        st_stack.append((st, subject_lp, paren_lp))
                        subject_lp = 0
                        paren_lp = 0
                        st = _PARTIAL_SUBJECT
                    else:
                        result.append((tktype, tkstr))

                else:
                    raise Exception("Unkown parsing state %d" % st)
            print "from functools import partial as superPartial\n"
            print tokenize.untokenize(result)
            print
