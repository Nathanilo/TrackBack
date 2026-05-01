import torch
import matplotlib.pyplot as plt
from data_prep import create_training_data
from model import train_model

import os

DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MODEL_PATH = "trackback_weights.pth"

def main():
    print("Starting offline training pipeline...")

    train_loader, test_loader, label_to_song, encoder = create_training_data(DATA_FOLDER)
    num_songs = len(label_to_song)

    trained_model, train_losses, val_losses = train_model(train_loader, test_loader, num_songs, epochs=100)

    print("Saving model weights...")
    torch.save(trained_model.state_dict(), MODEL_PATH)
    print(f"Model successfully saved to '{MODEL_PATH}'.")

    print("Generating learning curve plot...")
    plt.figure(figsize=(10, 6))
    plt.plot(train_losses, label='Training Loss', color='blue', marker='o', markersize=4)
    plt.plot(val_losses, label='Validation Loss', color='orange', marker='o', markersize=4)
    plt.title('TrackBack Network: Learning Curve')
    plt.xlabel('Epochs')
    plt.ylabel('Cross-Entropy Loss')
    plt.legend()
    plt.grid(True)
    
    plt.savefig('learning_curve.png')
    print("Plot saved as 'learning_curve.png'.")

if __name__ == "__main__":
    main()