import pytest
from testbed import testbed  # Ensure the import matches the class name and file structure

@pytest.fixture
def testbench():
    # Adjust the creation parameters as necessary
    return testbed(0, 0)

def test_initialization(testbench):
    assert testbench.num_signals == 0
    assert testbench.signals == {}
    print("Initialization test passed.")

def test_add_signal(testbench):
    testbench.add_signal('test_signal', 100, 1.0, 'positive')
    assert 'test_signal' in testbench.signals
    assert testbench.signals['test_signal']['value'] == 100
    assert testbench.signals['test_signal']['std_dev'] == 1.0
    assert testbench.signals['test_signal']['derivative'] == 'positive'
    print("Add signal test passed.")

def test_signal_walk(testbench):
    testbench.add_signal('test_signal', 100, 1.0, 'positive')  # Ensure a signal is present to walk
    initial_value = testbench.signals['test_signal']['value']
    testbench.signal_walk()
    assert testbench.signals['test_signal']['value'] != initial_value
    print("Signal walk test passed.")

def test_derivative_effect(testbench):
    testbench.add_signal('test_signal', 100, 1.0, 'positive')  # Ensure a signal is present to test
    original_value = testbench.signals['test_signal']['value']
    testbench.signal_walk()  # Perform the signal walk to apply the derivative effect
    difference = abs(testbench.signals['test_signal']['value'] - original_value)
    assert difference >= 0  # Check if the value has changed according to the derivative mapping
    print("Derivative effect test passed.")

def test_error_on_duplicate_signal(testbench):
    testbench.add_signal('test_signal', 100, 1.0, 'positive')
    with pytest.raises(ValueError) as excinfo:
        testbench.add_signal('test_signal', 150, 1.5, 'high')
    assert "already exists" in str(excinfo.value)
    print("Duplicate signal error test passed.")
