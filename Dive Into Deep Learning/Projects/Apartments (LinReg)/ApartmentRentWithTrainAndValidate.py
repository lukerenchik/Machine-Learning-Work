import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
import torch.optim as optim
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from Dataset import PriceDataset
from LinearRegressionModel import LinearRegressionModel

file_path = '/home/luke/Documents/Ai Dev/Reinforcement-Learning-An-Introduction/Dive Into Deep Learning/Datasets/apartments_for_rent_classified_10K.csv'

# Try reading the CSV with different parameters to handle parsing errors
try:
    df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=';', on_bad_lines='skip')
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

# Initialize the model, loss function, and optimizer
num_features = features.shape[1]
model = LinearRegressionModel(num_features)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.001)

# Training loop
num_epochs = 100
train_loss_values = []
val_loss_values = []

for epoch in range(num_epochs):
    model.train()
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

    average_train_loss = epoch_loss / len(dataloader)
    train_loss_values.append(average_train_loss)

    # Validation step
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for val_batch_features, val_batch_target in dataloader:  # Use a separate validation dataloader
            outputs = model(val_batch_features)
            loss = criterion(outputs, val_batch_target)
            val_loss += loss.item()

    average_val_loss = val_loss / len(dataloader)
    val_loss_values.append(average_val_loss)

    print(f'Epoch [{epoch + 1}/{num_epochs}], Train Loss: {average_train_loss:.4f}, Val Loss: {average_val_loss:.4f}')

# Plotting the loss values with markers
time_steps = list(range(num_epochs))

plt.plot(time_steps, train_loss_values, marker='o', label='Training Loss')
plt.plot(time_steps, val_loss_values, marker='o', label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss Over Time')
plt.legend()
plt.grid(True)
plt.show()
