# ============================================
# FILE: pages/outlier_detection.py (NEW)
# ============================================
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.data_processing import detect_outliers_zscore, detect_outliers_iqr, remove_outliers

def render(df):
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("### 🎯 Outlier Detection & Handling")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if not numeric_cols:
        st.warning("⚠️ No numeric columns found for outlier detection")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🔍 Detect Outliers")
        
        # Column selection
        selected_col = st.selectbox("Select column for analysis", numeric_cols)
        
        # Method selection
        method = st.selectbox(
            "Detection method",
            ["Z-Score (3σ)", "IQR (Interquartile Range)", "Both Methods"],
            help="Z-Score: values beyond 3 standard deviations | IQR: values beyond 1.5 * IQR"
        )
        
        # Detect outliers
        if selected_col:
            col_data = df[selected_col].dropna()
            
            # Calculate outliers
            if "Z-Score" in method or method == "Both Methods":
                zscore_outliers = detect_outliers_zscore(df, selected_col)
                zscore_count = len(zscore_outliers)
            
            if "IQR" in method or method == "Both Methods":
                iqr_outliers = detect_outliers_iqr(df, selected_col)
                iqr_count = len(iqr_outliers)
            
            # Display results
            st.markdown("##### 📊 Outlier Statistics")
            
            if method == "Z-Score (3σ)":
                st.metric("Outliers Detected (Z-Score)", zscore_count)
                outlier_indices = zscore_outliers
            elif method == "IQR (Interquartile Range)":
                st.metric("Outliers Detected (IQR)", iqr_count)
                outlier_indices = iqr_outliers
            else:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Z-Score Method", zscore_count)
                with col_b:
                    st.metric("IQR Method", iqr_count)
                # Use union of both methods
                outlier_indices = list(set(zscore_outliers) | set(iqr_outliers))
            
            # Visualization
            st.markdown("##### 📈 Visual Analysis")
            
            # Create box plot with outliers highlighted
            fig = go.Figure()
            
            # Box plot
            fig.add_trace(go.Box(
                y=col_data,
                name=selected_col,
                boxmean='sd',
                marker_color='lightblue'
            ))
            
            # Highlight outliers
            if outlier_indices:
                outlier_values = df.loc[outlier_indices, selected_col]
                fig.add_trace(go.Scatter(
                    y=outlier_values,
                    mode='markers',
                    name='Outliers',
                    marker=dict(color='red', size=8, symbol='x')
                ))
            
            fig.update_layout(
                title=f'Box Plot with Outliers - {selected_col}',
                template='plotly_white',
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Histogram with outliers
            fig2 = go.Figure()
            
            fig2.add_trace(go.Histogram(
                x=col_data,
                name='Distribution',
                marker_color='lightgreen',
                opacity=0.7
            ))
            
            if outlier_indices:
                outlier_values = df.loc[outlier_indices, selected_col]
                fig2.add_trace(go.Histogram(
                    x=outlier_values,
                    name='Outliers',
                    marker_color='red',
                    opacity=0.7
                ))
            
            fig2.update_layout(
                title=f'Distribution with Outliers - {selected_col}',
                template='plotly_white',
                height=350,
                showlegend=True,
                barmode='overlay'
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Show outlier data
            if outlier_indices:
                with st.expander(f"🔍 View {len(outlier_indices)} Outlier Records"):
                    st.dataframe(df.loc[outlier_indices], use_container_width=True)
            
            # Handling options
            st.markdown("##### 🛠️ Handle Outliers")
            
            if outlier_indices:
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("🗑️ Remove Outliers"):
                        cleaned_df = remove_outliers(df, selected_col, method)
                        st.session_state.df = cleaned_df
                        st.session_state.cleaning_history.append(cleaned_df.copy())
                        st.success(f"✓ Removed {len(outlier_indices)} outlier rows")
                        st.rerun()
                
                with col_b:
                    if st.button("📊 Cap at Percentiles"):
                        capped_df = df.copy()
                        lower = capped_df[selected_col].quantile(0.01)
                        upper = capped_df[selected_col].quantile(0.99)
                        capped_df[selected_col] = capped_df[selected_col].clip(lower, upper)
                        st.session_state.df = capped_df
                        st.session_state.cleaning_history.append(capped_df.copy())
                        st.success(f"✓ Capped values at 1st and 99th percentiles")
                        st.rerun()
                
                with col_c:
                    if st.button("🔄 Replace with Median"):
                        replaced_df = df.copy()
                        median_val = replaced_df[selected_col].median()
                        replaced_df.loc[outlier_indices, selected_col] = median_val
                        st.session_state.df = replaced_df
                        st.session_state.cleaning_history.append(replaced_df.copy())
                        st.success(f"✓ Replaced {len(outlier_indices)} outliers with median")
                        st.rerun()
    
    with col2:
        st.markdown("#### 📊 Column Statistics")
        
        if selected_col:
            stats = df[selected_col].describe()
            
            stats_display = pd.DataFrame({
                'Statistic': ['Count', 'Mean', 'Std Dev', 'Min', '25%', '50%', '75%', 'Max'],
                'Value': [
                    f"{stats['count']:.0f}",
                    f"{stats['mean']:.2f}",
                    f"{stats['std']:.2f}",
                    f"{stats['min']:.2f}",
                    f"{stats['25%']:.2f}",
                    f"{stats['50%']:.2f}",
                    f"{stats['75%']:.2f}",
                    f"{stats['max']:.2f}"
                ]
            })
            
            st.dataframe(stats_display, use_container_width=True, hide_index=True)
            
            # Additional metrics
            st.markdown("---")
            st.markdown("#### 📈 Additional Metrics")
            
            col_data = df[selected_col].dropna()
            
            metrics = {
                "Range": f"{col_data.max() - col_data.min():.2f}",
                "IQR": f"{col_data.quantile(0.75) - col_data.quantile(0.25):.2f}",
                "Skewness": f"{col_data.skew():.2f}",
                "Kurtosis": f"{col_data.kurtosis():.2f}"
            }
            
            for metric, value in metrics.items():
                st.metric(metric, value)
        
        st.markdown("---")
        st.markdown("#### 💡 Tips")
        st.info("""
        **Outlier Handling:**
        - **Z-Score**: Best for normal distributions
        - **IQR**: More robust to extreme values
        - **Remove**: Use with caution
        - **Cap**: Preserve data size
        - **Replace**: Maintain distribution
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)