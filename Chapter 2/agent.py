import random
from graphing_utility import AgentVisualizer

#TODO: Create Superclass Agent, which has three child classes, Sample_Average_Bandit,
# Gradient_Ascent_Bandit, Associative Search, Upper Confidence Bound Action Selection
class Agent:

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


    def choose_action(self):
        random_value = random.random()

        if random_value < self.exploration_rate:
            return self._explore()
        else:
            return self._exploit()

    def _exploit(self):
        if self.expected_rewards:
            max_key = max(self.expected_rewards, key=self.expected_rewards.get)
            return self.testbed.generate_signal_value(max_key), max_key
        else:
            return None

    def _explore(self):
        if self.expected_rewards:
            random_key = random.choice(list(self.expected_rewards.keys()))
            return self.testbed.generate_signal_value(random_key), random_key
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

        #TODO: Return Metadata and send to graphing utility
        visualizer = AgentVisualizer(self.expected_rewards)
        visualizer.plot_estimations()

    def sample_average_evaluation(self, key, returned_reward):
        if key not in self.expected_rewards:
            self.expected_rewards[key] = returned_reward
            self.counts[key] = 1
        elif key not in self.counts:
            self.counts[key] = 1
            step_size = 1 / self.counts[key]
            self.expected_rewards[key] = self.expected_rewards[key] + step_size * (
                    returned_reward - self.expected_rewards[key])
        else:
            self.counts[key] += 1
            step_size = 1 / self.counts[key]
            self.expected_rewards[key] = self.expected_rewards[key] + step_size * (
                    returned_reward - self.expected_rewards[key])

    def gradient_bandit(self, key, returned_reward, step_size):
        # Every Object has a Preference value, which is generated through a soft-max function, and all objects add up to 1
        # The probabilitiy of taking action A at time T is pi_t, initally all actions have an equal probability of being selected
        # When a action is selected and its reward is below the average previous rewards then decrease its preference, otherwise increase its preference
        # When a preference is increased/decreased all other preferences move in the opposite direction to make room for the movement in the selected object
        # This algorithm is most effective when a baseline is known, if a baseline is unknown performance preciptiously declines.

        self.reward_preference[key] += step_size * (returned_reward - self.expected_rewards[key]) * (1 - probability_of_selecting[key])

        for k in self.reward_preference:
            if k != key:
                self.reward_preference[k] -= step_size * (returned_reward - self.expected_rewards[key]) * \
                                             probability_of_selecting[k]

    def time_step(self):
        returned_value, key = self.choose_action()
        print(f"Signal {key} was tested, result was {returned_value}")
        self.sample_average_evaluation(key, returned_value)
        print("Expected Rewards have been updated:")
        self.print_expected_rewards()



# Running a cycle should look like this:
# 1. Choose Type of Action
# 2. Execute Action
# 3. Display Reward Signal
# 4. Update Equations
