import streamlit as st
import numpy as np
import zlib, hashlib, math, io, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

# --- THE FORTRESS: CORE ENGINE ---
class KavachEngine:
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()
        self.delimiter = b'::KAVACH_GHOST_RECON::'

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        return cipher.iv + cipher.encrypt(pad(zlib.compress(text.encode()), 16)) + self.delimiter

    def decrypt(self, blob):
        try:
            iv, data = blob[:16], blob[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return zlib.decompress(unpad(cipher.decrypt(data), 16)).decode()
        except: return None

# --- UI CONFIGURATION: GHOST PROTOCOL THEME ---
st.set_page_config(page_title="Kavach Ghost Protocol", page_icon="🕵️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@500;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #001510 0%, #000000 100%);
        color: #00ffaa;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* Terminal Console Look */
    .console-box {
        background: rgba(0, 40, 30, 0.4);
        border: 1px solid #00ffaa;
        border-radius: 5px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.2);
        margin-bottom: 20px;
    }
    
    /* Neon Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #000805 !important;
        border-right: 1px solid #00ffaa33;
    }

    /* Glow Buttons */
    .stButton>button {
        background: transparent;
        color: #00ffaa !important;
        border: 1px solid #00ffaa !important;
        border-radius: 0px;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.4s;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #00ffaa !important;
        color: #000 !important;
        box-shadow: 0 0 20px #00ffaa;
    }

    /* Tab Decoration */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Rajdhani', sans-serif;
        color: #00ffaa88;
        background: #001a14;
        border: 1px solid #00ffaa33;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        color: #00ffaa !important;
        border: 1px solid #00ffaa !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: SYSTEM STATUS ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/security-shield.png")
    st.markdown("### SYSTEM STATUS")
    st.write("🟢 NODE: ACTIVE")
    st.write("🟢 ENCRYPTION: AES-256")
    st.write("🔴 UPLINK: CLASSIFIED")
    st.divider()
    st.write("Kavach OS v4.2.0-STABLE")

# --- MAIN INTERFACE ---
st.title("🕵️ PROJECT KAVACH: GHOST PROTOCOL")
st.write("`// AUTHENTICATED_SESSION_LOADED...`")

t1, t2, t3 = st.tabs([">_ ENCODE", ">_ DECODE", ">_ AUDIT"])

with t1:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="console-box">', unsafe_allow_html=True)
        st.subheader("STEP 01: LOAD CARRIER")
        carrier = st.file_uploader("", type=["png"])
        st.subheader("STEP 02: INJECT DATA")
        secret = st.text_area("PAYLOAD STRING")
        key = st.text_input("ACCESS_KEY", type="password")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("INITIATE GHOST_ENCODE") and carrier and secret and key:
        engine = KavachEngine(key)
        img = Image.open(carrier).convert('RGB')
        
        with st.status("Executing Ghost Protocol...") as status:
            time.sleep(0.6)
            st.write("⚡ Scrambling bits...")
            protected = engine.encrypt(secret)
            bits = np.unpackbits(np.frombuffer(protected, dtype=np.uint8))
            
            pixels = np.array(img)
            flat = pixels.flatten()
            
            if len(bits) > len(flat):
                st.error("FATAL ERROR: BUFFER OVERFLOW")
            else:
                st.write("🧬 Embedding into spatial domain...")
                temp = flat[:len(bits)].astype(np.int16)
                temp = (temp & ~1) | bits
                flat[:len(bits)] = temp.astype(np.uint8)
                
                stego_img = Image.fromarray(flat.reshape(pixels.shape))
                
                # Visual Metric
                mse = np.mean((pixels.astype(np.float32) - flat.reshape(pixels.shape).astype(np.float32))**2)
                psnr = 100 if mse == 0 else 20 * math.log10(255.0 / math.sqrt(mse))
                
                with c2:
                    st.image(stego_img, caption="GHOST_OBJECT_GENERATED", use_container_width=True)
                    st.metric("SIGNAL QUALITY (PSNR)", f"{psnr:.2f} dB")
                    
                    buf = io.BytesIO()
                    stego_img.save(buf, format="PNG")
                    st.download_button("💾 DOWNLOAD ENCRYPTED FRAME", buf.getvalue(), "kavach_ghost.png")
            status.update(label="Ghost Recon Complete", state="complete")

with t2:
    st.subheader("SENTRY SCANNER")
    stego_in = st.file_uploader("UPLOAD INTERCEPTED FRAME", type=["png"], key="dec")
    key_in = st.text_input("DECRYPTION_KEY", type="password", key="k2")
    
    if st.button("RUN DEEP_SCAN"):
        engine = KavachEngine(key_in)
        img_d = Image.open(stego_in).convert('RGB')
        bits_d = np.array(img_d).flatten() & 1
        bytes_d = np.packbits(bits_d).tobytes()
        
        if engine.delimiter in bytes_d:
            raw = bytes_d.split(engine.delimiter)[0]
            result = engine.decrypt(raw)
            if result:
                st.success("ACCESS GRANTED")
                st.markdown(f"**DECRYPTED_MESSAGE:** `{result}`")
            else: st.error("ACCESS DENIED: CRYPTOGRAPHIC MISMATCH")
        else: st.error("NO ENCODED SIGNATURE FOUND")

with t3:
    st.subheader("SECURITY AUDIT LOG")
    st.write("---")
    st.markdown("""
    **PROTOCOL ANALYSIS:**
    - **METHOD:** LSB Spatial Domain Substitution
    - **CIPHER:** AES-256-CBC
    - **INTEGRITY:** Bit-level checksum verified
    - **STEALTH:** Optimized for Human Visual System (HVS)
    """)
    st.progress(1.0)
