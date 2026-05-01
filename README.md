# 💿 TrackBack

TrackBack is a custom Deep Learning pipeline built in PyTorch that maps text queries to their corresponding source documents. It uses a hybrid architecture, leveraging Transfer Learning for feature extraction and a custom neural network for classification. 

Currently, the frontend is themed around an "ABBA Lyric Finder," but the backend is completely generalized and can be trained on any text dataset (legal documents, medical records, FAQs, etc.).

## 🧠 Architecture
This project implements a multi-stage Machine Learning pipeline:
1. **Feature Extraction:** Uses the Hugging Face `all-MiniLM-L6-v2` SentenceTransformer to convert text into 384-dimensional dense semantic embeddings.
2. **Custom Classifier:** A PyTorch Feed-Forward Neural Network (FFNN) containing:
   - Input layer with Gaussian Noise (0.05) for extreme regularization during training.
   - Hidden Layer (128 neurons) with Batch Normalization and ReLU activation.
   - Dropout Layer (p=0.5) to prevent overfitting.
   - Output Layer dynamically sized to the number of classes.
3. **Optimization:** Trained using the Adam optimizer with Weight Decay (1e-3) and a `ReduceLROnPlateau` Learning Rate Scheduler.
4. **Validation:** Implements an 80/20 train/test split, tracks **Top-5 Accuracy**, and features Early Stopping to automatically save the weights of the best-performing epoch.

## 📂 Project Structure
```text
TrackBack/
│
├── scrapper/
│   ├── songs.txt               # List of songs to scrape from Genius Lyrics
│   └── scraper.py              # Script to scrape the data
├── data/                       # Directory for storing raw .txt files (one file per song)
├── trackback_weights.pth       # Saved model weights (Generated after training)
├── learning_curve.png          # Plotted loss metrics (Generated after training)
├── genius_api.env              # Environment file for Genius API credentials (Git ignored)
├── example_genius_api.env      # Example template for setting up API credentials
├── requirements.txt            # Python package dependencies
├── .gitignore                  # Ignored files configuration
├── README.md                   # Project documentation
│
└── src/
    ├── data_prep.py            # Data loading, cleaning, tokenization, and splitting
    ├── model.py                # PyTorch architecture and training loop definition
    ├── train.py                # Offline execution script for training and plotting
    ├── UiConfig.py             # UI configuration, styling, and YouTube links mapping
    └── app.py                  # Streamlit web application for deployment
```

## 🚀 Setup & Execution

### 1. Installation
Clone the repository and install the required dependencies using `pip`:
```bash
pip install -r requirements.txt
```

### 2. Scraping Lyrics (Optional)
If you wish to augment the dataset, you must configure the Genius Lyrics API:
1. Copy `example_genius_api.env` to a new file named `genius_api.env`.
2. Add your Genius API credentials (`GENIUS_CLIENT_ID`, `GENIUS_CLIENT_SECRET`, `GENIUS_ACCESS_TOKEN`).
3. Add any desired songs to `scrapper/songs.txt`.
4. Run the scraper:
   ```bash
   python scrapper/scraper.py
   ```

> [!NOTE]
> **Artist Filter:** By default, `scrapper/scraper.py` contains a strict condition that only downloads and saves lyrics explicitly matched to the artist `"ABBA"`. If you are training TrackBack on a different artist or a generic dataset, open `scrapper/scraper.py` and adjust or remove the `"ABBA"` condition to suit your preference!

### 3. Training the Model
Execute the offline training pipeline. This will process the data, extract embeddings, train the neural network, and generate the learning curve plot:
```bash
python src/train.py
```

### 4. Running the Web App
Launch the interactive Streamlit dashboard:
```bash
streamlit run src/app.py
```