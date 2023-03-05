import re

def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

def tokonize(code: list):
    tokens = []

    for i in range(len(code)):
        token = code[i]

        # check if the token is a number
        if token.isdigit():
            tokens.append(("STATIC", token))
            continue

        if token[0] == "@":
            tokens.append(("FUNCTION", token[1:]))
            continue

        if token[0] == "#":
            tokens.append(("VAR", token[1:]))
            continue

        if token in ["ted", "lib", "place", "print", "exit"]:
            tokens.append(("KEYWORD", token))
            continue

        if token[0] == ":":
            tokens.append(("TYPE", token[1:]))
            continue

        if token in ["(", ")"]:
            tokens.append(("BRACKET", token))
            continue

        if token in ["[", "]"]:
            tokens.append(("LIST", token))
            continue

        if token == "=":
            tokens.append(("SETTER", token))
            continue

        if token in ["+", "-", "*", "/", "%", "^", "&", "|", "~", "!", "<", ">"]:
            tokens.append(("OPERATOR", token))
            continue

        if token in ["==", "!=", "<=", ">=", "&&", "||"]:
            tokens.append(("STATEMENT", token))
            continue
        
        tokens.append(("IDENTIFIER", token))
    
    return tokens

def interpret_file(filename: str):
    code = ""

    with open(filename, "r") as f:
        code = f.read()
        f.close()
    
    # remove the comments
    code = remove_comments(code)

    # remove the newlines, tabs
    code = code.replace("\\t", "").replace("\\n", "").replace("(", " ( ").replace(")", " ) ").replace("[", " [ ").replace("]", " ] ").replace("=", " = ").replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ").replace("%", " % ").replace("^", " ^ ").replace("&", " & ").replace("|", " | ").replace("~", " ~ ").replace("!", " ! ").replace("<", " < ").replace(">", " > ").replace("==", " == ").replace("!=", " != ").replace("<=", " <= ").replace(">=", " >= ").replace("&&", " && ").replace("||", " || ")

    # remove the whitespaces
    code = code.split()

    tokens = []
    for x in code:
        # check if first character is a :
        if ":" in x and x[0] != ":": # label
            tokens.append(x.split(":")[0])
            tokens.append(":" + x.split(":")[1])
        else:
            tokens.append(x)

    tokens = tokonize(tokens)

    return tokens