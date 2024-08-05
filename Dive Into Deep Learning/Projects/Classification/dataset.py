import torch
from torch.utils.data import Dataset

class ARFFDataset(Dataset):
    def __init__(self, features, labels, transform = None):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.long)
        self.transform = transform

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        sample = self.features[idx]
        label = self.labels[idx]

        if self.transform:
            sample = self.transform(sample)

        return sample, label
