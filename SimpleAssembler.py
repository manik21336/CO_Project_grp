
from sys import stdin, stdout

# def binary(string): # should convert the string of number(decimal) into binary (8 bits) and return it as string
#     return string;

def binary(num): # to convert int int into 8 bits binary
    num=int(num);
    code=[0,0,0,0,0,0,0,0];
    
    i=-1;
    while num>0:
        code[i]= num%2;
        num=num//2;
        i-=1;
    
    code=[str(x) for x in code];
    return ("".join(code));

def assemble (line):
    code=[0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]

    # encoding opcode
    for i in range(0,5):
        code[i]= int(opcode[line[0]][i])
    
    # Type A
    if (line[0]=="add" or line[0]=="sub" or line[0]=="mul" or line[0]=="xor" or line[0]=="or" or line[0]=="and") :
        for i in range(7,10):
            code[i]= int(rega[line[1]] [i-7]);
        for i in range(10,13):
            code[i]= int(rega[line[2]] [i-10]);
        for i in range(13,16):
            code[i]= int(rega[line[3]] [i-13]);
        return code;

    # Type B
    elif ((line[0]=="mov" and line[2][0]=="$") or line[0]=="rs" or line[0]=="ls"):
        for i in range(5,8):
            code[i]= int(rega[line[1]] [i-5]);
        num=binary(line[2][1::]);
        for i in range(8,16):
            code[i]= int(num[i-8]);
        return code;

    # Type C
    elif (line[0]=="not" or line[0]=="cmp" or line[0]=="div"):
        for i in range(10,13):
            code[i]= int(rega[line[1]] [i-10]);
        for i in range(13,16):
            code[i]= int(rega[line[2]] [i-13]);
        return code;
    
    elif (line[0]=="mov" and line[2][0]!="$"):
        for i in range(0,5):
            code[i]= int(opcode["movr"][i])
        for i in range(5,8):
            code[i]= int(rega[line[1]] [i-5]);
        for i in range(8,16):
            code[i]= int(rega[line[2]] [i-8]);
        return code;
    
    # Type D
    elif (line[0]=="ld" or line[0]=="st"):
        for i in range(5,8):
            code[i]= int(rega[line[1]] [i-5]);
        for i in range(8,16):
            code[i]=int(binary(vars_d[line[2]])[i-8]);
        return code;
    
    # Type E
    elif (line[0]=="jmp" or line[0]=="jlt" or line[0]=="jgt" or line[0]=="je"):
        for i in range(8,16):
            code[i]=int(binary(labels[line[2]])[i-8])
        return code;
    
    # Type F
    elif (line[0]=="hlt"):
        return code;
                    
# main
bin=[]
opcode= {"add":"10000",  "sub":"10001", "mov" :"10010", "movr":"10011",
         "ld" :"10100",  "st" :"10101", "mul" :"10110", "div" :"10111",
         "rs" :"11000",  "ls" :"11001", "xor" :"11010", "or"  :"11011",
         "and":"11100",  "not":"11101", "cmp" :"11110", "jmp" :"11111",
         "jlt":"01100",  "jgt":"01101", "je"  :"01111", "hlt" :"01010" }
        
#reg addresses
rega= {"R0":"000", "R1":"001", "R2":"010", "R3":"011",
       "R4":"100", "R5":"101", "R6":"110" }

#reg values
regv={"R0":0, "R1":0, "R2":0, "R3":0, "R4":0, "R5":0, "R6":0}


assembly=[]; # to store assembly instructions
labels={}; #to store labels
vars=[];

# Taking inputs:
i=0;
for instruction in stdin:
    if instruction=="\n":
        continue;
    line= instruction.rstrip().split();
    
    if line[0][-1]==":":  # for label
        l=len(line[0]);
        labels[line[0][0:l-1]]=i;
        assembly.append(line[1::]);

    elif line[0]=="var":
        vars.append(line[1]);

    else:
        assembly.append(line);

    i+=1;
    if ("hlt" == line[0]):
        break

l=len(assembly);
vars_d={};
j=0;
for i in range (len(vars)):
    vars_d[vars[i]]=l+j;
    j+=1;

output=[];
for line in assembly:
    output.append(assemble(line));
    # stdout.write(assemble(line));

for line in output:
    line=[str(x) for x in line];
    stdout.write(''.join(line)+'\n');


# what is left?
# write a function to convert decimal to binary in 8 bits
# handling labels
# handling "var xyz" instructions
# handling flags and instruction "mov reg1 FLAGS"
# handling errors (false instructions)
