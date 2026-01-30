from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, 
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
                ],
                use_pages=True)

app.layout = html.Div(style={'backgroundColor': 'black', 'minHeight': '100vh'}, children=[
    html.Div(style={
        'backgroundColor': '#111',
        'padding': '20px',
        'borderBottom': '1px solid #333',
        'boxShadow': '0 2px 5px rgba(0,0,0,0.3)'
    }, children=[
        html.H1(
    [
        "the verification ",
        html.Span(
            "void",
            style={
                'color': 'white',
                'textShadow': '2px 2px 0 #ff0050, 4px 4px 0 #00f2ea, 6px 6px 0 #000000',
                'display': 'inline-block',
                'animation': 'glitch-effect 2.5s infinite' 
            }
        ),
        "?"
    ],
            style={
                'color': 'white',
                'fontFamily': '"Garamond", sans-serif',
                'marginBottom': '5px',
                'textAlign': 'center',
                'fontSize': '3rem',
                'fontWeight': 'bold',
                'position': 'relative',
                'zIndex': '1',
                'padding': '10px 10px 0 10px'
            }
        ),
        
        html.H2(
            [
                "can ",
                html.Span(
                    "TikTok",
                    style={
                        'textShadow': '1px 1px 0 #ff0050, 2px 2px 0 #00f2ea, 3px 3px 0 #000000',
                        'display': 'inline-block'
                    }
                ),
                " hold the leash on mis/disinformation?"
            ],
            style={
                'color': 'white',
                'fontFamily': '"Garamond", sans-serif',
                'textAlign': 'center',
                'fontSize': '1.5rem',
                'marginTop': '0px',
                'marginBottom': '20px',
                'padding': '0 10px 10px 10px'
            }
        ),
        
        html.Div(style={
    'display': 'flex',
    'justifyContent': 'center',
    'flexWrap': 'wrap',
    'gap': '10px'
}, children=[
    dcc.Link(
        html.Button(
            page['name'],
            id=f'btn-{page["name"].lower().replace(" ", "-")}',
            className='dash-button',
            n_clicks=0
        ),
        href=page['relative_path'],
        style={'textDecoration': 'none'}
    )
    for page in sorted(
        dash.page_registry.values(),
        key=lambda p: (p['name'] in ['About', 'References'], p['name'])
    )
])

    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)