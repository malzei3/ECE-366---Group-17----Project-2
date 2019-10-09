# Author: Trung Le
# Supported instrs: 
# addi, sub, beq, ori, sw

# Remember where each of the jump label is, and the target location 
def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')


def mipsToBin():
    labelIndex = []
    labelName = []

    f = open("mc.asm","w+")

    h = open("prog.asm","r")
    asm = h.readlines()
    line_count = 0

    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName) # Save all jump's destinations
    
    for line in asm:
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0

        #----------------------------------------------------- ADDIU    addiu $t, $s, imm     0010 01ss ssst tttt iiii iiii iiii iiii
        if(line[0:5] == "addiu"): 
            line = line.replace("addiu","")
            line = line.split(",")
            imm = format(int(line[2]),'016b')  if (int(line[2]) > 0) else format(65536 + int(line[2]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            f.write(str('001001') + str(rs) + str(rt) + str(imm) + '\n')
            line_count += 1

        elif(line[0:4] == "addi"): # ADDI      addi $t, $s, imm  	   0010 00ss ssst tttt iiii iiii iiii iiii
            line = line.replace("addi","")
            line = line.split(",")
            imm = format(int(line[2]),'016b') if (int(line[2]) > 0) else format(65536 + int(line[2]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            f.write(str('001000') + str(rs) + str(rt) + str(imm) + '\n')
            line_count += 1

        elif(line[0:3] == "add"): # ADD      add $d, $s, $t     0000 00ss ssst tttt dddd d000 0010 0000
            line = line.replace("add","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000') + '\n')
            line_count += 1

         #----------------------------------------------------- multu    multu $s, $t     0000 00ss ssst tttt 0000 0000 0001 1001      
        elif(line[0:5] == "multu"): 
            line = line.replace("multu","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000011001') + '\n')
            line_count += 1

        #----------------------------------------------------- MULT      mult $s, $t      0000 00ss ssst tttt 0000 0000 0001 1000
        elif(line[0:4] == "mult"): 
            line = line.replace("mult","")
            line = line.split(",")
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000011000') + '\n')
            line_count += 1

         #----------------------------------------------------- srl $d, $t, h        0000 00-- ---t tttt dddd dhhh hh00 0010
        elif(line[0:3] == "srl"):
            line = line.replace("srl","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            sh = format(int(line[2]),'05b')
            f.write(str('00000000000') + str(rt) + str(rd) + str(sh) + str('000010') + '\n')
            line_count += 1

         #----------------------------------------------------- lb         lb $t, offset($s)       1000 00ss ssst tttt iiii iiii iiii iiii  
        elif(line[0:2] == "lb"): # lb         lb $t, offset($s)       1000 00ss ssst tttt iiii iiii iiii iiii  
            line = line.replace("lb","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            line = line[1]
            line = line.split("(")
            line[1] = line[1].replace(")", "")
            rs = format(int(line[1]),'05b') 
            imm = format(int(line[0]),'016b')
            f.write(str('100000') + str(rs) + str(rt) + str(imm) + '\n')
            line_count += 1

         # ----------------------------------------------------- sb         sb $t, offset($s)      1010 00ss ssst tttt iiii iiii iiii iiii
        elif(line[0:2] == "sb"): 
            line = line.replace("sb","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            line = line[1]
            line = line.split("(")
            line[1] = line[1].replace(")", "")
            rs = format(int(line[1]),'05b')
            imm = format(int(line[0]),'016b')
            f.write(str('101000') + str(rs) + str(rt) + str(imm) + '\n')
            line_count += 1

        # ------------------------------------------------------- lw         lw $t, offset($s)       1000 11ss ssst tttt iiii iiii iiii iiii
        elif(line[0:2] == "lw"): 
            line = line.replace("lw", "")
            line = line.split(",")
            rt = format(int(line[0]), '05b')
            line = line[1]
            line = line.split("(")
            line[1] = line[1].replace(")", "")
            rs = format(int(line[1]),'05b')
            imm = format(int(line[0]),'016b')
            f.write(str('100011') + str(rs) + str(rt) + str(imm) + '\n')
            line_count += 1

         # ------------------------------------------------------ sw          sb $t, offset($s)       1010 11ss ssst tttt iiii iiii iiii iiii
        elif(line[0:2] == "sw"):
            line = line.replace("sw","")
            line = line.split(",")
            rt = format(int(line[0]),'05b')
            line = line[1]
            line = line.split("(")
            line[1] = line[1].replace(")", "")
            rs = format(int(line[1]),'05b')
            imm = format(int(line[0]),'016b')
            f.write(str('101011') + str(rs) + str(rt) + str(imm) + '\n')
            line_count += 1

        # ------------------------------------------------------ beq        beq $s, $t, offset       0001 00ss ssst tttt iiii iiii iiii iiii
        elif(line[0:3] == "beq"): 
            line = line.replace("beq","")
            line = line.split(",")
            for i in range(len(labelName)):
                if (labelName[i] == line[2]):
                    imm_dest = format(int(labelIndex[i]), '016b')
            line_count_bi = format(line_count, '016b')
            imm = int(imm_dest, 2) - int(line_count_bi, 2) - 1
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            if (imm < 0):
                imm = imm -1
                imm_bi = bin(imm^0b1111111111111111) [3:]

            else:
                imm_bi = format(imm, '016b')
            f.write(str('000100') + str(rs) + str(rt) + str(imm_bi) + '\n')
            line_count += 1

        # -------------------------------------------------------- bne         bne $s, $t, offset       0001 01ss ssst tttt iiii iiii iiii iiii
        elif(line[0:3] == "bne"): # bne         bne $s, $t, offset       0001 01ss ssst tttt iiii iiii iiii iiii
            line = line.replace("bne","")
            line = line.split(",")
            for i in range(len(labelName)):
                if (labelName[i] == line[2]):
                    imm_dest = format(int(labelIndex[i]), '016b')
            line_count_bi = format(line_count, '016b')
            imm = int(imm_dest, 2) - int(line_count_bi, 2) - 1
            rs = format(int(line[0]),'05b')
            rt = format(int(line[1]),'05b')
            if (imm < 0):
                imm = imm -1
                imm_bi = bin(imm^0b1111111111111111) [3:]

            else:
                imm_bi = format(imm, '016b')
            f.write(str('000101') + str(rs) + str(rt) + str(imm_bi) + '\n')
            line_count += 1

        # ------------------------------------------------------------ sltu       sltu $d, $s, $t      0000 00ss ssst tttt dddd d000 0010 1011
        elif(line[0:4] == "sltu"): 
            line = line.replace("sltu","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000101011') + '\n')
            line_count += 1

        # ------------------------------------------------------------ slt         slt $d, $s, $t       0000 00ss ssst tttt dddd d000 0010 1010
        elif(line[0:3] == "slt"): 
            line = line.replace("slt","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(str('000000') + str(rs) + str(rt)  + str(rd) + str('00000101010') + '\n')
            line_count += 1

        elif(line[0:1] == "j"): # JUMP
            line = line.replace("j","")
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                f.write(str('000010') + str(format(int(line[0]),'026b')) + '\n')
                line_count += 1

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                        f.write(str('000010') + str(format(int(labelIndex[i]),'026b')) + '\n')
                        line_count += 1

    f.close()

    return f



def sim(program):
    finished = False      # Is the simulation finished? 
    PC = 0                # Program Counter
    register = [0] * 32   # Let's initialize 32 empty registers
    mem = [0] * 12288     # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
                          # But my machine has 16GB of RAM, its ok :)
    DIC = 0               # Dynamic Instr Count
    while(not(finished)):
        if PC == len(program) - 4: 
            finished = True
        fetch = program[PC]
        DIC += 1
        #print(hex(int(fetch,2)), PC)
        if fetch[0:6] == '001000': # ADDI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            register[t] = register[s] + imm
            
        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100010': # SUB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] - register[t]
            
        elif fetch[0:6] == '000100':  # BEQ
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            # Compare the registers and decide if jumping or not
            if register[s] == register[t]:
                PC += imm*4
        
        elif fetch[0:6] == '001101':   # ORI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] | imm

        elif fetch[0:6] == '101011':  # SW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            mem[offset] = register[t]

        else:
            # This is not implemented on purpose
            print('Not implemented')

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***')
    print('Registers $8 - $23 ', register[8:23])
    print('Dynamic Instr Count ', DIC)
    print('Memory contents 0x2000 - 0x2050 ', mem[8192:8272])




def main():
    mipsToBin()
    file = open('mc.asm')

    program = []
    for line in file:
        
        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)
        if line[0] == '\n':
            continue
        line = line.replace('\n','')
        instr = line[0:]
        program.append(instr)       # since PC increment by 4 every cycle,
        program.append(0)           # let's align the program code by every
        program.append(0)           # 4 lines
        program.append(0)

    # We SHALL start the simulation! 
    sim(program)     

if __name__ == '__main__':
    main()