import sys #importing system library for stdin and stdout
import re
global REG # global list for resisters
global OPCODES #global list for operations and their respective codes
global TEMP   # global temperory storage for the binary instruction
global MEM_LINE # global memory occupied by the instructions or variable
global CURR_LINE # global current line for storing the initial line of the instruction
global VAR_S  # global variable dictionary for variable value and adress
global LABEL_S # global label dictionary for label value and adress
global TEST_NO # global test number 
global ANS # global 16 bit instruction
global INP

INP = []
ANS = []
ANS = [] # 16-bit instruction
VAR_S = {}  # "var_name": [addr(int in decimal starting from 0), val(int in decimal initially 0)]
LABEL_S = {}     # "label_name": [addr(int in decimal starting from 0)]
MEM_LINE = 0  # Mem occupied by instructions + variables 
CURR_LINE = 0 # current line in instruction 
TEST_NO = 0 # test number in instruction
TEMP = [0,0,0,0,0,0]    # [opcode, reg1, reg2, reg3, imm_val, mem_adr] 
REG_Names = {           # register key: Ri , value: register value
    "R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAGS":"111"
}
REG = [0,0,0,0,0,0,0,[0,0,0,0]]     # [R0, R1, ..., R6, [V,L,G,E]]
OPCODES = {             # operation code key:operation , value:[binarycode,type]
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
#=====================================================================================================================

def reset_temp():                   # resets the temprory starage list to [0,0,0,0,0]
    for i in range(len(TEMP)):
        TEMP[i] = 0
def reset_flags():                  # reset the flag list to [0,0,0,0]
    for i in range(0,4):
        REG[7][i] = 0
def instruction_type(instruction):  # fx to find the type of funciton from [A,B,C,D,E,F] with paramerter instruction
    is_reset_flag = False           # temprory reset flag
    reset_temp()                    # reset gloabal reset temp 
    op = instruction[0]             # function is op that is 1st element of instrction parameter list 
    if op in OPCODES:               # checking for instruction type
        op_code = OPCODES[op][0]    # op code is 
        op_type = OPCODES[op][1]
        TEMP[0] = op_code
    else:
        TEST_NO = 1
        op_error(CURR_LINE, TEST_NO, op)
        sys.exit()
    if(op=="mov"):
        if(len(instruction)>2 and instruction[2] in REG_Names): 
            TEMP[0] = "10011"
            op_type = "C"
        else:
            TEMP[0] = "10010"
            op_type = "B"
    if((op_type!="E" and op_code!="10011") or op_code=="11111"):
        is_reset_flag = True
        reset_flags()   # if it is not a jlt, jgt, je or mov Flags instr then reset flag register
    if(op_type=="B"): inst_B(instruction)
    if(op_type=="A"): inst_A(instruction)
    if(op_type=="C"): inst_C(instruction)
    if(op_type=="D"): inst_D(instruction)
    if(op_type=="F"): inst_F(instruction)
    if(op_type=="E"): inst_E(instruction)
    if(is_reset_flag==False):
        reset_flags()
 # fx for instruction type A to check for the type perform A type instructions [add ,sub,mul,xor,or,and]
def inst_A(instruction):
    if(len(instruction)!=4):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        improper_len_instr(CURR_LINE, TEST_NO, "A")
        sys.exit()
    reg2 = instruction[2] 
    reg1 = instruction[1] 
    reg3 = instruction[3] 
    verdict = val_reg([reg1, reg2, reg3], "A", REG_Names)
    if(verdict!=0):
        if(verdict==10):
            flags_invalid(CURR_LINE)
        else:
            invalid_reg(CURR_LINE, instruction[verdict])
        sys.exit()
    TEMP[2] = reg2
    TEMP[1] = reg1
    TEMP[3] = reg3
    if(TEMP[0]=="10000"):
        s = OPCODES["add"][0] + "00"
        s += REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
        res = REG[int(instruction[2][1:])] + REG[int(instruction[3][1:])]
        if(res>=(1<<16)):
            REG[int(instruction[1][1:])] = res%(1<<16)
            REG[-1][0] = 1
            
        else:
            REG[int(instruction[1][1:])] = res
        ANS.append(s)
    elif(TEMP[0]=="10001"):
        s = OPCODES["sub"][0] + "00"
        s += REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
        res = REG[int(instruction[2][1:])] - REG[int(instruction[3][1:])]
        if(res>=0):
            REG[int(instruction[1][1:])] = res
            
        else:
            REG[int(instruction[1][1:])] = 0
            REG[-1][0] = 1
        ANS.append(s)
    elif(TEMP[0]=="10110"):
        s = OPCODES["mul"][0] + "00"
        s += REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
        res = REG[int(instruction[2][1:])] * REG[int(instruction[3][1:])]
        if(res<(1<<16)):
            REG[int(instruction[1][1:])] = res
        else:
            REG[int(instruction[1][1:])] = res%(1<<16)
            REG[-1][0] = 1
            
        ANS.append(s)
    elif(TEMP[0]=="11010"):
        s = OPCODES["xor"][0] + "00"
        s += REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
        REG[int(instruction[1][1:])] =  REG[int(instruction[2][1:])] ^ REG[int(instruction[3][1:])]
        ANS.append(s)
    elif(TEMP[0]=="11011"):
        s = OPCODES["or"][0] + "00"
        s += REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
        REG[int(instruction[1][1:])] =  REG[int(instruction[2][1:])] | REG[int(instruction[3][1:])]
        ANS.append(s) 
    elif(TEMP[0]=="11100"):
        s = OPCODES["and"][0] + "00"
        s += REG_Names[instruction[1]] + REG_Names[instruction[2]] + REG_Names[instruction[3]]
        REG[int(instruction[1][1:])] =  REG[int(instruction[2][1:])] & REG[int(instruction[3][1:])]
        ANS.append(s)
 # fx for instruction type B to check for the type perform B type instructions [mov,ls,rs]
def inst_B(instruction):            
    if(len(instruction)!=3):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        improper_len_instr(CURR_LINE, TEST_NO, "B")
        sys.exit()
    reg1 = instruction[1] 
    imm_val = instruction[2] 
    verdict = val_reg([reg1, imm_val], "B", REG_Names)
    if(verdict!=0):
        if(verdict==1):
            invalid_reg(CURR_LINE, instruction[verdict])
        elif(verdict==2):
            invalid_imm(CURR_LINE, instruction[verdict])
        elif(verdict==10):
            flags_invalid(CURR_LINE)
        sys.exit()
    TEMP[4] = imm_val
    TEMP[1] = reg1
    
    if(TEMP[0]=="10010"):
        s = "10010" + REG_Names[instruction[1]]     
        s += dec_to_binary(int(instruction[2][1:]))
        REG[int(instruction[1][1:])] = int(instruction[2][1:])
        ANS.append(s)
    elif(TEMP[0]=="11000"):
        s = "11000" + REG_Names[instruction[1]]
        s += dec_to_binary(int(instruction[2][1:]))
        REG[int(instruction[1][1:])] = REG[int(instruction[1][1:])]>>int(instruction[2][1:])
        ANS.append(s)
    elif(TEMP[0]=="11001"):
        s = "11001" + REG_Names[instruction[1]]
        s += dec_to_binary(int(instruction[2][1:]))

        res = REG[int(instruction[1][1:])]<<min(16,int(instruction[2][1:]))
        if(res<(1<<16)):
            REG[int(instruction[1][1:])] = res
        else:
            
            REG[int(instruction[1][1:])] = res%(1<<16)
        ANS.append(s)
 # fx for instruction type C to check for the type perform C type instructions [mov,div,not,cmp]
def inst_C(instruction):
    if(len(instruction)!=3):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        improper_len_instr(CURR_LINE, TEST_NO, "C")
        sys.exit()
    reg2 = instruction[2] 
    reg1 = instruction[1] 
    
    verdict = val_reg([reg1, reg2], "C", REG_Names, {0:TEMP[0]})
    if(verdict!=0):
        if(verdict==10):
            flags_invalid(CURR_LINE)
        else:
            invalid_reg(CURR_LINE, instruction[verdict])
        sys.exit()
    TEMP[1] = reg1
    TEMP[2] = reg2 
    if(TEMP[0]=="10011"): 
        s="1001100000"
        s = s + REG_Names[instruction[1]] + REG_Names[instruction[2]]
        if(instruction[2]!="FLAGS"):
            REG[int(instruction[1][-1])] = REG[int(instruction[2][-1])]
            
        else:
            REG[int(instruction[1][-1])] = 1*REG[7][3] + 2*REG[7][2] + 4*REG[7][1] + 8*REG[7][0]
        ANS.append(s)
    elif(TEMP[0]=="10111"):
        s="1011100000"
        s = s + REG_Names[instruction[1]] + REG_Names[instruction[2]]
        REG[0] = REG[int(instruction[1][-1])] // REG[int(instruction[2][-1])]
        REG[1] = REG[int(instruction[1][-1])] % REG[int(instruction[2][-1])]
        ANS.append(s)
    elif(TEMP[0]=="11101"):
        s = "1110100000"
        s = s + REG_Names[instruction[1]] + REG_Names[instruction[2]]
        c = addr_to_bin(REG[int(instruction[2][-1])]) 
        c_c = ""
        for i in range(len(c)):
            if(c[i]=='0'):
                c_c+='1'
            else:
                c_c+='0'
        REG[int(instruction[1][-1])] = int(c_c, 2)
        ANS.append(s)
    elif(TEMP[0]=="11110"):
        s = "1111000000"
        s = s + REG_Names[instruction[1]] + REG_Names[instruction[2]]
        a = REG[int(instruction[1][-1])]
        b = REG[int(instruction[2][-1])]
        if(a>b):
            REG[7][2] = 1
        elif(a==b):
            REG[7][3] = 1
        else:
            REG[7][1] = 1
        ANS.append(s)
 # fx for instruction type D to check for the type perform D type instructions [ld,sd,]
def inst_D(instruction):
    if(len(instruction)!=3):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        improper_len_instr(CURR_LINE, TEST_NO, "D")
        sys.exit()
    reg1 = instruction[1] 
    mem_addr = instruction[2] 
    verdict = val_reg([reg1, mem_addr], "D", REG_Names, VAR_S)
    if(verdict!=0):
        if(verdict==1):
            invalid_reg(CURR_LINE, instruction[verdict])
        elif(verdict==2):
            TEST_NO = 0
            invalid_mem_addr(CURR_LINE, instruction[verdict], TEST_NO)
        elif(verdict==10):
            flags_invalid(CURR_LINE)
        sys.exit()
    TEMP[1] = reg1
    TEMP[5] = mem_addr
    if(TEMP[0]=="10100"):
        s = "10100"
        s = s + REG_Names[instruction[1]] + addr_to_bin(VAR_S[instruction[2]][0])
        REG[int(instruction[1][-1])] = VAR_S[instruction[2]][1]
        ANS.append(s)
    elif(TEMP[0]=="10101"):
        s = "10101"
        s = s + REG_Names[instruction[1]] + addr_to_bin(VAR_S[instruction[2]][0])
        VAR_S[instruction[2]][1] = REG[int(instruction[1][-1])]
        ANS.append(s)
 # fx for instruction type E to check for the type perform E type instructions [jmp,jlt,jgt,je]
def inst_E(instruction):
    if(len(instruction)!=2):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        improper_len_instr(CURR_LINE, TEST_NO, "E")
        sys.exit()
    mem_addr = instruction[1] 
    verdict = val_reg([mem_addr], "E", None, LABEL_S)
    if(verdict!=0):
        TEST_NO = 1
        invalid_mem_addr(CURR_LINE, instruction[verdict], TEST_NO)
        sys.exit()
    TEMP[5] = mem_addr
    if(TEMP[0]=="11111"):
        s = "11111000"
        s = s + addr_to_bin(LABEL_S[instruction[1]][0])
        ANS.append(s)
    elif(TEMP[0]=="01100"):
        s = "01100000"
        s = s + addr_to_bin(LABEL_S[instruction[1]][0])
        ANS.append(s)
    elif(TEMP[0]=="01101"):
        s = "01101000"
        s = s + addr_to_bin(LABEL_S[instruction[1]][0])
        ANS.append(s)
    elif(TEMP[0]=="01111"):
        s = "01111000"
        s = s + addr_to_bin(LABEL_S[instruction[1]][0])
        ANS.append(s)
 # fx for instruction type F to check for the type perform F type instructions [hlt]
def inst_F(instruction):
    if(len(instruction)!=1):
        for k, v in OPCODES.items():
            if v[0] == TEMP[0]:
                TEST_NO = k
                break
        improper_len_instr(CURR_LINE, TEST_NO, "F")
        sys.exit()
    if(TEMP[0]=="01010"):
        s = "0101000000000000"
        ANS.append(s)
#=====================================(print statement for all errors)================================================
# print statements for variable error
def variable_error(current_line, test_no, variable=None):  
    if(test_no==1):                        # 1 = variable iniitialization error
        print(f'''
        [ERROR] Invalid format for the variable initialization at the line no. {(current_line)}
        A Variable must be initialized in the format: var x''')

    elif(test_no==2):                      # 2 = alphanumeric invalid 
        print(f''' 
        [ERROR] {variable} is an invalid variable name at the line no. {(current_line)} 
        A Variable name must consists of alphanumeric characters and underscores only.''')

    elif(test_no==3):                      # 3 = in invalid variablename  
        print(f'''
        [ERROR] {variable} is an invalid variable name at the line no. {(current_line)}
        A Variable name must not be an instruction.''')

    elif(test_no==4):                      # 4 = invalid variable name registers 
        print(f'''
        [ERROR] {variable} is an invalid variable name at the line no. {(current_line)}
        A Variable name must not be a register.''')

    elif(test_no==5):                      #  5 = repetition of variable definition
        print(f'''
        [ERROR] {variable} is redefined at the line no. {(current_line)}
        A Variable name must be initialized once.''')

    elif(test_no==6):                      # 6 = all vars must be initialized at beginning
        print(f'''[ERROR] Invalid initialization of the variable at the line no. {current_line}
        All the variables must be initialized at the beginning of program.''')
 # print statements for label error
def label_error(current_line, test_no, Label=None):       

    if(test_no==2):                         # 2 = alphanumeric invalid
        print(f'''
        [ERROR] {Label} is an invalid label name at the line no. {(current_line)}
        A Label name must consists of alphanumeric characters and underscores only.''')
    
    elif(test_no==3):                       # 3 = in invalid labelname
        print(f'''
        [ERROR] {Label} is an invalid label name at the line no. {(current_line)}
        A Label name must not be an instruction.''')
    
    elif(test_no==4):                       # 4 = invalid label name registers
        print(f'''
        [ERROR] {Label} is an invalid label name at the line no. {(current_line)}
        A Label name must not be a register.''')
    
    elif(test_no==5):                       # 5 = repetition of label definition 
        print(f'''
        [ERROR] {Label} is redefined at the line no. {current_line}
        A Label name must be defined once.''')
    
    elif(test_no==6):                       # 6 = label is variable
        print(f'''
        [ERROR] {Label} is an invalid label name at the line no. {current_line}
        A Label name must not be a variable.''')
    
    elif(test_no==7):                       # 7 = label must be followed by instruction
        print(f'''
        [ERROR] {Label} is an invalid label name initialization at the line no. {(current_line)}
        A Label name must be followed by an instruction.''')
 # print statement for memory overflow
def mem_over_flow():                                        
    print('''
    [ERROR] Memory Overflow.
    Total number of instructions and variables must not exceed memory length i.e. 256''')
 # print statements for halt error
def hlt_error(current_line, test_no):                       
    if(test_no==1):                       # 1 = halt not last instuction
        print('''
        [ERROR] Program doesn't have any halt instruction at the end.
        Insert a hlt instruction at the end of the program.''')   

    elif(test_no==2):                     # 2 = more than one halt intruction
        print(f'''
        [ERROR] Program has more than one halt instruction at the line no.{(current_line)} 
        Use only one hlt instruction which is to be at the end of the program.''')   
 # print statement for op error
def op_error(current_line, test_no, op):                  

    if(test_no==1):                        # 1 = invalid instruction
        print(f"[ERROR] {op} is not a valid instruction at the line no. {(current_line)}")
 # print statement for improper length of instruction
def improper_len_instr(current_line, instruction_name,instruction_type ):
    print(f'''
    [ERROR] Syntax error at the line no. {(current_line)} 
    {instruction_name} is a type-{instruction_type} instruction.''')
 # print statement for invalid register
def invalid_reg(current_line, name):                       
    print(f"[ERROR] {name} is an invalid register at the line no. {current_line}")
 # print statement for an invalid immediate
def invalid_imm(current_line, imm):                        

    print(f'''
    [ERROR] {imm} is an invalid immediate at the line no. {current_line} 
    Immediate value must be an integer between 0 and 255 (both including).''')
 # print statement for invalid memory adress of labels and variable
def invalid_mem_addr(current_line, mem_addr, test_no):     
    
    if(test_no==0):                         # 0 = variable 
        print(f'''
        [ERROR] {mem_addr} is an undefined variable name at the line no. {current_line} 
        Variable name must be initialized first before using it.''')
    else:                                   # 1 = label
        print(f'''
        [ERROR] {mem_addr} is an undefined label name at the line no. {current_line}
        Label name must be defined first before using it.''')
 # illegal use of flag
def flags_invalid(line):                                  
    print(f"[ERROR] Illegal use of FLAGS register at the line no. {line}")

#====================================================(error tests)==================================================
 # check for valid variable name
def valid_var_name(name, var_dict, reg_dict, opcodes):
    if(not(name.replace('_', '').isalnum() or set(name)=={'_'}) or name.isnumeric()):
        return 2
    elif(name in opcodes.keys()):
        return 3
    elif(name in reg_dict.keys()):
        return 4
    elif(name in var_dict.keys()):
        return 5
    else:
        return 1    
 # check for valid label name
def valid_label_name(name, var_dict, label_dict, reg_dict, opcodes):
    if(not(name.replace('_', '').isalnum() or set(name)=={'_'}) or name.isnumeric()):
        return 2
    elif(name in opcodes.keys()):
        return 3
    elif(name in reg_dict.keys()):
        return 4
    elif(name in label_dict.keys()):
        return 5
    elif(name in var_dict.keys()):
        return 6
    else:
        return 1
 # fx to change decimal numbers to binary 8 bit code
def dec_to_binary(n):
    binary = ""        
    for i in range(0,8):
        binary=str(n & 1)+binary
        n=n>>1
    s='0'*max(0,8-len(binary))+binary
    return s
 # fx to change address to binary 8 bit code
def addr_to_bin(x):
    t = bin(x)
    t = t[2:]
    t = t[-8:]
    if(len(t)!=8):
        t = '0'*(8-len(t))+t
    return t
 # fx to create dictionary of variables
def val_reg(list_reg, type_instr, reg_names, var_label_dict=None):
    
    if(type_instr=="B"):
        if(list_reg[0] not in reg_names):
            return 1
        elif(list_reg[0] == "FLAGS"):
            return 10
        elif(int(list_reg[1][1:])>255 or int(list_reg[1][1:])<0):
            return 2
        else:
            return 0
    elif(type_instr=="A"):
        for i in range(0,len(list_reg)):
            if(list_reg[i] == "FLAGS"):
                return 10
            elif(list_reg[i] not in reg_names):
                return i+1
        return 0
    elif(type_instr=="C"):
        for i in range(len(list_reg)):
            if(list_reg[i] not in reg_names):
                return i+1
            
        if(list_reg[1] == "FLAGS" and var_label_dict[0]!="10011"):
            return 10
        elif(list_reg[0] == "FLAGS"):
            return 10
        else:
            return 0
    elif(type_instr=="D"):
        if(list_reg[0] not in reg_names):
            return 1
        elif(list_reg[0] == "FLAGS"):
            return 10
        elif(list_reg[1] not in var_label_dict.keys()):
            return 2
        else:
            return 0
    elif(type_instr=="E"):
        if(list_reg[0] not in var_label_dict.keys()):
            return 1
        return 0
    else:
        return 0
#=====================================================================================================================

 # input using the terminal
while(True):
    try:
        curr_instr = input().strip()
        curr_instr = str(re.sub(' +', ' ', curr_instr))
        INP.append(curr_instr)
    except EOFError:
        break
CURR_LINE = 1
TEST_NO = None
# VAR STORING
while(CURR_LINE <= len(INP)):
    if(INP[CURR_LINE-1]==""):
        CURR_LINE += 1
    elif(INP[CURR_LINE-1].split()[0]=="var"):
        if(len(INP[CURR_LINE-1].split()) != 2):
            TEST_NO = 1
            variable_error(CURR_LINE, TEST_NO)
            exit()
        else:
            myVar = INP[CURR_LINE-1].split()[1]
            # check_valid_var_name() along with not in instr or reg or redefinition
            verdict = valid_var_name(myVar, VAR_S, REG_Names, OPCODES)
            if(verdict!=1):
                TEST_NO = verdict
                variable_error(CURR_LINE, TEST_NO, myVar)
                exit()
            VAR_S[myVar] = [None, 0]
            CURR_LINE += 1
    else:
        break
MEM_LINE = 0
# Label Storing with address
while(CURR_LINE <= len(INP)):
    if(INP[CURR_LINE-1]==""):
        CURR_LINE += 1
        continue
    if(INP[CURR_LINE-1].split()[0][-1:]==":"):
        # check_valid_label_name() along with not in instruction or reg or redefinition
        myLabel = INP[CURR_LINE-1].split()[0][:-1]
        verdict = valid_label_name(myLabel, VAR_S, LABEL_S, REG_Names, OPCODES)
        if(verdict != 1):
            TEST_NO = verdict
            label_error(CURR_LINE, TEST_NO, myLabel)
            exit()
        if(len(INP[CURR_LINE-1].split())==1):
            TEST_NO = 7
            label_error(CURR_LINE, TEST_NO, myLabel)
            exit()
        LABEL_S[myLabel] = [MEM_LINE]
        MEM_LINE += 1
    elif(INP[CURR_LINE-1].split()[0]=="var"):
        TEST_NO = 6
        variable_error(CURR_LINE, TEST_NO)
        exit()
    elif(INP[CURR_LINE-1]!=""):
        MEM_LINE += 1
    CURR_LINE += 1
# Assign address to variables
for v in VAR_S:
    VAR_S[v][0] = MEM_LINE
    MEM_LINE += 1
# Check Memory Overflow
if(MEM_LINE>=257):
    mem_over_flow()
    exit()
# Check last instruction is hlt or not and how many hlt instructions
CURR_LINE = len(INP)
hlt_count = 0
while(CURR_LINE>=1):
    if(INP[CURR_LINE-1]!=""):
        if(INP[CURR_LINE-1].split()[0]=="hlt" or (INP[CURR_LINE-1].split()[0][-1]==":" and INP[CURR_LINE-1].split()[1]=="hlt")):
            hlt_count += 1 
        if(hlt_count==0):
            TEST_NO = 1
            hlt_error(CURR_LINE, TEST_NO)
            exit()
    if(hlt_count>1):
        TEST_NO = 2
        hlt_error(CURR_LINE, TEST_NO)
        exit()
    CURR_LINE -= 1
CURR_LINE = 1
# Start executing the assembly code
while(CURR_LINE<=len(INP)):
    if(INP[CURR_LINE-1]==""):
        CURR_LINE += 1
        continue
    myInstr = INP[CURR_LINE-1].split()
    if(myInstr[0]=="var"):
        CURR_LINE += 1
        continue
    if(myInstr[0][-1]==":"):
        myInstr = myInstr[1:]
    instruction_type(myInstr)
    CURR_LINE += 1
# output to the terminal
for i in ANS:
    print(i)

#====================================================================================================================
