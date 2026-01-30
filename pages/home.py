from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import dash

dash.register_page(__name__, path='/', name="Home")

tiktok_clean = pd.read_csv('data/tiktok_dataset.csv')

def create_sankey_figure(df):
    if df.empty:
        return go.Figure()

    source, target, value, colors, node_labels = [], [], [], [], []
    categories = ['claim_status', 'verified_status', 'author_ban_status']

    tiktok_colors = {
        'pink': '#FF0050',
        'aqua': '#00F2EA',
        'black': '#000000',
        'gray': '#333333',
        'white': '#FFFFFF',
        'magenta': '#de8c9d',
        'blue': '#397684'
    }

    flow_colors = {
        'claim': tiktok_colors['magenta'],
        'opinion': tiktok_colors['blue'],
        'not verified': tiktok_colors['pink'],
        'verified': tiktok_colors['aqua']
    }

    node_map = {}
    index = 0
    for col in categories:
        for label in df[col].unique():
            node_map[(col, label)] = index
            label_clean = str(label).title() 
            node_labels.append(label_clean)
            index += 1

    for i in range(len(categories) - 1):
        col1, col2 = categories[i], categories[i + 1]
        flow_data = df.groupby([col1, col2]).size().reset_index(name='count')
        for _, row in flow_data.iterrows():
            source.append(node_map[(col1, row[col1])])
            target.append(node_map[(col2, row[col2])])
            value.append(row['count'])
            if col2 == 'author_ban_status':
                if row[col2] == 'under review':
                    colors.append('#FFA500') 
                elif row[col2] == 'banned':
                    colors.append('#8B0000') 
                else:
                    colors.append(flow_colors.get(row[col1], tiktok_colors['gray']))
            else:
                colors.append(flow_colors.get(row[col1], tiktok_colors['gray']))

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color=tiktok_colors['black'], width=0.8),
            label=node_labels,
            color=tiktok_colors['gray'],
            hovertemplate='%{label}<extra></extra>'
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=colors,
            hovertemplate='From %{source.label}<br>To %{target.label}<br>Count: %{value}<extra></extra>'
        )
    ))

    fig.update_layout(
        
        font_family='Garamond, serif',
        font_size=18,
        font_color=tiktok_colors['white'],
        paper_bgcolor=tiktok_colors['black'],
        plot_bgcolor=tiktok_colors['black'],
        height=720,
        margin=dict(l=30, r=30, b=30, t=30,
        autoexpand=False
    ),
        hoverlabel=dict(
            font_family='Garamond',
            bgcolor=tiktok_colors['black'],
            font_color=tiktok_colors['white']
        )
    )
    return fig

layout = html.Div(
    className='main-container',
    style={
        'display': 'flex',
        'flexDirection': 'row',
        'gap': '20px',
        'backgroundColor': '#000',
        'padding': '20px'
    },
    children=[
        html.Div(className='text-info-box', style={'flex': '1', 'minWidth': '350px', 'height': '750px'}, children=[
            html.Div(className='text-info-header', children="Understanding the Journey of Misinformation"),
            html.Div(className='text-info-content', children=[
                html.P("TikTok is not just a platform for trends and entertainment — it is now one of the most influential engines of information for a new generation."),
                html.P("In the age of instant video, claims spread quickly, gaining momentum before they can be challenged."),
                html.P("This Sankey diagram visualizes how content flows from claim or opinion, through the layer of verification, and ends with whether the author is ultimately banned."),
                html.P("With the rise of AI-generated misinformation and deepfakes, the integrity of public discourse is more vulnerable than ever. The design of TikTok — fast, visual, and emotionally driven — accelerates the journey from content creation to mass influence.")
            ])
        ]),

        html.Div(style={'flex': '2'}, children=[
            dcc.Graph(
                id='sankey-graph',
                figure=create_sankey_figure(tiktok_clean),
                style={
                    'height': '700px', 'width': '1000px', 'minWidth': '800px', 'maxWidth': '1000px'
                }
            )
        ])
    ]
)
