import opcode
import error_s
from ast import Delete

global OPERATION_LIST   # OPERAION CODE DICTIONARY
global REGISTER         # RESISTORS LIST
global BINARY_CODE       # TEMPRORY INSTRUCTION
global CURRENT_LINE     # CURRENT LINE
global VARIABLE         # VARIABLE DICTIONARY
global LABEL            # LABEL DICTIONARY
global ans
global op_type
global op_code
global INP
CURRENT_LINE = 1

INP = []

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
    "hlt": ["01010", "F"]
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

BINARY_CODE = [0,0,0,0,0,0]   #BINARY CODE GENERATED IN LIST FORMATED 

REGISTER = [0,0,0,0,0,0,0,[0,0,0,0]]   #REGISTERS(R1,R2,R3,R4,R5,R6,R7,FLAG())

ans=''


def valid_var_name(name, var_dict, reg_dict, opcodes):
    if(not(name.replace('_', '').isalnum() or set(name)=={'_'}) or name.isnumeric()):
        return 2
    if(name in opcodes.keys()):
        return 3
    if(name in reg_dict.keys()):
        return 4
    if(name in var_dict.keys()):
        return 5
    return 1    

def valid_label_name(name, var_dict, label_dict, reg_dict, opcodes):
    if(not(name.replace('_', '').isalnum() or set(name)=={'_'}) or name.isnumeric()):
        return 2
    if(name in opcodes.keys()):
        return 3
    if(name in reg_dict.keys()):
        return 4
    if(name in label_dict.keys()):
        return 5
    if(name in var_dict.keys()):
        return 6
    return 1

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO


# VAR STORING
while(CURRENT_LINE <= len(INP)):
    if(INP[CURRENT_LINE-1]==""):
        CURRENT_LINE += 1
    elif(INP[CURRENT_LINE-1].split()[0]=="var"):
        if(len(INP[CURRENT_LINE-1].split()) != 2):
            TEST_NO = 1
            error_s.variable_error(CURRENT_LINE, TEST_NO)
            exit()
        else:
            myVar = INP[CURRENT_LINE-1].split()[1]
            # check_valid_var_name() along with not in instr or reg or redefinition
            verdict = valid_var_name(myVar, VARIABLE, REGISTER_NAMES, OPERATION_LIST)
            if(verdict!=1):
                TEST_NO = verdict
                error_s.variable_error(CURRENT_LINE, TEST_NO, myVar)
                exit()
            VARIABLE[myVar] = [None, 0]
            CURRENT_LINE += 1
    else:
        break
    
MEM_LINE = 0
    
# Label Storing with address
while(CURRENT_LINE <= len(INP)):
    if(INP[CURRENT_LINE-1]==""):
        CURRENT_LINE += 1
        continue
    if(INP[CURRENT_LINE-1].split()[0][-1:]==":"):
        # check_valid_label_name() along with not in instruction or reg or redefinition
        myLabel = INP[CURRENT_LINE-1].split()[0][:-1]
        verdict = valid_label_name(myLabel, VARIABLE, LABEL, REGISTER_NAMES, OPERATION_LIST)
        if(verdict != 1):
            TEST_NO = verdict
            error_s.label_error(CURRENT_LINE, TEST_NO, myLabel)
            exit()
        if(len(INP[CURRENT_LINE-1].split())==1):
            TEST_NO = 7
            error_s.label_error(CURRENT_LINE, TEST_NO, myLabel)
            exit()
        LABEL[myLabel] = [MEM_LINE]
        MEM_LINE += 1
    elif(INP[CURRENT_LINE-1].split()[0]=="var"):
        TEST_NO = 6
        error_s.variable_error(CURRENT_LINE, TEST_NO)
        exit()
    elif(INP[CURRENT_LINE-1]!=""):
        MEM_LINE += 1
    CURRENT_LINE += 1

# Assign address to variables
for v in VARIABLE:
    VARIABLE[v][0] = MEM_LINE
    MEM_LINE += 1

