import ply.lex as lex


class BoolLexer(object):
    tokens = (
        'VARIABLE',
        'CONJUCTION',
        'DISJUCTION',
        'IMPLICATION',
        'NEGATION',
        'LPAREN',
        'RPAREN',
    )

    # t_VARIABLE = r'[a-z]'
    t_VARIABLE = r'[a-zA-Z]+'
    t_CONJUCTION = r'\/\\'
    t_DISJUCTION = r'\\\/'
    t_IMPLICATION = r'\-\>'
    t_NEGATION = r'\~'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
        # Build the lexer

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def run(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


if __name__ == '__main__':
    data = '''
     (p -> q) /\ (~r \/ s) /\ (~q -> p)
    '''
    blexer = BoolLexer()
    # blexer.build(debug=1)
    blexer.build()
    blexer.run(data)
