from dash import dcc, html
import dash

dash.register_page(__name__, path='/references', name="References and More Info")

layout = html.Div(
    className="main-container",
    style={
        'backgroundColor': 'black',
        'padding': '40px',
        'minHeight': '100vh',
        'color': 'white',
        'fontFamily': 'Garamond, serif'
    },
    children=[
        html.H1(
            "About & References",
            style={
                'textAlign': 'center',
                'fontSize': '3rem',
                'marginBottom': '40px',
                'textShadow': '2px 2px 0 #ff0050, 4px 4px 0 #00f2ea'
            }
        ),

        html.Div(className='text-info-box', style={'fontSize': '1.15rem', 'lineHeight': '1.8'}, children=[
            html.Div(className='text-info-header', children="About This Project"),
            html.Div(className='text-info-content', children=[
                html.P("This dashboard was developed as part of the CMSE 402 course at Michigan State University to explore the structural pathways of misinformation propagation on TikTok using Python, Dash, and Plotly."),
                html.P("The goal of this project is to help users — especially those in positions of influence — understand how short-form content on platforms like TikTok can distort attention and, ultimately, truth."),
                html.P("This interactive dashboard allows exploration of metadata surrounding flagged content, creator verification, video duration, and moderation outcomes such as bans and under-review statuses."),
                ]),
            html.Div(style={'marginTop': '20px'}, children=[
                html.P("Created by Lowell Monis", style={'marginBottom': '5px'}),
                html.A("GitHub Profile", href="https://github.com/lowell-monis", target="_blank",
                       style={'color': '#FF0050', 'textDecoration': 'none', 'marginRight': '20px'}),
                html.A("CMSE 402 Spring 2025", href="https://msu-cmse-courses.github.io/cmse402-S25-student/", target="_blank",
                       style={'color': '#00F2EA', 'textDecoration': 'none'})
            ])
        ]),

        html.Div(className='text-info-box', children=[
            html.Div(className='text-info-header', children="References & Sources"),
            html.Div(className='text-info-content', children=[
                html.H5("Content", style={'marginTop': '20px'}),
                html.Ul([
                    html.Li(html.A("Deceptive Trends: The Societal Impact of Disinformation on TikTok (Australian Outlook)", href="https://www.internationalaffairs.org.au/australianoutlook/deceptive-trends-the-societal-impact-of-disinformation-on-tiktok/", target="_blank")),
                    html.Li(html.A("TikTok users being fed misleading election news (BBC)", href="https://www.bbc.com/news/articles/c1ww6vz1l81o", target="_blank"))
                ]),

                html.H5("Media, Visual & Stock Sources", style={'marginTop': '20px'}),
                html.Ul([
                    html.Li(html.A("Intro video clip: Samantha Bee - YouTube Clip", href="https://www.youtube.com/watch?v=UhrxV7AaLAc", target="_blank")),
                    html.Li(html.A("How conspiracy theories spread online", href="https://theconversation.com/how-conspiracy-theories-spread-online-its-not-just-down-to-algorithms-133891", target="_blank")),
                    html.Li(html.A("YouTube’s misinformation problem (NYTimes)", href="https://www.nytimes.com/2022/11/05/technology/youtube-misinformation.html", target="_blank"))
                ]),

                html.H5("Dataset"),
                html.Ul([
                    html.Li(html.A("TikTok Moderation Dataset on Kaggle", href="https://www.kaggle.com/datasets/raminhuseyn/dataset-from-tiktok/data", target="_blank"))
                ]),

                html.H5("TikTok Policy & Brand Guidelines"),
                html.Ul([
                    html.Li(html.A("TikTok Developer Design Guidelines", href="https://developers.tiktok.com/doc/getting-started-design-guidelines?enter_method=left_navigation", target="_blank"))
                ]),

                html.H5("Design Inspiration", style={'marginTop': '20px'}),
                html.Ul([
                    html.Li("TikTok's Brand Palette and Typography"),
                    html.Li("Glitch Art Aesthetics as a metaphor for distortion of truth"),
                    html.Li("TikTok's original glitch style animation"),
                    html.Li("Interactive and Ethical Data Visualization Principles")
                ])
            ])
        ]),
    ]
)
