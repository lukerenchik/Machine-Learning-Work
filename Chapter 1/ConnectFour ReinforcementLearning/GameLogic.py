#Luke Renchik - 3/29
import numpy as np
from StateGenerator import StateGenerator
BOARD_ROWS = 6
BOARD_COLS = 7
BOARD_SIZE = BOARD_ROWS * BOARD_COLS

#TODO: Figure out where to add logic about pieces falling into their location, and the connect 4 rules.

state_generator = StateGenerator()
all_states = state_generator.get_all_states()
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

    def nextState(self, i, j, symbol):
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


# TODO This function needs to be modified to check only next possible moves, which involves placing pieces at the top of
# TODO the board and having them fall into place. There are at most 7 possibles moves from any one state.






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

    def play(self, print_state=False):
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
            next_state_hash = current_state.nextState(i, j, symbol).hash()
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
        #This method will also require in depth study and modification
        pass