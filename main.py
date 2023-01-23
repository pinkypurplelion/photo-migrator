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


# module imports
import os
import shutil

# This is my path
PATH_RAW = "raw"
PATH_DATA = "data"
PATH_MEDIA = "media"
PATH_FINAL = "final"

FUNCTIONS = [mp4.process_image]

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


print("Modifying images...")
for f in media_files:
    # Will modify JPG files
    if '.jpg' in f.lower() and f + '.json' in data_files:
        jpg.process_image(PATH_MEDIA, PATH_DATA, PATH_FINAL, f)

    if bool([ft for ft in mp4.SUPPORTED_FILE_TYPES if (ft in f.lower())]) and f + '.json' in data_files:
        mp4.process_image(PATH_MEDIA, PATH_DATA, PATH_FINAL, f)

    # if '.heic' in f.lower() and f + '.json' in data_files:
    #     media_data = json.load(open(os.path.join('data', f + '.json'))) # change to data dir for production
    #     exif_dict = piexif.load(os.path.join('media', f)) # change to media dir for production

    #else:
        #print("No match found for:", f)



# for (root, dirs, file) in media_files:
#     for f in file:
#         print(f.split('.')[0] + '.json')
#         for (root, dirs, file) in data_files:
#
#
#         if (f.split('.')[0] + '.json') in data_files:
#             print("Found a match!")
#             # do something
#
#
#
# for (root, dirs, file) in data_files:
#     print()
