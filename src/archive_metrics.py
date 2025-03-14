# Import parent path
import sys
sys.path.append('..')
import os

# Move the one txt and json file from /data to /data/archive
data_dir = 'data'
archive_dir = 'data/archive'
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

# Find the txt and json files
txt_file = None
json_file = None
for file in os.listdir(data_dir):
    if file.endswith('.txt'):
        txt_file = os.path.join(data_dir, file)
    if file.endswith('.json'):
        json_file = os.path.join(data_dir, file)

if txt_file is None:
    raise FileNotFoundError('No .txt file found in data dir')
if json_file is None:
    raise FileNotFoundError('A txt file exist but a json does not, please parse the data first before archiving')

# Move the files
os.rename(txt_file, os.path.join(archive_dir, os.path.basename(txt_file)))
os.rename(json_file, os.path.join(archive_dir, os.path.basename(json_file)))