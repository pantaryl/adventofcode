from enum import Enum

class ParameterMode(Enum):
    Position  = 0
    Immediate = 1
    Relative  = 2

class Intcode:
    def __init__(self, verbose=False):
        self.verbose     = verbose
        self.program     = []
        self.inputStream = []
        self.ip          = 0
        self.relBase     = 0
        self.eop         = False
        self.needsInput  = False
        self.readOutput  = False
        self.stallOnOutput = False
        self.retVal = None
        self.opcodes = {
            1 : (self.opcode1, 3, "add"),
            2 : (self.opcode2, 3, "mul"),
            3 : (self.opcode3, 1, "inp"),
            4 : (self.opcode4, 1, "out"),
            5 : (self.opcode5, 2, "jmp1"),
            6 : (self.opcode6, 2, "jmp0"),
            7 : (self.opcode7, 3, "lt"),
            8 : (self.opcode8, 3, "eq"),
            9 : (self.opcode9, 1, "rel"),
            99: (self.opcode99, 0, "eop"),
        }

    def printOperandValues(self, numOperands:int):
        if numOperands > 0:
            return ",".join([str(x) for x in self.program[self.ip+1:self.ip+1+numOperands]])

    def initProgram(self, program: list, inputStream: list = [], stallOnOutput=False):
        self.program     = list(program) + [0] * 5000
        self.ip          = 0
        self.relBase     = 0
        self.eop         = False
        self.needsInput  = False
        self.readOutput  = False
        self.stallOnOutput = stallOnOutput
        self.retVal      = None
        self.inputStream = inputStream

    def runProgram(self, inputStream: list = None):
        self.readOutput = False
        if inputStream is not None:
            self.inputStream.extend(inputStream)
            self.needsInput = False

        while self.eop is False and self.needsInput is False and (self.stallOnOutput is False or self.readOutput is False):
            instruction = "00000000000000" + str(self.program[self.ip])
            opcode      = int(instruction[-2:])
            assert(opcode in self.opcodes)
            opcode = self.opcodes[opcode]
            if self.verbose: print(f"IP: {self.ip} - {instruction}({opcode[2]}) - Operands({self.printOperandValues(opcode[1])}) - ")
            opcode[0]([int(x) for x in instruction[:-2]])

        return self.retVal

    def getOperand(self, operand: int, modes: list, isDest=False):
        value = self.program[self.ip + operand]
        mode  = ParameterMode(modes[-operand])
        if isDest:
            if mode == ParameterMode.Position:
                assert(value is not None and value >= 0)
                if self.verbose: print(f"    (Operand {operand}, Mode {mode}) = DST({value})")
                return value
            elif mode == ParameterMode.Relative:
                assert((self.relBase + value) is not None and (self.relBase + value) >= 0)
                if self.verbose: print(f"    (Operand {operand}, Mode {mode}, RelBase {self.relBase}, Value {value}) = DST({self.relBase + value})")
                return self.relBase + value
        else:
            if mode == ParameterMode.Position:
                if self.verbose: print(f"    (Operand {operand}, Mode {mode}) = {self.program[value]}")
                assert(value >= 0)
                return self.program[value]
            elif mode == ParameterMode.Immediate:
                if self.verbose: print(f"    (Operand {operand}, Mode {mode}) = {value}")
                return value
            elif mode == ParameterMode.Relative:
                if self.verbose: print(f"    (Operand {operand}, Mode {mode}, RelBase {self.relBase}, Value {value}) = {self.program[self.relBase + value]}")
                assert((self.relBase + value) >= 0)
                return self.program[self.relBase + value]

    def opcode1(self, modes: list):
        src0 = self.getOperand(1, modes)
        src1 = self.getOperand(2, modes)
        dest = self.getOperand(3, modes, isDest=True)
        self.program[dest] = src0 + src1
        self.ip += 4

    def opcode2(self, modes: list):
        src0 = self.getOperand(1, modes)
        src1 = self.getOperand(2, modes)
        dest = self.getOperand(3, modes, isDest=True)
        self.program[dest] = src0 * src1
        self.ip += 4

    def opcode3(self, modes: list):
        if len(self.inputStream) == 0:
            self.needsInput = True
        else:
            dest  = self.getOperand(1, modes, isDest=True)
            assert(len(self.inputStream) > 0)
            value = int(self.inputStream.pop(0))
            self.program[dest] = value
            self.ip += 2

    def opcode4(self, modes: list):
        src0 = self.getOperand(1, modes)
        if self.verbose:
            print(f"Output: {src0}")
        self.retVal     = src0
        self.readOutput = True
        self.ip        += 2

    def opcode5(self, modes: list):
        src0    = self.getOperand(1, modes)
        jumpLoc = self.getOperand(2, modes)
        if src0 != 0:
            self.ip = jumpLoc
        else:
            self.ip += 3

    def opcode6(self, modes: list):
        src0    = self.getOperand(1, modes)
        jumpLoc = self.getOperand(2, modes)
        if src0 == 0:
            self.ip = jumpLoc
        else:
            self.ip += 3

    def opcode7(self, modes: list):
        src0    = self.getOperand(1, modes)
        src1    = self.getOperand(2, modes)
        dest    = self.getOperand(3, modes, isDest=True)
        self.program[dest] = 1 if src0 < src1 else 0
        self.ip += 4

    def opcode8(self, modes: list):
        src0    = self.getOperand(1, modes)
        src1    = self.getOperand(2, modes)
        dest    = self.getOperand(3, modes, isDest=True)
        self.program[dest] = 1 if src0 == src1 else 0
        self.ip += 4

    def opcode9(self, modes:list):
        src0 = self.getOperand(1, modes)
        self.relBase += src0
        self.ip += 2


    def opcode99(self, modes: list):
        self.ip  += 1
        self.eop  = True

        if self.retVal is None:
            self.retVal = self.program[0]

