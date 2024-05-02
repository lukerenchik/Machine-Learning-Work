import random
from graphing_utility import AgentVisualizer


class Agent:

    def __init__(self, testbed, exploration_rate=0.1):
        self.num_signals = testbed.num_signals
        self.expected_rewards = {}
        self.exploration_rate = exploration_rate
        self.counts = {}

        # I believe this line of code is now unecessary
        # for reward_signal in testbed.signals:
        #    self.expected_rewards[reward_signal] = 0.5

    def add_signals_from_testbed(self, signals):
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
            #TODO: This needs to return the actual signal from Testbed
        else:
            return None

    def explore(self):
        if self.expected_rewards:
            random_key = random.choice(list(self.expected_rewards.keys()))
            return self.expected_rewards[random_key]
            #TODO: This needs to return the actual signal from Testbed
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

    def sample_average_evaluation(self, key, returned_value):
        if key not in self.expected_rewards:
            self.expected_rewards[key] = returned_value
            self.counts[key] = 1
        else:
            self.counts[key] += 1
            step_size = 1 / self.counts[key]
            self.expected_rewards[key] = self.expected_rewards[key] + step_size * (
                        returned_value - self.expected_rewards[key])

    def time_step(self):
        #TODO: This should house all of the necessary calls to execute a time walk if parameters are kept constant.
        pass


# Running a cycle should look like this:
# 1. Choose Type of Action
# 2. Execute Action
# 3. Display Reward Signal
# 4. Update Equations
