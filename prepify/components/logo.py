# ============================================
# FILE: components/logo.py
# ============================================
import streamlit as st
import os
import base64

def get_base64_of_svg(svg_path):
    with open(svg_path, "r") as svg_file:
        svg_content = svg_file.read()
    return base64.b64encode(svg_content.encode('utf-8')).decode()

def display_logo():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    svg_path = os.path.join(base_dir, "assets", "prepify_icon.svg")
    
    if os.path.exists(svg_path):
        svg_base64 = get_base64_of_svg(svg_path)
        st.markdown(f"""
            <div class="logo-container">
                <img src="data:image/svg+xml;base64,{svg_base64}" alt="OnyxCode Logo" style="height: 60px;">
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ SVG Logo not found — make sure 'assets/onyxcode_black.svg' exists.")


