class Agent:

    def __init__(self, testbed, exploration_rate=0.1):
        self.num_signals = testbed.num_signals
        self.expected_rewards = {}
        self.exploration_rate = exploration_rate

        for reward_signal in testbed.signals:
            self.expected_rewards[reward_signal] = 0.5

    def choose_action(self):
        #TODO: Randomly generate value between 0 and 1, if below exploration rate, call explore function, else call exploit function.
        pass

    def find_exploitable_reward(self):
        #TODO: Search dictionary for highest value, (return the value | execute evaluation on that value).
        pass

    def find_exploratory_reward(self):
        #TODO: Randomly select a reward
        pass

    def print_expect_values(self):
        #TODO: Create a plot that demonstrates machines current thinking.
        pass

    def sample_average_evaluation(self):
        #TODO: Implement sample-average algroithm for reward evaluation.
        pass

    def exponential_recency_weighted_average(self):
        #TODO: Implement exponential recency weighted average algorithm for non-stationary problems.
        pass


    def print_expected_rewards(self):
        for reward_signal in self.expected_rewards:
            print(f"{reward_signal}: {self.expected_rewards[reward_signal]}")
