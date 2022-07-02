def variable_error(current_line, test_no, variable=None):  # print statements for variable error

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

def label_error(current_line, test_no, Label=None):        # print statements for label error

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

def mem_over_flow():                                       # print statement for memory overflow 
    print('''
    [ERROR] Memory Overflow.
    Total number of instructions and variables must not exceed memory length i.e. 256''')
    
def hlt_error(current_line, test_no):                      # print statements for halt error 
    if(test_no==1):                       # 1 = halt not last instuction
        print('''
        [ERROR] Program doesn't have any halt instruction at the end.
        Insert a hlt instruction at the end of the program.''')   

    elif(test_no==2):                     # 2 = more than one halt intruction
        print(f'''
        [ERROR] Program has more than one halt instruction at the line no.{(current_line)} 
        Use only one hlt instruction which is to be at the end of the program.''')   

def op_error(current_line, test_no, op):                   # print statement for op error

    if(test_no==1):                        # 1 = invalid instruction
        print(f"[ERROR] {op} is not a valid instruction at the line no. {(current_line)}")

def improper_len_instr(current_line, instruction_name,instruction_type ): # print statement for improper length of instruction
    print(f'''
    [ERROR] Syntax error at the line no. {(current_line)} 
    {instruction_name} is a type-{instruction_type} instruction.''')

def invalid_reg(current_line, name):                       # print statement for invalid register 
    print(f"[ERROR] {name} is an invalid register at the line no. {current_line}")

def invalid_imm(current_line, imm):                        # print statement for an invalid immediate

    print(f'''
    [ERROR] {str(imm)} is an invalid immediate at the line no. {(current_line)} 
    Immediate value must be an integer between 0 and 255 (both including).''')

def invalid_mem_addr(current_line, mem_addr, test_no):     # print statement for invalid memory adress of labels and variable
    
    if(test_no==0):                         # 0 = variable 
        print(f'''
        [ERROR] {mem_addr} is an undefined variable name at the line no. {current_line} 
        Variable name must be initialized first before using it.''')
    else:                                   # 1 = label
        print(f'''
        [ERROR] {mem_addr} is an undefined label name at the line no. {line}
        Label name must be defined first before using it.''')

def flags_invalid(line):                                   # illegal use of flag
    print(f"[ERROR] Illegal use of FLAGS register at the line no. {line}")
