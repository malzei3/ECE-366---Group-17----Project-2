addi $13, $0, 8192
addi $12, $0, 1

loop_1:
sb $12, 0($13)
addi $12, $12, 1
addi $13, $13, 1
bne $12, 256, loop_1

addi $12, $12, -1
sb $12, 0($13)

addi $14, $0, 8192
addi $15, $0, 0

loop_2:
lb $10, 0($14)
addi $8, $0, 0
addi $16, $0, 0
hwc:
andi $9, $10, 1
beq $9, $0, skip
addi $16, $16, 1
skip:
srl $10, $10, 1
addi $8, $8, 1
bne $8, 8, hwc

bne $16, 4, skip_count
addi $15, $15, 1

skip_count:
addi $14, $14, 1
bne $14, 8448, loop_2
