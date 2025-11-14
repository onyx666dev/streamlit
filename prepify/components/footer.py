# ============================================
# FILE: components/footer.py (Enhanced with Project Details)
# ============================================


import streamlit as st

def display_footer():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='
            text-align: center;
            color: #666;
            padding: 1.5rem 1rem;
            border: 2px solid #e0e7ff;
            background: linear-gradient(135deg, #f8f9ff 0%, #fff5f8 100%);
            border-radius: 12px;
            margin-top: 2rem;
            font-size: 0.85rem;
            font-weight: 400;
            font-family: Arial, sans-serif;
        '>
            <i>Made with ❤️ by <b style='color: #667eea;'>ONYXCODE</b> using Streamlit | © 2025 PrePify Pro Dashboard</i>
        </div>
    """, unsafe_allow_html=True)




