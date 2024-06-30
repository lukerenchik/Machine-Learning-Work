from agent import Agent
import numpy as np


class UpperConfidenceActionBandit(Agent):
    def __init__(self, testbed):
        super().__init__(testbed)
        self.SignalValueCountDict = {signal: [value, 0] for signal, value in self.expected_rewards.items()}
        self.UCBDict = {}
        self.timestep = 1
        self.exploration_rate = .1
        # In UCB Dict I want to store {Signal Name: expected value, num times been selected}

    def dictionary_init(self):
        self.SignalValueCountDict = {signal: [value, 0] for signal, value in self.expected_rewards.items()}


    def UCB_Selection(self):
        for signal, (value, count) in self.SignalValueCountDict.items():
            exploration_term = self.exploration_rate * np.sqrt(np.log(self.timestep) / (count + 1))
            action_value = value + exploration_term
            self.UCBDict[signal] = [action_value, count]
        argmax_signal = max(self.UCBDict, key=lambda x: self.UCBDict[x][0])
        self.SignalValueCountDict[argmax_signal][1] += 1
        self.timestep += 1

        return argmax_signal

    def sample_average_evaluation(self, signal, returned_reward):
        value, count = self.SignalValueCountDict[signal]
        count += 1
        step_size = 1 / count
        value += step_size * (returned_reward - value)
        self.SignalValueCountDict[signal] = [value, count]

    def time_step_UCB(self):
        signal_selection = self.UCB_Selection()
        returned_value = self.testbed.generate_signal_value(signal_selection)
        self.sample_average_evaluation(signal_selection, returned_value)
