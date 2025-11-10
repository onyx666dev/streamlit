# ============================================
# FILE: pages/advanced_analytics.py (FIXED VERSION)
# ============================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Import scipy.stats at the top level
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    st.warning("⚠️ scipy not installed. Some advanced features may be limited.")

def render(df):
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Statistical Summary Section
    if numeric_cols:
        st.markdown("### 📊 Statistical Summary Dashboard")
        
        # Enhanced statistics table
        stats_df = df[numeric_cols].describe().T
        stats_df['range'] = stats_df['max'] - stats_df['min']
        stats_df['cv'] = (stats_df['std'] / stats_df['mean'] * 100).round(2)  # Coefficient of variation
        
        # Color-code the statistics
        styled_stats = stats_df.style.background_gradient(cmap='RdYlGn', subset=['mean', 'std'])
        st.dataframe(styled_stats, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Distribution Analysis Grid
        st.markdown("### 📈 Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Select column for detailed analysis
            analysis_col = st.selectbox("Select column for detailed analysis", numeric_cols)
        
        with col2:
            if SCIPY_AVAILABLE:
                dist_type = st.selectbox("Distribution view", ["Histogram", "KDE", "Both"])
            else:
                dist_type = st.selectbox("Distribution view", ["Histogram"])
                st.info("Install scipy for KDE plots: pip install scipy")
        
        # Create distribution plots
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution plot
            fig = go.Figure()
            
            if dist_type in ["Histogram", "Both"]:
                fig.add_trace(go.Histogram(
                    x=df[analysis_col],
                    name='Histogram',
                    marker_color='rgb(102, 126, 234)',
                    opacity=0.7,
                    nbinsx=30
                ))
            
            if dist_type in ["KDE", "Both"] and SCIPY_AVAILABLE:
                try:
                    col_data = df[analysis_col].dropna()
                    if len(col_data) > 1:
                        kde_x = np.linspace(col_data.min(), col_data.max(), 100)
                        kde = stats.gaussian_kde(col_data)
                        kde_y = kde(kde_x)
                        
                        # Scale KDE to match histogram
                        if dist_type == "Both":
                            hist_vals, _ = np.histogram(col_data, bins=30)
                            scale_factor = hist_vals.max() / kde_y.max()
                            kde_y = kde_y * scale_factor
                        
                        fig.add_trace(go.Scatter(
                            x=kde_x,
                            y=kde_y,
                            name='KDE',
                            line=dict(color='red', width=2),
                            yaxis='y2' if dist_type == "Both" else 'y'
                        ))
                except Exception as e:
                    st.warning(f"Could not generate KDE plot: {str(e)}")
            
            fig.update_layout(
                title=f'Distribution of {analysis_col}',
                template='plotly_white',
                height=350,
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Q-Q Plot for normality (only if scipy available)
            if SCIPY_AVAILABLE:
                try:
                    fig = go.Figure()
                    
                    sorted_data = np.sort(df[analysis_col].dropna())
                    if len(sorted_data) > 0:
                        theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(sorted_data)))
                        
                        fig.add_trace(go.Scatter(
                            x=theoretical_quantiles,
                            y=sorted_data,
                            mode='markers',
                            name='Data',
                            marker=dict(color='rgb(72, 187, 120)', size=5)
                        ))
                        
                        # Add reference line
                        min_val, max_val = theoretical_quantiles.min(), theoretical_quantiles.max()
                        fig.add_trace(go.Scatter(
                            x=[min_val, max_val],
                            y=[sorted_data.min(), sorted_data.max()],
                            mode='lines',
                            name='Normal',
                            line=dict(color='red', dash='dash')
                        ))
                        
                        fig.update_layout(
                            title=f'Q-Q Plot - {analysis_col}',
                            xaxis_title='Theoretical Quantiles',
                            yaxis_title='Sample Quantiles',
                            template='plotly_white',
                            height=350,
                            showlegend=True
                        )
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating Q-Q plot: {str(e)}")
            else:
                # Alternative: Simple box plot
                fig = go.Figure()
                fig.add_trace(go.Box(
                    y=df[analysis_col],
                    name=analysis_col,
                    marker_color='rgb(102, 126, 234)'
                ))
                fig.update_layout(
                    title=f'Box Plot - {analysis_col}',
                    template='plotly_white',
                    height=350
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Correlation Analysis
        if len(numeric_cols) > 1:
            st.markdown("### 🔗 Correlation Analysis")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Correlation heatmap
                corr_matrix = df[numeric_cols].corr()
                
                fig = px.imshow(corr_matrix, 
                              text_auto='.2f',
                              aspect='auto',
                              color_continuous_scale='RdBu_r',
                              title='Feature Correlation Matrix',
                              zmin=-1, zmax=1)
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top correlations
                st.markdown("**🔝 Strongest Correlations:**")
                
                # Get top correlations (excluding diagonal)
                corr_pairs = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_pairs.append({
                            'Feature 1': corr_matrix.columns[i],
                            'Feature 2': corr_matrix.columns[j],
                            'Correlation': corr_matrix.iloc[i, j]
                        })
                
                if corr_pairs:
                    corr_df = pd.DataFrame(corr_pairs)
                    corr_df['Abs_Corr'] = corr_df['Correlation'].abs()
                    top_corr = corr_df.nlargest(min(10, len(corr_df)), 'Abs_Corr')[['Feature 1', 'Feature 2', 'Correlation']]
                    
                    st.dataframe(top_corr.style.background_gradient(cmap='RdYlGn', subset=['Correlation']),
                               use_container_width=True, hide_index=True)
                else:
                    st.info("No correlations to display")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Pairwise Scatter Plot Matrix
        if len(numeric_cols) >= 2:
            st.markdown("### 📊 Pairwise Relationships")
            
            selected_features = st.multiselect(
                "Select features to compare (max 4 recommended)",
                numeric_cols,
                default=numeric_cols[:min(3, len(numeric_cols))]
            )
            
            if selected_features and len(selected_features) >= 2:
                # Sample data if too large
                plot_df = df[selected_features].dropna()
                
                if len(plot_df) > 1000:
                    plot_df = plot_df.sample(n=1000, random_state=42)
                    st.info(f"📊 Showing sample of 1000 points for performance")
                
                if len(plot_df) > 0:
                    try:
                        fig = px.scatter_matrix(
                            plot_df,
                            dimensions=selected_features,
                            title="Pairwise Scatter Plot Matrix",
                            height=600
                        )
                        fig.update_traces(diagonal_visible=False, showupperhalf=False)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error creating scatter matrix: {str(e)}")
                else:
                    st.warning("No data available after removing missing values")
    
    # Categorical Analysis
    if categorical_cols:
        st.markdown("---")
        st.markdown("### 🏷️ Categorical Variable Analysis")
        
        selected_cat = st.selectbox("Select categorical variable", categorical_cols)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Frequency bar chart
            value_counts = df[selected_cat].value_counts().head(15)
            
            if len(value_counts) > 0:
                fig = px.bar(x=value_counts.index, y=value_counts.values,
                           title=f'Top 15 Categories - {selected_cat}',
                           labels={'x': selected_cat, 'y': 'Count'},
                           color=value_counts.values,
                           color_continuous_scale='Purples')
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data to display")
        
        with col2:
            # Pie chart
            if len(value_counts) > 0:
                fig = px.pie(values=value_counts.values, 
                           names=value_counts.index,
                           title=f'{selected_cat} Distribution',
                           color_discrete_sequence=px.colors.sequential.Purples,
                           hole=0.3)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Crosstab analysis if multiple categorical variables
        if len(categorical_cols) >= 2:
            st.markdown("#### 📊 Cross-Tabulation Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                cat1 = st.selectbox("First categorical variable", categorical_cols, key="cat1")
            with col2:
                cat2 = st.selectbox("Second categorical variable", categorical_cols, key="cat2")
            
            if cat1 != cat2:
                try:
                    # Create crosstab
                    crosstab = pd.crosstab(df[cat1], df[cat2])
                    
                    if not crosstab.empty:
                        # Heatmap of crosstab
                        fig = px.imshow(crosstab,
                                      labels=dict(x=cat2, y=cat1, color="Count"),
                                      title=f'Cross-tabulation: {cat1} vs {cat2}',
                                      color_continuous_scale='YlOrRd',
                                      text_auto=True)
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No data for cross-tabulation")
                except Exception as e:
                    st.error(f"Error creating cross-tabulation: {str(e)}")
    
    # Data Quality Report
    st.markdown("---")
    st.markdown("### 🎯 Data Quality Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Missing Data Analysis**")
        missing_data = df.isnull().sum()
        missing_pct = (missing_data / len(df) * 100).round(2)
        missing_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing': missing_data.values,
            'Percentage': missing_pct.values
        })
        missing_df = missing_df[missing_df['Missing'] > 0].sort_values('Missing', ascending=False)
        
        if len(missing_df) > 0:
            st.dataframe(missing_df, use_container_width=True, hide_index=True)
        else:
            st.success("✓ No missing values!")
    
    with col2:
        st.markdown("**Duplicate Analysis**")
        dup_count = df.duplicated().sum()
        st.metric("Duplicate Rows", dup_count)
        
        if dup_count > 0:
            dup_pct = (dup_count / len(df) * 100).round(2)
            st.warning(f"⚠️ {dup_pct}% of data is duplicated")
        else:
            st.success("✓ No duplicates found!")
    
    with col3:
        st.markdown("**Cardinality Analysis**")
        high_card_cols = [col for col in df.columns if df[col].nunique() > len(df) * 0.9]
        st.metric("High Cardinality Columns", len(high_card_cols))
        
        if high_card_cols:
            st.write("Columns:", ", ".join(high_card_cols[:3]))
            if len(high_card_cols) > 3:
                st.write(f"...and {len(high_card_cols) - 3} more")
    
    st.markdown('</div>', unsafe_allow_html=True)