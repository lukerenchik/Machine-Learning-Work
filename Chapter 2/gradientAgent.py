import random
from graphing_utility import AgentVisualizer


class GradientAgent():

    def __init__(self, testbed, exploration_rate=0.1):
        self.num_signals = testbed.num_signals
        self.expected_rewards = {}
        self.reward_preference = {}
        self.exploration_rate = exploration_rate
        self.counts = {}
        self.testbed = testbed


    def add_signals_from_testbed(self, signals):
        for signal_name in signals.keys():
            if signal_name not in self.expected_rewards.keys():
                self.expected_rewards[signal_name] = 0.5
            if signal_name not in self.testbed.signals.keys():
                self.testbed[signal_name] = signals[signal_name]
            if signal_name not in self.reward_preference.keys():
                self.reward_preference[signal_name] = 1 / len(signals)


