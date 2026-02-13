import streamlit as st
import numpy as np
import zlib, hashlib, math, io, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

# --- THE CAULDRON: CORE CRYPTO ---
class KavachEngine:
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()
        self.delimiter = b'::SPOOKY_END_OF_STRING::'

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        return cipher.iv + cipher.encrypt(pad(zlib.compress(text.encode()), 16)) + self.delimiter

    def decrypt(self, blob):
        try:
            iv, data = blob[:16], blob[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return zlib.decompress(unpad(cipher.decrypt(data), 16)).decode()
        except: return None

# --- UI CONFIGURATION: HALLOWEEN THEME ---
st.set_page_config(page_title="Kavach: Cursed Crypt", page_icon="🎃", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Creepster&family=Nosifer&family=Special+Elite&display=swap');
    
    .stApp {
        background: radial-gradient(circle, #1a0033 0%, #000000 100%);
        color: #ff6600;
        font-family: 'Special Elite', cursor;
    }
    
    h1 {
        font-family: 'Nosifer', sans-serif !important;
        color: #ff6600 !important;
        text-shadow: 0 0 15px #ff0000;
        text-align: center;
    }

    h2, h3 {
        font-family: 'Creepster', cursive !important;
        color: #9933ff !important;
        letter-spacing: 3px;
    }

    /* Spooky Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        color: #ff660088;
        background: #111;
        border: 1px solid #9933ff33;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        color: #ff6600 !important;
        border: 1px solid #ff6600 !important;
        box-shadow: 0 0 20px #ff660044;
    }

    /* Neon Orange Buttons */
    .stButton>button {
        background: transparent;
        color: #ff6600 !important;
        border: 2px solid #ff6600 !important;
        border-radius: 10px;
        font-weight: bold;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background: #ff6600 !important;
        color: #000 !important;
        box-shadow: 0 0 30px #ff6600;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("
