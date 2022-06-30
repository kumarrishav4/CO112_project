f = open('C:\\Users\\hardik\\Desktop\\C\\txt.txt')
con_lin=f.readlines()
opcodes = {
    "add": ["10000", "A"],
    "sub": ["10001", "A"],
    "mov": ["10010", "B"],
    "mov": ["10011", "C"],
    "ld": ["10100", "D"],
    "st": ["10101", "D"],
    "mul": ["10110", "A"],
    "div": ["10111", "C"],
    "rs": ["11000", "B"],
    "ls": ["11001", "B"],
    "xor": ["11010", "A"],
    "or": ["11011", "A"],
    "and": ["11100", "A"],
    "not": ["11101", "C"],
    "cmp": ["11110", "C"],
    "jmp": ["11111", "E"],
    "jlt": ["01100", "E"],
    "jgt": ["01101", "E"],
    "je": ["01111", "E"],
    "hlt": ["01010", "F"],
}

for i in con_lin:
    command=i.split(' ')
    if(command[0] in opcodes.keys()):
        if(opcodes[command[0]][1]=="A"):
            print(tya(command[0],command[1],command[2],command[3]))
        elif(opcodes[command[0]][1]=="B"):
            print(tyb(command[0],command[1],command[2]))
        elif(opcodes[command[0]][1]=="C"):
            print(tyc(command[0],command[1],command[2]))
        elif(opcodes[command[0]][1]=="D"):
            print(tyd(command[0],command[1],command[2]))
        elif(opcodes[command[0]][1]=="E"):
            print(tye(command[0],command[1]))
        elif(opcodes[command[0]][1]=="F"):
            print('01010')