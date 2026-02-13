import streamlit as st
import numpy as np
import zlib, hashlib, math, io, time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image

# --- MODULE 2: THE FORTRESS (Logic) ---
class KavachEngine:
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()
        self.delimiter = b'::KAVACH_EOS::'

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        # Structure: IV + Encrypted Data + Delimiter
        return cipher.iv + cipher.encrypt(pad(zlib.compress(text.encode()), 16)) + self.delimiter

    def decrypt(self, blob):
        try:
            iv, data = blob[:16], blob[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(data), 16)
            return zlib.decompress(decrypted).decode()
        except:
            return None

# --- UI CONFIG & CYBERPUNK STYLING ---
st.set_page_config(page_title="Project Kavach", page_icon="☣️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
    
    .stApp {
        background-color: #0a0a0b;
        color: #00ffcc;
        font-family: 'Fira Code', monospace;
    }
    
    /* Neon Borders for Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #121214 !important;
        color: #00ffcc !important;
        border: 1px solid #00ffcc44 !important;
    }
    
    /* Futuristic Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1c;
        border: 1px solid #333;
        padding: 10px 30px;
        color: #888;
    }

    .stTabs [aria-selected="true"] {
        color: #00ffcc !important;
        border: 1px solid #00ffcc !important;
        box-shadow: 0 0 10px #00ffcc44;
    }

    /* Metric Cards */
    [data-testid="stMetricValue"] {
        color: #00ffcc;
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("☣️ KAVACH SYSTEM TERMINAL")
st.write("`STATUS: ENCRYPTION_ACTIVE | PROTOCOL: AES-256-CBC`")
st.divider()

tab1, tab2, tab3 = st.tabs(["[ 1 ] THE SHIELD (Encoder)", "[ 2 ] THE SENTRY (Decoder)", "[ 3 ] SYSTEM_LOGS"])

# --- MODULE 1: ENCODER ---
with tab1:
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.subheader("📡 Input Stream")
        carrier = st.file_uploader("Upload Carrier Frame (PNG)", type=["png"])
        secret = st.text_area("Secret Message", height=150, placeholder="Classified information...")
        key = st.text_input("Security Key", type="password")
        
    if st.button("ACTIVATE KAVACH SHIELD") and carrier and secret and key:
        with st.status("Initializing Stealth Sequence...") as status:
            engine = KavachEngine(key)
            img = Image.open(carrier).convert('RGB')
            pixels = np.array(img)
            
            st.write("Locking Cryptographic Layer...")
            protected_blob = engine.encrypt(secret)
            bits = np.unpackbits(np.frombuffer(protected_blob, dtype=np.uint8))
            
            flat_pixels = pixels.flatten()
            
            if len(bits) > len(flat_pixels):
                st.error("INSUFFICIENT_CAPACITY: Image frame too small.")
            else:
                st.write("Injecting Bits into Spatial Domain...")
                # PREVENT OVERFLOW ERROR: Use int16 for math
                temp = flat_pixels[:len(bits)].astype(np.int16)
                temp = (temp & ~1) | bits
                flat_pixels[:len(bits)] = temp.astype(np.uint8)
                
                stego_img = Image.fromarray(flat_pixels.reshape(pixels.shape))
                
                # MODULE 3 ANALYSIS: PSNR
                mse = np.mean((pixels.astype(np.float32) - flat_pixels.reshape(pixels.shape).astype(np.float32)) ** 2)
                psnr = 100.0 if mse == 0 else 20 * math.log10(255.0 / math.sqrt(mse))
                
                with col_r:
                    st.subheader("🛰️ Output Verification")
                    st.image(stego_img, caption="Stego-Object (Hidden Data)", use_container_width=True)
                    
                    m1, m2 = st.columns(2)
                    m1.metric("Visual Integrity", f"{psnr:.2f} dB")
                    m2.metric("Data Density", f"{len(bits)} bits")
                    
                    buf = io.BytesIO()
                    stego_img.save(buf, format="PNG")
                    st.download_button("💾 DOWNLOAD SHIELDED IMAGE", buf.getvalue(), "kavach_stego.png")
            status.update(label="Sequence Complete", state="complete")

# --- MODULE 3: DECODER ---
with tab2:
    st.subheader("🔍 Deep Scan Analysis")
    stego_file = st.file_uploader("Analyze Stego-Image", type=["png"], key="dec")
    dec_pass = st.text_input("Sentry Access Key", type="password", key="p2")
    
    if st.button("RUN EXTRACTION") and stego_file and dec_pass:
        engine = KavachEngine(dec_pass)
        img = Image.open(stego_file).convert('RGB')
        pixels = np.array(img).flatten()
        
        # Extraction logic
        bits = pixels & 1
        byte_arr = np.packbits(bits).tobytes()
        
        if engine.delimiter in byte_arr:
            payload = byte_arr.split(engine.delimiter)[0]
            decoded = engine.decrypt(payload)
            
            if decoded:
                st.success("✅ DECRYPTION SUCCESSFUL")
                st.code(decoded, language="text")
            else:
                st.error("❌ KEY MISMATCH: Access Denied")
        else:
            st.error("⚠️ NO KAVACH PAYLOAD DETECTED")

# --- SYSTEM SPECS ---
with tab3:
    st.subheader("⚙️ Hardware & Protocol Specs")
    st.markdown("""
    - **Encryption Engine:** AES-256 (Cipher Block Chaining)
    - **Key Stretching:** SHA-256 Digest
    - **Methodology:** LSB Substitution with Integer-Hardening
    - **Visual Metrics:** PSNR-based Integrity Check
    """)
    st.progress(1.0)
    st.write("`System integrity 100% | Uptime: Battle Ready`")
