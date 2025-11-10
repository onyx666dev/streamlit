# ============================================
# FILE: components/header.py (With Version Badge)
# ============================================
import streamlit as st

def display_header():
    st.markdown("""
        <div class="hero-section">
            <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; flex-wrap: wrap;">
                <h1 class="hero-title">📊 PrePify Pro Dashboard</h1>
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