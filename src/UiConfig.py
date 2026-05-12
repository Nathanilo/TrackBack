# ── UI Configuration ───────────────────────────────────────────────────────────
# All theme palettes, CSS, and HTML rendering helpers for the TrackBack app.

import streamlit as st

# ── Theme Palettes ─────────────────────────────────────────────────────────────
LIGHT = {
    "bg":             "#faf7f0",
    "bg_gradient":    "radial-gradient(ellipse 80% 50% at 50% -5%, #f5e6b855 0%, transparent 65%)",
    "grid_color":     "rgba(180,140,40,0.06)",
    "text":           "#1a1530",
    "subtitle":       "#7a6e8a",
    "divider":        "#c8a830",
    "input_bg":       "#ffffff",
    "input_border":   "rgba(180,140,40,0.35)",
    "input_focus":    "rgba(180,140,40,0.75)",
    "input_shadow":   "rgba(180,140,40,0.15)",
    "input_text":     "#1a1530",
    "label_color":    "#7a6e8a",
    "card_border":    "rgba(0,0,0,0.07)",
    "card_strong_bg": "rgba(200,168,48,0.09)",
    "card_similar_bg":"rgba(100,80,160,0.07)",
    "song_name":      "#1a1530",
    "no_match":       "#9a8eaa",
    "toggle_icon":    "🌙",
    "toggle_label":   "Dark mode",
}

DARK = {
    "bg":             "#0d0b14",
    "bg_gradient":    "radial-gradient(ellipse 80% 60% at 50% -10%, #3a1a6e55 0%, transparent 70%)",
    "grid_color":     "rgba(255,215,0,0.04)",
    "text":           "#f5edd8",
    "subtitle":       "#c8bada",
    "divider":        "#f5d060",
    "input_bg":       "rgba(255,255,255,0.08)",
    "input_border":   "rgba(245,208,96,0.45)",
    "input_focus":    "rgba(245,208,96,0.9)",
    "input_shadow":   "rgba(245,208,96,0.18)",
    "input_text":     "#f5edd8",
    "label_color":    "#d0c0e8",
    "card_border":    "rgba(255,255,255,0.12)",
    "card_strong_bg": "rgba(245,208,96,0.13)",
    "card_similar_bg":"rgba(150,130,210,0.16)",
    "song_name":      "#f5edd8",
    "no_match":       "#a090c0",
    "toggle_icon":    "☀️",
    "toggle_label":   "Light mode",
}


def get_theme() -> dict:
    """Return the active palette based on session state."""
    return DARK if st.session_state.get("dark_mode", False) else LIGHT


def inject_css(T: dict) -> None:
    """Inject the full themed stylesheet into the Streamlit page."""
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
    background-color: {T["bg"]} !important;
    color: {T["text"]} !important;
    font-family: 'DM Sans', sans-serif;
    transition: background-color 0.3s, color 0.3s;
}}
[data-testid="stAppViewContainer"] {{
    background-image:
        {T["bg_gradient"]},
        repeating-linear-gradient(0deg,  transparent, transparent 60px, {T["grid_color"]} 60px, {T["grid_color"]} 61px),
        repeating-linear-gradient(90deg, transparent, transparent 60px, {T["grid_color"]} 60px, {T["grid_color"]} 61px);
}}

/* Hide Streamlit chrome */
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ display: none; }}

/* ── Header ── */
.abba-header {{
    text-align: center;
    padding: 1.5rem 0 1.5rem;
}}
.abba-header .disco-icon {{
    font-size: 3rem;
    display: block;
    margin-bottom: 0.5rem;
    animation: spin 8s linear infinite;
}}
@keyframes spin {{
    from {{ transform: rotate(0deg); }}
    to   {{ transform: rotate(360deg); }}
}}
.main-logo {{
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #c8a830 0%, #e8a020 45%, #a07010 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}}
.b-flip {{
    display: inline-block;
    transform: scaleX(-1);
}}
.abba-header .subtitle {{
    font-size: 0.95rem;
    color: {T["subtitle"]};
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}}

/* ── Divider ── */
.gold-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, {T["divider"]}55, {T["divider"]}, {T["divider"]}55, transparent);
    margin: 1.5rem 0 2rem;
}}

