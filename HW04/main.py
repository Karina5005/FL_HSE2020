import sys
import test


def split_and_keep(s, sep):
    if not s:
        return ['']
    p = chr(ord(max(s)) + 1)
    return s.replace(sep, sep + p).split(p)


def lexer(s):
    for i in range(len(s)):
        if (s[i] == ' ' and s[i - 1] == ' ') or (s[i] == '\n' and s[i - 1] == '\n') or (
                s[i] == '\t' and s[i - 1] == '\t'):
            continue
        yield s[i]
    while True:
        yield '\0'


def position_colon(s):
    pos = 0
    for i in range(len(s)):
        if (s[i] == ' ' and s[i - 1] == ' ') or (s[i] == '\n' and s[i - 1] == '\n') or (
                s[i] == '\t' and s[i - 1] == '\t'):
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

    def step(self):
        self.current = next(self.lex)
        self.current_pos_col = next(self.pos_col)
        self.current_pos_line = next(self.pos_line)

    def accept(self, c):
        if self.current == c:
            self.step()
            return True
        return False

    def skip(self):
        while self.current == '\n' or self.current == '\t' or self.current == ' ':
            self.step()

    def expect(self, c):
        if self.current == c:
            self.step()
            return True
        return False

    def letter(self):
        if self.current.isalpha():
            self.step()
            return True
        else:
            return False

    def word(self):
        if not (self.current.isalpha() or self.current == '_'):
            return False
        while self.current.isalnum() or self.current == '_':
            self.step()
        return True

    def tail(self):
        while self.current != '\0' and self.current != '.':
            if not self.disj():
                return False
            return True

    def process(self):
        self.skip()
        if not self.word():
            return self.current_pos_col, self.current_pos_line
        self.skip()
        if self.accept(':'):
            if self.expect('-'):
                self.skip()
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
        self.skip()
        if not self.conj():
            return False
        if self.accept(';'):
            self.skip()
            if not self.disj():
                return False
        return True

    def conj(self):
        if not self.lit():
            return False
        if self.accept(','):
            self.skip()
            if not self.conj():
                return False
            self.skip()
        return True

    def lit(self):
        if self.accept('('):
            self.skip()
            if not self.tail():
                return False
            self.skip()
            if not self.expect(')'):
                return False
            self.skip()
            return True
        self.skip()
        if not self.word():
            return False
        return True


if __name__ == "__main__":
    test.Tester().run()
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
        if part != '\n':
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
