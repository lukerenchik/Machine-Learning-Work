from scipy.io import arff
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import torch
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from models import SoftmaxRegression
import torch.nn as nn
import torch.optim as optim
from train import TrainingLoop

# Transform our data from .arff to a Pandas Dataframe
data, meta = arff.loadarff(
    "C:\Dev\Reinforcement-Learning-An-Introduction\Dive Into Deep Learning\Projects\Classification\DryBeanDataset\Dry_Bean_Dataset.arff")
df = pd.DataFrame(data)

X = df.drop("Class", axis=1)
y = df["Class"]

# Splitting Data into Train & Test Split
X_train, X_test1, y_train, y_test1 = train_test_split(X, y, test_size=0.3, random_state=42)

# Splitting Test Set into Two Subsets
X_test1, X_test2, y_test1, y_test2, = train_test_split(X_test1, y_test1, test_size=0.5, random_state=42)

# Creating a Validation set from Training Set
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Normalize the Feature Data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test1 = scaler.transform(X_test1)
X_test2 = scaler.transform(X_test2)

# Encode the Labels
le = LabelEncoder()
y_train = le.fit_transform(y_train)
y_val = le.transform(y_val)
y_test1 = le.transform(y_test1)
y_test2 = le.transform(y_test2)

# Converting to Tensors

X_train_tensor = torch.from_numpy(X_train).float()
y_train_tensor = torch.from_numpy(y_train).long()

X_val_tensor = torch.from_numpy(X_val).float()
y_val_tensor = torch.from_numpy(y_val).long()

X_test1_tensor = torch.from_numpy(X_test1).float()
y_test1_tensor = torch.from_numpy(y_test1).long()

X_test2_tensor = torch.from_numpy(X_test2).float()
y_test2_tensor = torch.from_numpy(y_test2).long()

# Creating DataSets
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
val_dataset = TensorDataset(X_val_tensor, y_val_tensor)
test1_dataset = TensorDataset(X_test1_tensor, y_test1_tensor)
test2_dataset = TensorDataset(X_test2_tensor, y_test2_tensor)

# Creating Dataloaders
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
test1_loader = DataLoader(test1_dataset, batch_size=64, shuffle=False)
test2_loader = DataLoader(test2_dataset, batch_size=64, shuffle=False)

# Parameters for Softmax Regression Model
input_dim = X_train.shape[1]
output_dim = len(set(y_train))
model = SoftmaxRegression(input_dim, output_dim)

# Parameters for Training Loop
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Training Loop
tl = TrainingLoop(model, train_loader, val_loader, criterion, optimizer, num_epochs=25)
tl.train_model()
tl.test_model(test1_loader)
tl.test_model(test2_loader)