# Check Memory Overflow
if(MEM_LINE>=257):
    error_s.mem_over_flow()
    exit()

# Check last instruction is hlt or not and how many hlt instructions
CURRENT_LINE = len(INP)
hlt_count = 0
while(CURRENT_LINE>=1):
    if(INP[CURRENT_LINE-1]!=""):
        if(INP[CURRENT_LINE-1].split()[0]=="hlt" or (INP[CURRENT_LINE-1].split()[0][-1]==":" and INP[CURRENT_LINE-1].split()[1]=="hlt")):
            hlt_count += 1 
        if(hlt_count==0):
            TEST_NO = 1
            error_s.hlt_error(CURRENT_LINE, TEST_NO)
            exit()
    if(hlt_count>1):
        TEST_NO = 2
        error_s.hlt_error(CURRENT_LINE, TEST_NO)
        exit()
    CURRENT_LINE -= 1
    
CURRENT_LINE = 1


#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

def valid_var_name(name, var_dict, reg_dict, opcodes):
    if(not(name.replace('_', '').isalnum() or set(name)=={'_'}) or name.isnumeric()):
        return 2
    if(name in opcodes.keys()):
        return 3
    if(name in reg_dict.keys()):
        return 4
    if(name in var_dict.keys()):
        return 5
    return 1    

def valid_label_name(name, var_dict, label_dict, reg_dict, opcodes):
    if(not(name.replace('_', '').isalnum() or set(name)=={'_'}) or name.isnumeric()):
        return 2
    if(name in opcodes.keys()):
        return 3
    if(name in reg_dict.keys()):
        return 4
    if(name in label_dict.keys()):
        return 5
    if(name in var_dict.keys()):
        return 6
    return 1

