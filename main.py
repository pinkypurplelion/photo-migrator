# Plan:
# 1. Parse the JSON data files in the directory
# 2. Parse the available images in the directory
# 3. If data file & image available, modify image data and move to new directory
# 4. Otherwise, move image/data file to new directory

# Readme:
# the raw files: /raw
#
#
#

import engines.mp4 as mp4
import engines.jpg as jpg
import engines.util as util


# module imports
import os
import shutil

# This is my path
PATH_RAW = "raw"
PATH_DATA = "data"
PATH_MEDIA = "media"
PATH_FINAL = "final"

ENGINES = [mp4, jpg]

# to store files in a list
path_raw_files = os.walk(PATH_RAW)

data_files = []
media_files = []

# Walks the media & data files and adds any existing files
print("Walking the media & data files and adding any existing files")
path_media_files = os.walk(PATH_MEDIA)
path_data_files = os.walk(PATH_DATA)
for (root, dirs, file) in path_media_files:
    for f in file:
        if '.json' in f:
            data_files.append(f)
        else:
            media_files.append(f)

for (root, dirs, file) in path_data_files:
    for f in file:
        if '.json' in f:
            data_files.append(f)
        else:
            media_files.append(f)

print(f"Existing files: data - {len(data_files)}, media - {len(media_files)}")

# Will separate the images and data files into separate folders (PATH_DATA & PATH_MEDIA) from the PATH_RAW directory
print("Separating images and data files...")
for (root, dirs, file) in path_raw_files:
    for f in file:
        if '.zip' in f:
            print("Skipping zip file: ", f)
            continue
        if '.json' in f:
            shutil.move(os.path.join(root, f), os.path.join('data', root.replace('/', '-') + '-' + f))
            data_files.append(root.replace('/', '-') + '-' + f)
        else:
            shutil.move(os.path.join(root, f), os.path.join('media', root.replace('/', '-') + '-' + f))
            media_files.append(root.replace('/', '-') + '-' + f)


# Will process the media files using the provided processing engines
print("Processing media...")
for file in media_files:
    for engine in ENGINES:
        if util.supports_file(file, engine.SUPPORTED_FILE_TYPES, data_files):
            engine.process_image(PATH_MEDIA, PATH_DATA, PATH_FINAL, file)
            break
