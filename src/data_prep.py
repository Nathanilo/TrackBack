import os
import re
import torch
from torch.utils.data import Dataset, DataLoader
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split

import string
from collections import defaultdict

class LyricsDataset(Dataset):
    def __init__(self, embeddings, labels):
        self.embeddings = embeddings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.embeddings[idx], self.labels[idx]

def create_training_data(data_folder):
    print("Initializing data preprocessing...")
    label_to_song = {}
    
    print("Loading SentenceTransformer model...")
    encoder = SentenceTransformer('all-MiniLM-L6-v2')

    song_id = 0
    raw_song_lines = defaultdict(list)
    line_to_songs = defaultdict(set)
    
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            title = filename.replace(".txt", "")
            label_to_song[song_id] = title
            
            with open(os.path.join(data_folder, filename), "r", encoding="utf-8") as file:
                clean_text = re.sub(r'\[.*?\]', '', file.read())
                lines = [line.strip() for line in clean_text.split('\n') if len(line.strip()) > 10]
                
                for line in lines:
                    normalized_line = line.lower().translate(str.maketrans('', '', string.punctuation))
                    normalized_line = " ".join(normalized_line.split())
                    
                    if len(normalized_line) > 10:
                        raw_song_lines[song_id].append(normalized_line)
                        line_to_songs[normalized_line].add(song_id)
            song_id += 1

    lyrics, labels = [], []
    for sid, lines in raw_song_lines.items():
        for line in lines:
            if len(line_to_songs[line]) == 1:
                lyrics.append(line)
                labels.append(sid)

    print(f"Processed {len(lyrics)} distinct lyric segments across {song_id} songs.")
    print("Generating embeddings. Please wait...")
    # Use MPS if available, otherwise CPU
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    X_tensors = encoder.encode(lyrics, convert_to_tensor=True).to(device)
    y_tensors = torch.tensor(labels, dtype=torch.long).to(device)

    print("Splitting dataset into training and validation sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_tensors, y_tensors, test_size=0.2, random_state=42
    )

    train_dataset = LyricsDataset(X_train, y_train)
    test_dataset = LyricsDataset(X_test, y_test)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    return train_loader, test_loader, label_to_song, encoder