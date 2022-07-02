def bin(num,j):
    st=''
    for i in range(j):
        a=num%2
        num=num//2
        st+=str(a)
    return st[::-1]
    
    



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

def reg(r):
    try:
        d={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110'}
        return d[r]
    except KeyError:
        return ''


opcodes = {
    "add": ["10000", "A"],
    "sub": ["10001", "A"],
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
tybopcodes = {
    "mov": ["10010", "B"],
    "rs": ["11000", "B"],
    "ls": ["11001", "B"]
}


def tya(op,r1,r2,r3):
    if(reg(r1)==''):
        return f'{r1} is invalid'
    elif(reg(r2)==''):
        return f'{r2} is invalid'
    elif(reg(r3)==''):
        return f'{r3} is invalid'
    else:
        ans=opcodes[op][0]+'00'+reg(r1)+reg(r2)+reg(r3)
        return ans
        
        
def tyb(op,r1,imm):
    if(int(imm[1:])>255):
        return f'{imm[1:]} is out of range'
    if(reg(r1)==''):
        return f'{r1} is invalid'
    else:
        ans=tybopcodes[op][0] + reg(r1) + bin(int(imm[1:]),8)
        return ans
    
def tyc(op,r1,r2):
    if(reg(r1)==''):
        return f'{r1} is invalid'
    elif(reg(r2)==''):
        return f'{r2} is invalid'
    else:
        ans= opcodes[op][0] + '00000' + reg(r1) + reg(r2) 
        return ans
    
print(tyc('mov', 'R1', '$10'))