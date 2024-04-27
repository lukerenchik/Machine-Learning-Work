from testbed import testbed as TB
from graphing_utility import ViolinPlotter as VGP
testbed = TB(num_signals=0, step_size_parameter=.1)

testbed.add_signal(name = "Easy_Problem_Solve", value =  10, st_dev = 2, derivative =  "negative")
testbed.add_signal("Medium_Problem_Solve" , 25, 5, "zero")
testbed.add_signal("Hard_Problem_Solve", 50, 15, "positive")

vertical_plotter = VGP("Reward Distribution")

signal_dictionary = testbed.return_all_signals_as_dictionary()

for signal_name, attrs in signal_dictionary.items():
    vertical_plotter.add_data(name=signal_name, value = attrs["value"], st_dev = attrs["std_dev"])

vertical_plotter.plot()

testbed.print_signals()

testbed.signal_walk()

testbed.print_signals()

for i in range(4):
    testbed.signal_walk()

testbed.print_signals()