import error_s


global OPERATION_LIST   # OPERAION CODE DICTIONARY
global REGISTER         # RESISTORS LIST
global BINARY_CODE             # TEMPRORY INSTRUCTION
global CURRENT_LINE     # CURRENT LINE
global VARIABLE         # VARIABLE DICTIONARY
global LABEL            # LABEL DICTIONARY

CURRENT_LINE = 1

OPERATION_LIST = {             # OPERATION_LIST CODES
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

REGISTER_NAMES = {            # REGISTER KEY-(RX) VALUE-[ADRESS]
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAGS":"111"
}

VARIABLE={}             # VARIBLE DICTIONARY KEY-(VARIABLE) VALUE-[ADRESS]

LABEL={}                # LABEL DICTIONARY KEY-(LABEL) VALUE-[ADRESS]

BINARY_CODE = [0,0,0,0,0,0]    

REGISTER = [0,0,0,0,0,0,0,[0,0,0,0]]

def reset_temp():
    for i in range(len(BINARY_CODE)):
        BINARY_CODE[i] = 0

def reset_flags():
    for i in range(0,4):
        REGISTER[7][i] = 0

def INSTRUCTION_TYPE(instruction):
    is_reset_flag = False
    op = instruction[0]
    if  op in OPERATION_LIST:
        op_code = OPERATION_LIST[op][0]
        op_type = OPERATION_LIST[op][1]
        BINARY_CODE[0] = op_code
    else:
        error_s.op_error(CURRENT_LINE, 1, op)

    if  (op=="mov"):
        if  (len(instruction)>2 and instruction[2] in REGISTER): 
            BINARY_CODE[0] = "10011"
            op_type = "C"
        else:
            BINARY_CODE[0] = "10010"
            op_type = "B"

    if  ((op_type!="E" and op_code!="10011") or op_code=="11111"):
        is_reset_flag = True
        reset_flags()
    if  (op_type=="A"): instruction_A(instruction)
    elif(op_type=="B"): instruction_B(instruction)
    elif(op_type=="C"): instruction_C(instruction)
    elif(op_type=="D"): instruction_D(instruction)
    elif(op_type=="E"): instruction_E(instruction)
    elif(op_type=="F"): instruction_F(instruction)
    if(is_reset_flag==False):
         reset_flags()

def instruction_A(instruction):
    if(len(instruction)!=4):
        for KEY, VALUE in OPERATION_LIST.items():
            if VALUE[0] == BINARY_CODE[0]:
                TEST_NO = KEY
                break
        error_s.improper_len_instr(CURRENT_LINE, TEST_NO, "A")
        exit()
    reg1 = instruction[1]
    reg2 = instruction[2]
    reg3 = instruction[3]
    for i in range(len(REGISTER)):
        if(REGISTER[i] not in REGISTER_NAMES ):
            verdict= i+1
        if(REGISTER[i] == "FLAGS"):
            verdict= 10
    if(verdict!=0):
        if(verdict==10):
            error_s.flags_invalid(CURRENT_LINE)
        else:
            error_s.invalid_reg(CURRENT_LINE, instruction[verdict])
        exit()
    BINARY_CODE[1] = reg1
    BINARY_CODE[2] = reg2
    BINARY_CODE[3] = reg3


