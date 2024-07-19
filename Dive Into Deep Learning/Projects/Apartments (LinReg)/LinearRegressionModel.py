import torch.nn as nn


class LinearRegressionModel(nn.Module):
    def __init__(self, num_features):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(num_features, 1)

    def forward(self, x):
        return self.linear(x)
