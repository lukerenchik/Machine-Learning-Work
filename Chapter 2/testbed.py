#Luke Renchik 4/24/24
import random


class testbed:
    def __init__(self, num_signals = 0, step_size_parameter = 0):
        self.observers = []
        self.num_signals = num_signals
        self.signals = {}
        self.step_size_parameter = step_size_parameter
        self.derivatives = ["positive", "negative", "zero", "random"]
        self.derivative_mapping = {
            'positive': (0, 1),
            'negative': (-1, 0),
            'zero': (0, 0),
            'random': (-1, 1),
        }
        # Initialize each signal in the dictionary
        for i in range(num_signals):
            self.signals[f'signal_{i}'] = {'value': 0, 'std_dev': 0, 'derivative': random.choice(self.derivatives)}

    def add_observer(self, observer):
        self.observers.append(observer)


    def print_signals(self):
        print("--- Signals ---")
        for name, info in self.signals.items():
            print(
                f'Signal: {name} Value: {info["value"]} Std_Dev: {info["std_dev"]} Derivative: {info["derivative"]}\n')


    def add_signal(self, name, value, st_dev, derivative):
        if name in self.signals:
            raise ValueError(f"A signal with the name '{name}' already exists.")
        self.signals[name] = {'value': value, 'std_dev': st_dev, 'derivative': derivative}
        self.num_signals += 1  # Increment the number of signals
        self.notify_observers()


    def notify_observers(self):
        for observer in self.observers:
            observer.add_signals_from_testbed(self.signals)

    def signal_walk(self):
        for signal in self.signals.values():
            # Determine the range for the uniform distribution based on the derivative
            range_min, range_max = self.derivative_mapping[signal['derivative']]
            # Update the signal value by sampling from the corresponding uniform distribution
            signal['value'] += random.uniform(range_min, range_max) * signal['std_dev']


    def return_all_signals_as_dictionary(self):
        return dict(self.signals.items())

    import random

    def generate_signal_value(self, key):
        if key in self.signals:
            signal_info = self.signals[key]
            # Generate a new value based on the Gaussian distribution
            new_value = random.gauss(signal_info['value'], signal_info['std_dev'])
            return new_value
        else:
            raise ValueError(f"No signal found for key: {key}")
