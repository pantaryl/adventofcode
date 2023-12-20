from shared import *

INPUT_DATA = [x for x in INPUT_DATA]

# % starts as off, ignore high, on low flip between on/off.
# if off, turn on send high, if on, turn off and send low

# & remember the type of most recent pulse received from each of their connected input
# default to low for each input
# update the last pulse for that input
# if all inputs are high, send low,
# otherwise send high

# when broadcast sends pulse, it sends the same to all destination

# FIFO
class Input:
    def __init__(self, line):
        if line[0] == "%":
            self.type = "%"
            line = line[1:]
            self.state = False
        elif line[0] == "&":
            self.type = "&"
            line = line[1:]
            self.state = "low"
        else:
            assert "broadcast" in line
            self.type = ""

        self.inputs: List["Input"] = []
        self.last_rec: Dict[str, str] = {}

        self.name, outputs = line.split(" -> ")
        self.outputs = [output for output in outputs.split(", ")]

    def __repr__(self):
        return f"{self.type}{self.name} -> {', '.join(self.outputs)} [{'|'.join([x.name for x in self.inputs])}]"

    def add_input(self, input):
        self.inputs.append(input)
        self.last_rec[input.name] = 'low'

    @property
    def remember(self):
        if len(self.last_rec.keys()) == 0:
            return 'high'
        elif all([x == 'high' for _, x in self.last_rec.items()]):
            return 'low'

        return 'high'

def make_inputs():
    INPUTS = {}
    for line in INPUT_DATA:
        new = Input(line)
        INPUTS[new.name] = new

    for name, input in INPUTS.items():
        for output in input.outputs:
            if output in INPUTS:
                INPUTS[output].add_input(input)
    return INPUTS

def push_button(iteration: int, part2: bool = False, debug: bool = False):
    global seen_rx_inputs, single_input_to_rx

    pulses = { 'low': 0, 'high': 0 }
    fifo = deque( [ ('low', 'broadcaster', None) ] )

    while fifo:
        signal, input_name, sender = fifo.popleft()
        pulses[signal] += 1

        if debug:
            if sender is None:
                print(f"button -{signal}-> {input_name}")
            else:
                print(f"{sender.name} -{signal}-> {input_name}")

        if input_name not in INPUTS:
            continue

        input = INPUTS[input_name]

        if input.name == 'broadcaster':
            for output in input.outputs:
                fifo.append((signal, output, input))
        elif input.type == "%":
            if signal == 'low':
                input.state = not input.state

                output_signal = 'high' if input.state else 'low'
                for output in input.outputs:
                    fifo.append((output_signal, output, input))
        elif input.type == "&":
            input.last_rec[sender.name] = signal

            output_signal = input.remember

            if part2 and single_input_to_rx in input.outputs and output_signal == 'high':
                # For Part2, the 'rx' module only has a single input, and it is a '&' type.
                # In order for the machines to send a low pulse to 'rx', the single input
                # to 'rx' must receive all 'high'.
                # Each one has its own cycle, so we want to calculate what the LCM of all of the
                # cycles is.
                seen_rx_inputs[input.name].append(iteration + 1)
            for output in input.outputs:
                fifo.append((output_signal, output, input))
    if debug: print()
    return pulses, False

INPUTS = make_inputs()
pulses = [push_button(i, False)[0] for i in range(1000)]
low    = sum([x['low'] for x in pulses])
high   = sum([x['high'] for x in pulses])
print(low * high)

INPUTS = make_inputs()
seen_rx_inputs = defaultdict(list)

# 'rx' module has only one input. Make sure.
single_input_to_rx = [name for name, input in INPUTS.items() if 'rx' in input.outputs]
if len(single_input_to_rx) == 1:
    # Get the name of the input to 'rx'.
    single_input_to_rx = single_input_to_rx[0]

    # We're assuming it is a '&' module that serves as the input to 'rx'.
    assert INPUTS[single_input_to_rx].type == '&'

    # We're also assuming that all of the inputs to single_input_to_rx are also '&'.
    assert all([x.type == '&' for name, x in INPUTS.items() if single_input_to_rx in x.outputs])

    for i in range(10000):
        push_button(i, True)

    # Check for when all of the cycles converge.
    cycles = []
    for input, seen in seen_rx_inputs.items():
        cycles.append(seen[1] - seen[0])
    print(lcm(cycles))
