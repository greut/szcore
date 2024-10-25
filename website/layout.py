def layout_with_figures(graph, datasets):
    dropdown = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Standardised Algorithm Evaluation</title>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
                <style>
                    body {{font-family: Roboto, sans-serif;}}
                </style>
        </head>
        <body>

            <h1>Validation of Epileptic Seizure Detection Algorithms</h1>
            <p><strong>Standardising benchmarking procedures across epilepsy models</strong></p>
            <div>
                <div style="width: 15%; float: left; background: aliceblue;">
                    <label for="datasets">Validation dataset:</label>
                    <div name="datasets" id="datasets">
                        """
    for d in datasets:
        val = d.lower()
        title = d.title()
        temp = f"""
                    <input type="checkbox" id="{val}" name="{val}" checked/>
                    <label for="{val}">{title}</label>
                """
        dropdown += temp
    dropdown += """<br></br>
                    </div>

                    <fieldset>
                        <legend>Performance Metrics</legend>
                        <div>
                            <input type="checkbox" id="sensitivity" name="sensitvity" checked />
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
                    <br></br>
                    <fieldset>
                        <legend>Scoring Type</legend>
                        
                        <div>
                            <input type="checkbox" id="scoringSampleBased" name="scoringSampleBased" value="scoringSampleBased" checked />
                            <label for="scoringSampleBased">Sample-based</label>
                        </div>
                        
                        <div>
                            <input type="checkbox" id="scoringEventBased" name="scoringEventBased" value="scoringEventBased" checked />
                            <label for="scoringEventBased">Event-based</label>
                        </div>
                    </fieldset>
                    <br></br>

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