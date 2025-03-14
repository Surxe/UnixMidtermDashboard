# Import parent path
import sys
sys.path.append('..')
import os
import json

data_dir = 'data'

# Get the metrics json file
metrics_path = None
for file in os.listdir(data_dir):
    if file.endswith('.json'):
        metrics_path = os.path.join(data_dir, file)
        break

if metrics_path is None:
    raise FileNotFoundError('No .json file found in data dir, please get and parse metrics before validating')

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
mem_metrics = metrics['Memory']
if mem_metrics['Available'] <= available_threshold:
    warnings.append(f"Memory Available is too low: {mem_metrics['Available']} <= {available_threshold}")

# Disk
usage_threshold = 90.0
disk_metrics = metrics['Disk']
usage = float(disk_metrics['Use%'].split('%')[0])
if usage >= usage_threshold:
    warnings.append(f"Disk Usage is too high: {usage}% >= {usage_threshold}%")

# Disk IO
cpu_usage_threshold = 95.0
disk_io_metrics = metrics['Disk I/O']
cpu_usage = disk_io_metrics['Percentage of CPU Utilization']
if usage >= cpu_usage_threshold:
    warnings.append(f"Disk IO CPU Usage is too high: {cpu_usage}% >= {cpu_usage_threshold}%")

print(f'Warnings: {warnings}')
