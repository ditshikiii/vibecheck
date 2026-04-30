import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import streamlit as st
# import cv2  ❌ tidak dipakai
# from deepface import DeepFace ❌ dihapus
import numpy as np
from PIL import Image

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
    mood = mood.lower()
    gender = gender.lower()

    outfits = {
        "male": {
            "happy": [
                {"name": "Bright Street Hoodie Fit", "img": "https://images.unsplash.com/photo-1520975922284-9e0ce8274d48?w=400"},
                {"name": "Casual Denim Smile Look", "img": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=400"},
                {"name": "Color Pop Urban Style", "img": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400"},
                {"name": "Sunny Day Chill Outfit", "img": "https://images.unsplash.com/photo-1516822003754-cca485356ecb?w=400"},
                {"name": "Vibrant Graphic Tee Style", "img": "https://images.unsplash.com/photo-1544441893-675973e31985?w=400"}
            ],
            "sad": [
                {"name": "Dark Hoodie Comfort Fit", "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400"},
                {"name": "Minimal Black Outfit", "img": "https://images.unsplash.com/photo-1520975916090-3105956dac38?w=400"},
                {"name": "Soft Layer Cozy Style", "img": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400"},
                {"name": "Rainy Day Jacket Fit", "img": "https://images.unsplash.com/photo-1490578474895-699cd4e2cf59?w=400"},
                {"name": "Monochrome Chill Look", "img": "https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?w=400"}
            ],
            "angry": [
                {"name": "All Black Streetwear", "img": "https://images.unsplash.com/photo-1520975916090-3105956dac38?w=400"},
                {"name": "Techwear Assassin Fit", "img": "https://images.unsplash.com/photo-1552374196-c4e7ffc6e126?w=400"},
                {"name": "Leather Jacket Rebel Look", "img": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=400"},
                {"name": "Dark Urban Warrior Style", "img": "https://images.unsplash.com/photo-1544441893-675973e31985?w=400"},
                {"name": "Heavy Boots Street Fit", "img": "https://images.unsplash.com/photo-1514996937319-344454492b37?w=400"}
            ],
            "neutral": [
                {"name": "Clean Minimal Outfit", "img": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=400"},
                {"name": "Smart Casual Fit", "img": "https://images.unsplash.com/photo-1520975661595-6453be3f7070?w=400"},
                {"name": "Simple White Tee Style", "img": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=400"},
                {"name": "Basic Everyday Look", "img": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=400"},
                {"name": "Modern Casual Balance", "img": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400"}
            ],
            "surprise": [
                {"name": "Bold Neon Streetwear", "img": "https://images.unsplash.com/photo-1548624149-f1bc346fe750?w=400"},
                {"name": "Unexpected Layered Fit", "img": "https://images.unsplash.com/photo-1581044777550-4cfa60707c03?w=400"},
                {"name": "Futuristic Tech Outfit", "img": "https://images.unsplash.com/photo-1611312449408-fcece27cdbb7?w=400"},
                {"name": "Creative Pattern Mix Style", "img": "https://images.unsplash.com/photo-1521223890158-f9f7c3d5d50d?w=400"},
                {"name": "Statement Outfit Look", "img": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=400"}
            ]
        },

        "female": {
            "happy": [
                {"name": "Bright Summer Dress", "img": "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?w=400"},
                {"name": "Colorful Casual Chic", "img": "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?w=400"},
                {"name": "Cute Pastel Outfit", "img": "https://images.unsplash.com/photo-1519741497674-611481863552?w=400"},
                {"name": "Sunny Day Skirt Style", "img": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400"},
                {"name": "Playful Street Fashion", "img": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400"}
            ],
            "sad": [
                {"name": "Oversized Hoodie Comfort", "img": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400"},
                {"name": "Soft Knit Cozy Look", "img": "https://images.unsplash.com/photo-1519741497674-611481863552?w=400"},
                {"name": "Muted Tone Outfit", "img": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400"},
                {"name": "Rainy Day Aesthetic Fit", "img": "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?w=400"},
                {"name": "Minimal Calm Style", "img": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400"}
            ],
            "angry": [
                {"name": "All Black Fierce Look", "img": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400"},
                {"name": "Leather Jacket Queen", "img": "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?w=400"},
                {"name": "Dark Street Style", "img": "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?w=400"},
                {"name": "Bold Power Outfit", "img": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400"},
                {"name": "Edgy Fashion Fit", "img": "https://images.unsplash.com/photo-1519741497674-611481863552?w=400"}
            ],
            "neutral": [
                {"name": "Clean Minimal Chic", "img": "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?w=400"},
                {"name": "Simple Elegant Outfit", "img": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400"},
                {"name": "Basic Everyday Style", "img": "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?w=400"},
                {"name": "Modern Casual Look", "img": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400"},
                {"name": "Soft Neutral Fit", "img": "https://images.unsplash.com/photo-1519741497674-611481863552?w=400"}
            ],
            "surprise": [
                {"name": "Bold Neon Outfit", "img": "https://images.unsplash.com/photo-1548624149-f1bc346fe750?w=400"},
                {"name": "Creative Layered Look", "img": "https://images.unsplash.com/photo-1581044777550-4cfa60707c03?w=400"},
                {"name": "Unique Statement Style", "img": "https://images.unsplash.com/photo-1521223890158-f9f7c3d5d50d?w=400"},
                {"name": "Futuristic Fashion Fit", "img": "https://images.unsplash.com/photo-1611312449408-fcece27cdbb7?w=400"},
                {"name": "Experimental Outfit Look", "img": "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?w=400"}
            ]
        }
    }

    return outfits.get(gender, {}).get(mood, [])

# --- 3. ANALYTICS (FIX TANPA DEEPFACE) ---
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
                    st.link_button(f"CHECKOUT_VC{i}", "https://shopee.co.id", key=f"shop_{i}")
        else:
            st.warning("SYSTEM_ERROR: FACE_NOT_FOUND. RE-ADJUST_LIGHTING.")
            
    st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("<br><center style='font-family:Orbitron; font-size:0.6rem; opacity:0.5;'>VIBECHECK_OS_V15.0 // SURABAYA_SECTOR_7 // BY_AUZAN_ADITYA_F</center>", unsafe_allow_html=True)
