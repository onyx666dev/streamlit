# ============================================
# FILE: pages/visualizations.py (FIXED - Colorscale Error)
# ============================================
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render(df):
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    
    st.markdown("### 🎨 Advanced Visualization Studio")
    
    # Enhanced controls
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
    
    with col1:
        x_axis = st.selectbox("📊 X-Axis", options=['None'] + df.columns.tolist())
    with col2:
        y_axis = st.selectbox("📈 Y-Axis", options=['None'] + df.columns.tolist())
    with col3:
        chart_type = st.selectbox("📉 Chart Type", 
                                 options=['Scatter', 'Line', 'Bar', 'Box', 'Histogram', 
                                         'Violin', 'Heatmap', 'Pie', 'Area', 'Funnel', 
                                         'Treemap', 'Sunburst', '3D Scatter'])
    with col4:
        color_by = st.selectbox("🎨 Color By", options=['None'] + df.columns.tolist())
    with col5:
        size_by = st.selectbox("📏 Size By", options=['None'] + df.select_dtypes(include=['number']).columns.tolist())
    
    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            color_scheme = st.selectbox("Color Scheme", 
                                       options=['Plotly', 'Viridis', 'Cividis', 'Blues', 
                                               'Reds', 'Greens', 'Purples', 'Rainbow'])
        with col2:
            chart_height = st.slider("Chart Height", 400, 800, 550)
        with col3:
            show_grid = st.checkbox("Show Grid", value=True)
        with col4:
            show_legend = st.checkbox("Show Legend", value=True)
    
    st.markdown("---")
    
    try:
        # Separate color maps for discrete and continuous scales
        discrete_color_map = {
            'Plotly': px.colors.qualitative.Plotly,
            'Viridis': px.colors.sequential.Viridis,
            'Cividis': px.colors.sequential.Cividis,
            'Blues': px.colors.sequential.Blues,
            'Reds': px.colors.sequential.Reds,
            'Greens': px.colors.sequential.Greens,
            'Purples': px.colors.sequential.Purples,
            'Rainbow': px.colors.sequential.Rainbow
        }
        
        # For continuous colorscales (heatmaps, etc.)
        continuous_colorscale_map = {
            'Plotly': 'Viridis',
            'Viridis': 'Viridis',
            'Cividis': 'Cividis',
            'Blues': 'Blues',
            'Reds': 'Reds',
            'Greens': 'Greens',
            'Purples': 'Purples',
            'Rainbow': 'Rainbow'
        }
        
        # Handle color and size parameters
        color_param = None if color_by == 'None' else color_by
        size_param = None if size_by == 'None' else size_by
        
        # Create visualizations
        if chart_type == 'Scatter':
            if x_axis != 'None' and y_axis != 'None':
                fig = px.scatter(df, x=x_axis, y=y_axis, 
                               color=color_param,
                               size=size_param,
                               title=f'{y_axis} vs {x_axis}',
                               color_discrete_sequence=discrete_color_map[color_scheme])
            else:
                st.warning("Please select both X and Y axis for scatter plot")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Line':
            if x_axis != 'None' and y_axis != 'None':
                fig = px.line(df, x=x_axis, y=y_axis, 
                             color=color_param,
                             title=f'{y_axis} vs {x_axis}',
                             color_discrete_sequence=discrete_color_map[color_scheme])
            else:
                st.warning("Please select both X and Y axis for line chart")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Bar':
            if x_axis != 'None' and y_axis != 'None':
                fig = px.bar(df, x=x_axis, y=y_axis, 
                            color=color_param,
                            title=f'{y_axis} by {x_axis}',
                            color_discrete_sequence=discrete_color_map[color_scheme])
            else:
                st.warning("Please select both X and Y axis for bar chart")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Box':
            if y_axis != 'None':
                fig = px.box(df, x=x_axis if x_axis != 'None' else None, 
                            y=y_axis, 
                            color=color_param,
                            title=f'{y_axis} Distribution',
                            color_discrete_sequence=discrete_color_map[color_scheme])
            else:
                st.warning("Please select Y axis for box plot")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Histogram':
            if x_axis != 'None':
                fig = px.histogram(df, x=x_axis,
                                 color=color_param,
                                 title=f'Distribution of {x_axis}',
                                 color_discrete_sequence=discrete_color_map[color_scheme])
            else:
                st.warning("Please select X axis for histogram")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Violin':
            if y_axis != 'None':
                fig = px.violin(df, x=x_axis if x_axis != 'None' else None,
                               y=y_axis,
                               color=color_param,
                               title=f'{y_axis} Distribution',
                               color_discrete_sequence=discrete_color_map[color_scheme])
            else:
                st.warning("Please select Y axis for violin plot")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Heatmap':
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if len(numeric_cols) >= 2:
                corr_matrix = df[numeric_cols].corr()
                fig = px.imshow(corr_matrix, 
                              text_auto='.2f',
                              aspect='auto',
                              color_continuous_scale=continuous_colorscale_map[color_scheme],  # Use continuous
                              title='Correlation Heatmap',
                              zmin=-1, zmax=1)
            else:
                st.warning("Need at least 2 numeric columns for heatmap")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Pie':
            if x_axis != 'None':
                value_counts = df[x_axis].value_counts().head(10)
                fig = px.pie(values=value_counts.values,
                           names=value_counts.index,
                           title=f'{x_axis} Distribution',
                           color_discrete_sequence=discrete_color_map[color_scheme])
            else:
                st.warning("Please select a column for pie chart")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Area':
            if x_axis != 'None' and y_axis != 'None':
                fig = px.area(df, x=x_axis, y=y_axis,
                            color=color_param,
                            title=f'{y_axis} vs {x_axis}',
                            color_discrete_sequence=discrete_color_map[color_scheme])
            else:
                st.warning("Please select both X and Y axis for area chart")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Funnel':
            if x_axis != 'None' and y_axis != 'None':
                fig = px.funnel(df, x=x_axis, y=y_axis,
                              title=f'Funnel Chart: {y_axis} by {x_axis}',
                              color_discrete_sequence=discrete_color_map[color_scheme])
            else:
                st.warning("Please select both X and Y axis for funnel chart")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Treemap':
            if x_axis != 'None' and y_axis != 'None':
                # Check if y_axis is numeric
                if df[y_axis].dtype in ['int64', 'float64']:
                    fig = px.treemap(df, path=[x_axis], values=y_axis,
                                   title=f'Treemap: {y_axis} by {x_axis}',
                                   color_discrete_sequence=discrete_color_map[color_scheme])
                else:
                    st.warning(f"{y_axis} must be numeric for treemap")
                    st.markdown('</div>', unsafe_allow_html=True)
                    return
            else:
                st.warning("Please select both X and Y axis for treemap")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == 'Sunburst':
            if x_axis != 'None' and y_axis != 'None':
                # Check if y_axis is numeric
                if df[y_axis].dtype in ['int64', 'float64']:
                    fig = px.sunburst(df, path=[x_axis], values=y_axis,
                                    title=f'Sunburst: {y_axis} by {x_axis}',
                                    color_discrete_sequence=discrete_color_map[color_scheme])
                else:
                    st.warning(f"{y_axis} must be numeric for sunburst")
                    st.markdown('</div>', unsafe_allow_html=True)
                    return
            else:
                st.warning("Please select both X and Y axis for sunburst")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        elif chart_type == '3D Scatter':
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if len(numeric_cols) >= 3:
                z_axis = st.selectbox("📊 Z-Axis", options=numeric_cols)
                if x_axis != 'None' and y_axis != 'None':
                    fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis,
                                      color=color_param,
                                      size=size_param,
                                      title=f'3D Scatter: {x_axis}, {y_axis}, {z_axis}',
                                      color_discrete_sequence=discrete_color_map[color_scheme])
                else:
                    st.warning("Please select X, Y, and Z axes for 3D scatter")
                    st.markdown('</div>', unsafe_allow_html=True)
                    return
            else:
                st.warning("Need at least 3 numeric columns for 3D scatter")
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        # Update layout
        fig.update_layout(
            template='plotly_white',
            height=chart_height,
            font=dict(size=12),
            title_font_size=20,
            plot_bgcolor='rgba(0,0,0,0)' if not show_grid else 'white',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=show_legend,
            xaxis=dict(showgrid=show_grid) if chart_type != 'Heatmap' else {},
            yaxis=dict(showgrid=show_grid) if chart_type != 'Heatmap' else {}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Chart info
        with st.expander("📊 Chart Information"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**X-Axis:**", x_axis if x_axis != 'None' else "Not set")
            with col2:
                st.write("**Y-Axis:**", y_axis if y_axis != 'None' else "Not set")
            with col3:
                st.write("**Chart Type:**", chart_type)
        
    except Exception as e:
        st.error(f"❌ Error creating visualization: {str(e)}")
        st.info("💡 Try selecting different columns or chart types that are compatible with your data.")
        
        # Debug info
        with st.expander("🐛 Debug Information"):
            st.code(f"Error: {str(e)}")
            st.write("Selected X:", x_axis)
            st.write("Selected Y:", y_axis)
            st.write("Chart Type:", chart_type)
    
    # Quick chart suggestions
    st.markdown("---")
    st.markdown("### 💡 Quick Chart Suggestions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    suggestions = []
    
    if len(numeric_cols) >= 2:
        suggestions.append(("Correlation Heatmap", "Show relationships between all numeric variables"))
    if len(numeric_cols) >= 1:
        suggestions.append(("Distribution Plot", "Visualize the distribution of numeric data"))
    if len(categorical_cols) >= 1:
        suggestions.append(("Category Analysis", "Analyze categorical variable frequencies"))
    if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
        suggestions.append(("Group Comparison", "Compare numeric values across categories"))
    
    for i, (title, desc) in enumerate(suggestions):
        with [col1, col2, col3, col4][i % 4]:
            st.markdown(f"""
                <div class="info-box" style="min-height: 120px;">
                    <div style="font-weight: 600; margin-bottom: 0.5rem;">{title}</div>
                    <div style="font-size: 0.85rem; color: #666;">{desc}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)