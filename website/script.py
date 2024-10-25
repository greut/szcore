import plotly.graph_objects as go
import pandas as pd
from layout import layout_with_figures
import json

path_to_eval = './data/sampleEval.json'
file = open(path_to_eval)

metrics = ["Sensitivity", "Precision", "F1 Score", "fpRate"] # hardcoded

eval = json.load(file)
data_for_df = []
datasets = set()
for entry in eval:
    algo_id = entry["algo_id"]
    for dataset in entry["datasets"]:
        dataset_name = dataset["dataset"]
        datasets.add(dataset_name)
        sample_results = dataset["sample_results"]
        row = {"algo_id": algo_id, "dataset": dataset_name, **sample_results}
        data_for_df.append(row)

df = pd.DataFrame(data_for_df)
headers = ["Algorithm", "Dataset"] + list(df.columns[2:])
table_data = [df[col].tolist() for col in df.columns]
# algorithms = [item["algo_id"] for item in eval]

# Table plot
fig = go.Figure(data=[go.Table(header=dict(values=headers),
    cells=dict(values=table_data))])


# Generate the Plotly figure HTML as a string
plotly_html = fig.to_html(full_html=False, include_plotlyjs='cdn')


# Combine the custom HTML and the Plotly figure
complete_html = layout_with_figures(plotly_html, datasets)

# Save everything into a single HTML file
with open("index.html", "w") as file:
    file.write(complete_html)
