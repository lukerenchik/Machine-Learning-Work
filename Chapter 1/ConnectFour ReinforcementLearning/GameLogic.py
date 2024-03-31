# Luke Renchik - 3/29
import numpy as np
BOARD_ROWS = 6
BOARD_COLS = 7
iter = 0


# TODO Implement: Alpha-Beta pruning, Symmetry Reduction,
# TODO Potential Implementations: Transposition Table, Depth-Limited Search with Heuristics, Parallel Processing
class StateGenerator:
    def __init__(self):
        self.all_states = None
        self.board_rows = 6
        self.board_cols = 7
    def get_all_states(self):
        current_symbol = 1
        current_state = State()
        all_states = dict()
        print("We have made it into the function")
        all_states[current_state.hash()] = (current_state, current_state.is_end())
        print("We have made it past the hashing section")
        self.get_all_states_impl(current_state, current_symbol, all_states)
        print("We have moved through the implied section")
        return all_states

    def get_all_states_impl(self, current_state, current_symbol, all_states):
        global iter
        for i in range(self.board_rows):
            for j in range(self.board_cols):
                if current_state.gameboard[i, j] == 0 and (i == 0 or current_state.gameboard[i - 1, j] != 0):
                    new_state = current_state.next_state(i, j, current_symbol)
                    mirrored_state = new_state.mirror()

                    # Generate hashes for both states
                    new_hash = new_state.hash()
                    mirrored_hash = mirrored_state.hash()

                    # Decide which state to store based on your criterion (here, the smaller hash)
                    state_to_store = new_state if new_hash < mirrored_hash else mirrored_state
                    hash_to_store = min(new_hash, mirrored_hash)

                    if hash_to_store not in all_states:
                        is_end = state_to_store.is_end()
                        all_states[hash_to_store] = (state_to_store, is_end)
                        iter += 1
                        print(iter)
                        if not is_end:
                            self.get_all_states_impl(state_to_store, -current_symbol, all_states)

    @staticmethod
    def save_states_to_file(states, file_path):
        # Serialization logic here
        pass

    @staticmethod
    def load_states_from_file(file_path):
        # Deserialization logic here
        pass


class State:
    def __init__(self):
        self.gameboard = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.winner = None
        self.hash_val = None
        self.end = None

    def hash(self):
        if self.hash_val is None:
            self.hash_val = 0
            for i in np.nditer(self.gameboard):
                self.hash_val = self.hash_val * 3 + i + 1
            return self.hash_val

    def is_end(self):
        if self.end is not None:
            return self.end

        # Check rows
        for line in self.gameboard:
            result = self.check_line(line=line)
            if result != 0:
                self.winner = result
                self.end = True
                return self.end

        # Check columns by iterating over the transpose
        for line in self.gameboard.T:
            result = self.check_line(line=line)
            if result != 0:
                self.winner = result
                self.end = True
                return self.end

        result = self.check_diagonals()
        if result != 0:
            self.winner = result
            self.end = True
            return self.end

        if not np.any(self.gameboard == 0) and self.end is not True:
            self.winner = 0
            self.end = True
            return self.end

        # game is still going on
        self.end = False
        return self.end

    def next_state(self, i, j, symbol):
        new_state = State()
        new_state.gameboard = np.copy(self.gameboard)
        new_state.gameboard[i, j] = symbol
        return new_state

    def print_state(self):
        for i in range(BOARD_ROWS):
            out = "| "
            for j in range(BOARD_COLS):
                if self.gameboard[i, j] == 1:
                    token = "*"
                elif self.gameboard[i, j] == -1:
                    token = "x"
                else:
                    token = "0"
                out += token + " | "
            print(out)

    def check_line(self, line, TARGET=4):
        if np.any(np.convolve(line == 1, np.ones(TARGET), mode='valid') == TARGET):
            return 1
        if np.any(np.convolve(line == -1, np.ones(TARGET), mode='valid') == TARGET):
            return -1
        return 0

    def check_diagonals(self, TARGET=4):
        for direction in [self.gameboard, np.fliplr(self.gameboard)]:
            for shift in range(-direction.shape[0] + TARGET, direction.shape[1] - TARGET + 1):
                diag = np.diagonal(direction, offset=shift)
                if self.check_line(diag, TARGET) != 0:
                    return self.check_line(diag, TARGET)
        return 0

    def mirror(self):
        mirrored_gameboard = np.fliplr(self.gameboard)  # Assuming the board is stored in a numpy array
        mirrored_state = State()
        mirrored_state.gameboard = mirrored_gameboard
        return mirrored_state


class Judger:
    # @player1: the player who will move first, its chessman will be 1
    # @player2: another player with a chessman -1
    def __init__(self, player1, player2):
        self.p1 = player1
        self.p2 = player2
        self.current_player = None
        self.p1_symbol = 1
        self.p2_symbol = -1
        self.p1.set_symbol(self.p1_symbol)
        self.p2.set_symbol(self.p2_symbol)
        self.current_state = State()

    def reset(self):
        self.p1.reset()
        self.p2.reset()

    def alternate(self):
        while True:
            yield self.p1
            yield self.p2

    def play(self, print_state=True):
        alternator = self.alternate()
        self.reset()
        current_state = State()
        self.p1.set_state(current_state)
        self.p2.set_state(current_state)
        if print_state:
            current_state.print_state()
        while True:
            player = next(alternator)
            i, j, symbol = player.act()
            next_state_hash = current_state.next_state(i, j, symbol).hash()
            current_state, is_end = all_states[next_state_hash]
            self.p1.set_state(current_state)
            self.p2.set_state(current_state)
            if print_state:
                current_state.print_state()
            if is_end:
                return current_state.winner


class HumanPlayer:
    def __init__(self, **kwargs):
        self.symbol = None
        self.keys = ['q', 'w', 'e', 'r', 't', 'y', 'u']
        self.state = None

    def reset(self):
        pass

    def set_state(self, state):
        self.state = state

    def set_symbol(self, symbol):
        self.symbol = symbol

    def act(self):
        self.state.print_state()
        key = input("Input your position:")
        pass

print("This is what is causing the slowdown")
state_generator = StateGenerator()
print("actually its this breakpoint")
all_states = state_generator.get_all_states()
print("no its running fine.")
