lui $8, 0xFA19
ori $8, $8, 0xE366

#this part for B (ii), saved all the cases where there is 11111
addi $18, $0,0xf8
sw $18, 0x2500($0)
addi $18, $0,0x7c
sw $18, 0x2504($0)
addi $18, $0,0x3e
sw $18, 0x2508($0)
addi $18, $0,0x1f
sw $18, 0x250c($0)
addi $18, $0,0x9f
sw $18, 0x2510($0)
addi $18, $0,0xdf
sw $18, 0x2514($0)
addi $18, $0,0xff
sw $18, 0x2518($0)
addi $18, $0,0x5f
sw $18, 0x251c($0)
addi $18, $0,0x3f
sw $18, 0x2520($0)
addi $18, $0,0xbf
sw $18, 0x2524($0)
addi $18, $0,0x7f
sw $18, 0x2528($0)
addi $18, $0,0xf9
sw $18, 0x252c($0)
addi $18, $0,0xfa
sw $18, 0x2530($0)
addi $18, $0,0xfc
sw $18, 0x2534($0)
addi $18, $0,0xfd
sw $18, 0x2538($0)
addi $18, $0,0xfe
sw $18, 0x253c($0)
addi $18, $0,0x7d
sw $18, 0x2540($0)
addi $18, $0,0xbe
sw $18, 0x2544($0)

#for loop 100
addi $13, $0, 1
#loop should stop at 101
addi $15, $0, 101
#Initialize 14 to 0 for the offset
addi $14, $0, 0
#Initialize 16 to hold the max value
addi $16, $0, 0
addi $20, $0, 0
addi $21, $0, 0
#loop 100 times {
loop100: 
add $9, $0, $13 
addi $12, $0, 5
#loop 5 times {
loop:
multu $8, $9
mflo $10
mfhi $11
xor $9, $10, $11
addi $12, $12, -1
bne $12, $0, loop
# } LOOP END
sll $10, $9, 16
srl $10, $10, 16
srl $11, $9, 16
xor $9, $10, $11
sll $10, $9, 24
srl $10, $10, 24
srl $11, $9, 8
xor $9, $10, $11

# if to save the max value and address
sltu $17, $16, $9
beq $17, $0, skip
add $16, $0,$9
sw $9, 0x2000($0)
addi $17, $14, 0x2020
sw $17, 0x2004($0)
addi $17, $0, 0
skip:
# }

addi $18, $0, 18
loop18:
lw $19, 0x2500($20)
addi $20, $20, 4
bne $19, $9, skip18
addi $21, $21, 1
skip18:
addi $18, $18, -1
bne $18, $0, loop18
addi $20, $0, 0
sw $9, 0x2020($14)
addi $14, $14, 4
addi $13, $13, 1
bne $13, $15, loop100
# } LOOP END

sw $21 0x2008($0)

#this part for B (iii)
addi $8, $0, 0
addi $9, $0, 99
addi $10, $0, 0
addi $11, $0, 0
addi $12, $0, 1
addi $13, $0, 0
addi $14, $0, 4
addi $15, $0, 0
addi $16, $0, 0

loop1:
lw $10, 0x2020($11)

loop2:
lw $13, 0x2020($14)
bne $10, $13, skip1
addi $15, $15, 1
skip1:

sltu $17, $12, $9
beq $17, $0, skip3
addi $12, $12, 1
skip3:
addi $14, $14, 4
bne $12, $9, loop2

sltu $17, $16, $15
beq $17, $0, skip2
add $16, $0, $15
sw $16, 0x2014($0)
sw $10, 0x2010($0)
skip2:

addi $11, $11, 4
addi $14, $11, 4
addi $8, $8, 1
addi $12, $8, 1
addi $15, $0, 0
bne $8, $9, loop1

