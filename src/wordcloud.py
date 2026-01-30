from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import dash
import numpy as np
from data import clean_dropdown_options, clean_dataset

df = clean_dataset()
dash.register_page(__name__, path='/wordcloud', name="Content Themes")

# color palette for py compatibility
tiktok_pink = '#FF0050'
tiktok_aqua = '#00F2EA'
tiktok_black = '#000000'
tiktok_dark = '#111111'
tiktok_white = '#FFFFFF'

# colormap generator for the wordcloud
def make_tiktok_colormap():
    from matplotlib.colors import LinearSegmentedColormap
    colors = [tiktok_pink, tiktok_aqua, '#FFFFFF']
    return LinearSegmentedColormap.from_list('tiktok', colors)

layout = html.Div([
    html.H1("What are the common themes in these videos?", className="text-center"),
    
    # dummy output
    html.Div(id='dummy-output', style={'display': 'none'}),
    html.Div(id='dummy-input', style={'display': 'none'}),
    
    # collapisble filters
    dbc.Collapse(
        html.Div([
            # discrete value filters
            dbc.Row([
                dbc.Col([
                    html.Label("Claim Status:"),
                    dcc.Dropdown(
                        id='claim-filter',
                        options=clean_dropdown_options(df['claim_status']),
                        value=[],
                        multi=True,
                        className='multi-dropdown mb-4'
                    ),
                ], width={"size": 3, "offset": 0}),
                
                dbc.Col([
                    html.Label("Verified Status:"),
                    dcc.Dropdown(
                        id='verified-filter',
                        options=clean_dropdown_options(df['verified_status']),
                        value=[],
                        multi=True,
                        className='multi-dropdown mb-4'
                    ),
                ], width={"size": 3, "offset": 0}),
                
                dbc.Col([
                    html.Label("Ban Status:"),
                    dcc.Dropdown(
                        id='ban-filter',
                        options=clean_dropdown_options(df['author_ban_status']),
                        value=[],
                        multi=True,
                        className='multi-dropdown mb-4'
                    ),
                ], width={"size": 3, "offset": 0}),
            ], justify="center", className="mb-4"),
            
            # numerical/continuous filters
            dbc.Row([
                dbc.Col([
                    html.Label("Video Duration (seconds):"),
                    dcc.RangeSlider(
                        id='duration-slider',
                        min=df['video_duration_sec'].min(),
                        max=df['video_duration_sec'].max(),
                        step=1,
                        value=[df['video_duration_sec'].min(), df['video_duration_sec'].max()],
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                        className='tiktok-slider'
                    ),
                ], width={"size": 3, "offset": 0}),
                
                dbc.Col([
                    html.Label("Video Views:"),
                    dcc.RangeSlider(
                        id='views-slider',
                        min=df['video_view_count'].min(),
                        max=df['video_view_count'].max(),
                        step=1000,
                        value=[df['video_view_count'].min(), df['video_view_count'].max()],
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                        className='tiktok-slider'
                    ),
                ], width={"size": 3, "offset": 0}),
                
                dbc.Col([
                    html.Label("Video Likes:"),
                    dcc.RangeSlider(
                        id='likes-slider',
                        min=df['video_like_count'].min(),
                        max=df['video_like_count'].max(),
                        step=1000,
                        value=[df['video_like_count'].min(), df['video_like_count'].max()],
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                        className='tiktok-slider'
                    ),
                ], width={"size": 3, "offset": 0}),
            ], justify="center", className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Label("Video Shares:"),
                    dcc.RangeSlider(
                        id='shares-slider',
                        min=df['video_share_count'].min(),
                        max=df['video_share_count'].max(),
                        step=100,
                        value=[df['video_share_count'].min(), df['video_share_count'].max()],
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                        className='tiktok-slider'
                    ),
                ], width={"size": 3, "offset": 0}),
                
                dbc.Col([
                    html.Label("Video Downloads:"),
                    dcc.RangeSlider(
                        id='downloads-slider',
                        min=df['video_download_count'].min(),
                        max=df['video_download_count'].max(),
                        step=100,
                        value=[df['video_download_count'].min(), df['video_download_count'].max()],
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                        className='tiktok-slider'
                    ),
                ], width={"size": 3, "offset": 0}),
                
                dbc.Col([
                    html.Label("Video Comments:"),
                    dcc.RangeSlider(
                        id='comments-slider',
                        min=df['video_comment_count'].min(),
                        max=df['video_comment_count'].max(),
                        step=100,
                        value=[df['video_comment_count'].min(), df['video_comment_count'].max()],
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                        className='tiktok-slider'
                    ),
                ], width={"size": 3, "offset": 0}),
            ], justify="center", className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Button('Generate Word Cloud', id='generate-btn', 
                            className='dash-button glitch-button generate-button')
                ], width={"size": 6, "offset": 3})
            ], justify="center", className="mb-4"),
            
        ], className="filter-container"),
        id="collapse-filters",
        is_open=True,
        className="collapsible"
    ),
    
    dbc.Row([
        dbc.Col([
            html.Button(
                html.I(className="fas fa-chevron-up"),
                id="collapse-button",
                className="dash-button arrow-button"
            ),
        ], width={"size": 2, "offset": 5})
    ], justify="center", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='wordcloud-container', className="wordcloud-container")
        ], width={"size": 10, "offset": 1})
    ], justify="center")
], className="main-container")

