def layout_with_figures(graph, datasets):
    dropdown = """<!DOCTYPE html>
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

            <h1>Epilepsy Benchmarks</h1>
            <p>Standardising benchmarking procedures across epilepsy models. Datasets, performance scores</p>
            <div>
                <div style="width: 15%; float: left; background: aliceblue;">
                    <label for="datasets">Choose a dataset:</label>
                    <select name="datasets" id="datasets">
                        """
    for d in datasets:
        val = d.lower()
        title = d.title()
        temp = f"""
                    <option value="{val}">{title}</option>
                """
        dropdown += temp
    dropdown += """
                    </select>

                    <fieldset>
                        <legend>Performance Metrics</legend>
                        <div>
                            <input type="checkbox" id="sensitivity" name="sensitvity" onclick=hideShowColumns() checked />
                            <label for="sensitivity">Sensitvity</label>
                        </div>
                        <div>
                            <input type="checkbox" id="precision" name="precision" checked />
                            <label for="precision">Precision</label>
                        </div>
                        <div>
                            <input type="checkbox" id="f1score" name="f1score" checked />
                            <label for="f1score">F1 Score</label>
                        </div>
                        <div>
                            <input type="checkbox" id="fpRate" name="fpRate" checked />
                            <label for="fpRate">fpRate</label>
                        </div>
                    </fieldset>

                    <fieldset>
                        <legend>Scoring Type</legend>
                        
                        <div>
                            <input type="radio" id="scoringSampleBased" name="scoringType" value="scoringSampleBased" checked />
                            <label for="scoringSampleBased">Sample-based</label>
                        </div>
                        
                        <div>
                            <input type="radio" id="scoringEventBased" name="scoringType" value="scoringEventBased" />
                            <label for="scoringEventBased">Event-based</label>
                        </div>
                    </fieldset>

                </div>
                <div style="margin-left: 15%;">
                    <!-- plotly heatmap will be inserted here -->
                    {graph}
                </div>
            </div>

            <script>
                function hideShowColumns() {{
                    alert("Button clicked! This is a message from JavaScript.");
                }}
            </script>
        </body>
        </html>
    """
    return dropdown.format(graph=graph)