import sys

program = sys.argv[1] # Gets filename from command line

memory = [0] * 256

reg = [0] * 8

sp = 7
reg[sp] = 0xF4   # reg slot 7 is stack pointer


halt = 0x01 # Halt
ldi = 0x82 # Load Immediately
prn = 0x47 # Print
add = 0xA0 # Add
mul = 0xA2 # Multiply
pop = 0x46 # Stack Operators
push = 0x45
call = 0x50
ret = 0x11 # Return (after call)

def alu(op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            reg[reg_a] += reg[reg_b]
        elif op == "MUL":
            reg[reg_a] *= reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")



# Loads program from file into memory

address = 0

with open(program, 'rt') as ls8exe:
    for eachline in ls8exe:
        command = eachline.split("#")[0].strip()
        if command != "":
            memory[address] = int(command, 2)
            address += 1

# Starts the loaded program a running

pc = 0 # Initializes program counter
running = True

while running == True:

    ir = memory[pc] # Instruction register holds current instruction

        # LDI = "Load Immediate". Fills the resgistry index specified by next line with value from the line after that to be used in later operation

    if ir == ldi:
        reg_slot = memory[pc + 1]
        val = memory[pc + 2]
        reg[reg_slot] = val
        pc += 3 # LDI consumes 3 successive bytes, so we move the counter by 3

    elif ir == prn:
        print(reg[memory[pc + 1]])
        pc += 2

    elif ir == push:
        reg[sp] -= 1 # Address of the top of stack minus 1 (Stack grows down)

        reg_slot = memory[pc + 1]
    # 2nd line of push instruction is address of value we want to push
        val = reg[reg_slot]

        address = reg[sp] # address of new top of stack
        memory[address] = val # stores the value to address at top of stack

        pc += 2

    elif ir == pop:

        reg_slot = memory[pc + 1] # designate register slot to hold popped val

        address = reg[sp] # Address of top of stack
        val = memory[address] # Value we popped

        reg[reg_slot] = val # Popped value now in designated registry slot

        pc += 2

        reg[sp] += 1 # move sp up one (new top of stack)

    elif ir == call:

        return_address = pc + 2 # Address to return to after sub-routine

        # Pushing return address onto stack just like push inst.
        reg[sp] -= 1
        memory[reg[sp]] = return_address

        # Gets address of sub-routine and sets pc to that value
        reg_slot = memory[pc + 1]
        target_address = reg[reg_slot]
        pc = target_address

    elif ir == ret:

        # Pop return address from top of stack and set the pc accordingly
        return_address = memory[reg[sp]]
        reg[sp] += 1
        pc = return_address

    elif ir == halt:
        running = False


#
# BIG TIME ALU OPERATIONS HERE
#

    elif ir == add:
        alu("ADD", memory[pc + 1], memory[pc + 2])
        pc += 3
    elif ir == mul:
        alu("MUL", memory[pc + 1], memory[pc + 2])
        pc += 3

#
# GO ALU MATHS SQUAD
#

    else:
        print("I don't understand")
        running = False