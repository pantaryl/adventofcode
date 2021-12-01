from intcode import Intcode
import threading, time

verbose = False

with open("../input/day23.txt", 'r') as inputFile:
    splitData = inputFile.read().split(",")
    data = [int(x) for x in splitData]

def runComputer(id: int):
    runner = computers[id]['runner']
    runner : Intcode
    runner.initProgram(data, inputStream=[id], stallOnOutput=True)
    runner.runProgram()
    while runner.eop is False:
        if computers['end']:
            break
        elif runner.readOutput:
            dest = runner.retVal
            runner.runProgram()
            assert(runner.readOutput)
            x    = runner.retVal
            runner.runProgram()
            assert (runner.readOutput)
            y    = runner.retVal

            if dest == 255 and computers['part1'] is None:
                print("Part1:", y)
                computers['part1'] = (dest, x, y)

            if verbose: print(id, "OUTPUT", dest, x, y)
            destLock =  computers[dest]['lock']
            destLock : threading.Lock
            destLock.acquire()
            if dest == 255:
                computers[dest]['input'] = [x, y]
            else:
                computers[dest]['input'].extend([x, y])
            destLock.release()

            computers[id]['output'].extend([dest, x, y])
            runner.runProgram()
        elif runner.needsInput:
            myLock = computers[id]['lock']
            myLock.acquire()
            if len(computers[id]['input']) == 0:
                myInput = [ -1 ]
            else:
                myInput = [ computers[id]['input'].pop(0) ]
            myLock.release()
            if verbose: print(id, "INPUT", myInput)
            runner.runProgram(inputStream=myInput)
    if verbose: print("ENDED PROGRAM", id)

def runNat():
    lastY = None
    while len(computers[255]['input']) == 0:
        time.sleep(0.5)
    while True:
        if computers['end']:
            break

        [computers[id]['lock'].acquire() for id, _ in threads]

        allEmpty = all([True if len(computers[id]['input']) == 0 else False for id in range(NUM_COMPUTERS)])
        if allEmpty:
            if verbose: print("NAT FOUND EMPTY!", computers[255]['input'], lastY)
            computers[0]['input'] = list(computers[255]['input'])
            assert(len(computers[0]['input']) == 2)
            yVal = computers[0]['input'][1]
            if yVal == lastY:
                print("Part2:", yVal)
                computers['end'] = True
            lastY = yVal

        [computers[id]['lock'].release() for id, _ in threads]

        time.sleep(0.05)

NUM_COMPUTERS = 50
computers     = { 'part1': None, 'end': False }
threads       = []

def initComputer(id):
    computers[id] = {}
    computers[id]['lock']   = threading.Lock()
    computers[id]['runner'] = Intcode()
    computers[id]['input']  = []
    computers[id]['output'] = []

for id in range(NUM_COMPUTERS):
    initComputer(id)
    threads.append((id, threading.Thread(target=runComputer, name=str(id), args=(id,))))

NAT = 255
initComputer(NAT)
threads.append((NAT, threading.Thread(target=runNat, name=str(NAT))))

for thread in threads:
    thread[1].start()

while computers['end'] is False:
    continue

for thread in threads:
    thread[1].join()