def reg(r):
    d={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110'}
    return d[r]

def bin(num,j):
    st=''
    for i in range(j):
        a=num%2
        num=num//2
        st+=str(a)
    return st[::-1]

def val_reg(list_reg, type_instr, reg_names, var_label_dict=None):
    if(type_instr=="A"):
        for i in range(len(list_reg)):
            if(list_reg[i] not in reg_names):
                return i+1
            if(list_reg[i] == "FLAGS"):
                return 10
        return 0
    if(type_instr=="B"):
        if(list_reg[0] not in reg_names):
            return 1
        if(list_reg[0] == "FLAGS"):
            return 10
        if(int(list_reg[1][1:])>255 or int(list_reg[1][1:])<0):
            return 2
        return 0
    if(type_instr=="C"):
        for i in range(len(list_reg)):
            if(list_reg[i] not in reg_names):
                return i+1
        if(list_reg[0] == "FLAGS"):
            return 10
        if(list_reg[1] == "FLAGS" and var_label_dict[0]!="00011"):
            return 10
        return 0
    if(type_instr=="D"):
        if(list_reg[0] not in reg_names):
            return 1
        if(list_reg[0] == "FLAGS"):
            return 10
        if(list_reg[1] not in var_label_dict.keys()):
            return 2
        return 0
    if(type_instr=="E"):
        if(list_reg[0] not in var_label_dict.keys()):
            return 1
        return 0
    return 0

def reset_binary_code():
    for i in range(len(BINARY_CODE)):
        BINARY_CODE[i] = 0

def reset_flags():
    for i in range(0,4):
        REGISTER[7][i] = 0

def INSTRUCTION_TYPE(instruction):       #CHECK COVERSION INSTRUCTION FROM INSTRUCTION AND OPERATION LIST AND CALLS EACH INSTRUCTION ERRORS 
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
    verdict = val_reg([reg1, reg2, reg3], "A", REGISTER_NAMES)
    if(verdict!=0):
        if(verdict==10):
            error_s.flags_invalid(CURRENT_LINE)
        else:
            error_s.invalid_reg(CURRENT_LINE, instruction[verdict])
        exit()
    BINARY_CODE[1] = REGISTER_NAMES[reg1]
    BINARY_CODE[2] = REGISTER_NAMES[reg2]
    BINARY_CODE[3] = REGISTER_NAMES[reg3]
    ans=str(BINARY_CODE[0])+'00'+str(BINARY_CODE[1])+str(BINARY_CODE[2])+str(BINARY_CODE[3])
    ans+='\n'
    # print(ans)
    
def instruction_B(instruction):
    if(len(instruction)!=3):
        for k, v in OPERATION_LIST.items():
            if v[0] == BINARY_CODE[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURRENT_LINE, TEST_NO, "B")
        exit()
    reg1 = instruction[1] 
    imm_val = instruction[2] 
    verdict = val_reg([reg1, imm_val], "B", REGISTER_NAMES)
    if(verdict!=0):
        if(verdict==1):
            error_s.invalid_reg(CURRENT_LINE, instruction[verdict])
        elif(verdict==2):
            error_s.invalid_imm(CURRENT_LINE, instruction[verdict])
        elif(verdict==10):
            error_s.flags_invalid(CURRENT_LINE)
        exit()
    BINARY_CODE[1] = REGISTER_NAMES[reg1]
    BINARY_CODE[4] = bin(imm_val,8)
    ans=str(BINARY_CODE[0])+str(BINARY_CODE[1])+str(BINARY_CODE[4])
    ans+='\n'
    
def instruction_C(instruction):
    if(len(instruction)!=3):
        for k, v in OPERATION_LIST.items():
            if v[0] == BINARY_CODE[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURRENT_LINE, TEST_NO, "C")
        exit()
    reg1 = instruction[1] 
    reg2 = instruction[2] 
    verdict = val_reg([reg1, reg2], "C", REGISTER_NAMES, {0:BINARY_CODE[0]})
    if(verdict!=0):
        if(verdict==10):
            error_s.flags_invalid(CURRENT_LINE)
        else:
            error_s.invalid_reg(CURRENT_LINE, instruction[verdict])
        exit()
    BINARY_CODE[1] = REGISTER_NAMES[reg1]
    BINARY_CODE[2] = REGISTER_NAMES[reg2]
    ans=str(BINARY_CODE[0])+'00000'+str(BINARY_CODE[1])+str(BINARY_CODE[2])
    ans+='\n'

def instruction_D(instruction):
    if(len(instruction)!=3):
        for k, v in OPERATION_LIST.items():
            if v[0] == BINARY_CODE[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURRENT_LINE, TEST_NO, "D")
        exit()
    reg1 = instruction[1] 
    mem_addr = instruction[2] 
    verdict = val_reg([reg1, mem_addr], "D", REGISTER_NAMES, VARIABLE)
    if(verdict!=0):
        if(verdict==1):
            error_s.invalid_reg(CURRENT_LINE, instruction[verdict])
        elif(verdict==2):
            TEST_NO = 0
            error_s.invalid_mem_addr(CURRENT_LINE, instruction[verdict], TEST_NO)
        elif(verdict==10):
            error_s.flags_invalid(CURRENT_LINE)
        exit()
    BINARY_CODE[1] = REGISTER_NAMES[reg1]
    BINARY_CODE[5] = mem_addr
    ans=str(BINARY_CODE[0])+str(BINARY_CODE[1])+str(BINARY_CODE[5])
    ans+='\n'

def instruction_E(instruction):
    if(len(instruction)!=2):
        for k, v in OPERATION_LIST.items():
            if v[0] == BINARY_CODE[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURRENT_LINE, TEST_NO, "E")
        exit()
    mem_addr = instruction[1]
    verdict = val_reg([mem_addr], "E", None, LABEL)
    if(verdict!=0):
        TEST_NO = 1
        error_s.invalid_mem_addr(CURRENT_LINE, instruction[verdict], TEST_NO)
        exit()

def instruction_F(instruction):
        if(len(instruction)!=1):
        for k, v in OPERATION_LIST.items():
            if v[0] == BINARY_CODE[0]:
                TEST_NO = k
                break
        error_s.improper_len_instr(CURRENT_LINE, TEST_NO, "F")
        exit()
for i in op_table.ANS:
    print(i)
