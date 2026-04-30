import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import streamlit as st
import numpy as np
from PIL import Image
import time
import random

# --- CONFIG ---
st.set_page_config(page_title="VibeCheck OUTFIT - UHD", page_icon="⚡", layout="wide")

# --- STYLE + GLITCH HALUS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Urbanist:wght@400;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #050505;
    font-family: 'Urbanist', sans-serif;
    color: #00ffcc;
}

/* TITLE */
.cyber-title {
    position: relative;
    font-family: 'Orbitron', sans-serif;
    font-size: 4rem;
    text-align: center;
    letter-spacing: 5px;
    color: #00ffcc;
}

/* glitch layer */
.cyber-title::before,
.cyber-title::after {
    content: attr(data-text);
    position: absolute;
    left: 0;
    width: 100%;
    opacity: 0;
}

/* merah */
.cyber-title::before {
    color: #ff00ff;
    animation: glitchFlash 6s infinite;
}

/* biru */
.cyber-title::after {
    color: #00ffff;
    animation: glitchFlash 6s infinite;
    animation-delay: 0.2s;
}

/* glitch SEKILAS */
@keyframes glitchFlash {
    0%, 92%, 100% {
        opacity: 0;
        transform: translate(0);
    }
    93% {
        opacity: 1;
        transform: translate(-2px, 2px);
    }
    95% {
        opacity: 1;
        transform: translate(2px, -2px);
    }
    97% {
        opacity: 0;
        transform: translate(0);
    }
}

video {
    border: 2px solid #00ffcc !important;
    box-shadow: 0 0 20px #00ffcc;
    border-radius: 15px !important;
}

.glass-panel {
    background: rgba(10, 10, 10, 0.8);
    border: 1px solid #00ffcc;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 0 40px rgba(0, 255, 204, 0.1);
}

.outfit-card {
    background: #111;
    border-left: 5px solid #00ffcc;
    padding: 10px;
    margin-bottom: 20px;
    transition: 0.3s;
}

.outfit-card:hover {
    background: #00ffcc;
    color: black !important;
    transform: scale(1.05);
    box-shadow: 0 0 25px #00ffcc;
}

.stButton>button {
    background: #00ffcc !important;
    color: black !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: bold !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
def get_outfit_data(mood, gender):
    return [
        {'name': f'{mood.capitalize()} Look {i}', 'img': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'}
        for i in range(1, 10)
    ]

# --- ANALISIS ---
def analyze_vibe(img):
    emotions = ["happy", "sad", "angry", "neutral", "surprise"]
    return random.choice(emotions), random.randint(70, 98)

# --- AI COMMENT ---
def ai_comment(mood):
    comments = {
        "happy": "⚡ ENERGY HIGH — YOU'RE GLOWING",
        "sad": "🌙 LOW VIBE — STYLE BOOST INITIATED",
        "angry": "🔥 INTENSE MODE — DOMINATE FIT",
        "neutral": "🧠 BALANCED — CLEAN LOOK READY",
        "surprise": "⚡ CHAOTIC ENERGY — UNIQUE STYLE"
    }
    return comments.get(mood, "SCANNING...")

# --- TITLE ---
st.markdown(
    "<h1 class='cyber-title' data-text='VIBECHECK OUTFIT'>VibeCheck OUTFIT</h1>",
    unsafe_allow_html=True
)

# --- MODE ---
mode = st.toggle("🌗 ACTIVATE NEON MODE")

if mode:
    st.markdown("""
    <style>
    body {
        background: radial-gradient(circle, #000000, #020024, #090979, #00d4ff);
    }
    </style>
    """, unsafe_allow_html=True)

# --- MAIN ---
with st.container():
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)

    col_cam, col_info = st.columns([1.5, 1])

    with col_info:
        st.markdown("### 🛠 SYSTEM_STATUS: ONLINE")
        gender = st.selectbox("SELECT_IDENTITY", ["MALE", "FEMALE"])
        st.caption("SCANNING BIOMETRICS...")

    with col_cam:
        img_file = st.camera_input("CAPTURE")

    if img_file:
        with st.spinner("🔍 ANALYZING VIBE..."):
            time.sleep(1.5)
            img = Image.open(img_file)
            mood, conf = analyze_vibe(img)

        st.markdown(f"## MOOD: <span style='color:#ff00ff'>{mood.upper()}</span>", unsafe_allow_html=True)

        progress_bar = st.progress(0)
        for i in range(conf):
            time.sleep(0.005)
            progress_bar.progress(i + 1)

        st.write(f"Confidence: {conf}%")

        st.info(ai_comment(mood))

        st.download_button(
            "💾 SAVE RESULT",
            data=img_file.getvalue(),
            file_name="vibecheck.png",
            mime="image/png"
        )

        st.markdown("### 🛍 OUTFIT GENERATED")
        outfits = get_outfit_data(mood, gender)

        cols = st.columns(3)
        for i, item in enumerate(outfits):
            with cols[i % 3]:
                st.markdown(f"""
                <div class='outfit-card'>
                    <img src='{item['img']}' style='width:100%; border-radius:10px;'>
                    <p>ID: VC-{i+100}</p>
                    <b>{item['name']}</b>
                </div>
                """, unsafe_allow_html=True)

                st.link_button(f"CHECKOUT_{i}", "https://shopee.co.id")

    st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("<center style='font-size:0.7rem;opacity:0.5;'>VIBECHECK_TELKOMUNIVERSITYSURABAYA_V15</center>", unsafe_allow_html=True)
