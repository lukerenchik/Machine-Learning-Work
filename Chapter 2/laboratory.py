from testbed import testbed as TB
from graphing_utility import ViolinPlotter as VGP
from sampleAverageBandit import SampleAverageBandit as SAB
from gradientBandit import GradientBandit
from upperConfidenceActionBandit import UpperConfidenceActionBandit
#TODO: Todo statements are used for text highlighting to better see the seperate sections of code in this file.

#TODO: Object Setup, These Shouldn't have to be modified.
testbed = TB(num_signals=0, step_size_parameter=.1)
sampleAverageBandit = SAB(testbed)
gradientBandit = GradientBandit(testbed)
upperConfidenceBandit = UpperConfidenceActionBandit(testbed)


testbed.add_observer(sampleAverageBandit)
testbed.add_observer(gradientBandit)
testbed.add_observer(upperConfidenceBandit)


#TODO: Example for Three Functions with Very Different Expected Rewards, Highlights the need for exploration.
#testbed.add_signal(name="Easy_Problem_Solve", value=10, st_dev=2, derivative="negative")
#testbed.add_signal("Medium_Problem_Solve", 25, 5, "zero")
#testbed.add_signal("Hard_Problem_Solve", 50, 15, "positive")


#TODO: Test for 10 moving signals, these can be modified to simulate different behavior
#TODO: Signal Set 1.
'''
testbed.add_signal("sig_1", 0, .1, "positive")
testbed.add_signal("sig_2", 0, .5, "positive")
testbed.add_signal("sig_3", 0, 1, "positive")
testbed.add_signal("sig_4", 0, .1, "negative")
testbed.add_signal("sig_5", 0, .5, "negative")
testbed.add_signal("sig_6", 0, 1, "negative")
testbed.add_signal("sig_7", 0, 1, "zero")
testbed.add_signal("sig_8", 0, .1, "random")
testbed.add_signal("sig_9", 0, .5, "random")
'''

#TODO: Signal Set 2.

testbed.add_signal("Positive Fast 50", 50, 1, "positive")
testbed.add_signal("Positive Faster -3", -3, 1.2, "positive")
testbed.add_signal("Positive Slow 100", 100, .5, "positive")
testbed.add_signal("Negative Slow 10", 10, .1, "negative")
testbed.add_signal("Negative Medium 100", 100, .5, "negative")
testbed.add_signal("Negative Fast 1000", 1000, 1, "negative")
testbed.add_signal("Zero Fast 10", 10, 1, "zero")
testbed.add_signal("Random Slow 20", 20, .1, "random")
testbed.add_signal("Random Medium 30", 30, .5, "random")



#TODO: Main Loop for Sample-Average
'''
sampleAverageBandit.print_expected_rewards()

for i in range(10000):
    testbed.signal_walk()
    sampleAverageBandit.time_step()
    if i % 1000 == 0:
        sampleAverageBandit.plot_expected_values()

'''

#TODO: Main Loop for Gradient
'''
for i in range(10000):
    testbed.signal_walk()
    gradientBandit.time_step()
    if i % 1000 == 0:
        gradientBandit.print_reward_preferences()
        gradientBandit.plot_reward_preferences()
'''

#TODO: Main Loop for UCB

upperConfidenceBandit.dictionary_init()

for i in range(100):
    testbed.signal_walk()
    upperConfidenceBandit.time_step_UCB()
    if i % 10 == 0:
        print(upperConfidenceBandit.UCBDict)
        print(upperConfidenceBandit.SignalValueCountDict)
        upperConfidenceBandit.print_expected_rewards()
        upperConfidenceBandit.plot_expected_values()




#TODO: I don't remember what this code was for, but I am pretty sure it is purely experimental

# agent.print_expected_rewards()
# vertical_plotter = VGP("Reward Distribution")
# agent.plot_expected_values()
# signal_dictionary = testbed.return_all_signals_as_dictionary()
# for signal_name, attrs in signal_dictionary.items():
# vertical_plotter.add_data(name=signal_name, value = attrs["value"], st_dev = attrs["std_dev"])
# vertical_plotter.plot()
# testbed.print_signals()
# testbed.signal_walk()
# testbed.print_signals()