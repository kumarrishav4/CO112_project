# def bin(num,j):
#     st=''
#     for i in range(j):
#         a=num%2
#         num=num//2
#         st+=str(a)
#     return st[::-1]
    
    
def reg(r):
    d={'r0':'000','r1':'001','r2':'010','r3':'011','r4':'100','r5':'101','r6':'110'}
    return d[r]


# def movim(r,im):
#     ans='10010'
#     if(r==''):
#         return f'{r} is invalid'
#     ans+=reg(r)+bin(int(im[1:]),6)
        
#     print('NO')
#     return ans

# def mul(r1,r2,r3):
#     if(r1==''):
#         return f'{r1} is invalid'
#     elif(r2==''):
#         return f'{r2} is invalid'
#     elif(r3==''):
#         return f'{r3} is invalid'
#     ans='1011000'
#     ans+=reg(r1)+reg(r2)+reg(r3)
#     return ans

# def add(r1,r2,r3):
#     if(r1==''):
#         return f'{r1} is invalid'
#     elif(r2==''):
#         return f'{r2} is invalid'
#     elif(r3==''):
#         return f'{r3} is invalid'
#     ans='1000000'
#     ans+=reg(r1)+reg(r2)+reg(r3)
#     return ans
    
# def sub(r1,r2,r3):
#     ans='1000100'
#     ans+=reg(r1)+reg(r2)+reg(r3)
#     return ans

# def movrg(r1,r2):
#     ans='1001100000'
#     ans+=reg(r1)+reg(r2)
#     return ans

# def halt():
#     return '0101000000000000'

# def load(r1, mem):
#     ans='10100'
#     ans+=reg(r1)+str(mem)
#     return ans
print("hello world")
# def st(r1,mem):
#     ans='10101'
#     ans+=reg(r1)+str(mem)
#     return ans

# def dv(r1,r2):
#     ans='1011100000'
#     ans+=reg(r1)+reg(r2)
#     return ans

# def rshift(r1,im):
#     ans='11000'
#     ans+=reg(r1)+bin(int(im[1:]),6)
#     return ans

# def lshift(r1,im):
#     ans='11001'
#     ans+=reg(r1)+bin(int(im[1:]),6)
#     return ans

    
# def XOR(r1,r2,r3):
#     ans='1101000'
#     ans+=reg(r1)+ reg(r2)+ reg(r3)
#     return ans

# def OR(r1,r2,r3):
#     ans='1101100'
#     ans+= reg(r1)+ reg(r2) + reg(r3)
#     return ans


# def And(r1,r2,r3):
#     ans='1110000'
#     ans+= reg(r1)+ reg(r2) + reg(r3)
#     return ans


# def Invert(r1,r2):
#     ans='1110100000'
#     ans+= reg(r1) + reg(r2)
#     return ans



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


def tya(op,r1,r2,r3):
    if(r1==''):
        return f'{r1} is invalid'
    elif(r2==''):
        return f'{r2} is invalid'
    elif(r3==''):
        return f'{r2} is invalid'
    else:
        ans=opcodes[op][0]+'00'+reg(r1)+reg(r2)+reg(r3)
        return ans
    
def tyb(op,r1,imm):
    if( imm<0 or imm>255):
        
        return f'{imm} is out of range'
    if(r1==''):
        return f'{r1} is invalid'
    else:
        if(op in OPCODES.keys()):
            ans=OPCODES[op][0] + reg(r1) + bin(imm)
            return ans
        else:
            return f'{op} is invalid'


def tyc(op,r1,r2):
    if(r1==''):
        return f'{r1} is invalid'
    elif(r2==''):
        return f'{r2} is invalid'
    else:
        ans= OPCODES[op][0] + '00000' + reg(r1) + reg(r2) 
        return ans
        
        
def call(cmd):
    if(cmd=="A"):
        tya
