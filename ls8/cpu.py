"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of RAM

        self.ram = [[0b00000000]] * 256

        # 8 registers of 8-bits each. r[0] - r[7]

        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)
        self.reg = [0] * 8
        for i in range(8):
            self.reg[i] = 0b00000000

        self.sp = 0xF4  # Power on state: Stack pointer is set to `0xF4`.

        self.reg[7] = self.sp   # registry index 7 reserved for stack pointer



        # Internal Registers

        # `PC`: Program Counter, address of the currently executing instruction

        self.pc = 0x00

        # `IR`: Instruction Register, contains a copy of the currently executing instruction


        # `MAR`: Memory Address Register, holds the memory address we're reading or writing

        # `MDR`: Memory Data Register, holds the value to write or the value just read

        self.hlt = 0x01
        self.ldi = 0x82 # Operation values for cpu to reference. Moving to hash system soon.compute
        self.prn = 0x47
        self.mul = 0xA2
        self.pop = 0x46
        self.push = 0x45

        # `FL`: Flags

        self.fl = 0x00


    # MAR contains ADDRESS that is being READ or WRITTEN TO (Memory Address Register)

    # MDR contains the DATA that WAS READ or is TO BE WRITTEN (Memory Data Register)

    # MAR == ADDRESS

    # MDR == DATA


    def ram_read(self, mar): # mar = address to read from
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar): # mdr = data to write
        self.ram[mar] = mdr        # mar = address where to write data

    def load(self, program):
        """Load a program into memory."""

        address = 0


        with open(program, 'rt') as ls8exe:
            for eachline in ls8exe:
                command = eachline.split("#")[0].strip()
                if command != "":
                    self.ram[address] = int(command, 2)
                    address += 1



        # for instruction in goose:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # `IR`: Instruction Register, contains a copy of the currently executing instruction

        ir = 0 # Resets IR to initial position before program begins to run

        # `PC`: Program Counter, address of the currently executing instruction

        ir = self.ram_read(self.pc) # Aligns IR with current contents of PC (This line probably unnecessary)
        running = True # Value to monitor if program is still executing.
                       # It starts at true and checks after executing each instruction
        while running == True:

            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

                # Pulling contents from position of program counter and the following 2 addresses

            if ir == self.hlt: # When the IR hits the halt value, the loop is exited and the program stops
                running = False
            else:
                if ir == self.ldi: # LDI = "Load Immediate". Fills the resgistry index specified by next line with value from the line after that to be used in later operation
                    self.reg[operand_a] = operand_b
                    self.pc += 3 # LDI consumes 3 successive bytes, so we move the counter by 3 for next instruction
                elif ir == self.prn: # Print the value from the registry index provided by next line
                    print(self.reg[operand_a])
                    self.pc += 2 # Print operation consumes 2 bytes, so we move counter by 2
                elif ir == self.mul: # Passes following two lines to the ALU to be multiplied
                    self.alu("MUL", operand_a, operand_b)
                    self.pc += 3 # Again, consumes 3 bytes, so pointer moves 3 lines
                elif ir == self.pop:
                    self.reg[operand_a] = self.ram_read(self.sp)
                    self.sp += 1
                    self.pc += 2
                elif ir == self.push:
                    self.sp -= 1
                    self.ram[self.sp] = self.reg[operand_a]
                    self.pc += 2

                else:
                    self.pc += 1 # Shouldn't ever hit this, but gives the program a chance to not crash if a useless line is present

    # hlt = 0x01
    # ldi = 0x82
    # prn = 0x47
    # mul = 0xA2

    # class Ops:


    #     def __init__(self):
    #         self.ops_table = {}
    #         self.ops_table[hlt] = self.handle_hlt
    #         self.ops_table[ldi] = self.handle_ldi
    #         self.ops_table[prn] = 0x47
    #         self.ops_table[mul] = 0xA2

    #     def handle_hlt(self):
    #         exit()

    #     def handle_ldi(self, operand_a, operand_b):
    #         CPU.reg[operand_a] = operand_b
    #         self.pc += 3