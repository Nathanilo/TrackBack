import os
import torch
import streamlit as st
from data_prep import create_training_data
from model import TrackBackNetwork
from UiConfig import get_theme, inject_css, render_theme_toggle, render_header, render_results

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "trackback_weights.pth")

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ABBA TrackBack",
    page_icon="💿",
    layout="centered",
)

# ── Theme ──────────────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

T = get_theme()
inject_css(T)
render_theme_toggle(T)
render_header()

# ── Pre-flight Check ────────────────────────────────────────────────────────────
if not os.path.exists(MODEL_PATH):
    st.error("⚠️ Model weights not found.")
    st.info("Run `python src/train.py` to train the model before launching this app.")
    st.stop()

# ── Resource Loading ────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_resources():
    _, _, label_to_song, encoder = create_training_data(DATA_FOLDER)
    num_songs = len(label_to_song)

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = TrackBackNetwork(input_size=384, hidden_size=256, num_songs=num_songs)
    model.load_state_dict(torch.load(MODEL_PATH, weights_only=True))
    model = model.to(device)
    model.eval()

    return label_to_song, encoder, model, device

with st.spinner("Warming up the band..."):
    label_to_song, encoder, model, device = load_resources()

# ── Search Input ────────────────────────────────────────────────────────────────
if "run_search" not in st.session_state:
    st.session_state.run_search = False

def on_enter():
    st.session_state.run_search = True

input_col, btn_col = st.columns([5, 1])
with input_col:
    user_query = st.text_input(
        "Lyric Snippet",
        placeholder='e.g. "you are the dancing queen, young and sweet..."',
        on_change=on_enter,
        key="query_input",
    )
with btn_col:
    st.markdown("<div style='height: 1.95rem'></div>", unsafe_allow_html=True)
    if st.button("Search", use_container_width=True):
        st.session_state.run_search = True

# ── Inference ──────────────────────────────────────────────────────────────────
if st.session_state.run_search and user_query:
    st.session_state.run_search = False

    with st.spinner("Searching the ABBA catalogue..."):
        query_tensor = encoder.encode(user_query, convert_to_tensor=True).to(device)
        
        # Ensure tensor is 2D (batch_size=1) for BatchNorm
        if query_tensor.dim() == 1:
            query_tensor = query_tensor.unsqueeze(0)

        with torch.no_grad():
            predictions = model(query_tensor).squeeze(0)

        probabilities = torch.nn.functional.softmax(predictions, dim=0)
        top_probs, top_indices = torch.topk(probabilities, 5)

    strong_matches, similar_matches = [], []

    for i in range(5):
        prob = top_probs[i].item()
        song_name = label_to_song[top_indices[i].item()]

        if prob > 0.60:
            strong_matches.append((song_name, prob))
        elif prob > 0.05:
            similar_matches.append((song_name, prob))

    if not strong_matches and similar_matches:
        strong_matches.append(similar_matches.pop(0))

    render_results(strong_matches, similar_matches)