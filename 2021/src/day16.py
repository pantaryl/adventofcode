from shared import *

ConversionTable = {
  "0" : "0000",
  "1" : "0001",
  "2" : "0010",
  "3" : "0011",
  "4" : "0100",
  "5" : "0101",
  "6" : "0110",
  "7" : "0111",
  "8" : "1000",
  "9" : "1001",
  "A" : "1010",
  "B" : "1011",
  "C" : "1100",
  "D" : "1101",
  "E" : "1110",
  "F" : "1111",
}

# Input data is in INPUT_DATA.
INPUT_DATA = "".join([ConversionTable[x] for x in INPUT_DATA[0]])

# Packet
# [2:0] = version
# [5:3] = type ID
# [6]   = length type id if typeId != 4

# type 4 is literal
# type N!=4 is operator

# operator contains 1+ sub-packets
# if lengthTypeId == 0, next 15 bits are a number that represents the total length in bits
# if lengthTypeId == 1, next 11 bits are a number that represents the number of subpackets immediately contained.

class Packet:
    version = 0
    typeId  = 0

    lengthId   = 0
    length     = 0
    subPackets : List["Packet"]

    startIdx        = 0
    totalLengthBits = 0
    data = ""
    literal = ""

    def __init__(self, index, data):
        self.startIdx = index
        self.version  = int(data[index     : index + 3], 2)
        self.typeId   = int(data[index + 3 : index + 6], 2)

        # Initialize this per object, otherwise you have a single list everyone is playing with.
        self.subPackets = []

        index += 6

        if self.typeId == 4:
            # Type 4, literal.
            while True:
                if index > len(data):
                    # We're at a zero.
                    break
                elif data[index] == '1':
                    self.literal += data[index + 1 : index + 5]
                    index += 5
                elif data[index] == '0':
                    # Last group.
                    self.literal += data[index + 1 : index + 5]
                    index += 5
                    break
            self.literal = int(self.literal, 2)
        else:
            assert(self.typeId != 4)
            # operator
            if data[index] == '0':
                # length is encoded as bits
                lengthInBits = int(data[index+1:index+1+15], 2)
                index += 16

                subPacketStart = index
                while index < subPacketStart + lengthInBits:
                    self.subPackets.append(Packet(index, data))
                    index += self.subPackets[-1].totalLengthBits
                assert(index == subPacketStart + lengthInBits)
            else:
                assert(data[index] == '1')
                # length is encoded as packet count
                packetCount = int(data[index + 1 : index + 1 + 11], 2)
                index += 12

                for i in range(packetCount):
                    self.subPackets.append(Packet(index, data))
                    index += self.subPackets[-1].totalLengthBits


        self.totalLengthBits = index - self.startIdx
        self.data            = data[self.startIdx : index]

    @property
    def versions(self):
        return self.version + sum([x.versions for x in self.subPackets])

    @property
    def calculate(self):
        if self.typeId == 0:
            return sum([x.calculate for x in self.subPackets])
        elif self.typeId == 1:
            product = 1
            for x in self.subPackets:
                product *= x.calculate
            return product
        elif self.typeId == 2:
            return min([x.calculate for x in self.subPackets])
        elif self.typeId == 3:
            return max([x.calculate for x in self.subPackets])
        elif self.typeId == 4:
            return self.literal
        elif self.typeId == 5:
            assert(len(self.subPackets) == 2)
            return self.subPackets[0].calculate > self.subPackets[1].calculate
        elif self.typeId == 6:
            assert(len(self.subPackets) == 2)
            return self.subPackets[0].calculate < self.subPackets[1].calculate
        elif self.typeId == 7:
            assert(len(self.subPackets) == 2)
            return self.subPackets[0].calculate == self.subPackets[1].calculate

# Part 1
packet = Packet(0, INPUT_DATA)
assert((len(set(INPUT_DATA[packet.totalLengthBits:])) == 1) and INPUT_DATA[packet.totalLengthBits] == '0')

print(packet.versions)

# Part 2
print(packet.calculate)
