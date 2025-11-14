# ============================================
# FILE: components/header.py (With Version Badge)
# ============================================
import streamlit as st
import os
import base64

def get_base64_of_svg(svg_path):
    with open(svg_path, "r") as svg_file:
        svg_content = svg_file.read()
    return base64.b64encode(svg_content.encode('utf-8')).decode()

def display_header():
    # Adjust the path to your SVG icon file
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    svg_path = os.path.join(base_dir, "assets", "prepify_icon.svg")
    
    if os.path.exists(svg_path):
        svg_base64 = get_base64_of_svg(svg_path)
        svg_img_html = f'<img src="data:image/svg+xml;base64,{svg_base64}" style="height:1.7em; vertical-align:middle; margin-right:0.5em;" alt="Icon">'
    else:
        svg_img_html = "📊"  # fallback emoji if SVG not found

    st.markdown(f"""
        <div class="hero-section">
            <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; flex-wrap: wrap;">
                <h1 class="hero-title" style="display: flex; align-items: center; gap: 0.5rem;">
                    {svg_img_html}
                    PrePify Pro Dashboard
                </h1>
                <span style="background: rgba(255,255,255,0.25); 
                             padding: 0.4rem 1rem; 
                             border-radius: 25px; 
                             font-size: 0.95rem; 
                             font-weight: 700;
                             color: white;
                             border: 2px solid rgba(255,255,255,0.3);
                             box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                             letter-spacing: 0.5px;">
                    v2.0.0 Enhanced
                </span>
            </div>
            <p class="hero-subtitle">Powerful Data Analysis & Visualization Platform</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; opacity: 0.9;">
                🎓 1st Streamlit App | 👨‍🏫 Trainer: Yash Sharma | 📚 Course: AI & Machine Learning Training | 🏛️ Nexpert Academy
            </p>
        </div>
    """, unsafe_allow_html=True)

