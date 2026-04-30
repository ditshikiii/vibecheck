import streamlit as st
import random
import time
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="VibeCheck AI", page_icon="⚡", layout="wide")

# --- STYLE ---
st.markdown("""
<style>
body, .stApp {
    background: #050505;
    color: #00ffcc;
    font-family: 'Arial';
}

.cyber-title {
    font-size: 3.5rem;
    text-align: center;
    color: #00ffcc;
    text-shadow: 0 0 10px #00ffcc;
}

.glass {
    background: rgba(0,0,0,0.7);
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #00ffcc;
}

.outfit {
    background: #111;
    padding: 10px;
    border-left: 4px solid #00ffcc;
    margin-bottom: 15px;
    transition: 0.3s;
}

.outfit:hover {
    background: #00ffcc;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# --- VIBE SYSTEM ---
def analyze_vibe():
    vibes = ["happy", "sad", "angry", "neutral", "confident", "chill"]
    return random.choice(vibes), random.randint(75, 98)

# --- OUTFIT DATABASE ---
def get_outfits(vibe):
    data = {
        "happy": [
            ("Bright Hoodie + Cargo", "https://images.unsplash.com/photo-1520975916090-3105956dac38", "hoodie colorful pria"),
            ("Colorful Streetwear", "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c", "streetwear colorful"),
        ],
        "sad": [
            ("Oversized Black Hoodie", "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2", "hoodie hitam oversized"),
            ("Dark Aesthetic Fit", "https://images.unsplash.com/photo-1520975916090-3105956dac38", "outfit dark aesthetic"),
        ],
        "angry": [
            ("Leather Jacket Fit", "https://images.unsplash.com/photo-1556821840-3a63f95609a7", "jaket kulit pria"),
            ("Street Rebel Outfit", "https://images.unsplash.com/photo-1548624149-f1bc346fe750", "streetwear hitam pria"),
        ],
        "neutral": [
            ("Minimal Clean Look", "https://images.unsplash.com/photo-1551028719-00167b16eac5", "kaos polos outfit pria"),
            ("Smart Casual", "https://images.unsplash.com/photo-1523381210434-271e8be1f52b", "smart casual pria"),
        ],
        "confident": [
            ("Blazer + Sneaker", "https://images.unsplash.com/photo-1581044777550-4cfa60707c03", "blazer pria casual"),
            ("All Black Fit", "https://images.unsplash.com/photo-1550991152-12469a931ca9", "outfit hitam keren"),
        ],
        "chill": [
            ("Hoodie Santai", "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2", "hoodie santai pria"),
            ("Kaos + Shorts", "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c", "outfit santai pria"),
        ]
    }
    return data.get(vibe, data["neutral"])

# --- AI COMMENT ---
def ai_comment(vibe):
    return {
        "happy": "⚡ ENERGY HIGH — YOU'RE GLOWING",
        "sad": "🌙 LOW VIBE — BOOSTING STYLE...",
        "angry": "🔥 INTENSE MODE — DOMINATE FIT",
        "neutral": "🧠 CLEAN & BALANCED",
        "confident": "💎 MAIN CHARACTER ENERGY",
        "chill": "🌴 RELAX MODE ACTIVATED"
    }[vibe]

# --- TITLE ---
st.markdown("<h1 class='cyber-title'>VibeCheck AI</h1>", unsafe_allow_html=True)

# --- MAIN ---
with st.container():
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1])

    with col2:
        st.markdown("### SYSTEM ONLINE")
        gender = st.selectbox("IDENTITY", ["MALE", "FEMALE"])

    with col1:
        img = st.camera_input("CAPTURE FACE")

    if img:
        with st.spinner("Analyzing vibe..."):
            time.sleep(1.5)
            vibe, conf = analyze_vibe()

        st.markdown(f"## MOOD: **{vibe.upper()}**")
        st.progress(conf / 100)
        st.write(f"Confidence: {conf}%")

        st.info(ai_comment(vibe))

        st.markdown("### RECOMMENDED OUTFIT")

        outfits = get_outfits(vibe)

        cols = st.columns(2)
        for i, (name, img_url, keyword) in enumerate(outfits):
            with cols[i % 2]:
                st.image(img_url)
                st.write(name)
                st.link_button(
                    "Buy on Shopee",
                    f"https://shopee.co.id/search?keyword={keyword}"
                )

    st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("<center style='opacity:0.5;'>VibeCheck AI • Safe Mode • Cloud Ready</center>", unsafe_allow_html=True)
