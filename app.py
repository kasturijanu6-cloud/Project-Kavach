import streamlit as st
import numpy as np
import zlib, hashlib, math, io, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

# --- THE CORE ENGINE ---
class KavachEngine:
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()
        self.delimiter = b'::KAVACH_ELITE_SIG::'

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        return cipher.iv + cipher.encrypt(pad(zlib.compress(text.encode()), 16)) + self.delimiter

    def decrypt(self, blob):
        try:
            iv, data = blob[:16], blob[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return zlib.decompress(unpad(cipher.decrypt(data), 16)).decode()
        except: return None

# --- UI CONFIGURATION: HYPER-CYBER GLOW ---
st.set_page_config(page_title="Kavach Hyper-Cyber", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0a0e17 0%, #000000 100%);
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Neon Title Animation */
    .hyper-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 4rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #39ff14, #bc13fe, #00f2ff, #39ff14);
        background-size: 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 10s linear infinite;
        margin-bottom: 0px;
    }
    @keyframes glow { 0% { background-position: 0%; } 100% { background-position: 300%; } }

    /* Glassmorphism Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 30px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px 10px 0 0;
        color: #888;
        padding: 0 40px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0, 242, 255, 0.1) !important;
        border: 1px solid #00f2ff !important;
        color: #00f2ff !important;
        box-shadow: 0px 0px 15px #00f2ff55;
    }

    /* Cyber Buttons */
    .stButton>button {
        background: transparent;
        border: 2px solid #39ff14;
        color: #39ff14;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        border-radius: 0px;
        transition: 0.5s;
        text-transform: uppercase;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        background: #39ff14;
        color: #000;
        box-shadow: 0 0 40px #39ff14;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- MAIN INTERFACE ---
st.markdown('<h1 class="hyper-title">KAVACH ELITE</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #bc13fe; font-family: Orbitron;'><b>CORE PROTOCOL // AES-256 // LSB-INT16</b></p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["[ 1. SHIELD_ENCODE ]", "[ 2.
