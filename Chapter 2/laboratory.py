from testbed import testbed as TB

testbed = TB(num_signals=0, step_size_parameter=.1)

testbed.add_signal("Easy_Problem_Solve", 10, 2, "negative")
testbed.add_signal("Medium_Problem_Solve" , 25, 5, "zero")
testbed.add_signal("Hard_Problem_Solve", 50, 15, "positive")

testbed.print_signals()

testbed.signal_walk()

testbed.print_signals()

for i in range(4):
    testbed.signal_walk()

testbed.print_signals()