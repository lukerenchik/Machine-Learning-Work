from agent import Agent
import random


class SampleAverageBandit(Agent):
    def update_expected_rewards(self, key, returned_reward):
        if key not in self.expected_rewards:
            self.expected_rewards[key] = returned_reward
            self.counts[key] = 1
        else:
            self.counts[key] += 1
            step_size = 1 / self.counts[key]
            self.expected_rewards[key] += step_size * (returned_reward - self.expected_rewards[key])

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

    def time_step(self):
        returned_value, key = self.choose_action()
        print(f"Signal {key} was tested, result was {returned_value}")
        self.sample_average_evaluation(key, returned_value)
        print("Expected Rewards have been updated:")
        self.print_expected_rewards()