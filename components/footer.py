# ============================================
# FILE: components/footer.py (Enhanced with Project Details)
# ============================================
import streamlit as st

def display_footer():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 2rem; border-top: 2px solid #e0e7ff; background: linear-gradient(135deg, #f8f9ff 0%, #fff5f8 100%); border-radius: 12px; margin-top: 2rem;'>
            <div style='display: inline-block; text-align: left; margin: 0.5rem 0;'>
                <p style='margin: 0.3rem 0; font-size: 0.9rem; color: #4a5568;'>
                    🎓 <strong>Info:</strong> 2nd Streamlit Application
                </p>
                <p style='margin: 0.3rem 0; font-size: 0.9rem; color: #4a5568;'>
                    👨‍🏫 <strong>Trainer:</strong> Yash Sharma
                </p>
                <p style='margin: 0.3rem 0; font-size: 0.9rem; color: #4a5568;'>
                    📚 <strong>Course:</strong> AI & Machine Learning Training
                </p>
                <p style='margin: 0.3rem 0; font-size: 0.9rem; color: #4a5568;'>
                    🏛️ <strong>Institution:</strong> Nexpert Academy
                </p>
            </div>
            <hr style='border: none; border-top: 1px solid #e0e7ff; margin: 1rem 0;'>
            <!-- <div style='text-align: center; color: #999; padding: 2rem; border-top: 1px solid #eee;'> -->
            <p style='margin: 0;'>Made with ❤️ by <b style='color: #667eea;'>ONYXCODE</b> using Streamlit | © 2025 PrePify Pro Dashboard</p>
            <!-- </div> -->
        </div>
    """, unsafe_allow_html=True)