/* ── Search Input ── */
/* Target every known Streamlit input wrapper variant for cloud consistency */
[data-testid="stTextInput"] input,
[data-testid="stTextInput"] > div > div > input,
.stTextInput input {{
    background-color: {T["input_bg"]} !important;
    background: {T["input_bg"]} !important;
    border: 1px solid {T["input_border"]} !important;
    border-radius: 12px !important;
    color: {T["input_text"]} !important;
    -webkit-text-fill-color: {T["input_text"]} !important;
    caret-color: {T["input_text"]} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.6rem 1rem !important;
    min-height: 2.55rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-shadow: none !important;
}}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextInput"] > div > div > input:focus,
.stTextInput input:focus {{
    border-color: {T["input_focus"]} !important;
    box-shadow: 0 0 0 3px {T["input_shadow"]} !important;
    outline: none !important;
}}
/* Autofill overrides — browsers inject their own bg on autofill */
[data-testid="stTextInput"] input:-webkit-autofill,
[data-testid="stTextInput"] input:-webkit-autofill:hover,
[data-testid="stTextInput"] input:-webkit-autofill:focus {{
    -webkit-box-shadow: 0 0 0px 1000px {T["input_bg"]} inset !important;
    -webkit-text-fill-color: {T["input_text"]} !important;
    caret-color: {T["input_text"]} !important;
}}
[data-testid="stTextInput"] label,
.stTextInput label {{
    color: {T["label_color"]} !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}

/* ── Result Cards ── */
.result-section-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin: 1.5rem 0 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.result-section-title.strong  {{ color: #c8a830; }}
.result-section-title.similar {{ color: #7b68b0; }}

.song-card {{
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1px solid {T["card_border"]};
}}
.song-card.strong {{
    border-left: 3px solid #c8a830;
    background: {T["card_strong_bg"]};
}}
.song-card.similar {{
    border-left: 3px solid #7b68b0;
    background: {T["card_similar_bg"]};
}}
.song-name {{
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 1rem;
    color: {T["song_name"]};
    text-decoration: none;
    transition: opacity 0.2s;
}}
.song-name:hover {{
    opacity: 0.8;
}}
.song-card.strong .song-name {{ font-weight: 700; }}

.no-match {{
    color: {T["no_match"]};
    font-style: italic;
    font-size: 0.9rem;
    padding: 0.5rem 0;
}}

/* ── Play Button ── */
.play-btn {{
    background: linear-gradient(135deg, #c8a830 0%, #e8a020 100%);
    color: #1a1530 !important;
    text-decoration: none !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.75rem;
    border-radius: 8px;
    padding: 0.35rem 0.7rem;
    transition: opacity 0.2s, transform 0.1s;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
}}
.play-btn:hover {{
    opacity: 0.88;
    transform: translateY(-1px);
}}
.play-btn:active {{
    transform: translateY(0);
    opacity: 1;
}}
.song-card.similar .play-btn {{
    background: linear-gradient(135deg, #7b68b0 0%, #9b88d0 100%);
    color: #fff !important;
}}

/* ── Search Button ── */
[data-testid="stButton"] button,
.stButton > button {{
    background: linear-gradient(135deg, #c8a830 0%, #e8a020 100%) !important;
    color: #1a1530 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.1s !important;
    width: 100% !important;
}}
[data-testid="stButton"] button:hover,
.stButton > button:hover {{
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}}
[data-testid="stButton"] button:active,
.stButton > button:active {{
    transform: translateY(0px) !important;
    opacity: 1 !important;
}}

[data-testid="stSpinner"] {{ color: #c8a830 !important; }}

[data-testid="stAlert"] {{
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}}

/* Toggle label */
[data-testid="stToggle"] p,
.stToggle p {{
    color: {T["label_color"]} !important;
    font-size: 0.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}}

/* ── Force Streamlit's own dark-theme overrides to yield ── */
[data-testid="stAppViewContainer"] [data-baseweb="input"] {{
    background-color: transparent !important;
}}
[data-baseweb="base-input"] {{
    background-color: {T["input_bg"]} !important;
}}
[data-baseweb="base-input"] input {{
    color: {T["input_text"]} !important;
    -webkit-text-fill-color: {T["input_text"]} !important;
    background-color: {T["input_bg"]} !important;
}}
</style>
""", unsafe_allow_html=True)


def render_theme_toggle(T: dict) -> None:
    """Render the light/dark mode toggle in the top-right corner."""
    _, toggle_col = st.columns([5, 1])
    with toggle_col:
        new_dark = st.toggle(
            T["toggle_icon"],
            value=st.session_state.get("dark_mode", False),
            help=T["toggle_label"],
        )
        if new_dark != st.session_state.get("dark_mode", False):
            st.session_state.dark_mode = new_dark
            st.rerun()


def render_header() -> None:
    """Render the spinning disc, TrackBack logo, and ABBA subtitle."""
    st.markdown("""
<div class="abba-header">
    <span class="disco-icon">💿</span>
    <h1 class="main-logo">TrackBack</h1>
    <p class="subtitle">A<span class="b-flip">B</span>BA &middot; Lyric-to-Song Search</p>
</div>
<div class="gold-divider"></div>
""", unsafe_allow_html=True)


def render_divider() -> None:
    """Render the gold gradient divider."""
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)


SONG_MAP = {
    "Ring Ring": "https://www.youtube.com/watch?v=TL0EoXdpZR0",
    "Another Town, Another Train": "https://www.youtube.com/watch?v=wCDwOuuGprg",
    "Disillusion": "https://www.youtube.com/watch?v=FQElL6jThxo",
    "People Need Love": "https://www.youtube.com/watch?v=pO7ubf4h8sk",
    "I Saw It in the Mirror": "https://www.youtube.com/watch?v=zjLKwahiQrU",
    "Nina, Pretty Ballerina": "https://www.youtube.com/watch?v=Rnz-qwt8hE4",
    "Love Isn't Easy (But It Sure Is Hard Enough)": "https://www.youtube.com/watch?v=YloY5vzw_oE",
    "Me and Bobby and Bobby's Brother": "https://www.youtube.com/watch?v=-DJ4UrMO0m0",
    "He Is Your Brother": "https://www.youtube.com/watch?v=UTLGrElgxt0",
    "She's My Kind of Girl": "https://www.youtube.com/watch?v=jWnKGNTUnDo",
    "I Am Just a Girl": "https://www.youtube.com/watch?v=zLu_gWq4NUA",
    "Rock'n Roll Band": "https://www.youtube.com/watch?v=nPrkyBa0j7s",
    "Waterloo": "https://www.youtube.com/watch?v=Sj_9CiNkkn4",
    "Sitting in the Palmtree": "https://www.youtube.com/watch?v=eSBHdxyhPWo",
    "King Kong Song": "https://www.youtube.com/watch?v=w7YwFrApvP0",
    "Hasta Mañana": "https://www.youtube.com/watch?v=3DinorrElWM",
    "My Mama Said": "https://www.youtube.com/watch?v=92L6balksi8",
    "Dance (While the Music Still Goes On)": "https://www.youtube.com/watch?v=eFBlbcT1VKU",
    "Honey, Honey": "https://www.youtube.com/watch?v=SnjzEsKM95I",
    "Watch Out": "https://www.youtube.com/watch?v=NDFytIpijRU",
    "What About Livingstone": "https://www.youtube.com/watch?v=k7fwX3yGUv0",
    "Gonna Sing You My Lovesong": "https://www.youtube.com/watch?v=EvVngDm7IG8",
    "Suzy-Hang-Around": "https://www.youtube.com/watch?v=lXKTeGIr9H0",
    "Mamma Mia": "https://www.youtube.com/watch?v=unfzfe8f9NI",
    "Hey, Hey Helen": "https://www.youtube.com/watch?v=HSa86pFukDE",
    "Tropical Loveland": "https://www.youtube.com/watch?v=GNQ7E0GIjzE",
    "SOS": "https://www.youtube.com/watch?v=cvChjHcABPA",
    "Man in the Middle": "https://www.youtube.com/watch?v=CaVAf6T5kkY",
    "Bang-A-Boomerang": "https://www.youtube.com/watch?v=_CsJCa2TlXU",
    "I Do, I Do, I Do, I Do, I Do": "https://www.youtube.com/watch?v=tW3HN_pvbE4",
    "Rock Me": "https://www.youtube.com/watch?v=ISkMe6nOYVU",
    "Intermezzo No. 1": "https://www.youtube.com/watch?v=0ZQ9qqPG3EM",
    "I've Been Waiting for You": "https://www.youtube.com/watch?v=ueeRcRn-owg",
    "So Long": "https://www.youtube.com/watch?v=ZskAO2VUHPE",
    "When I Kissed the Teacher": "https://www.youtube.com/watch?v=jGj8oM9NUZk",
    "Dancing Queen": "https://www.youtube.com/watch?v=xFrGuyw1V8s",
    "My Love, My Life": "https://www.youtube.com/watch?v=SfJA0euJ0A8",
    "Dum Dum Diddle": "https://www.youtube.com/watch?v=1g7kXC-bOgY",
    "Knowing Me, Knowing You": "https://www.youtube.com/watch?v=iUrzicaiRLU",
    "Money, Money, Money": "https://www.youtube.com/watch?v=ETxmCCsMoD0",
    "That's Me": "https://www.youtube.com/watch?v=mP_dk429rbc",
    "Why Did It Have to Be Me": "https://www.youtube.com/watch?v=zsx0NwK3pOQ",
    "Tiger": "https://www.youtube.com/watch?v=wWQ7wrPyUe0",
    "Eagle": "https://www.youtube.com/watch?v=dDI7x1nwTUw",
    "Take a Chance on Me": "https://www.youtube.com/watch?v=-crgQGdpZR0",
    "One Man, One Woman": "https://www.youtube.com/watch?v=sw_fuu9jIOc",
    "The Name of the Game": "https://www.youtube.com/watch?v=iJ90ZqH0PWI",
    "Move On": "https://www.youtube.com/watch?v=Kc7b_cEE7ys",
    "Hole in Your Soul": "https://www.youtube.com/watch?v=CR1nWKphP9Q",
    "Thank You for the Music": "https://www.youtube.com/watch?v=0dcbw4IEY5w",
    "I Wonder (Departure)": "https://www.youtube.com/watch?v=98_Q7Mztm8A",
    "I'm a Marionette": "https://www.youtube.com/watch?v=iB3349AaNUw",
    "As Good as New": "https://www.youtube.com/watch?v=A3gHZFKJ7nE",
    "Voulez-Vous": "https://www.youtube.com/watch?v=za05HBtGsgU",
    "I Have a Dream": "https://www.youtube.com/watch?v=ER_3h03omdE",
    "Angeleyes": "https://www.youtube.com/watch?v=2LfmJmtm4Xs",
    "The King Has Lost His Crown": "https://www.youtube.com/watch?v=Cd_ZkAiVwzI",
    "Does Your Mother Know": "https://www.youtube.com/watch?v=WkL7Fkigfn8",
    "If It Wasn't for the Nights": "https://www.youtube.com/watch?v=6YhMInq_Rj8",
    "Chiquitita": "https://www.youtube.com/watch?v=p4QqMKe3rwY",
    "Lovers (Live a Little Longer)": "https://www.youtube.com/watch?v=bAz0eb5y_Tc",
    "Kisses of Fire": "https://www.youtube.com/watch?v=BPFrUsJkscc",
    "Super Trouper": "https://www.youtube.com/watch?v=BshxCIjNEjY",
    "The Winner Takes It All": "https://www.youtube.com/watch?v=92cwKCU8Z5c",
    "On and On and On": "https://www.youtube.com/watch?v=PyxBYbfu6k8",
    "Andante, Andante": "https://www.youtube.com/watch?v=RT2mtWbN6aY",
    "Me and I": "https://www.youtube.com/watch?v=_X0zJQKj2VU",
    "Happy New Year": "https://www.youtube.com/watch?v=3Uo0JAUWijM",
    "Our Last Summer": "https://www.youtube.com/watch?v=KoyNlVQbUPc",
    "The Piper": "https://www.youtube.com/watch?v=UWMnwx997_4",
    "Lay All Your Love on Me": "https://www.youtube.com/watch?v=ulZQTrV8QlQ",
    "The Visitors": "https://www.youtube.com/watch?v=MtNKJ3wird8",
    "Head Over Heels": "https://www.youtube.com/watch?v=pL2_PZwKDPg",
    "When All Is Said and Done": "https://www.youtube.com/watch?v=tUh4u-lYEhM",
    "Soldiers": "https://www.youtube.com/watch?v=QGtl1z7Ck_k",
    "I Let the Music Speak": "https://www.youtube.com/watch?v=nLM1pRQVPQE",
    "One of Us": "https://www.youtube.com/watch?v=IIKAe8Wi0S0",
    "Two for the Price of One": "https://www.youtube.com/watch?v=Cb-54eCK3QY",
    "Slipping Through My Fingers": "https://www.youtube.com/watch?v=amleyiECy1w",
    "Like an Angel Passing Through My Room": "https://www.youtube.com/watch?v=0PncVgET-O8",
    "I Still Have Faith in You": "https://www.youtube.com/watch?v=pAzEY1MfXrQ",
    "When You Danced with Me": "https://www.youtube.com/watch?v=YDJZlPTFol8",
    "Little Things": "https://www.youtube.com/watch?v=f0qO04Y9Pwk",
    "Don't Shut Me Down": "https://www.youtube.com/watch?v=hWGWFa3jznI",
    "Just a Notion": "https://www.youtube.com/watch?v=vy4bLOYDmsQ",
    "I Can Be That Woman": "https://www.youtube.com/watch?v=o3kxl6_ejh0",
    "Keep An Eye On Dan": "https://www.youtube.com/watch?v=LM0NEyZtEdE",
    "Bumblebee": "https://www.youtube.com/watch?v=ofOaQ2CHm5M",
    "No Doubt About It": "https://www.youtube.com/watch?v=5zgHboLmonQ",
    "Ode to Freedom": "https://www.youtube.com/watch?v=YtNJybve8j4"
}

def render_results(strong_matches: list, similar_matches: list) -> None:
    """Render strong and similar match result cards."""
    render_divider()

    st.markdown('<p class="result-section-title strong">✨ Strong Matches</p>', unsafe_allow_html=True)
    if strong_matches:
        for song, _ in strong_matches:
            url = SONG_MAP.get(song, "#")
            tag = f'<a href="{url}" target="_blank" class="song-name">🎵 {song}</a>' if url != "#" else f'<span class="song-name">🎵 {song}</span>'
            btn = f'<a href="{url}" target="_blank" class="play-btn">▶ Play Video</a>' if url != "#" else ""
            st.markdown(f"""
            <div class="song-card strong">
                {tag}
                {btn}
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<p class="no-match">No strong matches found.</p>', unsafe_allow_html=True)

    st.markdown('<p class="result-section-title similar">🪩 Similar Matches</p>', unsafe_allow_html=True)
    if similar_matches:
        for song, _ in similar_matches:
            url = SONG_MAP.get(song, "#")
            tag = f'<a href="{url}" target="_blank" class="song-name">{song}</a>' if url != "#" else f'<span class="song-name">{song}</span>'
            btn = f'<a href="{url}" target="_blank" class="play-btn">▶ Play Video</a>' if url != "#" else ""
            st.markdown(f"""
            <div class="song-card similar">
                {tag}
                {btn}
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<p class="no-match">No similar matches found.</p>', unsafe_allow_html=True)