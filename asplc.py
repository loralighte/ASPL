import sys 
if len(sys.argv) != 2: print("Usage: ASPLC <file>.aspl"); exit()
fileName = sys.argv[1]
if not fileName.endswith(".aspl"): print("Usage: ASPLC <file>.aspl"); exit()
contents = str()
with open(fileName) as file:
    fileContents = file.readlines()
    for line in fileContents: contents += line 
scannerStageOne = list(); word = str()
for char in contents:
    if char.isalnum(): word += char
    else:
        if word: scannerStageOne.append(word); word = str()
        scannerStageOne.append(char)
scannerStageTwo = list(); string = str()
for item in scannerStageOne:
    if string:
        if item == "\"": string += item; scannerStageTwo.append(string); string = str()
        else: string += item
    else: 
        if item == "\"": string += item
        else: scannerStageTwo.append(item)
scannerStageThree = list()
for item in scannerStageTwo:
    if item != " ": scannerStageThree.append(item)
scanner = scannerStageThree; lexer = list()
for i in scanner:
    if i == "(": lexer.append([i, "OpenParen"])
    elif i == ")": lexer.append([i, "ClosedParen"])
    elif i[0].isalpha(): lexer.append([i, "Identifer"])
    elif i.isdigit(): lexer.append([i, "Integer"])
    elif i[0] == "\"": lexer.append([i, "String"])
    else: lexer.append([i, "Token"])
position = -1; ast = list()
while position < len(lexer)-1:
    position += 1; token = lexer[position]
    def walk():
        global position, token
        if token[1] == "OpenParen":
            position += 1; token = lexer[position]; node = { "type": "CallExpression",  "value": token[0], "body": list() }
            while token[1] != "ClosedParen": position += 1; token = lexer[position]; node["body"].append(walk())
            for i in node["body"]:
                if None in node["body"]: node["body"].remove(None)
            return node
        elif token[1] == "String": node = { "type": "StringLiteral", "value": token[0] }; return node
        elif token[1] == "Integer":  node = { "type": "NumberLiteral", "value": token[0] }; return node
    ast.append(walk())
    for i in ast:
        if None in ast: ast.remove(None)
    break
generator = list()
for i in ast:
    def walk(node):
        lineGenerates = str()
        if node["type"] == "CallExpression":
            if node["value"] == "write": 
                lineGenerates += "print("
                for i in node["body"]: lineGenerates += walk(i)
            if node["value"] == "*": 
                lineGenerates += "("; position = -1
                while position < len(node["body"]) -1:
                    position += 1
                    lineGenerates += walk(node["body"][position])
                    if position < len(node["body"]) -1: lineGenerates += "*"
            if node["value"] == "+": 
                lineGenerates += "("; position = -1
                while position < len(node["body"]) -1:
                    position += 1
                    lineGenerates += walk(node["body"][position])
                    if position < len(node["body"]) -1: lineGenerates += "+"
            if node["value"] == "/": 
                lineGenerates += "("; position = -1
                while position < len(node["body"]) -1:
                    position += 1
                    lineGenerates += walk(node["body"][position])
                    if position < len(node["body"]) -1: lineGenerates += "/"
            if node["value"] == "-": 
                lineGenerates += "("; position = -1
                while position < len(node["body"]) -1:
                    position += 1
                    lineGenerates += walk(node["body"][position])
                    if position < len(node["body"]) -1: lineGenerates += "-"
            lineGenerates += ")"
        if node["type"] == "NumberLiteral": return node["value"]
        if node["type"] == "StringLiteral": return node["value"]
        return lineGenerates
    generator.append(walk(i))
with open(fileName.replace(".aspl", ".py"), "w") as generatefile: generatefile.writelines(generator)