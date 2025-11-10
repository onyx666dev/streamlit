# ============================================
# FILE: pages/data_cleaning.py
# ============================================
import streamlit as st
import pandas as pd
from utils.data_processing import remove_missing_values, fill_missing_values, remove_duplicates, clean_all
from utils.file_handlers import convert_df_to_csv

def render(df):
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("### 🧹 Data Cleaning Operations")
    st.markdown("Select a cleaning operation to process your dataset")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Missing Values Section
        st.markdown("#### ❌ Handle Missing Values")
        missing_count = df.isnull().sum().sum()
        
        if missing_count > 0:
            st.warning(f"⚠️ Found {missing_count} missing values in your dataset")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown('<div class="cleaning-card">', unsafe_allow_html=True)
                st.markdown("**🗑️ Remove Missing Values**")
                st.caption("Remove all rows containing any missing values")
                
                if st.button("🧹 Remove Missing Values", key="remove_missing"):
                    cleaned_df = remove_missing_values(df)
                    removed_rows = len(df) - len(cleaned_df)
                    st.success(f"✓ Removed {removed_rows} rows with missing values")
                    
                    csv = convert_df_to_csv(cleaned_df)
                    st.download_button(
                        label="📥 Download Cleaned CSV",
                        data=csv,
                        file_name="cleaned_data_no_missing.csv",
                        mime="text/csv",
                        key="download_no_missing"
                    )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_b:
                st.markdown('<div class="cleaning-card">', unsafe_allow_html=True)
                st.markdown("**🔧 Fill Missing Values**")
                st.caption("Fill missing: mode for object, interpolate for numeric")
                
                if st.button("🔧 Fill Missing Values", key="fill_missing"):
                    cleaned_df = fill_missing_values(df)
                    st.success(f"✓ Filled {missing_count} missing values")
                    
                    csv = convert_df_to_csv(cleaned_df)
                    st.download_button(
                        label="📥 Download Cleaned CSV",
                        data=csv,
                        file_name="cleaned_data_filled.csv",
                        mime="text/csv",
                        key="download_filled"
                    )
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("✓ No missing values found in the dataset!")
        
        st.markdown("---")
        
        # Duplicates Section
        st.markdown("#### 🔁 Handle Duplicate Rows")
        duplicate_count = df.duplicated().sum()
        
        if duplicate_count > 0:
            st.warning(f"⚠️ Found {duplicate_count} duplicate rows in your dataset")
            
            st.markdown('<div class="cleaning-card">', unsafe_allow_html=True)
            st.markdown("**🗑️ Remove Duplicate Rows**")
            st.caption("Keep only the first occurrence of each duplicate row")
            
            if st.button("🧹 Remove Duplicates", key="remove_duplicates"):
                cleaned_df = remove_duplicates(df)
                removed_rows = len(df) - len(cleaned_df)
                st.success(f"✓ Removed {removed_rows} duplicate rows")
                
                csv = convert_df_to_csv(cleaned_df)
                st.download_button(
                    label="📥 Download Cleaned CSV",
                    data=csv,
                    file_name="cleaned_data_no_duplicates.csv",
                    mime="text/csv",
                    key="download_no_duplicates"
                )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("✓ No duplicate rows found in the dataset!")
        
        st.markdown("---")
        
        # Combined Cleaning
        st.markdown("#### 🎯 Complete Data Cleaning")
        
        if missing_count > 0 or duplicate_count > 0:
            st.markdown('<div class="cleaning-card">', unsafe_allow_html=True)
            st.markdown("**✨ Apply All Cleaning Operations**")
            st.caption("Fill missing values + Remove duplicates in one step")
            
            if st.button("🚀 Clean All", key="clean_all"):
                initial_len = len(df)
                cleaned_df = clean_all(df)
                
                st.success(f"✓ Filled {missing_count} missing values and removed {initial_len - len(cleaned_df)} duplicates")
                
                csv = convert_df_to_csv(cleaned_df)
                st.download_button(
                    label="📥 Download Fully Cleaned CSV",
                    data=csv,
                    file_name="cleaned_data_complete.csv",
                    mime="text/csv",
                    key="download_complete"
                )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("✓ Dataset is already clean! No operations needed.")
    
    with col2:
        st.markdown("#### 📋 Cleaning Summary")
        
        summary_data = {
            "Metric": ["Total Rows", "Total Columns", "Missing Values", "Duplicate Rows"],
            "Count": [len(df), len(df.columns), missing_count, duplicate_count],
            "Status": [
                "✓" if len(df) > 0 else "⚠️",
                "✓" if len(df.columns) > 0 else "⚠️",
                "✓" if missing_count == 0 else "⚠️",
                "✓" if duplicate_count == 0 else "⚠️"
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("#### 💡 Tips")
        st.info("""
        **Best Practices:**
        - Always review your data before cleaning
        - Keep a backup of original data
        - Understand the impact of each operation
        - Test on a sample first
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
