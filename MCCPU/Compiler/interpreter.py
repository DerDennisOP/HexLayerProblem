
import sys

def get_all_tokens():
    return ["KEYWORD", "IDENTIFIER", "NUMBER", "FUNCTION", "TYPE", "BRACKET", "OPERATOR", "SETTER", "STATEMENT"]

def get_all_start_tokens():
    return ["KEYWORD", "FUNCTION", "BRACKET", "VAR"]

def interpret_place(tokens: list, i = 0):
    next_token = ["STATIC", "OPERATOR", "ONLY_NEG", "LIST"]
    expression = []
    coords = []
    in_vars = 0
    next_val_neg = False

    while i < len(tokens):
        token = tokens[i]
        if token[0] in next_token:
            if token[0] == "STATIC":
                if next_val_neg:
                    next_val_neg = False
                    coords.append(-int(token[1]))
                else:
                    coords.append(int(token[1]))
                if len(coords) == 3:
                    expression.append(("COORDINATES", coords))
                    coords = []
                    next_token = ["IDENTIFIER", "OPERATOR", "STATIC", "ONLY_NEG"]
                elif len(coords) == 1 and len(expression) == 1 and expression[-1][0] == "COORDINATES":
                    expression.append(("STATIC", coords[0]))
                    coords = []
                    next_token = ["IDENTIFIER", "CORDS_DONE"]
                else:
                    next_token = ["STATIC", "OPERATOR", "ONLY_NEG"]
            elif token[0] == "IDENTIFIER" and not "CORDS_DONE" in next_token:
                expression.append(token)
                next_token = ["IDENTIFIER", "CORDS_DONE"]
            elif token[0] == "IDENTIFIER" and "CORDS_DONE" in next_token:
                if token[1] == "input" or token[1] == "output":
                    expression.append(token)
                    next_token = ["IDENTIFIER", "CORDS_DONE"]
                    in_vars = 1
                elif in_vars > 0:
                    in_vars -= 1
                    expression.append(token)
                    if in_vars == 0:
                        # next_token = ["STATIC", "OPERATOR", "ONLY_NEG", "LIST"]
                        return (expression, i)
            elif token[0] == "OPERATOR":
                if token[1] == "!" and not "ONLY_NEG" in next_token:
                    expression.append(token)
                    next_token = ["IDENTIFIER"]
                elif token[1] == "-":
                    next_val_neg = True
                    next_token = ["STATIC"]
        else:
            print(f"Syntax error at {token[0]} \"{token[1]}\"")
            sys.exit(1)
        i += 1

    return (expression, i)

def interpret_expressions(tokens: list, i = 0):
    next_token = get_all_start_tokens()
    expression = []

    while i < len(tokens):
        token = tokens[i]
        if token[0] in next_token:
            if token[0] == "KEYWORD":
                if token[1] == "ted":
                    next_token = ["IDENTIFIER"]
                    expression.append(token)
                elif token[1] == "lib":
                    next_token = ["IDENTIFIER"]
                    expression.append(token)
                elif token[1] == "place":
                    next_token = ["LIST", "PLACE"]
                    expression.append(token)
            elif token[0] == "IDENTIFIER":
                expression.append(token)
                if expression[0][0] == "KEYWORD":
                    return (expression, i)
                else:
                    next_token = ["TYPE"]
            elif token[0] == "FUNCTION":
                next_token = ["IDENTIFIER", "SETTER"]
                expression.append(token)
            elif token[0] == "SETTER":
                next_token = ["EXP", "STATIC"]
                expression.append(token)
            elif token[0] == "TYPE":
                expression.append(token)
                if expression[0][0] == "FUNCTION":
                    next_token = ["SETTER", "IDENTIFIER"]
                elif expression[0][0] == "VAR" and expression[-1][0] == "TYPE":
                    next_token = ["SETTER"]
                else:
                    next_token = ["IDENTIFIER", "TYPE"]
            elif token[0] == "VAR":
                expression.append(token)
                next_token = ["TYPE"]
            elif token[0] == "STATIC":
                if expression[0][0] == "VAR":
                    expression.append(token)
                    return (expression, i)
            elif token[0] == "BRACKET":
                if token[1] == "(":
                    next_token = ["EXP"]
                elif token[1] == ")":
                    return (expression, i)
            elif token[0] == "LIST":
                if token[1] == "[":
                    next_token = ["PLACE", "LIST"]
                elif token[1] == "]":
                    return (expression, i)
        elif next_token[0] == "EXP" and i < len(tokens):
            exp, i = interpret_expressions(tokens, i)
            if len(exp) > 1:
                expression.append(exp)
            elif len(exp) == 1:
                expression.append(exp[0])
        elif next_token[0] == "PLACE" and i < len(tokens):
            exp, i = interpret_place(tokens, i)
            if len(exp) > 1:
                expression.append(exp)
            elif len(exp) == 1:
                expression.append(exp[0])
        else:
            print(f"Syntax error at {token[0]} \"{token[1]}\"")
            sys.exit(1)
        i += 1

    return (expression, i)

def interpret_tokens(tokens: list):
    expression = []
    i = 0

    while i < len(tokens):
        token = tokens[i]
        if token[0] in get_all_start_tokens():
            exp, i = interpret_expressions(tokens, i)
            expression.append(exp)
        i += 1
    
    return expression
