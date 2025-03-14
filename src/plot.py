# Import parent path
import sys
sys.path.append('..')
import os
import json

import plotly.graph_objects as go
import plotly.subplots as sp

# Open the data dir
data_dir = 'data'

if not os.path.exists(data_dir):
    raise Exception(f"Data directory '{data_dir}' does not exist")


historical_data = dict()
for i in range(1, 4): # [1, 2, 3]
    server_archive_dir = f"{data_dir}/server{i}/archive" # data/archive/serverN
    if not os.path.exists(server_archive_dir):
        os.makedirs(server_archive_dir) 

    # Find the json files for the server
    server_data = {}
    server_name = f"server{i}"
    for file in os.listdir(f"data/{server_name}/archive"):
        print(f"Found file: {file}")
        if file.endswith('.json'):
            # Open the json file
            now_data = None
            with open(f"data/server{i}/archive/{file}", 'r', encoding='utf-8') as f:
                date = file.split('.')[0].split('metrics_')[1] # metrics_<date>.json -> <date>
                now_data = json.load(f)
            if now_data is None:
                raise ValueError('No data found in the metrics file')
            server_data[date] = now_data    
            print(f"Loaded data from {file}")
        historical_data[server_name] = server_data

print(json.dumps(historical_data, indent=4)) #human readable str

transformed_data = dict()
timestamps = dict()
for server_name, server_data in historical_data.items():
    if len(server_data) == 0:
        raise FileNotFoundError(f'Server {server_name} had no .json files found in data dir, please get and parse metrics before plotting')

    # Reformat timestamp from "2025-03-11_23-14-42" to "2025-03-11 23:14:42"
    timestamps[server_name] = [timestamp.replace('_', ' ') for timestamp in list(server_data.keys())]

    # Transform 
        # "2025-03-11_23-14-42": {
        #     "%CPU(s)": {"User": 0.0, "System": 50.0, "Idle": 50.0},
        #     "Memory": {"Total": 969, "Used": 469, "Free": 208}
        # },
        # "2025-03-11_23-14-43": {
        #     "%CPU(s)": {"User": 0.0, "System": 49.0, "Idle": 50.0},
        #     "Memory": {"Total": 700, "Used": 469, "Free": 208}
        # }
    # to
        # {
        #     "%CPU(s)": {"User": [0.0, 0.0], "System": [50.0, 49.0], "Idle": [50.0, 50.0]},
        #     "Memory": {"Total": [969, 700], "Used": [469, 469], "Free": [208, 208]}
        # }

    transformed_data[server_name] = dict()
    for date, data in server_data.items():
        for metrics_category, metrics_data in data.items():
            if metrics_category not in transformed_data[server_name]:
                transformed_data[server_name][metrics_category] = {key: [] for key in metrics_data.keys()}
            for metric_name, metric_values in metrics_data.items():
                # Skip lots of data that isnt needed
                if metrics_category == "Disk":
                    if metric_name not in ["Use%"]:
                        continue
                if metrics_category == "Disk I/O":
                    if metric_name not in ["Percentage of CPU Utilization"]:
                        continue

                transformed_data[server_name][metrics_category][metric_name].append(metric_values)

    print(json.dumps(transformed_data[server_name], indent=4)) #human readable str

    num_rows = len(historical_data) # num servers
    num_cols = len(transformed_data[server_name]) # num metrics categories
    metrics_categories = list(transformed_data[server_name].keys())

subplot_titles = [f'{server_name} - {metrics_category}' for server_name in historical_data.keys() for metrics_category in metrics_categories]

fig = sp.make_subplots(rows=num_rows, cols=num_cols, subplot_titles=subplot_titles)

server_index = 0
for server_name, server_data in transformed_data.items():
    print('DEBUG', list(server_data.keys()))
    server_index += 1 # [1, len(historical_data)]

    metric_category_index = 0
    for metrics_category, metrics_data in server_data.items(): #"%CPU(s)", {"User": [0.0, ..]}
        metric_category_index += 1 # [1, len(transformed_data)]
        for metric_name, metric_values in metrics_data.items():
            print(f"{server_name} {metrics_category} {metric_name}: {metric_values}")
            line_name = f"{server_name} {metrics_category} {metric_name}"
            fig.add_trace(go.Scatter(x=timestamps[server_name], y=metric_values, mode='lines+markers', name=line_name), row=server_index, col=metric_category_index)

fig.show()