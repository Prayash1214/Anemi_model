import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Anime Recom-Station", page_icon="🌸", layout="centered")

# --- 2. MODEL & ASSET LOADING ---
@st.cache_resource
def load_assets():
    # Resolves the absolute path to your project folder
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    model_path = current_dir / "anime_model.pkl"
    le_path = current_dir / "label_encoder.pkl"

    # Log to terminal for debugging
    print(f"DEBUG: Looking for assets in: {current_dir}")

    if not model_path.exists() or not le_path.exists():
        return None, None, f"Missing files in {current_dir}"

    try:
        loaded_model = joblib.load(model_path)
        loaded_le = joblib.load(le_path)
        return loaded_model, loaded_le, None
    except Exception as e:
        return None, None, str(e)

# Initialize the load
model, le, error_msg = load_assets()

# --- 3. CUSTOM CSS & ANIMATIONS ---
BG_URL = "https://images.alphacoders.com/605/605592.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(14, 17, 23, 0.8), rgba(14, 17, 23, 0.85)), 
                    url("{BG_URL}") no-repeat center center fixed;
        background-size: cover;
    }}
    [data-testid="stAppViewContainer"] > section:first-child {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 25px;
        border: 1px solid rgba(255, 183, 197, 0.2);
        padding: 3rem;
        margin-top: 20px;
    }}
    .sakura {{
        position: fixed; top: -10%; z-index: 9999; color: #ffb7c5;
        font-size: 20px; user-select: none; pointer-events: none;
        animation: fall 10s linear infinite;
    }}
    @keyframes fall {{
        0% {{ top: -10%; transform: translateX(0) rotate(0deg); opacity: 1; }}
        100% {{ top: 110%; transform: translateX(100px) rotate(360deg); opacity: 0; }}
    }}
    .p1 {{ left: 10%; animation-duration: 7s; }}
    .p2 {{ left: 30%; animation-duration: 12s; animation-delay: 2s; }}
    .p3 {{ left: 50%; animation-duration: 9s; animation-delay: 4s; }}
    .p4 {{ left: 70%; animation-duration: 15s; }}
    .p5 {{ left: 90%; animation-duration: 11s; animation-delay: 3s; }}
    .title-text {{
        text-align: center; color: #ffb7c5; font-size: 3.2rem; font-weight: bold;
        text-shadow: 0px 0px 15px rgba(255, 183, 197, 0.7);
    }}
    .section-header {{
        color: #ffb7c5; font-size: 1.2rem; font-weight: bold; text-transform: uppercase;
        border-left: 5px solid #ff416c; padding-left: 15px; margin-bottom: 20px;
    }}
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white; border: none; padding: 18px; font-size: 1.5rem;
        font-weight: bold; border-radius: 15px; width: 100%;
        text-transform: uppercase; letter-spacing: 5px;
        box-shadow: 0 0 15px rgba(255, 65, 108, 0.5);
    }}
    label {{ color: #f8f9fa !important; }}
    </style>
    <div class="sakura p1">🌸</div><div class="sakura p2">🌸</div>
    <div class="sakura p3">🌸</div><div class="sakura p4">🌸</div>
    <div class="sakura p5">🌸</div>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
st.markdown("<h1 class='title-text'>🌸 ANIME RECOM-STATION 🌸</h1>", unsafe_allow_html=True)

if error_msg:
    st.error(f"🔮 The summoning circle is broken: {error_msg}")
    st.info("Check if anime_model.pkl and label_encoder.pkl are in your PyCharm project folder.")

# --- 5. UI LAYOUT ---
col1, col2 = st.columns(2, gap="large")

mood_map = {"lonely":0, "happy":1, "anxious":2, "neutral":3, "bored":4, "excited":5, "angry":6, "tired":7, "nostalgic":8, "sad":9}
intent_map = {"relax":0, "escape":1, "entertain":2, "motivate":3, "thrill":4, "cry":5, "pass_time":6, "excite":7}
genre_map = {"comedy":1, "fantasy":2, "adventure":3, "shounen":4, "isekai":5, "drama":6, "romance":7, "action":8, "slice_of_life":9}

with col1:
    st.markdown("<div class='section-header'>🔮 SPIRIT STATS</div>", unsafe_allow_html=True)
    selected_mood = st.selectbox("CURRENT MOOD", list(mood_map.keys()))
    selected_intent = st.selectbox("YOUR INTENT", list(intent_map.keys()))
    selected_genre = st.selectbox("GENRE PREFERENCE", list(genre_map.keys()))
    energy_level = st.select_slider("CHAKRA INTENSITY (ENERGY)", options=["low", "medium", "high"], value="medium")

with col2:
    st.markdown("<div class='section-header'>🎭 AURA & FORMAT</div>", unsafe_allow_html=True)
    emotion_level = st.select_slider("EMOTION INTENSITY", options=["low", "medium", "high"], value="medium")
    anime_type = st.radio("CONTENT TYPE", ["series", "movie", "short"], horizontal=True)
    context = st.radio("WATCHING CONTEXT", ["alone", "with_family", "with_friends"])

st.write("---")

# --- 6. PREDICTION LOGIC ---
if st.button("✨ SUMMON DESTINY ✨"):
    if model and le:
        # Create DataFrame matching training columns
        test_input = pd.DataFrame({
            "Mood": [mood_map[selected_mood]],
            "Intent": [intent_map[selected_intent]],
            "Genre_Preference": [genre_map[selected_genre]],
            "Emotion_Intensity_low": [True if emotion_level == "low" else False],
            "Emotion_Intensity_medium": [True if emotion_level == "medium" else False],
            "Energy_Level_low": [True if energy_level == "low" else False],
            "Energy_Level_medium": [True if energy_level == "medium" else False],
            "Type_series": [True if anime_type == "series" else False],
            "Type_short": [True if anime_type == "short" else False],
            "Watching_Context_with_family": [True if context == "with_family" else False],
            "Watching_Context_with_friends": [True if context == "with_friends" else False]
        })

        try:
            prediction_num = model.predict(test_input)
            anime_name = le.inverse_transform(prediction_num)[0]

            st.balloons()
            st.markdown(f"""
                <div style='text-align: center; margin-top: 30px; padding: 30px; border: 2px solid #ff416c; 
                            border-radius: 20px; background-color: rgba(14, 17, 23, 0.95); 
                            box-shadow: 0 0 40px rgba(255, 65, 108, 0.6);'>
                    <h3 style='color: #cccccc; text-transform: uppercase; letter-spacing: 3px;'>The Gate has Opened...</h3>
                    <p style='color: #ffb7c5; font-size: 1.1rem;'>YOUR SOULMATE ANIME IS:</p>
                    <h1 style='color: #ff416c; font-size: 4rem; text-shadow: 0 0 20px #ff416c; margin: 10px 0;'>
                        {anime_name.upper()}
                    </h1>
                    <p style='color: #f8f9fa; font-style: italic; font-size: 1.2rem;'>“Believe it! Your next journey awaits.”</p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Calculation Error: {e}")
    else:
        st.warning("Please resolve the file errors above before summoning.")