# ============================================
# FILE: components/whats_new.py (NEW)
# ============================================
import streamlit as st

def show_whats_new():
    """Display What's New notification for new version"""
    
    # Initialize session state for version tracking
    if 'last_seen_version' not in st.session_state:
        st.session_state.last_seen_version = "1.0.0"
    
    if 'dismissed_whats_new' not in st.session_state:
        st.session_state.dismissed_whats_new = False
    
    current_version = "2.0.0"
    
    # Show notification if user hasn't seen this version
    if (st.session_state.last_seen_version != current_version and 
        not st.session_state.dismissed_whats_new):
        
        with st.expander("🎉 What's New in v2.0.0 - Enhanced Edition! Click to explore →", expanded=True):
            st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            color: white;
                            margin-bottom: 1rem;'>
                    <h3 style='margin: 0; color: white;'>🚀 Major Update Released!</h3>
                    <p style='margin: 0.5rem 0 0 0; opacity: 0.95;'>
                        We've added 40+ new features to make your data analysis even better!
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**🆕 New Features**")
                st.markdown("""
                - 📊 **13+ Chart Types**
                  - 3D Scatter, Treemap, Sunburst
                - 🎯 **Outlier Detection**
                  - Z-Score & IQR methods
                - ⏱️ **Time Series Analysis**
                  - Moving averages & trends
                - 🔄 **Data Transformation**
                  - Encoding & scaling tools
                """)
            
            with col2:
                st.markdown("**✨ Improvements**")
                st.markdown("""
                - 📁 **Multi-format Support**
                  - Excel, JSON, CSV
                - 🔍 **Advanced Filtering**
                  - Smart data sampling
                - 📥 **Export Options**
                  - Multiple formats
                - 🔙 **Undo/Redo**
                  - Change history tracking
                """)
            
            with col3:
                st.markdown("**🐛 Bug Fixes**")
                st.markdown("""
                - ✅ Heatmap colorscale fixed
                - ✅ Better error handling
                - ✅ Performance optimized
                - ✅ Session state improved
                
                **📊 Statistics**
                - 40+ new features
                - 3 new pages
                - 15+ bug fixes
                """)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("📋 View Full Changelog", use_container_width=True):
                    st.session_state.dismissed_whats_new = True
                    st.session_state.last_seen_version = current_version
                    st.info("💡 You can always view the changelog in the Changelog tab!")
                    st.rerun()
            
            with col2:
                if st.button("✅ Got it, thanks!", use_container_width=True):
                    st.session_state.dismissed_whats_new = True
                    st.session_state.last_seen_version = current_version
                    st.success("🎉 Enjoy the new features!")
                    st.rerun()
            
            with col3:
                if st.button("⏭️ Remind me later", use_container_width=True):
                    st.session_state.dismissed_whats_new = True
                    st.info("We'll remind you next time!")
                    st.rerun()


def show_version_badge():
    """Show a small version badge in the corner"""
    st.markdown("""
        <div style='position: fixed;
                    bottom: 20px;
                    right: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-size: 0.85rem;
                    font-weight: 600;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                    z-index: 1000;
                    cursor: pointer;'>
            v2.0.0
        </div>
    """, unsafe_allow_html=True)