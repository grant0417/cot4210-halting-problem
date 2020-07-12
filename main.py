from enum import Enum
from random import randint


class Shift(Enum):
    L = 0  # Left
    R = 1  # Right


class Tape:
    # Infinite tape that goes in positive and negative direction
    # and stores integers
    def __init__(self, input_symbol=None, blank_symbol=0):
        if input_symbol is None:
            input_symbol = [1]
        self.positive = input_symbol
        self.negative = []
        self.blank_symbol = blank_symbol
        self.max_index = 0
        self.min_index = 0

    def __repr__(self):
        neg_tmp = self.negative
        neg_tmp.reverse()
        return str(neg_tmp + self.positive)

    def __getitem__(self, key: int) -> int:
        if key > self.max_index or key < self.min_index:
            return self.blank_symbol
        elif key >= 0:
            return self.positive[key]
        else:
            return self.negative[abs(key) - 1]

    def __setitem__(self, key: int, value: int):
        if key >= 0:
            if key > self.max_index:
                self.max_index = key
                self.positive.append(value)
            else:
                self.positive[key] = value
        else:
            if key < self.min_index:
                self.min_index = key
                self.negative.append(value)
            else:
                self.negative[abs(key) - 1] = value


class TuringMachine:
    def __init__(self,
                 states=None,
                 symbols=None,
                 blank_symbol=None,
                 input_symbols=None,
                 initial_state=None,
                 final_states=None,
                 transitions=None):
        if states is None:
            states = {'HALT', 'A', 'B', 'C'}
        if symbols is None:
            symbols = {0, 1}
        if blank_symbol is None:
            blank_symbol = 0
        if input_symbols is None:
            input_symbols = [1]
        if initial_state is None:
            initial_state = 'A'
        if final_states is None:
            final_states = ['HALT']
        if transitions is None:
            transitions = {
                ('A', 0): (1, Shift.R, 'B'),
                ('B', 0): (0, Shift.R, 'C'),
                ('C', 0): (1, Shift.L, 'C'),
                ('A', 1): (1, Shift.R, 'HALT'),
                ('B', 1): (1, Shift.R, 'B'),
                ('C', 1): (1, Shift.L, 'A'),
            }
        self.states = states
        self.symbols = symbols
        self.blank_symbol = blank_symbol
        self.tape = Tape(input_symbols)  # Input Symbol
        self.state = initial_state
        self.final_states = final_states
        self.transitions = transitions
        self.tape_position = 0

        # Checks to make sure turing machine is valid
        if self.blank_symbol not in self.symbols:
            raise ValueError("Blank symbol is not in Symbols")
        for value in input_symbols:
            if value not in self.symbols:
                raise ValueError("Input symbol is not in Symbols")
        if self.state not in self.states:
            raise ValueError("Initial state is not in Symbols")
        for state in self.final_states:
            if state not in self.states:
                raise ValueError("Final state is not in Symbols")
        if (len(self.states) - 1) * len(self.symbols) != len(self.transitions):
            raise ValueError("Number of transition is incorrect")
        for state in self.states:
            for symbol in self.symbols:
                if state not in self.final_states:
                    if (state, symbol) not in transitions:
                        raise ValueError("Transition for non-halting value is not in transitions")

    def step(self):
        if self.state not in self.final_states:
            write_symbol, shift, next_state = self.transitions[(self.state, self.tape[self.tape_position])]
            self.state = next_state
            self.tape[self.tape_position] = write_symbol
            if shift is Shift.R:
                self.tape_position += 1
            elif shift is Shift.L:
                self.tape_position -= 1
            return True
        else:
            return False


def encoding_to_transitions(encoding, states, halting_states, symbols):
    transitions = {}
    encoding = encoding.split('/')

    # Verify encoding is same good for symbols and states
    machine_description = encoding[0].split('-')
    if (len(states) - len(halting_states)) != int(machine_description[0]):
        raise Exception("Unequal number of states from encoding to states provided")
    if len(symbols) != int(machine_description[1]):
        raise Exception("Unequal number of symbols from encoding to symbols provided")

    i = 1
    for symbol in symbols:
        for state in states:
            if state not in halting_states:
                transition_encoding = encoding[i].split('-')
                transitions[(state, symbol)] = (int(transition_encoding[0]),
                                                Shift(int(transition_encoding[1])),
                                                states[int(transition_encoding[2])])
                i += 1
    return transitions


