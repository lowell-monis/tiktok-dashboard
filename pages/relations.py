from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash

data = pd.read_csv('data/tiktok_dataset.csv')

def clean_dropdown_options(series):
    return [{'label': str(s), 'value': s} for s in series.unique() if pd.notna(s)]

allowed_metrics = [
    'video_duration_sec',
    'video_view_count', 
    'video_like_count', 
    'video_share_count',
    'video_download_count', 
    'video_comment_count'
]

numeric_options = [{'label': col.replace('_', ' ').title(), 'value': col} 
                  for col in allowed_metrics if col in data.columns]

dash.register_page(__name__, path='/relations', name="Correlations")

tiktok_pink = '#FF0050'
tiktok_aqua = '#00F2EA'
tiktok_black = '#000000'
tiktok_dark = '#111111'
tiktok_white = '#FFFFFF'

dropdown_style = {
    'color': 'white',
    'backgroundColor': tiktok_black,
    'borderColor': tiktok_pink
}

hover_style = {
    'max-width': '300px',
    'white-space': 'pre-wrap',
    'overflow': 'hidden',
    'text-overflow': 'ellipsis',
    'font-family': 'Arial',
    'font-size': '12px',
    'background-color': tiktok_black,
    'color': tiktok_white,
    'border': f'1px solid {tiktok_pink}',
    'padding': '5px'
}

layout = html.Div([
    html.H1("How are various engagement metrics correlated?", className="text-center"),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("Plot Controls", className="filter-header"),
                
                html.Label("Select X-Axis:"),
                dcc.Dropdown(
                    id='x-axis-selector',
                    options=numeric_options,
                    value='video_view_count' if 'video_view_count' in data.columns else allowed_metrics[0],
                    className='axis-dropdown mb-3',
                    style=dropdown_style,
                ),
                
                html.Label("Select Y-Axis:"),
                dcc.Dropdown(
                    id='y-axis-selector',
                    options=numeric_options,
                    value='video_like_count' if 'video_like_count' in data.columns else allowed_metrics[1],
                    className='axis-dropdown mb-3',
                    style=dropdown_style,
                ),
                
                html.Label("Color By:"),
                dcc.Dropdown(
                    id='color-selector',
                    options=[
                        {'label': 'None', 'value': 'none'},
                        {'label': 'Content Classification', 'value': 'claim_status'},
                        {'label': 'Verification Status', 'value': 'verified_status'},
                        {'label': 'Ban Status', 'value': 'author_ban_status'},
                    ],
                    value='none',
                    className='color-dropdown mb-4',
                    style=dropdown_style,
                ),
                
                html.Hr(className="filter-divider"),
                
                html.H3("Data Filters", className="filter-header"),
                
                dbc.Row([
                    dbc.Col([
                        html.Label("Content Classification:"),
                        dcc.Dropdown(
                            id='claim-filter',
                            options=clean_dropdown_options(data['claim_status']),
                            value=[],
                            multi=True,
                            className='multi-dropdown mb-4',
                            style=dropdown_style,
                        ),
                    ], width=6),
                    
                    dbc.Col([
                        html.Label("Verification Status:"),
                        dcc.Dropdown(
                            id='verified-filter',
                            options=clean_dropdown_options(data['verified_status']),
                            value=[],
                            multi=True,
                            className='multi-dropdown mb-4',
                            style=dropdown_style,
                        ),
                    ], width=6),
                ], justify="center", className="mb-4"),
                
                dbc.Row([
                    dbc.Col([
                        html.Label("Ban Status:"),
                        dcc.Dropdown(
                            id='ban-filter',
                            options=clean_dropdown_options(data['author_ban_status']),
                            value=[],
                            multi=True,
                            className='multi-dropdown mb-4',
                            style=dropdown_style,
                        ),
                    ], width=6),
                ], justify="center", className="mb-4"),
                
                dbc.Row([
                    dbc.Col([
                        html.Label("Video Duration (seconds):"),
                        dcc.RangeSlider(
                            id='duration-slider',
                            min=data['video_duration_sec'].min(),
                            max=data['video_duration_sec'].max(),
                            step=1,
                            value=[data['video_duration_sec'].min(), data['video_duration_sec'].max()],
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                            className='tiktok-slider'
                        ),
                    ], width=12),
                ], justify="center", className="mb-4"),
                
                dbc.Row([
                    dbc.Col([
                        html.Label("Video Views:"),
                        dcc.RangeSlider(
                            id='views-slider',
                            min=data['video_view_count'].min(),
                            max=data['video_view_count'].max(),
                            step=1000,
                            value=[data['video_view_count'].min(), data['video_view_count'].max()],
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                            className='tiktok-slider'
                        ),
                    ], width=12),
                ], justify="center", className="mb-4"),
                
                dbc.Row([
                    dbc.Col([
                        html.Label("Video Likes:"),
                        dcc.RangeSlider(
                            id='likes-slider',
                            min=data['video_like_count'].min(),
                            max=data['video_like_count'].max(),
                            step=1000,
                            value=[data['video_like_count'].min(), data['video_like_count'].max()],
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True},
                            className='tiktok-slider'
                        ),
                    ], width=12),
                ], justify="center", className="mb-4"),
                
                dbc.Row([
                    dbc.Col([
                        html.Button(
                            'Update Plot', 
                            id='update-plot-btn', 
                            className='dash-button glitch-button generate-button'
                        )
                    ], width=12, className="text-center")
                ], justify="center", className="mb-4"),
                
            ], className="filter-container", style={'width': '100%'})
        ], width=6), 
        
        dbc.Col([
            html.Div([
                dcc.Graph(
                    id='point-plot',
                    config={'displayModeBar': True, 'scrollZoom': True},
                    className='point-plot-graph'
                ),
                html.Div([
                    html.H3("Data Insights", className="text-info-header"),
                    html.Div(id='data-summary', className="text-info-content")
                ], className="text-info-box plot-insights-box")
            ], className="plot-container")
        ], width=6) 
    ]),
], className="main-container")

