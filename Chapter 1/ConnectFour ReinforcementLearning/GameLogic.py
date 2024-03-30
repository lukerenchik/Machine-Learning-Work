# Luke Renchik - 3/29
import numpy as np

BOARD_ROWS = 6
BOARD_COLS = 7
BOARD_SIZE = BOARD_ROWS * BOARD_COLS

class StateGenerator:
    def __init__(self):
        self.all_states = None
        self.board_rows = 6
        self.board_cols = 7
        self.board_size = self.board_rows * self.board_cols
    def get_all_states(self):
        current_symbol = 1
        current_state = State()
        all_states = dict()
        all_states[current_state.hash()] = (current_state, current_state.is_end())
        self.get_all_states_impl(current_state, current_symbol, all_states)
        return all_states

    #this function is currently looping through every place on the connect 4 board, need to only check the insertion locations
    def get_all_states_impl(self, current_state, current_symbol, all_states):
        for i in range(self.board_rows):
            for j in range(self.board_cols):
                if current_state.gameboard[i, j] == 0 and (current_state.gameboard[i, j - 1] != 0 or current_state.gameboard[i, 0]):
                    new_state = current_state.next_state(i, j, current_symbol)
                    new_hash = new_state.hash()
                    if new_hash not in all_states:
                        is_end = new_state.is_end()
                        all_states[new_hash] = (new_state, is_end)
                        if not is_end:
                            self.get_all_states_impl(new_state, -current_symbol, all_states)

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
        self.gameboard = np.zeros(BOARD_SIZE)
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

        # Define the target sequence length
        TARGET = 4

        # Check rows and columns
        for axis in range(2):
            for line in np.rot90(self.gameboard, axis):
                if np.any(np.convolve(line == 1, np.ones(TARGET), mode='valid') == TARGET):
                    self.winner = 1
                    self.end = True
                    return self.end
                if np.any(np.convolve(line == -1, np.ones(TARGET), mode='valid') == TARGET):
                    self.winner = -1
                    self.end = True
                    return self.end

        # Check diagonals
        for shift in range(-self.gameboard.shape[0] + TARGET, self.gameboard.shape[1] - TARGET + 1):

            diag = np.diagonal(self.gameboard, offset=shift)

            if np.any(np.convolve(diag == 1, np.ones(TARGET), mode='valid') == TARGET):
                self.winner = 1
                self.end = True
                return self.end
            if np.any(np.convolve(diag == -1, np.ones(TARGET), mode='valid') == TARGET):
                self.winner = -1
                self.end = True
                return self.end

            diag = np.diagonal(np.fliplr(self.gameboard), offset=shift)

            if np.any(np.convolve(diag == 1, np.ones(TARGET), mode='valid') == TARGET):
                self.winner = 1
                self.end = True
                return self.end
            if np.any(np.convolve(diag == -1, np.ones(TARGET), mode='valid') == TARGET):
                self.winner = -1
                self.end = True
                return self.end

        # whether it's a tie
        if not np.any(self.gameboard == 0):
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


state_generator = StateGenerator()
all_states = state_generator.get_all_states()

