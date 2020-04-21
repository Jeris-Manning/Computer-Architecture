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
        self.reg = []
        for i in range(8):
            self.reg[i] = 0b00000000

        self.reg[7] = 0xF4  #Power on state: * `R7` is set to `0xF4`.

        # Internal Registers

        # `PC`: Program Counter, address of the currently executing instruction

        self.pc = 0x00

        # `IR`: Instruction Register, contains a copy of the currently executing instruction

        # ir = 0x00

        # `MAR`: Memory Address Register, holds the memory address we're reading or writing

        # mar = 0b00000000

        # `MDR`: Memory Data Register, holds the value to write or the value just read

        # mdr = 0b00000000

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

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

        ir = 0

        ir = self.pc
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)







        print(ir, operand_a, operand_b) # THIS WAS TO SHUT THE LINTER UP