def enumerate_transition_encodings(machine_numb: int, states: int, halting_states: int, symbols: int):
    encoding = []
    encoding.append("{}-{}".format(states - halting_states, symbols))
    for _ in range((states - halting_states) * symbols):
        symbol = machine_numb % symbols
        machine_numb //= symbols
        shift = machine_numb % 2
        machine_numb //= 2
        state = machine_numb % states
        machine_numb //= states
        encoding.append("{}-{}-{}".format(symbol, shift, state))
    return '/'.join(encoding)


def max_machines(states: int, halting_states: int, symbols: int):
    return (2 * states * symbols) ** ((states - halting_states) * symbols)


if __name__ == "__main__":
    print("Halting Solver")
    print()
    print("Assuming there are 2 symbols [0, 1].")
    print("Choosing 6 states will take a VERY long time")
    print("For >6 symbols you must enter the busy beaver")
    print("Also note that 5 and 6 states are not proven as the busy beaver so they will not necessary be correct.")
    print()

    n_states = int(input("How many states do you want, not including the halting state (1-6): ")) + 1

    if n_states < 2:
        raise ValueError("Invalid number of states")

    states = ['HALT']

    for i in range(n_states - 1):
        s = ""
        while True:
            char = i % 26
            i = i // 26
            s = chr(ord('A') + char) + s
            if i == 0:
                break
        states.append(s)

    halting_states = ['HALT']
    symbols = [0, 1]

    n_halting_states = len(halting_states)
    n_symbols = len(symbols)

    # 1 state busy beaver
    busy_1 = "1-2/1-1-0/0-0-0"

    # 2 state busy beaver
    busy_2 = "2-2/1-1-2/1-0-1/1-0-2/1-1-0"

    # 3 state busy beaver
    busy_3 = "3-2/1-1-2/0-1-3/1-0-3/1-1-0/1-1-2/1-0-1"

    # 4 state busy beaver
    busy_4 = "4-2/1-1-2/1-0-1/1-1-0/1-1-4/1-0-2/0-0-3/1-0-4/0-1-1"

    # 5 state busy beaver
    busy_5 = "5-2/1-1-2/1-1-3/1-1-4/1-0-1/1-1-0/1-0-3/1-1-2/0-0-5/1-0-4/0-0-1"

    # 6 state busy beaver
    busy_6 = "6-2/1-1-2/1-1-3/1-0-4/1-1-5/1-0-1/1-0-0/1-0-5/1-1-6/0-1-2/0-0-3/0-1-4/1-1-3"

    n_busy = ""

    if n_states > 7:
        n_busy = input("Input the transition encoding for the {} state busy beaver: ".format(n_states-1))
    else:
        busy_beavers = [busy_1, busy_2, busy_3, busy_4, busy_5, busy_6]
        n_busy = busy_beavers[n_states - 2]

        print("The encoding of the busy beaver is:", n_busy)
        print()

    print("What type of Turing machine do you want to see if it halts?")
    type = input("(R)andom, (M)achine Number, (T)ransition encoding: ").strip().lower()

    encoding = ""

    if type.startswith("r"):
        encoding = enumerate_transition_encodings(
            randint(0, max_machines(n_states, n_halting_states, n_symbols)), n_states, n_halting_states, n_symbols)
        print("The encoding is: {}".format(encoding))
    elif type.startswith('m'):
        machine_num = \
            int(input("Enter a number between 0 and {}: "
                      .format(max_machines(n_states, n_halting_states, n_symbols)))) \
            % max_machines(n_states, n_halting_states, n_symbols)
        encoding = enumerate_transition_encodings(machine_num, n_states, n_halting_states, n_symbols)
        print("The encoding is: {}".format(encoding))
    elif type.startswith('t'):
        encoding = input("Enter a valid {} state encoding: ".format(n_states))
    else:
        raise ValueError("Unknown input for machine type: {}".format(type))

    busy_transitions = encoding_to_transitions(n_busy, states, halting_states, symbols)

    input_transitions = encoding_to_transitions(encoding, states, halting_states, symbols)

    busy_turing = TuringMachine(states=states, symbols=symbols, input_symbols=[0], transitions=busy_transitions)

    input_turing = TuringMachine(states=states, symbols=symbols, input_symbols=[0], transitions=input_transitions)

    print()
    print("Running busy beaver to find the number of steps it takes...")
    busy_steps = 0
    while busy_turing.step():
        busy_steps += 1

    print("The busy beaver of {} states takes {} steps.".format(n_states - 1, busy_steps))
    print()
    print("Running the selected Turing machine to see if it halts in {} steps...".format(busy_steps))

    input_steps = 0
    while input_turing.step() and input_steps <= busy_steps:
        input_steps += 1

    if not input_turing.step():
        print("The Turing machine halts in {} steps.".format(input_steps))
    else:
        print("The selected Turing machine will never halt!")
