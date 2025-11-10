# ============================================
# FILE: pages/time_series_analysis.py (NEW)
# ============================================
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def render(df):
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("### ⏱️ Time Series Analysis")
    
    # Check for datetime columns
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Try to identify potential date columns
    potential_date_cols = []
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                pd.to_datetime(df[col].head(10))
                potential_date_cols.append(col)
            except:
                pass
    
    if not datetime_cols and not potential_date_cols:
        st.warning("⚠️ No datetime columns detected in your dataset")
        st.info("💡 Try converting a column to datetime in the Data Transformation tab")
        
        # Show columns that might be dates
        st.markdown("#### 🔍 Potential Date Columns")
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        if text_cols:
            st.write("Columns that might contain dates:", ", ".join(text_cols[:5]))
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Combine datetime and potential date columns
    all_date_cols = datetime_cols + potential_date_cols
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📅 Select Time Series Data")
        
        # Date column selection
        date_col = st.selectbox("Select date column", all_date_cols)
        
        # Convert if needed
        if date_col in potential_date_cols:
            try:
                df[date_col] = pd.to_datetime(df[date_col])
                st.success(f"✓ Converted {date_col} to datetime")
            except Exception as e:
                st.error(f"❌ Could not convert to datetime: {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        # Value column selection
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            st.warning("No numeric columns found for time series analysis")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        value_col = st.selectbox("Select value column", numeric_cols)
        
        # Sort by date
        df_sorted = df.sort_values(date_col)
        
        # Basic time series plot
        st.markdown("#### 📈 Time Series Visualization")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_sorted[date_col],
            y=df_sorted[value_col],
            mode='lines+markers',
            name=value_col,
            line=dict(color='#667eea', width=2),
            marker=dict(size=4)
        ))
        
        fig.update_layout(
            title=f'{value_col} over Time',
            xaxis_title='Date',
            yaxis_title=value_col,
            template='plotly_white',
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Aggregation options
        st.markdown("#### 📊 Time-Based Aggregation")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            agg_period = st.selectbox(
                "Aggregation period",
                ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"]
            )
        
        with col_b:
            agg_method = st.selectbox(
                "Aggregation method",
                ["Mean", "Sum", "Count", "Min", "Max", "Median"]
            )
        
        # Perform aggregation
        df_agg = df_sorted.copy()
        df_agg.set_index(date_col, inplace=True)
        
        period_map = {
            "Daily": "D",
            "Weekly": "W",
            "Monthly": "M",
            "Quarterly": "Q",
            "Yearly": "Y"
        }
        
        method_map = {
            "Mean": "mean",
            "Sum": "sum",
            "Count": "count",
            "Min": "min",
            "Max": "max",
            "Median": "median"
        }
        
        try:
            aggregated = df_agg[value_col].resample(period_map[agg_period]).agg(method_map[agg_method])
            
            fig2 = go.Figure()
            
            fig2.add_trace(go.Bar(
                x=aggregated.index,
                y=aggregated.values,
                name=f'{agg_method} by {agg_period}',
                marker_color='#48bb78'
            ))
            
            fig2.update_layout(
                title=f'{agg_method} of {value_col} by {agg_period}',
                xaxis_title='Date',
                yaxis_title=value_col,
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Aggregation failed: {str(e)}")
        
        # Moving average
        st.markdown("#### 📉 Moving Average")
        
        window_size = st.slider("Window size (periods)", min_value=2, max_value=30, value=7)
        
        try:
            df_sorted['Moving_Avg'] = df_sorted[value_col].rolling(window=window_size).mean()
            
            fig3 = go.Figure()
            
            fig3.add_trace(go.Scatter(
                x=df_sorted[date_col],
                y=df_sorted[value_col],
                mode='lines',
                name='Original',
                line=dict(color='lightgray', width=1),
                opacity=0.5
            ))
            
            fig3.add_trace(go.Scatter(
                x=df_sorted[date_col],
                y=df_sorted['Moving_Avg'],
                mode='lines',
                name=f'{window_size}-Period MA',
                line=dict(color='#667eea', width=3)
            ))
            
            fig3.update_layout(
                title=f'{value_col} with {window_size}-Period Moving Average',
                xaxis_title='Date',
                yaxis_title=value_col,
                template='plotly_white',
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig3, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Moving average calculation failed: {str(e)}")
    
    with col2:
        st.markdown("#### 📊 Time Series Statistics")
        
        try:
            # Date range
            st.metric("Start Date", df_sorted[date_col].min().strftime('%Y-%m-%d'))
            st.metric("End Date", df_sorted[date_col].max().strftime('%Y-%m-%d'))
            
            # Duration
            duration = df_sorted[date_col].max() - df_sorted[date_col].min()
            st.metric("Duration (days)", duration.days)
            
            st.markdown("---")
            
            # Value statistics
            st.markdown("**Value Statistics:**")
            st.metric("Mean", f"{df_sorted[value_col].mean():.2f}")
            st.metric("Std Dev", f"{df_sorted[value_col].std():.2f}")
            st.metric("Min", f"{df_sorted[value_col].min():.2f}")
            st.metric("Max", f"{df_sorted[value_col].max():.2f}")
            
        except Exception as e:
            st.error(f"Error calculating statistics: {str(e)}")
        
        st.markdown("---")
        st.markdown("#### 💡 Tips")
        st.info("""
        **Time Series Analysis:**
        - Look for trends and patterns
        - Check for seasonality
        - Use moving averages to smooth data
        - Consider different aggregation periods
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)