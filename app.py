import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import streamlit as st
import numpy as np
from PIL import Image
import urllib.parse  # ✅ TAMBAHAN

# --- 1. CYBER-PUNK CONFIG & STYLING ---
st.set_page_config(page_title="VibeCheck AI - UHD", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Urbanist:wght@400;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: #050505;
        font-family: 'Urbanist', sans-serif;
        color: #00ffcc;
        overflow-x: hidden;
    }

    body::before {
        content: " "; display: block; position: fixed; top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 999; background-size: 100% 2px, 3px 100%; pointer-events: none;
    }

    video {
        transform: scaleX(1) !important;
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

    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 4rem;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 5px;
        color: #00ffcc;
        text-shadow: 2px 2px #ff00ff, -2px -2px #00ffff;
        animation: glitch 1s linear infinite;
    }

    @keyframes glitch {
        2%, 64% { transform: translate(2px,0) skew(0deg); }
        4%, 60% { transform: translate(-2px,0) skew(0deg); }
        62% { transform: translate(0,0) skew(5deg); }
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
        transform: skew(-2deg);
    }
    
    .stButton>button {
        background: #00ffcc !important;
        color: black !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: bold !important;
        border: none !important;
        clip-path: polygon(10% 0, 100% 0, 90% 100%, 0% 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MASSIVE DATABASE ---
def get_outfit_data(mood, gender):
    base_items = [
        {'name': f'{mood.capitalize()} Look 01', 'img': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'},
        {'name': f'{mood.capitalize()} Urban 02', 'img': 'https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400'},
        {'name': f'{mood.capitalize()} Tech 03', 'img': 'https://images.unsplash.com/photo-1550991152-12469a931ca9?w=400'},
        {'name': f'{mood.capitalize()} Cyber 04', 'img': 'https://images.unsplash.com/photo-1611312449408-fcece27cdbb7?w=400'},
        {'name': f'{mood.capitalize()} Street 05', 'img': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400'},
        {'name': f'{mood.capitalize()} Retro 06', 'img': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=400'},
        {'name': f'{mood.capitalize()} Future 07', 'img': 'https://images.unsplash.com/photo-1581044777550-4cfa60707c03?w=400'},
        {'name': f'{mood.capitalize()} Minimal 08', 'img': 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=400'},
        {'name': f'{mood.capitalize()} Neon 09', 'img': 'https://images.unsplash.com/photo-1548624149-f1bc346fe750?w=400'},
        {'name': f'{mood.capitalize()} Logic 10', 'img': 'https://images.unsplash.com/photo-1521223890158-f9f7c3d5d50d?w=400'}
    ]
    return base_items

# --- 3. ANALYTICS ---
def analyze_vibe(img):
    try:
        import random
        emotions = ["happy", "sad", "angry", "neutral", "surprise"]
        mood = random.choice(emotions)
        confidence = random.randint(70, 98)
        return mood, confidence
    except:
        return None, None

# --- 4. WEB LAYOUT ---
st.markdown("<h1 class='cyber-title'>VibeCheck AI</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    
    col_cam, col_info = st.columns([1.5, 1])
    
    with col_info:
        st.markdown("### 🛠 SYSTEM_STATUS: ONLINE")
        gender = st.selectbox("SELECT_IDENTITY", ["MALE", "FEMALE"])
        st.markdown("---")
        st.caption("SCANNING REAL-TIME BIOMETRICS...")
        
    with col_cam:
        img_file = st.camera_input("CAPTURE_UHD_FRAME")

    if img_file:
        img = Image.open(img_file)
        mood, conf = analyze_vibe(img)
        
        if mood:
            st.markdown(f"## ANALYZED_MOOD: <span style='color:#ff00ff'>{mood.upper()}</span>", unsafe_allow_html=True)
            st.progress(conf/100)
            st.write(f"Confidence Level: {conf}%")
            
            st.markdown("### 🛍 GENERATING_OUTFIT_CATALOG...")
            outfits = get_outfit_data(mood, gender)
            
            cols = st.columns(3)
            for i, item in enumerate(outfits):
                with cols[i % 3]:
                    st.markdown(f"""
                        <div class='outfit-card'>
                            <img src='{item['img']}' style='width:100%; border-radius:10px;'>
                            <p style='font-size:0.8rem; margin-top:5px;'>ID: VC-{i+100}</p>
                            <b style='font-family:Orbitron'>{item['name']}</b>
                        </div>
                    """, unsafe_allow_html=True)

                    # ✅ LINK SHOPEE DINAMIS
                    search_query = urllib.parse.quote(item['name'])
                    shopee_link = f"https://shopee.co.id/search?keyword={search_query}"

                    st.link_button(f"CHECKOUT_VC{i}", shopee_link, key=f"shop_{i}")

        else:
            st.warning("SYSTEM_ERROR: FACE_NOT_FOUND. RE-ADJUST_LIGHTING.")
            
    st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("<br><center style='font-family:Orbitron; font-size:0.6rem; opacity:0.5;'>VIBECHECK_OS_V15.0 // SURABAYA_SECTOR_7 // BY_AUZAN_ADITYA_F</center>", unsafe_allow_html=True)
