# Luke Renchik - 3/29
from GameLogic import state_generator
import pickle
import numpy as np


BOARD_ROWS = 6
BOARD_COLS = 7

class Player:
    # @step_size: the step size to update estimations
    # @epsilon: the probability to explore
    def __init__(self, step_size=0.1, epsilon=0.1):
        self.estimations = dict()
        self.step_size = step_size
        self.epsilon = epsilon
        self.states = []
        self.greedy = []
        self.symbol = 0

    def reset(self):
        self.states = []
        self.greedy = []

    def set_state(self, state):
        self.states.append(state)
        self.greedy.append(True)


    def set_symbol(self, symbol):
        self.symbol = symbol
        #TODO Revisit and see if more is needed here

    def backup(self):
        states = [state.hash() for state in self.states]
        for i in reversed(range(len(states) - 1)):
            state = states[i]
            # Ensure states[i + 1] is in estimations, or initialize it
            if states[i + 1] not in self.estimations:
                self.estimations[states[i + 1]] = 0.5  # Default unknown state value
            # Similar check for current state
            if state not in self.estimations:
                self.estimations[state] = 0.5
            td_error = self.greedy[i] * (self.estimations[states[i + 1]] - self.estimations[state])
            self.estimations[state] += self.step_size * td_error

    def act(self):
        print("we have entered another iteration")
        state = self.states[-1]
        next_states = []
        next_positions = []

        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if state.gameboard[i, j] == 0 and (state.gameboard[i - 1, j] != 0 or i == 0):
                    next_positions.append([i, j])
                    next_state_hash = state.next_state(i, j, self.symbol).hash()
                    if next_state_hash not in self.estimations:
                        self.estimations[next_state_hash] = 0.5
                    next_states.append(next_state_hash)
        if np.random.rand() < self.epsilon:
            action = next_positions[np.random.randint(len(next_positions))]
            action.append(self.symbol)
            self.greedy[-1] = False
            return action
        values = []

        for hash_val, pos in zip(next_states, next_positions):
            values.append((self.estimations[hash_val], pos))
        # to select one of the actions of equal value at random due to Python's sort is stable
        np.random.shuffle(values)
        values.sort(key=lambda x: x[0], reverse=True)
        action = values[0][1]
        action.append(self.symbol)
        return action

    def save_policy(self):
        with open('policy_%s.bin' % ('first' if self.symbol == 1 else 'second'), 'wb') as f:
            pickle.dump(self.estimations, f)

    def load_policy(self):
        with open('policy_%s.bin' % ('first' if self.symbol == 1 else 'second'), 'rb') as f:
            self.estimations = pickle.load(f)
