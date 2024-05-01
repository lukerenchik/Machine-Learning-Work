import random
from graphing_utility import AgentVisualizer

class Agent:

    def __init__(self, testbed, exploration_rate=0.1):
        self.num_signals = testbed.num_signals
        self.expected_rewards = {}
        self.exploration_rate = exploration_rate

        for reward_signal in testbed.signals:
            self.expected_rewards[reward_signal] = 0.5


    def update_signals(self, signals):
        for signal_name in signals.keys():
            if signal_name not in self.expected_rewards.keys():
                self.expected_rewards[signal_name] = 0.5


    def choose_action(self):
        random_value = random.random()

        if random_value < self.exploration_rate:
            return self.explore()
        else:
            return self.exploit()

    def exploit(self):
        if self.expected_rewards:
            max_key = max(self.expected_rewards, key=self.expected_rewards.get)
            return self.expected_rewards[max_key]
        else:
            return None

    def explore(self):
        if self.expected_rewards:
            random_key = random.choice(list(self.expected_rewards.keys()))
            return self.expected_rewards[random_key]
        else:
            return None

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

        visualizer = AgentVisualizer(self.expected_rewards)
        visualizer.plot_estimations()


    def sample_average_evaluation(self):
        # TODO: Implement sample-average algroithm for reward evaluation.
        pass

    def exponential_recency_weighted_average(self):
        # TODO: Implement exponential recency weighted average algorithm for non-stationary problems.
        pass



# Running a cycle should look like this:
# 1. Choose Type of Action
# 2. Execute Action
# 3. Display Reward Signal
# 4. Update Equations
