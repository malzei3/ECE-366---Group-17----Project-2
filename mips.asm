add $1, $0, $5
addi $2, $8, -20
adds:
addi $2, $8, 30
lump:
addiu $9, $0, 255
mult $2, $4
j lump
branch:
multu $2, $9
srl $20, $9, 16
lb $20, 24($0)
sb $20, 24($0)
lw $20, 24($0)
sw $20, 24($zero)
next:
beq $7, $0, next
bne $20, $2, branch
slt $9, $23, $0
sltu $8, $20, $0
