import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader
from Dataset import PriceDataset
import torch.optim as optim
from LinearRegressionModel import LinearRegressionModel
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
import csv
import matplotlib.pyplot as plt

file_path = '/home/luke/Documents/Ai Dev/Reinforcement-Learning-An-Introduction/Dive Into Deep Learning/Datasets/apartments_for_rent_classified_10K.csv'

# Try reading the CSV with different parameters to handle parsing errors
try:
    df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';', on_bad_lines='skip', quoting=csv.QUOTE_NONE)
except pd.errors.ParserError:
    print("Error reading the CSV file. Please check the file for inconsistencies.")
    exit()

feature_columns = ['bathrooms', 'bedrooms', 'square_feet']
target_column = 'price'

# Fill NaNs with 0 for both features and target columns
df[feature_columns] = df[feature_columns].fillna(0)
df[target_column] = df[target_column].fillna(0)

# Extract features and target
features = df[feature_columns].values
target = df[target_column].values

# Normalize the features
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Optionally, normalize the target if it varies significantly in scale
# target = scaler.fit_transform(target.reshape(-1, 1)).flatten()

# Convert to PyTorch tensors
features_tensor = torch.tensor(features, dtype=torch.float32)
target_tensor = torch.tensor(target, dtype=torch.float32).view(-1, 1)

# Check for NaN or infinite values
assert not np.isnan(features).any(), "Features contain NaN values"
assert not np.isnan(target).any(), "Target contains NaN values"
assert np.isfinite(features).all(), "Features contain infinite values"
assert np.isfinite(target).all(), "Target contains infinite values"

# Create a DataLoader
dataset = PriceDataset(features_tensor, target_tensor)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)


# Define the model

# Initialize the model, loss function, and optimizer
num_features = features.shape[1]
model = LinearRegressionModel(num_features)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.001)

# Training loop
num_epochs = 100
loss_values = []

for epoch in range(num_epochs):
    epoch_loss = 0
    for batch_features, batch_target in dataloader:
        # Forward pass
        outputs = model(batch_features)
        loss = criterion(outputs, batch_target)

        # Check for NaN loss
        if torch.isnan(loss):
            raise ValueError("Loss is NaN during training")

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()

    average_loss = epoch_loss / len(dataloader)
    loss_values.append(average_loss)

    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {average_loss:.4f}')

# Plotting the loss values
time_steps = list(range(num_epochs))

plt.plot(time_steps, loss_values, marker='o')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss Over Time')
plt.grid(True)
plt.show()
