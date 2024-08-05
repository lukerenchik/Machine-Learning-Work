# Training Loop
import torch


class TrainingLoop:
    def __init__(self, model, train_loader, val_loader, criterion, optimizer, num_epochs=25):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.num_epochs = num_epochs

    def train_model(self):
        for epoch in range(self.num_epochs):
            self.model.train()
            running_loss = 0.0

            for inputs, labels in self.train_loader:
                # Zero the parameter gradients
                self.optimizer.zero_grad()

                # Forward Pass
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)

                # Back Prop & Optimize
                loss.backward()
                self.optimizer.step()

                running_loss += loss.item()

            epoch_loss = running_loss / len(self.train_loader)
            val_loss, val_acc = self.validate_model()

            print(
                f"Epoch {epoch + 1}/{self.num_epochs}, Training Loss: {epoch_loss:.4f}, Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_acc:.4f}")

    def validate_model(self):
        self.model.eval()
        val_loss = 0.0
        correct = 0

        with torch.no_grad():
            for inputs, labels in self.val_loader:
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                val_loss += loss.item()

                _, preds = torch.max(outputs, 1)
                correct += torch.sum(preds == labels.data)

        val_loss /= len(self.val_loader)
        val_acc = correct.double() / len(self.val_loader.dataset)

        return val_loss, val_acc

    def test_model(self, test_loader):
        self.model.eval()
        correct = 0

        with torch.no_grad():
            for inputs, labels in test_loader:
                outputs = self.model(inputs)
                _, preds = torch.max(outputs, 1)
                correct += torch.sum(preds == labels.data)

        accuracy = correct.double() / len(test_loader.dataset)
        print(f"Test Accuracy: {accuracy:.4f}")