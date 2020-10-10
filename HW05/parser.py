import ply.yacc as yacc
from lex import tokens

'''
P -> O POINT | O POINT P
O -> A_HEAD SPIN D | A_HEAD
D -> C OR D | C
C -> E AND C | E
E -> LBR D RBR | A_HEAD
A_HEAD -> ID | ID A_TAIL
A_TAIL -> LBR A_ARG RBR | MORE_A | LBR A_ARG RBR A_TAIL
A_ARG -> A_HEAD | LBR A_ARG RBR
MORE_A -> ID | ID A_TAIL
'''


def p_prog(p):
    """prog : oper POINT
            | oper POINT prog"""
    if len(p) == 3:
        p[0] = '(' + p[1] + ').\n'
    else:
        p[0] = '(' + p[1] + ').\n' + p[3]


def p_oper(p):
    """oper : atom_head SPIN disj
            | atom_head"""
    if len(p) == 4:
        p[0] = p[1] + ' :- ' + p[3]
    else:
        p[0] = p[1]


def p_disj(p):
    """disj : conj OR disj
            | conj"""
    if len(p) == 4:
        p[0] = 'dicj (' + str(p[1]) + ', ' + str(p[3]) + ')'
    elif len(p) == 2:
        p[0] = p[1]


def p_conj(p):
    """conj : expr AND conj
            | expr"""
    if len(p) == 4:
        p[0] = 'conj (' + str(p[1]) + ', ' + str(p[3]) + ')'
    elif len(p) == 2:
        p[0] = p[1]


def p_expr(p):
    """expr : LBR disj RBR
            |  atom_head """
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = p[1]


def p_atom_head(p):
    """atom_head : ID
                 | ID atom_tail"""
    if len(p) == 2:
        p[0] = 'ID(' + str(p[1]) + ')'
    else:
        p[0] = 'ID(' + str(p[1]) + '), ' + 'ATOMS{' + p[2] + '}'


def p_more_atom(p):
    """more_atom : ID
                 | ID atom_tail"""
    if len(p) == 2:
        p[0] = 'ID(' + str(p[1]) + ')'
    else:
        p[0] = 'ID(' + str(p[1]) + '), ' + p[2]


def p_atom_tail(p):
    """atom_tail : LBR atom_argument RBR
                 | more_atom
                 | LBR atom_argument RBR atom_tail"""
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = str(p[1])
    else:
        p[0] = str(p[2]) + ', ' + p[4]


def p_atom_argument(p):
    """atom_argument : atom_head
                     | LBR atom_argument RBR"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]


def p_error(p):
    print("Syntax error")


parser = yacc.yacc()


def parse(text):
    return parser.parse(text)
