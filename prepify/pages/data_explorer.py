# ============================================
# FILE: pages/data_explorer.py (Enhanced)
# ============================================
import streamlit as st
import pandas as pd
from utils.file_handlers import convert_df_to_csv, convert_df_to_excel, convert_df_to_json

def render(df):
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    
    # Header with export options
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown('<h3 style="color: #2d3748;">📊 Data Preview & Exploration</h3>', unsafe_allow_html=True)
    with col2:
        n_rows = st.number_input("Rows to display", min_value=5, max_value=500, value=10, step=5)
    with col3:
        export_format = st.selectbox("Export as", ["CSV", "Excel", "JSON"])
    
    # Data sampling option
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("#### 🎲 Data Sampling")
    with col2:
        use_sampling = st.checkbox("Enable sampling", value=False)
    
    display_df = df
    if use_sampling:
        col1, col2, col3 = st.columns(3)
        with col1:
            sample_method = st.selectbox("Method", ["Random", "First N", "Last N"])
        with col2:
            sample_size = st.number_input("Sample size", min_value=1, max_value=len(df), value=min(1000, len(df)))
        with col3:
            if sample_method == "Random":
                random_seed = st.number_input("Random seed", value=42)
        
        if sample_method == "Random":
            display_df = df.sample(n=min(sample_size, len(df)), random_state=random_seed)
            st.info(f"📊 Showing random sample of {len(display_df)} rows")
        elif sample_method == "First N":
            display_df = df.head(sample_size)
            st.info(f"📊 Showing first {len(display_df)} rows")
        else:
            display_df = df.tail(sample_size)
            st.info(f"📊 Showing last {len(display_df)} rows")
    
    # Column selector
    with st.expander("🔽 Select Columns to Display"):
        all_cols = df.columns.tolist()
        selected_cols = st.multiselect(
            "Choose columns",
            options=all_cols,
            default=all_cols,
            help="Select specific columns to view"
        )
        
        if selected_cols:
            display_df = display_df[selected_cols]
    
    # Display dataframe
    st.dataframe(display_df.head(n_rows), use_container_width=True, height=400)
    
    # Export button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if export_format == "CSV":
            csv_data = convert_df_to_csv(display_df)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name="exported_data.csv",
                mime="text/csv"
            )
        elif export_format == "Excel":
            excel_data = convert_df_to_excel(display_df)
            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name="exported_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            json_data = convert_df_to_json(display_df)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name="exported_data.json",
                mime="application/json"
            )
    
    # Enhanced column details
    with st.expander("🔽 Detailed Column Information"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📊 Numeric Columns:**")
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                for col in numeric_cols:
                    st.write(f"• {col} ({df[col].dtype})")
            else:
                st.write("None")
        
        with col2:
            st.markdown("**🏷️ Categorical Columns:**")
            cat_cols = df.select_dtypes(include=['object']).columns.tolist()
            if cat_cols:
                for col in cat_cols:
                    st.write(f"• {col} (unique: {df[col].nunique()})")
            else:
                st.write("None")
        
        with col3:
            st.markdown("**📅 Datetime Columns:**")
            date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            if date_cols:
                for col in date_cols:
                    st.write(f"• {col}")
            else:
                st.write("None")
    
    # Data filtering
    with st.expander("🔍 Filter Data"):
        st.markdown("**Apply filters to your dataset**")
        
        filter_col = st.selectbox("Select column to filter", df.columns.tolist())
        
        if filter_col:
            if df[filter_col].dtype in ['int64', 'float64']:
                # Numeric filtering
                min_val = float(df[filter_col].min())
                max_val = float(df[filter_col].max())
                
                filter_range = st.slider(
                    f"Range for {filter_col}",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val)
                )
                
                if st.button("Apply Numeric Filter"):
                    filtered_df = df[(df[filter_col] >= filter_range[0]) & (df[filter_col] <= filter_range[1])]
                    st.session_state.df = filtered_df
                    st.session_state.data_filtered = True
                    st.success(f"✓ Filtered to {len(filtered_df)} rows")
                    st.rerun()
            else:
                # Categorical filtering
                unique_vals = df[filter_col].unique().tolist()
                selected_vals = st.multiselect(
                    f"Select values for {filter_col}",
                    options=unique_vals,
                    default=unique_vals[:min(5, len(unique_vals))]
                )
                
                if st.button("Apply Categorical Filter"):
                    filtered_df = df[df[filter_col].isin(selected_vals)]
                    st.session_state.df = filtered_df
                    st.session_state.data_filtered = True
                    st.success(f"✓ Filtered to {len(filtered_df)} rows")
                    st.rerun()
    
    # Search functionality
    with st.expander("🔎 Search Data"):
        search_col = st.selectbox("Search in column", df.columns.tolist(), key="search_col")
        search_term = st.text_input("Enter search term")
        
        if search_term:
            if df[search_col].dtype == 'object':
                search_results = df[df[search_col].str.contains(search_term, case=False, na=False)]
            else:
                try:
                    search_results = df[df[search_col] == float(search_term)]
                except:
                    search_results = pd.DataFrame()
            
            st.write(f"Found {len(search_results)} matching rows")
            if len(search_results) > 0:
                st.dataframe(search_results, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)