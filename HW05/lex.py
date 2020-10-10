import ply.lex as lex

tokens = [
    'POINT',
    'SPIN',
    'OR',
    'AND',
    'LBR',
    'RBR',
    'ID'
]

t_POINT = r'\.'
t_SPIN = r'\:\-'
t_OR = r'\;'
t_AND = r'\,'
t_LBR = r'\('
t_RBR = r'\)'


def t_ID(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s' at line %i at pos %i" % (t.value[0], t.lineno, t.lexpos))
    t.lexer.skip(1)


lexer = lex.lex()
