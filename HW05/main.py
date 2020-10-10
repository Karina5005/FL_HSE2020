import sys
import parser

if __name__ == "__main__":
    file_input = open(sys.argv[1])
    file_output = open(sys.argv[1] + ".out", "w")
    text = file_input.read()
    out = parser.parser.parse(text)
    if out:
        file_output.write(out)
    else:
        print("Failed")
