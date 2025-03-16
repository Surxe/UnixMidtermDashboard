# UnixMidtermDashboard
Dashboard for a mid term project for a Unix System Administration course

## Overview
Create 3 servers and 1 dashboard api/agent that monitors the servers, displays performance statistics, reboots the servers when they fail, and includes basic notification support.

## Disclaimer
This dashboard is designed to be connected to a GCP Google Cloud Ubuntu VM instance that has [MightBeRaptor/UnixMidtermServer](https://github.com/MightBeRaptor/UnixMidtermServer.git) cloned. The `plot.py` script may not function as expected in other environments and may require alterations for other operating systems.

## Setup
1. `git clone https://github.com/Surxe/UnixMidtermDashboard.git`
2. `cd UnixMidtermDashboard`
3. `pip install plotly` - See `requirements.txt`
4. Setup [MightBeRaptor/UnixMidtermServer](https://github.com/MightBeRaptor/UnixMidtermServer.git)
5. Wait for the crontab to start the server's socket connection

## Starting the dashboard socket
1. `python src/controller.py` - Connects to the servers
2. Every 5 minutes of the dashboard's runtime, it will request the server to retrieve metrics of the server's status. When the dashboard receives them, it will run:
   1. `python src/validate_metrics.py` - Validates the metrics to ensure they do not exceed any arbitrarily set thresholds.
   2. `python src/archive_metrics.py` - Archives all json metrics from `data/serverN/metrics_<timestamp>.json` to `data/serverN/archive/metrics_<timestamp>json`
   3. `python src/plot.py` - Plots the archived metrics from all servers and all timestamps using the `plotly` library.
