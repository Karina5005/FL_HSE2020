import main


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
        return main.parser('f.').process()[0] == -1

    def good_test2(self):
        return main.parser('f :- g.').process()[0] == -1

    def good_test3(self):
        return main.parser('f :- g, h; t.').process()[0] == -1

    def good_test4(self):
        return main.parser('f :- g, (h; t).').process()[0] == -1

    def good_test5(self):
        return main.parser('f :- (g),h.').process()[0] == -1

    def good_test6(self):
        return main.parser("f :- ((gh, kl); (qw, po); k) ;p.").process()[0] == -1

    def good_test7(self):
        return main.parser('f :- ((g),(h)).').process()[0] == -1

    def good_test8(self):
        return main.parser('f :- ((g);(h)).').process()[0] == -1

    def good_test9(self):
        return main.parser('fAb :- ((g),(h)).').process()[0] == -1

    def good_test10(self):
        return main.parser('o_o :- ((g);(h)).').process()[0] == -1

    def good_test11(self):
        return main.parser('fAb1 :- ((g),(h)).').process()[0] == -1

    def bad_test1(self):
        return main.parser('f').process()[0] != -1

    def bad_test2(self):
        return main.parser('f : g.').process()[0] != -1

    def bad_test3(self):
        return main.parser('f :- g, h; t).').process()[0] != -1

    def bad_test4(self):
        return main.parser('f :- g, (h t).').process()[0] != -1

    def bad_test5(self):
        return main.parser('f :- (g),h).').process()[0] != -1

    def bad_test6(self):
        return main.parser(' :- (g);h.').process()[0] != -1

    def bad_test7(self):
        return main.parser('f :- ((g),(h)').process()[0] != -1

    def bad_test8(self):
        return main.parser('f ((g);(h)).').process()[0] != -1

    def bad_test9(self):
        return main.parser('f : - g.').process()[0] != -1

    def bad_test10(self):
        return main.parser('f :- g h.').process()[0] != -1

    def bad_test11(self):
        return main.parser('1f :- g h.').process()[0] != -1
