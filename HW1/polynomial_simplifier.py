# -----------------------------------------------------------------------------
# polysimpl.py
#
# Polynomial simplifier 
# Modified from calc.py, see  O'Reilly's "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys

sys.path.insert(0, "../..")

tokens = ['INT']
literals = ['+', '-', '(', ')', '^', 'x']


# 1. Tokens

def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print
        "Too large!", t.value
        t.value = 0
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print
    "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()


# 2. Helper functions for working with polynomials

# add a monomial to a polynomial, extending it if needed
def safeadd(q, i, x):
    if (i < len(q)):
        q[i] += x
    else:
        for _ in xrange(i - len(q)): q.append(0)
        q.append(x)
    return q


# pad array with zeroes to given length
def array_zpad(q, l):
    if (l >= len(q)):
        for _ in xrange(l - len(q)): q.append(0)
    return q


# add two polynomials
def polyadd(p, q):
    p = array_zpad(p, len(q))
    q = array_zpad(q, len(p))
    return map((lambda x, y: x + y), p, q)


# polynomial multiplication
def polymult(p, q):
    r = []
    for i in xrange(len(p)):
        for j in xrange(len(q)):
            safeadd(r, i + j, p[i] * q[j])
    return r


# print polynomial
def poly_to_string(p):
    if (len(p) == 0): return "0"

    if (p[0] != 0):
        r = str(p[0])
    else:
        r = ""

    msign = ""

    if (p[0] > 0): msign = "+"

    if (len(p) >= 1 and p[1] != 0):
        if (p[1] == 1):
            r = 'x' + msign + r
        else:
            r = str(p[1]) + 'x' + msign + r

        if (p[1] < 0): msign = ""

    for i in range(2, len(p)):
        if (p[i] != 0):
            if (p[i] == 1):
                r = 'x^' + str(i) + msign + r
            else:
                r = str(p[i]) + 'x^' + str(i) + msign + r

            if (p[i] < 0):
                msign = ""
            else:
                msign = "+"

    return r


# 3. Parsing rules

def p_final(p):
    'quest : expr'
    print
    poly_to_string(p[1])


def p_expr_tm(p):
    'expr : tm'
    p[0] = p[1]


def p_expr_mtm(p):
    "expr : '-' tm"
    p[0] = map((lambda x: (-x)), p[2])


def p_expr_addtm(p):
    "expr : expr '+' tm"
    p[0] = polyadd(p[1], p[3])


def p_expr_addmtm(p):
    "expr : expr '-' tm"
    p[0] = polyadd(p[1], map((lambda x: (-x)), p[3]))


def p_tm_mon(p):
    'tm : mon'
    p[0] = p[1]


def p_tm_brackets(p):
    "tm : '(' expr ')'"
    p[0] = p[2]


def p_tm_mult(p):
    "tm : tm '(' expr ')'"
    p[0] = polymult(p[1], p[3])


def p_mon(p):
    "mon : intopt 'x' powopt"
    p[0] = []
    safeadd(p[0], p[3], p[1])


def p_mon_free(p):
    'mon : INT'
    p[0] = [p[1]]


def p_intopt(p):
    '''intopt : INT
              | '''
    if len(p) == 1:
        p[0] = 1
    else:
        p[0] = p[1]


def p_powopt(p):
    '''powopt : '^' INT
              | '''
    if len(p) == 1:
        p[0] = 1
    else:
        p[0] = p[2]


def p_error(p):
    print
    "Syntax error at '%s'" % p.value


# Build the parser
import ply.yacc as yacc

yacc.yacc()

# 4. Simplify polynomials in an infinite loop
while 1:
    try:
        s = raw_input('input polynomial > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)