import torch
import torch.nn as nn
import torch.optim as optim
import copy

class TrackBackNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_songs):
        super(TrackBackNetwork, self).__init__()
        self.layer1 = nn.Linear(input_size, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(p=0.5) 
        
        self.layer2 = nn.Linear(128, num_songs)

    def forward(self, x):
        if self.training:
            # Add Gaussian noise to input embeddings during training to combat overfitting
            x = x + torch.randn_like(x) * 0.05
            
        out = self.layer1(x)
        out = self.bn1(out)
        out = self.relu1(out)
        out = self.dropout1(out)
        
        out = self.layer2(out)
        return out

def train_model(train_loader, test_loader, num_songs, epochs=100):
    print("Initializing model training sequence with Adam and Regularization...")
    
    # Use MPS if available (Apple Silicon), otherwise CPU
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")
    
    model = TrackBackNetwork(384, 256, num_songs).to(device)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-3)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=10)
    
    train_loss_history = []
    val_loss_history = []
    
    best_accuracy = 0.0
    best_model_weights = copy.deepcopy(model.state_dict())
    patience_counter = 0
    early_stopping_patience = 25
    
    for epoch in range(epochs):
        model.train()
        total_train_loss = 0
        
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()
            
        avg_train_loss = total_train_loss / len(train_loader)
        train_loss_history.append(avg_train_loss)
        
        model.eval()
        total_val_loss = 0
        correct_guesses = 0
        total_samples = 0
        
        with torch.no_grad():
            for batch_X, batch_y in test_loader:
                batch_X, batch_y = batch_X.to(device), batch_y.to(device)
                predictions = model(batch_X)
                loss = criterion(predictions, batch_y)
                total_val_loss += loss.item()
                
                # Calculate Top-5 Accuracy because the UI displays 5 matches total
                top_5_guesses = torch.topk(predictions, 5, dim=1).indices
                correct_guesses += (batch_y.view(-1, 1) == top_5_guesses).sum().item()
                total_samples += batch_y.size(0)
                
        avg_val_loss = total_val_loss / len(test_loader)
        val_loss_history.append(avg_val_loss)
        accuracy = (correct_guesses / total_samples) * 100
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model_weights = copy.deepcopy(model.state_dict())
            patience_counter = 0
        else:
            patience_counter += 1
            
        scheduler.step(accuracy)
        
        if (epoch + 1) % 10 == 0 or epoch == 0:
            print(f"Epoch [{epoch+1}/{epochs}] | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f} | Top-5 Accuracy: {accuracy:.2f}%")
        
        if patience_counter >= early_stopping_patience:
            print(f"Early stopping triggered at epoch {epoch+1}")
            break
        
    print(f"Training sequence complete. Best Top-5 Accuracy achieved: {best_accuracy:.2f}%")
    
    model.load_state_dict(best_model_weights)
    
    return model, train_loss_history, val_loss_history