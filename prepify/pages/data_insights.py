# ============================================
# FILE: pages/data_insights.py
# ============================================
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render(df):
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Column Information")
        dtype_df = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.astype(str).values,
            'Non-Null': df.count().values,
            'Null': df.isnull().sum().values,
            'Unique': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(dtype_df, use_container_width=True, height=400)
    
    with col2:
        st.markdown("### ⚠️ Missing Values Analysis")
        missing_df = pd.DataFrame({
            'Column': df.columns,
            'Missing': df.isnull().sum().values,
            'Percentage': (df.isnull().sum().values / len(df) * 100).round(2)
        })
        missing_df = missing_df[missing_df['Missing'] > 0].sort_values('Missing', ascending=False)
        
        if len(missing_df) > 0:
            st.dataframe(missing_df, use_container_width=True)
            
            fig = go.Figure(data=[
                go.Bar(x=missing_df['Column'], y=missing_df['Percentage'],
                      marker=dict(color=missing_df['Percentage'],
                                colorscale='Reds',
                                showscale=True))
            ])
            fig.update_layout(
                title='Missing Values %',
                template='plotly_white',
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✓ No missing values detected!")
    
    st.markdown('</div>', unsafe_allow_html=True)