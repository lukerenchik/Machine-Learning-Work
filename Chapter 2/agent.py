import random
from graphing_utility import AgentVisualizer

#TODO: Create Superclass Agent, which has three child classes, Sample_Average_Bandit,
# Gradient_Ascent_Bandit, Associative Search, Upper Confidence Bound Action Selection
class Agent:

    def __init__(self, testbed, exploration_rate=0.1):
        self.num_signals = testbed.num_signals
        self.expected_rewards = {}
        self.reward_preferences = {}
        self.exploration_rate = exploration_rate
        self.counts = {}
        self.testbed = testbed


    def add_signals_from_testbed(self, signals):
        for signal_name in signals.keys():
            if signal_name not in self.expected_rewards.keys():
                self.expected_rewards[signal_name] = 0.5
            if signal_name not in self.testbed.signals.keys():
                self.testbed[signal_name] = signals[signal_name]
            if signal_name not in self.reward_preferences.keys():
                self.reward_preferences[signal_name] = 1 / len(signals)


    def print_expected_rewards(self):
        if self.expected_rewards:
            for key, value in self.expected_rewards.items():
                print(f"{key}: {value}")
        else:
            print("No expected rewards available.")
        pass

    def plot_expected_values(self):
        if not self.expected_rewards:
            print("No expected rewards available.")
            return

        #TODO: Return Metadata and send to graphing utility
        visualizer = AgentVisualizer(self.expected_rewards)
        visualizer.plot_estimations()



