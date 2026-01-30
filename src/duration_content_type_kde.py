import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

# 1. Load and Clean Data
df = pd.read_csv('data/tiktok_dataset.csv')
# Filtering for non-null durations and specific statuses
df = df[df['video_duration_sec'].notna() & df['claim_status'].isin(['claim', 'opinion'])]

# 2. Configuration
colors = {'claim': '#FF0050', 'opinion': '#00F2EA'}
fig_kde = go.Figure()

# 3. Kernel Density Estimation (KDE) Calculation
for label in ['claim', 'opinion']:
    subset = df[df['claim_status'] == label]['video_duration_sec']
    
    # Calculate the density curve
    kde = gaussian_kde(subset, bw_method=0.3)
    x_vals = np.linspace(subset.min(), subset.max(), 500)
    y_vals = kde(x_vals)

    # Add the density trace
    fig_kde.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='lines',
        name=label.capitalize(),
        line=dict(color=colors[label], width=3),
        fill='tozeroy',
        hovertemplate=f"{label.capitalize()}<br>Duration: %{{x:.1f}} sec<br>Density: %{{y:.4f}}<extra></extra>"
    ))

    # Add Median Vertical Line
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

# 4. Styling & Layout
fig_kde.update_layout(
    title=dict(
        text="Duration Dynamics: Claims vs. Opinions",
        x=0.5,
        font=dict(size=24)
    ),
    font=dict(
        family="Garamond",
        color="white"
    ),
    xaxis_title="Video Duration (seconds)",
    yaxis_title="Density",
    template="plotly_dark",
    plot_bgcolor='black',
    paper_bgcolor='black',
    height=720,
    margin=dict(t=100, b=50, l=50, r=50)
)

# 5. Export to HTML
fig_kde.write_html("results/duration_dynamics.html")
print("KDE Visualization saved as 'duration_dynamics.html'")