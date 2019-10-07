import ply.yacc as yacc
import ply.lex as lex


SAT = 'satisfiable'
NO_SAT = 'not satisfiable'
tokens = (
    'VARIABLE',
    'CONJUCTION',
    'DISJUCTION',
    'IMPLICATION',
    # 'NEGATION',
    'LPAREN',
    'RPAREN',
)

t_VARIABLE = r'~?[a-zA-Z]+'
t_CONJUCTION = r'\/\\'
t_DISJUCTION = r'\\\/'
t_IMPLICATION = r'\-\>'
# t_NEGATION = r'\~'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

list_var = []


def p_statement_expr(t):
    'statement : expression'
    # print(t[1])



def p_expression_conjuction(t):
    'expression : expression CONJUCTION expression'
    if t[1] is not None:
        list_var.append([t[1], None])
    if t[3] is not None:
        list_var.append([t[3], None])


def p_expression_disjuction(t):
    'expression : expression DISJUCTION expression'

    list_var.append([t[1], t[3]])


def p_expression_implication(t):
    'expression : expression IMPLICATION expression'

    if t[1][0] == '~':
        list_var.append([t[1][1:], t[3]])
    else:
        list_var.append(['~' + t[1], t[3]])


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]


def p_expression_var(t):
    'expression : VARIABLE'
    t[0] = t[1]
    # print(t[:3])


def p_error(t):
    print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()


def is_opposite(var1, var2):
    return ((var1 is not None) and (len(var1) > 1) and (
            var2 == var1[1:]) and (var1[0] == '~')) or (
                   (var2 is not None) and (len(var2) > 1) and (
                   var2[1:] == var1) and (var2[0] == '~'))


def pair_is_None(pair):
    return (pair[0] is None) and (pair[1] is None)


def check_sat(list_var):
    i = 1
    while i < len(list_var):
        if pair_is_None(list_var[i]):
            return NO_SAT
        for j in range(i):
            for k1 in range(len(list_var[i])):  # cycle length 2
                for k2 in range(len(list_var[j])):  # cycle length 2
                    if (list_var[j][k2] is None) or (list_var[i][k1] is None):
                        continue
                    if is_opposite(list_var[j][k2], list_var[i][k1]):
                        if list_var[i][(k1 + 1) % 2] != list_var[j][(k2 + 1) % 2]:
                            if ~is_opposite(list_var[i][(k1 + 1) % 2], list_var[j][(k2 + 1) % 2]):
                                el = [list_var[i][(k1 + 1) % 2], list_var[j][(k2 + 1) % 2]]
                                if pair_is_None(el):
                                    return NO_SAT
                                list_var.append(el)
                        else:
                            el = [list_var[i][(k1 + 1) % 2], None]
                            if pair_is_None(el):
                                return NO_SAT
                            list_var.append(el)

        i += 1
    return SAT


def run(s, print_list=False):
    list_var.clear()
    parser.parse(s)
    if print_list:
        print(list_var)
    res = check_sat(list_var)
    list_var.clear()
    return res


flag_print = False
assert (run('a /\ ~a', flag_print) == NO_SAT)
assert (run('a /\ a', flag_print) == SAT)
assert (run('a -> b', flag_print) == SAT)
assert (run('(a -> b) /\ (b->c) /\ (c -> d) /\ (~d) /\ (a)', flag_print) == NO_SAT)
assert (run('(p -> q) /\ (~r \/ s) /\ (~q -> p)', flag_print) == SAT)
assert (run('(a\/~b)/\(b\/c)/\(~a\/c)/\ e /\(~e\/~c)', flag_print) == NO_SAT)
