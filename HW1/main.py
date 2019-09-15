import ply.lex as lex

tokens = (
    'VARIABLE',
    'CONJUCTION',
    'DISJUCTION',
    'IMPLICATION',
    'NEGATION',
    'LPAREN',
    'RPAREN',
)

t_VARIABLE = r'[a-z]'
t_CONJUCTION = r'\/\\'
t_DISJUCTION = r'\\\/'
t_IMPLICATION = r'\-\>'
t_NEGATION = r'\~'
t_LPAREN = r'\('
t_RPAREN = r'\)'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
 (p -> q) /\ (~r \/ s) /\ (~q -> p)
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    # print(tok)
    print(tok.type, tok.value, tok.lineno, tok.lexpos)
