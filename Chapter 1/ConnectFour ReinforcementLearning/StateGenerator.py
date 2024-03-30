#Luke Renchik - 3/29
from GameLogic import State  # Assuming State class is defined elsewhere
import numpy as np

class StateGenerator:
    def __init__(self):
        self.all_states = None
        self.board_rows = 7
        self.board_cols = 7
        self.board_size = self.board_rows * self.board_cols
    def get_all_states(self):
        current_symbol = 1
        current_state = State()
        all_states = dict()
        all_states[current_state.hash()] = (current_state, current_state.is_end())
        self.get_all_states_impl(current_state, current_symbol, all_states)
        return all_states

    def get_all_states_impl(self, current_state, current_symbol, all_states):
        for i in range(self.board_rows):
            for j in range(self.board_cols):
                if current_state.data[i, j] == 0:
                    new_state = current_state.nextState(i, j, current_symbol)
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

