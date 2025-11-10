# ============================================
# FILE: styles/custom_css.py (UPDATED - Add Scrollable Tabs)
# ============================================
import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Main styling */
        .main { padding: 0rem; }
        [data-testid="stSidebar"] { display: none; }
        
        /* Logo Styling */
        .logo-container {
            text-align: center;
            padding: 2rem 0 1rem 0;
            margin: 0 auto;
            animation: fadeIn 1.5s ease-in-out;
        }
        .logo-container img {
            max-width: 250px;
            height: auto;
            display: inline-block;
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
            transition: transform 0.4s ease;
        }
        .logo-container img:hover { transform: scale(1.05); }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Hero section */
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem 2rem 3rem 2rem;
            border-radius: 0 0 30px 30px;
            margin: 0 -1rem 2rem -1rem;
            color: white;
            text-align: center;
            animation: fadeIn 1.2s ease-in-out;
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .hero-subtitle {
            font-size: 1.2rem;
            opacity: 0.95;
            margin-top: 0.5rem;
        }
        
        /* Upload section */
        .upload-card {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            border: 2px dashed #667eea;
            text-align: center;
            margin: 2rem auto;
            max-width: 600px;
            animation: fadeIn 1.2s ease-in-out;
        }
        
        /* Stats cards */
        .stats-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1.5rem;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .stats-card:hover { transform: translateY(-5px); }
        .stats-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #667eea;
            margin: 0;
        }
        .stats-label {
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }
        
        /* Section headers */
        .section-header {
            font-size: 1.8rem;
            font-weight: 600;
            color: #2d3748;
            margin: 2rem 0 1rem 0;
            padding-left: 1rem;
            border-left: 4px solid #667eea;
        }
        
        /* ========================================== */
        /* ENHANCED TABS WITH SCROLLING - FIX HERE! */
        /* ========================================== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.8rem;
            background: #f7fafc;
            padding: 1rem;
            border-radius: 16px;
            overflow-x: auto !important;
            overflow-y: hidden;
            white-space: nowrap;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: thin;
            scrollbar-color: #667eea #f0f2f6;
            display: flex;
            flex-wrap: nowrap !important;
        }
        
        /* Custom scrollbar for Chrome/Safari/Edge */
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            height: 8px;
            margin-top: 10px;
        }
        
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-track {
            background: #f0f2f6;
            border-radius: 10px;
            margin: 0 10px;
        }
        
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            transition: background 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab"] {
            height: 60px;
            padding: 0 1.5rem;
            background: white;
            border-radius: 12px;
            color: #4a5568;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            flex-shrink: 0;
            min-width: fit-content;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        /* Scroll hint indicators */
        .stTabs [data-baseweb="tab-list"]::before,
        .stTabs [data-baseweb="tab-list"]::after {
            content: '';
            position: absolute;
            top: 0;
            bottom: 0;
            width: 30px;
            pointer-events: none;
            z-index: 1;
        }
        
        .stTabs [data-baseweb="tab-list"]::before {
            left: 0;
            background: linear-gradient(to right, #f7fafc 0%, transparent 100%);
        }
        
        .stTabs [data-baseweb="tab-list"]::after {
            right: 0;
            background: linear-gradient(to left, #f7fafc 0%, transparent 100%);
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Download button */
        .stDownloadButton>button {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4);
            transition: all 0.3s ease;
        }
        .stDownloadButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(72, 187, 120, 0.6);
        }
        
        /* File uploader */
        [data-testid="stFileUploader"] {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            border: 2px dashed #667eea;
        }
        
        /* Dataframe */
        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* Info box */
        .info-box {
            background: linear-gradient(135deg, #e0e7ff 0%, #f0e7ff 100%);
            padding: 1.5rem;
            border-radius: 16px;
            border-left: 4px solid #667eea;
            margin: 1rem 0;
            animation: fadeIn 1s ease-in-out;
        }
        
        /* Card container */
        .card-container {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            margin: 1rem 0;
        }
        
        /* Cleaning action card */
        .cleaning-card {
            background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
            padding: 1.5rem;
            border-radius: 16px;
            border-left: 4px solid #f56565;
            margin: 1rem 0;
            transition: transform 0.3s ease;
        }
        .cleaning-card:hover { transform: translateX(5px); }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 0 1rem;
                min-width: 120px;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)