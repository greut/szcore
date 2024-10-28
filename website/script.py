import os
import plotly.graph_objects as go
import pandas as pd
from layout import layout_with_figures
import json, re, sys
from algo_details_script import create_algo_page

github_pages_root_url = "https://esl-epfl.github.io/szcore/"

path_to_eval = sys.argv[1]
path_to_algo_yaml = "./algorithms/"
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
        algo_html = "<a href='" + github_pages_root_url + (re.sub(r'[^a-zA-Z0-9]', '', algo_id)).lower() + ".html'>" + algo_id + "</a>"
        row = {"algo_id": algo_html, "dataset": dataset_name, **sample_results}
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
# os.makedirs("./public", exist_ok=True)
with open("./website/public/index.html", "w") as file:
    file.write(complete_html)

# Create second HTML file for algo details (from yaml)
create_algo_page(path_to_algo_yaml)
