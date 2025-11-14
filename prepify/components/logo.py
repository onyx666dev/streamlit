# ============================================
# FILE: components/logo.py
# ============================================
import streamlit as st
import os
import base64

def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def display_logo():
    # Get absolute path to project root (one level up from components/)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    logo_path = os.path.join(base_dir, "assets", "onyxcode_black.png")
    
    if os.path.exists(logo_path):
        st.markdown(f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{get_base64_of_image(logo_path)}" alt="OnyxCode Logo">
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Logo not found — make sure 'assets/onyxcode_black.png' exists.")

