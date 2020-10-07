import sys


def split_and_keep(s, sep):
    if not s:
        return ['']
    p = chr(ord(max(s)) + 1)
    return s.replace(sep, sep + p).split(p)


def lexer(s):
    for i in range(len(s)):
        if ((s[i] == " " and s[i - 1] == ' ') or s[i] == "\n") and s[i - 1] != ':' and s[i + 1] != '-':
            continue
        yield s[i]
    while True:
        yield '\0'


def position_colon(s):
    pos = 0
    for i in range(len(s)):
        if ((s[i] == " " and s[i - 1] == ' ') or s[i] == "\n") and s[i - 1] != ':' and s[i + 1] != '-':
            pos += 1
            continue
        pos += 1
        yield pos
    while True:
        yield pos


def position_line(s):
    pos = 0
    for c in s:
        if c == "\n":
            pos += 1
        yield pos
    while True:
        yield pos


class parser:
    def __init__(self, s):
        self.size = len(s)
        self.lex = lexer(s)
        self.pos_col = position_colon(s)
        self.pos_line = position_line(s)
        self.current = next(self.lex)
        self.current_pos_col = next(self.pos_col)
        self.current_pos_line = next(self.pos_line)

    def accept(self, c):
        if self.current == c:
            self.current = next(self.lex)
            self.current_pos_col = next(self.pos_col)
            self.current_pos_line = next(self.pos_line)
            return True
        return False

    def expect(self, c):
        if self.current == c:
            self.current = next(self.lex)
            self.current_pos_col = next(self.pos_col)
            self.current_pos_line = next(self.pos_line)
            return True
        # print("Unexpected character", self.current, "expected", c, self.current_pos)
        return False

    def letter(self):
        if self.current.isalpha():
            self.current = next(self.lex)
            self.current_pos_col = next(self.pos_col)
            self.current_pos_line = next(self.pos_line)
            return True
        else:
            return False

    def word(self):
        if not (self.current.isalpha() or self.current == '_'):
            return False
        while self.current.isalnum() or self.current == '_':
            self.current = next(self.lex)
            self.current_pos_col = next(self.pos_col)
            self.current_pos_line = next(self.pos_line)
        return True

    def tail(self):
        if not self.disj():
            return False
        return True

    def process(self):
        if not self.word():
            return self.current_pos_col, self.current_pos_line
        self.accept(' ')
        if self.accept(':'):
            if self.expect('-'):
                self.accept(' ')
                if not self.tail():
                    return self.current_pos_col, self.current_pos_line
            else:
                return self.current_pos_col, self.current_pos_line
        elif not self.current == '.':
            return self.current_pos_col, self.current_pos_line
        if self.expect('.'):
            return -1, self.current_pos_line
        return self.current_pos_col, self.current_pos_line

    def disj(self):
        self.accept(' ')
        if not self.conj():
            return False
        if self.accept(';'):
            self.accept(' ')
            if not self.disj():
                return False
        return True

    def conj(self):
        if not self.lit():
            return False
        if self.accept(','):
            self.accept(' ')
            if not self.conj():
                return False
            self.accept(' ')
        return True

    def lit(self):
        if self.accept('('):
            self.accept(' ')
            if not self.tail():
                return False
            self.accept(' ')
            if not self.expect(')'):
                return False
            self.accept(' ')
            return True
        self.accept(' ')
        if not self.word():
            return False
        return True


class Tester:
    def run(self):
        if not self.good_test1():
            print("Failed good_test1")
        if not self.good_test2():
            print("Failed good_test2")
        if not self.good_test3():
            print("Failed good_test3")
        if not self.good_test4():
            print("Failed good_test4")
        if not self.good_test5():
            print("Failed good_test5")
        if not self.good_test6():
            print("Failed good_test6")
        if not self.good_test7():
            print("Failed good_test7")
        if not self.good_test8():
            print("Failed good_test8")
        if not self.good_test9():
            print("Failed good_test9")
        if not self.good_test10():
            print("Failed good_test10")
        if not self.good_test11():
            print("Failed good_test11")
        if not self.bad_test1():
            print("Failed bad_test1")
        if not self.bad_test2():
            print("Failed bad_test2")
        if not self.bad_test3():
            print("Failed bad_test3")
        if not self.bad_test4():
            print("Failed bad_test4")
        if not self.bad_test5():
            print("Failed bad_test5")
        if not self.bad_test6():
            print("Failed bad_test6")
        if not self.bad_test7():
            print("Failed bad_test7")
        if not self.bad_test8():
            print("Failed bad_test8")
        if not self.bad_test9():
            print("Failed bad_test9")
        if not self.bad_test10():
            print("Failed bad_test10")
        if not self.bad_test11():
            print("Failed bad_test11")

    def good_test1(self):
        return parser('f.').process()[0] == -1

    def good_test2(self):
        return parser('f :- g.').process()[0] == -1

    def good_test3(self):
        return parser('f :- g, h; t.').process()[0] == -1

    def good_test4(self):
        return parser('f :- g, (h; t).').process()[0] == -1

    def good_test5(self):
        return parser('f :- (g),h.').process()[0] == -1

    def good_test6(self):
        return parser('f :- (g);h.').process()[0] == -1

    def good_test7(self):
        return parser('f :- ((g),(h)).').process()[0] == -1

    def good_test8(self):
        return parser('f :- ((g);(h)).').process()[0] == -1

    def good_test9(self):
        return parser('fAb :- ((g),(h)).').process()[0] == -1

    def good_test10(self):
        return parser('o_o :- ((g);(h)).').process()[0] == -1

    def good_test11(self):
        return parser('fAb1 :- ((g),(h)).').process()[0] == -1

    def bad_test1(self):
        return parser('f').process()[0] != -1

    def bad_test2(self):
        return parser('f : g.').process()[0] != -1

    def bad_test3(self):
        return parser('f :- g, h; t).').process()[0] != -1

    def bad_test4(self):
        return parser('f :- g, (h t).').process()[0] != -1

    def bad_test5(self):
        return parser('f :- (g),h).').process()[0] != -1

    def bad_test6(self):
        return parser(' :- (g);h.').process()[0] != -1

    def bad_test7(self):
        return parser('f :- ((g),(h)').process()[0] != -1

    def bad_test8(self):
        return parser('f ((g);(h)).').process()[0] != -1

    def bad_test9(self):
        return parser('f : - g.').process()[0] != -1

    def bad_test10(self):
        return parser('f :- g h.').process()[0] != -1

    def bad_test11(self):
        return parser('1f :- g h.').process()[0] != -1


if __name__ == "__main__":
    Tester().run()
    filename = sys.argv[1]
    file = open(filename, 'r')
    inp = file.read()
    program = ""
    for line in inp:
        program += line
    program = split_and_keep(program, '.')
    line = 0
    colon = 0
    for part in program:
        print(part)
        p = parser(part)
        result = p.process()
        line += result[1]
        if result[1] == 0 and result[0] != -1:
            colon += result[0]
        if not result[0] == -1:
            print("Syntax error ", "line:", line, ", colon:", colon + result[0])
            break
        if result[1] == 0 and result[0] != -1:
            colon += len(part)
        else:
            colon = 0
