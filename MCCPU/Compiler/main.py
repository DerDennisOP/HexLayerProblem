import lexer
import interpreter
import sys
import os


if len(sys.argv) != 2:
    filename = "MCCPU/main.red"
    # print("Usage: python main.py <filename>.red")
    # sys.exit(1)
# filename = sys.argv[1]

# check if the file extension is .red
if filename[-4:] != ".red":
    print("The file extension should be \".red\"")
    sys.exit(1)

# check if the file exists
if not os.path.exists(filename):
    print("The file does not exist.")
    sys.exit(1)

tokens = lexer.interpret_file(filename)
expressions = interpreter.interpret_tokens(tokens)

print(expressions)