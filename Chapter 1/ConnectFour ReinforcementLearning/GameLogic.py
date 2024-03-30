#Luke Renchik - 3/29
import numpy as np
from StateGenerator import StateGenerator
BOARD_ROWS = 7
BOARD_COLS = 7
BOARD_SIZE = BOARD_ROWS * BOARD_COLS

state_generator = StateGenerator()
all_states = state_generator.get_all_states()
class State:
    def __init__(self):
        self.data = np.zeros(BOARD_SIZE)
        self.winner = None
        self.hash_val = None
        self.end = None

    def hash(self):
        if self.hash_val is None:
            self.hash_val = 0
            for i in np.nditer(self.data):
                self.hash_val = self.hash_val * 3 + i + 1
            return self.hash_val

    def is_end(self):
        if self.end is not None:
            return self.end
        results = []
        # TODO: IDEA: Iterate through board (Horiz, Vert, Diag), dropping the tail
        # TODO: adding to the head, if the total value ever equals 4 declare player 1 as winner, if snakes equal -4
        # TODO: declare player 2 winner.
        for i in range(BOARD_ROWS):
            results.append(np.sum(self.data[i, :]))
        # Check Cols
        for i in range(BOARD_COLS):
            results.append(np.sum(self.data[:, i]))

        for result in results:
            if result == 4:
                self.winner = 1
                self.end = True
                return self.end
            if result == -4:
                self.winner = -1
                self.end = True
                return self.end

        # whether it's a tie
        sum_values = np.sum(np.abs(self.data))
        if sum_values == BOARD_SIZE:
            self.winner = 0
            self.end = True
            return self.end

        # game is still going on
        self.end = False
        return self.end

    def nextState(self, i, j, symbol):
        new_state = State()
        new_state.data = np.copy(self.data)
        new_state.data[i, j] = symbol
        return new_state

    def print_state(self):
        for i in range(BOARD_ROWS):
            out = "| "
            for j in range(BOARD_COLS):
                if self.data[i, j] == 1:
                    token = "*"
                elif self.data[i, j] == -1:
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