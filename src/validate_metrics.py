# Import parent path
import sys
sys.path.append('..')
import os
import json

data_dir = 'data'

for server_dir in os.listdir(data_dir):
    server_name = server_dir
    server_path = os.path.join(data_dir, server_dir)
   
    # Get the metrics json file
    metrics_path = None
    for file in os.listdir(server_path):
        if not file.endswith('.json'):
            continue

        metrics_path = os.path.join(server_path, file)
        

        # Load the metrics
        metrics = None
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        if metrics is None:
            raise ValueError('No data found in the metrics file')

        # Validate the metrics
        warnings = []

        # Cpu
        idle_threshold = 50.0 #%
        cpu_metrics = metrics['%CPU(s)']
        if cpu_metrics['Idle'] >= idle_threshold:
            warnings.append(f"CPU Idle is too high: {cpu_metrics['Idle']}% >= {idle_threshold}%")

        # Memory
        available_threshold = 10
        mem_metrics = metrics['Memory (MB)']
        if mem_metrics['Available'] <= available_threshold:
            warnings.append(f"Memory Available is too low: {mem_metrics['Available']} <= {available_threshold}")

        # Disk
        usage_threshold = 75.0
        disk_metrics = metrics['Disk']
        usage = float(disk_metrics['Use %'])
        if usage >= usage_threshold:
            warnings.append(f"Disk Usage is too high: {usage}% >= {usage_threshold}%")

        # Disk IO
        cpu_usage_threshold = 95.0
        disk_io_metrics = metrics['Disk I/O']
        cpu_usage = disk_io_metrics['Percentage of CPU Utilization']
        if usage >= cpu_usage_threshold:
            warnings.append(f"Disk IO CPU Usage is too high: {cpu_usage}% >= {cpu_usage_threshold}%")

        print(f"Server '{server_name}' has Warnings: {warnings}")
