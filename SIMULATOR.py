import sys
import math
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt



array=[] #stores stdin

yaxis=[] #stores pc when accessed
xaxis=[] #storing the cycle no.


def memory(pc):
    global array

    return array[pc]

reg={"R0":0,"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0,"FLAGS":0} #stores the value of registers

def rf(R):  #Register File
    global reg
    return reg[R]

# def GNR(code): #Give Register Name
#     nameR={"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS"}
#     return nameR[code]

GNR={"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS"}

def checkResult(result):  #For overloading in add,div,sub
    global reg
    if result>256:
        reg["FLAGS"]=8
        return 255
    elif result<0:
        reg["FLAGS"]=8
        return 0
    else:
        reg["FLAGS"]=0
        return result

# def cto16bin(z):   #Converting to 16bin
#     bnr=bin(z).replace('0b','')    
  
#     x = bnr[::-1]
#     while len(x) < 16:
#         x += '0'
#     bnr = x[::-1]
#     return bnr

# def cto8bin(z):  #Converting to 8bin
#     bnr=bin(z).replace('0b','')    
  
#     x = bnr[::-1]
#     while len(x) < 8:
#         x += '0'
#     bnr = x[::-1]
#     return bnr

def ctb(z,n):
    bnr=bin(z).replace('0b','')    
  
    x = bnr[::-1]
    while len(x) < n:
        x += '0'
    bnr = x[::-1]
    return bnr


def ctoint(z):  #Converting to INT

    c_table = {"0": 0, "1":1,"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "A":10 , 'B':11, 'C':12, 'D':13, 'E':14 , 'F': 15}
    
    decimal = 0

    power = len(z) -1
    for i in z:
        decimal += c_table[i]2*power
        power -= 1
    return decimal


#main function

nextpc=0 #next value of Program Counter
haltValue=True #halt variable
cycleno=0 #cycle no

    
def main():
    global yaxis
    global array
    global haltValue
    global nextpc
    global xaxis
    global cycleno
  
    array=sys.stdin.read().splitlines()
    

    pc=0 #Program counter


    while(haltValue and pc<len(array)):
        
        EE(pc)

        # yaxis.append(pc)
        # xaxis.append(cycleno)

        BinPC= ctb(pc,8)

        BinR0= ctb(reg["R0"],16)
        BinR1= ctb(reg["R1"],16)
        BinR2= ctb(reg["R2"],16)
        BinR3= ctb(reg["R3"],16)
        BinR4= ctb(reg["R4"],16)
        BinR5= ctb(reg["R5"],16)
        BinR6= ctb(reg["R6"],16)
        BinFLAGS= ctb(reg["FLAGS"],16)

        print(f"{BinPC} {BinR0} {BinR1} {BinR2} {BinR3} {BinR4} {BinR5} {BinR6} {BinFLAGS}")
        
        pc=nextpc
        cycleno=cycleno+1
        
    for k in array:
        print(k)
    for j in vararr:
        print(ctb(variable[j],16))
    
    i=0
    while(i<(256-len(array)-len(vararr))):
        print("0000000000000000")
        i+=1
    
        

variable={}     #to store memory address of variables
vararr=[]

def add(inst):
	
    register=GNR[(inst[7:10])]
    o1=GNR[(inst[10:13])]
    o2=GNR[(inst[13:16])]
    result = rf(o1) + rf(o2)
    reg[register]=checkResult(result)

def halt():
	haltValue=False
 
def je(inst):
    flagval=reg["FLAGS"]
    if flagval==1:
        nextpc=ctoint(inst[8:16])
    reg["FLAGS"]=0
    
def jgt(inst):
    flagval=reg["FLAGS"]
    if flagval==2:
        nextpc=ctoint(inst[8:16])
    reg["FLAGS"]=0
    
def jlt(inst):
    flagval=reg["FLAGS"]
    if flagval==4:
        nextpc=ctoint(inst[8:16])
    reg["FLAGS"]=0
    
def j(inst):
    nextpc=ctoint(inst[8:16])
    reg["FLAGS"]=0
    
def cmp(inst):
    o1=rf(GNR[(inst[10:13])])
        
    o2=rf(GNR[(inst[13:16])])
    
    
    if o1>o2:
        reg["FLAGS"]=2
    elif o1==o2:
        reg["FLAGS"]=1
    else:
        reg["FLAGS"]=4
        
def sub(inst):
        register=GNR[(inst[7:10])]
        o1=GNR[(inst[10:13])]
        o2=GNR[(inst[13:16])]
        result = rf(o1) - rf(o2)
        reg[register]=checkResult(result)
def mov_imm(inst):
        register=GNR[(inst[5:8])]
        imm=ctoint(inst[8:16])
        
        reg[register]=imm    #wrong
        
        reg["FLAGS"]=0
def mov_reg(inst):
        register=GNR[(inst[10:13])]
        
        o1=GNR[(inst[13:16])]
        
        reg[register]=rf(o1)
        reg["FLAGS"]=0
def load(inst):
        register=GNR[(inst[5:8])]
        value=variable[inst[8:16]]
        reg[register]=value
        reg["FLAGS"]=0
        yaxis.append(ctoint(inst[8:16]))
        xaxis.append(cycleno)
        
def inv(inst):
    register=GNR[(inst[10:13])]
    o1 = str(inst[13:16])
    result = ""
    for i in o1:
        if i!="0":
            result=result+'0'
        else:
            result=result+'1'
    result=int(result)
    reg[register]=ctoint(result)
    reg["FLAGS"]=0
        
def andd(inst):
    register=GNR[(inst[7:10])]
    o1=GNR[(inst[10:13])]
    o2=GNR[(inst[13:16])]
    result = rf(o1) & rf(o2)
    reg[register]=result
    reg["FLAGS"]=0
    
def orr(inst):
    register=GNR[(inst[7:10])]
    o1=GNR[(inst[10:13])]
    o2=GNR[(inst[13:16])]
    result = rf(o1) | rf(o2)
    reg[register]=result
    reg["FLAGS"]=0
    
def xor(inst):
    register=GNR[(inst[7:10])]
    o1=GNR[(inst[10:13])]
    o2=GNR[(inst[13:16])]
    result = rf(o1) ^ rf(o2)
    reg[register]=result
    reg["FLAGS"]=0
    
def ls(inst):
    register=GNR[(inst[5:8])]
    imm=ctoint(inst[8:16])
    result=reg[register]<<imm
    result=ctb(result,16)
    convertedResult=result[-8:]
    reg[register]=ctoint(convertedResult)
    reg["FLAGS"]=0
    
def st(inst):
    register=GNR[(inst[5:8])]
    variable[inst[8:16]]=rf(register)
    vararr.append(inst[8:16])
    reg["FLAGS"]=0
    yaxis.append(ctoint(inst[8:16]))
    xaxis.append(cycleno)

def mul(inst):
    register=GNR[(inst[7:10])]
    o1=GNR[(inst[10:13])]
    o2=GNR[(inst[13:16])]
    result = rf(o1) * rf(o2)
    reg[register]=checkResult(result)
def load(inst):
    register=GNR[(inst[5:8])]
    variable[inst[8:16]]=rf(register)
    vararr.append(inst[8:16])
    reg["FLAGS"]=0
    yaxis.append(ctoint(inst[8:16]))
    xaxis.append(cycleno)
def rs(inst):

    o1=rf(GNR[(inst[10:13])])
    o2=rf(GNR[(inst[13:16])])
    reg["R0"]=o1/o2
    reg["R1"]=o1%o2
    reg["FLAGS"]=0
    
def div(inst):

    o1=rf(GNR[(inst[10:13])])
    o2=rf(GNR[(inst[13:16])])
    reg["R0"]=o1/o2
    reg["R1"]=o1%o2
    reg["FLAGS"]=0

def EE(pc):

    global nextpc
    global haltValue
    global variable
    global reg
    global vararr
    global xaxis
    global yaxis
    global cycleno

    inst=memory(pc)                           #instruction to be executed
    nextpc=pc+1                               #nextpc

    
    #halt    
    if inst[:5]=="01010":
        halt()

     #Add
    elif inst[:5]=="10000":
        add(inst)
    
    #Subtract
    elif inst[:5]=="10001":
        sub(inst)


    #Move Immediate
    elif inst[:5]=="10010":
        mov_imm(inst)

    #Move Register
    elif inst[:5]=="10011":
        mov_reg(inst)
    #Load
    elif inst[:5]=="10100":
        load(inst)    
    #Store
    elif inst[:5]=="10101":
        st(inst)
        

    #Multiply
    elif inst[:5]=="10110":
        mul(inst)
    #Divide
    elif inst[:5]=="10111":
        div(inst)
    #RightShift
    elif inst[:5]=="11000":
        rs(inst)

    #LeftShift
    elif inst[:5]=="11001":

        ls(inst)

    #ExclusiveOr
    elif inst[:5]=="11010":
        xor(inst)
        

    #Or
    elif inst[:5]=="11011":

        orr(inst)

    #And
    elif inst[:5]=="11100":

        andd(inst)

    #Invert
    elif inst[:5]=="11101":

        inv(inst)

    #Compare    
    elif inst[:5]=="11110":

        cmp(inst)

    #Unconditional Jump
    elif inst[:5]=="11111":

        j(inst)

    #Jump if less than
    elif inst[:5]=="01100":
        
        jlt(inst)

    #Jump if  than greater than
    elif inst[:5]=="01101":
        
        jgt(inst)

    #Jump if equal
    elif inst[:5]=="01111":
        
        je(inst)

main()
