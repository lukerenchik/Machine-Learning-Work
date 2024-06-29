import random
import numpy as np
import random
from agent import Agent
from graphing_utility import AgentVisualizer
class GradientBandit(Agent):


    def softmax(self, preferences):
        exp_prefs = np.exp(list(preferences.values()))
        sum_exp_prefs = np.sum(exp_prefs)
        return {key: exp_pref / sum_exp_prefs for key, exp_pref in zip(preferences.keys(), exp_prefs)}

    def choose_action(self):
        #This method will choose an action based on the probabilities generated by the softmax function.
        actions = list(self.reward_preferences.keys())
        probabilities = list(self.reward_preferences.values())
        selection_action = random.choices(actions, weights=probabilities, k=1)[0]
        return selection_action
        #This selected action is the key to the gradient_bandit


    def gradient_bandit(self, key, returned_reward, step_size):
        # Every object has a preference value that is assigned and changes each epoch.
        # The preference value is ran through a soft-max function, bounding each preference between 0 and 1.
        # The total sum of preferences after softmax is equal to 1.
        # Initially all actions have an equal probability of being selected.
        # When a below average reward is selected the preference of that action is decreased, all other preferences are increased.
        # When an above average reward is selected the preference of that action is increased, all other preferences are decreased.
        # This algorithm is most effective when a baseline is known, if a baseline is unknown performance preciptiously declines.



        selection_probabilities = self.softmax(self.reward_preferences)

        self.reward_preferences[key] += step_size * (returned_reward - self.expected_rewards[key]) * (1 - selection_probabilities[key])

        for k in self.reward_preferences:
            if k != key:
                self.reward_preferences[k] -= step_size * (returned_reward - self.expected_rewards[k]) * selection_probabilities[k]


    def print_reward_preferences(self):
        if self.reward_preferences:
            for key, value in self.reward_preferences.items():
                print(f"{key}: {value}")
        else:
            print("No reward preferences.")
        pass


    def plot_reward_preferences(self):
        if not self.reward_preferences:
            print("No expected rewards available.")
            return
        visualizer = AgentVisualizer(self.reward_preferences)
        visualizer.plot_estimations()

    def time_step(self):
        #This function will package the choose_action and gradient_bandit steps into one operation callable by the laboratory.
        key = self.choose_action()
        self.gradient_bandit(key, self.testbed.generate_signal_value(key), .1)
        self.print_reward_preferences()
        #self.plot_reward_preferences()