import plotly.graph_objects as go
from data import clean_dataset

# 1. Load your data
tiktok_clean = clean_dataset()
df = tiktok_clean.copy()

# 2. Configuration & Colors
categories = ['claim_status', 'verified_status', 'author_ban_status']
tiktok_colors = {
    'pink': '#FF0050', 'aqua': '#00F2EA', 'black': '#000000',
    'gray': '#333333', 'white': '#FFFFFF', 'magenta': '#de8c9d', 'blue': '#397684'
}

flow_colors = {
    'claim': tiktok_colors['magenta'],
    'opinion': tiktok_colors['blue'],
    'not verified': tiktok_colors['pink'],
    'verified': tiktok_colors['aqua']
}

# 3. Create Node Map
# This assigns a unique integer ID to every unique value across your categories
source, target, value, colors, node_labels = [], [], [], [], []
node_map = {}
index = 0

for col in categories:
    for label in df[col].unique():
        node_map[(col, label)] = index
        node_labels.append(str(label).title())
        index += 1

# 4. Generate Flows (Links)
for i in range(len(categories) - 1):
    col1, col2 = categories[i], categories[i + 1]
    flow_data = df.groupby([col1, col2]).size().reset_index(name='count')
    
    for _, row in flow_data.iterrows():
        source.append(node_map[(col1, row[col1])])
        target.append(node_map[(col2, row[col2])])
        value.append(row['count'])
        
        # Color logic based on status
        if col2 == 'author_ban_status':
            if row[col2] == 'under review':
                colors.append('#FFA500') 
            elif row[col2] == 'banned':
                colors.append('#8B0000') 
            else:
                colors.append(flow_colors.get(row[col1], tiktok_colors['gray']))
        else:
            colors.append(flow_colors.get(row[col1], tiktok_colors['gray']))

# 5. Build the Figure
fig = go.Figure(go.Sankey(
    node=dict(
        pad=20, thickness=25,
        line=dict(color=tiktok_colors['black'], width=0.8),
        label=node_labels,
        color=tiktok_colors['gray'],
        hovertemplate='%{label}<extra></extra>'
    ),
    link=dict(
        source=source, target=target, value=value, color=colors,
        hovertemplate='From %{source.label}<br>To %{target.label}<br>Count: %{value}<extra></extra>'
    )
))

# 6. Styling & Layout
fig.update_layout(
    title_text="TikTok Content Journey",
    font_family='Garamond, serif',
    font_size=18,
    font_color=tiktok_colors['white'],
    paper_bgcolor=tiktok_colors['black'],
    plot_bgcolor=tiktok_colors['black'],
    height=720,
    margin=dict(l=30, r=30, b=30, t=50)
)

# 7. Export to HTML
fig.write_html("results/tiktok_sankey.html")
print("Sankey diagram saved as 'tiktok_sankey.html'")