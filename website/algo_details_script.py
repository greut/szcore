import yaml
import os, re
def create_algo_page(path):
    for x in os.listdir(path):
        if x.endswith(".yaml"):
            with open(path+x, 'r', encoding="UTF-8") as file:
                data = yaml.safe_load(file)
                algo_id = (re.sub(r'[^a-zA-Z0-9]', '-', data["image"])).lower()
                algo_html = f"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Epilepsy Benchmarks</title>
                    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
                        <style>
                            body {{font-family: Roboto, sans-serif;}}
                        </style>
                </head>
                <body>
                    <h1>{data["title"]}</h1>
                    <p>Image ID: {data["image"]}</p>

                    <h2>Authors:</h2>
                    <p>{', '.join([a['given-names'] + " " + a['family-names'] for a in data["authors"]])}</p>
                    
                    <p>Version: {data["version"]}</p>

                    <p>Date released: {data["date-released"]}</p>

                    <p>License: {data["license"]}</p>

                    <a href="{data["repository"]}">Repository: {data["repository"]}</a>
                    
                    <h2>Abstract:</h2>
                    <p>{data["abstract"]}</p>

                    <h2>Dataset</h2>
                    <p><strong>Title:</strong> {data['Dataset'][0]['title']}</p>
                    <p><strong>License:</strong> <a href="{data['Dataset'][0]['license']}">{data['Dataset'][0]['license']}</a></p>
                    <p><strong>Identifiers:</strong></p>
                    <p>
                        <strong>Description:</strong> {data['Dataset'][0]['identifiers'][0]['description']}<br>
                        <strong>Type:</strong> {data['Dataset'][0]['identifiers'][0]['type']}<br>
                        <strong>Value:</strong> <a href="https://doi.org/{data['Dataset'][0]['identifiers'][0]['value']}">{data['Dataset'][0]['identifiers'][0]['value']}</a>
                    </p>
                </body>
                """

            with open(f"./public/{algo_id}.html", "w", encoding="UTF-8") as file:
                file.write(algo_html)
    return algo_html

