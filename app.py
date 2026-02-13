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
        self.delimiter = b'::PRISM_GUARD_SECURE::'

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        return cipher.iv + cipher.encrypt(pad(zlib.compress(text.encode()), 16)) + self.delimiter

    def decrypt(self, blob):
        try:
            iv, data = blob[:16], blob[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return zlib.decompress(unpad(cipher.decrypt(data), 16)).decode()
        except: return None

# --- UI CONFIGURATION & CSS ---
st.set_page_config(page_title="Kavach Prism Defense", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Space+Grotesk:wght@300;500&display=swap');
    
    .stApp {
        background: linear-gradient(125deg, #050505 0%, #0a0a12 50%, #050505 100%);
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .prism-title {
        font-family: 'Syncopate', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        background: linear-gradient(90deg, #00f2ff, #7000ff, #ff0055);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }

    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        margin-top: 20px;
    }

    .stButton>button {
        background: transparent;
        border: 2px solid #00f2ff;
        color: #00f2ff;
        border-radius: 50px;
        padding: 10px 40px;
        font-weight: bold;
        transition: 0.4s;
        width: 100%;
    }
    .stButton>button:hover {
        background: #00f2ff;
        color: #000;
        box-shadow: 0 0 30px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="prism-title">PROJECT KAVACH</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.6;'>// PRISM DEFENSE PROTOCOL v5.0 // MULTI-LAYER STEALTH</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["💎 ENCODE", "👁️ DECODE", "📊 AUDIT"])

# --- ENCODER (FIXED LINE 71) ---
with t1:
    col_in, col_pre = st.columns([1, 1.2])
    with col_in:
        st.markdown("### 📥 Payload Input")
        carrier = st.file_uploader("Upload Carrier Frame", type=["png"])
        secret = st.text_area("Secure String", placeholder="Enter data to hide...")
        key = st.text_input("Master Key", type="password")
        
    if st.button("🚀 DEPLOY PRISM SHIELD") and carrier and secret and key:
        with st.status("Refracting Data...") as status:
            engine = KavachEngine(key)
            img = Image.open(carrier).convert('RGB')
            pixels = np.array(img)
            
            blob = engine.encrypt(secret)
            bits = np.unpackbits(np.frombuffer(blob, dtype=np.uint8))
            
            flat = pixels.flatten()
            if len(bits) > len(flat):
                st.error("CAPACITY BREACH")
            else:
                # FIX FOR LINE 71: Cast to int16 to prevent OverflowError
                temp = flat[:len(bits)].astype(np.int16)
                temp = (temp & ~1) | bits
                flat[:len(bits)] = temp.astype(np.uint8)
                
                stego_img = Image.fromarray(flat.reshape(pixels.shape))
                
                # Analysis
                mse = np.mean((pixels.astype(np.float32) - flat.reshape(pixels.shape).astype(np.float32))**2)
                psnr = 100 if mse == 0 else 20 * math.log10(255.0 / math.sqrt(mse))
                
                with col_pre:
                    st.image(stego_img, use_container_width=True)
                    st.metric("Visual Fidelity", f"{psnr:.2f} dB")
                    buf = io.BytesIO()
                    stego_img.save(buf, format="PNG")
                    st.download_button("💾 EXPORT SECURE PNG", buf.getvalue(), "kavach_prism.png")
            status.update(label="System Shielded", state="complete")

# --- DECODER ---
with t2:
    st.markdown("### 🔍 Deep Signal Extraction")
    stego_in = st.file_uploader("Upload Stego-Object", type=["png"], key="dec_p")
    key_in = st.text_input("Enter Extraction Key", type="password", key="key_p")
    
    if st.button("🔓 RUN DECRYPTION") and stego_in and key_in:
        engine = KavachEngine(key_in)
        img_d = Image.open(stego_in).convert('RGB')
        bits_d = np.array(img_d).flatten() & 1
        bytes_d = np.packbits(bits_d).tobytes()
        
        if engine.delimiter in bytes_d:
            raw = bytes_d.split(engine.delimiter)[0]
            result = engine.decrypt(raw)
            if result:
                st.success("AUTHENTICATION VERIFIED")
                st.code(result)
            else: st.error("ACCESS DENIED")
        else: st.error("NO SIGNATURE FOUND")

# --- AUDIT ---
with t3:
    st.markdown("### 📊 System Integrity Ledger")
    st.progress(100)
    st.markdown("`SYSTEM UPTIME: 100% | ALL NODES SECURE`")
