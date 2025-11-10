# ============================================
# FILE: app.py (Enhanced Main Entry Point)
# ============================================
import streamlit as st
import pandas as pd
from components.whats_new import show_whats_new, show_version_badge
from config.settings import ENABLE_WHATS_NEW, ENABLE_VERSION_BADGE
from styles.custom_css import apply_custom_css
from components.logo import display_logo
from components.header import display_header
from components.footer import display_footer
from pages import (data_explorer, data_cleaning, data_insights, 
                   visualizations, advanced_analytics, data_transformation,
                   outlier_detection, time_series_analysis, changelog)

# Page configuration
st.set_page_config(
    page_title="PrePify Pro Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styling
apply_custom_css()

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'data_filtered' not in st.session_state:
    st.session_state.data_filtered = False
if 'cleaning_history' not in st.session_state:
    st.session_state.cleaning_history = []

# Display logo and header
display_logo()
display_header()

# Show What's New notification (only for new users or version updates)
if ENABLE_WHATS_NEW:
    show_whats_new()

# Show version badge (optional - floating badge in corner)
if ENABLE_VERSION_BADGE:
    show_version_badge()

# Main application logic
if st.session_state.df is None:
    # File upload section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        st.markdown("### 📁 Upload Your Dataset")
        st.markdown("Supports CSV, Excel (.xlsx, .xls), and JSON files")
        
        uploaded_file = st.file_uploader(
            "", 
            type=['csv', 'xlsx', 'xls', 'json'], 
            label_visibility="collapsed"
        )
        
        # File size limit warning
        if uploaded_file is not None:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > 200:
                st.error(f"⚠️ File size ({file_size_mb:.1f} MB) exceeds 200 MB limit")
                uploaded_file = None
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            try:
                # Determine file type and read accordingly
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                with st.spinner('Loading your data...'):
                    if file_extension == 'csv':
                        df = pd.read_csv(uploaded_file)
                    elif file_extension in ['xlsx', 'xls']:
                        df = pd.read_excel(uploaded_file)
                    elif file_extension == 'json':
                        df = pd.read_json(uploaded_file)
                    
                    # Store both original and working copy
                    st.session_state.df = df
                    st.session_state.original_df = df.copy()
                    st.success(f"✓ Successfully loaded: {uploaded_file.name}")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.info("💡 Make sure your file is properly formatted")

    # Enhanced Feature highlights
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">✨ Enhanced Features</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("📋", "Data Explorer", "Advanced filtering & sampling"),
        ("🧹", "Smart Cleaning", "Intelligent data processing"),
        ("📈", "Rich Visualizations", "20+ chart types"),
        ("🔍", "Deep Analytics", "ML-powered insights")
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
                <div class="info-box" style="text-align: center;">
                    <div style="font-size: 3rem;">{icon}</div>
                    <div style="font-weight: 600; margin: 0.5rem 0;">{title}</div>
                    <div style="font-size: 0.9rem; color: #666;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # New features section
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    new_features = [
        ("🎯", "Outlier Detection", "Z-score & IQR methods"),
        ("🔄", "Data Transform", "Type conversion & encoding"),
        ("⏱️", "Time Series", "Temporal analysis")
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3], new_features):
        with col:
            st.markdown(f"""
                <div class="info-box" style="text-align: center;">
                    <div style="font-size: 2.5rem;">{icon}</div>
                    <div style="font-weight: 600; margin: 0.5rem 0;">{title}</div>
                    <div style="font-size: 0.9rem; color: #666;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)

else:
    # Data loaded - show enhanced dashboard
    df = st.session_state.df
    
    # Top controls with enhanced features
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        st.markdown(f'<p style="font-size: 1.2rem; color: #666; margin-top: 1rem;">📄 Dataset: <strong>{len(df):,} rows × {len(df.columns)} columns</strong> | Size: <strong>{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB</strong></p>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Reset Data"):
            if st.session_state.original_df is not None:
                st.session_state.df = st.session_state.original_df.copy()
                st.session_state.data_filtered = False
                st.session_state.cleaning_history = []
                st.success("✓ Data reset to original")
                st.rerun()
    with col3:
        if st.session_state.cleaning_history:
            if st.button("↩️ Undo Last"):
                if len(st.session_state.cleaning_history) > 0:
                    st.session_state.cleaning_history.pop()
                    if st.session_state.cleaning_history:
                        st.session_state.df = st.session_state.cleaning_history[-1].copy()
                    else:
                        st.session_state.df = st.session_state.original_df.copy()
                    st.rerun()
    with col4:
        if st.button("📤 New File"):
            for key in ['df', 'cleaned_df', 'original_df', 'data_filtered', 'cleaning_history']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Enhanced Quick Stats
    st.markdown('<h2 class="section-header">📊 Quick Statistics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    stats = [
        ("📝", "Total Rows", f"{len(df):,}"),
        ("📋", "Columns", f"{len(df.columns)}"),
        ("🔢", "Numeric", f"{len(numeric_cols)}"),
        ("🏷️", "Categorical", f"{len(categorical_cols)}"),
        ("❌", "Missing", f"{df.isnull().sum().sum():,}"),
        ("🔁", "Duplicates", f"{df.duplicated().sum():,}")
    ]
    
    for col, (icon, label, value) in zip([col1, col2, col3, col4, col5, col6], stats):
        with col:
            st.markdown(f"""
                <div class="stats-card">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div class="stats-number">{value}</div>
                    <div class="stats-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enhanced Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📋 Data Explorer", 
    "🔄 Transformation",
    "🎯 Outlier Detection",
    "🔍 Data Insights", 
    "📈 Visualizations", 
    "📊 Advanced Analytics",
    "⏱️ Time Series",
    "🧹 Data Cleaning",
    "📋 Changelog"  # ← ADD THIS
])
    
    with tab1:
        data_explorer.render(df)
    
    with tab2:
        data_transformation.render(df)
    
    with tab3:
        outlier_detection.render(df)
    
    with tab4:
        data_insights.render(df)
    
    with tab5:
        visualizations.render(df)
    
    with tab6:
        advanced_analytics.render(df)
    
    with tab7:
        time_series_analysis.render(df)

    with tab8:
        data_cleaning.render(df)
    
    with tab9:
        changelog.render()

# Display footer
display_footer()