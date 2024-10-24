import plotly.graph_objects as go
import pandas as pd

# Create heatmap data
data = pd.DataFrame({
    'x': ['A', 'B', 'C'],
    'y': ['W', 'X', 'Y'],
    'z': [1, 3, 2]
})

fig = go.Figure(data=go.Heatmap(
    z=data['z'],
    x=data['x'],
    y=data['y'],
    colorscale='Viridis'
))


# Generate the Plotly figure HTML as a string
plotly_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

# Create your custom body section (you can expand this)
custom_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Epilepsy Benchmarks</title>
</head>
<body>

    <h1>Epilepsy Benchmarks</h1>
    <p>Standardising benchmarking procedures across epilepsy models. Datasets, performance scores</p>
    
    <!-- Your plotly heatmap will be inserted here -->
    {plotly_figure}

    <p>Click to sort</p>

</body>
</html>
"""

# Combine the custom HTML and the Plotly figure
complete_html = custom_html.format(plotly_figure=plotly_html)

# Save everything into a single HTML file
with open("index.html", "w") as file:
    file.write(complete_html)
