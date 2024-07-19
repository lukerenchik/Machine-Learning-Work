import pandas as pd
import math
import numpy as np
import torch
from torch import nn
import inspect
import collections
from Module import Module
from HyperParameters import HyperParameters
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim

file_path = '/Dive Into Deep Learning/Datasets/apartments_for_rent_classified_10K.csv'

df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';')

features = df.drop(columns=['price']).values
target = df['price'].values

features = np.array(features)
target = np.array(target)

features_tensor = torch.tensor(features, dtype=torch.float32)
target_tensor = torch.tensor(target, dtype=torch.float32).view(-1, 1)

class PriceDataset(Dataset):
    def __init__(self, features, target):
        self.features = features
        self.target = target

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.target[idx]



dataset = PriceDataset(features_tensor, target_tensor)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)




class ApartmentLinearRegression(Module):
    def __init__(self, num_features, learn_rate, st_dev=0.01):
        super().__init__()
        self.save_hyperparameters()
        self.weights = torch.normal(0, st_dev, (num_features, 1), requires_grad=True)
        self.bias = torch.zeros(1, requires_grad=True)

    def forward(self, X):
        return torch.matmul(X, self.weights) + self.bias

    def loss(self, y_pred, y_true):
        loss = (y_pred - y_true)**2 / 2
        return loss.mean()

    def configure_optimizers(self):
        return MinibatchStochasticGradientDescent([self.weights, self.bias], self.learn_rate)


class MinibatchStochasticGradientDescent(HyperParameters):
    def __init__(self, _params, _learning_rate):
        self.save_hyperparameters()
        self.params = _params
        self.learning_rate = _learning_rate

    def step(self):
        for param in self.params:
            param -= self.learning_rate * param.grad

    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()






model = ApartmentLinearRegression(21, learn_rate=0.03)
data =