# toggle filters callback
@callback(
    Output("collapse-filters", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse-filters", "is_open")]
)
def toggle_filters(n, is_open):
    if n:
        return not is_open
    return is_open

# callback to update button icon based on collapse state
@callback(
    Output("collapse-button", "children"),
    [Input("collapse-filters", "is_open")]
)
def update_button_icon(is_open):
    if is_open:
        return html.I(className="fas fa-chevron-up")
    else:
        return html.I(className="fas fa-chevron-down")

# callback to generate word cloud
@callback(
    Output('wordcloud-container', 'children'),
    [Input('generate-btn', 'n_clicks')],
    [State('claim-filter', 'value'),
     State('verified-filter', 'value'),
     State('ban-filter', 'value'),
     State('duration-slider', 'value'),
     State('views-slider', 'value'),
     State('likes-slider', 'value'),
     State('shares-slider', 'value'),
     State('downloads-slider', 'value'),
     State('comments-slider', 'value')]
)
def update_wordcloud(n_clicks, claim_status, verified_status, ban_status, 
                     duration_range, views_range, likes_range, 
                     shares_range, downloads_range, comments_range):
    if n_clicks is None:
        return html.Div("Adjust filters and click 'Generate Word Cloud'", 
                       className="default-text")
    
    # filter dataframe
    filtered_df = df.copy()
    
    if claim_status and len(claim_status) > 0:
        filtered_df = filtered_df[filtered_df['claim_status'].isin(claim_status)]
    if verified_status and len(verified_status) > 0:
        filtered_df = filtered_df[filtered_df['verified_status'].isin(verified_status)]
    if ban_status and len(ban_status) > 0:
        filtered_df = filtered_df[filtered_df['author_ban_status'].isin(ban_status)]
    
    if duration_range:
        filtered_df = filtered_df[
            (filtered_df['video_duration_sec'] >= duration_range[0]) & 
            (filtered_df['video_duration_sec'] <= duration_range[1])]
    if views_range:
        filtered_df = filtered_df[
            (filtered_df['video_view_count'] >= views_range[0]) & 
            (filtered_df['video_view_count'] <= views_range[1])]
    if likes_range:
        filtered_df = filtered_df[
            (filtered_df['video_like_count'] >= likes_range[0]) & 
            (filtered_df['video_like_count'] <= likes_range[1])]
    if shares_range:
        filtered_df = filtered_df[
            (filtered_df['video_share_count'] >= shares_range[0]) & 
            (filtered_df['video_share_count'] <= shares_range[1])]
    if downloads_range:
        filtered_df = filtered_df[
            (filtered_df['video_download_count'] >= downloads_range[0]) & 
            (filtered_df['video_download_count'] <= downloads_range[1])]
    if comments_range:
        filtered_df = filtered_df[
            (filtered_df['video_comment_count'] >= comments_range[0]) & 
            (filtered_df['video_comment_count'] <= comments_range[1])]
    
    text = ' '.join(filtered_df['video_transcription_text'].dropna())
    
    if not text:
        return html.Div("No transcripts match these filters", className="default-text")
    
    try:
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color=tiktok_black,
            colormap=make_tiktok_colormap(),
            max_words=100,
            prefer_horizontal=0.9,
            relative_scaling=0.5
        ).generate(text)
    except:
        # if colormap fails, fallback to default colormap
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color=tiktok_black,
            colormap='viridis',
            max_words=100
        ).generate(text)
    
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    
    # buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, facecolor=tiktok_black)
    plt.close()
    buf.seek(0)
    
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return html.Img(
        src=f'data:imsage/png;base64,{img_str}', 
        className="wordcloud-image"
    )