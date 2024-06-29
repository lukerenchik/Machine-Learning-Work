import matplotlib.pyplot as plt
import numpy as np


class ViolinPlotter:
    def __init__(self, title="Testbed Visualization", ):
        self.data = {}
        self.title = title


    def add_data(self, name, value, st_dev):
        self.data[name] = (value, st_dev)

    def plot(self):
        fig, ax = plt.subplots()
        positions = np.arange(1, len(self.data) + 1)
        values = []
        names = []
        for name, (value, st_dev) in self.data.items():
            # Generate random data for the violin plot based on the mean and st_dev
            dist_data = np.random.normal(value, st_dev, 1000)
            values.append(dist_data)
            names.append(name)

        # Create violin plots
        ax.violinplot(values, positions, showmeans=True)

        # Setting the names for each violin plot
        ax.set_xticks(positions)
        ax.set_xticklabels(names, rotation=45, ha='right')

        ax.set_ylabel('Value')
        ax.set_title(self.title)

        plt.show()


class AgentVisualizer:
    def __init__(self, estimations, title="title", x_label="x", y_label="y"):
        self.estimations = estimations
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def plot_estimations(self):
        # Extract keys and values from the dictionary
        reward_signals = list(self.estimations.keys())
        expected_rewards = list(self.estimations.values())

        # Creating the bar graph
        plt.figure(figsize=(10, 5))  # Adjust the figure size as needed
        plt.bar(reward_signals, expected_rewards, color='blue')  # Customize color as needed

        # Adding title and labels
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)

        # Optional: Adding value labels on top of each bar
        for i, value in enumerate(expected_rewards):
            rounded_value = round(value, 2)  # Round to 2 decimal places
            plt.text(i, rounded_value + 0.5, f"{rounded_value:.2f}", ha='center', va='bottom')

        # Show the plot
        plt.show()

# Usage example
# plotter = VerticalGraphPlotter("Problem Solving Metrics")
# plotter.add_data("Easy Problem Solve", 10, 2)
# plotter.plot()