@callback(
    [Output('point-plot', 'figure'),
     Output('data-summary', 'children')],
    [Input('update-plot-btn', 'n_clicks'),
     Input('duration-slider', 'value'),
     Input('views-slider', 'value'),
     Input('likes-slider', 'value')],
    [State('x-axis-selector', 'value'),
     State('y-axis-selector', 'value'),
     State('color-selector', 'value'),
     State('claim-filter', 'value'),
     State('verified-filter', 'value'),
     State('ban-filter', 'value')]
)
def update_plot(n_clicks, duration_range, views_range, likes_range, 
                x_axis, y_axis, color_by, claim_status, verified_status, ban_status):
    try:
        filtered_df = data.copy()
        
        if claim_status and len(claim_status) > 0:
            filtered_df = filtered_df[filtered_df['claim_status'].isin(claim_status)]
        if verified_status and len(verified_status) > 0:
            filtered_df = filtered_df[filtered_df['verified_status'].isin(verified_status)]
        if ban_status and len(ban_status) > 0:
            filtered_df = filtered_df[filtered_df['author_ban_status'].isin(ban_status)]
        
        filtered_df = filtered_df[
            (filtered_df['video_duration_sec'] >= duration_range[0]) & 
            (filtered_df['video_duration_sec'] <= duration_range[1]) &
            (filtered_df['video_view_count'] >= views_range[0]) & 
            (filtered_df['video_view_count'] <= views_range[1]) &
            (filtered_df['video_like_count'] >= likes_range[0]) & 
            (filtered_df['video_like_count'] <= likes_range[1])
        ]
        
        if x_axis not in filtered_df.columns or y_axis not in filtered_df.columns:
            raise ValueError("Selected axis columns not found in data")
            
        filtered_df = filtered_df.dropna(subset=[x_axis, y_axis])
        
        if filtered_df.empty:
            empty_fig = go.Figure()
            empty_fig.update_layout(
                title="No data available for selected filters",
                plot_bgcolor=tiktok_black,
                paper_bgcolor=tiktok_black,
                font=dict(color=tiktok_white)
            )
            return empty_fig, "No data available for the selected filters"
        
        if color_by != 'none':
            fig = px.scatter(
                filtered_df, 
                x=x_axis, 
                y=y_axis, 
                color=color_by,
                hover_data={
                    'video_transcription_text': True,
                    x_axis: False,
                    y_axis: False,
                    color_by: False
                }
            )
            
            color_title_map = {
                'claim_status': 'Content Classification',
                'verified_status': 'Verification Status',
                'author_ban_status': 'Ban Status'
            }
            fig.update_layout(legend_title_text=color_title_map.get(color_by, ''))
        else:
            fig = px.scatter(
                filtered_df, 
                x=x_axis, 
                y=y_axis,
                hover_data={
                    'video_transcription_text': True,
                    x_axis: False,
                    y_axis: False
                }
            )
            fig.update_traces(marker=dict(color=tiktok_pink))

        fig.update_traces(
            hovertemplate=(
                '<span style="font-family: Arial; font-size: 12px; color: white; '
                'background-color: #111111; padding: 5px; border: 1px solid #FF0050; '
                'border-radius: 3px; max-width: 300px; white-space: pre-wrap; '
                'display: inline-block;">%{customdata[0]}</span><extra></extra>'
            ),
            customdata=filtered_df[['video_transcription_text']].values
        )

        fig.update_layout(
            hoverlabel=dict(
                bgcolor=tiktok_black,
                font_size=12,
                font_family="Arial",
                align="left"
            )
        )
        
        x_title = x_axis.replace('_', ' ').title()
        y_title = y_axis.replace('_', ' ').title()
        
        fig.update_layout(
            plot_bgcolor=tiktok_black,
            paper_bgcolor=tiktok_black,
            font=dict(color=tiktok_white),
            xaxis_title=x_title,
            yaxis_title=y_title,
            hoverlabel=dict(
                bgcolor=tiktok_black,
                font_size=14,
                font_family="Arial"
            )
        )
        
        try:
            corr = filtered_df[x_axis].corr(filtered_df[y_axis])*100
            corr_text = f"Correlation: {corr:.3f}%"
        except:
            corr_text = "Correlation: Could not calculate"
        
        summary = [
            html.P(f"Total points: {len(filtered_df)}"),
            html.P(f"X-Axis: {filtered_df[x_axis].min():.2f} to {filtered_df[x_axis].max():.2f}"),
            html.P(f"Y-Axis: {filtered_df[y_axis].min():.2f} to {filtered_df[y_axis].max():.2f}"),
            html.P(corr_text)
        ]
        
        return fig, summary
        
    except Exception as e:
        error_fig = go.Figure()
        error_fig.update_layout(
            title=f"Error: {str(e)}",
            plot_bgcolor=tiktok_black,
            paper_bgcolor=tiktok_black,
            font=dict(color=tiktok_white)
        )
        return error_fig, f"Error occurred: {str(e)}"