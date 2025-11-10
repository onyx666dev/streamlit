# ============================================
# FILE: pages/data_transformation.py (NEW)
# ============================================
import streamlit as st
import pandas as pd
from utils.data_processing import (encode_categorical, normalize_data, 
                                   standardize_data, convert_column_type)

def render(df):
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("### 🔄 Data Transformation Tools")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Type Conversion
        st.markdown("#### 🔀 Column Type Conversion")
        st.markdown('<div class="cleaning-card">', unsafe_allow_html=True)
        
        col_to_convert = st.selectbox("Select column", df.columns.tolist(), key="convert_col")
        current_type = str(df[col_to_convert].dtype)
        st.write(f"Current type: `{current_type}`")
        
        new_type = st.selectbox(
            "Convert to",
            ["int", "float", "str", "datetime", "category"],
            key="new_type"
        )
        
        if st.button("🔄 Convert Type"):
            try:
                converted_df = convert_column_type(df, col_to_convert, new_type)
                st.session_state.df = converted_df
                st.session_state.cleaning_history.append(converted_df.copy())
                st.success(f"✓ Converted {col_to_convert} to {new_type}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Conversion failed: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Categorical Encoding
        st.markdown("#### 🏷️ Categorical Encoding")
        st.markdown('<div class="cleaning-card">', unsafe_allow_html=True)
        
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if cat_cols:
            col_to_encode = st.selectbox("Select categorical column", cat_cols, key="encode_col")
            encoding_method = st.selectbox(
                "Encoding method",
                ["Label Encoding", "One-Hot Encoding"],
                key="encoding_method"
            )
            
            if st.button("🔢 Encode Column"):
                try:
                    encoded_df = encode_categorical(df, col_to_encode, encoding_method)
                    st.session_state.df = encoded_df
                    st.session_state.cleaning_history.append(encoded_df.copy())
                    st.success(f"✓ Encoded {col_to_encode} using {encoding_method}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Encoding failed: {str(e)}")
        else:
            st.info("No categorical columns found")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Normalization & Standardization
        st.markdown("#### 📏 Feature Scaling")
        st.markdown('<div class="cleaning-card">', unsafe_allow_html=True)
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            cols_to_scale = st.multiselect(
                "Select columns to scale",
                numeric_cols,
                key="scale_cols"
            )
            
            scaling_method = st.selectbox(
                "Scaling method",
                ["Min-Max Normalization (0-1)", "Z-Score Standardization"],
                key="scaling_method"
            )
            
            if cols_to_scale and st.button("📊 Apply Scaling"):
                try:
                    if "Normalization" in scaling_method:
                        scaled_df = normalize_data(df, cols_to_scale)
                        method_name = "normalized"
                    else:
                        scaled_df = standardize_data(df, cols_to_scale)
                        method_name = "standardized"
                    
                    st.session_state.df = scaled_df
                    st.session_state.cleaning_history.append(scaled_df.copy())
                    st.success(f"✓ Successfully {method_name} {len(cols_to_scale)} columns")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Scaling failed: {str(e)}")
        else:
            st.info("No numeric columns found")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 Transformation Summary")
        
        summary_data = {
            "Category": ["Data Types", "Numeric", "Categorical", "Datetime", "Boolean"],
            "Count": [
                len(df.dtypes.unique()),
                len(df.select_dtypes(include=['number']).columns),
                len(df.select_dtypes(include=['object', 'category']).columns),
                len(df.select_dtypes(include=['datetime64']).columns),
                len(df.select_dtypes(include=['bool']).columns)
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("#### 💡 Tips")
        st.info("""
        **Transformation Guide:**
        - Convert types before analysis
        - Encode categories for ML models
        - Normalize for distance-based algorithms
        - Standardize for gradient descent
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)