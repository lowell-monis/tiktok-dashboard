from dash import dcc, html
import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde
import dash
import pandas as pd

dash.register_page(__name__, name="Duration Dynamics", path="/duration-density")
df = pd.read_csv('data/tiktok_dataset.csv')
df = df[df['video_duration_sec'].notna() & df['claim_status'].isin(['claim', 'opinion'])]

colors = {'claim': '#FF0050', 'opinion': '#00F2EA'}

fig_kde = go.Figure()

for label in ['claim', 'opinion']:
    subset = df[df['claim_status'] == label]['video_duration_sec']
    kde = gaussian_kde(subset, bw_method=0.3)
    x_vals = np.linspace(subset.min(), subset.max(), 500)
    y_vals = kde(x_vals)

    fig_kde.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='lines',
        name=label.capitalize(),
        line=dict(color=colors[label], width=3),
        fill='tozeroy',
        hovertemplate=f"{label.capitalize()}<br>Duration: %{{x:.1f}} sec<br>Density: %{{y:.4f}}<extra></extra>"
    ))

    median_val = subset.median()

    fig_kde.add_vline(
        x=median_val,
        line=dict(color=colors[label], width=2, dash='dash'),
        annotation_text=f"{label.capitalize()} Median: {median_val:.1f}s",
        annotation_position="top right" if label == 'claim' else "top left",
        annotation_font=dict(color='white', family="Garamond", size=13),
        annotation=dict(
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor=colors[label],
            borderwidth=1,
            borderpad=4,
            showarrow=False
        ),
        opacity=0.8
)

fig_kde.update_layout(
    font=dict(
        family="Garamond",
        color="white"
    ),
    autosize=False,
    height=600,
    xaxis_title="Video Duration (seconds)",
    yaxis_title="Density",
    template="plotly_dark",
    plot_bgcolor='black',
    paper_bgcolor='black'
)


layout = html.Div(className='main-container', children=[
    html.H1("Claim videos are just as short, if not shorter, than opinion videos — and that’s what makes them dangerous.", style={'fontFamily': 'Garamond'}),

    html.Div(style={
        'display': 'flex',
        'flexDirection': 'row',
        'gap': '20px',
        'alignItems': 'flex-start',
        'flexWrap': 'wrap'
    }, children=[

        html.Div(className='text-info-box', style={
            'flex': '1 1 300px',
            'minWidth': '300px',
            'maxWidth': '500px',
            'height': '650px'
        }, children=[
            html.Div(className='text-info-header', children="Why It Matters"),
            html.Div(className='text-info-content', children=[
                html.P("TikTok’s short-form format isn't just about entertainment — it compresses complex narratives into a matter of seconds."),
                html.P("As this density plot shows, there is virtually no difference in video length between content flagged as claims and that categorized as opinions."),
                html.P("In fact, some of the most potentially misleading content may be even shorter."),
                html.P("Because shorter content leaves less room for nuance, context, or rebuttal. Claims — especially false or unverifiable ones — thrive when viewers have no time to think critically."),
                html.P("With the average video duration clustering under a minute, TikTok makes it easy to absorb, believe, and move on."),
                html.P("This isn’t just a format choice. It’s a design that accelerates misinformation — at the speed of a swipe.")
            ])
        ]),

        html.Div(style={'flex': '2 1 800px'}, children=[
            dcc.Graph(
                figure=fig_kde,
                style={'height': '600px'},
                className='point-plot-graph',
                config={'displayModeBar': True},
            )
        ])
    ])
])
