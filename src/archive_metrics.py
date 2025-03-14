# Import parent path
import sys
sys.path.append('..')
import os

# Move the json file from /data/serverN to /data/serverN/archive
data_dir = 'data'

if not os.path.exists(data_dir):
    raise Exception(f"Data directory '{data_dir}' does not exist")

for i in range(1, 4): # [1, 2, 3]
    server_dir = f"{data_dir}/server{i}" # data/serverN
    if not os.path.exists(server_dir):
        os.makedirs(server_dir) # Create the server dir

    archive_dir = f"{server_dir}/archive" # data/serverN/archive
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir) # Create the archive subdir

    # Find the json files
    json_file = None
    for file in os.listdir(data_dir):
        if file.endswith('.json'):
            json_file = os.path.join(data_dir, file)

    if json_file is not None:
        new_path = os.path.join(archive_dir, os.path.basename(json_file))
        os.rename(json_file, new_path)
        print(f"Moved {json_file} to {new_path}")